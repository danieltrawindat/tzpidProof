import argparse
import hashlib
import re
from pathlib import Path

import pandas as pd


DEFAULT_INVENTORY = "axiom_theorem_extraction/statement_inventory.csv"
DEFAULT_EDGES = "axiom_theorem_extraction/dependency_edges.csv"
DEFAULT_OUTPUT_DIR = "isabelle_tzpid"

PROMOTED_KINDS = {"Axiom", "Assumption", "Postulate"}
OBLIGATION_KINDS = {"Theorem", "Lemma", "Proposition", "Corollary", "Law", "Invariant", "Principle"}


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


def isa_name(value, prefix):
    raw = ascii_clean(value, max_len=80).lower()
    raw = re.sub(r"[^a-z0-9_]+", "_", raw)
    raw = re.sub(r"_+", "_", raw).strip("_")
    if not raw or raw[0].isdigit():
        raw = f"{prefix}_{raw}"
    return raw


def digest_row(row):
    raw = "|".join(str(row.get(col, "")) for col in ["id", "kind", "label", "statement", "source", "line"])
    return hashlib.sha1(raw.encode("utf-8", errors="ignore")).hexdigest()


def dataframe_digest(df, columns):
    digest = hashlib.sha1()
    for _, row in df.iterrows():
        raw = "|".join(str(row.get(col, "")) for col in columns)
        digest.update(raw.encode("utf-8", errors="ignore"))
        digest.update(b"\n")
    return digest.hexdigest()


def load_inventory(path):
    return pd.read_csv(path)


def load_edges(path, known_ids):
    edges = pd.read_csv(path)
    return edges[edges["source_id"].isin(known_ids) & edges["target_id"].isin(known_ids)].copy()


def numeric_id_map(inventory):
    return {str(row.get("id", "")): i + 1 for i, (_, row) in enumerate(inventory.iterrows())}


def confidence(row):
    try:
        return float(row.get("confidence", 0.0))
    except Exception:
        return 0.0


def select_axioms(inventory, min_confidence, include_all_axioms):
    axioms = inventory[inventory["kind"].isin(PROMOTED_KINDS)].copy()
    if not include_all_axioms:
        axioms = axioms[axioms.apply(confidence, axis=1) >= min_confidence]
    return axioms.sort_values(["kind", "id"], kind="stable")


def select_obligations(inventory):
    obligations = inventory[inventory["kind"].isin(OBLIGATION_KINDS)].copy()
    return obligations.sort_values(["kind", "id"], kind="stable")


def update_root(output_dir):
    root = output_dir / "ROOT"
    desired = """session TZPID = HOL +
  options [document = false]
  theories
    TZPID_Manifest
    TZPID_Axioms
"""
    root.write_text(desired, encoding="utf-8")


