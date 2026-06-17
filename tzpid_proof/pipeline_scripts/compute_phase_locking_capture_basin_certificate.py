#!/usr/bin/env python
"""Generate a Phase 2 certificate for phase-locking capture basins.

This certificate backs ``TZPID_PhaseLockingResonance_CaptureBasin.thy``.  It
samples coupled-oscillator threshold semantics:

    capture iff |Delta| <= K, K > 0
    phase witness = Delta / K
    residual = K * witness - Delta
    basin width = 2K

The script is a numerical certificate for the typed carrier, not a dynamical
simulation of all possible oscillator models.
"""

from __future__ import annotations

import csv
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path


OUT_DIR = Path("phase2_checks")
JSON_OUT = OUT_DIR / "PHASE_LOCKING_CAPTURE_BASIN_CERTIFICATE.json"
CSV_OUT = OUT_DIR / "PHASE_LOCKING_CAPTURE_BASIN_GRID.csv"
MD_OUT = OUT_DIR / "PHASE_LOCKING_CAPTURE_BASIN_CERTIFICATE.md"


@dataclass(frozen=True)
class Scenario:
    name: str
    role: str
    coupling: float
    detuning_min: float
    detuning_max: float
    samples: int


SCENARIOS = [
    Scenario(
        name="unit_coupling_capture_window",
        role="Baseline K=1 capture interval with boundary points included.",
        coupling=1.0,
        detuning_min=-1.25,
        detuning_max=1.25,
        samples=501,
    ),
    Scenario(
        name="weak_coupling_narrow_window",
        role="Small K gives a narrow admissible basin.",
        coupling=0.35,
        detuning_min=-0.6,
        detuning_max=0.6,
        samples=481,
    ),
    Scenario(
        name="strong_coupling_wide_window",
        role="Larger K gives a wider capture basin.",
        coupling=2.0,
        detuning_min=-2.5,
        detuning_max=2.5,
        samples=501,
    ),
]


def detuning_grid(scenario: Scenario) -> list[float]:
    if scenario.samples < 3:
        raise ValueError("samples must be at least 3")
    step = (scenario.detuning_max - scenario.detuning_min) / (scenario.samples - 1)
    return [scenario.detuning_min + index * step for index in range(scenario.samples)]


def grid_rows(scenario: Scenario) -> list[dict[str, float | str | int]]:
    rows: list[dict[str, float | str | int]] = []
    tolerance = max(scenario.coupling, 1.0) * 1.0e-12
    for detuning in detuning_grid(scenario):
        coupling = scenario.coupling
        admissible = abs(detuning) <= coupling + tolerance
        witness = detuning / coupling
        residual = coupling * witness - detuning
        margin = coupling - abs(detuning)
        rows.append(
            {
                "scenario": scenario.name,
                "coupling": coupling,
                "detuning": detuning,
                "capture_margin": margin,
                "capture_admissible": int(admissible),
                "phase_witness": witness,
                "witness_abs": abs(witness),
                "phase_velocity_residual": residual,
                "basin_width": 2.0 * coupling,
            }
        )
    return rows


def check_scenario(scenario: Scenario) -> dict[str, float | str | int]:
    rows = grid_rows(scenario)
    tolerance = max(scenario.coupling, 1.0) * 1.0e-12
    admissible_rows = [row for row in rows if int(row["capture_admissible"]) == 1]
    outside_rows = [row for row in rows if int(row["capture_admissible"]) == 0]
    residuals = [abs(float(row["phase_velocity_residual"])) for row in rows]
    width_errors = [
        abs(float(row["basin_width"]) - 2.0 * scenario.coupling) for row in rows
    ]
    checks = {
        "positive_coupling": scenario.coupling > 0.0,
        "basin_width_matches_2K": max(width_errors) <= tolerance,
        "residual_zeroes_for_witness": max(residuals) <= tolerance,
        "inside_basin_witness_bounded": all(
            float(row["witness_abs"]) <= 1.0 + tolerance for row in admissible_rows
        ),
        "outside_basin_witness_exceeds_one": all(
            float(row["witness_abs"]) >= 1.0 - tolerance for row in outside_rows
        ),
        "admissible_iff_margin_nonnegative": all(
            (float(row["capture_margin"]) >= -tolerance)
            == (int(row["capture_admissible"]) == 1)
            for row in rows
        ),
    }

    return {
        "scenario": scenario.name,
        "role": scenario.role,
        "coupling": scenario.coupling,
        "detuning_min": scenario.detuning_min,
        "detuning_max": scenario.detuning_max,
        "samples": scenario.samples,
        "admissible_samples": len(admissible_rows),
        "outside_samples": len(outside_rows),
        "expected_basin_width": 2.0 * scenario.coupling,
        "max_residual": max(residuals),
        "max_width_error": max(width_errors),
        "tolerance": tolerance,
        "status": "pass" if all(checks.values()) else "fail",
        **{key: "pass" if value else "fail" for key, value in checks.items()},
    }


def build_certificate() -> dict:
    summaries = [check_scenario(scenario) for scenario in SCENARIOS]
    all_pass = all(row["status"] == "pass" for row in summaries)
    return {
        "certificate": "PHASE_LOCKING_CAPTURE_BASIN_CERTIFICATE",
        "generated_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "creator": "Daniel Alexander Trawin",
        "orcid": "https://orcid.org/0009-0001-4630-3715",
        "engine": "Python standard library",
        "claim_boundary": (
            "Computational certificate for the algebraic capture-basin carrier; "
            "not a full nonlinear oscillator simulation."
        ),
        "equations": {
            "capture_condition": "|Delta| <= K, K > 0",
            "capture_margin": "K - |Delta|",
            "phase_witness": "Delta / K",
            "phase_residual": "K(Delta/K) - Delta = 0",
            "basin_width": "2K",
        },
        "checks": {
            "all_scenarios_pass": "pass" if all_pass else "fail",
            "threshold_semantics_verified": "pass"
            if all(row["admissible_iff_margin_nonnegative"] == "pass" for row in summaries)
            else "fail",
            "witness_residual_verified": "pass"
            if all(row["residual_zeroes_for_witness"] == "pass" for row in summaries)
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
        "detuning",
        "capture_margin",
        "capture_admissible",
        "phase_witness",
        "witness_abs",
        "phase_velocity_residual",
        "basin_width",
    ]
    with CSV_OUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for scenario in SCENARIOS:
            writer.writerows(grid_rows(scenario))

    lines = [
        "# Phase-Locking Capture Basin Certificate",
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
            "- `{scenario}`: status `{status}`, K `{coupling:.6g}`, "
            "admissible samples `{admissible_samples}`, max residual `{max_residual:.6g}`".format(
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
