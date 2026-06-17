import argparse
import csv
import hashlib
import re
from pathlib import Path

import pandas as pd


DEFAULT_CORE_MAP = "isabelle_tzpid/core_candidate_id_map.csv"
DEFAULT_CANDIDATES = "zenodo_tex_axiom_theory_scan/axiom_theory_candidates.csv"
DEFAULT_ENCYCLOPEDIA = "TZPID_ENCYCLOPEDIA.md"
DEFAULT_DEPENDENCIES = "axiom_theorem_extraction/dependency_edges.csv"
DEFAULT_TOE_SHORTLIST = "toe_shortlist.csv"
DEFAULT_OUTPUT_DIR = "isabelle_tzpid"


CORE_TERMS = {
    "tzp",
    "trawin",
    "zero",
    "point",
    "helical",
    "holographic",
    "hamiltonian",
    "lindblad",
    "manifold",
    "metric",
    "curvature",
    "winding",
    "topological",
    "daansphere",
    "gyromagnetic",
    "invariant",
    "operator",
    "closure",
    "projection",
    "correspondence",
    "vacuum",
    "energy",
    "field",
    "quantum",
    "semiclassical",
    "classical",
    "limit",
}

TAG_PATTERNS = {
    "tzp_foundation": r"\btzp\b|trawin zero point|zero point",
    "trawin_operator": r"\btrawin\b|operator alphabet|closure|composition",
    "helical_geometry": r"helical|helix|lemniscate|winding",
    "holographic_duality": r"holographic|boundary|ads|correspondence",
    "hamiltonian_dynamics": r"hamiltonian|liouvillian|lindblad|schrodinger|master equation",
    "field_geometry": r"manifold|metric|curvature|connection|laplacian|d'alembertian",
    "topological_invariant": r"topological|invariant|charge|characteristic|cohomology|holonomy",
    "quantum_limit": r"quantum|semiclassical|hbar|decoherence|observable",
    "macro_reduction": r"classical|macro|limit|reduction|scale",
    "daansphere_encoding": r"daansphere|153600|encoding|metamaterial|projection",
    "gyromagnetic": r"gyromagnetic|elsasser|magnetic|helicity",
    "thermodynamic": r"entropy|thermodynamic|temperature|landauer|fluctuation|dissipation",
}

NOISY_PATTERNS = re.compile(r"\bsorry\b|\badmit\b|\btbd\b|conversation|proof\. admit", re.I)

TITLE_ANCHORS = [
    (re.compile(r"helical spacetime|helical.*embedding", re.I), "ID0113"),
    (re.compile(r"trawin transition hamiltonian|tzp hamiltonian|hamiltonian", re.I), "ID0030"),
    (re.compile(r"lindblad|master equation", re.I), "ID0066"),
    (re.compile(r"tzp uniqueness|existence and uniqueness|trawin zero point.*existence", re.I), "ID0000"),
    (re.compile(r"toroidal.*fibrational|dna.*fibration", re.I), "ID0053"),
    (re.compile(r"methylation|uracil|thymine|u_to_t|u to t", re.I), "ID9542"),
    (re.compile(r"zero.point coupling|vacuum energy density|zpe", re.I), "ID0024"),
    (re.compile(r"daansphere|153600|helical projection", re.I), "ID9564"),
    (re.compile(r"metamaterial.*encoding|encoding state", re.I), "ID0568"),
    (re.compile(r"holographic.*helical|helical.*holographic|correspondence", re.I), "ID9579"),
    (re.compile(r"trawinistic manifold", re.I), "ID0002"),
    (re.compile(r"least action", re.I), "ID0033"),
    (re.compile(r"topological charge", re.I), "ID0025"),
    (re.compile(r"information flux", re.I), "ID0026"),
    (re.compile(r"winding", re.I), "ID0020"),
    (re.compile(r"curvature singularity", re.I), "ID0022"),
    (re.compile(r"manifold curvature", re.I), "ID0016"),
    (re.compile(r"trawin base unit", re.I), "ID0006"),
    (re.compile(r"causal loop", re.I), "ID0011"),
    (re.compile(r"semiclassical", re.I), "ID0080"),
]


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


def sha1_text(text):
    return hashlib.sha1(str(text).encode("utf-8", errors="ignore")).hexdigest()


def file_hash(path):
    digest = hashlib.sha1()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def tokenize(text):
    return {
        token
        for token in re.findall(r"[a-zA-Z][a-zA-Z0-9]+", str(text).lower())
        if len(token) > 2
    }


