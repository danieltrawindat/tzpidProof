import argparse
import hashlib
import json
import re
from pathlib import Path


DEFAULT_RESULTS = "wolfram_checks/einstein_focus_results.json"
DEFAULT_OUTPUT_DIR = "isabelle_tzpid"


CHECK_CONSTRUCTORS = {
    ("ID0335", "far_field_classical_einstein_limit"): "Wolfram_ID0335_Far_Field_Classical_Einstein_Limit",
    ("ID0400", "density_side_dimensional_balance"): "Wolfram_ID0400_Density_Side_Dimensional_Balance",
    ("ID0400", "direct_hubble_square_dimension"): "Wolfram_ID0400_Direct_Hubble_Square_Dimension",
    ("ID0400", "critical_density_normalized_hubble_square"): "Wolfram_ID0400_Critical_Density_Normalized_Hubble_Square",
    ("ID0400", "omega_lambda_observed_density_match"): "Wolfram_ID0400_Omega_Lambda_Observed_Density_Match",
    ("ID0400", "observed_density_flux_ratio_requirement"): "Wolfram_ID0400_Observed_Density_Flux_Ratio_Requirement",
    ("ID0394", "perfect_fluid_vacuum_tensor_form"): "Wolfram_ID0394_Perfect_Fluid_Vacuum_Tensor_Form",
    ("ID0394", "bessel_inverse_density_profile"): "Wolfram_ID0394_Bessel_Inverse_Density_Profile",
    ("ID0167", "total_stress_energy_decomposition"): "Wolfram_ID0167_Total_Stress_Energy_Decomposition",
    ("ID0167", "vacuum_component_tzp_handoff"): "Wolfram_ID0167_Vacuum_Component_TZP_Handoff",
    ("ID0167", "componentwise_conservation_linearity"): "Wolfram_ID0167_Componentwise_Conservation_Linearity",
    ("ID0958", "wave_operator_source_relation"): "Wolfram_ID0958_Wave_Operator_Source_Relation",
    ("ID0958", "effective_einstein_sector_relation"): "Wolfram_ID0958_Effective_Einstein_Sector_Relation",
    ("ID0958", "unified_lagrangian_decomposition"): "Wolfram_ID0958_Unified_Lagrangian_Decomposition",
    ("ID0958", "action_generates_effective_einstein_sector"): "Wolfram_ID0958_Action_Generates_Effective_Einstein_Sector",
}


FOCUS_CONSTRUCTORS = {
    "ID0335": "Focus_ID0335",
    "ID0400": "Focus_ID0400",
    "ID1392": "Focus_ID1392",
    "ID0167": "Focus_ID0167",
    "ID0394": "Focus_ID0394",
    "ID0958": "Focus_ID0958",
}


def sha1_file(path):
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
    key = (row.get("id", ""), row.get("check", ""))
    if key in CHECK_CONSTRUCTORS:
        return CHECK_CONSTRUCTORS[key]
    raw = "_".join(key)
    safe = re.sub(r"[^A-Za-z0-9]+", "_", raw).strip("_")
    return "Wolfram_" + safe


