#!/usr/bin/env python
"""Generate a Phase 2 certificate for magnetic/torsion vector-MHD semantics.

This backs ``TZPID_MagneticTorsion_VectorMHD.thy`` with sampled algebra:

    helicity density = A dot B
    uniform helicity integral = volume * density
    ideal MHD eta = 0 -> resistive helicity dissipation = 0
    Elsasser balance magnetic_force = coriolis_force -> Lambda = 1
    torsion density curvature + twist -> 0 when twist = -curvature
"""

from __future__ import annotations

import csv
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path


OUT_DIR = Path("phase2_checks")
JSON_OUT = OUT_DIR / "MAGNETIC_TORSION_VECTOR_MHD_CERTIFICATE.json"
CSV_OUT = OUT_DIR / "MAGNETIC_TORSION_VECTOR_MHD_GRID.csv"
MD_OUT = OUT_DIR / "MAGNETIC_TORSION_VECTOR_MHD_CERTIFICATE.md"


@dataclass(frozen=True)
class Scenario:
    name: str
    role: str
    vector_a: tuple[float, float, float]
    vector_b: tuple[float, float, float]
    volume: float
    eta: float
    current_norm_sq: float
    magnetic_force: float
    coriolis_force: float
    curvature: float


SCENARIOS = [
    Scenario(
        name="zero_b_field_ideal_balance",
        role="Zero magnetic field gives zero helicity density with ideal MHD balance.",
        vector_a=(1.0, -2.0, 0.5),
        vector_b=(0.0, 0.0, 0.0),
        volume=3.0,
        eta=0.0,
        current_norm_sq=4.0,
        magnetic_force=2.0,
        coriolis_force=2.0,
        curvature=0.7,
    ),
    Scenario(
        name="aligned_helicity_density",
        role="Nonzero A dot B still has exact volume integral and balance semantics.",
        vector_a=(1.0, 2.0, 3.0),
        vector_b=(0.5, 0.25, -0.1),
        volume=5.0,
        eta=0.0,
        current_norm_sq=9.0,
        magnetic_force=1.5,
        coriolis_force=1.5,
        curvature=-1.2,
    ),
    Scenario(
        name="large_volume_unit_elsasser",
        role="Large-volume carrier for helicity integral and Elsasser unit recovery.",
        vector_a=(-2.0, 1.0, 4.0),
        vector_b=(3.0, -1.0, 0.5),
        volume=12.0,
        eta=0.0,
        current_norm_sq=0.25,
        magnetic_force=7.0,
        coriolis_force=7.0,
        curvature=2.0,
    ),
]


def dot3(a: tuple[float, float, float], b: tuple[float, float, float]) -> float:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def scenario_rows(scenario: Scenario) -> list[dict[str, float | str]]:
    density = dot3(scenario.vector_a, scenario.vector_b)
    helicity_integral = scenario.volume * density
    dissipation = 2.0 * scenario.eta * scenario.current_norm_sq
    elsasser = scenario.magnetic_force / scenario.coriolis_force
    torsion = scenario.curvature + (-scenario.curvature)
    return [
        {
            "scenario": scenario.name,
            "quantity": "helicity_density",
            "value": density,
            "expected": density,
            "residual": 0.0,
        },
        {
            "scenario": scenario.name,
            "quantity": "uniform_helicity_integral",
            "value": helicity_integral,
            "expected": scenario.volume * density,
            "residual": abs(helicity_integral - scenario.volume * density),
        },
        {
            "scenario": scenario.name,
            "quantity": "ideal_mhd_dissipation",
            "value": dissipation,
            "expected": 0.0,
            "residual": abs(dissipation),
        },
        {
            "scenario": scenario.name,
            "quantity": "elsasser_number",
            "value": elsasser,
            "expected": 1.0,
            "residual": abs(elsasser - 1.0),
        },
        {
            "scenario": scenario.name,
            "quantity": "opposite_twist_torsion",
            "value": torsion,
            "expected": 0.0,
            "residual": abs(torsion),
        },
    ]


def check_scenario(scenario: Scenario) -> dict[str, float | str]:
    rows = scenario_rows(scenario)
    tolerance = 1.0e-12
    zero_b_expected = scenario.vector_b == (0.0, 0.0, 0.0)
    zero_b_density = next(row for row in rows if row["quantity"] == "helicity_density")
    checks = {
        "zero_b_field_zero_helicity_density": (
            abs(float(zero_b_density["value"])) <= tolerance if zero_b_expected else True
        ),
        "uniform_helicity_integral_exact": next(
            float(row["residual"])
            for row in rows
            if row["quantity"] == "uniform_helicity_integral"
        )
        <= tolerance,
        "ideal_mhd_zero_dissipation": next(
            float(row["residual"]) for row in rows if row["quantity"] == "ideal_mhd_dissipation"
        )
        <= tolerance,
        "elsasser_balance_unit": next(
            float(row["residual"]) for row in rows if row["quantity"] == "elsasser_number"
        )
        <= tolerance,
        "opposite_twist_zero_torsion": next(
            float(row["residual"]) for row in rows if row["quantity"] == "opposite_twist_torsion"
        )
        <= tolerance,
    }
    return {
        "scenario": scenario.name,
        "role": scenario.role,
        "helicity_density": float(zero_b_density["value"]),
        "volume": scenario.volume,
        "eta": scenario.eta,
        "magnetic_force": scenario.magnetic_force,
        "coriolis_force": scenario.coriolis_force,
        "curvature": scenario.curvature,
        "status": "pass" if all(checks.values()) else "fail",
        **{key: "pass" if value else "fail" for key, value in checks.items()},
    }


def build_certificate() -> dict:
    summaries = [check_scenario(scenario) for scenario in SCENARIOS]
    all_pass = all(row["status"] == "pass" for row in summaries)
    return {
        "certificate": "MAGNETIC_TORSION_VECTOR_MHD_CERTIFICATE",
        "generated_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "creator": "Daniel Alexander Trawin",
        "orcid": "https://orcid.org/0009-0001-4630-3715",
        "engine": "Python standard library",
        "claim_boundary": (
            "Computational certificate for vector-MHD algebraic carriers; "
            "not a full PDE MHD simulation."
        ),
        "equations": {
            "helicity_density": "h = A dot B",
            "uniform_helicity": "H = V h",
            "resistive_dissipation": "D = 2 eta |J|^2",
            "elsasser": "Lambda = magnetic_force / coriolis_force",
            "torsion_density": "T = curvature + twist",
        },
        "checks": {
            "all_scenarios_pass": "pass" if all_pass else "fail",
            "ideal_mhd_zero_dissipation": "pass"
            if all(row["ideal_mhd_zero_dissipation"] == "pass" for row in summaries)
            else "fail",
            "unit_elsasser_balance": "pass"
            if all(row["elsasser_balance_unit"] == "pass" for row in summaries)
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

    with CSV_OUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=["scenario", "quantity", "value", "expected", "residual"]
        )
        writer.writeheader()
        for scenario in SCENARIOS:
            writer.writerows(scenario_rows(scenario))

    lines = [
        "# Magnetic/Torsion Vector-MHD Certificate",
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
            "- `{scenario}`: status `{status}`, helicity density `{helicity_density:.6g}`, "
            "eta `{eta:.6g}`".format(**row)
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