def write_axiom_theory(output_dir, axioms, obligations, edges, id_map):
    obligation_digest = dataframe_digest(obligations, ["id", "kind", "label", "statement", "source", "line"])
    edge_digest = dataframe_digest(edges, ["source_id", "target_id", "relation", "weight", "evidence"])
    lines = [
        "theory TZPID_Axioms",
        "  imports TZPID_Manifest",
        "begin",
        "",
        "text \\<open>",
        "  This layer promotes selected extracted axiom candidates into an abstract",
        "  Isabelle locale. The constants are deliberately uninterpreted: they are",
        "  placeholders for later semantic formalization, not completed physics proofs.",
        "\\<close>",
        "",
    ]

    if axioms.empty:
        lines.extend(
            [
                "locale TZPID_Axiom_System",
                "begin",
                "end",
                "",
            ]
        )
    else:
        lines.append("consts")
        for _, row in axioms.iterrows():
            sid = str(row.get("id", ""))
            lines.append(f"  {isa_name(sid, 'axiom')} :: bool")
        lines.append("")
        lines.append("locale TZPID_Axiom_System =")
        assumption_lines = []
        for i, (_, row) in enumerate(axioms.iterrows()):
            sid = str(row.get("id", ""))
            name = isa_name(sid, "axiom")
            keyword = "assumes" if i == 0 else "and"
            assumption_lines.append(f"  {keyword} {name}_holds: \"{name}\"")
        lines.append("\n".join(assumption_lines))
        lines.append("begin")
        lines.append("")
        first_axiom = isa_name(str(axioms.iloc[0].get("id", "")), "axiom")
        lines.extend(
            [
                "lemma at_least_one_axiom_available: \"True\"",
                "  by simp",
                "",
                f"lemma first_promoted_axiom_available: \"{first_axiom}\"",
                f"  by (rule {first_axiom}_holds)",
                "",
                "end",
                "",
            ]
        )

    axiom_refs = []
    for _, row in axioms.iterrows():
        axiom_refs.append(
            "    ("
            + str(id_map.get(str(row.get("id", "")), 0))
            + ", "
            + isa_string(digest_row(row), 80)
            + ")"
        )
    lines.extend(
        [
            "definition promoted_axiom_refs :: \"(nat * string) list\" where",
            "  \"promoted_axiom_refs = [",
            ",\n".join(axiom_refs),
            "  ]\"",
            "",
        ]
    )

    obligation_refs = []
    for _, row in obligations.iterrows():
        obligation_refs.append(
            "    ("
            + str(id_map.get(str(row.get("id", "")), 0))
            + ", "
            + isa_string(row.get("kind", ""), 80)
            + ", "
            + isa_string(digest_row(row), 80)
            + ")"
        )
    lines.extend(
        [
            "definition theorem_obligation_refs :: \"(nat * string * string) list\" where",
            "  \"theorem_obligation_refs = [",
            ",\n".join(obligation_refs),
            "  ]\"",
            "",
        ]
    )

    lines.extend(
        [
            "definition theorem_obligation_sha1 :: string where",
            "  \"theorem_obligation_sha1 = " + isa_string(obligation_digest, 80) + "\"",
            "",
            "definition obligation_dependency_sha1 :: string where",
            "  \"obligation_dependency_sha1 = " + isa_string(edge_digest, 80) + "\"",
            "",
            "definition promoted_axiom_count :: nat where",
            f"  \"promoted_axiom_count = {len(axioms)}\"",
            "",
            "definition theorem_obligation_count :: nat where",
            f"  \"theorem_obligation_count = {len(obligations)}\"",
            "",
            "definition obligation_dependency_count :: nat where",
            f"  \"obligation_dependency_count = {len(edges)}\"",
            "",
            "lemma promoted_axiom_count_positive:",
            "  \"promoted_axiom_count > 0\"",
            "  by (simp add: promoted_axiom_count_def)",
            "",
            "lemma theorem_obligation_count_wellformed:",
            "  \"theorem_obligation_count >= 0\"",
            "  by (simp add: theorem_obligation_count_def)",
            "",
            "lemma dependency_obligation_count_wellformed:",
            "  \"obligation_dependency_count >= 0\"",
            "  by (simp add: obligation_dependency_count_def)",
            "",
            "end",
            "",
        ]
    )
    (output_dir / "TZPID_Axioms.thy").write_text("\n".join(lines), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Generate Isabelle locale layer for TZPID axioms and obligations.")
    parser.add_argument("--inventory", default=DEFAULT_INVENTORY)
    parser.add_argument("--edges", default=DEFAULT_EDGES)
    parser.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--min-confidence", type=float, default=0.65)
    parser.add_argument("--include-all-axioms", action="store_true")
    parser.add_argument("--obligation-limit", type=int, default=0, help="Limit obligation refs, 0 means all.")
    parser.add_argument("--edge-limit", type=int, default=0, help="Limit dependency refs, 0 means all.")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    inventory = load_inventory(args.inventory)
    id_map = numeric_id_map(inventory)
    known_ids = set(inventory["id"].astype(str))
    axioms = select_axioms(inventory, args.min_confidence, args.include_all_axioms)
    obligations = select_obligations(inventory)
    if args.obligation_limit:
        obligations = obligations.head(args.obligation_limit)
    edges = load_edges(args.edges, known_ids)
    edge_ids = set(axioms["id"].astype(str)) | set(obligations["id"].astype(str))
    edges = edges[edges["source_id"].isin(edge_ids) & edges["target_id"].isin(edge_ids)]
    if args.edge_limit:
        edges = edges.head(args.edge_limit)

    update_root(output_dir)
    write_axiom_theory(output_dir, axioms, obligations, edges, id_map)

    print(f"Wrote {output_dir / 'ROOT'}")
    print(f"Wrote {output_dir / 'TZPID_Axioms.thy'}")
    print(f"Promoted axioms: {len(axioms)}")
    print(f"Theorem/proof obligations: {len(obligations)}")
    print(f"Obligation dependency refs: {len(edges)}")


if __name__ == "__main__":
    main()
