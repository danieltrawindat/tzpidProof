import argparse
import csv
import hashlib
import re
from pathlib import Path

import pandas as pd


DEFAULT_CANDIDATES = "zenodo_tex_axiom_theory_scan/axiom_theory_candidates.csv"
DEFAULT_OUTPUT_DIR = "isabelle_tzpid"

KIND_TYPE_PREDICATE = {
    "Axiom": ("axiom_claim", "registered_axiom"),
    "Theorem": ("theorem_claim", "registered_theorem"),
    "Lemma": ("lemma_claim", "registered_lemma"),
    "Postulate": ("postulate_claim", "registered_postulate"),
    "Principle": ("principle_claim", "registered_principle"),
    "Definition": ("definition_claim", "registered_definition"),
    "Proposition": ("proposition_claim", "registered_proposition"),
    "Corollary": ("corollary_claim", "registered_corollary"),
    "Hypothesis": ("hypothesis_claim", "registered_hypothesis"),
    "Conjecture": ("conjecture_claim", "registered_conjecture"),
    "Invariant": ("invariant_claim", "registered_invariant"),
    "Law": ("law_claim", "registered_law"),
}


def ascii_clean(value, max_len=120):
    text = "" if pd.isna(value) else str(value)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"\s+", " ", text).strip()
    text = text.replace("''", "'")
    return text[:max_len]


def isa_string(value, max_len=120):
    text = ascii_clean(value, max_len=max_len)
    text = text.replace("\\", "/")
    text = text.replace("''", "'")
    return f"''{text}''"


def isa_name(value, prefix, max_len=56):
    raw = ascii_clean(value, max_len=max_len).lower()
    raw = re.sub(r"[^a-z0-9_]+", "_", raw)
    raw = re.sub(r"_+", "_", raw).strip("_")
    if not raw:
        raw = prefix
    if raw[0].isdigit():
        raw = f"{prefix}_{raw}"
    return raw


def file_hash(path):
    digest = hashlib.sha1()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def dataframe_digest(df):
    digest = hashlib.sha1()
    for _, row in df.iterrows():
        raw = "|".join(
            str(row.get(col, ""))
            for col in ["rank", "score", "kind", "title", "source", "line", "digest"]
        )
        digest.update(raw.encode("utf-8", errors="ignore"))
        digest.update(b"\n")
    return digest.hexdigest()


def load_candidates(path):
    df = pd.read_csv(path)
    df["rank"] = df["rank"].astype(int)
    return df.sort_values("rank", kind="stable")


def candidate_symbol(row, used):
    rank = int(row.get("rank", 0))
    kind = isa_name(row.get("kind", "candidate"), "candidate", 18)
    title = isa_name(row.get("title", ""), "claim", 48)
    base = f"cand_{rank:03d}_{kind}_{title}"
    name = base
    suffix = 2
    while name in used:
        name = f"{base}_{suffix}"
        suffix += 1
    used.add(name)
    return name


def update_root(output_dir):
    (output_dir / "ROOT").write_text(
        """session TZPID = HOL +
  options [document = false]
  theories
    TZPID_Manifest
    TZPID_Axioms
    TZPID_Core
""",
        encoding="utf-8",
    )


def write_candidate_map(output_dir, candidates):
    path = output_dir / "core_candidate_id_map.csv"
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "rank",
                "isabelle_name",
                "claim_type",
                "registration_predicate",
                "kind",
                "score",
                "title",
                "source",
                "line",
                "digest",
            ],
        )
        writer.writeheader()
        for cand in candidates:
            writer.writerow(cand)
    return path


def declaration_blocks(candidates):
    by_type = {}
    for cand in candidates:
        by_type.setdefault(cand["claim_type"], []).append(cand["isabelle_name"])

    lines = []
    for claim_type in sorted(by_type):
        lines.append("consts")
        for name in by_type[claim_type]:
            lines.append(f"  {name} :: {claim_type}")
        lines.append("")
    return lines


