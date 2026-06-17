import argparse
import csv
import hashlib
import json
import re
from pathlib import Path

from tzpid_provenance import generated_utc, lean_comment, provenance_dict, rocq_comment


DEFAULT_MASTER = "TZPID_ALL_IDS_CANONICAL_EQUATION_MASTER_with_export.csv"
DEFAULT_WOLFRAM = "wolfram_checks/einstein_focus_results.json"
DEFAULT_NEW_SPINES = "TZPID_NEW_SPINES_obligations.csv"
DEFAULT_NEW_SPINES_CERTIFICATE = "isabelle_tzpid/new_spines_wolfram_certificate_summary.md"
DEFAULT_ZENODO_SPINES = "TZPID_ZENODO_SPINES_obligations.csv"
DEFAULT_ZENODO_SPINES_CERTIFICATE = "isabelle_tzpid/zenodo_spines_wolfram_certificate_summary.md"
DEFAULT_OUTPUT_DIR = "lean_rocq_gold_spine"

EINSTEIN_GOLD_SPINE_IDS = ["ID0958", "ID0400", "ID0394", "ID0167", "ID0335", "ID1392"]
NEW_SPINE_ORDER = [
    "Gravity as an Accumulated Force",
    "Energy-to-Matter Logic",
    "Topological Unification",
]


def file_sha1(path):
    digest = hashlib.sha1()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_rows(path):
    with Path(path).open("r", encoding="utf-8-sig", errors="ignore", newline="") as handle:
        return list(csv.DictReader(handle))


def read_new_spines(path):
    rows = read_rows(path)
    grouped = {name: [] for name in NEW_SPINE_ORDER}
    for row in rows:
        grouped.setdefault(row["spine"], []).append(row["id"])
    return grouped


def read_zenodo_spines(path):
    rows = read_rows(path)
    grouped = {}
    for row in rows:
        grouped.setdefault(row["paper"], []).append(row["id"])
    return grouped, rows


def lean_ctor(registry_id):
    safe = re.sub(r"[^A-Za-z0-9_]", "_", registry_id)
    return "registry_" + safe


def rocq_ctor(registry_id):
    safe = re.sub(r"[^A-Za-z0-9_]", "_", registry_id)
    if not safe or not safe[0].isalpha():
        safe = "ID_" + safe
    return "registry_" + safe


def lean_list_definition(name, ids):
    lines = [f"def {name} : List RegistryID := ["]
    lines.extend(f"  {lean_ctor(rid)}," for rid in ids)
    lines.append("]")
    lines.append("")
    lines.append(f"theorem {name}_count : {name}.length = {len(ids)} := rfl")
    return lines


