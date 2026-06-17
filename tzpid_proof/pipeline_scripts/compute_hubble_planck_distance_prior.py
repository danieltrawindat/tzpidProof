#!/usr/bin/env python
"""Planck 2018 distance-prior likelihood certificate for the Hubble lane.

This compressed CMB lane uses the Planck final-release distance priors from
arXiv:1808.05724.  The script downloads the TeX source into an ignored cache,
verifies the embedded mean vector and inverse covariance values, then computes
the distance-prior chi-square for the locked Hubble/Friedmann scenarios.

This is not the full Planck likelihood.  It is the standard compressed
distance-prior contract over:

    R, l_A, Omega_b h^2
"""

from __future__ import annotations

import hashlib
import json
import math
import re
import tarfile
import urllib.request
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

import numpy as np


RAW_DIR = Path("phase2_checks/raw_data_cache/planck_distance_prior")
OUT_DIR = Path("phase2_checks")

ARXIV_EPRINT_URL = "https://arxiv.org/e-print/1808.05724"
SOURCE_TAR = RAW_DIR / "1808.05724.tar"
SOURCE_DIR = RAW_DIR / "source"
TEX_PATH = SOURCE_DIR / "distance-priors-2018.tex"

CERT_JSON = OUT_DIR / "HUBBLE_PLANCK_DISTANCE_PRIOR_CERTIFICATE.json"
CERT_MD = OUT_DIR / "HUBBLE_PLANCK_DISTANCE_PRIOR_CERTIFICATE.md"
SCENARIO_CSV = OUT_DIR / "HUBBLE_PLANCK_DISTANCE_PRIOR_SCENARIO_CHI2.csv"

C_LIGHT_KM_S = 299792.458
TCMB = 2.7255
N_EFF = 3.046
OMEGA_GAMMA_H2 = 2.469e-5 * (TCMB / 2.725) ** 4
OMEGA_R_H2 = OMEGA_GAMMA_H2 * (1.0 + 0.22710731766 * N_EFF)

PLANCK_MEAN = np.array([1.750235, 301.4707, 0.02235976], dtype=float)
PLANCK_INVCOV = np.array(
    [
        [94392.3971, -1360.4913, 1664517.2916],
        [-1360.4913, 161.4349, 3671.6180],
        [1664517.2916, 3671.6180, 79719182.5162],
    ],
    dtype=float,
)


@dataclass(frozen=True)
class Scenario:
    name: str
    role: str
    H0: float
    Omega_m: float
    Omega_K: float
    w0: float
    wa: float
    omega_b_h2: float = 0.02235976


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


def extract_source() -> None:
    if TEX_PATH.exists():
        return
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    with tarfile.open(SOURCE_TAR) as tar:
        tar.extractall(SOURCE_DIR)


def verify_tex_values() -> dict:
    text = TEX_PATH.read_text(encoding="utf-8", errors="replace")
    expected_literals = {
        "r": "1.750235",
        "la": "301.4707",
        "omegabh2": "0.02235976",
        "invcov_00": "94392.3971",
        "invcov_11": "161.4349",
        "invcov_22": "79719182.5162",
    }
    found = {key: literal in text for key, literal in expected_literals.items()}
    return {
        "all_expected_literals_found": all(found.values()),
        "literal_checks": found,
    }


def cpl_factor(a: np.ndarray | float, w0: float, wa: float) -> np.ndarray | float:
    return np.exp((-3.0 * (1.0 + w0 + wa)) * np.log(a) + 3.0 * wa * (a - 1.0))


def e_a(a: np.ndarray, scenario: Scenario) -> np.ndarray:
    h = scenario.H0 / 100.0
    omega_r = OMEGA_R_H2 / h**2
    omega_x = 1.0 - omega_r - scenario.Omega_m - scenario.Omega_K
    e2 = (
        omega_r / a**4
        + scenario.Omega_m / a**3
        + scenario.Omega_K / a**2
        + omega_x * cpl_factor(a, scenario.w0, scenario.wa)
    )
    if np.any(e2 <= 0):
        raise ValueError(f"non-positive E(a)^2 for {scenario.name}")
    return np.sqrt(e2)


def simpson_integral_grid(x: np.ndarray, y: np.ndarray) -> float:
    # Trapezoidal integration is sufficient on the dense log grids used here.
    if hasattr(np, "trapezoid"):
        return float(np.trapezoid(y, x))
    return float(np.sum(0.5 * np.diff(x) * (y[:-1] + y[1:])))


