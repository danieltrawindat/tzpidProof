#!/usr/bin/env python
"""Observed-summary residual scaffold for the Hubble/Friedmann CPL lane.

This is intentionally a summary-constraint fit, not a raw CMB/BAO/SN
likelihood.  Each row is a published parameter constraint with a symmetric
one-sigma approximation.  The certificate computes normalized residuals for
the locked scenarios and a diagonal weighted least-squares parameter summary
over:

    H0, Omega_m, Omega_K, w0, wa

The purpose is to make the next proof/certificate layer concrete and
reproducible while keeping the claim boundary explicit.
"""

from __future__ import annotations

import csv
import json
import math
from collections import defaultdict
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path


OUT_DIR = Path("phase2_checks")
OBSERVED_CSV = OUT_DIR / "HUBBLE_FRIEDMANN_OBSERVED_SUMMARY_CONSTRAINTS.csv"
FIT_JSON = OUT_DIR / "HUBBLE_FRIEDMANN_OBSERVED_FIT_CERTIFICATE.json"
FIT_MD = OUT_DIR / "HUBBLE_FRIEDMANN_OBSERVED_FIT_CERTIFICATE.md"


@dataclass(frozen=True)
class ObservedConstraint:
    probe: str
    source: str
    source_url: str
    parameter: str
    observed_value: float
    sigma: float
    note: str


@dataclass(frozen=True)
class Scenario:
    name: str
    role: str
    H0: float
    Omega_m: float
    Omega_K: float
    w0: float
    wa: float


OBSERVED_CONSTRAINTS = [
    ObservedConstraint(
        probe="CMB",
        source="Planck 2018 VI base-LambdaCDM",
        source_url="https://arxiv.org/abs/1807.06209",
        parameter="H0",
        observed_value=67.4,
        sigma=0.5,
        note="Planck base-LambdaCDM H0 = 67.4 +/- 0.5 km/s/Mpc.",
    ),
    ObservedConstraint(
        probe="CMB",
        source="Planck 2018 VI base-LambdaCDM",
        source_url="https://arxiv.org/abs/1807.06209",
        parameter="Omega_m",
        observed_value=0.315,
        sigma=0.007,
        note="Planck base-LambdaCDM Omega_m = 0.315 +/- 0.007.",
    ),
    ObservedConstraint(
        probe="CMB+BAO",
        source="Planck 2018 VI joint curvature constraint",
        source_url="https://www.aanda.org/articles/aa/abs/2020/09/aa33910-18/aa33910-18.html",
        parameter="Omega_K",
        observed_value=0.001,
        sigma=0.002,
        note="Planck+BAO curvature constraint is consistent with flatness, Omega_K about 0.001 +/- 0.002.",
    ),
    ObservedConstraint(
        probe="SN distance ladder",
        source="SH0ES 2022",
        source_url="https://ui.adsabs.harvard.edu/abs/2022ApJ...934L...7R/abstract",
        parameter="H0",
        observed_value=73.04,
        sigma=1.04,
        note="Cepheid-SN Ia distance ladder baseline H0 = 73.04 +/- 1.04 km/s/Mpc.",
    ),
    ObservedConstraint(
        probe="SN+Cepheid",
        source="Pantheon+ with SH0ES",
        source_url="https://arxiv.org/abs/2202.04077",
        parameter="H0",
        observed_value=73.3,
        sigma=1.1,
        note="Pantheon+ including SH0ES reports H0 = 73.3 +/- 1.1 km/s/Mpc.",
    ),
    ObservedConstraint(
        probe="DESI DR2+CMB+Pantheon+",
        source="DESI DR2 summary constraint",
        source_url="https://academic.oup.com/nsr/article/13/10/nwag115/8497412",
        parameter="w0",
        observed_value=-0.838,
        sigma=0.055,
        note="Published summary gives w0 = -0.838 +/- 0.055 for DESI+CMB+Pantheon+.",
    ),
    ObservedConstraint(
        probe="DESI DR2+CMB+Pantheon+",
        source="DESI DR2 summary constraint",
        source_url="https://academic.oup.com/nsr/article/13/10/nwag115/8497412",
        parameter="wa",
        observed_value=-0.62,
        sigma=0.205,
        note="Symmetric approximation to wa = -0.62 +0.22/-0.19.",
    ),
    ObservedConstraint(
        probe="Pantheon+ CMB+BAO",
        source="Pantheon+ cosmological constraints",
        source_url="https://arxiv.org/abs/2202.04077",
        parameter="wa",
        observed_value=-0.65,
        sigma=0.30,
        note="Symmetric approximation to wa = -0.65 +0.28/-0.32 from Pantheon+ with CMB and BAO.",
    ),
]


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
        name="dynamic_cpl_demo",
        role="Prior non-fit CPL demonstration point.",
        H0=67.4,
        Omega_m=0.315,
        Omega_K=0.0,
        w0=-0.95,
        wa=0.2,
    ),
]


