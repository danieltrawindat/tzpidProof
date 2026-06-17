#!/usr/bin/env python
"""Joint Hubble/Friedmann likelihood certificate.

Combines the locked Pantheon+, Planck distance-prior, and DESI DR2 BAO
certificate lanes by summing their chi-square values over the common scenario
set.  This is a reproducibility combiner, not a new parameter fit.
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path


OUT_DIR = Path("phase2_checks")

PANTHEON_JSON = OUT_DIR / "HUBBLE_PANTHEONPLUS_RAW_LIKELIHOOD_CERTIFICATE.json"
PLANCK_JSON = OUT_DIR / "HUBBLE_PLANCK_DISTANCE_PRIOR_CERTIFICATE.json"
DESI_JSON = OUT_DIR / "HUBBLE_DESI_DR2_BAO_LIKELIHOOD_CERTIFICATE.json"

PANTHEON_CSV = OUT_DIR / "HUBBLE_PANTHEONPLUS_RAW_SCENARIO_CHI2.csv"
PLANCK_CSV = OUT_DIR / "HUBBLE_PLANCK_DISTANCE_PRIOR_SCENARIO_CHI2.csv"
DESI_CSV = OUT_DIR / "HUBBLE_DESI_DR2_BAO_SCENARIO_CHI2.csv"

CERT_JSON = OUT_DIR / "HUBBLE_JOINT_LIKELIHOOD_CERTIFICATE.json"
CERT_MD = OUT_DIR / "HUBBLE_JOINT_LIKELIHOOD_CERTIFICATE.md"
JOINT_CSV = OUT_DIR / "HUBBLE_JOINT_SCENARIO_CHI2.csv"

LANES = [
    ("pantheon_plus_raw", PANTHEON_JSON, PANTHEON_CSV),
    ("planck_distance_prior", PLANCK_JSON, PLANCK_CSV),
    ("desi_dr2_bao", DESI_JSON, DESI_CSV),
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def read_rows(path: Path) -> dict[str, dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    return {row["name"]: row for row in rows}


def as_float(row: dict[str, str], key: str) -> float:
    return float(row[key])


def as_int(row: dict[str, str], key: str) -> int:
    return int(float(row[key]))


def lane_inputs() -> list[dict]:
    inputs = []
    for lane_name, json_path, csv_path in LANES:
        cert = read_json(json_path)
        rows = read_rows(csv_path)
        inputs.append(
            {
                "lane": lane_name,
                "json_path": str(json_path),
                "csv_path": str(csv_path),
                "json_sha256": sha256(json_path),
                "csv_sha256": sha256(csv_path),
                "overall_status": cert.get("overall_status"),
                "best_scenario_by_chi2": cert.get("best_scenario_by_chi2"),
                "scenario_count": len(rows),
                "rows": rows,
            }
        )
    return inputs


def common_scenarios(inputs: list[dict]) -> list[str]:
    scenario_sets = [set(item["rows"].keys()) for item in inputs]
    common = set.intersection(*scenario_sets)
    if not common:
        raise ValueError("no common scenarios across input lanes")
    if any(scenarios != common for scenarios in scenario_sets):
        raise ValueError("input lanes do not have identical scenario sets")
    return sorted(common)


def joint_rows(inputs: list[dict], scenario_names: list[str]) -> list[dict]:
    rows = []
    lookup = {item["lane"]: item["rows"] for item in inputs}
    for name in scenario_names:
        pantheon = lookup["pantheon_plus_raw"][name]
        planck = lookup["planck_distance_prior"][name]
        desi = lookup["desi_dr2_bao"][name]
        chi2_pantheon = as_float(pantheon, "chi2")
        chi2_planck = as_float(planck, "chi2")
        chi2_desi = as_float(desi, "chi2")
        dof_pantheon = as_int(pantheon, "dof")
        dof_planck = as_int(planck, "dof")
        dof_desi = as_int(desi, "dof")
        total_chi2 = chi2_pantheon + chi2_planck + chi2_desi
        total_dof = dof_pantheon + dof_planck + dof_desi
        rows.append(
            {
                "name": name,
                "role": pantheon["role"],
                "H0": as_float(pantheon, "H0"),
                "Omega_m": as_float(pantheon, "Omega_m"),
                "Omega_K": as_float(pantheon, "Omega_K"),
                "w0": as_float(pantheon, "w0"),
                "wa": as_float(pantheon, "wa"),
                "pantheon_chi2": chi2_pantheon,
                "pantheon_dof": dof_pantheon,
                "planck_chi2": chi2_planck,
                "planck_dof": dof_planck,
                "desi_chi2": chi2_desi,
                "desi_dof": dof_desi,
                "total_chi2": total_chi2,
                "total_dof": total_dof,
                "reduced_total_chi2": total_chi2 / total_dof,
                "delta_chi2_from_best": 0.0,
                "status": "computed",
            }
        )
    best_chi2 = min(row["total_chi2"] for row in rows)
    for row in rows:
        row["delta_chi2_from_best"] = row["total_chi2"] - best_chi2
    return sorted(rows, key=lambda row: row["total_chi2"])


def build_certificate() -> dict:
    inputs = lane_inputs()
    scenario_names = common_scenarios(inputs)
    rows = joint_rows(inputs, scenario_names)
    all_inputs_pass = all(item["overall_status"] == "pass" for item in inputs)
    finite_joint = all(math.isfinite(row["total_chi2"]) for row in rows)
    positive_dof = all(row["total_dof"] > 0 for row in rows)
    best = rows[0]
    return {
        "certificate": "HUBBLE_JOINT_LIKELIHOOD_CERTIFICATE",
        "generated_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "creator": "Daniel Alexander Trawin",
        "orcid": "https://orcid.org/0009-0001-4630-3715",
        "engine": "Python standard library",
        "claim_boundary": "Sum of locked Pantheon+, Planck distance-prior, and DESI DR2 BAO chi-square lanes; not a refit or full likelihood.",
        "input_lanes": [
            {key: value for key, value in item.items() if key != "rows"}
            for item in inputs
        ],
        "checks": {
            "input_certificates_pass": "pass" if all_inputs_pass else "fail",
            "common_scenario_set": "pass",
            "finite_joint_chi2": "pass" if finite_joint else "fail",
            "positive_joint_dof": "pass" if positive_dof else "fail",
            "joint_scenarios_computed": "computed",
        },
        "scenario_results": rows,
        "best_scenario_by_joint_chi2": best["name"],
        "best_joint_chi2": best["total_chi2"],
        "best_joint_dof": best["total_dof"],
        "best_reduced_joint_chi2": best["reduced_total_chi2"],
        "overall_status": "pass" if all_inputs_pass and finite_joint and positive_dof else "fail",
    }


def write_outputs(cert: dict) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    CERT_JSON.write_text(json.dumps(cert, indent=2), encoding="utf-8")

    fieldnames = [
        "name",
        "role",
        "H0",
        "Omega_m",
        "Omega_K",
        "w0",
        "wa",
        "pantheon_chi2",
        "pantheon_dof",
        "planck_chi2",
        "planck_dof",
        "desi_chi2",
        "desi_dof",
        "total_chi2",
        "total_dof",
        "reduced_total_chi2",
        "delta_chi2_from_best",
        "status",
    ]
    with JOINT_CSV.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows({field: row[field] for field in fieldnames} for row in cert["scenario_results"])

    input_rows = "\n".join(
        "| {lane} | {overall_status} | {scenario_count} | {best_scenario_by_chi2} | `{json_sha256}` |".format(
            **lane
        )
        for lane in cert["input_lanes"]
    )
    check_rows = "\n".join(
        f"| `{name}` | `{status}` |" for name, status in cert["checks"].items()
    )
    scenario_rows = "\n".join(
        "| {name} | {H0:.8g} | {Omega_K:.8g} | {w0:.8g} | {wa:.8g} | {pantheon_chi2:.8g} | {planck_chi2:.8g} | {desi_chi2:.8g} | {total_chi2:.8g} | {reduced_total_chi2:.8g} | {delta_chi2_from_best:.8g} |".format(
            **row
        )
        for row in cert["scenario_results"]
    )
    CERT_MD.write_text(
        f"""# Hubble/Friedmann Joint Likelihood Certificate

