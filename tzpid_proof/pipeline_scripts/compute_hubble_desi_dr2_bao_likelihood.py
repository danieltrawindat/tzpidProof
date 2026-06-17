#!/usr/bin/env python
"""DESI DR2 BAO covariance likelihood certificate for the Hubble lane.

Downloads the CosmoSIS DESI DR2 BAO module into an ignored cache, extracts the
embedded data vector/covariance recipe, and computes BAO chi-square values for
the locked Hubble/Friedmann scenarios.

This is a compressed BAO distance-ratio lane.  It covers the DESI DR2 Gaussian
BAO measurements only; it is not a full joint cosmological parameter fit.
"""

from __future__ import annotations

import ast
import csv
import hashlib
import json
import math
import urllib.request
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

import numpy as np


RAW_DIR = Path("phase2_checks/raw_data_cache/desi_dr2_bao")
OUT_DIR = Path("phase2_checks")

MODULE_URL = (
    "https://raw.githubusercontent.com/cosmosis-developers/"
    "cosmosis-standard-library/main/likelihood/bao/desi-dr2/desi_dr2.py"
)
YAML_URL = (
    "https://raw.githubusercontent.com/cosmosis-developers/"
    "cosmosis-standard-library/main/likelihood/bao/desi-dr2/module.yaml"
)
MODULE_PATH = RAW_DIR / "desi_dr2.py"
YAML_PATH = RAW_DIR / "module.yaml"

CERT_JSON = OUT_DIR / "HUBBLE_DESI_DR2_BAO_LIKELIHOOD_CERTIFICATE.json"
CERT_MD = OUT_DIR / "HUBBLE_DESI_DR2_BAO_LIKELIHOOD_CERTIFICATE.md"
SCENARIO_CSV = OUT_DIR / "HUBBLE_DESI_DR2_BAO_SCENARIO_CHI2.csv"
MEASUREMENT_CSV = OUT_DIR / "HUBBLE_DESI_DR2_BAO_MEASUREMENTS.csv"

C_LIGHT_KM_S = 299792.458
TCMB = 2.7255
N_EFF = 3.046
OMEGA_GAMMA_H2 = 2.469e-5 * (TCMB / 2.725) ** 4
OMEGA_R_H2 = OMEGA_GAMMA_H2 * (1.0 + 0.22710731766 * N_EFF)


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


def extract_desi_data_sets(path: Path) -> dict:
    module_ast = ast.parse(path.read_text(encoding="utf-8"))
    for node in module_ast.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "DESI_DATA_SETS":
                    return ast.literal_eval(node.value)
    raise ValueError("DESI_DATA_SETS assignment not found")


def default_data_set_names(data_sets: dict) -> list[str]:
    names = list(data_sets.keys())
    for excluded in ("ELG1", "LRG3"):
        names.remove(excluded)
    return names


def build_measurement_vector(data_sets: dict, names: list[str]) -> tuple[list[dict], np.ndarray, np.ndarray]:
    rows: list[dict] = []
    mean: list[float] = []
    cov = np.zeros((13, 13), dtype=float)
    index = 0
    for name in names:
        ds = data_sets[name]
        z_eff = float(ds["z_eff"])
        if ds["kind"] == "d_v":
            rows.append(
                {
                    "dataset": name,
                    "observable": "DV_over_rd",
                    "z_eff": z_eff,
                    "mean": float(ds["mean"]),
                    "sigma": float(ds["sigma"]),
                    "correlation_partner": "",
                    "correlation": "",
                }
            )
            mean.append(float(ds["mean"]))
            cov[index, index] = float(ds["sigma"]) ** 2
            index += 1
        elif ds["kind"] == "d_m_d_h":
            sig_dm, sig_dh = map(float, ds["sigma"])
            corr = float(ds["corr"])
            values = list(map(float, ds["mean"]))
            rows.extend(
                [
                    {
                        "dataset": name,
                        "observable": "DM_over_rd",
                        "z_eff": z_eff,
                        "mean": values[0],
                        "sigma": sig_dm,
                        "correlation_partner": "DH_over_rd",
                        "correlation": corr,
                    },
                    {
                        "dataset": name,
                        "observable": "DH_over_rd",
                        "z_eff": z_eff,
                        "mean": values[1],
                        "sigma": sig_dh,
                        "correlation_partner": "DM_over_rd",
                        "correlation": corr,
                    },
                ]
            )
            mean.extend(values)
            cov[index, index] = sig_dm**2
            cov[index + 1, index + 1] = sig_dh**2
            cov[index, index + 1] = cov[index + 1, index] = corr * sig_dm * sig_dh
            index += 2
        else:
            raise ValueError(f"unknown DESI kind {ds['kind']} for {name}")
    if index != 13:
        raise ValueError(f"expected 13 DESI BAO measurements, got {index}")
    return rows, np.array(mean, dtype=float), cov


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


