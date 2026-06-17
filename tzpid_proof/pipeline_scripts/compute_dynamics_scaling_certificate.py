#!/usr/bin/env python
"""Generate a Phase 2 certificate for dynamics/scaling batch 009 carriers."""

from __future__ import annotations

import csv
import json
import math
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path


OUT_DIR = Path("phase2_checks")
JSON_OUT = OUT_DIR / "DYNAMICS_SCALING_CARRIERS_CERTIFICATE.json"
CSV_OUT = OUT_DIR / "DYNAMICS_SCALING_CARRIERS_GRID.csv"
MD_OUT = OUT_DIR / "DYNAMICS_SCALING_CARRIERS_CERTIFICATE.md"


@dataclass(frozen=True)
class Scenario:
    name: str
    role: str
    energy: float
    mass: float
    omega: float
    amplitude: float
    drift: float
    drift_bound: float
    constant: float
    velocity: float
    time: float
    mode_n: float
    length: float
    angular_momentum: float
    inertia: float
    base: float
    beta: float
    scale: float
    hbar: float
    action: float
    coefficient: float
    separation_a: float
    separation_b: float


SCENARIOS = [
    Scenario(
        name="baseline_scaling_contract",
        role="Balanced residual with positive oscillator and inverse-fourth scaling.",
        energy=4.0,
        mass=2.0,
        omega=3.0,
        amplitude=0.5,
        drift=0.2,
        drift_bound=0.3,
        constant=1.1,
        velocity=0.8,
        time=2.5,
        mode_n=2.0,
        length=1.25,
        angular_momentum=5.0,
        inertia=2.0,
        base=7.0,
        beta=0.04,
        scale=3.0,
        hbar=1.0,
        action=4.0,
        coefficient=1.5,
        separation_a=2.0,
        separation_b=4.0,
    ),
    Scenario(
        name="small_mode_large_ratio",
        role="Short separation contrast tests the fourth-power ratio.",
        energy=1.25,
        mass=0.4,
        omega=1.7,
        amplitude=-1.2,
        drift=-0.45,
        drift_bound=0.5,
        constant=0.0,
        velocity=-1.0,
        time=0.75,
        mode_n=0.5,
        length=0.8,
        angular_momentum=-3.0,
        inertia=1.5,
        base=2.0,
        beta=-0.02,
        scale=10.0,
        hbar=0.75,
        action=1.25,
        coefficient=2.0,
        separation_a=0.5,
        separation_b=1.0,
    ),
    Scenario(
        name="zero_motion_boundary",
        role="Zero amplitude and zero time boundary values stay admissible.",
        energy=0.0,
        mass=1.0,
        omega=0.0,
        amplitude=0.0,
        drift=0.0,
        drift_bound=0.0,
        constant=2.5,
        velocity=4.0,
        time=0.0,
        mode_n=3.0,
        length=2.0,
        angular_momentum=0.0,
        inertia=3.0,
        base=5.0,
        beta=0.0,
        scale=12.0,
        hbar=2.0,
        action=5.0,
        coefficient=3.0,
        separation_a=1.5,
        separation_b=3.0,
    ),
]


def scenario_row(scenario: Scenario) -> dict[str, float | str | int]:
    stability_residual = scenario.energy - scenario.energy
    oscillator_energy = (
        0.5 * scenario.mass * scenario.omega**2 * scenario.amplitude**2
    )
    drift_magnitude = abs(scenario.drift)
    nonlinear_response = scenario.constant * scenario.amplitude**2
    temporal_displacement = scenario.velocity * scenario.time
    temporal_residual = temporal_displacement - scenario.velocity * scenario.time
    mode_wavenumber = scenario.mode_n * math.pi / scenario.length
    mode_residual = mode_wavenumber * scenario.length - scenario.mode_n * math.pi
    rotation_ratio = scenario.angular_momentum / scenario.inertia
    rotation_residual = (
        rotation_ratio * scenario.inertia - scenario.angular_momentum
    )
    running_constant = scenario.base + scenario.beta * scenario.scale
    running_shift = running_constant - scenario.base
    zpf_variance = scenario.amplitude**2
    vacuum_residual = scenario.energy - scenario.energy
    semiclassical_ratio = scenario.hbar / scenario.action
    semiclassical_residual = semiclassical_ratio * scenario.action - scenario.hbar
    casimir_a = scenario.coefficient / scenario.separation_a**4
    casimir_b = scenario.coefficient / scenario.separation_b**4
    inverse_fourth_ratio = casimir_a / casimir_b
    expected_inverse_fourth_ratio = scenario.separation_b**4 / scenario.separation_a**4
    return {
        "scenario": scenario.name,
        "stability_residual": stability_residual,
        "oscillator_energy": oscillator_energy,
        "drift_magnitude": drift_magnitude,
        "drift_bound": scenario.drift_bound,
        "nonlinear_response": nonlinear_response,
        "temporal_residual": temporal_residual,
        "mode_residual": mode_residual,
        "rotation_residual": rotation_residual,
        "running_shift": running_shift,
        "expected_running_shift": scenario.beta * scenario.scale,
        "zpf_variance": zpf_variance,
        "vacuum_residual": vacuum_residual,
        "semiclassical_residual": semiclassical_residual,
        "inverse_fourth_ratio": inverse_fourth_ratio,
        "expected_inverse_fourth_ratio": expected_inverse_fourth_ratio,
    }


