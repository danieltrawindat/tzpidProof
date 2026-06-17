import argparse
import csv
import hashlib
import re
from pathlib import Path


DEFAULT_MASTER = "TZPID_ALL_IDS_CANONICAL_EQUATION_MASTER_with_export.csv"
DEFAULT_ENCYCLOPEDIA = "TZPID_ENCYCLOPEDIA.md"
DEFAULT_OUTPUT_DIR = "isabelle_tzpid"

FOCUS_IDS = ["ID0335", "ID0400", "ID1392", "ID0167", "ID0394", "ID0958"]

SOURCE_HINTS = [
    r"D:\Zenodo\Gravitational-Emergence-TPZ-.pdf",
    r"D:\Zenodo\Universal_Field_Theory_Rendered.pdf",
    r"D:\Zenodo\trawin_zero_point_quantum_field_theory.pdf",
    r"D:\Tex\TEX_20260224_182530\Volume_02_Complete.tex",
    r"D:\Tex\TEX_20260224_182530\Universal_Field_via_Bridge_Tunnel_Theory_SECOND_PASS.tex",
    r"D:\Tex\TEX_20260224_182530\Vol.01.tex",
    r"D:\Tex\theory_of_it_all_trawin_topology.tex",
]


def sha1_text(text):
    return hashlib.sha1(str(text).encode("utf-8", errors="ignore")).hexdigest()


def file_hash(path):
    digest = hashlib.sha1()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def ascii_clean(value, max_len=220):
    text = "" if value is None else str(value)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = text.replace("\\", "/")
    text = text.replace("''", "'")
    text = re.sub(r"\s+", " ", text).strip()
    return text[:max_len]


def isa_string(value, max_len=220):
    return "''" + ascii_clean(value, max_len=max_len) + "''"