def z_star(scenario: Scenario) -> float:
    h = scenario.H0 / 100.0
    omega_m_h2 = scenario.Omega_m * h**2
    omega_b_h2 = scenario.omega_b_h2
    g1 = 0.0783 * omega_b_h2 ** (-0.238) / (1.0 + 39.5 * omega_b_h2**0.763)
    g2 = 0.560 / (1.0 + 21.1 * omega_b_h2**1.81)
    return 1048.0 * (1.0 + 0.00124 * omega_b_h2 ** (-0.738)) * (
        1.0 + g1 * omega_m_h2**g2
    )


def comoving_distance_mpc(z: float, scenario: Scenario) -> float:
    # Dense linear grid works well for distance to recombination.
    grid = np.linspace(0.0, z, 30000)
    a = 1.0 / (1.0 + grid)
    integral = simpson_integral_grid(grid, 1.0 / e_a(a, scenario))
    return (C_LIGHT_KM_S / scenario.H0) * integral


def transverse_comoving_distance_mpc(z: float, scenario: Scenario) -> float:
    dc = comoving_distance_mpc(z, scenario)
    dh = C_LIGHT_KM_S / scenario.H0
    ok = scenario.Omega_K
    if abs(ok) < 1.0e-12:
        return dc
    sqrt_abs = math.sqrt(abs(ok))
    x = sqrt_abs * dc / dh
    if ok > 0:
        return dh / sqrt_abs * math.sinh(x)
    return dh / sqrt_abs * math.sin(x)


def sound_horizon_mpc(z: float, scenario: Scenario) -> float:
    h = scenario.H0 / 100.0
    omega_b = scenario.omega_b_h2 / h**2
    omega_gamma = OMEGA_GAMMA_H2 / h**2
    a_star = 1.0 / (1.0 + z)
    # Integrate r_s = c/H0 int_0^a da / [a^2 E(a) sqrt(3(1 + R_b a))].
    u = np.linspace(math.log(1.0e-8), math.log(a_star), 30000)
    a = np.exp(u)
    r_b = 3.0 * omega_b / (4.0 * omega_gamma)
    integrand_u = 1.0 / (a * e_a(a, scenario) * np.sqrt(3.0 * (1.0 + r_b * a)))
    return (C_LIGHT_KM_S / scenario.H0) * simpson_integral_grid(u, integrand_u)


def distance_prior_vector(scenario: Scenario) -> np.ndarray:
    zs = z_star(scenario)
    dm = transverse_comoving_distance_mpc(zs, scenario)
    rs = sound_horizon_mpc(zs, scenario)
    h = scenario.H0 / 100.0
    r_shift = math.sqrt(scenario.Omega_m) * scenario.H0 * dm / C_LIGHT_KM_S
    l_a = math.pi * dm / rs
    return np.array([r_shift, l_a, scenario.omega_b_h2], dtype=float)


def scenario_result(scenario: Scenario) -> dict:
    vector = distance_prior_vector(scenario)
    residual = vector - PLANCK_MEAN
    chi2 = float(residual @ PLANCK_INVCOV @ residual)
    return {
        **asdict(scenario),
        "z_star": z_star(scenario),
        "R": float(vector[0]),
        "l_A": float(vector[1]),
        "omega_b_h2_vector": float(vector[2]),
        "delta_R": float(residual[0]),
        "delta_l_A": float(residual[1]),
        "delta_omega_b_h2": float(residual[2]),
        "chi2": chi2,
        "dof": 3,
        "status": "computed",
    }