def extract_encyclopedia(path):
    text = Path(path).read_text(encoding="utf-8", errors="ignore")
    entry_re = re.compile(
        r"^###\s+(ID\d{4})\s+[—-]\s+(.+?)\s*$\n(?P<body>.*?)(?=^###\s+ID\d{4}\s+[—-]|\Z)",
        re.M | re.S,
    )
    entries = []
    for match in entry_re.finditer(text):
        eid = match.group(1)
        title = match.group(2).strip()
        body = match.group("body").strip()
        entries.append(
            {
                "id": eid,
                "title": title,
                "body": body,
                "tokens": tokenize(title + " " + body),
                "digest": sha1_text(eid + "|" + title + "|" + body),
            }
        )
    return entries


def id_from_text(text):
    match = re.search(r"\bID\s*0*([0-9]{1,5})\b", str(text), re.I)
    if match:
        return f"ID{int(match.group(1)):04d}"
    return ""


def best_encyclopedia_match(row, entries):
    title_text = str(row.get("title", ""))
    source_text = str(row.get("source", ""))
    for pattern, anchor in TITLE_ANCHORS:
        if pattern.search(title_text) or pattern.search(source_text):
            for entry in entries:
                if entry["id"] == anchor:
                    return entry, 1200

    explicit = id_from_text(row.get("title", "")) or id_from_text(row.get("body", ""))
    if explicit:
        for entry in entries:
            if entry["id"] == explicit:
                return entry, 1000

    candidate_tokens = tokenize(
        " ".join(
            str(row.get(col, ""))
            for col in ["title", "body", "source"]
        )
    )
    if not candidate_tokens:
        return None, 0

    best = None
    best_score = -1
    for entry in entries:
        overlap = candidate_tokens & entry["tokens"]
        weighted = len(overlap) + 2 * len(overlap & CORE_TERMS)
        if weighted > best_score:
            best = entry
            best_score = weighted
    return best, best_score


def semantic_tags(text):
    tags = []
    for tag, pattern in TAG_PATTERNS.items():
        if re.search(pattern, text, re.I):
            tags.append(tag)
    return tags or ["general_formal_candidate"]


def classify_role(row, tags, semantic_score):
    kind = str(row.get("kind", ""))
    title = str(row.get("title", ""))
    source = str(row.get("source", ""))
    body = str(row.get("body", ""))
    score = float(row.get("score", 0) or 0)
    haystack = f"{title} {source} {body}"

    if NOISY_PATTERNS.search(haystack):
        if kind in {"Theorem", "Lemma", "Proposition", "Corollary"}:
            return "Needs_Semantic_Translation"
        if score < 70:
            return "Needs_Semantic_Translation"

    if kind in {"Hypothesis", "Conjecture"}:
        return "Hypothesis_Only"
    if kind == "Definition":
        if semantic_score >= 4 or "tzp_foundation" in tags or "trawin_operator" in tags:
            return "Core_Definition"
        return "Needs_Semantic_Translation"
    if kind in {"Axiom", "Postulate"}:
        if score >= 95 or any(tag in tags for tag in ["tzp_foundation", "trawin_operator", "helical_geometry", "hamiltonian_dynamics", "holographic_duality"]):
            return "Core_Axiom"
        return "Needs_Semantic_Translation"
    if kind in {"Theorem", "Lemma", "Proposition", "Corollary", "Law", "Invariant", "Principle"}:
        if semantic_score >= 3 or tags:
            return "Derived_Theorem_Obligation"
        return "Needs_Semantic_Translation"
    return "Needs_Semantic_Translation"


def checks_for_role(role, tags):
    checks = ["semantic_grounding", "dependency_coverage"]
    if role in {"Core_Axiom", "Core_Definition"}:
        checks.append("core_spine_alignment")
    if role == "Derived_Theorem_Obligation":
        checks.extend(["dimensional_balance", "custom_algebraic_consistency", "limiting_reduction"])
    if role == "Hypothesis_Only":
        checks.extend(["falsifiability_note", "non_axiom_guard"])
    if "quantum_limit" in tags or "macro_reduction" in tags:
        checks.append("scale_transition_check")
    if "thermodynamic" in tags:
        checks.append("thermodynamic_consistency")
    return sorted(set(checks))


def load_csv(path):
    return pd.read_csv(path)


def dependency_counts(path):
    if not Path(path).exists():
        return {}
    df = pd.read_csv(path)
    counts = {}
    for col in ["source_id", "target_id"]:
        if col in df.columns:
            for value, count in df[col].astype(str).value_counts().items():
                counts[value] = counts.get(value, 0) + int(count)
    return counts


def shortlist_ids(path):
    if not Path(path).exists():
        return set()
    df = pd.read_csv(path)
    if "ID" not in df.columns:
        return set()
    return set(df["ID"].astype(str))