Generated UTC: `{cert["generated_utc"]}`

Creator: Daniel Alexander Trawin

ORCID: https://orcid.org/0009-0001-4630-3715

Engine: `{cert["engine"]}`

Overall status: `{cert["overall_status"]}`

## Claim Boundary

This certificate sums the locked Pantheon+ raw-covariance, Planck
distance-prior, and DESI DR2 BAO chi-square lanes over their common scenario
set. It is not a new parameter minimization, refit, or full survey likelihood.

## Input Lanes

| Lane | Status | Scenario count | Best lane scenario | JSON SHA256 |
|---|---|---:|---|---|
{input_rows}

## Checks

| Check | Status |
|---|---|
{check_rows}

## Joint Scenario Ranking

| Scenario | H0 | Omega_K | w0 | wa | Pantheon chi2 | Planck chi2 | DESI chi2 | Total chi2 | Reduced total | Delta chi2 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
{scenario_rows}

Best scenario by joint chi-square: `{cert["best_scenario_by_joint_chi2"]}`

Best reduced joint chi-square: `{cert["best_reduced_joint_chi2"]:.8g}`

## Files

- JSON certificate: `phase2_checks/HUBBLE_JOINT_LIKELIHOOD_CERTIFICATE.json`
- Scenario CSV: `phase2_checks/HUBBLE_JOINT_SCENARIO_CHI2.csv`

## Next Use

Promote the scenario-sum certificate into a small parameter-search lane over
`H0`, `Omega_m`, `Omega_K`, `w0`, and `wa`, while keeping this file as the
locked reproducibility baseline.
""",
        encoding="utf-8",
    )


def main() -> None:
    cert = build_certificate()
    write_outputs(cert)
    print(f"wrote {CERT_JSON}")
    print(f"wrote {CERT_MD}")
    print(f"wrote {JOINT_CSV}")
    print(f"overall_status={cert['overall_status']}")
    print(f"best_scenario_by_joint_chi2={cert['best_scenario_by_joint_chi2']}")
    print(f"best_reduced_joint_chi2={cert['best_reduced_joint_chi2']:.8g}")


if __name__ == "__main__":
    main()
