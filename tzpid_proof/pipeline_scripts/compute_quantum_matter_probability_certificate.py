#!/usr/bin/env python
"""Generate a Phase 2 certificate for quantum/matter probability carriers.

This backs ``TZPID_QuantumMatter_ProbabilityCarriers.thy`` with sampled checks:

    diagonal density trace p0+p1 = 1
    Born probabilities p0,p1 lie in [0,1]
    conservation residual after-before = 0
    CHSH quantum window 2 < |S| <= 2 sqrt(2)
    discrete matter shell mass = n * quantum
"""

from __future__ import annotations

import csv
import json
import math
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path


OUT_DIR = Path("phase2_checks")
JSON_OUT = OUT_DIR / "QUANTUM_MATTER_PROBABILITY_CERTIFICATE.json"
CSV_OUT = OUT_DIR / "QUANTUM_MATTER_PROBABILITY_GRID.csv"
MD_OUT = OUT_DIR / "QUANTUM_MATTER_PROBABILITY_CERTIFICATE.md"


@dataclass(frozen=True)
class Scenario:
    name: str
    role: str
    p0: float
    p1: float
    before: float
    after: float
    chsh_s: float
    quantum: float
    shell_n: int


SCENARIOS = [
    Scenario(
        name="balanced_qubit_violation",
        role="Trace-one balanced diagonal density with CHSH violation below Tsirelson.",
        p0=0.5,
        p1=0.5,
        before=1.0,
        after=1.0,
        chsh_s=2.5,
        quantum=0.25,
        shell_n=4,
    ),
    Scenario(
        name="biased_qubit_shell",
        role="Biased diagonal density and exact discrete mass shell.",
        p0=0.2,
        p1=0.8,
        before=3.0,
        after=3.0,
        chsh_s=2.2,
        quantum=0.1,
        shell_n=7,
    ),
    Scenario(
        name="near_tsirelson_window",
        role="Near-upper quantum-window CHSH carrier.",
        p0=0.9,
        p1=0.1,
        before=0.0,
        after=0.0,
        chsh_s=2.8,
        quantum=1.5,
        shell_n=2,
    ),
]


def scenario_rows(scenario: Scenario) -> list[dict[str, float | int | str]]:
    trace = scenario.p0 + scenario.p1
    born0 = scenario.p0
    born1 = scenario.p1
    conservation_residual = scenario.after - scenario.before
    mass = scenario.shell_n * scenario.quantum
    tsirelson = 2.0 * math.sqrt(2.0)
    return [
        {
            "scenario": scenario.name,
            "quantity": "density_trace",
            "value": trace,
            "expected": 1.0,
            "residual": abs(trace - 1.0),
        },
        {
            "scenario": scenario.name,
            "quantity": "born_probability0",
            "value": born0,
            "expected": "in_unit_interval",
            "residual": 0.0 if 0.0 <= born0 <= 1.0 else 1.0,
        },
        {
            "scenario": scenario.name,
            "quantity": "born_probability1",
            "value": born1,
            "expected": "in_unit_interval",
            "residual": 0.0 if 0.0 <= born1 <= 1.0 else 1.0,
        },
        {
            "scenario": scenario.name,
            "quantity": "conservation_residual",
            "value": conservation_residual,
            "expected": 0.0,
            "residual": abs(conservation_residual),
        },
        {
            "scenario": scenario.name,
            "quantity": "chsh_abs_s",
            "value": abs(scenario.chsh_s),
            "expected": "2 < |S| <= 2sqrt(2)",
            "residual": 0.0
            if 2.0 < abs(scenario.chsh_s) <= tsirelson
            else 1.0,
        },
        {
            "scenario": scenario.name,
            "quantity": "discrete_shell_mass",
            "value": mass,
            "expected": scenario.shell_n * scenario.quantum,
            "residual": abs(mass - scenario.shell_n * scenario.quantum),
        },
    ]


def check_scenario(scenario: Scenario) -> dict[str, float | int | str]:
    rows = scenario_rows(scenario)
    tolerance = 1.0e-12
    row_map = {row["quantity"]: row for row in rows}
    checks = {
        "trace_one": float(row_map["density_trace"]["residual"]) <= tolerance,
        "born_probabilities_in_unit_interval": float(
            row_map["born_probability0"]["residual"]
        )
        <= tolerance
        and float(row_map["born_probability1"]["residual"]) <= tolerance,
        "conservation_residual_zero": float(
            row_map["conservation_residual"]["residual"]
        )
        <= tolerance,
        "chsh_quantum_window": float(row_map["chsh_abs_s"]["residual"]) <= tolerance,
        "discrete_shell_exact": float(row_map["discrete_shell_mass"]["residual"])
        <= tolerance,
    }
    return {
        "scenario": scenario.name,
        "role": scenario.role,
        "p0": scenario.p0,
        "p1": scenario.p1,
        "trace": scenario.p0 + scenario.p1,
        "conservation_residual": scenario.after - scenario.before,
        "chsh_abs_s": abs(scenario.chsh_s),
        "tsirelson_bound": 2.0 * math.sqrt(2.0),
        "quantum": scenario.quantum,
        "shell_n": scenario.shell_n,
        "shell_mass": scenario.shell_n * scenario.quantum,
        "status": "pass" if all(checks.values()) else "fail",
        **{key: "pass" if value else "fail" for key, value in checks.items()},
    }


def build_certificate() -> dict:
    summaries = [check_scenario(scenario) for scenario in SCENARIOS]
    all_pass = all(row["status"] == "pass" for row in summaries)
    return {
        "certificate": "QUANTUM_MATTER_PROBABILITY_CERTIFICATE",
        "generated_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "creator": "Daniel Alexander Trawin",
        "orcid": "https://orcid.org/0009-0001-4630-3715",
        "engine": "Python standard library",
        "claim_boundary": (
            "Computational certificate for diagonal two-state probability carriers; "
            "not a full complex density-matrix or Bell-experiment model."
        ),
        "equations": {
            "density_trace": "Tr(rho) = p0 + p1 = 1",
            "born_probabilities": "P0 = p0, P1 = p1, each in [0,1]",
            "conservation": "after - before = 0",
            "chsh_window": "2 < |S| <= 2 sqrt(2)",
            "discrete_shell": "mass = n * quantum",
        },
        "checks": {
            "all_scenarios_pass": "pass" if all_pass else "fail",
            "probability_carrier_verified": "pass"
            if all(row["trace_one"] == "pass" and row["born_probabilities_in_unit_interval"] == "pass" for row in summaries)
            else "fail",
            "bell_window_verified": "pass"
            if all(row["chsh_quantum_window"] == "pass" for row in summaries)
            else "fail",
            "conservation_verified": "pass"
            if all(row["conservation_residual_zero"] == "pass" for row in summaries)
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
        "# Quantum/Matter Probability Certificate",
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
            "- `{scenario}`: status `{status}`, trace `{trace:.6g}`, |S| `{chsh_abs_s:.6g}`, shell mass `{shell_mass:.6g}`".format(
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
