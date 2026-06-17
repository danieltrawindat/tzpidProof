#!/usr/bin/env python
"""Generate a Phase 2 certificate for emergence/bifurcation normal forms.

This backs ``TZPID_EmergenceBifurcation_NormalForms.thy`` with sampled checks:

    pitchfork residual f(mu,x) = mu*x - x^3
    nonzero branches x = +/- sqrt(mu) for mu > 0
    saddle-node cusp residual g(mu,x) = mu + x^2 at (0,0)
    transition boundary residual control - critical
    asymptotic emergence profile exp(-scale/t), t > 0
"""

from __future__ import annotations

import csv
import json
import math
from datetime import datetime, timezone
from pathlib import Path


OUT_DIR = Path("phase2_checks")
JSON_OUT = OUT_DIR / "EMERGENCE_BIFURCATION_NORMAL_FORM_CERTIFICATE.json"
CSV_OUT = OUT_DIR / "EMERGENCE_BIFURCATION_NORMAL_FORM_GRID.csv"
MD_OUT = OUT_DIR / "EMERGENCE_BIFURCATION_NORMAL_FORM_CERTIFICATE.md"


MU_VALUES = [0.0, 0.01, 0.05, 0.1, 0.25, 1.0, 2.25]
TIME_VALUES = [-1.0, 0.0, 0.01, 0.05, 0.1, 0.5, 1.0, 2.0]
SCALE = 1.0


def pitchfork_residual(mu: float, x: float) -> float:
    return mu * x - x**3


def saddle_node_residual(mu: float, x: float) -> float:
    return mu + x**2


def transition_boundary_residual(control: float, critical: float) -> float:
    return control - critical


def asymptotic_profile(scale: float, t: float) -> float:
    return math.exp(-(scale / t)) if t > 0.0 else 0.0


def build_rows() -> list[dict[str, float | str]]:
    rows: list[dict[str, float | str]] = []
    for mu in MU_VALUES:
        branch_values = [0.0]
        if mu > 0.0:
            root = math.sqrt(mu)
            branch_values.extend([root, -root])
        for x in branch_values:
            rows.append(
                {
                    "kind": "pitchfork",
                    "mu": mu,
                    "x": x,
                    "t": "",
                    "residual": pitchfork_residual(mu, x),
                    "value": "",
                    "expected": 0.0,
                }
            )
    rows.append(
        {
            "kind": "saddle_node_cusp",
            "mu": 0.0,
            "x": 0.0,
            "t": "",
            "residual": saddle_node_residual(0.0, 0.0),
            "value": "",
            "expected": 0.0,
        }
    )
    for control, critical in [(1.0, 1.0), (0.0, 0.0), (2.5, 2.5)]:
        rows.append(
            {
                "kind": "transition_boundary",
                "mu": "",
                "x": "",
                "t": "",
                "residual": transition_boundary_residual(control, critical),
                "value": control,
                "expected": critical,
            }
        )
    for t in TIME_VALUES:
        rows.append(
            {
                "kind": "asymptotic_profile",
                "mu": "",
                "x": "",
                "t": t,
                "residual": "",
                "value": asymptotic_profile(SCALE, t),
                "expected": "positive" if t > 0.0 else 0.0,
            }
        )
    return rows


def build_certificate() -> dict:
    rows = build_rows()
    tolerance = 1.0e-12
    pitchfork_residuals = [
        abs(float(row["residual"])) for row in rows if row["kind"] == "pitchfork"
    ]
    saddle_residual = next(
        abs(float(row["residual"])) for row in rows if row["kind"] == "saddle_node_cusp"
    )
    boundary_residuals = [
        abs(float(row["residual"]))
        for row in rows
        if row["kind"] == "transition_boundary"
    ]
    profile_rows = [row for row in rows if row["kind"] == "asymptotic_profile"]
    checks = {
        "pitchfork_branches_zero_residual": max(pitchfork_residuals) <= tolerance,
        "saddle_node_cusp_zero_residual": saddle_residual <= tolerance,
        "transition_boundary_zero_residual": max(boundary_residuals) <= tolerance,
        "asymptotic_profile_zero_before_onset": all(
            float(row["value"]) == 0.0 for row in profile_rows if float(row["t"]) <= 0.0
        ),
        "asymptotic_profile_positive_after_onset": all(
            float(row["value"]) > 0.0 for row in profile_rows if float(row["t"]) > 0.0
        ),
    }
    all_pass = all(checks.values())
    return {
        "certificate": "EMERGENCE_BIFURCATION_NORMAL_FORM_CERTIFICATE",
        "generated_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "creator": "Daniel Alexander Trawin",
        "orcid": "https://orcid.org/0009-0001-4630-3715",
        "engine": "Python standard library",
        "claim_boundary": (
            "Computational certificate for normal-form carriers; not a full "
            "domain-specific physical bifurcation fit."
        ),
        "equations": {
            "pitchfork": "f(mu,x) = mu*x - x^3",
            "pitchfork_branches": "x = 0 and x^2 = mu imply f(mu,x)=0",
            "saddle_node": "g(mu,x) = mu + x^2",
            "transition_boundary": "control - critical = 0",
            "asymptotic_profile": "E(t)=exp(-scale/t) for t>0 else 0",
        },
        "checks": {key: "pass" if value else "fail" for key, value in checks.items()},
        "sample_rows": len(rows),
        "max_pitchfork_residual": max(pitchfork_residuals),
        "max_boundary_residual": max(boundary_residuals),
        "status": "pass" if all_pass else "fail",
    }


def write_outputs(certificate: dict, rows: list[dict[str, float | str]]) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    JSON_OUT.write_text(json.dumps(certificate, indent=2), encoding="utf-8")

    with CSV_OUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=["kind", "mu", "x", "t", "residual", "value", "expected"]
        )
        writer.writeheader()
        writer.writerows(rows)

    lines = [
        "# Emergence/Bifurcation Normal Form Certificate",
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
    lines.extend(
        [
            "",
            "## Residual Summary",
            "",
            f"- Sample rows: `{certificate['sample_rows']}`",
            f"- Max pitchfork residual: `{certificate['max_pitchfork_residual']:.3g}`",
            f"- Max boundary residual: `{certificate['max_boundary_residual']:.3g}`",
            "",
        ]
    )
    MD_OUT.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    rows = build_rows()
    certificate = build_certificate()
    write_outputs(certificate, rows)
    if certificate["status"] != "pass":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
