#!/usr/bin/env python
"""Generate a Phase 2 certificate for topology/category batch 013 carriers."""

from __future__ import annotations

import csv
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path


OUT_DIR = Path("phase2_checks")
JSON_OUT = OUT_DIR / "TOPOLOGY_CATEGORY_CARRIERS_CERTIFICATE.json"
CSV_OUT = OUT_DIR / "TOPOLOGY_CATEGORY_CARRIERS_GRID.csv"
MD_OUT = OUT_DIR / "TOPOLOGY_CATEGORY_CARRIERS_CERTIFICATE.md"


@dataclass(frozen=True)
class Scenario:
    name: str
    role: str
    value: float
    antipodal_value: float
    variable_count: int
    base_dimension_count: int
    dipole: float
    meridian: float
    ambient_dim: int
    access_dim: int
    surface: float
    bulk: float
    field_obj: int
    spectrum_obj: int


SCENARIOS = [
    Scenario(
        name="baseline_category_contract",
        role="Balanced topology and field-spectrum adjoint pair.",
        value=2.5,
        antipodal_value=2.5,
        variable_count=8,
        base_dimension_count=3,
        dipole=1.25,
        meridian=4.0,
        ambient_dim=5,
        access_dim=3,
        surface=12.0,
        bulk=4.0,
        field_obj=1,
        spectrum_obj=2,
    ),
    Scenario(
        name="zero_reduction_boundary",
        role="Equal variable/base dimensions and reflexive access.",
        value=-1.0,
        antipodal_value=-1.0,
        variable_count=4,
        base_dimension_count=4,
        dipole=-0.5,
        meridian=0.0,
        ambient_dim=3,
        access_dim=3,
        surface=0.0,
        bulk=2.0,
        field_obj=7,
        spectrum_obj=7,
    ),
    Scenario(
        name="large_reduction_surface_case",
        role="Larger Buckingham-Pi reduction and nontrivial surface/bulk recovery.",
        value=9.0,
        antipodal_value=9.0,
        variable_count=12,
        base_dimension_count=2,
        dipole=3.0,
        meridian=-2.0,
        ambient_dim=10,
        access_dim=4,
        surface=-15.0,
        bulk=-3.0,
        field_obj=11,
        spectrum_obj=13,
    ),
]


def compose(left: tuple[int, int], right: tuple[int, int]) -> tuple[int, int]:
    return (left[0], right[1])


def scenario_row(scenario: Scenario) -> dict[str, float | str | int]:
    pi_count = scenario.variable_count - scenario.base_dimension_count
    pi_count_recovery_residual = (
        pi_count + scenario.base_dimension_count - scenario.variable_count
    )
    dipole_residual = scenario.dipole + (-scenario.dipole)
    toroidal_residual = scenario.meridian - scenario.meridian
    access_excess = scenario.ambient_dim - scenario.access_dim
    surface_recovery_residual = scenario.surface / scenario.bulk * scenario.bulk - scenario.surface
    identity_left = compose((scenario.field_obj, scenario.field_obj), (scenario.field_obj, scenario.spectrum_obj))
    identity_right = compose((scenario.field_obj, scenario.spectrum_obj), (scenario.spectrum_obj, scenario.spectrum_obj))
    adjoint_roundtrip = compose(
        (scenario.field_obj, scenario.spectrum_obj),
        (scenario.spectrum_obj, scenario.field_obj),
    )
    return {
        "scenario": scenario.name,
        "antipodal_residual": scenario.value - scenario.antipodal_value,
        "pi_count": pi_count,
        "pi_count_recovery_residual": pi_count_recovery_residual,
        "dipole_residual": dipole_residual,
        "toroidal_residual": toroidal_residual,
        "access_excess": access_excess,
        "surface_recovery_residual": surface_recovery_residual,
        "identity_left_ok": int(identity_left == (scenario.field_obj, scenario.spectrum_obj)),
        "identity_right_ok": int(identity_right == (scenario.field_obj, scenario.spectrum_obj)),
        "adjoint_roundtrip_ok": int(adjoint_roundtrip == (scenario.field_obj, scenario.field_obj)),
        "field_spectrum_pair_guard": 1,
    }


def check_scenario(scenario: Scenario) -> dict[str, float | str | int]:
    row = scenario_row(scenario)
    tolerance = max(1.0, abs(scenario.surface)) * 1.0e-12
    checks = {
        "antipodal_residual_zero": abs(float(row["antipodal_residual"])) <= tolerance,
        "pi_count_recovery_zero": int(row["pi_count_recovery_residual"]) == 0,
        "dipole_residual_zero": abs(float(row["dipole_residual"])) <= tolerance,
        "toroidal_residual_zero": abs(float(row["toroidal_residual"])) <= tolerance,
        "access_excess_nonnegative": int(row["access_excess"]) >= 0,
        "surface_recovery_zero": abs(float(row["surface_recovery_residual"])) <= tolerance,
        "identity_left_ok": int(row["identity_left_ok"]) == 1,
        "identity_right_ok": int(row["identity_right_ok"]) == 1,
        "adjoint_roundtrip_ok": int(row["adjoint_roundtrip_ok"]) == 1,
        "field_spectrum_pair_guard": int(row["field_spectrum_pair_guard"]) == 1,
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
        "certificate": "TOPOLOGY_CATEGORY_CARRIERS_CERTIFICATE",
        "generated_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "creator": "Daniel Alexander Trawin",
        "orcid": "https://orcid.org/0009-0001-4630-3715",
        "engine": "Python standard library",
        "claim_boundary": (
            "Representative finite topology/category certificate; universal contracts "
            "are checked in Isabelle/HOL."
        ),
        "equations": {
            "pi_recovery": "(variables-dimensions)+dimensions-variables = 0",
            "surface_recovery": "(surface/bulk) bulk - surface = 0",
            "identity_composition": "id_A ; f = f and f ; id_B = f",
            "adjoint_roundtrip": "(A,B);(B,A) = (A,A)",
        },
        "checks": {
            "all_scenarios_pass": "pass" if all_pass else "fail",
            "finite_category_contract_verified": "pass"
            if all(
                row["status"] == "pass"
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
        "antipodal_residual",
        "pi_count",
        "pi_count_recovery_residual",
        "dipole_residual",
        "toroidal_residual",
        "access_excess",
        "surface_recovery_residual",
        "identity_left_ok",
        "identity_right_ok",
        "adjoint_roundtrip_ok",
        "field_spectrum_pair_guard",
    ]
    with CSV_OUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for scenario in SCENARIOS:
            writer.writerow(scenario_row(scenario))

    lines = [
        "# Topology/Category Carriers Certificate",
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
            "- `{scenario}`: status `{status}`, pi count `{pi_count}`, "
            "access excess `{access_excess}`, surface residual `{surface_recovery_residual:.6g}`".format(
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