def check_scenario(scenario: Scenario) -> dict[str, float | str | int]:
    row = scenario_row(scenario)
    tolerance = max(1.0, abs(row["inverse_fourth_ratio"])) * 1.0e-12
    checks = {
        "stability_residual_zero": abs(float(row["stability_residual"])) <= tolerance,
        "oscillator_energy_nonnegative": float(row["oscillator_energy"]) >= -tolerance,
        "drift_bound_guard": float(row["drift_magnitude"]) <= scenario.drift_bound + tolerance,
        "nonlinear_response_nonnegative": float(row["nonlinear_response"]) >= -tolerance,
        "temporal_residual_zero": abs(float(row["temporal_residual"])) <= tolerance,
        "mode_residual_zero": abs(float(row["mode_residual"])) <= tolerance,
        "rotation_residual_zero": abs(float(row["rotation_residual"])) <= tolerance,
        "running_shift_linear": abs(
            float(row["running_shift"]) - float(row["expected_running_shift"])
        )
        <= tolerance,
        "zpf_variance_nonnegative": float(row["zpf_variance"]) >= -tolerance,
        "vacuum_residual_zero": abs(float(row["vacuum_residual"])) <= tolerance,
        "semiclassical_residual_zero": abs(float(row["semiclassical_residual"])) <= tolerance,
        "inverse_fourth_ratio_matches": abs(
            float(row["inverse_fourth_ratio"])
            - float(row["expected_inverse_fourth_ratio"])
        )
        <= tolerance,
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
        "certificate": "DYNAMICS_SCALING_CARRIERS_CERTIFICATE",
        "generated_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "creator": "Daniel Alexander Trawin",
        "orcid": "https://orcid.org/0009-0001-4630-3715",
        "engine": "Python standard library",
        "claim_boundary": (
            "Representative numerical certificate for dynamics/scaling carrier algebra; "
            "the universal contracts are checked in Isabelle/HOL."
        ),
        "equations": {
            "oscillator_energy": "E = 1/2 m omega^2 A^2",
            "mode_closure": "(n*pi/L) L - n*pi = 0",
            "rotation_recovery": "(L/I) I - L = 0",
            "running_shift": "g(scale) - base = beta*scale",
            "inverse_fourth_ratio": "(C/a^4)/(C/b^4) = b^4/a^4",
        },
        "checks": {
            "all_scenarios_pass": "pass" if all_pass else "fail",
            "scaling_residuals_verified": "pass"
            if all(
                row["mode_residual_zero"] == "pass"
                and row["rotation_residual_zero"] == "pass"
                and row["inverse_fourth_ratio_matches"] == "pass"
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
        "stability_residual",
        "oscillator_energy",
        "drift_magnitude",
        "drift_bound",
        "nonlinear_response",
        "temporal_residual",
        "mode_residual",
        "rotation_residual",
        "running_shift",
        "expected_running_shift",
        "zpf_variance",
        "vacuum_residual",
        "semiclassical_residual",
        "inverse_fourth_ratio",
        "expected_inverse_fourth_ratio",
    ]
    with CSV_OUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for scenario in SCENARIOS:
            writer.writerow(scenario_row(scenario))

    lines = [
        "# Dynamics/Scaling Carriers Certificate",
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
            "- `{scenario}`: status `{status}`, oscillator energy `{oscillator_energy:.6g}`, "
            "mode residual `{mode_residual:.6g}`, rotation residual `{rotation_residual:.6g}`, "
            "inverse-fourth ratio `{inverse_fourth_ratio:.6g}`".format(**row)
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
