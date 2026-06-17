#!/usr/bin/env python
"""Generate a Phase 2 certificate for phi/log-periodic ripple scaling.

This certificate backs ``TZPID_Ripple_LogPeriodic_PhiBridge.thy``.  It verifies
the algebraic bridge from fifth-flip phi-inflation into projected ripple
scale-invariance:

    alpha = 1/phi
    shell_k = base_radius * alpha^k
    shell_{k+1} / shell_k = alpha
    ripple_index(lambda_k, height_k) = lambda_0 / height_0

The rows are numerical samples, not a new empirical ripple dataset.
"""

from __future__ import annotations

import csv
import json
import math
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path


OUT_DIR = Path("phase2_checks")
JSON_OUT = OUT_DIR / "RIPPLE_LOG_PERIODIC_PHI_CERTIFICATE.json"
CSV_OUT = OUT_DIR / "RIPPLE_LOG_PERIODIC_PHI_GRID.csv"
MD_OUT = OUT_DIR / "RIPPLE_LOG_PERIODIC_PHI_CERTIFICATE.md"


@dataclass(frozen=True)
class Scenario:
    name: str
    role: str
    base_radius: float
    wavelength: float
    height: float
    levels: int


SCENARIOS = [
    Scenario(
        name="sand_ripple_index_15",
        role="Representative aeolian ripple index carrier.",
        base_radius=1.0,
        wavelength=0.15,
        height=0.01,
        levels=12,
    ),
    Scenario(
        name="water_ripple_index_8",
        role="Representative water-surface ripple index carrier.",
        base_radius=2.0,
        wavelength=0.08,
        height=0.01,
        levels=12,
    ),
    Scenario(
        name="wide_megaripple_index_20",
        role="Larger-scale bedform ratio carrier.",
        base_radius=30.0,
        wavelength=4.0,
        height=0.2,
        levels=12,
    ),
]


def phi_value() -> float:
    return (1.0 + math.sqrt(5.0)) / 2.0


def scenario_rows(scenario: Scenario) -> list[dict[str, float | int | str]]:
    phi = phi_value()
    alpha = 1.0 / phi
    initial_index = scenario.wavelength / scenario.height
    rows: list[dict[str, float | int | str]] = []
    for level in range(scenario.levels + 1):
        scale = alpha**level
        shell_radius = scenario.base_radius * scale
        wavelength = scenario.wavelength * scale
        height = scenario.height * scale
        rows.append(
            {
                "scenario": scenario.name,
                "level": level,
                "phi": phi,
                "alpha": alpha,
                "scale": scale,
                "shell_radius": shell_radius,
                "wavelength": wavelength,
                "height": height,
                "ripple_index": wavelength / height,
                "initial_ripple_index": initial_index,
            }
        )
    return rows


def check_scenario(scenario: Scenario) -> dict[str, float | int | str]:
    rows = scenario_rows(scenario)
    alpha = float(rows[0]["alpha"])
    tolerance = 1.0e-12
    shell_ratio_residuals = []
    for index in range(len(rows) - 1):
        ratio = float(rows[index + 1]["shell_radius"]) / float(rows[index]["shell_radius"])
        shell_ratio_residuals.append(abs(ratio - alpha))
    ripple_index_residuals = [
        abs(float(row["ripple_index"]) - float(row["initial_ripple_index"]))
        for row in rows
    ]
    scale_ratio_residuals = []
    for index in range(len(rows) - 1):
        ratio = float(rows[index + 1]["scale"]) / float(rows[index]["scale"])
        scale_ratio_residuals.append(abs(ratio - alpha))

    checks = {
        "alpha_open_unit_interval": 0.0 < alpha < 1.0,
        "shell_successor_ratio_constant": max(shell_ratio_residuals) <= tolerance,
        "projection_scale_successor_ratio_constant": max(scale_ratio_residuals)
        <= tolerance,
        "ripple_index_invariant": max(ripple_index_residuals) <= tolerance,
        "shells_monotone_inward": all(
            float(rows[index + 1]["shell_radius"]) < float(rows[index]["shell_radius"])
            for index in range(len(rows) - 1)
        ),
    }

    return {
        "scenario": scenario.name,
        "role": scenario.role,
        "base_radius": scenario.base_radius,
        "wavelength": scenario.wavelength,
        "height": scenario.height,
        "levels": scenario.levels,
        "phi": float(rows[0]["phi"]),
        "alpha": alpha,
        "initial_ripple_index": float(rows[0]["initial_ripple_index"]),
        "final_shell_radius": float(rows[-1]["shell_radius"]),
        "max_shell_ratio_residual": max(shell_ratio_residuals),
        "max_scale_ratio_residual": max(scale_ratio_residuals),
        "max_ripple_index_residual": max(ripple_index_residuals),
        "tolerance": tolerance,
        "status": "pass" if all(checks.values()) else "fail",
        **{key: "pass" if value else "fail" for key, value in checks.items()},
    }


def build_certificate() -> dict:
    summaries = [check_scenario(scenario) for scenario in SCENARIOS]
    all_pass = all(row["status"] == "pass" for row in summaries)
    return {
        "certificate": "RIPPLE_LOG_PERIODIC_PHI_CERTIFICATE",
        "generated_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "creator": "Daniel Alexander Trawin",
        "orcid": "https://orcid.org/0009-0001-4630-3715",
        "engine": "Python standard library",
        "claim_boundary": (
            "Computational certificate for phi-scaled log-periodic projection "
            "and dimensionless ripple-index invariance; not a new empirical dataset."
        ),
        "equations": {
            "phi": "phi = (1 + sqrt(5))/2",
            "alpha": "alpha = 1/phi",
            "shell_sequence": "r_k = r0 alpha^k",
            "successor_ratio": "r_{k+1}/r_k = alpha",
            "ripple_index": "(alpha^k wavelength)/(alpha^k height) = wavelength/height",
        },
        "checks": {
            "all_scenarios_pass": "pass" if all_pass else "fail",
            "shell_ratio_verified": "pass"
            if all(row["shell_successor_ratio_constant"] == "pass" for row in summaries)
            else "fail",
            "ripple_index_invariance_verified": "pass"
            if all(row["ripple_index_invariant"] == "pass" for row in summaries)
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
        "level",
        "phi",
        "alpha",
        "scale",
        "shell_radius",
        "wavelength",
        "height",
        "ripple_index",
        "initial_ripple_index",
    ]
    with CSV_OUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for scenario in SCENARIOS:
            writer.writerows(scenario_rows(scenario))

    lines = [
        "# Ripple Log-Periodic Phi Certificate",
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
            "- `{scenario}`: status `{status}`, alpha `{alpha:.12g}`, "
            "index `{initial_ripple_index:.6g}`, max index residual `{max_ripple_index_residual:.3g}`".format(
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
