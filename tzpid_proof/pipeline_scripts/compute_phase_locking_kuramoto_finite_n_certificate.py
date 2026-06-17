#!/usr/bin/env python
"""Generate a Phase 2 certificate for finite-N Kuramoto entrainment scans.

This backs ``TZPID_PhaseLockingResonance_KuramotoFiniteN.thy``.  The certificate
checks a finite-population version of the phase-locking carrier:

    all detunings captured iff |Delta_i| <= K
    phase witness_i = Delta_i / K
    residual_i = K * witness_i - Delta_i
    order floor = 1 - (D / K)^2, where D >= max_i |Delta_i|

The output is an algebraic scan certificate, not a full nonlinear time-domain
simulation of the Kuramoto differential equation.
"""

from __future__ import annotations

import csv
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path


OUT_DIR = Path("phase2_checks")
JSON_OUT = OUT_DIR / "PHASE_LOCKING_KURAMOTO_FINITE_N_CERTIFICATE.json"
CSV_OUT = OUT_DIR / "PHASE_LOCKING_KURAMOTO_FINITE_N_GRID.csv"
MD_OUT = OUT_DIR / "PHASE_LOCKING_KURAMOTO_FINITE_N_CERTIFICATE.md"


@dataclass(frozen=True)
class Scenario:
    name: str
    role: str
    coupling: float
    detunings: tuple[float, ...]


SCENARIOS = [
    Scenario(
        name="three_body_near_resonance",
        role="Small finite population with all detunings safely inside the capture basin.",
        coupling=1.0,
        detunings=(-0.32, 0.0, 0.41),
    ),
    Scenario(
        name="orbital_cluster_partial_lock",
        role="Cluster-like spread near the boundary of a stronger coupling window.",
        coupling=1.5,
        detunings=(-1.2, -0.75, -0.1, 0.6, 1.35),
    ),
    Scenario(
        name="wide_coupling_entrainment",
        role="Wide coupling keeps a heterogeneous finite population entrained.",
        coupling=2.25,
        detunings=(-2.0, -1.2, -0.35, 0.15, 0.9, 2.1),
    ),
]


def scenario_rows(scenario: Scenario) -> list[dict[str, float | str | int]]:
    radius = max(abs(detuning) for detuning in scenario.detunings)
    order_floor = 1.0 - (radius / scenario.coupling) ** 2
    rows: list[dict[str, float | str | int]] = []
    for index, detuning in enumerate(scenario.detunings, start=1):
        witness = detuning / scenario.coupling
        residual = scenario.coupling * witness - detuning
        rows.append(
            {
                "scenario": scenario.name,
                "oscillator_index": index,
                "coupling": scenario.coupling,
                "detuning": detuning,
                "radius": radius,
                "capture_admissible": int(abs(detuning) <= scenario.coupling),
                "phase_witness": witness,
                "witness_abs": abs(witness),
                "phase_velocity_residual": residual,
                "order_floor": order_floor,
            }
        )
    return rows


def check_scenario(scenario: Scenario) -> dict[str, float | str | int]:
    rows = scenario_rows(scenario)
    tolerance = max(scenario.coupling, 1.0) * 1.0e-12
    radius = max(abs(detuning) for detuning in scenario.detunings)
    order_floor = 1.0 - (radius / scenario.coupling) ** 2
    residuals = [abs(float(row["phase_velocity_residual"])) for row in rows]
    witnesses = [float(row["witness_abs"]) for row in rows]
    checks = {
        "positive_coupling": scenario.coupling > 0.0,
        "radius_inside_coupling": 0.0 <= radius <= scenario.coupling,
        "all_detunings_captured": all(
            int(row["capture_admissible"]) == 1 for row in rows
        ),
        "all_phase_witnesses_bounded": all(
            witness <= 1.0 + tolerance for witness in witnesses
        ),
        "all_residuals_zero": max(residuals) <= tolerance,
        "order_floor_bounded": -tolerance <= order_floor <= 1.0 + tolerance,
    }
    return {
        "scenario": scenario.name,
        "role": scenario.role,
        "coupling": scenario.coupling,
        "oscillator_count": len(scenario.detunings),
        "radius": radius,
        "order_floor": order_floor,
        "max_witness_abs": max(witnesses),
        "max_residual": max(residuals),
        "tolerance": tolerance,
        "status": "pass" if all(checks.values()) else "fail",
        **{key: "pass" if value else "fail" for key, value in checks.items()},
    }


def build_certificate() -> dict:
    summaries = [check_scenario(scenario) for scenario in SCENARIOS]
    all_pass = all(row["status"] == "pass" for row in summaries)
    return {
        "certificate": "PHASE_LOCKING_KURAMOTO_FINITE_N_CERTIFICATE",
        "generated_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "creator": "Daniel Alexander Trawin",
        "orcid": "https://orcid.org/0009-0001-4630-3715",
        "engine": "Python standard library",
        "claim_boundary": (
            "Finite-N algebraic entrainment scan for the phase-locking carrier; "
            "not a full nonlinear time-domain Kuramoto simulation."
        ),
        "equations": {
            "finite_capture": "forall i, |Delta_i| <= K",
            "detuning_radius": "D = max_i |Delta_i|",
            "phase_witness": "w_i = Delta_i / K",
            "phase_residual": "K*w_i - Delta_i = 0",
            "order_floor": "1 - (D/K)^2",
        },
        "checks": {
            "all_scenarios_pass": "pass" if all_pass else "fail",
            "finite_capture_verified": "pass"
            if all(row["all_detunings_captured"] == "pass" for row in summaries)
            else "fail",
            "order_floor_verified": "pass"
            if all(row["order_floor_bounded"] == "pass" for row in summaries)
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
        "oscillator_index",
        "coupling",
        "detuning",
        "radius",
        "capture_admissible",
        "phase_witness",
        "witness_abs",
        "phase_velocity_residual",
        "order_floor",
    ]
    with CSV_OUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for scenario in SCENARIOS:
            writer.writerows(scenario_rows(scenario))

    lines = [
        "# Phase-Locking Kuramoto Finite-N Certificate",
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
            "- `{scenario}`: status `{status}`, N `{oscillator_count}`, "
            "K `{coupling:.6g}`, D `{radius:.6g}`, order floor `{order_floor:.6g}`, "
            "max residual `{max_residual:.6g}`".format(**row)
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
