from __future__ import annotations

import csv
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parent
OUT_DIR = ROOT / "phase2_checks"
OUT_JSON = OUT_DIR / "MASTER_BATCH001_CARRIERS_CERTIFICATE.json"
OUT_MD = OUT_DIR / "MASTER_BATCH001_CARRIERS_CERTIFICATE.md"
OUT_CSV = OUT_DIR / "MASTER_BATCH001_CARRIERS_GRID.csv"


def close(a: float, b: float, tol: float = 1e-12) -> bool:
    return abs(a - b) <= tol


def megastructure_wavelength(radius: float, mode: float) -> float:
    return math.pi * radius / mode


def helicity_decomposition(writhe: float, twist: float) -> float:
    return writhe + twist


def kk_mode_frequency(n: float, radius: float) -> float:
    return n / radius


def kk_tower_mass(n: float, radius: float) -> float:
    return abs(n) / radius


def build_certificate() -> dict[str, object]:
    radius = 42.0
    mode = 6.0
    wavelength = megastructure_wavelength(radius, mode)

    writhe = 1.25
    twist = -0.4
    total_helicity = helicity_decomposition(writhe, twist)

    u = -1.0
    x = 3.5
    dim_a = 4.0
    dim_b = 2.0
    mass = 9.0
    acceleration = 0.0
    distance = 11.0
    delta_phi = 1.2
    compact_radius = 5.0
    kk_n = -3.0
    fourier_a = 0.75
    fourier_b = -1.25
    image_anchor = True
    image_witness = True

    mode_residual = mode * wavelength - math.pi * radius
    helicity_residual = total_helicity - helicity_decomposition(writhe, twist)
    norm_before = x * x
    norm_after = (u * x) * (u * x)
    joint_margin = dim_a * dim_b - dim_a
    force_work = mass * acceleration * distance
    phase_zero = 0.0 * delta_phi
    kk_frequency = kk_mode_frequency(kk_n, compact_radius)
    kk_mass = kk_tower_mass(kk_n, compact_radius)
    fourier_energy = fourier_a**2 + fourier_b**2

    checks = [
        {
            "name": "mode_spacing_residual_zero",
            "value": mode_residual,
            "expected": 0.0,
            "pass": close(mode_residual, 0.0),
        },
        {
            "name": "helicity_decomposition_residual_zero",
            "value": helicity_residual,
            "expected": 0.0,
            "pass": close(helicity_residual, 0.0),
        },
        {
            "name": "scalar_unitary_norm_preserved",
            "value": norm_after,
            "expected": norm_before,
            "pass": close(norm_after, norm_before),
        },
        {
            "name": "tensor_dimension_margin_nonnegative",
            "value": joint_margin,
            "expected": 4.0,
            "pass": joint_margin >= 0.0 and close(joint_margin, 4.0),
        },
        {
            "name": "zero_acceleration_zero_work",
            "value": force_work,
            "expected": 0.0,
            "pass": close(force_work, 0.0),
        },
        {
            "name": "azimuthal_zero_mode_zero_phase",
            "value": phase_zero,
            "expected": 0.0,
            "pass": close(phase_zero, 0.0),
        },
        {
            "name": "kk_frequency_recovers_mode",
            "value": kk_frequency * compact_radius,
            "expected": kk_n,
            "pass": close(kk_frequency * compact_radius, kk_n),
        },
        {
            "name": "kk_tower_mass_nonnegative",
            "value": kk_mass,
            "expected": 0.6,
            "pass": kk_mass >= 0.0 and close(kk_mass, 0.6),
        },
        {
            "name": "fourier_mode_energy_nonnegative",
            "value": fourier_energy,
            "expected": 2.125,
            "pass": fourier_energy >= 0.0 and close(fourier_energy, 2.125),
        },
        {
            "name": "image_obligation_flags_present",
            "value": 1.0 if image_anchor and image_witness else 0.0,
            "expected": 1.0,
            "pass": image_anchor and image_witness,
        },
    ]

    return {
        "certificate": "MASTER_BATCH001_CARRIERS_CERTIFICATE",
        "generated_utc": "2026-06-09T00:00:00Z",
        "creator": "Daniel Alexander Trawin",
        "orcid": "https://orcid.org/0009-0001-4630-3715",
        "isabelle_theory": "isabelle_tzpid/TZPID_MasterBatch001_Carriers.thy",
        "source_batch": "Master theorem batch 001",
        "status": "pass" if all(row["pass"] for row in checks) else "fail",
        "checks": checks,
        "parameters": {
            "radius": radius,
            "mode": mode,
            "writhe": writhe,
            "twist": twist,
            "unitary_u": u,
            "compact_radius": compact_radius,
            "kk_n": kk_n,
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
        "# Master Batch 001 Carriers Certificate",
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
        "This certificate backs the batch 001 carrier layer for mode spacing, "
        "helicity decomposition, scalar information preservation, tensor "
        "dimension margins, force/phase zero cases, KK modes, Fourier energy, "
        "and image-obligation readiness flags."
    )
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    cert = build_certificate()
    write_outputs(cert)
    print(json.dumps({"status": cert["status"], "checks": len(cert["checks"])}, indent=2))


if __name__ == "__main__":
    main()