def trapezoid(x: np.ndarray, y: np.ndarray) -> float:
    if hasattr(np, "trapezoid"):
        return float(np.trapezoid(y, x))
    return float(np.sum(0.5 * np.diff(x) * (y[:-1] + y[1:])))


def z_drag(scenario: Scenario) -> float:
    h = scenario.H0 / 100.0
    omega_m_h2 = scenario.Omega_m * h**2
    omega_b_h2 = scenario.omega_b_h2
    b1 = 0.313 * omega_m_h2 ** (-0.419) * (1.0 + 0.607 * omega_m_h2**0.674)
    b2 = 0.238 * omega_m_h2**0.223
    return (
        1291.0
        * omega_m_h2**0.251
        / (1.0 + 0.659 * omega_m_h2**0.828)
        * (1.0 + b1 * omega_b_h2**b2)
    )


def sound_horizon_drag_mpc(scenario: Scenario) -> float:
    h = scenario.H0 / 100.0
    omega_b = scenario.omega_b_h2 / h**2
    omega_gamma = OMEGA_GAMMA_H2 / h**2
    a_drag = 1.0 / (1.0 + z_drag(scenario))
    u = np.linspace(math.log(1.0e-8), math.log(a_drag), 32000)
    a = np.exp(u)
    r_b = 3.0 * omega_b / (4.0 * omega_gamma)
    integrand_u = 1.0 / (a * e_a(a, scenario) * np.sqrt(3.0 * (1.0 + r_b * a)))
    return (C_LIGHT_KM_S / scenario.H0) * trapezoid(u, integrand_u)


def comoving_distance_mpc(z: float, scenario: Scenario) -> float:
    grid = np.linspace(0.0, z, 12000)
    a = 1.0 / (1.0 + grid)
    return (C_LIGHT_KM_S / scenario.H0) * trapezoid(grid, 1.0 / e_a(a, scenario))


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


def h_z_km_s_mpc(z: float, scenario: Scenario) -> float:
    a = np.array([1.0 / (1.0 + z)], dtype=float)
    return float(scenario.H0 * e_a(a, scenario)[0])


def bao_prediction_vector(measurements: list[dict], scenario: Scenario) -> tuple[np.ndarray, float, float]:
    rd = sound_horizon_drag_mpc(scenario)
    theory: list[float] = []
    for row in measurements:
        z = float(row["z_eff"])
        dm = transverse_comoving_distance_mpc(z, scenario)
        dh = C_LIGHT_KM_S / h_z_km_s_mpc(z, scenario)
        if row["observable"] == "DM_over_rd":
            theory.append(dm / rd)
        elif row["observable"] == "DH_over_rd":
            theory.append(dh / rd)
        elif row["observable"] == "DV_over_rd":
            dv = (z * dm * dm * dh) ** (1.0 / 3.0)
            theory.append(dv / rd)
        else:
            raise ValueError(f"unknown observable {row['observable']}")
    return np.array(theory, dtype=float), rd, z_drag(scenario)


