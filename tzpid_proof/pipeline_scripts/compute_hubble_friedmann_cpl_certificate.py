#!/usr/bin/env python
"""Generate a Phase 2 certificate for Hubble/Friedmann CPL dark energy.

This is a computational scaffold, not an observational fit.  It verifies the
closed-form CPL factor

    F(a) = exp(3 int_a^1 (1 + w(a')) / a' da')
    w(a) = w0 + wa (1 - a)

against direct numerical quadrature, then records parameter-style CMB/BAO/SN
anchors for later data-fitting work.
"""

from __future__ import annotations

import csv
import json
import math
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable


OUT_DIR = Path("phase2_checks")
JSON_OUT = OUT_DIR / "HUBBLE_FRIEDMANN_CPL_CERTIFICATE.json"
CSV_OUT = OUT_DIR / "HUBBLE_FRIEDMANN_CPL_ANCHORS.csv"
MD_OUT = OUT_DIR / "HUBBLE_FRIEDMANN_CPL_CERTIFICATE.md"


@dataclass(frozen=True)
class Scenario:
    name: str
    role: str
    h0_km_s_mpc: float
    omega_r: float
    omega_m: float
    omega_k: float
    omega_x: float
    w0: float
    wa: float


@dataclass(frozen=True)
class Anchor:
    scenario: str
    anchor: str
    z: float
    a: float
    f_a: float
    e_z: float
    h_z_km_s_mpc: float
    dimensionless_comoving_distance: float
    dimensionless_luminosity_distance: float
    status: str


SCENARIOS = [
    Scenario(
        name="lambda_cdm_flat_anchor",
        role="Planck-style flat LambdaCDM reference carrier",
        h0_km_s_mpc=67.4,
        omega_r=0.000092,
        omega_m=0.315,
        omega_k=0.0,
        omega_x=1.0 - 0.000092 - 0.315,
        w0=-1.0,
        wa=0.0,
    ),
    Scenario(
        name="closed_breathing_anchor",
        role="Closed-enclosure Friedmann carrier with small negative Omega_K",
        h0_km_s_mpc=67.4,
        omega_r=0.000092,
        omega_m=0.315,
        omega_k=-0.001,
        omega_x=1.0 - 0.000092 - 0.315 + 0.001,
        w0=-1.0,
        wa=0.0,
    ),
    Scenario(
        name="dynamic_cpl_demo",
        role="Non-fit CPL scaffold for future CMB/BAO/SN parameter scans",
        h0_km_s_mpc=67.4,
        omega_r=0.000092,
        omega_m=0.315,
        omega_k=0.0,
        omega_x=1.0 - 0.000092 - 0.315,
        w0=-0.95,
        wa=0.2,
    ),
]

ANCHOR_REDSHIFTS = [
    ("local_sn_low_z", 0.10),
    ("bao_boss_like_mid_z", 0.57),
    ("cmb_last_scattering_proxy", 1089.0),
]


def cpl_w(a: float, w0: float, wa: float) -> float:
    return w0 + wa * (1.0 - a)


def cpl_f_closed(a: float, w0: float, wa: float) -> float:
    if a <= 0:
        raise ValueError("scale factor a must be positive")
    return a ** (-3.0 * (1.0 + w0 + wa)) * math.exp(3.0 * wa * (a - 1.0))


def simpson_integral(fn: Callable[[float], float], lo: float, hi: float, n: int = 4000) -> float:
    if lo == hi:
        return 0.0
    if n % 2:
        n += 1
    sign = 1.0
    if hi < lo:
        lo, hi = hi, lo
        sign = -1.0
    h = (hi - lo) / n
    total = fn(lo) + fn(hi)
    for i in range(1, n):
        x = lo + i * h
        total += (4.0 if i % 2 else 2.0) * fn(x)
    return sign * total * h / 3.0


