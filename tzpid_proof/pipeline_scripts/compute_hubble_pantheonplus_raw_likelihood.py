#!/usr/bin/env python
"""Pantheon+ raw covariance likelihood certificate for the Hubble lane.

Downloads the public Pantheon+SH0ES distance table and STAT+SYS covariance
matrix into an ignored cache, selects the SH0ES Hubble-flow rows, and computes
full-covariance chi-square values for the locked Hubble/Friedmann scenarios.

This is a first raw-likelihood lane.  It intentionally covers Pantheon+ only;
Planck distance priors and DESI BAO covariance tables are separate raw lanes.
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
import urllib.request
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

import numpy as np


RAW_DIR = Path("phase2_checks/raw_data_cache/pantheon_plus")
OUT_DIR = Path("phase2_checks")

DATA_URL = (
    "https://raw.githubusercontent.com/PantheonPlusSH0ES/DataRelease/main/"
    "Pantheon%2B_Data/4_DISTANCES_AND_COVAR/Pantheon%2BSH0ES.dat"
)
COV_URL = (
    "https://raw.githubusercontent.com/PantheonPlusSH0ES/DataRelease/main/"
    "Pantheon%2B_Data/4_DISTANCES_AND_COVAR/Pantheon%2BSH0ES_STAT%2BSYS.cov"
)
README_URL = (
    "https://raw.githubusercontent.com/PantheonPlusSH0ES/DataRelease/main/"
    "Pantheon%2B_Data/4_DISTANCES_AND_COVAR/README"
)

DATA_PATH = RAW_DIR / "Pantheon+SH0ES.dat"
COV_PATH = RAW_DIR / "Pantheon+SH0ES_STAT+SYS.cov"
README_PATH = RAW_DIR / "README"

CERT_JSON = OUT_DIR / "HUBBLE_PANTHEONPLUS_RAW_LIKELIHOOD_CERTIFICATE.json"
CERT_MD = OUT_DIR / "HUBBLE_PANTHEONPLUS_RAW_LIKELIHOOD_CERTIFICATE.md"
SCENARIO_CSV = OUT_DIR / "HUBBLE_PANTHEONPLUS_RAW_SCENARIO_CHI2.csv"

C_LIGHT_KM_S = 299792.458


@dataclass(frozen=True)
class Scenario:
    name: str
    role: str
    H0: float
    Omega_m: float
    Omega_K: float
    w0: float
    wa: float


SCENARIOS = [
    Scenario(
        name="planck_lambda_cdm_flat",
        role="Locked flat LambdaCDM reference from the CPL scaffold.",
        H0=67.4,
        Omega_m=0.315,
        Omega_K=0.0,
        w0=-1.0,
        wa=0.0,
    ),
    Scenario(
        name="closed_breathing_lambda_cdm",
        role="Closed-enclosure LambdaCDM carrier with small negative curvature.",
        H0=67.4,
        Omega_m=0.315,
        Omega_K=-0.001,
        w0=-1.0,
        wa=0.0,
    ),
    Scenario(
        name="observed_summary_best_fit",
        role="Best-fit summary point from the observed-summary residual certificate.",
        H0=69.15456889642843,
        Omega_m=0.315,
        Omega_K=0.001,
        w0=-0.838,
        wa=-0.6295493277788298,
    ),
    Scenario(
        name="shoes_h0_lambda_cdm_flat",
        role="Local-distance-ladder H0 point with flat LambdaCDM background.",
        H0=73.04,
        Omega_m=0.315,
        Omega_K=0.0,
        w0=-1.0,
        wa=0.0,
    ),
]


def download_if_needed(url: str, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.stat().st_size > 0:
        return
    request = urllib.request.Request(url, headers={"User-Agent": "Codex"})
    with urllib.request.urlopen(request, timeout=120) as response:
        path.write_bytes(response.read())


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_table(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8") as fh:
        reader = csv.DictReader(fh, delimiter=" ", skipinitialspace=True)
        rows = list(reader)
        return reader.fieldnames or [], rows


def read_covariance(path: Path) -> np.ndarray:
    with path.open("r", encoding="utf-8") as fh:
        n = int(fh.readline().strip())
    data = np.loadtxt(path, skiprows=1)
    if data.size != n * n:
        raise ValueError(f"covariance size mismatch: got {data.size}, expected {n*n}")
    return data.reshape((n, n))


def cpl_factor(a: np.ndarray, w0: float, wa: float) -> np.ndarray:
    return np.exp((-3.0 * (1.0 + w0 + wa)) * np.log(a) + 3.0 * wa * (a - 1.0))


def e_z(z: np.ndarray, scenario: Scenario) -> np.ndarray:
    a = 1.0 / (1.0 + z)
    omega_r = 0.000092
    omega_x = 1.0 - omega_r - scenario.Omega_m - scenario.Omega_K
    e2 = (
        omega_r / a**4
        + scenario.Omega_m / a**3
        + scenario.Omega_K / a**2
        + omega_x * cpl_factor(a, scenario.w0, scenario.wa)
    )
    if np.any(e2 <= 0):
        raise ValueError(f"non-positive E(z)^2 for scenario {scenario.name}")
    return np.sqrt(e2)


def cumulative_comoving_distance(z_values: np.ndarray, scenario: Scenario) -> np.ndarray:
    order = np.argsort(z_values)
    sorted_z = z_values[order]
    unique_z, inverse = np.unique(sorted_z, return_inverse=True)
    grid = np.concatenate(([0.0], unique_z))
    inv_e = 1.0 / e_z(grid, scenario)
    integral = np.zeros_like(grid)
    dz = np.diff(grid)
    integral[1:] = np.cumsum(0.5 * dz * (inv_e[:-1] + inv_e[1:]))
    dc_unique = integral[1:]
    dc_sorted = dc_unique[inverse]
    dc = np.empty_like(dc_sorted)
    dc[order] = dc_sorted
    return dc


def distance_modulus(z_values: np.ndarray, scenario: Scenario) -> np.ndarray:
    dc = cumulative_comoving_distance(z_values, scenario)
    omega_k = scenario.Omega_K
    if abs(omega_k) < 1.0e-12:
        transverse = dc
    else:
        sqrt_abs = math.sqrt(abs(omega_k))
        if omega_k > 0:
            transverse = np.sinh(sqrt_abs * dc) / sqrt_abs
        else:
            transverse = np.sin(sqrt_abs * dc) / sqrt_abs
    dl_mpc = (C_LIGHT_KM_S / scenario.H0) * (1.0 + z_values) * transverse
    if np.any(dl_mpc <= 0):
        raise ValueError(f"non-positive luminosity distance for {scenario.name}")
    return 5.0 * np.log10(dl_mpc) + 25.0


def best_additive_offset(residual: np.ndarray, cov: np.ndarray) -> float:
    ones = np.ones_like(residual)
    cov_inv_res = np.linalg.solve(cov, residual)
    cov_inv_ones = np.linalg.solve(cov, ones)
    return float((ones @ cov_inv_res) / (ones @ cov_inv_ones))


def chi2_full_covariance(observed_mu: np.ndarray, model_mu: np.ndarray, cov: np.ndarray) -> dict:
    raw_residual = model_mu - observed_mu
    offset = best_additive_offset(raw_residual, cov)
    residual = raw_residual - offset
    solved = np.linalg.solve(cov, residual)
    chi2 = float(residual @ solved)
    dof = int(observed_mu.size - 1)
    return {
        "chi2": chi2,
        "dof": dof,
        "reduced_chi2": chi2 / dof,
        "best_additive_offset_mag": offset,
        "rms_residual_mag": float(np.sqrt(np.mean(residual**2))),
        "max_abs_residual_mag": float(np.max(np.abs(residual))),
    }


def build_certificate() -> dict:
    download_if_needed(DATA_URL, DATA_PATH)
    download_if_needed(COV_URL, COV_PATH)
    download_if_needed(README_URL, README_PATH)

    header, rows = read_table(DATA_PATH)
    cov = read_covariance(COV_PATH)
    if cov.shape[0] != len(rows):
        raise ValueError(f"data/covariance mismatch: {len(rows)} rows vs {cov.shape}")

    mask = np.array(
        [
            row.get("USED_IN_SH0ES_HF") == "1"
            and float(row["zHD"]) > 0.01
            and float(row["MU_SH0ES"]) > 0
            for row in rows
        ],
        dtype=bool,
    )
    selected_indices = np.where(mask)[0]
    z = np.array([float(rows[i]["zHD"]) for i in selected_indices], dtype=float)
    observed_mu = np.array([float(rows[i]["MU_SH0ES"]) for i in selected_indices], dtype=float)
    selected_cov = cov[np.ix_(selected_indices, selected_indices)]

    eigenvalues = np.linalg.eigvalsh(selected_cov)
    scenario_results = []
    for scenario in SCENARIOS:
        model_mu = distance_modulus(z, scenario)
        stats = chi2_full_covariance(observed_mu, model_mu, selected_cov)
        scenario_results.append({**asdict(scenario), **stats, "status": "computed"})

    positive_cov = bool(np.min(eigenvalues) > 0)
    finite_results = all(math.isfinite(row["chi2"]) for row in scenario_results)
    best = min(scenario_results, key=lambda row: row["chi2"])
    return {
        "certificate": "HUBBLE_PANTHEONPLUS_RAW_LIKELIHOOD_CERTIFICATE",
        "generated_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "creator": "Daniel Alexander Trawin",
        "orcid": "https://orcid.org/0009-0001-4630-3715",
        "engine": "Python + numpy",
        "claim_boundary": (
            "Pantheon+ Hubble-flow full-covariance likelihood only; additive "
            "magnitude offset is analytically profiled; not a joint CMB/DESI/SN fit."
        ),
        "source": {
            "repository": "PantheonPlusSH0ES/DataRelease",
            "data_url": DATA_URL,
            "covariance_url": COV_URL,
            "readme_url": README_URL,
            "data_sha256": sha256(DATA_PATH),
            "covariance_sha256": sha256(COV_PATH),
            "readme_sha256": sha256(README_PATH),
        },
        "data_shape": {
            "columns": header,
            "total_rows": len(rows),
            "covariance_rows": int(cov.shape[0]),
            "selected_hubble_flow_rows": int(selected_indices.size),
            "selection": "USED_IN_SH0ES_HF == 1 and zHD > 0.01 and MU_SH0ES > 0",
            "covariance": "STAT+SYS submatrix for selected rows",
            "min_covariance_eigenvalue": float(np.min(eigenvalues)),
            "max_covariance_eigenvalue": float(np.max(eigenvalues)),
        },
        "checks": {
            "downloaded_public_pantheonplus_files": "pass",
            "data_covariance_shape_match": "pass",
            "selected_covariance_positive_definite": "pass" if positive_cov else "fail",
            "finite_full_covariance_chi2": "pass" if finite_results else "fail",
            "scenario_likelihoods_computed": "computed",
        },
        "scenario_results": scenario_results,
        "best_scenario_by_chi2": best["name"],
        "overall_status": "pass" if positive_cov and finite_results else "fail",
    }


def write_outputs(cert: dict) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    CERT_JSON.write_text(json.dumps(cert, indent=2), encoding="utf-8")

    with SCENARIO_CSV.open("w", newline="", encoding="utf-8") as fh:
        fields = [
            "name",
            "role",
            "H0",
            "Omega_m",
            "Omega_K",
            "w0",
            "wa",
            "chi2",
            "dof",
            "reduced_chi2",
            "best_additive_offset_mag",
            "rms_residual_mag",
            "max_abs_residual_mag",
            "status",
        ]
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        writer.writerows({field: row[field] for field in fields} for row in cert["scenario_results"])

    check_rows = "\n".join(
        f"| `{name}` | `{status}` |" for name, status in cert["checks"].items()
    )
    scenario_rows = "\n".join(
        "| {name} | {H0:.8g} | {Omega_K:.8g} | {w0:.8g} | {wa:.8g} | {chi2:.8g} | {dof} | {reduced_chi2:.8g} | {best_additive_offset_mag:.8g} |".format(
            **row
        )
        for row in cert["scenario_results"]
    )
    shape = cert["data_shape"]
    CERT_MD.write_text(
        f"""# Hubble/Pantheon+ Raw Likelihood Certificate