def scenario_result(
    scenario: Scenario, measurements: list[dict], mean: np.ndarray, cov: np.ndarray
) -> dict:
    theory, rd, zd = bao_prediction_vector(measurements, scenario)
    residual = theory - mean
    solved = np.linalg.solve(cov, residual)
    chi2 = float(residual @ solved)
    return {
        **asdict(scenario),
        "z_drag": zd,
        "rd_mpc": rd,
        "chi2": chi2,
        "dof": int(mean.size),
        "reduced_chi2": chi2 / float(mean.size),
        "rms_residual": float(np.sqrt(np.mean(residual**2))),
        "max_abs_residual": float(np.max(np.abs(residual))),
        "status": "computed",
    }


def build_certificate() -> dict:
    download_if_needed(MODULE_URL, MODULE_PATH)
    download_if_needed(YAML_URL, YAML_PATH)

    data_sets = extract_desi_data_sets(MODULE_PATH)
    names = default_data_set_names(data_sets)
    measurements, mean, cov = build_measurement_vector(data_sets, names)
    cov_eig = np.linalg.eigvalsh(cov)
    invcov = np.linalg.inv(cov)
    scenario_results = [scenario_result(scenario, measurements, mean, cov) for scenario in SCENARIOS]
    finite_results = all(math.isfinite(row["chi2"]) for row in scenario_results)
    positive_cov = bool(np.min(cov_eig) > 0.0)
    source_text = MODULE_PATH.read_text(encoding="utf-8", errors="replace")
    source_checks = {
        "contains_desi_data_sets": "DESI_DATA_SETS" in source_text,
        "contains_dr2_arxiv": "2503.14738" in source_text or "2503.14738" in YAML_PATH.read_text(encoding="utf-8", errors="replace"),
        "default_measurement_count_is_13": len(mean) == 13,
        "default_dataset_count_is_7": len(names) == 7,
    }
    best = min(scenario_results, key=lambda row: row["chi2"])
    return {
        "certificate": "HUBBLE_DESI_DR2_BAO_LIKELIHOOD_CERTIFICATE",
        "generated_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "creator": "Daniel Alexander Trawin",
        "orcid": "https://orcid.org/0009-0001-4630-3715",
        "engine": "Python + numpy",
        "claim_boundary": "DESI DR2 Gaussian BAO distance-ratio likelihood, not a full joint cosmological fit.",
        "source": {
            "cosmosis_module_url": MODULE_URL,
            "cosmosis_yaml_url": YAML_URL,
            "module_sha256": sha256(MODULE_PATH),
            "yaml_sha256": sha256(YAML_PATH),
            "desi_dr2_arxiv": "https://arxiv.org/abs/2503.14738",
        },
        "measurement_contract": {
            "dataset_names": names,
            "vector_order": [f"{row['dataset']}:{row['observable']}" for row in measurements],
            "mean": mean.tolist(),
            "covariance": cov.tolist(),
            "inverse_covariance": invcov.tolist(),
            "min_covariance_eigenvalue": float(np.min(cov_eig)),
            "max_covariance_eigenvalue": float(np.max(cov_eig)),
        },
        "checks": {
            "downloaded_cosmosis_module": "pass",
            "parsed_embedded_desi_dataset_table": "pass"
            if source_checks["contains_desi_data_sets"]
            else "fail",
            "source_references_desi_dr2": "pass" if source_checks["contains_dr2_arxiv"] else "fail",
            "default_measurement_shape_matches": "pass"
            if source_checks["default_measurement_count_is_13"] and source_checks["default_dataset_count_is_7"]
            else "fail",
            "covariance_positive_definite": "pass" if positive_cov else "fail",
            "finite_bao_chi2": "pass" if finite_results else "fail",
            "scenario_bao_likelihoods_computed": "computed",
        },
        "source_checks": source_checks,
        "measurements": measurements,
        "scenario_results": scenario_results,
        "best_scenario_by_chi2": best["name"],
        "overall_status": "pass"
        if all(source_checks.values()) and positive_cov and finite_results
        else "fail",
    }


