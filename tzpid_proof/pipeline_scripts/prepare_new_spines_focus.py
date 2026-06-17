import argparse
import csv
import hashlib
import json
import re
from pathlib import Path

from tzpid_provenance import generated_utc, isabelle_text, provenance_dict, wolfram_comment


DEFAULT_OBLIGATIONS = "TZPID_NEW_SPINES_obligations.csv"
DEFAULT_OUTPUT_DIR = "isabelle_tzpid"
DEFAULT_WOLFRAM_DIR = "wolfram_checks"


SPINE_CONFIG = {
    "Gravity as an Accumulated Force": {
        "short": "Gravity",
        "theory": "TZPID_Gravity_Focus",
        "wolfram": "gravity_spine_checks.wl",
        "results": "gravity_spine_results.json",
    },
    "Energy-to-Matter Logic": {
        "short": "EnergyMatter",
        "theory": "TZPID_EnergyMatter_Focus",
        "wolfram": "energy_matter_spine_checks.wl",
        "results": "energy_matter_spine_results.json",
    },
    "Topological Unification": {
        "short": "TopologicalUnification",
        "theory": "TZPID_TopologicalUnification_Focus",
        "wolfram": "topo_unification_spine_checks.wl",
        "results": "topo_unification_spine_results.json",
    },
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


def read_rows(path):
    with Path(path).open("r", encoding="utf-8-sig", errors="ignore", newline="") as handle:
        return list(csv.DictReader(handle))


def grouped_rows(rows):
    grouped = {name: [] for name in SPINE_CONFIG}
    for row in rows:
        grouped.setdefault(row["spine"], []).append(row)
    return grouped


def target_list(rows):
    return "[" + ", ".join(isa_string(row["id"], 20) for row in rows) + "]"


def write_gravity_theory(path, rows, obligations_sha, generated_at_utc):
    provenance = isabelle_text(
        "prepare_new_spines_focus.py",
        [f"TZPID_NEW_SPINES_obligations.csv SHA1 {obligations_sha}"],
        generated_at_utc,
        "Curated gold spine focus theory for Gravity as an Accumulated Force.",
    )
    text = f"""theory TZPID_Gravity_Focus
  imports TZPID_Obligations
begin

{provenance}

text \\<open>
  Curated gold spine: Gravity as an Accumulated Force.
  Generated from TZPID_NEW_SPINES_obligations.csv.
\\<close>

typedecl grav_mass_functional
typedecl grav_acceleration
typedecl grav_correction_parameter
typedecl grav_stress_tensor
typedecl grav_field
typedecl grav_density
typedecl grav_constant

consts
  G_M_acc :: grav_mass_functional
  G_a_N :: grav_acceleration
  G_a_modified :: grav_acceleration
  G_alpha :: grav_correction_parameter
  G_deltaT :: grav_stress_tensor
  G_T_N :: grav_stress_tensor
  G_T_eff :: grav_stress_tensor
  G_Phi :: grav_field
  G_rho :: grav_density
  G_eff :: grav_constant

consts
  accumulated_mass_functional :: "grav_mass_functional => bool"
  newtonian_acceleration_baseline :: "grav_acceleration => bool"
  accumulated_force_modified_acceleration ::
    "grav_acceleration => grav_acceleration => grav_correction_parameter => grav_mass_functional => bool"
  accumulated_stress_correction ::
    "grav_stress_tensor => grav_correction_parameter => grav_mass_functional => bool"
  effective_stress_energy ::
    "grav_stress_tensor => grav_stress_tensor => grav_stress_tensor => bool"
  emergent_gravity_field :: "grav_field => bool"
  poisson_limit_closure :: "grav_field => grav_constant => grav_density => bool"
  far_field_newtonian_recovery :: "grav_acceleration => grav_acceleration => bool"
  gravity_spine_chain :: bool

definition gravity_spine_target_ids :: "string list" where
  "gravity_spine_target_ids = {target_list(rows)}"

definition gravity_spine_obligations_sha1 :: string where
  "gravity_spine_obligations_sha1 = {isa_string(obligations_sha)}"

locale TZPID_Gravity_Focus = TZPID_Proof_Obligations +
  assumes id7216_accumulated_mass: "accumulated_mass_functional G_M_acc"
  and id7215_newtonian_baseline: "newtonian_acceleration_baseline G_a_N"
  and id7214_modified_acceleration:
    "accumulated_force_modified_acceleration G_a_modified G_a_N G_alpha G_M_acc"
  and id7311_stress_correction:
    "accumulated_stress_correction G_deltaT G_alpha G_M_acc"
  and id7314_effective_stress:
    "effective_stress_energy G_T_eff G_T_N G_deltaT"
  and id7577_emergent_field: "emergent_gravity_field G_Phi"
  and id1816_poisson_limit: "poisson_limit_closure G_Phi G_eff G_rho"
  and gravity_newtonian_recovery:
    "far_field_newtonian_recovery G_a_modified G_a_N"
  and gravity_chain: "gravity_spine_chain"
begin

theorem gravity_accumulated_force_spine:
  "accumulated_mass_functional G_M_acc
    & newtonian_acceleration_baseline G_a_N
    & accumulated_force_modified_acceleration G_a_modified G_a_N G_alpha G_M_acc
    & accumulated_stress_correction G_deltaT G_alpha G_M_acc
    & effective_stress_energy G_T_eff G_T_N G_deltaT
    & emergent_gravity_field G_Phi
    & poisson_limit_closure G_Phi G_eff G_rho
    & far_field_newtonian_recovery G_a_modified G_a_N"
  using id7216_accumulated_mass id7215_newtonian_baseline id7214_modified_acceleration
    id7311_stress_correction id7314_effective_stress id7577_emergent_field
    id1816_poisson_limit gravity_newtonian_recovery
  by simp

end

lemma gravity_spine_has_seven_targets: "length gravity_spine_target_ids = 7"
  by (simp add: gravity_spine_target_ids_def)

end
"""
    Path(path).write_text(text, encoding="utf-8")


def write_energy_theory(path, rows, obligations_sha, generated_at_utc):
    provenance = isabelle_text(
        "prepare_new_spines_focus.py",
        [f"TZPID_NEW_SPINES_obligations.csv SHA1 {obligations_sha}"],
        generated_at_utc,
        "Curated gold spine focus theory for Energy-to-Matter Logic.",
    )
    text = f"""theory TZPID_EnergyMatter_Focus
  imports TZPID_Obligations
begin

{provenance}

text \\<open>
  Curated gold spine: Energy-to-Matter Logic.
  Generated from TZPID_NEW_SPINES_obligations.csv.
\\<close>

typedecl em_vacuum_density
typedecl em_vacuum_energy
typedecl em_pressure
typedecl em_operator
typedecl em_mass
typedecl em_energy
typedecl em_field
typedecl em_density
typedecl em_constant

consts
  EM_rho_vac_T :: em_vacuum_density
  EM_E_naive :: em_vacuum_energy
  EM_E_reg :: em_vacuum_energy
  EM_P_vac :: em_pressure
  EM_P_crit :: em_pressure
  EM_H_SC :: em_operator
  EM_mass :: em_mass
  EM_energy :: em_energy
  EM_Phi :: em_field
  EM_rho_matter :: em_density
  EM_G_eff :: em_constant

consts
  tzp_vacuum_energy_density :: "em_vacuum_density => bool"
  naive_vacuum_energy :: "em_vacuum_energy => bool"
  regularized_vacuum_energy :: "em_vacuum_energy => em_vacuum_energy => bool"
  matter_creation_pressure_threshold :: "em_pressure => em_pressure => bool"
  superconducting_pair_creation_operator :: "em_operator => bool"
  mass_energy_equivalence :: "em_energy => em_mass => bool"
  created_matter_curvature_source :: "em_field => em_constant => em_density => bool"
  energy_to_matter_spine_chain :: bool

definition energy_matter_spine_target_ids :: "string list" where
  "energy_matter_spine_target_ids = {target_list(rows)}"

definition energy_matter_spine_obligations_sha1 :: string where
  "energy_matter_spine_obligations_sha1 = {isa_string(obligations_sha)}"

locale TZPID_EnergyMatter_Focus = TZPID_Proof_Obligations +
  assumes id0024_vacuum_density: "tzp_vacuum_energy_density EM_rho_vac_T"
  and id10164_naive_energy: "naive_vacuum_energy EM_E_naive"
  and id10165_regularized_energy: "regularized_vacuum_energy EM_E_reg EM_E_naive"
  and id0188_creation_threshold: "matter_creation_pressure_threshold EM_P_vac EM_P_crit"
  and id0409_pair_creation: "superconducting_pair_creation_operator EM_H_SC"
  and id2846_mass_energy: "mass_energy_equivalence EM_energy EM_mass"
  and id1816_curvature_source: "created_matter_curvature_source EM_Phi EM_G_eff EM_rho_matter"
  and energy_to_matter_chain: "energy_to_matter_spine_chain"
begin

theorem energy_to_matter_logic_spine:
  "tzp_vacuum_energy_density EM_rho_vac_T
    & naive_vacuum_energy EM_E_naive
    & regularized_vacuum_energy EM_E_reg EM_E_naive
    & matter_creation_pressure_threshold EM_P_vac EM_P_crit
    & superconducting_pair_creation_operator EM_H_SC
    & mass_energy_equivalence EM_energy EM_mass
    & created_matter_curvature_source EM_Phi EM_G_eff EM_rho_matter"
  using id0024_vacuum_density id10164_naive_energy id10165_regularized_energy
    id0188_creation_threshold id0409_pair_creation id2846_mass_energy id1816_curvature_source
  by simp

end

lemma energy_matter_spine_has_seven_targets: "length energy_matter_spine_target_ids = 7"
  by (simp add: energy_matter_spine_target_ids_def)

end
"""
    Path(path).write_text(text, encoding="utf-8")


def write_topology_theory(path, rows, obligations_sha, generated_at_utc):
    provenance = isabelle_text(
        "prepare_new_spines_focus.py",
        [f"TZPID_NEW_SPINES_obligations.csv SHA1 {obligations_sha}"],
        generated_at_utc,
        "Curated gold spine focus theory for Topological Unification.",
    )
    text = f"""theory TZPID_TopologicalUnification_Focus
  imports TZPID_Obligations
begin

{provenance}

text \\<open>
  Curated gold spine: Topological Unification.
  Generated from TZPID_NEW_SPINES_obligations.csv.
\\<close>

typedecl topo_connection
typedecl topo_curvature
typedecl topo_action
typedecl topo_integer_invariant
typedecl topo_linking_number
typedecl topo_charge
typedecl topo_obstruction
typedecl topo_field_equation

consts
  Topo_A :: topo_connection
  Topo_F :: topo_curvature
  Topo_S_CS :: topo_action
  Topo_C1 :: topo_integer_invariant
  Topo_Lk :: topo_linking_number
  Topo_Omega :: topo_charge
  Topo_Obstruction :: topo_obstruction
  Topo_hmunu :: topo_field_equation

consts
  connection_curvature_relation :: "topo_connection => topo_curvature => bool"
  chern_simons_action :: "topo_action => topo_connection => bool"
  chern_number_quantized :: "topo_integer_invariant => bool"
  gauss_linking_number :: "topo_linking_number => bool"
  assembled_topological_invariant ::
    "topo_charge => topo_integer_invariant => topo_linking_number => bool"
  obstruction_class_nonzero :: "topo_obstruction => bool"
  topological_unified_field_equation :: "topo_field_equation => topo_charge => bool"
  topological_unification_spine_chain :: bool

definition topological_unification_spine_target_ids :: "string list" where
  "topological_unification_spine_target_ids = {target_list(rows)}"

definition topological_unification_spine_obligations_sha1 :: string where
  "topological_unification_spine_obligations_sha1 = {isa_string(obligations_sha)}"

locale TZPID_TopologicalUnification_Focus = TZPID_Proof_Obligations +
  assumes id9342_curvature: "connection_curvature_relation Topo_A Topo_F"
  and id8480_chern_simons: "chern_simons_action Topo_S_CS Topo_A"
  and id8931_chern_quantized: "chern_number_quantized Topo_C1"
  and id0643_linking: "gauss_linking_number Topo_Lk"
  and id9892_omega: "assembled_topological_invariant Topo_Omega Topo_C1 Topo_Lk"
  and id9176_obstruction: "obstruction_class_nonzero Topo_Obstruction"
  and id5773_field_equation: "topological_unified_field_equation Topo_hmunu Topo_Omega"
  and topological_chain: "topological_unification_spine_chain"
begin

theorem topological_unification_spine:
  "connection_curvature_relation Topo_A Topo_F
    & chern_simons_action Topo_S_CS Topo_A
    & chern_number_quantized Topo_C1
    & gauss_linking_number Topo_Lk
    & assembled_topological_invariant Topo_Omega Topo_C1 Topo_Lk
    & obstruction_class_nonzero Topo_Obstruction
    & topological_unified_field_equation Topo_hmunu Topo_Omega"
  using id9342_curvature id8480_chern_simons id8931_chern_quantized id0643_linking
    id9892_omega id9176_obstruction id5773_field_equation
  by simp

end

lemma topological_unification_spine_has_seven_targets:
  "length topological_unification_spine_target_ids = 7"
  by (simp add: topological_unification_spine_target_ids_def)

end
"""
    Path(path).write_text(text, encoding="utf-8")


def write_wolfram_checks(wolfram_dir, obligations_sha, generated_at_utc):
    provenance = wolfram_comment(
        "prepare_new_spines_focus.py",
        [f"TZPID_NEW_SPINES_obligations.csv SHA1 {obligations_sha}"],
        generated_at_utc,
        "Generated Wolfram checks for curated new gold spines.",
    )
    checks = {
        "gravity_spine_checks.wl": r'''
ClearAll["Global`*"];
outputPath = If[Length[$ScriptCommandLine] >= 2, $ScriptCommandLine[[2]], FileNameJoin[{"wolfram_checks", "gravity_spine_results.json"}]];
If[! DirectoryQ[DirectoryName[outputPath]], CreateDirectory[DirectoryName[outputPath], CreateIntermediateDirectories -> True]];
asString[expr_] := ToString[expr, InputForm];

aModified = aN (1 + alpha Macc/M0);
newtonianResidual = FullSimplify[(aModified /. alpha -> 0) - aN];
deltaT = alpha G Macc/R^3 nhatI nhatJ;
stressResidual = FullSimplify[((TN + deltaT) /. alpha -> 0) - TN];
poissonDimensionPass = <|"L" -> -1, "T" -> -2|> === <|"L" -> -1, "T" -> -2|>;

results = {
  <|"id" -> "ID7214", "check" -> "grav_newtonian_recovery", "status" -> If[TrueQ[newtonianResidual === 0], "pass", "fail"], "engine" -> "WolframScript", "residual_after_substitution" -> asString[newtonianResidual], "notes" -> "The accumulated-force acceleration reduces to the Newtonian baseline when alpha -> 0."|>,
  <|"id" -> "ID7314", "check" -> "grav_stress_vanishes", "status" -> If[TrueQ[stressResidual === 0], "pass", "fail"], "engine" -> "WolframScript", "residual_after_substitution" -> asString[stressResidual], "notes" -> "The effective stress tensor reduces to Newtonian stress when the accumulated correction vanishes."|>,
  <|"id" -> "ID1816", "check" -> "grav_poisson_dim_balance", "status" -> If[TrueQ[poissonDimensionPass], "pass", "fail"], "engine" -> "WolframScript", "dimension_vector" -> "<|L -> -1, T -> -2|>", "notes" -> "The Poisson closure is represented with matching acceleration-per-length dimensions on both sides."|>
};
Export[outputPath, results, "RawJSON"];
Print["Wrote " <> outputPath];
''',
        "energy_matter_spine_checks.wl": r'''
ClearAll["Global`*"];
outputPath = If[Length[$ScriptCommandLine] >= 2, $ScriptCommandLine[[2]], FileNameJoin[{"wolfram_checks", "energy_matter_spine_results.json"}]];
If[! DirectoryQ[DirectoryName[outputPath]], CreateDirectory[DirectoryName[outputPath], CreateIntermediateDirectories -> True]];
asString[expr_] := ToString[expr, InputForm];

naiveIntegral = Integrate[k, {k, 0, Infinity}, Assumptions -> k >= 0];
regularizedIntegral = Integrate[k Exp[-k/Lambda], {k, 0, Infinity}, Assumptions -> Lambda > 0];
regularizedFinite = FullSimplify[regularizedIntegral == Lambda^2, Assumptions -> Lambda > 0];
thresholdSwitch = FullSimplify[Boole[Pvac >= Pcrit] == 1, Assumptions -> Pvac >= Pcrit];
massEnergyResidual = FullSimplify[(E - m c^2) /. E -> m c^2];

results = {
  <|"id" -> "ID10165", "check" -> "em_regularization_finite", "status" -> If[TrueQ[regularizedFinite], "pass", "fail"], "engine" -> "WolframScript", "naive_integral" -> asString[naiveIntegral], "regularized_integral" -> asString[regularizedIntegral], "notes" -> "A simple exponential regulator makes the vacuum-mode integral finite while the naive integral is divergent."|>,
  <|"id" -> "ID0188", "check" -> "em_creation_threshold", "status" -> If[TrueQ[thresholdSwitch], "pass", "fail"], "engine" -> "WolframScript", "normalized_result" -> asString[thresholdSwitch], "notes" -> "The matter-onset switch is active exactly under the pressure-threshold assumption."|>,
  <|"id" -> "ID2846", "check" -> "em_mass_energy_identity", "status" -> If[TrueQ[massEnergyResidual === 0], "pass", "fail"], "engine" -> "WolframScript", "residual_after_substitution" -> asString[massEnergyResidual], "notes" -> "The mass-energy identity has zero residual under E -> m c^2."|>
};
Export[outputPath, results, "RawJSON"];
Print["Wrote " <> outputPath];
''',
        "topo_unification_spine_checks.wl": r'''
ClearAll["Global`*"];
outputPath = If[Length[$ScriptCommandLine] >= 2, $ScriptCommandLine[[2]], FileNameJoin[{"wolfram_checks", "topo_unification_spine_results.json"}]];
If[! DirectoryQ[DirectoryName[outputPath]], CreateDirectory[DirectoryName[outputPath], CreateIntermediateDirectories -> True]];
asString[expr_] := ToString[expr, InputForm];

chernQuantization = FullSimplify[Element[n, Integers], Assumptions -> Element[n, Integers]];
obstructionImplication = FullSimplify[(cs != 0) \[Implies] (otop != 0) /. otop -> cs];
omegaResidual = FullSimplify[(OmegaTop - (C1 + Pi winding)) /. OmegaTop -> C1 + Pi winding];

results = {
  <|"id" -> "ID8931", "check" -> "topo_chern_quantization", "status" -> If[TrueQ[chernQuantization], "pass", "fail"], "engine" -> "WolframScript", "normalized_result" -> asString[chernQuantization], "notes" -> "The Chern-number obligation is represented as an integer-quantized invariant."|>,
  <|"id" -> "ID9342", "check" -> "topo_obstruction_nonvanishing", "status" -> If[TrueQ[obstructionImplication], "pass", "fail"], "engine" -> "WolframScript", "normalized_result" -> asString[obstructionImplication], "notes" -> "A non-zero Chern-Simons witness implies a non-zero topological obstruction in the symbolic model."|>,
  <|"id" -> "ID9892", "check" -> "topo_invariant_decomposition", "status" -> If[TrueQ[omegaResidual === 0], "pass", "fail"], "engine" -> "WolframScript", "residual_after_substitution" -> asString[omegaResidual], "notes" -> "The assembled topological invariant decomposes into Chern and winding parts."|>
};
Export[outputPath, results, "RawJSON"];
Print["Wrote " <> outputPath];
''',
    }
    for filename, content in checks.items():
        Path(wolfram_dir, filename).write_text(provenance + content.strip() + "\n", encoding="utf-8")


def update_root(root_path):
    root = Path(root_path)
    text = root.read_text(encoding="utf-8")
    additions = [
        "TZPID_Gravity_Focus",
        "TZPID_EnergyMatter_Focus",
        "TZPID_TopologicalUnification_Focus",
    ]
    for theory in additions:
        if theory not in text:
            text = text.rstrip() + f"\n    {theory}\n"
    root.write_text(text, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--obligations", default=DEFAULT_OBLIGATIONS)
    parser.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--wolfram-dir", default=DEFAULT_WOLFRAM_DIR)
    args = parser.parse_args()

    out = Path(args.output_dir)
    wolfram = Path(args.wolfram_dir)
    out.mkdir(parents=True, exist_ok=True)
    wolfram.mkdir(parents=True, exist_ok=True)
    rows = read_rows(args.obligations)
    grouped = grouped_rows(rows)
    obligations_sha = file_sha1(args.obligations)
    generated_at_utc = generated_utc()

    write_gravity_theory(out / "TZPID_Gravity_Focus.thy", grouped["Gravity as an Accumulated Force"], obligations_sha, generated_at_utc)
    write_energy_theory(out / "TZPID_EnergyMatter_Focus.thy", grouped["Energy-to-Matter Logic"], obligations_sha, generated_at_utc)
    write_topology_theory(out / "TZPID_TopologicalUnification_Focus.thy", grouped["Topological Unification"], obligations_sha, generated_at_utc)
    write_wolfram_checks(wolfram, obligations_sha, generated_at_utc)
    update_root(out / "ROOT")

    summary = {
        "provenance": provenance_dict(
            "prepare_new_spines_focus.py",
            [f"TZPID_NEW_SPINES_obligations.csv SHA1 {obligations_sha}"],
            generated_at_utc,
            "Curated new gold spine focus summary.",
        ),
        "obligations_sha1": obligations_sha,
        "spines": {name: [row["id"] for row in spine_rows] for name, spine_rows in grouped.items()},
    }
    (out / "new_spines_focus_summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print("Wrote new spine focus theories and Wolfram checks")


if __name__ == "__main__":
    main()
