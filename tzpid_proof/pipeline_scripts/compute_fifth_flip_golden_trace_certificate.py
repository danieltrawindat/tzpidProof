#!/usr/bin/env python
"""Generate a Phase 2 certificate for the fifth-flip golden trace.

This certificate backs ``TZPID_FifthFlip_CrystalScaleInvariance.thy`` by
checking the trigonometric/crystallographic hinge:

    phi = (1 + sqrt(5))/2
    1/phi = phi - 1
    2 cos(72 degrees) = 1/phi

The certificate also records that the fivefold trace lies strictly between 0
and 1 and is therefore not one of the integer traces {-2,-1,0,1,2} used by
periodic lattice rotation restrictions.
"""

from __future__ import annotations

import csv
import json
import math
from datetime import datetime, timezone
from pathlib import Path


OUT_DIR = Path("phase2_checks")
JSON_OUT = OUT_DIR / "FIFTH_FLIP_GOLDEN_TRACE_CERTIFICATE.json"
CSV_OUT = OUT_DIR / "FIFTH_FLIP_GOLDEN_TRACE_VALUES.csv"
MD_OUT = OUT_DIR / "FIFTH_FLIP_GOLDEN_TRACE_CERTIFICATE.md"


def build_rows() -> list[dict[str, float | str]]:
    phi = (1.0 + math.sqrt(5.0)) / 2.0
    golden_reciprocal = 1.0 / phi
    phi_minus_one = phi - 1.0
    fivefold_trace = 2.0 * math.cos(2.0 * math.pi / 5.0)
    pentagon_diagonal_ratio = phi
    musical_fifth = 3.0 / 2.0
    descending_fifth = 2.0 / 3.0
    return [
        {
            "quantity": "phi",
            "value": phi,
            "expected": phi,
            "absolute_residual": 0.0,
            "role": "positive golden fixed point",
        },
        {
            "quantity": "phi_squared_minus_phi_minus_one",
            "value": phi * phi - phi - 1.0,
            "expected": 0.0,
            "absolute_residual": abs(phi * phi - phi - 1.0),
            "role": "golden fixed-point residual",
        },
        {
            "quantity": "golden_reciprocal_minus_phi_minus_one",
            "value": golden_reciprocal - phi_minus_one,
            "expected": 0.0,
            "absolute_residual": abs(golden_reciprocal - phi_minus_one),
            "role": "reciprocal flip identity",
        },
        {
            "quantity": "fivefold_trace",
            "value": fivefold_trace,
            "expected": golden_reciprocal,
            "absolute_residual": abs(fivefold_trace - golden_reciprocal),
            "role": "2 cos(72 degrees) equals 1/phi",
        },
        {
            "quantity": "pentagon_diagonal_ratio",
            "value": pentagon_diagonal_ratio,
            "expected": phi,
            "absolute_residual": abs(pentagon_diagonal_ratio - phi),
            "role": "fivefold geometric scale ratio",
        },
        {
            "quantity": "musical_fifth_reciprocal",
            "value": 1.0 / musical_fifth,
            "expected": descending_fifth,
            "absolute_residual": abs((1.0 / musical_fifth) - descending_fifth),
            "role": "3/2 reciprocal flip to 2/3",
        },
    ]


def build_certificate() -> dict:
    rows = build_rows()
    tolerance = 1.0e-12
    value_map = {row["quantity"]: float(row["value"]) for row in rows}
    residual_map = {row["quantity"]: float(row["absolute_residual"]) for row in rows}
    fivefold_trace = value_map["fivefold_trace"]
    integer_traces = {-2, -1, 0, 1, 2}
    checks = {
        "golden_fixed_point": residual_map["phi_squared_minus_phi_minus_one"] <= tolerance,
        "golden_reciprocal_identity": residual_map[
            "golden_reciprocal_minus_phi_minus_one"
        ]
        <= tolerance,
        "fivefold_trace_equals_golden_reciprocal": residual_map["fivefold_trace"]
        <= tolerance,
        "fivefold_trace_open_unit_interval": 0.0 < fivefold_trace < 1.0,
        "fivefold_trace_not_integer_crystal_trace": all(
            abs(fivefold_trace - trace) > tolerance for trace in integer_traces
        ),
        "musical_fifth_flip": residual_map["musical_fifth_reciprocal"] <= tolerance,
    }
    all_pass = all(checks.values())
    return {
        "certificate": "FIFTH_FLIP_GOLDEN_TRACE_CERTIFICATE",
        "generated_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "creator": "Daniel Alexander Trawin",
        "orcid": "https://orcid.org/0009-0001-4630-3715",
        "engine": "Python standard library",
        "claim_boundary": (
            "Computational/trigonometric certificate for the golden trace hinge; "
            "not a full crystallographic restriction proof."
        ),
        "equations": {
            "phi": "phi = (1 + sqrt(5))/2",
            "golden_fixed_point": "phi^2 = phi + 1",
            "golden_reciprocal": "1/phi = phi - 1",
            "fivefold_trace": "2 cos(2 pi / 5) = 1/phi",
            "crystal_trace_guard": "2 cos(2 pi / 5) notin {-2,-1,0,1,2}",
        },
        "checks": {key: "pass" if value else "fail" for key, value in checks.items()},
        "values": rows,
        "tolerance": tolerance,
        "status": "pass" if all_pass else "fail",
    }


def write_outputs(certificate: dict) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    JSON_OUT.write_text(json.dumps(certificate, indent=2), encoding="utf-8")

    with CSV_OUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "quantity",
                "value",
                "expected",
                "absolute_residual",
                "role",
            ],
        )
        writer.writeheader()
        writer.writerows(certificate["values"])

    lines = [
        "# Fifth-Flip Golden Trace Certificate",
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
    lines.extend(["", "## Values", ""])
    for row in certificate["values"]:
        lines.append(
            "- `{quantity}`: value `{value:.15g}`, expected `{expected:.15g}`, residual `{absolute_residual:.3g}`".format(
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