def scenario_value(scenario: Scenario, parameter: str) -> float:
    return getattr(scenario, parameter)


def residual_row(scenario: Scenario, constraint: ObservedConstraint) -> dict:
    model_value = scenario_value(scenario, constraint.parameter)
    residual = model_value - constraint.observed_value
    pull = residual / constraint.sigma
    return {
        "scenario": scenario.name,
        "probe": constraint.probe,
        "source": constraint.source,
        "parameter": constraint.parameter,
        "model_value": model_value,
        "observed_value": constraint.observed_value,
        "sigma": constraint.sigma,
        "residual": residual,
        "pull_sigma": pull,
        "chi2": pull * pull,
    }


def fit_parameter_summaries() -> dict[str, dict]:
    grouped: dict[str, list[ObservedConstraint]] = defaultdict(list)
    for constraint in OBSERVED_CONSTRAINTS:
        grouped[constraint.parameter].append(constraint)

    summaries = {}
    for parameter, rows in grouped.items():
        weight_sum = sum(1.0 / (row.sigma * row.sigma) for row in rows)
        weighted_value = sum(row.observed_value / (row.sigma * row.sigma) for row in rows) / weight_sum
        sigma = math.sqrt(1.0 / weight_sum)
        chi2 = sum(((weighted_value - row.observed_value) / row.sigma) ** 2 for row in rows)
        dof = max(0, len(rows) - 1)
        summaries[parameter] = {
            "parameter": parameter,
            "fit_value": weighted_value,
            "fit_sigma": sigma,
            "constraint_count": len(rows),
            "chi2": chi2,
            "dof": dof,
            "reduced_chi2": chi2 / dof if dof else None,
            "status": "computed",
        }
    return summaries


def build_certificate() -> dict:
    residuals = [residual_row(s, c) for s in SCENARIOS for c in OBSERVED_CONSTRAINTS]
    scenario_totals = {}
    for scenario in SCENARIOS:
        rows = [row for row in residuals if row["scenario"] == scenario.name]
        chi2 = sum(row["chi2"] for row in rows)
        dof = len(rows)
        scenario_totals[scenario.name] = {
            "scenario": scenario.name,
            "chi2": chi2,
            "dof": dof,
            "reduced_chi2": chi2 / dof if dof else None,
            "max_abs_pull_sigma": max(abs(row["pull_sigma"]) for row in rows),
            "status": "computed",
        }

    parameter_fit = fit_parameter_summaries()
    best_fit_point = {
        "H0": parameter_fit["H0"]["fit_value"],
        "Omega_m": parameter_fit["Omega_m"]["fit_value"],
        "Omega_K": parameter_fit["Omega_K"]["fit_value"],
        "w0": parameter_fit["w0"]["fit_value"],
        "wa": parameter_fit["wa"]["fit_value"],
    }
    finite_checks = all(
        math.isfinite(row["chi2"]) and math.isfinite(row["pull_sigma"]) for row in residuals
    )
    sigma_checks = all(row.sigma > 0 for row in OBSERVED_CONSTRAINTS)
    coverage_checks = {"H0", "Omega_m", "Omega_K", "w0", "wa"} <= set(parameter_fit)
    return {
        "certificate": "HUBBLE_FRIEDMANN_OBSERVED_FIT_CERTIFICATE",
        "generated_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "creator": "Daniel Alexander Trawin",
        "orcid": "https://orcid.org/0009-0001-4630-3715",
        "engine": "Python standard library",
        "claim_boundary": (
            "Published summary-constraint residual scaffold; not a raw likelihood "
            "and not a full covariance cosmology fit."
        ),
        "observed_constraints": [asdict(row) for row in OBSERVED_CONSTRAINTS],
        "scenarios": [asdict(row) for row in SCENARIOS],
        "residuals": residuals,
        "scenario_totals": scenario_totals,
        "parameter_fit": parameter_fit,
        "best_fit_point": best_fit_point,
        "checks": {
            "positive_uncertainties": "pass" if sigma_checks else "fail",
            "finite_residuals": "pass" if finite_checks else "fail",
            "parameter_coverage_H0_Omega_m_Omega_K_w0_wa": "pass" if coverage_checks else "fail",
            "summary_fit_computed": "computed",
        },
        "overall_status": "pass" if sigma_checks and finite_checks and coverage_checks else "fail",
    }


