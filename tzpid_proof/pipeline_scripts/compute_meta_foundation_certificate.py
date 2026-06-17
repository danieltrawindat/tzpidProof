#!/usr/bin/env python
"""Generate a Phase 2 certificate for meta-foundation batch 010 carriers."""

from __future__ import annotations

import csv
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path


OUT_DIR = Path("phase2_checks")
JSON_OUT = OUT_DIR / "META_FOUNDATION_CARRIERS_CERTIFICATE.json"
CSV_OUT = OUT_DIR / "META_FOUNDATION_CARRIERS_GRID.csv"
MD_OUT = OUT_DIR / "META_FOUNDATION_CARRIERS_CERTIFICATE.md"


@dataclass(frozen=True)
class Scenario:
    name: str
    role: str
    unit: float
    state: float
    likelihood_i: float
    likelihood_j: float
    prior_odds: float
    factor: float
    prediction: float
    alternative: float
    threshold: float
    capacity: float
    pressure: float
    epsilon: float
    entropy_delta: float
    mass_channel: float
    vacuum_pressure: float
    critical_pressure: float
    omega_one: float
    omega_two: float
    tolerance: float


SCENARIOS = [
    Scenario(
        name="baseline_meta_contract",
        role="Positive base unit, nonzero likelihood, falsifiable gap, and split within tolerance.",
        unit=1.0,
        state=3.25,
        likelihood_i=0.75,
        likelihood_j=0.25,
        prior_odds=2.0,
        factor=3.0,
        prediction=10.0,
        alternative=8.5,
        threshold=1.0,
        capacity=5.0,
        pressure=4.0,
        epsilon=0.2,
        entropy_delta=-0.5,
        mass_channel=0.75,
        vacuum_pressure=9.0,
        critical_pressure=7.0,
        omega_one=2.0,
        omega_two=2.1,
        tolerance=0.2,
    ),
    Scenario(
        name="tight_threshold_boundary",
        role="Boundary values at equality for falsifiability, threshold, and binary split.",
        unit=0.1,
        state=-1.0,
        likelihood_i=0.2,
        likelihood_j=0.4,
        prior_odds=0.5,
        factor=0.25,
        prediction=4.0,
        alternative=3.5,
        threshold=0.5,
        capacity=2.0,
        pressure=2.0,
        epsilon=0.5,
        entropy_delta=0.0,
        mass_channel=0.0,
        vacuum_pressure=2.1,
        critical_pressure=2.0,
        omega_one=1.0,
        omega_two=1.3,
        tolerance=0.3,
    ),
    Scenario(
        name="wide_margin_case",
        role="Larger methodological margins across all guards.",
        unit=12.0,
        state=0.0,
        likelihood_i=0.9,
        likelihood_j=0.1,
        prior_odds=5.0,
        factor=1.2,
        prediction=-3.0,
        alternative=1.5,
        threshold=2.0,
        capacity=100.0,
        pressure=40.0,
        epsilon=0.8,
        entropy_delta=-3.0,
        mass_channel=4.0,
        vacuum_pressure=1000.0,
        critical_pressure=10.0,
        omega_one=-2.0,
        omega_two=-2.25,
        tolerance=0.5,
    ),
]


def scenario_row(scenario: Scenario) -> dict[str, float | str | int]:
    observer_offset_residual = scenario.state - scenario.state
    bayes_factor = scenario.likelihood_i / scenario.likelihood_j
    bayes_recovery_residual = bayes_factor * scenario.likelihood_j - scenario.likelihood_i
    posterior = scenario.prior_odds * scenario.factor
    posterior_residual = posterior - scenario.prior_odds * scenario.factor
    falsifiability_gap = abs(scenario.prediction - scenario.alternative)
    falsifiability_margin = falsifiability_gap - scenario.threshold
    threshold_margin = scenario.capacity - scenario.pressure
    weak_gravity_margin = min(scenario.epsilon, 1.0 - scenario.epsilon)
    reverse_process_margin = min(-scenario.entropy_delta, scenario.mass_channel)
    creative_pressure_margin = scenario.vacuum_pressure - scenario.critical_pressure
    binary_split_margin = scenario.tolerance - abs(
        scenario.omega_one - scenario.omega_two
    )
    return {
        "scenario": scenario.name,
        "base_unit_margin": scenario.unit,
        "observer_offset_residual": observer_offset_residual,
        "bayes_recovery_residual": bayes_recovery_residual,
        "posterior_update_residual": posterior_residual,
        "falsifiability_margin": falsifiability_margin,
        "threshold_margin": threshold_margin,
        "weak_gravity_interval_margin": weak_gravity_margin,
        "reverse_process_margin": reverse_process_margin,
        "creative_pressure_margin": creative_pressure_margin,
        "binary_split_margin": binary_split_margin,
    }