def write_theory(path, rows, results_sha):
    constructors = [constructor_for(row) for row in rows]
    datatype_lines = "\n  | ".join(constructors)

    status_cases = []
    registry_cases = []
    check_name_cases = []
    note_cases = []
    for row in rows:
        ctor = constructor_for(row)
        focus = FOCUS_CONSTRUCTORS.get(row.get("id", ""), "Focus_ID0400")
        status_cases.append(f"{ctor} => {isa_string(row.get('status', ''), 80)}")
        registry_cases.append(f"{ctor} => {focus}")
        check_name_cases.append(f"{ctor} => {isa_string(row.get('check', ''), 160)}")
        note_cases.append(f"{ctor} => {isa_string(row.get('notes', ''), 700)}")

    def case_body(cases):
        return " | ".join(cases)

    theory = f"""theory TZPID_Einstein_Computational_Checks
  imports TZPID_Einstein_Focus
begin

text \\<open>
  Wolfram-backed certificate layer for the focused Einstein/cosmology branch.
  The JSON result file is treated as an external computational certificate:
  pass statuses become checked predicates, while dimensional gaps become
  explicit normalization obligations.
\\<close>

datatype wolfram_focus_check =
  {datatype_lines}

definition wolfram_einstein_focus_results_sha1 :: string where
  \"wolfram_einstein_focus_results_sha1 = {isa_string(results_sha)}\"

definition wolfram_check_status :: \"wolfram_focus_check => string\" where
  \"wolfram_check_status check = (case check of {case_body(status_cases)})\"

definition wolfram_check_registry_id :: \"wolfram_focus_check => tzpid_einstein_focus_id\" where
  \"wolfram_check_registry_id check = (case check of {case_body(registry_cases)})\"

definition wolfram_check_name :: \"wolfram_focus_check => string\" where
  \"wolfram_check_name check = (case check of {case_body(check_name_cases)})\"

definition wolfram_check_notes :: \"wolfram_focus_check => string\" where
  \"wolfram_check_notes check = (case check of {case_body(note_cases)})\"

definition wolfram_verified_check :: \"wolfram_focus_check => bool\" where
  \"wolfram_verified_check check = (wolfram_check_status check = ''pass'')\"

definition wolfram_normalization_obligation :: \"wolfram_focus_check => bool\" where
  \"wolfram_normalization_obligation check = (wolfram_check_status check = ''needs_normalization'')\"

definition wolfram_computed_check :: \"wolfram_focus_check => bool\" where
  \"wolfram_computed_check check = (wolfram_check_status check = ''computed'')\"

definition wolfram_review_check :: \"wolfram_focus_check => bool\" where
  \"wolfram_review_check check = (wolfram_check_status check = ''review'')\"

lemma id0335_wolfram_far_field_reduction_passed:
  \"wolfram_verified_check Wolfram_ID0335_Far_Field_Classical_Einstein_Limit\"
  by (simp add: wolfram_verified_check_def wolfram_check_status_def)

lemma id0400_wolfram_density_dimension_passed:
  \"wolfram_verified_check Wolfram_ID0400_Density_Side_Dimensional_Balance\"
  by (simp add: wolfram_verified_check_def wolfram_check_status_def)

lemma id0400_hubble_square_requires_normalization:
  \"wolfram_normalization_obligation Wolfram_ID0400_Direct_Hubble_Square_Dimension\"
  by (simp add: wolfram_normalization_obligation_def wolfram_check_status_def)

lemma id0400_critical_density_normalized_hubble_square_passed:
  \"wolfram_verified_check Wolfram_ID0400_Critical_Density_Normalized_Hubble_Square\"
  by (simp add: wolfram_verified_check_def wolfram_check_status_def)

lemma id0400_omega_lambda_observed_density_match_passed:
  \"wolfram_verified_check Wolfram_ID0400_Omega_Lambda_Observed_Density_Match\"
  by (simp add: wolfram_verified_check_def wolfram_check_status_def)

lemma id0400_flux_ratio_requirement_computed:
  \"wolfram_computed_check Wolfram_ID0400_Observed_Density_Flux_Ratio_Requirement\"
  by (simp add: wolfram_computed_check_def wolfram_check_status_def)

lemma id0394_perfect_fluid_vacuum_tensor_form_passed:
  \"wolfram_verified_check Wolfram_ID0394_Perfect_Fluid_Vacuum_Tensor_Form\"
  by (simp add: wolfram_verified_check_def wolfram_check_status_def)

lemma id0394_bessel_inverse_density_profile_passed:
  \"wolfram_verified_check Wolfram_ID0394_Bessel_Inverse_Density_Profile\"
  by (simp add: wolfram_verified_check_def wolfram_check_status_def)

lemma id0167_total_stress_energy_decomposition_passed:
  \"wolfram_verified_check Wolfram_ID0167_Total_Stress_Energy_Decomposition\"
  by (simp add: wolfram_verified_check_def wolfram_check_status_def)

lemma id0167_vacuum_component_tzp_handoff_passed:
  \"wolfram_verified_check Wolfram_ID0167_Vacuum_Component_TZP_Handoff\"
  by (simp add: wolfram_verified_check_def wolfram_check_status_def)

lemma id0167_componentwise_conservation_linearity_passed:
  \"wolfram_verified_check Wolfram_ID0167_Componentwise_Conservation_Linearity\"
  by (simp add: wolfram_verified_check_def wolfram_check_status_def)

lemma id0958_wave_operator_source_relation_passed:
  \"wolfram_verified_check Wolfram_ID0958_Wave_Operator_Source_Relation\"
  by (simp add: wolfram_verified_check_def wolfram_check_status_def)

lemma id0958_effective_einstein_sector_relation_passed:
  \"wolfram_verified_check Wolfram_ID0958_Effective_Einstein_Sector_Relation\"
  by (simp add: wolfram_verified_check_def wolfram_check_status_def)

lemma id0958_unified_lagrangian_decomposition_passed:
  \"wolfram_verified_check Wolfram_ID0958_Unified_Lagrangian_Decomposition\"
  by (simp add: wolfram_verified_check_def wolfram_check_status_def)

lemma id0958_action_generates_effective_einstein_sector_passed:
  \"wolfram_verified_check Wolfram_ID0958_Action_Generates_Effective_Einstein_Sector\"
  by (simp add: wolfram_verified_check_def wolfram_check_status_def)

lemma wolfram_focus_registry_alignment:
  \"wolfram_check_registry_id Wolfram_ID0335_Far_Field_Classical_Einstein_Limit = Focus_ID0335
    & wolfram_check_registry_id Wolfram_ID0400_Density_Side_Dimensional_Balance = Focus_ID0400
    & wolfram_check_registry_id Wolfram_ID0400_Direct_Hubble_Square_Dimension = Focus_ID0400
    & wolfram_check_registry_id Wolfram_ID0400_Critical_Density_Normalized_Hubble_Square = Focus_ID0400
    & wolfram_check_registry_id Wolfram_ID0400_Omega_Lambda_Observed_Density_Match = Focus_ID0400
    & wolfram_check_registry_id Wolfram_ID0394_Perfect_Fluid_Vacuum_Tensor_Form = Focus_ID0394
    & wolfram_check_registry_id Wolfram_ID0394_Bessel_Inverse_Density_Profile = Focus_ID0394
    & wolfram_check_registry_id Wolfram_ID0167_Total_Stress_Energy_Decomposition = Focus_ID0167
    & wolfram_check_registry_id Wolfram_ID0167_Vacuum_Component_TZP_Handoff = Focus_ID0167
    & wolfram_check_registry_id Wolfram_ID0167_Componentwise_Conservation_Linearity = Focus_ID0167
    & wolfram_check_registry_id Wolfram_ID0958_Wave_Operator_Source_Relation = Focus_ID0958
    & wolfram_check_registry_id Wolfram_ID0958_Effective_Einstein_Sector_Relation = Focus_ID0958
    & wolfram_check_registry_id Wolfram_ID0958_Unified_Lagrangian_Decomposition = Focus_ID0958
    & wolfram_check_registry_id Wolfram_ID0958_Action_Generates_Effective_Einstein_Sector = Focus_ID0958\"
  by (simp add: wolfram_check_registry_id_def)

context TZPID_Einstein_Focus
begin

theorem id0335_formal_limit_has_wolfram_certificate:
  \"wolfram_verified_check Wolfram_ID0335_Far_Field_Classical_Einstein_Limit
    & classical_einstein_limit Einstein_left_tensor Classical_stress_energy\"
  using id0335_wolfram_far_field_reduction_passed
    id0335_recovers_classical_einstein_far_from_tzp
  by simp

theorem id0400_density_handoff_has_wolfram_certificate:
  \"wolfram_verified_check Wolfram_ID0400_Density_Side_Dimensional_Balance
    & small_positive_vacuum_residue rho_Lambda
    & vacuum_pressure_handoff rho_Lambda TZP_vacuum_tensor\"
  using id0400_wolfram_density_dimension_passed
    id0400_supplies_positive_vacuum_residue
    id0400_hands_off_to_metric_chain
  by simp

theorem id0400_hubble_comparison_left_as_normalization_obligation:
  \"wolfram_normalization_obligation Wolfram_ID0400_Direct_Hubble_Square_Dimension\"
  by (rule id0400_hubble_square_requires_normalization)

theorem id0400_hubble_normalization_has_wolfram_certificate:
  \"wolfram_verified_check Wolfram_ID0400_Critical_Density_Normalized_Hubble_Square
    & wolfram_verified_check Wolfram_ID0400_Omega_Lambda_Observed_Density_Match
    & wolfram_normalization_obligation Wolfram_ID0400_Direct_Hubble_Square_Dimension
    & critical_density_normalization Critical_Density_Energy_Factor H0_scale Observed_Dark_Energy_Density
    & normalized_hubble_density_bridge rho_Lambda Omega_Lambda Critical_Density_Energy_Factor H0_scale
    & observed_density_tolerance rho_Lambda Observed_Dark_Energy_Density ID0400_Density_Tolerance\"
  using id0400_critical_density_normalized_hubble_square_passed
    id0400_omega_lambda_observed_density_match_passed
    id0400_hubble_square_requires_normalization
    id0400_has_critical_density_normalization
    id0400_has_normalized_hubble_bridge
    id0400_matches_observed_density_tolerance
  by simp

theorem id0394_vacuum_tensor_has_wolfram_certificate:
  \"wolfram_verified_check Wolfram_ID0394_Perfect_Fluid_Vacuum_Tensor_Form
    & wolfram_verified_check Wolfram_ID0394_Bessel_Inverse_Density_Profile
    & perfect_fluid_vacuum_tensor TZP_vacuum_tensor TZP_vacuum_density TZP_vacuum_pressure TZP_four_velocity
    & bessel_inverse_vacuum_profile TZP_vacuum_density TZP_bessel_inverse_profile
    & tzp_vacuum_stress_energy_tensor TZP_vacuum_tensor\"
  using id0394_perfect_fluid_vacuum_tensor_form_passed
    id0394_bessel_inverse_density_profile_passed
    id0394_has_perfect_fluid_vacuum_tensor
    id0394_has_bessel_inverse_density_profile
    id0394_vacuum_tensor
  by simp

theorem id0167_total_stress_energy_has_wolfram_certificate:
  \"wolfram_verified_check Wolfram_ID0167_Total_Stress_Energy_Decomposition
    & wolfram_verified_check Wolfram_ID0167_Vacuum_Component_TZP_Handoff
    & wolfram_verified_check Wolfram_ID0167_Componentwise_Conservation_Linearity
    & total_stress_energy_sum Total_stress_energy Gravitational_stress_energy Electromagnetic_stress_energy Weak_stress_energy Strong_stress_energy Vacuum_stress_energy
    & vacuum_component_links_tzp_tensor Vacuum_stress_energy TZP_vacuum_tensor
    & componentwise_conservation_closure Total_stress_energy Gravitational_stress_energy Electromagnetic_stress_energy Weak_stress_energy Strong_stress_energy Vacuum_stress_energy
    & covariantly_conserved Total_stress_energy\"
  using id0167_total_stress_energy_decomposition_passed
    id0167_vacuum_component_tzp_handoff_passed
    id0167_componentwise_conservation_linearity_passed
    id0167_has_total_stress_energy_sum
    id0167_links_vacuum_component_to_tzp_tensor
    id0167_has_componentwise_conservation_closure
    id0167_conservation
  by simp

theorem id0394_id0167_stress_energy_bridge_has_wolfram_certificate:
  \"wolfram_verified_check Wolfram_ID0394_Perfect_Fluid_Vacuum_Tensor_Form
    & wolfram_verified_check Wolfram_ID0167_Total_Stress_Energy_Decomposition
    & wolfram_verified_check Wolfram_ID0167_Vacuum_Component_TZP_Handoff
    & wolfram_verified_check Wolfram_ID0167_Componentwise_Conservation_Linearity
    & vacuum_component_links_tzp_tensor Vacuum_stress_energy TZP_vacuum_tensor
    & total_stress_energy_sum Total_stress_energy Gravitational_stress_energy Electromagnetic_stress_energy Weak_stress_energy Strong_stress_energy Vacuum_stress_energy
    & covariantly_conserved Total_stress_energy\"
  using id0394_perfect_fluid_vacuum_tensor_form_passed
    id0167_total_stress_energy_decomposition_passed
    id0167_vacuum_component_tzp_handoff_passed
    id0167_componentwise_conservation_linearity_passed
    id0394_id0167_stress_energy_bridge
  by simp

theorem id0958_action_level_bridge_has_wolfram_certificate:
  \"wolfram_verified_check Wolfram_ID0958_Wave_Operator_Source_Relation
    & wolfram_verified_check Wolfram_ID0958_Effective_Einstein_Sector_Relation
    & wolfram_verified_check Wolfram_ID0958_Unified_Lagrangian_Decomposition
    & wolfram_verified_check Wolfram_ID0958_Action_Generates_Effective_Einstein_Sector
    & effective_einstein_action_equation Effective_Einstein_equation
    & wave_operator_source_relation Unified_Wave_Field N_rho_source
    & effective_einstein_sector_relation Effective_Einstein_equation TZP_vacuum_tensor
    & unified_lagrangian_decomposition Unified_Lagrangian Einstein_Hilbert_Lagrangian QFT_Lagrangian Topological_Lagrangian Information_Lagrangian
    & action_generates_effective_einstein_sector Unified_Lagrangian Effective_Einstein_equation\"
  using id0958_wave_operator_source_relation_passed
    id0958_effective_einstein_sector_relation_passed
    id0958_unified_lagrangian_decomposition_passed
    id0958_action_generates_effective_einstein_sector_passed
    id0958_action_level_einstein_bridge
  by simp

theorem id0958_to_id0335_focused_chain_has_wolfram_certificate:
  \"wolfram_verified_check Wolfram_ID0958_Effective_Einstein_Sector_Relation
    & wolfram_verified_check Wolfram_ID0394_Perfect_Fluid_Vacuum_Tensor_Form
    & wolfram_verified_check Wolfram_ID0167_Total_Stress_Energy_Decomposition
    & wolfram_verified_check Wolfram_ID0335_Far_Field_Classical_Einstein_Limit
    & effective_einstein_sector_relation Effective_Einstein_equation TZP_vacuum_tensor
    & vacuum_component_links_tzp_tensor Vacuum_stress_energy TZP_vacuum_tensor
    & total_stress_energy_sum Total_stress_energy Gravitational_stress_energy Electromagnetic_stress_energy Weak_stress_energy Strong_stress_energy Vacuum_stress_energy
    & classical_einstein_limit Einstein_left_tensor Classical_stress_energy\"
  using id0958_effective_einstein_sector_relation_passed
    id0394_perfect_fluid_vacuum_tensor_form_passed
    id0167_total_stress_energy_decomposition_passed
    id0335_wolfram_far_field_reduction_passed
    id0958_has_effective_einstein_sector_relation
    id0167_links_vacuum_component_to_tzp_tensor
    id0167_has_total_stress_energy_sum
    id0335_recovers_classical_einstein_far_from_tzp
  by simp

end

end
"""
    Path(path).write_text(theory, encoding="utf-8")


