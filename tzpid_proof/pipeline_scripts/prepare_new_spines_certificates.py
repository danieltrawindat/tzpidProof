import argparse
import hashlib
import json
import re
from pathlib import Path

from tzpid_provenance import generated_utc, isabelle_text


DEFAULT_WOLFRAM_DIR = "wolfram_checks"
DEFAULT_OUTPUT_DIR = "isabelle_tzpid"

RESULT_FILES = [
    "gravity_spine_results.json",
    "energy_matter_spine_results.json",
    "topo_unification_spine_results.json",
]

CHECK_CONSTRUCTORS = {
    "grav_newtonian_recovery": "Gravity_Newtonian_Recovery",
    "grav_stress_vanishes": "Gravity_Stress_Vanishes",
    "grav_poisson_dim_balance": "Gravity_Poisson_Dim_Balance",
    "em_regularization_finite": "EnergyMatter_Regularization_Finite",
    "em_creation_threshold": "EnergyMatter_Creation_Threshold",
    "em_mass_energy_identity": "EnergyMatter_Mass_Energy_Identity",
    "topo_chern_quantization": "Topo_Chen_Quantization",
    "topo_obstruction_nonvanishing": "Topo_Obstruction_Nonvanishing",
    "topo_invariant_decomposition": "Topo_Invariant_Decomposition",
}


def file_sha1(path):
    digest = hashlib.sha1()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def ascii_clean(value, max_len=500):
    text = "" if value is None else str(value)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = text.replace("\\", "/")
    text = text.replace("''", "'")
    text = re.sub(r"\s+", " ", text).strip()
    return text[:max_len]


def isa_string(value, max_len=500):
    return "''" + ascii_clean(value, max_len=max_len) + "''"


def constructor_for(row):
    check = row.get("check", "")
    if check in CHECK_CONSTRUCTORS:
        return CHECK_CONSTRUCTORS[check]
    safe = re.sub(r"[^A-Za-z0-9]+", "_", check).strip("_")
    return "NewSpine_" + safe


def read_results(wolfram_dir):
    rows = []
    sha_parts = []
    for filename in RESULT_FILES:
        path = Path(wolfram_dir, filename)
        data = json.loads(path.read_text(encoding="utf-8"))
        rows.extend(data)
        sha_parts.append(f"{filename}:{file_sha1(path)}")
    return rows, hashlib.sha1("|".join(sha_parts).encode("utf-8")).hexdigest()