def registration_assumptions(candidates):
    lines = ["locale TZPID_Core_Candidate_Inventory ="]
    assumptions = []
    for i, cand in enumerate(candidates):
        keyword = "assumes" if i == 0 else "and"
        assumptions.append(
            f"  {keyword} {cand['isabelle_name']}_registered: "
            f"\"{cand['registration_predicate']} {cand['isabelle_name']}\""
        )
    lines.extend(assumptions)
    lines.extend(
        [
            "begin",
            "",
            "lemma candidate_inventory_loaded: \"True\"",
            "  by simp",
            "",
            "end",
            "",
        ]
    )
    return lines


def write_core_theory(output_dir, candidate_rows, candidates_path):
    kind_counts = candidate_rows["kind"].value_counts().to_dict()
    used = set()
    candidates = []
    for _, row in candidate_rows.iterrows():
        kind = str(row.get("kind", "Candidate"))
        claim_type, predicate = KIND_TYPE_PREDICATE.get(kind, ("candidate_claim", "registered_candidate"))
        candidates.append(
            {
                "rank": int(row.get("rank", 0)),
                "isabelle_name": candidate_symbol(row, used),
                "claim_type": claim_type,
                "registration_predicate": predicate,
                "kind": kind,
                "score": row.get("score", ""),
                "title": row.get("title", ""),
                "source": row.get("source", ""),
                "line": row.get("line", ""),
                "digest": row.get("digest", ""),
            }
        )

    kind_count_lines = []
    for kind in sorted(KIND_TYPE_PREDICATE):
        kind_count_lines.append(f"    ({isa_string(kind, 40)}, {int(kind_counts.get(kind, 0))})")

    lines = [
        "theory TZPID_Core",
        "  imports TZPID_Manifest",
        "begin",
        "",
        "text \\<open>",
        "  Focused typed core for TZPID. This theory gives the clean TZPID spine",
        "  explicit object types and predicates, while registering all scanned",
        "  D:/Zenodo and D:/Tex candidates as typed claim objects.",
        "\\<close>",
        "",
        "typedecl tzp_point",
        "typedecl tzp_manifold",
        "typedecl information_carrier",
        "typedecl helix_parameter",
        "typedecl trawin_realization",
        "typedecl trawin_closure",
        "typedecl branch_symmetry",
        "typedecl quantum_state",
        "typedecl density_operator",
        "typedecl hamiltonian",
        "typedecl liouvillian",
        "typedecl natural_transformation",
        "typedecl encoding_space",
        "typedecl metamaterial_state",
        "typedecl field_observable",
        "typedecl correspondence",
        "",
        "typedecl axiom_claim",
        "typedecl theorem_claim",
        "typedecl lemma_claim",
        "typedecl postulate_claim",
        "typedecl principle_claim",
        "typedecl definition_claim",
        "typedecl proposition_claim",
        "typedecl corollary_claim",
        "typedecl hypothesis_claim",
        "typedecl conjecture_claim",
        "typedecl invariant_claim",
        "typedecl law_claim",
        "typedecl candidate_claim",
        "",
        "consts",
        "  registered_axiom :: \"axiom_claim \\<Rightarrow> bool\"",
        "  registered_theorem :: \"theorem_claim \\<Rightarrow> bool\"",
        "  registered_lemma :: \"lemma_claim \\<Rightarrow> bool\"",
        "  registered_postulate :: \"postulate_claim \\<Rightarrow> bool\"",
        "  registered_principle :: \"principle_claim \\<Rightarrow> bool\"",
        "  registered_definition :: \"definition_claim \\<Rightarrow> bool\"",
        "  registered_proposition :: \"proposition_claim \\<Rightarrow> bool\"",
        "  registered_corollary :: \"corollary_claim \\<Rightarrow> bool\"",
        "  registered_hypothesis :: \"hypothesis_claim \\<Rightarrow> bool\"",
        "  registered_conjecture :: \"conjecture_claim \\<Rightarrow> bool\"",
        "  registered_invariant :: \"invariant_claim \\<Rightarrow> bool\"",
        "  registered_law :: \"law_claim \\<Rightarrow> bool\"",
        "  registered_candidate :: \"candidate_claim \\<Rightarrow> bool\"",
        "",
        "consts",
        "  TZP :: tzp_point",
        "  M_helix :: tzp_manifold",
        "  M_holographic :: tzp_manifold",
        "  Euclidean3 :: tzp_manifold",
        "  DNA_helix :: tzp_manifold",
        "  DAANSphere153600 :: encoding_space",
        "  MetaEncoding :: metamaterial_state",
        "  TRAWIN_Core_Realization :: trawin_realization",
        "  TRAWIN_Core_Closure :: trawin_closure",
        "  BranchExchange :: branch_symmetry",
        "  H_Trawin :: hamiltonian",
        "  H_tunnel :: hamiltonian",
        "  H_ER :: hamiltonian",
        "  H_SC :: hamiltonian",
        "  H_cymatic :: hamiltonian",
        "  H_TZP :: hamiltonian",
        "  Rho_Trawin :: density_operator",
        "  L_Trawin :: liouvillian",
        "  Methylation_U_to_T :: natural_transformation",
        "  HelicalProjection :: natural_transformation",
        "  HolographicHelical_Duality :: correspondence",
        "  MagneticFlux :: field_observable",
        "  HelicityInvariant :: field_observable",
        "  GyromagneticCoupling :: field_observable",
        "",
        "consts",
        "  unique_tzp :: \"tzp_point \\<Rightarrow> bool\"",
        "  fixed_locus_point :: \"tzp_point \\<Rightarrow> branch_symmetry \\<Rightarrow> bool\"",
        "  admissible_realization :: \"trawin_realization \\<Rightarrow> bool\"",
        "  closure_of :: \"trawin_realization \\<Rightarrow> trawin_closure \\<Rightarrow> bool\"",
        "  closed_admissibly :: \"trawin_closure \\<Rightarrow> bool\"",
        "  embeds_into :: \"tzp_manifold \\<Rightarrow> tzp_manifold \\<Rightarrow> bool\"",
        "  logarithmic_helical :: \"tzp_manifold \\<Rightarrow> bool\"",
        "  pi_phi_coupled :: \"tzp_manifold \\<Rightarrow> bool\"",
        "  hamiltonian_component :: \"hamiltonian \\<Rightarrow> hamiltonian \\<Rightarrow> bool\"",
        "  governs_density :: \"hamiltonian \\<Rightarrow> density_operator \\<Rightarrow> bool\"",
        "  evolves_by_liouvillian :: \"density_operator \\<Rightarrow> liouvillian \\<Rightarrow> bool\"",
        "  functorial_transition :: \"natural_transformation \\<Rightarrow> bool\"",
        "  projects_to_encoding :: \"natural_transformation \\<Rightarrow> encoding_space \\<Rightarrow> bool\"",
        "  encodes_metamaterial_state :: \"metamaterial_state \\<Rightarrow> encoding_space \\<Rightarrow> bool\"",
        "  corresponds :: \"correspondence \\<Rightarrow> tzp_manifold \\<Rightarrow> tzp_manifold \\<Rightarrow> bool\"",
        "  observable_of_core :: \"field_observable \\<Rightarrow> bool\"",
        "",
        "locale TZPID_Core_Spine =",
        "  assumes tzp_unique: \"unique_tzp TZP\"",
        "  and tzp_fixed: \"fixed_locus_point TZP BranchExchange\"",
        "  and trawin_realization_admissible: \"admissible_realization TRAWIN_Core_Realization\"",
        "  and trawin_closure_bound: \"closure_of TRAWIN_Core_Realization TRAWIN_Core_Closure\"",
        "  and trawin_closure_admissible: \"closed_admissibly TRAWIN_Core_Closure\"",
        "  and axiom_i_embedding: \"embeds_into M_helix Euclidean3\"",
        "  and axiom_i_log_helix: \"logarithmic_helical M_helix\"",
        "  and postulate_pi_phi: \"pi_phi_coupled M_helix\"",
        "  and axiom_ii_tunnel: \"hamiltonian_component H_tunnel H_Trawin\"",
        "  and axiom_ii_er: \"hamiltonian_component H_ER H_Trawin\"",
        "  and axiom_ii_sc: \"hamiltonian_component H_SC H_Trawin\"",
        "  and axiom_ii_cymatic: \"hamiltonian_component H_cymatic H_Trawin\"",
        "  and axiom_ii_tzp: \"hamiltonian_component H_TZP H_Trawin\"",
        "  and axiom_iii_governs_density: \"governs_density H_Trawin Rho_Trawin\"",
        "  and axiom_iii_lindblad: \"evolves_by_liouvillian Rho_Trawin L_Trawin\"",
        "  and axiom_iv_dna_fibration: \"logarithmic_helical DNA_helix\"",
        "  and axiom_v_methylation: \"functorial_transition Methylation_U_to_T\"",
        "  and axiom_vii_projection: \"projects_to_encoding HelicalProjection DAANSphere153600\"",
        "  and axiom_viii_metamaterial: \"encodes_metamaterial_state MetaEncoding DAANSphere153600\"",
        "  and axiom_ix_holographic: \"corresponds HolographicHelical_Duality M_helix M_holographic\"",
        "  and observable_flux: \"observable_of_core MagneticFlux\"",
        "  and observable_helicity: \"observable_of_core HelicityInvariant\"",
        "  and observable_gyro: \"observable_of_core GyromagneticCoupling\"",
        "begin",
        "",
        "theorem core_hamiltonian_has_tzp_component:",
        "  \"hamiltonian_component H_TZP H_Trawin\"",
        "  by (rule axiom_ii_tzp)",
        "",
        "theorem core_has_holographic_helical_correspondence:",
        "  \"corresponds HolographicHelical_Duality M_helix M_holographic\"",
        "  by (rule axiom_ix_holographic)",
        "",
        "theorem core_tzp_is_unique_fixed_locus:",
        "  \"unique_tzp TZP \\<and> fixed_locus_point TZP BranchExchange\"",
        "  using tzp_unique tzp_fixed by simp",
        "",
        "end",
        "",
    ]

    lines.extend(declaration_blocks(candidates))
    lines.extend(registration_assumptions(candidates))
    lines.extend(
        [
            "definition core_candidate_inventory_sha1 :: string where",
            "  \"core_candidate_inventory_sha1 = " + isa_string(file_hash(candidates_path), 80) + "\"",
            "",
            "definition core_candidate_slice_sha1 :: string where",
            "  \"core_candidate_slice_sha1 = " + isa_string(dataframe_digest(candidate_rows), 80) + "\"",
            "",
            "definition core_candidate_count :: nat where",
            f"  \"core_candidate_count = {len(candidate_rows)}\"",
            "",
            "definition core_candidate_kind_counts :: \"(string * nat) list\" where",
            "  \"core_candidate_kind_counts = [",
            ",\n".join(kind_count_lines),
            "  ]\"",
            "",
            "lemma core_candidate_count_positive: \"core_candidate_count > 0\"",
            "  by (simp add: core_candidate_count_def)",
            "",
            "end",
            "",
        ]
    )

    (output_dir / "TZPID_Core.thy").write_text("\n".join(lines), encoding="utf-8")
    write_candidate_map(output_dir, candidates)


def main():
    parser = argparse.ArgumentParser(description="Generate a typed Isabelle TZPID core from the 618-candidate scan.")
    parser.add_argument("--candidates", default=DEFAULT_CANDIDATES)
    parser.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    rows = load_candidates(args.candidates)
    update_root(output_dir)
    write_core_theory(output_dir, rows, args.candidates)

    print(f"Wrote {output_dir / 'ROOT'}")
    print(f"Wrote {output_dir / 'TZPID_Core.thy'}")
    print(f"Wrote {output_dir / 'core_candidate_id_map.csv'}")
    print(f"Candidates: {len(rows)}")
    print("Kind counts:")
    for kind, count in rows["kind"].value_counts().sort_index().items():
        print(f"  {kind}: {count}")


if __name__ == "__main__":
    main()