def build_obligations(args):
    candidates = load_csv(args.candidates)
    core_map = load_csv(args.core_map)
    merged = candidates.merge(
        core_map[["rank", "isabelle_name", "claim_type", "registration_predicate"]],
        on="rank",
        how="left",
        suffixes=("", "_core"),
    )
    entries = extract_encyclopedia(args.encyclopedia)
    dep_counts = dependency_counts(args.dependencies)
    parsed_ids = shortlist_ids(args.toe_shortlist)

    rows = []
    for _, row in merged.iterrows():
        entry, semantic_score = best_encyclopedia_match(row, entries)
        text = " ".join(str(row.get(col, "")) for col in ["title", "body", "source"])
        tags = semantic_tags(text + " " + (entry["body"] if entry else ""))
        role = classify_role(row, tags, semantic_score)
        anchor_id = entry["id"] if entry else ""
        source_id = id_from_text(row.get("title", "")) or anchor_id
        checks = checks_for_role(role, tags)
        rows.append(
            {
                "rank": int(row.get("rank", 0)),
                "isabelle_name": row.get("isabelle_name", ""),
                "claim_type": row.get("claim_type", ""),
                "kind": row.get("kind", ""),
                "score": row.get("score", ""),
                "title": row.get("title", ""),
                "source": row.get("source", ""),
                "line": row.get("line", ""),
                "candidate_digest": row.get("digest", ""),
                "semantic_anchor_id": anchor_id,
                "semantic_anchor_title": entry["title"] if entry else "",
                "semantic_score": semantic_score,
                "semantic_digest": entry["digest"] if entry else "",
                "obligation_role": role,
                "semantic_tags": ";".join(tags),
                "required_checks": ";".join(checks),
                "dependency_degree": dep_counts.get(source_id, 0),
                "has_parsed_equation": "yes" if source_id in parsed_ids else "no",
                "obligation_digest": sha1_text(
                    "|".join(
                        str(v)
                        for v in [
                            row.get("rank", ""),
                            row.get("isabelle_name", ""),
                            row.get("kind", ""),
                            row.get("digest", ""),
                            anchor_id,
                            role,
                            ";".join(tags),
                            ";".join(checks),
                        ]
                    )
                ),
            }
        )
    return pd.DataFrame(rows)


def update_root(output_dir):
    (output_dir / "ROOT").write_text(
        """session TZPID = HOL +
  options [document = false]
  theories
    TZPID_Manifest
    TZPID_Axioms
    TZPID_Core
    TZPID_Obligations
""",
        encoding="utf-8",
    )


def role_predicate_name(role):
    return {
        "Core_Axiom": "core_axiom_obligation",
        "Core_Definition": "core_definition_obligation",
        "Derived_Theorem_Obligation": "derived_theorem_obligation",
        "Hypothesis_Only": "hypothesis_obligation",
        "Needs_Semantic_Translation": "semantic_translation_obligation",
    }.get(role, "semantic_translation_obligation")


def role_predicate_type(role, claim_type):
    return f"{role_predicate_name(role)}_{claim_type}"


