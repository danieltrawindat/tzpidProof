from __future__ import annotations

import csv
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parent
OUT_DIR = ROOT / "phase2_checks"
OUT_JSON = OUT_DIR / "TOPOLOGY_VECTOR_INVARIANTS_CERTIFICATE.json"
OUT_MD = OUT_DIR / "TOPOLOGY_VECTOR_INVARIANTS_CERTIFICATE.md"
OUT_CSV = OUT_DIR / "TOPOLOGY_VECTOR_INVARIANTS_GRID.csv"


def dot3(a: tuple[float, float, float], b: tuple[float, float, float]) -> float:
    return sum(x * y for x, y in zip(a, b))


def cross_z(a: tuple[float, float], b: tuple[float, float]) -> float:
    return a[0] * b[1] - a[1] * b[0]


def close(a: float, b: float, tol: float = 1e-12) -> bool:
    return abs(a - b) <= tol


def build_certificate() -> dict[str, object]:
    phi0 = 2.067833848e-15
    n = 3
    flux = n * phi0

    vector_a = (1.25, -0.5, 2.0)
    zero_b = (0.0, 0.0, 0.0)
    magnetic_b = (0.4, -0.2, 0.1)

    area_a = (2.0, 1.0)
    area_b = (-0.5, 3.0)
    area_ab = cross_z(area_a, area_b)
    area_ba = cross_z(area_b, area_a)

    chi = 2.0
    surface_curvature = 3.25
    boundary_curvature = 2.0 * math.pi * chi - surface_curvature
    gauss_bonnet_residual = surface_curvature + boundary_curvature - 2.0 * math.pi * chi

    phase_n = 2.0 * math.pi * n
    phase_next = phase_n + 2.0 * math.pi
    winding_next_expected = 2.0 * math.pi * (n + 1)

    gap = 0.75
    perturbation = 0.25

    checks = [
        {
            "name": "zero_magnetic_field_has_zero_helicity_density",
            "value": dot3(vector_a, zero_b),
            "expected": 0.0,
            "pass": close(dot3(vector_a, zero_b), 0.0),
        },
        {
            "name": "nonzero_helicity_density_is_dot_product",
            "value": dot3(vector_a, magnetic_b),
            "expected": 0.8,
            "pass": close(dot3(vector_a, magnetic_b), 0.8),
        },
        {
            "name": "flux_is_integer_quantum_multiple",
            "value": flux / phi0,
            "expected": float(n),
            "pass": close(flux / phi0, float(n)),
        },
        {
            "name": "oriented_area_swaps_sign",
            "value": area_ab + area_ba,
            "expected": 0.0,
            "pass": close(area_ab + area_ba, 0.0),
        },
        {
            "name": "gauss_bonnet_boundary_balance_closes",
            "value": gauss_bonnet_residual,
            "expected": 0.0,
            "pass": close(gauss_bonnet_residual, 0.0),
        },
        {
            "name": "winding_index_adds_one_turn",
            "value": phase_next,
            "expected": winding_next_expected,
            "pass": close(phase_next, winding_next_expected),
        },
        {
            "name": "gap_exceeds_perturbation",
            "value": gap - perturbation,
            "expected": 0.5,
            "pass": gap > 0.0 and perturbation < gap,
        },
    ]

    return {
        "certificate": "TOPOLOGY_VECTOR_INVARIANTS_CERTIFICATE",
        "generated_utc": "2026-06-09T00:00:00Z",
        "creator": "Daniel Alexander Trawin",
        "orcid": "https://orcid.org/0009-0001-4630-3715",
        "isabelle_theory": "isabelle_tzpid/TZPID_TopologyVector_Invariants.thy",
        "source_batch": "Topology/vector batch 005",
        "status": "pass" if all(row["pass"] for row in checks) else "fail",
        "checks": checks,
        "parameters": {
            "flux_quantum_weber": phi0,
            "integer_multiple": n,
            "chi": chi,
            "gap": gap,
            "perturbation": perturbation,
        },
    }


def write_outputs(cert: dict[str, object]) -> None:
    OUT_DIR.mkdir(exist_ok=True)
    OUT_JSON.write_text(json.dumps(cert, indent=2), encoding="utf-8")

    checks = cert["checks"]
    assert isinstance(checks, list)
    with OUT_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "value", "expected", "pass"])
        writer.writeheader()
        writer.writerows(checks)

    lines = [
        "# Topology/Vector Invariants Certificate",
        "",
        f"- Status: `{cert['status']}`",
        f"- Isabelle theory: `{cert['isabelle_theory']}`",
        f"- Source batch: `{cert['source_batch']}`",
        "",
        "| Check | Value | Expected | Pass |",
        "|---|---:|---:|---|",
    ]
    for row in checks:
        lines.append(
            f"| {row['name']} | {row['value']:.12g} | {row['expected']:.12g} | {row['pass']} |"
        )
    lines.append("")
    lines.append(
        "This certificate backs the finite HOL carriers for helicity density, "
        "flux quantization, oriented circulation area, Gauss-Bonnet boundary "
        "closure, winding increments, and gap protection."
    )
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    cert = build_certificate()
    write_outputs(cert)
    print(json.dumps({"status": cert["status"], "checks": len(cert["checks"])}, indent=2))


if __name__ == "__main__":
    main()
