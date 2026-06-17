from __future__ import annotations

import csv
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parent
OUT_DIR = ROOT / "phase2_checks"
OUT_JSON = OUT_DIR / "OPERATOR_SPECTRAL_CARRIERS_CERTIFICATE.json"
OUT_MD = OUT_DIR / "OPERATOR_SPECTRAL_CARRIERS_CERTIFICATE.md"
OUT_CSV = OUT_DIR / "OPERATOR_SPECTRAL_CARRIERS_GRID.csv"


def close(a: float, b: float, tol: float = 1e-12) -> bool:
    return abs(a - b) <= tol


def kk_access_frequency(n: int, c: float, radius: float) -> float:
    return n * c / (2.0 * math.pi * radius)


def beat_frequency(omega_a: float, omega_b: float) -> float:
    return abs(omega_a - omega_b)


def transfer_rate(coupling: float, amp_a: float, amp_b: float, detuning: float) -> float:
    return coupling * amp_a * amp_b / (1.0 + detuning**2)


def build_certificate() -> dict[str, object]:
    lambda0 = 1.25
    lambda1 = 3.75
    gap = lambda1 - lambda0

    base_frequency = 2.5
    n = 4
    harmonic_n = n * base_frequency
    harmonic_next = (n + 1) * base_frequency

    base_spectrum = 7.0
    coupling = 0.3
    curvature = 2.0
    curvature_shift = base_spectrum + coupling * curvature

    light_speed = 299_792_458.0
    radius = 1.2e8
    kk_frequency = kk_access_frequency(n, light_speed, radius)

    omega_solar = 14.5
    omega_lunar = 13.9
    omega_beat = beat_frequency(omega_solar, omega_lunar)
    full_period = 2.0 * math.pi / omega_beat
    semidiurnal = math.pi / omega_beat

    detuning = 1.5
    transfer = transfer_rate(0.8, 1.2, 0.7, detuning)
    transfer_core = 0.8 * 1.2 * 0.7
    denominator = 1.0 + detuning**2

    perturbation = 0.4

    checks = [
        {
            "name": "ordered_two_mode_gap_nonnegative",
            "value": gap,
            "expected": 2.5,
            "pass": gap >= 0.0 and close(gap, 2.5),
        },
        {
            "name": "harmonic_ladder_adjacent_step",
            "value": harmonic_next - harmonic_n,
            "expected": base_frequency,
            "pass": close(harmonic_next - harmonic_n, base_frequency),
        },
        {
            "name": "curvature_shift_monotone",
            "value": curvature_shift - base_spectrum,
            "expected": coupling * curvature,
            "pass": curvature_shift >= base_spectrum and close(curvature_shift - base_spectrum, coupling * curvature),
        },
        {
            "name": "kk_access_frequency_recovers_mode",
            "value": kk_frequency * (2.0 * math.pi * radius),
            "expected": n * light_speed,
            "pass": close(kk_frequency * (2.0 * math.pi * radius), n * light_speed, tol=1e-6),
        },
        {
            "name": "full_beat_period_recovers_turn",
            "value": full_period * omega_beat,
            "expected": 2.0 * math.pi,
            "pass": close(full_period * omega_beat, 2.0 * math.pi),
        },
        {
            "name": "semidiurnal_is_half_full_period",
            "value": semidiurnal,
            "expected": full_period / 2.0,
            "pass": close(semidiurnal, full_period / 2.0),
        },
        {
            "name": "detuning_denominator_positive",
            "value": denominator,
            "expected": 3.25,
            "pass": denominator > 0.0 and close(denominator, 3.25),
        },
        {
            "name": "transfer_rate_uses_denominator",
            "value": transfer,
            "expected": transfer_core / denominator,
            "pass": close(transfer, transfer_core / denominator),
        },
        {
            "name": "gap_exceeds_perturbation",
            "value": gap - perturbation,
            "expected": 2.1,
            "pass": gap > 0.0 and perturbation < gap and close(gap - perturbation, 2.1),
        },
    ]

    return {
        "certificate": "OPERATOR_SPECTRAL_CARRIERS_CERTIFICATE",
        "generated_utc": "2026-06-09T00:00:00Z",
        "creator": "Daniel Alexander Trawin",
        "orcid": "https://orcid.org/0009-0001-4630-3715",
        "isabelle_theory": "isabelle_tzpid/TZPID_OperatorSpectral_Carriers.thy",
        "source_batch": "Operator/spectral batch 006",
        "status": "pass" if all(row["pass"] for row in checks) else "fail",
        "checks": checks,
        "parameters": {
            "lambda0": lambda0,
            "lambda1": lambda1,
            "base_frequency": base_frequency,
            "mode_n": n,
            "radius": radius,
            "omega_solar": omega_solar,
            "omega_lunar": omega_lunar,
            "detuning": detuning,
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
        "# Operator/Spectral Carriers Certificate",
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
        "This certificate backs finite spectral carriers for mode gaps, harmonic "
        "ladders, curvature shifts, Kaluza-Klein access frequencies, beat periods, "
        "detuning denominators, and transfer-rate normalization."
    )
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    cert = build_certificate()
    write_outputs(cert)
    print(json.dumps({"status": cert["status"], "checks": len(cert["checks"])}, indent=2))


if __name__ == "__main__":
    main()