Generated UTC: `{cert["generated_utc"]}`

Creator: Daniel Alexander Trawin

ORCID: https://orcid.org/0009-0001-4630-3715

Engine: `{cert["engine"]}`

Overall status: `{cert["overall_status"]}`

## Claim Boundary

This is the first raw-likelihood lane for the Hubble/Friedmann branch. It uses
the public Pantheon+SH0ES distance table and the full STAT+SYS covariance
submatrix for the selected Hubble-flow rows. It does not yet include Planck
distance priors or DESI BAO covariance tables.

## Data Source

- Repository: `PantheonPlusSH0ES/DataRelease`
- Data: {cert["source"]["data_url"]}
- Covariance: {cert["source"]["covariance_url"]}
- README: {cert["source"]["readme_url"]}
- Data SHA256: `{cert["source"]["data_sha256"]}`
- Covariance SHA256: `{cert["source"]["covariance_sha256"]}`

## Data Shape

```json
{json.dumps(shape, indent=2)}
```

## Checks

| Check | Status |
|---|---|
{check_rows}

## Scenario Full-Covariance Chi-Square

| Scenario | H0 | Omega_K | w0 | wa | Chi2 | DoF | Reduced chi2 | Profiled offset mag |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
{scenario_rows}

Best scenario by chi-square: `{cert["best_scenario_by_chi2"]}`

## Files

- JSON certificate: `phase2_checks/HUBBLE_PANTHEONPLUS_RAW_LIKELIHOOD_CERTIFICATE.json`
- Scenario CSV: `phase2_checks/HUBBLE_PANTHEONPLUS_RAW_SCENARIO_CHI2.csv`
- Raw cache: `phase2_checks/raw_data_cache/pantheon_plus/` (ignored by git)

## Next Use

Add companion raw lanes for Planck/CMB distance priors and DESI DR2 BAO
covariance tables, then combine their chi-square terms with this Pantheon+
likelihood in one joint certificate.
""",
        encoding="utf-8",
    )


def main() -> None:
    cert = build_certificate()
    write_outputs(cert)
    print(f"wrote {CERT_JSON}")
    print(f"wrote {CERT_MD}")
    print(f"wrote {SCENARIO_CSV}")
    print(f"overall_status={cert['overall_status']}")
    print(f"selected_hubble_flow_rows={cert['data_shape']['selected_hubble_flow_rows']}")
    print(f"best_scenario_by_chi2={cert['best_scenario_by_chi2']}")


if __name__ == "__main__":
    main()