def write_theory(output_dir, obligations, paths):
    role_counts = obligations["obligation_role"].value_counts().to_dict()
    check_counts = {}
    for checks in obligations["required_checks"].fillna(""):
        for check in str(checks).split(";"):
            if check:
                check_counts[check] = check_counts.get(check, 0) + 1

    role_lines = [f"    ({isa_string(role, 80)}, {int(count)})" for role, count in sorted(role_counts.items())]
    check_lines = [f"    ({isa_string(check, 80)}, {int(count)})" for check, count in sorted(check_counts.items())]

    predicate_decls = []
    needed = sorted(
        {
            (row["obligation_role"], row["claim_type"])
            for _, row in obligations.iterrows()
            if str(row.get("claim_type", "")).strip()
        }
    )
    for role, claim_type in needed:
        predicate_decls.append(f"  {role_predicate_type(role, claim_type)} :: \"{claim_type} \\<Rightarrow> bool\"")

    assumption_lines = []
    for i, row in obligations.iterrows():
        keyword = "assumes" if i == 0 else "and"
        name = row["isabelle_name"]
        pred = role_predicate_type(row["obligation_role"], row["claim_type"])
        assumption_lines.append(f"  {keyword} {name}_obligation: \"{pred} {name}\"")

    ref_lines = []
    for _, row in obligations.iterrows():
        ref_lines.append(
            "    ("
            + str(int(row["rank"]))
            + ", "
            + isa_string(row["obligation_role"], 80)
            + ", "
            + isa_string(row["semantic_anchor_id"], 40)
            + ", "
            + isa_string(row["obligation_digest"], 80)
            + ")"
        )

    lines = [
        "theory TZPID_Obligations",
        "  imports TZPID_Core",
        "begin",
        "",
        "text \\<open>",
        "  Semantic proof-obligation layer generated from the 618 D:/Zenodo and",
        "  D:/Tex candidates, grounded against TZPID_ENCYCLOPEDIA.md where possible.",
        "  The predicates classify proof work; they do not assert completed physics.",
        "\\<close>",
        "",
        "consts",
        *predicate_decls,
        "",
        "locale TZPID_Proof_Obligations = TZPID_Core_Spine + TZPID_Core_Candidate_Inventory +",
        *assumption_lines,
        "begin",
        "",
        "lemma obligations_loaded: \"True\"",
        "  by simp",
        "",
        "end",
        "",
        "definition obligation_refs :: \"(nat * string * string * string) list\" where",
        "  \"obligation_refs = [",
        ",\n".join(ref_lines),
        "  ]\"",
        "",
        "definition obligation_inventory_sha1 :: string where",
        "  \"obligation_inventory_sha1 = " + isa_string(file_hash(paths["obligations_csv"]), 80) + "\"",
        "",
        "definition obligation_encyclopedia_sha1 :: string where",
        "  \"obligation_encyclopedia_sha1 = " + isa_string(file_hash(paths["encyclopedia"]), 80) + "\"",
        "",
        "definition obligation_candidate_scan_sha1 :: string where",
        "  \"obligation_candidate_scan_sha1 = " + isa_string(file_hash(paths["candidates"]), 80) + "\"",
        "",
        "definition obligation_count :: nat where",
        f"  \"obligation_count = {len(obligations)}\"",
        "",
        "definition obligation_role_counts :: \"(string * nat) list\" where",
        "  \"obligation_role_counts = [",
        ",\n".join(role_lines),
        "  ]\"",
        "",
        "definition obligation_check_counts :: \"(string * nat) list\" where",
        "  \"obligation_check_counts = [",
        ",\n".join(check_lines),
        "  ]\"",
        "",
        "lemma obligation_count_positive: \"obligation_count > 0\"",
        "  by (simp add: obligation_count_def)",
        "",
        "end",
        "",
    ]
    (output_dir / "TZPID_Obligations.thy").write_text("\n".join(lines), encoding="utf-8")


def write_report(output_dir, obligations):
    path = output_dir / "obligation_summary.md"
    lines = [
        "# TZPID Proof Obligation Summary",
        "",
        f"- Obligations: **{len(obligations)}**",
        "- Source candidates: `zenodo_tex_axiom_theory_scan/axiom_theory_candidates.csv`",
        "- Semantic source: `TZPID_ENCYCLOPEDIA.md`",
        "- Isabelle theory: `TZPID_Obligations.thy`",
        "",
        "## Roles",
        "",
    ]
    for role, count in obligations["obligation_role"].value_counts().sort_index().items():
        lines.append(f"- {role}: {count}")
    lines.extend(["", "## Top Grounded Obligations", ""])
    top = obligations.sort_values(["semantic_score", "score"], ascending=False).head(40)
    for _, row in top.iterrows():
        lines.extend(
            [
                f"### {int(row['rank'])}. {row['obligation_role']} - {row['title']}",
                "",
                f"- Isabelle: `{row['isabelle_name']}`",
                f"- Kind: `{row['kind']}`",
                f"- Semantic anchor: `{row['semantic_anchor_id']} - {row['semantic_anchor_title']}`",
                f"- Tags: `{row['semantic_tags']}`",
                f"- Checks: `{row['required_checks']}`",
                "",
            ]
        )
    path.write_text("\n".join(lines), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Generate Isabelle TZPID proof obligations.")
    parser.add_argument("--core-map", default=DEFAULT_CORE_MAP)
    parser.add_argument("--candidates", default=DEFAULT_CANDIDATES)
    parser.add_argument("--encyclopedia", default=DEFAULT_ENCYCLOPEDIA)
    parser.add_argument("--dependencies", default=DEFAULT_DEPENDENCIES)
    parser.add_argument("--toe-shortlist", default=DEFAULT_TOE_SHORTLIST)
    parser.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    obligations = build_obligations(args)
    obligations_csv = output_dir / "proof_obligations.csv"
    obligations.to_csv(obligations_csv, index=False)
    update_root(output_dir)
    write_theory(
        output_dir,
        obligations,
        {
            "obligations_csv": str(obligations_csv),
            "encyclopedia": args.encyclopedia,
            "candidates": args.candidates,
        },
    )
    write_report(output_dir, obligations)

    print(f"Wrote {obligations_csv}")
    print(f"Wrote {output_dir / 'TZPID_Obligations.thy'}")
    print(f"Wrote {output_dir / 'obligation_summary.md'}")
    print(f"Obligations: {len(obligations)}")
    print("Roles:")
    for role, count in obligations["obligation_role"].value_counts().sort_index().items():
        print(f"  {role}: {count}")


if __name__ == "__main__":
    main()