def write_outputs(cert: dict) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    CERT_JSON.write_text(json.dumps(cert, indent=2), encoding="utf-8")

    with MEASUREMENT_CSV.open("w", newline="", encoding="utf-8") as fh:
        fieldnames = [
            "dataset",
            "observable",
            "z_eff",
            "mean",
            "sigma",
            "correlation_partner",
            "correlation",
        ]
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(cert["measurements"])

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
            "z_drag",
            "rd_mpc",
            "chi2",
            "dof",
            "reduced_chi2",
            "rms_residual",
            "max_abs_residual",
            "status",
        ]
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows({field: row[field] for field in fieldnames} for row in cert["scenario_results"])

    check_rows = "\n".join(
        f"| `{name}` | `{status}` |" for name, status in cert["checks"].items()
    )
    measurement_rows = "\n".join(
        "| {dataset} | {observable} | {z_eff:.3f} | {mean:.8g} | {sigma:.8g} | {correlation_partner} | {correlation} |".format(
            **row
        )
        for row in cert["measurements"]
    )
    scenario_rows = "\n".join(
        "| {name} | {H0:.8g} | {Omega_K:.8g} | {w0:.8g} | {wa:.8g} | {rd_mpc:.8g} | {chi2:.8g} | {reduced_chi2:.8g} |".format(
            **row
        )
        for row in cert["scenario_results"]
    )
    CERT_MD.write_text(
        f"""# Hubble/DESI DR2 BAO Certificate

Generated UTC: `{cert["generated_utc"]}`

Creator: Daniel Alexander Trawin

ORCID: https://orcid.org/0009-0001-4630-3715

Engine: `{cert["engine"]}`

Overall status: `{cert["overall_status"]}`

## Claim Boundary

This is a Gaussian DESI DR2 BAO distance-ratio likelihood over `DV/rd`,
`DM/rd`, and `DH/rd`. It is not a full joint cosmological fit.

## Source

- CosmoSIS module: {cert["source"]["cosmosis_module_url"]}
- CosmoSIS metadata: {cert["source"]["cosmosis_yaml_url"]}
- DESI DR2 BAO paper: {cert["source"]["desi_dr2_arxiv"]}
- Module SHA256: `{cert["source"]["module_sha256"]}`

## Checks

| Check | Status |
|---|---|
{check_rows}

## DESI BAO Measurement Vector

| Dataset | Observable | z_eff | Mean | Sigma | Correlation partner | Correlation |
|---|---|---:|---:|---:|---|---:|
{measurement_rows}

## Scenario BAO Chi-Square

| Scenario | H0 | Omega_K | w0 | wa | rd Mpc | Chi2 | Reduced Chi2 |
|---|---:|---:|---:|---:|---:|---:|---:|
{scenario_rows}

Best scenario by chi-square: `{cert["best_scenario_by_chi2"]}`

## Files

- JSON certificate: `phase2_checks/HUBBLE_DESI_DR2_BAO_LIKELIHOOD_CERTIFICATE.json`
- Scenario CSV: `phase2_checks/HUBBLE_DESI_DR2_BAO_SCENARIO_CHI2.csv`
- Measurement CSV: `phase2_checks/HUBBLE_DESI_DR2_BAO_MEASUREMENTS.csv`
- Raw cache: `phase2_checks/raw_data_cache/desi_dr2_bao/` (ignored by git)

## Next Use

Combine DESI DR2 BAO, Planck distance priors, and Pantheon+ raw covariance into
one joint Hubble/Friedmann chi-square certificate.
""",
        encoding="utf-8",
    )


def main() -> None:
    cert = build_certificate()
    write_outputs(cert)
    print(f"wrote {CERT_JSON}")
    print(f"wrote {CERT_MD}")
    print(f"wrote {SCENARIO_CSV}")
    print(f"wrote {MEASUREMENT_CSV}")
    print(f"overall_status={cert['overall_status']}")
    print(f"best_scenario_by_chi2={cert['best_scenario_by_chi2']}")


if __name__ == "__main__":
    main()