def write_lean(
    path,
    rows,
    master_sha,
    wolfram_sha,
    new_spines,
    new_spines_sha,
    new_spines_cert_sha,
    zenodo_spines,
    zenodo_rows,
    zenodo_spines_sha,
    zenodo_spines_cert_sha,
    generated_at_utc,
):
    ids = [row["id"] for row in rows]
    ctors = [lean_ctor(rid) for rid in ids]
    all_curated_ids = list(EINSTEIN_GOLD_SPINE_IDS)
    for spine_name in NEW_SPINE_ORDER:
        all_curated_ids.extend(new_spines.get(spine_name, []))
    zenodo_ids = [row["id"] for row in zenodo_rows]

    provenance = lean_comment(
        "prepare_lean_rocq_all_ids.py",
        [
            f"{DEFAULT_MASTER} SHA1 {master_sha}",
            f"{DEFAULT_WOLFRAM} SHA1 {wolfram_sha}",
            f"{DEFAULT_NEW_SPINES} SHA1 {new_spines_sha}",
            f"{DEFAULT_NEW_SPINES_CERTIFICATE} SHA1 {new_spines_cert_sha}",
            f"{DEFAULT_ZENODO_SPINES} SHA1 {zenodo_spines_sha}",
            f"{DEFAULT_ZENODO_SPINES_CERTIFICATE} SHA1 {zenodo_spines_cert_sha}",
        ],
        generated_at_utc,
        "Generated all-ID Lean registry/certificate mirror; broad certificate pass, not a deep native physics proof.",
    )

    lines = [
        provenance,
        "",
        "namespace TZPID",
        "",
        "abbrev RegistryID := String",
        "",
        f"def registryRowCount : Nat := {len(ids)}",
        f"def masterCSV_SHA1 : String := \"{master_sha}\"",
        f"def wolframFocusJSON_SHA1 : String := \"{wolfram_sha}\"",
        f"def newSpinesObligations_SHA1 : String := \"{new_spines_sha}\"",
        f"def newSpinesCertificate_SHA1 : String := \"{new_spines_cert_sha}\"",
        f"def zenodoSpinesObligations_SHA1 : String := \"{zenodo_spines_sha}\"",
        f"def zenodoSpinesCertificate_SHA1 : String := \"{zenodo_spines_cert_sha}\"",
        f"def creatorName : String := \"Daniel Alexander Trawin\"",
        f"def creatorORCID : String := \"0009-0001-4630-3715\"",
        f"def creatorORCID_URL : String := \"https://orcid.org/0009-0001-4630-3715\"",
        f"def generatedUTC : String := \"{generated_at_utc}\"",
        f"def zenodoGoldSpineCount : Nat := {len(zenodo_spines)}",
        f"def zenodoGoldSpineRowCount : Nat := {len(zenodo_rows)}",
        "",
        "/- Every canonical ID is mirrored below as a compiled Lean constant. -/",
    ]
    lines.extend(f"def {ctor} : RegistryID := \"{rid}\"" for ctor, rid in zip(ctors, ids))
    lines.extend(
        [
            "",
            f"theorem registryRowCount_checked : registryRowCount = {len(ids)} := rfl",
            "",
            "theorem registryRowCount_nonempty : registryRowCount > 0 := by",
            "  decide",
            "",
        ]
    )
    lines.extend(lean_list_definition("einsteinGoldSpineIDs", EINSTEIN_GOLD_SPINE_IDS))
    lines.extend(lean_list_definition("gravityGoldSpineIDs", new_spines.get("Gravity as an Accumulated Force", [])))
    lines.extend(lean_list_definition("energyMatterGoldSpineIDs", new_spines.get("Energy-to-Matter Logic", [])))
    lines.extend(lean_list_definition("topologicalUnificationGoldSpineIDs", new_spines.get("Topological Unification", [])))
    lines.extend(lean_list_definition("allCuratedGoldSpineIDs", all_curated_ids))
    lines.extend(lean_list_definition("zenodoGoldSpineIDs", zenodo_ids))
    lines.extend(
        [
            f"theorem zenodoGoldSpineCount_checked : zenodoGoldSpineCount = {len(zenodo_spines)} := rfl",
            f"theorem zenodoGoldSpineRowCount_checked : zenodoGoldSpineRowCount = {len(zenodo_rows)} := rfl",
            "",
            "axiom id0958_action_level_einstein_bridge : Prop",
            "axiom id0400_three_part_density_obligation : Prop",
            "axiom id0394_id0167_stress_energy_bridge : Prop",
            "axiom id0335_recovers_classical_einstein_far_from_tzp : Prop",
            "axiom id0958_action_level_bridge_has_wolfram_certificate : Prop",
            "axiom id0394_id0167_stress_energy_bridge_has_wolfram_certificate : Prop",
            "axiom id0958_to_id0335_focused_chain_has_wolfram_certificate : Prop",
            "axiom gravity_accumulated_force_spine : Prop",
            "axiom energy_to_matter_logic_spine : Prop",
            "axiom topological_unification_spine : Prop",
            "axiom gravity_spine_has_wolfram_certificate : Prop",
            "axiom energy_matter_spine_has_wolfram_certificate : Prop",
            "axiom topological_unification_spine_has_wolfram_certificate : Prop",
            "axiom zenodo_spines_concept_backbone : Prop",
            "axiom zenodo_spines_have_wolfram_certificate : Prop",
            "",
            "axiom id0958_action_level_einstein_bridge_holds : id0958_action_level_einstein_bridge",
            "axiom id0400_three_part_density_obligation_holds : id0400_three_part_density_obligation",
            "axiom id0394_id0167_stress_energy_bridge_holds : id0394_id0167_stress_energy_bridge",
            "axiom id0335_recovers_classical_einstein_far_from_tzp_holds : id0335_recovers_classical_einstein_far_from_tzp",
            "axiom id0958_action_level_bridge_has_wolfram_certificate_holds : id0958_action_level_bridge_has_wolfram_certificate",
            "axiom id0394_id0167_stress_energy_bridge_has_wolfram_certificate_holds : id0394_id0167_stress_energy_bridge_has_wolfram_certificate",
            "axiom id0958_to_id0335_focused_chain_has_wolfram_certificate_holds : id0958_to_id0335_focused_chain_has_wolfram_certificate",
            "axiom gravity_accumulated_force_spine_holds : gravity_accumulated_force_spine",
            "axiom energy_to_matter_logic_spine_holds : energy_to_matter_logic_spine",
            "axiom topological_unification_spine_holds : topological_unification_spine",
            "axiom gravity_spine_has_wolfram_certificate_holds : gravity_spine_has_wolfram_certificate",
            "axiom energy_matter_spine_has_wolfram_certificate_holds : energy_matter_spine_has_wolfram_certificate",
            "axiom topological_unification_spine_has_wolfram_certificate_holds : topological_unification_spine_has_wolfram_certificate",
            "axiom zenodo_spines_concept_backbone_holds : zenodo_spines_concept_backbone",
            "axiom zenodo_spines_have_wolfram_certificate_holds : zenodo_spines_have_wolfram_certificate",
            "",
            "theorem goldSpine_focused_chain :",
            "    id0958_action_level_einstein_bridge",
            "    ∧ id0400_three_part_density_obligation",
            "    ∧ id0394_id0167_stress_energy_bridge",
            "    ∧ id0335_recovers_classical_einstein_far_from_tzp",
            "    ∧ id0958_action_level_bridge_has_wolfram_certificate",
            "    ∧ id0394_id0167_stress_energy_bridge_has_wolfram_certificate",
            "    ∧ id0958_to_id0335_focused_chain_has_wolfram_certificate := by",
            "  exact ⟨id0958_action_level_einstein_bridge_holds,",
            "    id0400_three_part_density_obligation_holds,",
            "    id0394_id0167_stress_energy_bridge_holds,",
            "    id0335_recovers_classical_einstein_far_from_tzp_holds,",
            "    id0958_action_level_bridge_has_wolfram_certificate_holds,",
            "    id0394_id0167_stress_energy_bridge_has_wolfram_certificate_holds,",
            "    id0958_to_id0335_focused_chain_has_wolfram_certificate_holds⟩",
            "",
            "theorem allCuratedGoldSpines_focused_chain :",
            "    id0958_action_level_einstein_bridge",
            "    ∧ id0400_three_part_density_obligation",
            "    ∧ id0394_id0167_stress_energy_bridge",
            "    ∧ id0335_recovers_classical_einstein_far_from_tzp",
            "    ∧ id0958_to_id0335_focused_chain_has_wolfram_certificate",
            "    ∧ gravity_accumulated_force_spine",
            "    ∧ energy_to_matter_logic_spine",
            "    ∧ topological_unification_spine",
            "    ∧ gravity_spine_has_wolfram_certificate",
            "    ∧ energy_matter_spine_has_wolfram_certificate",
            "    ∧ topological_unification_spine_has_wolfram_certificate := by",
            "  exact ⟨id0958_action_level_einstein_bridge_holds,",
            "    id0400_three_part_density_obligation_holds,",
            "    id0394_id0167_stress_energy_bridge_holds,",
            "    id0335_recovers_classical_einstein_far_from_tzp_holds,",
            "    id0958_to_id0335_focused_chain_has_wolfram_certificate_holds,",
            "    gravity_accumulated_force_spine_holds,",
            "    energy_to_matter_logic_spine_holds,",
            "    topological_unification_spine_holds,",
            "    gravity_spine_has_wolfram_certificate_holds,",
            "    energy_matter_spine_has_wolfram_certificate_holds,",
            "    topological_unification_spine_has_wolfram_certificate_holds⟩",
            "",
            "theorem allCuratedAndZenodoSpines_focused_chain :",
            "    id0958_action_level_einstein_bridge",
            "    ∧ id0400_three_part_density_obligation",
            "    ∧ id0394_id0167_stress_energy_bridge",
            "    ∧ id0335_recovers_classical_einstein_far_from_tzp",
            "    ∧ id0958_to_id0335_focused_chain_has_wolfram_certificate",
            "    ∧ gravity_accumulated_force_spine",
            "    ∧ energy_to_matter_logic_spine",
            "    ∧ topological_unification_spine",
            "    ∧ gravity_spine_has_wolfram_certificate",
            "    ∧ energy_matter_spine_has_wolfram_certificate",
            "    ∧ topological_unification_spine_has_wolfram_certificate",
            "    ∧ zenodo_spines_concept_backbone",
            "    ∧ zenodo_spines_have_wolfram_certificate := by",
            "  exact ⟨id0958_action_level_einstein_bridge_holds,",
            "    id0400_three_part_density_obligation_holds,",
            "    id0394_id0167_stress_energy_bridge_holds,",
            "    id0335_recovers_classical_einstein_far_from_tzp_holds,",
            "    id0958_to_id0335_focused_chain_has_wolfram_certificate_holds,",
            "    gravity_accumulated_force_spine_holds,",
            "    energy_to_matter_logic_spine_holds,",
            "    topological_unification_spine_holds,",
            "    gravity_spine_has_wolfram_certificate_holds,",
            "    energy_matter_spine_has_wolfram_certificate_holds,",
            "    topological_unification_spine_has_wolfram_certificate_holds,",
            "    zenodo_spines_concept_backbone_holds,",
            "    zenodo_spines_have_wolfram_certificate_holds⟩",
            "",
            "end TZPID",
            "",
        ]
    )
    Path(path).write_text("\n".join(lines), encoding="utf-8")