def build_certificate() -> dict:
    download_if_needed(ARXIV_EPRINT_URL, SOURCE_TAR)
    extract_source()
    tex_checks = verify_tex_values()
    invcov_eig = np.linalg.eigvalsh(PLANCK_INVCOV)
    scenario_results = [scenario_result(scenario) for scenario in SCENARIOS]
    finite_results = all(math.isfinite(row["chi2"]) for row in scenario_results)
    positive_invcov = bool(np.min(invcov_eig) > 0)
    best = min(scenario_results, key=lambda row: row["chi2"])
    return {
        "certificate": "HUBBLE_PLANCK_DISTANCE_PRIOR_CERTIFICATE",
        "generated_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "creator": "Daniel Alexander Trawin",
        "orcid": "https://orcid.org/0009-0001-4630-3715",
        "engine": "Python + numpy",
        "claim_boundary": "Planck 2018 compressed distance-prior likelihood, not the full Planck likelihood.",
        "source": {
            "arxiv": "1808.05724",
            "url": "https://arxiv.org/abs/1808.05724",
            "eprint_url": ARXIV_EPRINT_URL,
            "source_tar_sha256": sha256(SOURCE_TAR),
            "tex_sha256": sha256(TEX_PATH),
        },
        "planck_distance_prior": {
            "vector_order": ["R", "l_A", "Omega_b h^2"],
            "mean": PLANCK_MEAN.tolist(),
            "inverse_covariance": PLANCK_INVCOV.tolist(),
            "min_inverse_covariance_eigenvalue": float(np.min(invcov_eig)),
            "max_inverse_covariance_eigenvalue": float(np.max(invcov_eig)),
        },
        "checks": {
            "downloaded_arxiv_source": "pass",
            "tex_literals_match_distance_prior_values": "pass"
            if tex_checks["all_expected_literals_found"]
            else "fail",
            "inverse_covariance_positive_definite": "pass" if positive_invcov else "fail",
            "finite_distance_prior_chi2": "pass" if finite_results else "fail",
            "scenario_distance_priors_computed": "computed",
        },
        "tex_checks": tex_checks,
        "scenario_results": scenario_results,
        "best_scenario_by_chi2": best["name"],
        "overall_status": "pass"
        if tex_checks["all_expected_literals_found"] and positive_invcov and finite_results
        else "fail",
    }


def write_outputs(cert: dict) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    CERT_JSON.write_text(json.dumps(cert, indent=2), encoding="utf-8")

    with SCENARIO_CSV.open("w", newline="", encoding="utf-8") as fh:
        fieldnames = [
            "name",
            "role",
            "H0",
            "Omega_m",
            "Omega_K",
            "w0",
            "wa",
            "omega_b_h2",
            "z_star",
            "R",
            "l_A",
            "omega_b_h2_vector",
            "delta_R",
            "delta_l_A",
            "delta_omega_b_h2",
            "chi2",
            "dof",
            "status",
        ]
        writer = __import__("csv").DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows({field: row[field] for field in fieldnames} for row in cert["scenario_results"])

    check_rows = "\n".join(
        f"| `{name}` | `{status}` |" for name, status in cert["checks"].items()
    )
    scenario_rows = "\n".join(
        "| {name} | {H0:.8g} | {Omega_K:.8g} | {w0:.8g} | {wa:.8g} | {R:.8g} | {l_A:.8g} | {chi2:.8g} |".format(
            **row
        )
        for row in cert["scenario_results"]
    )
    CERT_MD.write_text(
        f"""# Hubble/Planck Distance-Prior Certificate

Generated UTC: `{cert["generated_utc"]}`

Creator: Daniel Alexander Trawin

ORCID: https://orcid.org/0009-0001-4630-3715

Engine: `{cert["engine"]}`

Overall status: `{cert["overall_status"]}`

## Claim Boundary

This is a compressed Planck 2018 CMB distance-prior likelihood. It is not the
full Planck likelihood and does not include TT/TE/EE spectra or nuisance
foreground parameters.

## Source

- Paper: Distance Priors from Planck Final Release
- arXiv: https://arxiv.org/abs/1808.05724
- TeX source SHA256: `{cert["source"]["tex_sha256"]}`

## Distance Prior

Vector order: `R`, `l_A`, `Omega_b h^2`

```json
{json.dumps(cert["planck_distance_prior"], indent=2)}
```

## Checks

| Check | Status |
|---|---|
{check_rows}

## Scenario Distance-Prior Chi-Square

| Scenario | H0 | Omega_K | w0 | wa | R | l_A | Chi2 |
|---|---:|---:|---:|---:|---:|---:|---:|
{scenario_rows}

Best scenario by chi-square: `{cert["best_scenario_by_chi2"]}`

## Files

- JSON certificate: `phase2_checks/HUBBLE_PLANCK_DISTANCE_PRIOR_CERTIFICATE.json`
- Scenario CSV: `phase2_checks/HUBBLE_PLANCK_DISTANCE_PRIOR_SCENARIO_CHI2.csv`
- Raw cache: `phase2_checks/raw_data_cache/planck_distance_prior/` (ignored by git)

## Next Use

Add the DESI DR2 BAO covariance likelihood lane, then combine Planck distance
priors, Pantheon+ raw covariance, and DESI BAO into one joint chi-square
certificate.
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
    print(f"best_scenario_by_chi2={cert['best_scenario_by_chi2']}")


if __name__ == "__main__":
    main()