def write_theory(path, rows, aggregate_sha, generated_at_utc):
    constructors = [constructor_for(row) for row in rows]
    datatype_lines = "\n  | ".join(constructors)
    status_cases = []
    id_cases = []
    note_cases = []
    for row in rows:
        ctor = constructor_for(row)
        status_cases.append(f"{ctor} => {isa_string(row.get('status', ''), 80)}")
        id_cases.append(f"{ctor} => {isa_string(row.get('id', ''), 20)}")
        note_cases.append(f"{ctor} => {isa_string(row.get('notes', ''), 700)}")

    def case_body(cases):
        return " | ".join(cases)

    provenance = isabelle_text(
        "prepare_new_spines_certificates.py",
        [f"new spine Wolfram result aggregate SHA1 {aggregate_sha}"],
        generated_at_utc,
        "Wolfram-backed certificate layer for the three curated new gold spines.",
    )

    text = f"""theory TZPID_NewSpines_Computational_Checks
  imports
    TZPID_Gravity_Focus
    TZPID_EnergyMatter_Focus
    TZPID_TopologicalUnification_Focus
begin

{provenance}

text \\<open>
  Wolfram-backed certificate layer for the three new curated gold spines.
\\<close>

datatype new_spine_check =
  {datatype_lines}

definition new_spines_wolfram_results_sha1 :: string where
  "new_spines_wolfram_results_sha1 = {isa_string(aggregate_sha)}"

definition new_spine_check_status :: "new_spine_check => string" where
  "new_spine_check_status check = (case check of {case_body(status_cases)})"

definition new_spine_check_registry_id :: "new_spine_check => string" where
  "new_spine_check_registry_id check = (case check of {case_body(id_cases)})"

definition new_spine_check_notes :: "new_spine_check => string" where
  "new_spine_check_notes check = (case check of {case_body(note_cases)})"

definition new_spine_verified_check :: "new_spine_check => bool" where
  "new_spine_verified_check check = (new_spine_check_status check = ''pass'')"

lemma gravity_newtonian_recovery_passed:
  "new_spine_verified_check Gravity_Newtonian_Recovery"
  by (simp add: new_spine_verified_check_def new_spine_check_status_def)

lemma gravity_stress_vanishes_passed:
  "new_spine_verified_check Gravity_Stress_Vanishes"
  by (simp add: new_spine_verified_check_def new_spine_check_status_def)

lemma gravity_poisson_dim_balance_passed:
  "new_spine_verified_check Gravity_Poisson_Dim_Balance"
  by (simp add: new_spine_verified_check_def new_spine_check_status_def)

lemma energy_matter_regularization_finite_passed:
  "new_spine_verified_check EnergyMatter_Regularization_Finite"
  by (simp add: new_spine_verified_check_def new_spine_check_status_def)

lemma energy_matter_creation_threshold_passed:
  "new_spine_verified_check EnergyMatter_Creation_Threshold"
  by (simp add: new_spine_verified_check_def new_spine_check_status_def)

lemma energy_matter_mass_energy_identity_passed:
  "new_spine_verified_check EnergyMatter_Mass_Energy_Identity"
  by (simp add: new_spine_verified_check_def new_spine_check_status_def)

lemma topo_chern_quantization_passed:
  "new_spine_verified_check Topo_Chen_Quantization"
  by (simp add: new_spine_verified_check_def new_spine_check_status_def)

lemma topo_obstruction_nonvanishing_passed:
  "new_spine_verified_check Topo_Obstruction_Nonvanishing"
  by (simp add: new_spine_verified_check_def new_spine_check_status_def)

lemma topo_invariant_decomposition_passed:
  "new_spine_verified_check Topo_Invariant_Decomposition"
  by (simp add: new_spine_verified_check_def new_spine_check_status_def)

context TZPID_Gravity_Focus
begin

theorem gravity_spine_has_wolfram_certificate:
  "new_spine_verified_check Gravity_Newtonian_Recovery
    & new_spine_verified_check Gravity_Stress_Vanishes
    & new_spine_verified_check Gravity_Poisson_Dim_Balance
    & accumulated_mass_functional G_M_acc
    & far_field_newtonian_recovery G_a_modified G_a_N
    & poisson_limit_closure G_Phi G_eff G_rho"
  using gravity_newtonian_recovery_passed gravity_stress_vanishes_passed
    gravity_poisson_dim_balance_passed gravity_accumulated_force_spine
  by simp

end

context TZPID_EnergyMatter_Focus
begin

theorem energy_matter_spine_has_wolfram_certificate:
  "new_spine_verified_check EnergyMatter_Regularization_Finite
    & new_spine_verified_check EnergyMatter_Creation_Threshold
    & new_spine_verified_check EnergyMatter_Mass_Energy_Identity
    & tzp_vacuum_energy_density EM_rho_vac_T
    & regularized_vacuum_energy EM_E_reg EM_E_naive
    & matter_creation_pressure_threshold EM_P_vac EM_P_crit
    & mass_energy_equivalence EM_energy EM_mass"
  using energy_matter_regularization_finite_passed energy_matter_creation_threshold_passed
    energy_matter_mass_energy_identity_passed energy_to_matter_logic_spine
  by simp

end

context TZPID_TopologicalUnification_Focus
begin

theorem topological_unification_spine_has_wolfram_certificate:
  "new_spine_verified_check Topo_Chen_Quantization
    & new_spine_verified_check Topo_Obstruction_Nonvanishing
    & new_spine_verified_check Topo_Invariant_Decomposition
    & chern_number_quantized Topo_C1
    & assembled_topological_invariant Topo_Omega Topo_C1 Topo_Lk
    & topological_unified_field_equation Topo_hmunu Topo_Omega"
  using topo_chern_quantization_passed topo_obstruction_nonvanishing_passed
    topo_invariant_decomposition_passed topological_unification_spine
  by simp

end

end
"""
    Path(path).write_text(text, encoding="utf-8")


def write_summary(path, rows, aggregate_sha, generated_at_utc):
    lines = [
        "# New Gold Spine Wolfram Certificates",
        "",
        "Project: TZPID Proof Pipeline",
        "Creator: Daniel Alexander Trawin",
        "ORCID: https://orcid.org/0009-0001-4630-3715",
        "Generator: prepare_new_spines_certificates.py",
        f"Generated UTC: {generated_at_utc}",
        "",
        f"Aggregate SHA1: `{aggregate_sha}`",
        "",
        "| ID | Check | Status | Notes |",
        "|---|---|---|---|",
    ]
    for row in rows:
        lines.append(
            f"| {row.get('id', '')} | `{row.get('check', '')}` | `{row.get('status', '')}` | {ascii_clean(row.get('notes', ''), 240)} |"
        )
    Path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")


def update_root(root_path):
    root = Path(root_path)
    text = root.read_text(encoding="utf-8")
    theory = "TZPID_NewSpines_Computational_Checks"
    if theory not in text:
        text = text.rstrip() + f"\n    {theory}\n"
    root.write_text(text, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--wolfram-dir", default=DEFAULT_WOLFRAM_DIR)
    parser.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()

    out = Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)
    rows, aggregate_sha = read_results(args.wolfram_dir)
    generated_at_utc = generated_utc()
    write_theory(out / "TZPID_NewSpines_Computational_Checks.thy", rows, aggregate_sha, generated_at_utc)
    write_summary(out / "new_spines_wolfram_certificate_summary.md", rows, aggregate_sha, generated_at_utc)
    update_root(out / "ROOT")
    print("Wrote new spine Isabelle certificate theory")


if __name__ == "__main__":
    main()