def cpl_f_quadrature(a: float, w0: float, wa: float) -> float:
    # Integrate in log-scale-factor u = log(a).  This removes the harmless
    # 1/a shape from the CPL integrand and keeps the CMB proxy point stable.
    integral = simpson_integral(
        lambda u: 1.0 + cpl_w(math.exp(u), w0, wa), math.log(a), 0.0
    )
    return math.exp(3.0 * integral)


def e_squared(s: Scenario, z: float) -> float:
    a = 1.0 / (1.0 + z)
    return (
        s.omega_r / a**4
        + s.omega_m / a**3
        + s.omega_k / a**2
        + s.omega_x * cpl_f_closed(a, s.w0, s.wa)
    )


def e_of_z(s: Scenario, z: float) -> float:
    value = e_squared(s, z)
    if value <= 0:
        raise ValueError(f"E(z)^2 is non-positive for {s.name} at z={z}")
    return math.sqrt(value)


def dimensionless_comoving_distance(s: Scenario, z: float) -> float:
    return simpson_integral(lambda zp: 1.0 / e_of_z(s, zp), 0.0, z, n=6000)


def make_anchor(s: Scenario, label: str, z: float) -> Anchor:
    a = 1.0 / (1.0 + z)
    f_a = cpl_f_closed(a, s.w0, s.wa)
    e_z = e_of_z(s, z)
    dc = dimensionless_comoving_distance(s, z)
    return Anchor(
        scenario=s.name,
        anchor=label,
        z=z,
        a=a,
        f_a=f_a,
        e_z=e_z,
        h_z_km_s_mpc=s.h0_km_s_mpc * e_z,
        dimensionless_comoving_distance=dc,
        dimensionless_luminosity_distance=(1.0 + z) * dc,
        status="computed",
    )


def build_certificate() -> dict:
    scale_grid = [1.0, 0.9, 0.75, 0.5, 0.25, 1.0 / 11.0, 1.0 / 1090.0]
    cpl_checks = []
    for s in SCENARIOS:
        for a in scale_grid:
            closed = cpl_f_closed(a, s.w0, s.wa)
            quadrature = cpl_f_quadrature(a, s.w0, s.wa)
            residual = abs(closed - quadrature)
            tolerance = max(1.0e-8, abs(closed) * 1.0e-8)
            cpl_checks.append(
                {
                    "scenario": s.name,
                    "a": a,
                    "w0": s.w0,
                    "wa": s.wa,
                    "closed_form_F": closed,
                    "quadrature_F": quadrature,
                    "absolute_residual": residual,
                    "tolerance": tolerance,
                    "status": "pass" if residual <= tolerance else "fail",
                }
            )

    anchors = [make_anchor(s, label, z) for s in SCENARIOS for label, z in ANCHOR_REDSHIFTS]
    all_pass = all(row["status"] == "pass" for row in cpl_checks)
    normalization_pass = all(
        abs(s.omega_r + s.omega_m + s.omega_k + s.omega_x - 1.0) <= 1.0e-12
        for s in SCENARIOS
    )
    lambda_unity_pass = all(
        abs(cpl_f_closed(a, -1.0, 0.0) - 1.0) <= 1.0e-12 for a in scale_grid
    )
    closed_curvature_pass = next(s.omega_k < 0 for s in SCENARIOS if s.name == "closed_breathing_anchor")

    return {
        "certificate": "HUBBLE_FRIEDMANN_CPL_CERTIFICATE",
        "generated_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "creator": "Daniel Alexander Trawin",
        "orcid": "https://orcid.org/0009-0001-4630-3715",
        "engine": "Python standard library",
        "claim_boundary": "Computational scaffold and parameter-style anchors, not an observational fit.",
        "equations": {
            "w_a": "w(a) = w0 + wa(1 - a)",
            "F_a_integral": "F(a) = exp(3 integral_a^1 (1 + w(a'))/a' da')",
            "F_a_closed_form": "F(a) = a^(-3(1+w0+wa)) exp(3 wa (a-1))",
            "E_z_squared": "E(z)^2 = Omega_r a^-4 + Omega_m a^-3 + Omega_K a^-2 + Omega_X F(a)",
        },
        "scenarios": [asdict(s) for s in SCENARIOS],
        "checks": {
            "cpl_closed_form_matches_quadrature": "pass" if all_pass else "fail",
            "present_epoch_component_normalization": "pass" if normalization_pass else "fail",
            "lambda_cdm_F_is_unity": "pass" if lambda_unity_pass else "fail",
            "closed_breathing_has_negative_omega_k": "pass" if closed_curvature_pass else "fail",
        },
        "cpl_grid_checks": cpl_checks,
        "anchors": [asdict(a) for a in anchors],
        "overall_status": "pass"
        if all_pass and normalization_pass and lambda_unity_pass and closed_curvature_pass
        else "fail",
    }


