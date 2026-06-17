#!/usr/bin/env python
"""Generate a Phase 2 certificate for matter-creation temporal flow.

This is a computational certificate for the closed-form carrier formalized in
``TZPID_MatterCreation_TemporalFlow.thy``.  It checks the numerical behavior of

    rho_vac(t) = rho0 exp(-t/tau)
    J_emerge(t) = (rho0/tau) exp(-t/tau)
    rho_matter(t) = A (1 - exp(-t/tau))

over a time grid.  The certificate is intentionally scoped: it verifies the
transfer equations and their conservation/derivative consistency, not the
physical premise that a vacuum reservoir must create matter.
"""

from __future__ import annotations

import csv
import json
import math
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path


OUT_DIR = Path("phase2_checks")
JSON_OUT = OUT_DIR / "MATTER_CREATION_TEMPORAL_FLOW_CERTIFICATE.json"
CSV_OUT = OUT_DIR / "MATTER_CREATION_TEMPORAL_FLOW_GRID.csv"
MD_OUT = OUT_DIR / "MATTER_CREATION_TEMPORAL_FLOW_CERTIFICATE.md"


@dataclass(frozen=True)
class Scenario:
    name: str
    role: str
    rho0: float
    tau: float
    amplitude: float
    t_max_factor: float
    samples: int


SCENARIOS = [
    Scenario(
        name="closed_transfer_unit_reservoir",
        role="Equal amplitude carrier: rho_vac + rho_matter remains rho0.",
        rho0=1.0,
        tau=1.0,
        amplitude=1.0,
        t_max_factor=8.0,
        samples=2001,
    ),
    Scenario(
        name="slow_transfer_scaled_reservoir",
        role="Equal amplitude carrier with larger reservoir and slower decay.",
        rho0=2.5,
        tau=3.0,
        amplitude=2.5,
        t_max_factor=8.0,
        samples=2001,
    ),
    Scenario(
        name="partial_matter_channel",
        role="Non-closed diagnostic carrier where only part of the reservoir is routed into matter.",
        rho0=1.0,
        tau=1.5,
        amplitude=0.72,
        t_max_factor=8.0,
        samples=2001,
    ),
]


def rho_vac(t: float, rho0: float, tau: float) -> float:
    return rho0 * math.exp(-(t / tau))


def j_emerge(t: float, rho0: float, tau: float) -> float:
    return (rho0 / tau) * math.exp(-(t / tau))


def rho_matter(t: float, amplitude: float, tau: float) -> float:
    return amplitude * (1.0 - math.exp(-(t / tau)))


def time_grid(t_max: float, samples: int) -> list[float]:
    if samples < 3:
        raise ValueError("samples must be at least 3")
    return [i * t_max / (samples - 1) for i in range(samples)]


def finite_difference_current(values: list[float], times: list[float]) -> list[float]:
    currents: list[float] = []
    for index in range(1, len(times) - 1):
        dt = times[index + 1] - times[index - 1]
        currents.append(-(values[index + 1] - values[index - 1]) / dt)
    return currents


def scenario_grid_rows(scenario: Scenario) -> list[dict[str, float | str]]:
    times = time_grid(scenario.tau * scenario.t_max_factor, scenario.samples)
    rows: list[dict[str, float | str]] = []
    for t in times:
        vac = rho_vac(t, scenario.rho0, scenario.tau)
        current = j_emerge(t, scenario.rho0, scenario.tau)
        matter = rho_matter(t, scenario.amplitude, scenario.tau)
        rows.append(
            {
                "scenario": scenario.name,
                "t": t,
                "rho_vac": vac,
                "j_emerge": current,
                "rho_matter": matter,
                "total_transfer_density": vac + matter,
            }
        )
    return rows


def monotone_nonincreasing(values: list[float], tolerance: float = 1.0e-12) -> bool:
    return all(values[i + 1] <= values[i] + tolerance for i in range(len(values) - 1))


def monotone_nondecreasing(values: list[float], tolerance: float = 1.0e-12) -> bool:
    return all(values[i + 1] + tolerance >= values[i] for i in range(len(values) - 1))


