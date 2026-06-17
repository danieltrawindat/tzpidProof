#!/usr/bin/env python
"""Generate a Phase 2 certificate for the matter-creation pressure EoS.

The Isabelle theory ``TZPID_MatterCreation_PressureEoS.thy`` introduces a
local Landau-style pressure carrier

    p(rho) = p0 + a (rho - rho_c)^2
    p'(rho) = 2 a (rho - rho_c)

This script verifies the corresponding numerical behavior over several
scenarios: the derivative vanishes at rho_c, the sampled pressure is never below
p0 when a >= 0, and the sampled minimum occurs at the critical density.
"""

from __future__ import annotations

import csv
import json
import math
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path


OUT_DIR = Path("phase2_checks")
JSON_OUT = OUT_DIR / "MATTER_CREATION_PRESSURE_EOS_CERTIFICATE.json"
CSV_OUT = OUT_DIR / "MATTER_CREATION_PRESSURE_EOS_GRID.csv"
MD_OUT = OUT_DIR / "MATTER_CREATION_PRESSURE_EOS_CERTIFICATE.md"


@dataclass(frozen=True)
class Scenario:
    name: str
    role: str
    p0: float
    curvature_a: float
    rho_c: float
    half_width: float
    samples_each_side: int


SCENARIOS = [
    Scenario(
        name="unit_critical_density",
        role="Unit critical density with positive quadratic pressure curvature.",
        p0=0.0,
        curvature_a=1.0,
        rho_c=1.0,
        half_width=1.0,
        samples_each_side=1000,
    ),
    Scenario(
        name="offset_pressure_floor",
        role="Nonzero pressure floor with broad positive curvature.",
        p0=0.25,
        curvature_a=0.4,
        rho_c=2.5,
        half_width=2.0,
        samples_each_side=1000,
    ),
    Scenario(
        name="sharp_stationary_carrier",
        role="Sharper local pressure well around a small critical density.",
        p0=-0.1,
        curvature_a=3.0,
        rho_c=0.35,
        half_width=0.7,
        samples_each_side=1000,
    ),
]


def pressure(rho: float, p0: float, curvature_a: float, rho_c: float) -> float:
    return p0 + curvature_a * (rho - rho_c) ** 2


def pressure_derivative(rho: float, curvature_a: float, rho_c: float) -> float:
    return 2.0 * curvature_a * (rho - rho_c)


def pressure_grid(scenario: Scenario) -> list[dict[str, float | str]]:
    total_steps = 2 * scenario.samples_each_side
    lo = scenario.rho_c - scenario.half_width
    step = (2.0 * scenario.half_width) / total_steps
    rows: list[dict[str, float | str]] = []
    for index in range(total_steps + 1):
        rho = lo + index * step
        value = pressure(rho, scenario.p0, scenario.curvature_a, scenario.rho_c)
        deriv = pressure_derivative(rho, scenario.curvature_a, scenario.rho_c)
        rows.append(
            {
                "scenario": scenario.name,
                "rho_vac": rho,
                "pressure": value,
                "pressure_derivative": deriv,
                "pressure_gap": value - scenario.p0,
            }
        )
    return rows


def check_scenario(scenario: Scenario) -> dict[str, float | str]:
    rows = pressure_grid(scenario)
    pressures = [float(row["pressure"]) for row in rows]
    derivatives = [float(row["pressure_derivative"]) for row in rows]
    gaps = [float(row["pressure_gap"]) for row in rows]
    rho_values = [float(row["rho_vac"]) for row in rows]
    min_index = min(range(len(rows)), key=lambda idx: pressures[idx])
    min_rho = rho_values[min_index]
    critical_derivative = pressure_derivative(
        scenario.rho_c, scenario.curvature_a, scenario.rho_c
    )
    critical_pressure = pressure(
        scenario.rho_c, scenario.p0, scenario.curvature_a, scenario.rho_c
    )

    derivative_tolerance = 1.0e-12
    pressure_tolerance = max(abs(scenario.p0), 1.0) * 1.0e-12
    grid_step = (2.0 * scenario.half_width) / (2 * scenario.samples_each_side)

    checks = {
        "critical_derivative_zero": abs(critical_derivative) <= derivative_tolerance,
        "critical_pressure_equals_p0": abs(critical_pressure - scenario.p0)
        <= pressure_tolerance,
        "pressure_not_below_p0": min(gaps) >= -pressure_tolerance,
        "sampled_minimum_at_rho_c": abs(min_rho - scenario.rho_c) <= grid_step / 2.0,
        "derivative_changes_sign_across_rho_c": derivatives[0] < 0.0
        and derivatives[-1] > 0.0,
    }

    return {
        "scenario": scenario.name,
        "role": scenario.role,
        "p0": scenario.p0,
        "curvature_a": scenario.curvature_a,
        "rho_c": scenario.rho_c,
        "half_width": scenario.half_width,
        "samples": len(rows),
        "critical_pressure": critical_pressure,
        "critical_derivative": critical_derivative,
        "sampled_min_pressure": min(pressures),
        "sampled_min_rho": min_rho,
        "max_pressure_gap": max(gaps),
        "min_pressure_gap": min(gaps),
        "grid_step": grid_step,
        "status": "pass" if all(checks.values()) else "fail",
        **{key: "pass" if value else "fail" for key, value in checks.items()},
    }


def build_certificate() -> dict:
    summaries = [check_scenario(scenario) for scenario in SCENARIOS]
    all_pass = all(row["status"] == "pass" for row in summaries)
    return {
        "certificate": "MATTER_CREATION_PRESSURE_EOS_CERTIFICATE",
        "generated_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "creator": "Daniel Alexander Trawin",
        "orcid": "https://orcid.org/0009-0001-4630-3715",
        "engine": "Python standard library",
        "claim_boundary": (
            "Computational certificate for a local quadratic pressure carrier; "
            "not a final physical equation of state."
        ),
        "equations": {
            "pressure": "p(rho_vac) = p0 + a(rho_vac - rho_c)^2",
            "pressure_derivative": "p'(rho_vac) = 2a(rho_vac - rho_c)",
            "stationary_point": "p'(rho_c) = 0",
            "pressure_floor": "p(rho_vac) >= p0 when a >= 0",
        },
        "checks": {
            "all_scenarios_pass": "pass" if all_pass else "fail",
            "stationary_point_verified": "pass"
            if all(row["critical_derivative_zero"] == "pass" for row in summaries)
            else "fail",
            "pressure_floor_verified": "pass"
            if all(row["pressure_not_below_p0"] == "pass" for row in summaries)
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
        "rho_vac",
        "pressure",
        "pressure_derivative",
        "pressure_gap",
    ]
    with CSV_OUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for scenario in SCENARIOS:
            writer.writerows(pressure_grid(scenario))

    lines = [
        "# Matter Creation Pressure EoS Certificate",
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
            "- `{scenario}`: status `{status}`, rho_c `{rho_c:.6g}`, "
            "critical derivative `{critical_derivative:.6g}`, min pressure `{sampled_min_pressure:.6g}`".format(
                **row
            )
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