def write_summary(path, rows, results_sha):
    lines = [
        "# Wolfram Einstein Focus Certificates",
        "",
        f"Result SHA1: `{results_sha}`",
        "",
        "| ID | Check | Status | Notes |",
        "|---|---|---|---|",
    ]
    for row in rows:
        lines.append(
            f"| {row.get('id', '')} | `{row.get('check', '')}` | `{row.get('status', '')}` | {ascii_clean(row.get('notes', ''), 260)} |"
        )
    Path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")


def update_root(path):
    root = Path(path)
    text = root.read_text(encoding="utf-8")
    if "TZPID_Einstein_Computational_Checks" in text:
        return
    text = text.rstrip() + "\n    TZPID_Einstein_Computational_Checks\n"
    root.write_text(text, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--results", default=DEFAULT_RESULTS)
    parser.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()

    results_path = Path(args.results)
    rows = json.loads(results_path.read_text(encoding="utf-8"))
    results_sha = sha1_file(results_path)

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    write_theory(output_dir / "TZPID_Einstein_Computational_Checks.thy", rows, results_sha)
    write_summary(output_dir / "wolfram_certificate_summary.md", rows, results_sha)
    update_root(output_dir / "ROOT")

    print(f"Wrote {output_dir / 'TZPID_Einstein_Computational_Checks.thy'}")
    print(f"Wrote {output_dir / 'wolfram_certificate_summary.md'}")


if __name__ == "__main__":
    main()