def write_outputs(cert: dict) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OBSERVED_CSV.write_text("", encoding="utf-8")
    with OBSERVED_CSV.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(asdict(OBSERVED_CONSTRAINTS[0]).keys()))
        writer.writeheader()
        writer.writerows(asdict(row) for row in OBSERVED_CONSTRAINTS)

    FIT_JSON.write_text(json.dumps(cert, indent=2), encoding="utf-8")

    check_rows = "\n".join(
        f"| `{name}` | `{status}` |" for name, status in cert["checks"].items()
    )
    fit_rows = "\n".join(
        "| {parameter} | {fit_value:.8g} | {fit_sigma:.8g} | {constraint_count} | {chi2:.8g} | {dof} | {reduced} |".format(
            parameter=row["parameter"],
            fit_value=row["fit_value"],
            fit_sigma=row["fit_sigma"],
            constraint_count=row["constraint_count"],
            chi2=row["chi2"],
            dof=row["dof"],
            reduced="n/a" if row["reduced_chi2"] is None else f"{row['reduced_chi2']:.8g}",
        )
        for row in cert["parameter_fit"].values()
    )
    scenario_rows = "\n".join(
        "| {scenario} | {chi2:.8g} | {dof} | {reduced_chi2:.8g} | {max_abs_pull_sigma:.8g} |".format(
            **row
        )
        for row in cert["scenario_totals"].values()
    )
    constraint_rows = "\n".join(
        "| {probe} | {parameter} | {observed_value:.8g} | {sigma:.8g} | {source} |".format(
            **row
        )
        for row in cert["observed_constraints"]
    )
    source_lines = "\n".join(
        f"- {row['source']}: {row['source_url']}" for row in cert["observed_constraints"]
    )
    FIT_MD.write_text(
        f"""# Hubble/Friedmann Observed-Fit Certificate

Generated UTC: `{cert["generated_utc"]}`

Creator: Daniel Alexander Trawin

ORCID: https://orcid.org/0009-0001-4630-3715

Engine: `{cert["engine"]}`

Overall status: `{cert["overall_status"]}`

## Claim Boundary

This is a published-summary residual scaffold. It is not a raw likelihood and
does not include covariance matrices. It turns the prior CPL parameter anchor
lane into a concrete observed-data residual lane over `H0`, `Omega_m`,
`Omega_K`, `w0`, and `wa`.

## Checks

| Check | Status |
|---|---|
{check_rows}

## Observed Summary Constraints

| Probe | Parameter | Observed | Sigma | Source |
|---|---|---:|---:|---|
{constraint_rows}

## Diagonal Weighted Parameter Summary

| Parameter | Fit value | Fit sigma | Constraints | Chi2 | DoF | Reduced chi2 |
|---|---:|---:|---:|---:|---:|---:|
{fit_rows}

## Locked Scenario Residuals

| Scenario | Chi2 | DoF | Reduced chi2 | Max abs pull sigma |
|---|---:|---:|---:|---:|
{scenario_rows}

## Best-Fit Summary Point

```json
{json.dumps(cert["best_fit_point"], indent=2)}
```

## Sources

{source_lines}

## Files

- Observed constraints: `phase2_checks/HUBBLE_FRIEDMANN_OBSERVED_SUMMARY_CONSTRAINTS.csv`
- Certificate JSON: `phase2_checks/HUBBLE_FRIEDMANN_OBSERVED_FIT_CERTIFICATE.json`

## Next Use

Replace these diagonal summary constraints with raw CMB distance priors, DESI
BAO distance-ratio covariance tables, and Pantheon+ supernova likelihood data.
That will promote this from a summary residual scaffold into a true joint
likelihood lane.
""",
        encoding="utf-8",
    )


def main() -> None:
    cert = build_certificate()
    write_outputs(cert)
    print(f"wrote {OBSERVED_CSV}")
    print(f"wrote {FIT_JSON}")
    print(f"wrote {FIT_MD}")
    print(f"overall_status={cert['overall_status']}")


if __name__ == "__main__":
    main()