def write_outputs(certificate: dict) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    JSON_OUT.write_text(json.dumps(certificate, indent=2), encoding="utf-8")

    anchors = certificate["anchors"]
    with CSV_OUT.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(anchors[0].keys()))
        writer.writeheader()
        writer.writerows(anchors)

    check_rows = "\n".join(
        f"| `{name}` | `{status}` |" for name, status in certificate["checks"].items()
    )
    anchor_rows = "\n".join(
        "| {scenario} | {anchor} | {z:.5g} | {a:.8g} | {f_a:.8g} | {e_z:.8g} | {h_z_km_s_mpc:.8g} |".format(
            **anchor
        )
        for anchor in anchors
    )
    scenario_rows = "\n".join(
        "| {name} | {role} | {omega_r:.8g} | {omega_m:.8g} | {omega_k:.8g} | {omega_x:.8g} | {w0:.8g} | {wa:.8g} |".format(
            **scenario
        )
        for scenario in certificate["scenarios"]
    )
    MD_OUT.write_text(
        f"""# Hubble/Friedmann CPL Certificate

Generated UTC: `{certificate["generated_utc"]}`

Creator: Daniel Alexander Trawin

ORCID: https://orcid.org/0009-0001-4630-3715

Engine: `{certificate["engine"]}`

Overall status: `{certificate["overall_status"]}`

## Claim Boundary

This is a computational scaffold and parameter-style anchor set. It does not
claim an observational fit. It locks the dynamic dark-energy carrier used by
the Hubble-breathing Friedmann bridge.

## Equations

```text
w(a) = w0 + wa(1 - a)
F(a) = exp(3 integral_a^1 (1 + w(a'))/a' da')
F(a) = a^(-3(1+w0+wa)) exp(3 wa (a-1))
E(z)^2 = Omega_r a^-4 + Omega_m a^-3 + Omega_K a^-2 + Omega_X F(a)
```

## Checks

| Check | Status |
|---|---|
{check_rows}

## Scenarios

| Scenario | Role | Omega_r | Omega_m | Omega_K | Omega_X | w0 | wa |
|---|---|---:|---:|---:|---:|---:|---:|
{scenario_rows}

## Parameter-Style Anchors

| Scenario | Anchor | z | a | F(a) | E(z) | H(z) km/s/Mpc |
|---|---|---:|---:|---:|---:|---:|
{anchor_rows}

## Files

- JSON: `phase2_checks/HUBBLE_FRIEDMANN_CPL_CERTIFICATE.json`
- CSV: `phase2_checks/HUBBLE_FRIEDMANN_CPL_ANCHORS.csv`

## Next Use

This certificate can be promoted into a real fit lane by replacing the anchor
redshifts with an observed CMB/BAO/SN data table and minimizing residuals over
`H0`, `Omega_m`, `Omega_K`, `w0`, and `wa`.
""",
        encoding="utf-8",
    )


def main() -> None:
    certificate = build_certificate()
    write_outputs(certificate)
    print(f"wrote {JSON_OUT}")
    print(f"wrote {CSV_OUT}")
    print(f"wrote {MD_OUT}")
    print(f"overall_status={certificate['overall_status']}")


if __name__ == "__main__":
    main()
