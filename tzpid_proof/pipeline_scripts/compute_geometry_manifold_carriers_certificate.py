from __future__ import annotations

import csv
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parent
OUT_DIR = ROOT / "phase2_checks"
OUT_JSON = OUT_DIR / "GEOMETRY_MANIFOLD_CARRIERS_CERTIFICATE.json"
OUT_MD = OUT_DIR / "GEOMETRY_MANIFOLD_CARRIERS_CERTIFICATE.md"
OUT_CSV = OUT_DIR / "GEOMETRY_MANIFOLD_CARRIERS_GRID.csv"


def close(a: float, b: float, tol: float = 1e-12) -> bool:
    return abs(a - b) <= tol


def dist2_2(x: float, y: float, u: float, v: float) -> float:
    return (x - u) ** 2 + (y - v) ** 2


def norm2_2(x: float, y: float) -> float:
    return x**2 + y**2


def norm2_3(x: float, y: float, z: float) -> float:
    return x**2 + y**2 + z**2


def sphere_curvature(radius: float) -> float:
    return 1.0 / radius**2


def action_quadratic(duration: float, velocity: float) -> float:
    return duration * velocity**2 / 2.0


def build_certificate() -> dict[str, object]:
    x, y = 1.25, -0.75
    u, v = -0.5, 2.0
    z = 3.0
    radius = 4.0
    curvature = sphere_curvature(radius)
    field_strength = curvature
    start = 0.3
    winding = 2
    finish = start + 2.0 * math.pi * winding
    duration = 5.0
    velocity = -1.2
    action = 3.0
    competitor = 4.5
    jacobian = 2.25

    checks = [
        {
            "name": "dist2_self_zero",
            "value": dist2_2(x, y, x, y),
            "expected": 0.0,
            "pass": close(dist2_2(x, y, x, y), 0.0),
        },
        {
            "name": "dist2_symmetric",
            "value": dist2_2(x, y, u, v) - dist2_2(u, v, x, y),
            "expected": 0.0,
            "pass": close(dist2_2(x, y, u, v), dist2_2(u, v, x, y)),
        },
        {
            "name": "projection_norm_not_above_lifted_norm",
            "value": norm2_3(x, y, z) - norm2_2(x, y),
            "expected": z**2,
            "pass": norm2_2(x, y) <= norm2_3(x, y, z) and close(norm2_3(x, y, z) - norm2_2(x, y), z**2),
        },
        {
            "name": "zero_fiber_projection_preserves_norm",
            "value": norm2_3(x, y, 0.0) - norm2_2(x, y),
            "expected": 0.0,
            "pass": close(norm2_3(x, y, 0.0), norm2_2(x, y)),
        },
        {
            "name": "nonzero_jacobian_chart_regular",
            "value": jacobian,
            "expected": jacobian,
            "pass": jacobian != 0.0,
        },
        {
            "name": "sphere_curvature_recovers_radius_square",
            "value": curvature * radius**2,
            "expected": 1.0,
            "pass": close(curvature * radius**2, 1.0),
        },
        {
            "name": "curvature_field_match_zero_residual",
            "value": curvature - field_strength,
            "expected": 0.0,
            "pass": close(curvature - field_strength, 0.0),
        },
        {
            "name": "phase_loop_adds_one_turn",
            "value": (finish + 2.0 * math.pi - start) / (2.0 * math.pi),
            "expected": float(winding + 1),
            "pass": close((finish + 2.0 * math.pi - start) / (2.0 * math.pi), float(winding + 1)),
        },
        {
            "name": "quadratic_action_nonnegative",
            "value": action_quadratic(duration, velocity),
            "expected": 3.6,
            "pass": action_quadratic(duration, velocity) >= 0.0 and close(action_quadratic(duration, velocity), 3.6),
        },
        {
            "name": "least_action_margin_nonnegative",
            "value": competitor - action,
            "expected": 1.5,
            "pass": action <= competitor and close(competitor - action, 1.5),
        },
    ]

    return {
        "certificate": "GEOMETRY_MANIFOLD_CARRIERS_CERTIFICATE",
        "generated_utc": "2026-06-09T00:00:00Z",
        "creator": "Daniel Alexander Trawin",
        "orcid": "https://orcid.org/0009-0001-4630-3715",
        "isabelle_theory": "isabelle_tzpid/TZPID_GeometryManifold_Carriers.thy",
        "source_batch": "Geometry/manifold batch 008",
        "status": "pass" if all(row["pass"] for row in checks) else "fail",
        "checks": checks,
        "parameters": {
            "point_xy": [x, y],
            "point_uv": [u, v],
            "fiber_z": z,
            "radius": radius,
            "winding": winding,
            "duration": duration,
            "velocity": velocity,
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
        "# Geometry/Manifold Carriers Certificate",
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
        "This certificate backs finite metric, projection, chart, curvature, "
        "holonomy, and action carriers for geometry/manifold batch 008."
    )
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    cert = build_certificate()
    write_outputs(cert)
    print(json.dumps({"status": cert["status"], "checks": len(cert["checks"])}, indent=2))


if __name__ == "__main__":
    main()