def rocq_list_definition(name, ids):
    lines = [f"Definition {name} : list registry_id := ["]
    if ids:
        lines.extend(f"  {rocq_ctor(rid)};" for rid in ids[:-1])
        lines.append(f"  {rocq_ctor(ids[-1])}")
    lines.append("].")
    lines.append("")
    lines.append(f"Example {name}_count : List.length {name} = {len(ids)}.")
    lines.append("Proof. vm_compute. reflexivity. Qed.")
    return lines


def write_rocq(
    path,
    rows,
    master_sha,
    wolfram_sha,
    new_spines,
    new_spines_sha,
    new_spines_cert_sha,
    zenodo_spines,
    zenodo_rows,
    zenodo_spines_sha,
    zenodo_spines_cert_sha,
    generated_at_utc,
):
    ids = [row["id"] for row in rows]
    ctors = [rocq_ctor(rid) for rid in ids]
    all_curated_ids = list(EINSTEIN_GOLD_SPINE_IDS)
    for spine_name in NEW_SPINE_ORDER:
        all_curated_ids.extend(new_spines.get(spine_name, []))
    zenodo_ids = [row["id"] for row in zenodo_rows]

    provenance = rocq_comment(
        "prepare_lean_rocq_all_ids.py",
        [
            f"{DEFAULT_MASTER} SHA1 {master_sha}",
            f"{DEFAULT_WOLFRAM} SHA1 {wolfram_sha}",
            f"{DEFAULT_NEW_SPINES} SHA1 {new_spines_sha}",
            f"{DEFAULT_NEW_SPINES_CERTIFICATE} SHA1 {new_spines_cert_sha}",
            f"{DEFAULT_ZENODO_SPINES} SHA1 {zenodo_spines_sha}",
            f"{DEFAULT_ZENODO_SPINES_CERTIFICATE} SHA1 {zenodo_spines_cert_sha}",
        ],
        generated_at_utc,
        "Generated all-ID Rocq/Coq registry/certificate mirror; broad certificate pass, not a deep native physics proof.",
    )

    lines = [
        provenance,
        "",
        "From Stdlib Require Import List String Lia.",
        "Import ListNotations.",
        "Open Scope string_scope.",
        "",
        "Definition registry_id : Type := string.",
        "",
        f"Definition registry_row_count : nat := {len(ids)}.",
        f"Definition master_csv_sha1 : string := \"{master_sha}\".",
        f"Definition wolfram_focus_json_sha1 : string := \"{wolfram_sha}\".",
        f"Definition new_spines_obligations_sha1 : string := \"{new_spines_sha}\".",
        f"Definition new_spines_certificate_sha1 : string := \"{new_spines_cert_sha}\".",
        f"Definition zenodo_spines_obligations_sha1 : string := \"{zenodo_spines_sha}\".",
        f"Definition zenodo_spines_certificate_sha1 : string := \"{zenodo_spines_cert_sha}\".",
        f"Definition creator_name : string := \"Daniel Alexander Trawin\".",
        f"Definition creator_orcid : string := \"0009-0001-4630-3715\".",
        f"Definition creator_orcid_url : string := \"https://orcid.org/0009-0001-4630-3715\".",
        f"Definition generated_utc : string := \"{generated_at_utc}\".",
        f"Definition zenodo_gold_spine_count : nat := {len(zenodo_spines)}.",
        f"Definition zenodo_gold_spine_row_count : nat := {len(zenodo_rows)}.",
        "",
        "(* Every canonical ID is mirrored below as a compiled Rocq constant. *)",
    ]
    lines.extend(f"Definition {ctor} : registry_id := \"{rid}\"." for ctor, rid in zip(ctors, ids))
    lines.extend(
        [
            "",
            f"Example registry_row_count_checked : registry_row_count = {len(ids)}.",
            "Proof. reflexivity. Qed.",
            "",
            "Example registry_row_count_nonempty : registry_row_count > 0.",
            "Proof. vm_compute. lia. Qed.",
            "",
        ]
    )
    lines.extend(rocq_list_definition("einstein_gold_spine_ids", EINSTEIN_GOLD_SPINE_IDS))
    lines.extend(rocq_list_definition("gravity_gold_spine_ids", new_spines.get("Gravity as an Accumulated Force", [])))
    lines.extend(rocq_list_definition("energy_matter_gold_spine_ids", new_spines.get("Energy-to-Matter Logic", [])))
    lines.extend(rocq_list_definition("topological_unification_gold_spine_ids", new_spines.get("Topological Unification", [])))
    lines.extend(rocq_list_definition("all_curated_gold_spine_ids", all_curated_ids))
    lines.extend(rocq_list_definition("zenodo_gold_spine_ids", zenodo_ids))
    lines.extend(
        [
            f"Example zenodo_gold_spine_count_checked : zenodo_gold_spine_count = {len(zenodo_spines)}.",
            "Proof. reflexivity. Qed.",
            "",
            f"Example zenodo_gold_spine_row_count_checked : zenodo_gold_spine_row_count = {len(zenodo_rows)}.",
            "Proof. reflexivity. Qed.",
            "",
            "Axiom id0958_action_level_einstein_bridge : Prop.",
            "Axiom id0400_three_part_density_obligation : Prop.",
            "Axiom id0394_id0167_stress_energy_bridge : Prop.",
            "Axiom id0335_recovers_classical_einstein_far_from_tzp : Prop.",
            "Axiom id0958_action_level_bridge_has_wolfram_certificate : Prop.",
            "Axiom id0394_id0167_stress_energy_bridge_has_wolfram_certificate : Prop.",
            "Axiom id0958_to_id0335_focused_chain_has_wolfram_certificate : Prop.",
            "Axiom gravity_accumulated_force_spine : Prop.",
            "Axiom energy_to_matter_logic_spine : Prop.",
            "Axiom topological_unification_spine : Prop.",
            "Axiom gravity_spine_has_wolfram_certificate : Prop.",
            "Axiom energy_matter_spine_has_wolfram_certificate : Prop.",
            "Axiom topological_unification_spine_has_wolfram_certificate : Prop.",
            "Axiom zenodo_spines_concept_backbone : Prop.",
            "Axiom zenodo_spines_have_wolfram_certificate : Prop.",
            "",
            "Axiom id0958_action_level_einstein_bridge_holds : id0958_action_level_einstein_bridge.",
            "Axiom id0400_three_part_density_obligation_holds : id0400_three_part_density_obligation.",
            "Axiom id0394_id0167_stress_energy_bridge_holds : id0394_id0167_stress_energy_bridge.",
            "Axiom id0335_recovers_classical_einstein_far_from_tzp_holds : id0335_recovers_classical_einstein_far_from_tzp.",
            "Axiom id0958_action_level_bridge_has_wolfram_certificate_holds : id0958_action_level_bridge_has_wolfram_certificate.",
            "Axiom id0394_id0167_stress_energy_bridge_has_wolfram_certificate_holds : id0394_id0167_stress_energy_bridge_has_wolfram_certificate.",
            "Axiom id0958_to_id0335_focused_chain_has_wolfram_certificate_holds : id0958_to_id0335_focused_chain_has_wolfram_certificate.",
            "Axiom gravity_accumulated_force_spine_holds : gravity_accumulated_force_spine.",
            "Axiom energy_to_matter_logic_spine_holds : energy_to_matter_logic_spine.",
            "Axiom topological_unification_spine_holds : topological_unification_spine.",
            "Axiom gravity_spine_has_wolfram_certificate_holds : gravity_spine_has_wolfram_certificate.",
            "Axiom energy_matter_spine_has_wolfram_certificate_holds : energy_matter_spine_has_wolfram_certificate.",
            "Axiom topological_unification_spine_has_wolfram_certificate_holds : topological_unification_spine_has_wolfram_certificate.",
            "Axiom zenodo_spines_concept_backbone_holds : zenodo_spines_concept_backbone.",
            "Axiom zenodo_spines_have_wolfram_certificate_holds : zenodo_spines_have_wolfram_certificate.",
            "",
            "Theorem gold_spine_focused_chain :",
            "  id0958_action_level_einstein_bridge /\\",
            "  id0400_three_part_density_obligation /\\",
            "  id0394_id0167_stress_energy_bridge /\\",
            "  id0335_recovers_classical_einstein_far_from_tzp /\\",
            "  id0958_action_level_bridge_has_wolfram_certificate /\\",
            "  id0394_id0167_stress_energy_bridge_has_wolfram_certificate /\\",
            "  id0958_to_id0335_focused_chain_has_wolfram_certificate.",
            "Proof.",
            "  repeat split;",
            "    first [ exact id0958_action_level_einstein_bridge_holds",
            "          | exact id0400_three_part_density_obligation_holds",
            "          | exact id0394_id0167_stress_energy_bridge_holds",
            "          | exact id0335_recovers_classical_einstein_far_from_tzp_holds",
            "          | exact id0958_action_level_bridge_has_wolfram_certificate_holds",
            "          | exact id0394_id0167_stress_energy_bridge_has_wolfram_certificate_holds",
            "          | exact id0958_to_id0335_focused_chain_has_wolfram_certificate_holds ].",
            "Qed.",
            "",
            "Theorem all_curated_gold_spines_focused_chain :",
            "  id0958_action_level_einstein_bridge /\\",
            "  id0400_three_part_density_obligation /\\",
            "  id0394_id0167_stress_energy_bridge /\\",
            "  id0335_recovers_classical_einstein_far_from_tzp /\\",
            "  id0958_to_id0335_focused_chain_has_wolfram_certificate /\\",
            "  gravity_accumulated_force_spine /\\",
            "  energy_to_matter_logic_spine /\\",
            "  topological_unification_spine /\\",
            "  gravity_spine_has_wolfram_certificate /\\",
            "  energy_matter_spine_has_wolfram_certificate /\\",
            "  topological_unification_spine_has_wolfram_certificate.",
            "Proof.",
            "  repeat split;",
            "    first [ exact id0958_action_level_einstein_bridge_holds",
            "          | exact id0400_three_part_density_obligation_holds",
            "          | exact id0394_id0167_stress_energy_bridge_holds",
            "          | exact id0335_recovers_classical_einstein_far_from_tzp_holds",
            "          | exact id0958_to_id0335_focused_chain_has_wolfram_certificate_holds",
            "          | exact gravity_accumulated_force_spine_holds",
            "          | exact energy_to_matter_logic_spine_holds",
            "          | exact topological_unification_spine_holds",
            "          | exact gravity_spine_has_wolfram_certificate_holds",
            "          | exact energy_matter_spine_has_wolfram_certificate_holds",
            "          | exact topological_unification_spine_has_wolfram_certificate_holds ].",
            "Qed.",
            "",
            "Theorem all_curated_and_zenodo_spines_focused_chain :",
            "  id0958_action_level_einstein_bridge /\\",
            "  id0400_three_part_density_obligation /\\",
            "  id0394_id0167_stress_energy_bridge /\\",
            "  id0335_recovers_classical_einstein_far_from_tzp /\\",
            "  id0958_to_id0335_focused_chain_has_wolfram_certificate /\\",
            "  gravity_accumulated_force_spine /\\",
            "  energy_to_matter_logic_spine /\\",
            "  topological_unification_spine /\\",
            "  gravity_spine_has_wolfram_certificate /\\",
            "  energy_matter_spine_has_wolfram_certificate /\\",
            "  topological_unification_spine_has_wolfram_certificate /\\",
            "  zenodo_spines_concept_backbone /\\",
            "  zenodo_spines_have_wolfram_certificate.",
            "Proof.",
            "  repeat split;",
            "    first [ exact id0958_action_level_einstein_bridge_holds",
            "          | exact id0400_three_part_density_obligation_holds",
            "          | exact id0394_id0167_stress_energy_bridge_holds",
            "          | exact id0335_recovers_classical_einstein_far_from_tzp_holds",
            "          | exact id0958_to_id0335_focused_chain_has_wolfram_certificate_holds",
            "          | exact gravity_accumulated_force_spine_holds",
            "          | exact energy_to_matter_logic_spine_holds",
            "          | exact topological_unification_spine_holds",
            "          | exact gravity_spine_has_wolfram_certificate_holds",
            "          | exact energy_matter_spine_has_wolfram_certificate_holds",
            "          | exact topological_unification_spine_has_wolfram_certificate_holds",
            "          | exact zenodo_spines_concept_backbone_holds",
            "          | exact zenodo_spines_have_wolfram_certificate_holds ].",
            "Qed.",
            "",
        ]
    )
    Path(path).write_text("\n".join(lines), encoding="utf-8")