def check_scenario(scenario: Scenario) -> dict[str, float | str]:
    rows = scenario_grid_rows(scenario)
    times = [float(row["t"]) for row in rows]
    vac = [float(row["rho_vac"]) for row in rows]
    current = [float(row["j_emerge"]) for row in rows]
    matter = [float(row["rho_matter"]) for row in rows]
    total = [float(row["total_transfer_density"]) for row in rows]

    fd_current = finite_difference_current(vac, times)
    interior_exact_current = current[1:-1]
    derivative_residuals = [
        abs(approx - exact) for approx, exact in zip(fd_current, interior_exact_current)
    ]
    derivative_scale = max(max(interior_exact_current), 1.0)
    derivative_tolerance = derivative_scale * 1.1e-5

    conservation_residuals = [abs(value - scenario.rho0) for value in total]
    conservation_expected = abs(scenario.amplitude - scenario.rho0) <= 1.0e-12
    conservation_tolerance = max(abs(scenario.rho0), 1.0) * 1.0e-12

    checks = {
        "positive_vacuum_density": all(value > 0.0 for value in vac),
        "positive_emergence_current": all(value > 0.0 for value in current),
        "nonnegative_matter_density": all(value >= -1.0e-12 for value in matter),
        "vacuum_density_monotone_decay": monotone_nonincreasing(vac),
        "matter_density_monotone_growth": monotone_nondecreasing(matter),
        "current_matches_negative_vacuum_derivative": max(derivative_residuals)
        <= derivative_tolerance,
        "closed_transfer_conserved": (
            max(conservation_residuals) <= conservation_tolerance
            if conservation_expected
            else True
        ),
    }

    return {
        "scenario": scenario.name,
        "role": scenario.role,
        "rho0": scenario.rho0,
        "tau": scenario.tau,
        "amplitude": scenario.amplitude,
        "samples": scenario.samples,
        "t_max": scenario.tau * scenario.t_max_factor,
        "final_rho_vac": vac[-1],
        "final_rho_matter": matter[-1],
        "final_total_transfer_density": total[-1],
        "max_derivative_residual": max(derivative_residuals),
        "derivative_tolerance": derivative_tolerance,
        "max_conservation_residual": max(conservation_residuals),
        "conservation_tolerance": conservation_tolerance,
        "closed_transfer_expected": str(conservation_expected).lower(),
        "status": "pass" if all(checks.values()) else "fail",
        **{key: "pass" if value else "fail" for key, value in checks.items()},
    }


def build_certificate() -> dict:
    summaries = [check_scenario(scenario) for scenario in SCENARIOS]
    all_rows: list[dict[str, float | str]] = []
    for scenario in SCENARIOS:
        all_rows.extend(scenario_grid_rows(scenario))

    closed_summaries = [
        row for row in summaries if row["closed_transfer_expected"] == "true"
    ]
    all_pass = all(row["status"] == "pass" for row in summaries)
    closed_transfer_pass = all(
        row["closed_transfer_conserved"] == "pass" for row in closed_summaries
    )
    derivative_pass = all(
        row["current_matches_negative_vacuum_derivative"] == "pass"
        for row in summaries
    )

    return {
        "certificate": "MATTER_CREATION_TEMPORAL_FLOW_CERTIFICATE",
        "generated_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "creator": "Daniel Alexander Trawin",
        "orcid": "https://orcid.org/0009-0001-4630-3715",
        "engine": "Python standard library",
        "claim_boundary": (
            "Computational certificate for the temporal transfer carrier; "
            "not a proof of the physical matter-creation premise."
        ),
        "equations": {
            "vacuum_density": "rho_vac(t) = rho0 exp(-t/tau)",
            "emergence_current": "J_emerge(t) = (rho0/tau) exp(-t/tau) = -d rho_vac/dt",
            "matter_density": "rho_matter(t) = A(1 - exp(-t/tau))",
            "closed_transfer": "rho_vac(t) + rho_matter(t) = rho0 when A = rho0",
        },
        "checks": {
            "all_scenarios_pass": "pass" if all_pass else "fail",
            "closed_transfer_conservation": "pass" if closed_transfer_pass else "fail",
            "derivative_current_consistency": "pass" if derivative_pass else "fail",
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
        "t",
        "rho_vac",
        "j_emerge",
        "rho_matter",
        "total_transfer_density",
    ]
    with CSV_OUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for scenario in SCENARIOS:
            writer.writerows(scenario_grid_rows(scenario))

    lines = [
        "# Matter Creation Temporal Flow Certificate",
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
            "- `{scenario}`: status `{status}`, max derivative residual `{max_derivative_residual:.6g}`, "
            "max conservation residual `{max_conservation_residual:.6g}`".format(**row)
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