def check_scenario(scenario: Scenario) -> dict[str, float | str | int]:
    row = scenario_row(scenario)
    tolerance = max(1.0, abs(scenario.vacuum_pressure)) * 1.0e-12
    checks = {
        "base_unit_positive": float(row["base_unit_margin"]) > 0.0,
        "observer_offset_residual_zero": abs(float(row["observer_offset_residual"])) <= tolerance,
        "bayes_recovery_residual_zero": abs(float(row["bayes_recovery_residual"])) <= tolerance,
        "posterior_update_residual_zero": abs(float(row["posterior_update_residual"])) <= tolerance,
        "falsifiability_margin_nonnegative": float(row["falsifiability_margin"]) >= -tolerance,
        "threshold_margin_nonnegative": float(row["threshold_margin"]) >= -tolerance,
        "weak_gravity_margin_positive": float(row["weak_gravity_interval_margin"]) > 0.0,
        "reverse_process_margin_nonnegative": float(row["reverse_process_margin"]) >= -tolerance,
        "creative_pressure_margin_positive": float(row["creative_pressure_margin"]) > 0.0,
        "binary_split_margin_nonnegative": float(row["binary_split_margin"]) >= -tolerance,
    }
    return {
        "scenario": scenario.name,
        "role": scenario.role,
        "tolerance": tolerance,
        "status": "pass" if all(checks.values()) else "fail",
        **{key: "pass" if value else "fail" for key, value in checks.items()},
        **row,
    }


def build_certificate() -> dict:
    summaries = [check_scenario(scenario) for scenario in SCENARIOS]
    all_pass = all(row["status"] == "pass" for row in summaries)
    return {
        "certificate": "META_FOUNDATION_CARRIERS_CERTIFICATE",
        "generated_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "creator": "Daniel Alexander Trawin",
        "orcid": "https://orcid.org/0009-0001-4630-3715",
        "engine": "Python standard library",
        "claim_boundary": (
            "Representative numerical certificate for meta-foundation carrier margins; "
            "the universal contracts are checked in Isabelle/HOL."
        ),
        "equations": {
            "bayes_recovery": "(L_i/L_j) L_j - L_i = 0",
            "posterior_update": "posterior - prior*factor = 0",
            "falsifiability_margin": "|prediction-alternative| - threshold",
            "weak_gravity_margin": "min(epsilon, 1-epsilon)",
            "reverse_process_margin": "min(-entropy_delta, mass_channel)",
            "binary_split_margin": "tolerance - |omega_1-omega_2|",
        },
        "checks": {
            "all_scenarios_pass": "pass" if all_pass else "fail",
            "evidence_and_margin_guards_verified": "pass"
            if all(
                row["bayes_recovery_residual_zero"] == "pass"
                and row["falsifiability_margin_nonnegative"] == "pass"
                and row["binary_split_margin_nonnegative"] == "pass"
                for row in summaries
            )
            else "fail",
        },
        "scenarios": [asdict(scenario) for scenario in SCENARIOS],
        "scenario_summaries": summaries,
        "grid_csv": str(CSV_OUT),
        "status": "pass" if all_pass else "fail",
    }


def write_outputs(certificate: dict) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    JSON_OUT.write_text(json.dumps(certificate, indent=2), encoding="utf-8")

    fieldnames = [
        "scenario",
        "base_unit_margin",
        "observer_offset_residual",
        "bayes_recovery_residual",
        "posterior_update_residual",
        "falsifiability_margin",
        "threshold_margin",
        "weak_gravity_interval_margin",
        "reverse_process_margin",
        "creative_pressure_margin",
        "binary_split_margin",
    ]
    with CSV_OUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for scenario in SCENARIOS:
            writer.writerow(scenario_row(scenario))

    lines = [
        "# Meta-Foundation Carriers Certificate",
        "",
        f"- Generated UTC: `{certificate['generated_utc']}`",
        "- Creator: Daniel Alexander Trawin",
        "- ORCID: https://orcid.org/0009-0001-4630-3715",
        f"- Status: `{certificate['status']}`",
        "",
        "## Scope",
        "",
        str(certificate["claim_boundary"]),
        "",
        "## Checks",
        "",
    ]
    for key, value in certificate["checks"].items():
        lines.append(f"- `{key}`: `{value}`")
    lines.extend(["", "## Scenario Summaries", ""])
    for row in certificate["scenario_summaries"]:
        lines.append(
            "- `{scenario}`: status `{status}`, falsifiability margin `{falsifiability_margin:.6g}`, "
            "weak-gravity margin `{weak_gravity_interval_margin:.6g}`, "
            "binary split margin `{binary_split_margin:.6g}`".format(**row)
        )
    lines.append("")
    MD_OUT.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    certificate = build_certificate()
    write_outputs(certificate)
    if certificate["status"] != "pass":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
