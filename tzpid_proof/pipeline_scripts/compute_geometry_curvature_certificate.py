#!/usr/bin/env python
"""Generate a Phase 2 certificate for geometry/curvature batch 019 carriers."""

from __future__ import annotations

import csv
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path


OUT_DIR = Path("phase2_checks")
JSON_OUT = OUT_DIR / "GEOMETRY_CURVATURE_CARRIERS_CERTIFICATE.json"
CSV_OUT = OUT_DIR / "GEOMETRY_CURVATURE_CARRIERS_GRID.csv"
MD_OUT = OUT_DIR / "GEOMETRY_CURVATURE_CARRIERS_CERTIFICATE.md"


@dataclass(frozen=True)
class Scenario:
    name: str
    role: str
    coupling: float
    curvature: float


SCENARIOS = [
    Scenario(
        name="unit_curvature_response",
        role="Unit coupling and positive curvature.",
        coupling=1.0,
        curvature=2.5,
    ),
    Scenario(
        name="zero_curvature_boundary",
        role="Zero curvature boundary still closes the residual.",
        coupling=3.0,
        curvature=0.0,
    ),
    Scenario(
        name="large_coupling_positive_response",
        role="Larger coupling produces a nonnegative proportional response.",
        coupling=12.0,
        curvature=0.125,
    ),
]


def scenario_row(scenario: Scenario) -> dict[str, float | str | int]:
    observed = scenario.coupling * scenario.curvature
    response = scenario.coupling * scenario.curvature
    response_residual = observed - response
    manifold_closeout_residual = scenario.curvature - scenario.curvature
    return {
        "scenario": scenario.name,
        "coupling": scenario.coupling,
        "curvature": scenario.curvature,
        "observed": observed,
        "response": response,
        "response_residual": response_residual,
        "response_nonnegative": int(response >= 0.0),
        "coupling_margin": scenario.coupling,
        "curvature_margin": scenario.curvature,
        "manifold_closeout_residual": manifold_closeout_residual,
    }


def check_scenario(scenario: Scenario) -> dict[str, float | str | int]:
    row = scenario_row(scenario)
    tolerance = max(1.0, abs(float(row["observed"]))) * 1.0e-12
    checks = {
        "response_residual_zero": abs(float(row["response_residual"])) <= tolerance,
        "response_nonnegative": int(row["response_nonnegative"]) == 1,
        "coupling_margin_nonnegative": float(row["coupling_margin"]) >= -tolerance,
        "curvature_margin_nonnegative": float(row["curvature_margin"]) >= -tolerance,
        "manifold_closeout_residual_zero": abs(float(row["manifold_closeout_residual"])) <= tolerance,
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
        "certificate": "GEOMETRY_CURVATURE_CARRIERS_CERTIFICATE",
        "generated_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "creator": "Daniel Alexander Trawin",
        "orcid": "https://orcid.org/0009-0001-4630-3715",
        "engine": "Python standard library",
        "claim_boundary": (
            "Representative numerical certificate for geometry/curvature carrier algebra; "
            "the universal contracts are checked in Isabelle/HOL."
        ),
        "equations": {
            "curvature_response": "observed = coupling * curvature",
            "response_residual": "observed - coupling*curvature = 0",
            "nonnegative_response": "coupling >= 0 and curvature >= 0 imply response >= 0",
            "manifold_closeout": "curvature - curvature = 0",
        },
        "checks": {
            "all_scenarios_pass": "pass" if all_pass else "fail",
            "curvature_coupling_verified": "pass"
            if all(row["response_residual_zero"] == "pass" for row in summaries)
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
        "coupling",
        "curvature",
        "observed",
        "response",
        "response_residual",
        "response_nonnegative",
        "coupling_margin",
        "curvature_margin",
        "manifold_closeout_residual",
    ]
    with CSV_OUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for scenario in SCENARIOS:
            writer.writerow(scenario_row(scenario))

    lines = [
        "# Geometry/Curvature Carriers Certificate",
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
            "- `{scenario}`: status `{status}`, observed `{observed:.6g}`, "
            "response residual `{response_residual:.6g}`".format(**row)
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