def read_master_rows(path):
    rows = {}
    with Path(path).open("r", encoding="utf-8-sig", errors="ignore", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            rid = row.get("id") or row.get("ID") or row.get("registry_id") or ""
            rid = rid.strip()
            if rid:
                rows.setdefault(rid, []).append(row)
    return rows


def read_encyclopedia_entries(path):
    text = Path(path).read_text(encoding="utf-8", errors="ignore")
    entry_re = re.compile(
        r"^###\s+(ID\d{4,5})\s+[—-]\s+(.+?)\s*$\n(?P<body>.*?)(?=^###\s+ID\d{4,5}\s+[—-]|\Z)",
        re.M | re.S,
    )
    entries = {}
    for match in entry_re.finditer(text):
        entries[match.group(1)] = {
            "id": match.group(1),
            "title": match.group(2).strip(),
            "body": match.group("body").strip(),
        }
    return entries


def first_existing(paths):
    return [path for path in paths if Path(path).exists()]


def build_focus_rows(master_rows, encyclopedia_entries, source_paths):
    focus = []
    for rid in FOCUS_IDS:
        master = (master_rows.get(rid) or [{}])[0]
        enc = encyclopedia_entries.get(rid, {})
        title = (
            master.get("title")
            or master.get("Title")
            or enc.get("title")
            or f"Registry focus {rid}"
        )
        statement = (
            master.get("canonical_statement")
            or master.get("statement")
            or master.get("Statement")
            or ""
        )
        equation = (
            master.get("canonical_equation")
            or master.get("equation")
            or master.get("Equation")
            or ""
        )
        classification = (
            master.get("classification")
            or master.get("equation_type")
            or master.get("type")
            or ""
        )
        variables = master.get("variables") or master.get("symbols") or ""
        enc_body = enc.get("body", "")
        source_blob = "|".join(
            [
                rid,
                title,
                statement,
                equation,
                classification,
                variables,
                enc_body[:5000],
            ]
        )
        role = {
            "ID0335": "Modified_Einstein_Source_Equation",
            "ID0400": "Cosmological_Constant_Master_Equation",
            "ID1392": "Cosmological_Constant_Normalized_Duplicate",
            "ID0167": "Unified_Einstein_Total_Stress_Energy",
            "ID0394": "TZP_Vacuum_Stress_Energy_Tensor",
            "ID0958": "Unified_Operator_Action_Effective_Einstein",
        }.get(rid, "Einstein_Focus_Dependency")
        focus.append(
            {
                "registry_id": rid,
                "role": role,
                "title": ascii_clean(title, 260),
                "classification": ascii_clean(classification, 120),
                "variables": ascii_clean(variables, 160),
                "canonical_statement": ascii_clean(statement, 700),
                "canonical_equation": ascii_clean(equation, 700),
                "encyclopedia_digest": sha1_text(enc_body),
                "master_row_digest": sha1_text(source_blob),
                "source_paths": " | ".join(source_paths),
            }
        )
    return focus


def write_focus_csv(path, rows):
    fields = [
        "registry_id",
        "role",
        "title",
        "classification",
        "variables",
        "canonical_statement",
        "canonical_equation",
        "encyclopedia_digest",
        "master_row_digest",
        "source_paths",
    ]
    with Path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_focus_summary(path, rows, source_paths):
    lines = [
        "# TZPID Einstein Focus Obligations",
        "",
        "This focused layer promotes the cosmological constant and modified Einstein entries into typed Isabelle obligations.",
        "",
        "## Focus IDs",
        "",
    ]
    for row in rows:
        lines.extend(
            [
                f"- **{row['registry_id']}** — {row['title']}",
                f"  - Role: `{row['role']}`",
                f"  - Classification: {row['classification'] or 'n/a'}",
                f"  - Equation: `{row['canonical_equation'] or 'n/a'}`",
            ]
        )
    lines.extend(["", "## Source Hints", ""])
    for source in source_paths:
        lines.append(f"- `{source}`")
    Path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_theory(path, rows, master_sha, encyclopedia_sha, source_sha):
    row_by_id = {row["registry_id"]: row for row in rows}
    id0335 = row_by_id.get("ID0335", {})
    id0400 = row_by_id.get("ID0400", {})
    id0167 = row_by_id.get("ID0167", {})
    id0394 = row_by_id.get("ID0394", {})
    id0958 = row_by_id.get("ID0958", {})

    theory = f"""theory TZPID_Einstein_Focus
  imports TZPID_Obligations
begin

text <open>
  Focused typed obligation layer for the cosmological constant handoff
  and the TZP-modified Einstein equation. This file is generated from
  TZPID_ENCYCLOPEDIA.md and the canonical equation master CSV.
open>

datatype tzpid_einstein_focus_id =
    Focus_ID0335
  | Focus_ID0400
  | Focus_ID1392
  | Focus_ID0167
  | Focus_ID0394
  | Focus_ID0958

typedecl scalar_density
typedecl radius_scale
typedecl flux_quantity
typedecl hubble_scale
typedecl physical_constant
typedecl tensor2
typedecl tensor_source
typedecl spacetime_region
typedecl asymptotic_regime
typedecl field_equation
typedecl cosmological_fraction
typedecl density_tolerance
typedecl pressure_density
typedecl four_velocity
typedecl radial_profile
typedecl wave_field
typedecl source_density
typedecl lagrangian_density

consts
  rho_Lambda :: scalar_density
  hbar_c_const :: physical_constant
  cosmic_radius_R :: radius_scale
  Phi0 :: flux_quantity
  Phi_total :: flux_quantity
  H0_scale :: hubble_scale
  Omega_Lambda :: cosmological_fraction
  Critical_Density_Energy_Factor :: physical_constant
  Observed_Dark_Energy_Density :: scalar_density
  ID0400_Density_Tolerance :: density_tolerance
  Einstein_left_tensor :: tensor2
  Classical_stress_energy :: tensor2
  Total_stress_energy :: tensor2
  Gravitational_stress_energy :: tensor2
  Electromagnetic_stress_energy :: tensor2
  Weak_stress_energy :: tensor2
  Strong_stress_energy :: tensor2
  Vacuum_stress_energy :: tensor2
  TZP_source_tensor :: tensor_source
  TZP_vacuum_tensor :: tensor2
  TZP_vacuum_density :: scalar_density
  TZP_vacuum_pressure :: pressure_density
  TZP_four_velocity :: four_velocity
  TZP_bessel_inverse_profile :: radial_profile
  Effective_Einstein_equation :: field_equation
  Unified_Wave_Field :: wave_field
  N_rho_source :: source_density
  Unified_Lagrangian :: lagrangian_density
  Einstein_Hilbert_Lagrangian :: lagrangian_density
  QFT_Lagrangian :: lagrangian_density
  Topological_Lagrangian :: lagrangian_density
  Information_Lagrangian :: lagrangian_density
  Far_From_TZP :: asymptotic_regime

consts
  cosmological_density_equation ::
    \"scalar_density => physical_constant => radius_scale => flux_quantity => flux_quantity => hubble_scale => bool\"
  critical_density_normalization ::
    \"physical_constant => hubble_scale => scalar_density => bool\"
  normalized_hubble_density_bridge ::
    \"scalar_density => cosmological_fraction => physical_constant => hubble_scale => bool\"
  observed_density_tolerance ::
    \"scalar_density => scalar_density => density_tolerance => bool\"
  id0400_structured_obligation ::
    \"scalar_density => physical_constant => radius_scale => flux_quantity => flux_quantity => hubble_scale => cosmological_fraction => density_tolerance => bool\"
  small_positive_vacuum_residue :: \"scalar_density => bool\"
  vacuum_pressure_handoff :: \"scalar_density => tensor2 => bool\"
  modified_einstein_equation :: \"tensor2 => tensor2 => tensor_source => bool\"
  tzp_source_far_field_vanishes :: \"tensor_source => asymptotic_regime => bool\"
  classical_einstein_limit :: \"tensor2 => tensor2 => bool\"
  total_stress_energy_decomposition :: \"tensor2 => bool\"
  total_stress_energy_sum ::
    \"tensor2 => tensor2 => tensor2 => tensor2 => tensor2 => tensor2 => bool\"
  vacuum_component_links_tzp_tensor :: \"tensor2 => tensor2 => bool\"
  componentwise_conservation_closure ::
    \"tensor2 => tensor2 => tensor2 => tensor2 => tensor2 => tensor2 => bool\"
  covariantly_conserved :: \"tensor2 => bool\"
  perfect_fluid_vacuum_tensor ::
    \"tensor2 => scalar_density => pressure_density => four_velocity => bool\"
  bessel_inverse_vacuum_profile :: \"scalar_density => radial_profile => bool\"
  tzp_vacuum_stress_energy_tensor :: \"tensor2 => bool\"
  wave_operator_source_relation :: \"wave_field => source_density => bool\"
  effective_einstein_sector_relation :: \"field_equation => tensor2 => bool\"
  unified_lagrangian_decomposition ::
    \"lagrangian_density => lagrangian_density => lagrangian_density => lagrangian_density => lagrangian_density => bool\"
  action_generates_effective_einstein_sector ::
    \"lagrangian_density => field_equation => bool\"
  effective_einstein_action_equation :: \"field_equation => bool\"
  focus_registry_grounded :: \"tzpid_einstein_focus_id => bool\"

definition einstein_focus_master_sha1 :: string where
  \"einstein_focus_master_sha1 = {isa_string(master_sha)}\"

definition einstein_focus_encyclopedia_sha1 :: string where
  \"einstein_focus_encyclopedia_sha1 = {isa_string(encyclopedia_sha)}\"

definition einstein_focus_source_sha1 :: string where
  \"einstein_focus_source_sha1 = {isa_string(source_sha)}\"

definition id0335_title :: string where
  \"id0335_title = {isa_string(id0335.get('title', ''), 260)}\"

definition id0335_canonical_equation :: string where
  \"id0335_canonical_equation = {isa_string(id0335.get('canonical_equation', ''), 700)}\"

definition id0400_title :: string where
  \"id0400_title = {isa_string(id0400.get('title', ''), 260)}\"

definition id0400_canonical_equation :: string where
  \"id0400_canonical_equation = {isa_string(id0400.get('canonical_equation', ''), 700)}\"

definition einstein_focus_dependencies :: \"(tzpid_einstein_focus_id * string) list\" where
  \"einstein_focus_dependencies = [
    (Focus_ID0335, {isa_string(id0335.get('role', ''))}),
    (Focus_ID0400, {isa_string(id0400.get('role', ''))}),
    (Focus_ID0167, {isa_string(id0167.get('role', ''))}),
    (Focus_ID0394, {isa_string(id0394.get('role', ''))}),
    (Focus_ID0958, {isa_string(id0958.get('role', ''))})
  ]\"

locale TZPID_Einstein_Focus = TZPID_Proof_Obligations +
  assumes focus_id0335_grounded: \"focus_registry_grounded Focus_ID0335\"
  and focus_id0400_grounded: \"focus_registry_grounded Focus_ID0400\"
  and focus_id0167_grounded: \"focus_registry_grounded Focus_ID0167\"
  and focus_id0394_grounded: \"focus_registry_grounded Focus_ID0394\"
  and focus_id0958_grounded: \"focus_registry_grounded Focus_ID0958\"
  and id0400_master_density:
    \"cosmological_density_equation rho_Lambda hbar_c_const cosmic_radius_R Phi0 Phi_total H0_scale\"
  and id0400_critical_density_normalization:
    \"critical_density_normalization Critical_Density_Energy_Factor H0_scale Observed_Dark_Energy_Density\"
  and id0400_normalized_hubble_bridge:
    \"normalized_hubble_density_bridge rho_Lambda Omega_Lambda Critical_Density_Energy_Factor H0_scale\"
  and id0400_observed_density_tolerance:
    \"observed_density_tolerance rho_Lambda Observed_Dark_Energy_Density ID0400_Density_Tolerance\"
  and id0400_structured:
    \"id0400_structured_obligation rho_Lambda hbar_c_const cosmic_radius_R Phi0 Phi_total H0_scale Omega_Lambda ID0400_Density_Tolerance\"
  and id0400_small_positive_residue: \"small_positive_vacuum_residue rho_Lambda\"
  and id0400_metric_handoff: \"vacuum_pressure_handoff rho_Lambda TZP_vacuum_tensor\"
  and id0335_modified_einstein:
    \"modified_einstein_equation Einstein_left_tensor Classical_stress_energy TZP_source_tensor\"
  and id0335_far_field_vanishing: \"tzp_source_far_field_vanishes TZP_source_tensor Far_From_TZP\"
  and id0335_classical_recovery:
    \"tzp_source_far_field_vanishes TZP_source_tensor Far_From_TZP
      ==> classical_einstein_limit Einstein_left_tensor Classical_stress_energy\"
  and id0167_total_stress_energy: \"total_stress_energy_decomposition Total_stress_energy\"
  and id0167_total_stress_energy_sum:
    \"total_stress_energy_sum Total_stress_energy Gravitational_stress_energy Electromagnetic_stress_energy Weak_stress_energy Strong_stress_energy Vacuum_stress_energy\"
  and id0167_vacuum_component_links_tzp:
    \"vacuum_component_links_tzp_tensor Vacuum_stress_energy TZP_vacuum_tensor\"
  and id0167_componentwise_conservation:
    \"componentwise_conservation_closure Total_stress_energy Gravitational_stress_energy Electromagnetic_stress_energy Weak_stress_energy Strong_stress_energy Vacuum_stress_energy\"
  and id0167_conservation: \"covariantly_conserved Total_stress_energy\"
  and id0394_perfect_fluid_tensor:
    \"perfect_fluid_vacuum_tensor TZP_vacuum_tensor TZP_vacuum_density TZP_vacuum_pressure TZP_four_velocity\"
  and id0394_bessel_inverse_profile:
    \"bessel_inverse_vacuum_profile TZP_vacuum_density TZP_bessel_inverse_profile\"
  and id0394_vacuum_tensor: \"tzp_vacuum_stress_energy_tensor TZP_vacuum_tensor\"
  and id0958_wave_operator_source:
    \"wave_operator_source_relation Unified_Wave_Field N_rho_source\"
  and id0958_effective_einstein_sector_relation:
    \"effective_einstein_sector_relation Effective_Einstein_equation TZP_vacuum_tensor\"
  and id0958_lagrangian_decomposition:
    \"unified_lagrangian_decomposition Unified_Lagrangian Einstein_Hilbert_Lagrangian QFT_Lagrangian Topological_Lagrangian Information_Lagrangian\"
  and id0958_action_generates_einstein_sector:
    \"action_generates_effective_einstein_sector Unified_Lagrangian Effective_Einstein_equation\"
  and id0958_effective_action: \"effective_einstein_action_equation Effective_Einstein_equation\"
begin

lemma id0400_is_grounded:
  \"focus_registry_grounded Focus_ID0400\"
  by (rule focus_id0400_grounded)

lemma id0400_supplies_positive_vacuum_residue:
  \"small_positive_vacuum_residue rho_Lambda\"
  by (rule id0400_small_positive_residue)

lemma id0400_hands_off_to_metric_chain:
  \"vacuum_pressure_handoff rho_Lambda TZP_vacuum_tensor\"
  by (rule id0400_metric_handoff)

lemma id0400_has_critical_density_normalization:
  \"critical_density_normalization Critical_Density_Energy_Factor H0_scale Observed_Dark_Energy_Density\"
  by (rule id0400_critical_density_normalization)

lemma id0400_has_normalized_hubble_bridge:
  \"normalized_hubble_density_bridge rho_Lambda Omega_Lambda Critical_Density_Energy_Factor H0_scale\"
  by (rule id0400_normalized_hubble_bridge)

lemma id0400_matches_observed_density_tolerance:
  \"observed_density_tolerance rho_Lambda Observed_Dark_Energy_Density ID0400_Density_Tolerance\"
  by (rule id0400_observed_density_tolerance)

theorem id0400_three_part_density_obligation:
  \"cosmological_density_equation rho_Lambda hbar_c_const cosmic_radius_R Phi0 Phi_total H0_scale
    & normalized_hubble_density_bridge rho_Lambda Omega_Lambda Critical_Density_Energy_Factor H0_scale
    & observed_density_tolerance rho_Lambda Observed_Dark_Energy_Density ID0400_Density_Tolerance\"
  using id0400_master_density id0400_normalized_hubble_bridge id0400_observed_density_tolerance
  by simp

lemma id0335_is_grounded:
  \"focus_registry_grounded Focus_ID0335\"
  by (rule focus_id0335_grounded)

lemma id0335_has_tzp_modified_einstein_equation:
  \"modified_einstein_equation Einstein_left_tensor Classical_stress_energy TZP_source_tensor\"
  by (rule id0335_modified_einstein)

theorem id0335_recovers_classical_einstein_far_from_tzp:
  \"classical_einstein_limit Einstein_left_tensor Classical_stress_energy\"
  by (rule id0335_classical_recovery, rule id0335_far_field_vanishing)

lemma id0394_has_perfect_fluid_vacuum_tensor:
  \"perfect_fluid_vacuum_tensor TZP_vacuum_tensor TZP_vacuum_density TZP_vacuum_pressure TZP_four_velocity\"
  by (rule id0394_perfect_fluid_tensor)

lemma id0394_has_bessel_inverse_density_profile:
  \"bessel_inverse_vacuum_profile TZP_vacuum_density TZP_bessel_inverse_profile\"
  by (rule id0394_bessel_inverse_profile)

lemma id0167_has_total_stress_energy_sum:
  \"total_stress_energy_sum Total_stress_energy Gravitational_stress_energy Electromagnetic_stress_energy Weak_stress_energy Strong_stress_energy Vacuum_stress_energy\"
  by (rule id0167_total_stress_energy_sum)

lemma id0167_links_vacuum_component_to_tzp_tensor:
  \"vacuum_component_links_tzp_tensor Vacuum_stress_energy TZP_vacuum_tensor\"
  by (rule id0167_vacuum_component_links_tzp)

lemma id0167_has_componentwise_conservation_closure:
  \"componentwise_conservation_closure Total_stress_energy Gravitational_stress_energy Electromagnetic_stress_energy Weak_stress_energy Strong_stress_energy Vacuum_stress_energy\"
  by (rule id0167_componentwise_conservation)

theorem id0394_id0167_stress_energy_bridge:
  \"tzp_vacuum_stress_energy_tensor TZP_vacuum_tensor
    & perfect_fluid_vacuum_tensor TZP_vacuum_tensor TZP_vacuum_density TZP_vacuum_pressure TZP_four_velocity
    & bessel_inverse_vacuum_profile TZP_vacuum_density TZP_bessel_inverse_profile
    & vacuum_component_links_tzp_tensor Vacuum_stress_energy TZP_vacuum_tensor
    & total_stress_energy_sum Total_stress_energy Gravitational_stress_energy Electromagnetic_stress_energy Weak_stress_energy Strong_stress_energy Vacuum_stress_energy
    & covariantly_conserved Total_stress_energy\"
  using id0394_vacuum_tensor id0394_perfect_fluid_tensor id0394_bessel_inverse_profile
    id0167_vacuum_component_links_tzp id0167_total_stress_energy_sum id0167_conservation
  by simp

lemma id0958_has_wave_operator_source_relation:
  \"wave_operator_source_relation Unified_Wave_Field N_rho_source\"
  by (rule id0958_wave_operator_source)

lemma id0958_has_effective_einstein_sector_relation:
  \"effective_einstein_sector_relation Effective_Einstein_equation TZP_vacuum_tensor\"
  by (rule id0958_effective_einstein_sector_relation)

lemma id0958_has_unified_lagrangian_decomposition:
  \"unified_lagrangian_decomposition Unified_Lagrangian Einstein_Hilbert_Lagrangian QFT_Lagrangian Topological_Lagrangian Information_Lagrangian\"
  by (rule id0958_lagrangian_decomposition)

lemma id0958_action_generates_effective_sector:
  \"action_generates_effective_einstein_sector Unified_Lagrangian Effective_Einstein_equation\"
  by (rule id0958_action_generates_einstein_sector)

theorem id0958_action_level_einstein_bridge:
  \"effective_einstein_action_equation Effective_Einstein_equation
    & wave_operator_source_relation Unified_Wave_Field N_rho_source
    & effective_einstein_sector_relation Effective_Einstein_equation TZP_vacuum_tensor
    & unified_lagrangian_decomposition Unified_Lagrangian Einstein_Hilbert_Lagrangian QFT_Lagrangian Topological_Lagrangian Information_Lagrangian
    & action_generates_effective_einstein_sector Unified_Lagrangian Effective_Einstein_equation
    & tzp_vacuum_stress_energy_tensor TZP_vacuum_tensor\"
  using id0958_effective_action id0958_wave_operator_source id0958_effective_einstein_sector_relation
    id0958_lagrangian_decomposition id0958_action_generates_einstein_sector id0394_vacuum_tensor
  by simp

theorem einstein_focus_dependency_chain_registered:
  \"focus_registry_grounded Focus_ID0400
    & focus_registry_grounded Focus_ID0335
    & total_stress_energy_decomposition Total_stress_energy
    & covariantly_conserved Total_stress_energy
    & tzp_vacuum_stress_energy_tensor TZP_vacuum_tensor
    & effective_einstein_action_equation Effective_Einstein_equation\"
  using focus_id0400_grounded focus_id0335_grounded id0167_total_stress_energy
    id0167_conservation id0394_vacuum_tensor id0958_effective_action
  by simp

end

lemma einstein_focus_has_six_registry_targets:
  \"length [Focus_ID0335, Focus_ID0400, Focus_ID1392, Focus_ID0167, Focus_ID0394, Focus_ID0958] = 6\"
  by simp

end
"""
    theory = theory.replace("text <open>", "text \\<open>").replace("\nopen>\n", "\n\\<close>\n")
    Path(path).write_text(theory, encoding="utf-8")


def update_root(path):
    root = Path(path)
    text = root.read_text(encoding="utf-8")
    if "TZPID_Einstein_Focus" in text:
        return
    text = text.rstrip() + "\n    TZPID_Einstein_Focus\n"
    root.write_text(text, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--master", default=DEFAULT_MASTER)
    parser.add_argument("--encyclopedia", default=DEFAULT_ENCYCLOPEDIA)
    parser.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    master_rows = read_master_rows(args.master)
    encyclopedia_entries = read_encyclopedia_entries(args.encyclopedia)
    source_paths = first_existing(SOURCE_HINTS)
    rows = build_focus_rows(master_rows, encyclopedia_entries, source_paths)

    master_sha = file_hash(args.master)
    encyclopedia_sha = file_hash(args.encyclopedia)
    source_sha = sha1_text("|".join(source_paths))

    write_focus_csv(output_dir / "einstein_focus_obligations.csv", rows)
    write_focus_summary(output_dir / "einstein_focus_summary.md", rows, source_paths)
    write_theory(output_dir / "TZPID_Einstein_Focus.thy", rows, master_sha, encyclopedia_sha, source_sha)
    update_root(output_dir / "ROOT")

    print(f"Wrote {output_dir / 'TZPID_Einstein_Focus.thy'}")
    print(f"Wrote {output_dir / 'einstein_focus_obligations.csv'}")
    print(f"Wrote {output_dir / 'einstein_focus_summary.md'}")


if __name__ == "__main__":
    main()