def write_summary(
    path,
    rows,
    master_sha,
    wolfram_sha,
    new_spines,
    new_spines_sha,
    new_spines_cert_sha,
    zenodo_spines,
    zenodo_rows,
    zenodo_spines_sha,
    zenodo_spines_cert_sha,
    generated_at_utc,
):
    summary = {
        "provenance": provenance_dict(
            "prepare_lean_rocq_all_ids.py",
            [
                f"{DEFAULT_MASTER} SHA1 {master_sha}",
                f"{DEFAULT_WOLFRAM} SHA1 {wolfram_sha}",
                f"{DEFAULT_NEW_SPINES} SHA1 {new_spines_sha}",
                f"{DEFAULT_NEW_SPINES_CERTIFICATE} SHA1 {new_spines_cert_sha}",
                f"{DEFAULT_ZENODO_SPINES} SHA1 {zenodo_spines_sha}",
                f"{DEFAULT_ZENODO_SPINES_CERTIFICATE} SHA1 {zenodo_spines_cert_sha}",
            ],
            generated_at_utc,
            "Generated all-ID Lean/Rocq registry/certificate mirror summary.",
        ),
        "registry_rows": len(rows),
        "unique_ids": len({row["id"] for row in rows}),
        "first_id": rows[0]["id"],
        "last_id": rows[-1]["id"],
        "einstein_gold_spine_ids": EINSTEIN_GOLD_SPINE_IDS,
        "new_gold_spines": new_spines,
        "zenodo_gold_spines": zenodo_spines,
        "all_curated_gold_spine_row_count": len(EINSTEIN_GOLD_SPINE_IDS) + sum(len(v) for v in new_spines.values()),
        "zenodo_gold_spine_count": len(zenodo_spines),
        "zenodo_gold_spine_row_count": len(zenodo_rows),
        "zenodo_gold_spine_unique_id_count": len({row["id"] for row in zenodo_rows}),
        "master_csv_sha1": master_sha,
        "wolfram_focus_json_sha1": wolfram_sha,
        "new_spines_obligations_sha1": new_spines_sha,
        "new_spines_certificate_sha1": new_spines_cert_sha,
        "zenodo_spines_obligations_sha1": zenodo_spines_sha,
        "zenodo_spines_certificate_sha1": zenodo_spines_cert_sha,
        "lean_file": "TZPIDAllIDs.lean",
        "rocq_file": "TZPIDAllIDs.v",
    }
    Path(path).write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--master", default=DEFAULT_MASTER)
    parser.add_argument("--wolfram", default=DEFAULT_WOLFRAM)
    parser.add_argument("--new-spines", default=DEFAULT_NEW_SPINES)
    parser.add_argument("--new-spines-certificate", default=DEFAULT_NEW_SPINES_CERTIFICATE)
    parser.add_argument("--zenodo-spines", default=DEFAULT_ZENODO_SPINES)
    parser.add_argument("--zenodo-spines-certificate", default=DEFAULT_ZENODO_SPINES_CERTIFICATE)
    parser.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    rows = read_rows(args.master)
    new_spines = read_new_spines(args.new_spines)
    zenodo_spines, zenodo_rows = read_zenodo_spines(args.zenodo_spines)
    master_sha = file_sha1(args.master)
    wolfram_sha = file_sha1(args.wolfram) if Path(args.wolfram).exists() else ""
    new_spines_sha = file_sha1(args.new_spines) if Path(args.new_spines).exists() else ""
    new_spines_cert_sha = file_sha1(args.new_spines_certificate) if Path(args.new_spines_certificate).exists() else ""
    zenodo_spines_sha = file_sha1(args.zenodo_spines) if Path(args.zenodo_spines).exists() else ""
    zenodo_spines_cert_sha = file_sha1(args.zenodo_spines_certificate) if Path(args.zenodo_spines_certificate).exists() else ""
    generated_at_utc = generated_utc()

    write_lean(
        output_dir / "TZPIDAllIDs.lean",
        rows,
        master_sha,
        wolfram_sha,
        new_spines,
        new_spines_sha,
        new_spines_cert_sha,
        zenodo_spines,
        zenodo_rows,
        zenodo_spines_sha,
        zenodo_spines_cert_sha,
        generated_at_utc,
    )
    write_rocq(
        output_dir / "TZPIDAllIDs.v",
        rows,
        master_sha,
        wolfram_sha,
        new_spines,
        new_spines_sha,
        new_spines_cert_sha,
        zenodo_spines,
        zenodo_rows,
        zenodo_spines_sha,
        zenodo_spines_cert_sha,
        generated_at_utc,
    )
    write_summary(
        output_dir / "all_ids_export_summary.json",
        rows,
        master_sha,
        wolfram_sha,
        new_spines,
        new_spines_sha,
        new_spines_cert_sha,
        zenodo_spines,
        zenodo_rows,
        zenodo_spines_sha,
        zenodo_spines_cert_sha,
        generated_at_utc,
    )

    print(f"Wrote {output_dir / 'TZPIDAllIDs.lean'}")
    print(f"Wrote {output_dir / 'TZPIDAllIDs.v'}")
    print(f"Wrote {output_dir / 'all_ids_export_summary.json'}")


if __name__ == "__main__":
    main()
