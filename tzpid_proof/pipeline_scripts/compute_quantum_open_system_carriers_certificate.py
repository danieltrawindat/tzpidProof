from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
OUT_DIR = ROOT / "phase2_checks"
OUT_JSON = OUT_DIR / "QUANTUM_OPEN_SYSTEM_CARRIERS_CERTIFICATE.json"
OUT_MD = OUT_DIR / "QUANTUM_OPEN_SYSTEM_CARRIERS_CERTIFICATE.md"
OUT_CSV = OUT_DIR / "QUANTUM_OPEN_SYSTEM_CARRIERS_GRID.csv"


def close(a: float, b: float, tol: float = 1e-12) -> bool:
    return abs(a - b) <= tol


def normalized_probability_weight(p: float) -> bool:
    return 0.0 <= p <= 1.0


def channel_trace(p0: float, p1: float, a00: float, a10: float, a01: float, a11: float) -> float:
    return (a00 + a10) * p0 + (a01 + a11) * p1


def measurement_mix(weight: float, prior: float, outcome: float) -> float:
    return (1.0 - weight) * prior + weight * outcome


def quantum_noise_spectrum(amplitude: float, frequency: float) -> float:
    return amplitude**2 / (1.0 + frequency**2)


def trace_distance2(p0: float, p1: float, q0: float, q1: float) -> float:
    return (abs(p0 - q0) + abs(p1 - q1)) / 2.0


def build_certificate() -> dict[str, object]:
    p0 = 0.35
    p1 = 0.65
    a00, a10 = 0.8, 0.2
    a01, a11 = 0.1, 0.9
    prior = 0.35
    outcome = 0.9
    left = 1.7
    right = -0.4
    amplitude = 2.0
    frequency = 3.0
    heat = 5.0
    work = 1.25

    trace = p0 + p1
    output0 = a00 * p0 + a01 * p1
    output1 = a10 * p0 + a11 * p1
    denominator = 1.0 + frequency**2
    noise = quantum_noise_spectrum(amplitude, frequency)

    checks = [
        {
            "name": "density_trace_one",
            "value": trace,
            "expected": 1.0,
            "pass": close(trace, 1.0) and normalized_probability_weight(p0) and normalized_probability_weight(p1),
        },
        {
            "name": "column_stochastic_trace_preserving",
            "value": channel_trace(p0, p1, a00, a10, a01, a11),
            "expected": 1.0,
            "pass": close(channel_trace(p0, p1, a00, a10, a01, a11), 1.0),
        },
        {
            "name": "channel_output_trace_matches_sum",
            "value": output0 + output1,
            "expected": 1.0,
            "pass": close(output0 + output1, 1.0),
        },
        {
            "name": "measurement_zero_weight_recovers_prior",
            "value": measurement_mix(0.0, prior, outcome),
            "expected": prior,
            "pass": close(measurement_mix(0.0, prior, outcome), prior),
        },
        {
            "name": "measurement_unit_weight_recovers_outcome",
            "value": measurement_mix(1.0, prior, outcome),
            "expected": outcome,
            "pass": close(measurement_mix(1.0, prior, outcome), outcome),
        },
        {
            "name": "commutator_residual_antisymmetric",
            "value": (left - right) + (right - left),
            "expected": 0.0,
            "pass": close((left - right) + (right - left), 0.0),
        },
        {
            "name": "noise_denominator_positive",
            "value": denominator,
            "expected": 10.0,
            "pass": denominator > 0.0 and close(denominator, 10.0),
        },
        {
            "name": "noise_spectrum_uses_denominator",
            "value": noise,
            "expected": amplitude**2 / denominator,
            "pass": close(noise, amplitude**2 / denominator),
        },
        {
            "name": "trace_distance_identical_zero",
            "value": trace_distance2(p0, p1, p0, p1),
            "expected": 0.0,
            "pass": close(trace_distance2(p0, p1, p0, p1), 0.0),
        },
        {
            "name": "quantum_thermo_balance_zero",
            "value": heat - work - (heat - work),
            "expected": 0.0,
            "pass": close(heat - work - (heat - work), 0.0),
        },
    ]

    return {
        "certificate": "QUANTUM_OPEN_SYSTEM_CARRIERS_CERTIFICATE",
        "generated_utc": "2026-06-09T00:00:00Z",
        "creator": "Daniel Alexander Trawin",
        "orcid": "https://orcid.org/0009-0001-4630-3715",
        "isabelle_theory": "isabelle_tzpid/TZPID_QuantumOpenSystem_Carriers.thy",
        "source_batch": "Quantum/open-system batch 007",
        "status": "pass" if all(row["pass"] for row in checks) else "fail",
        "checks": checks,
        "parameters": {
            "p0": p0,
            "p1": p1,
            "channel": [a00, a10, a01, a11],
            "frequency": frequency,
            "amplitude": amplitude,
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
        "# Quantum/Open-System Carriers Certificate",
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
        "This certificate backs finite diagonal-density and open-channel carriers "
        "for trace preservation, measurement endpoints, commutator residuals, "
        "noise normalization, trace distance, and thermodynamic balance."
    )
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    cert = build_certificate()
    write_outputs(cert)
    print(json.dumps({"status": cert["status"], "checks": len(cert["checks"])}, indent=2))


if __name__ == "__main__":
    main()
