import argparse
import csv
import hashlib
import re
from pathlib import Path

import pandas as pd


DEFAULT_INVENTORY = "axiom_theorem_extraction/statement_inventory.csv"
DEFAULT_EDGES = "axiom_theorem_extraction/dependency_edges.csv"
DEFAULT_OUTPUT_DIR = "isabelle_tzpid"

KIND_MAP = {
    "Axiom": "AxiomKind",
    "Definition": "DefinitionKind",
    "Theorem": "TheoremKind",
    "Lemma": "LemmaKind",
    "Proposition": "PropositionKind",
    "Corollary": "CorollaryKind",
    "Postulate": "PostulateKind",
    "Assumption": "AssumptionKind",
    "Invariant": "InvariantKind",
    "Principle": "PrincipleKind",
    "Law": "LawKind",
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


def statement_hash(row):
    raw = "|".join(str(row.get(col, "")) for col in ["id", "kind", "label", "statement", "source", "line"])
    return hashlib.sha1(raw.encode("utf-8", errors="ignore")).hexdigest()


def file_hash(path):
    digest = hashlib.sha1()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_inventory(path, limit):
    df = pd.read_csv(path)
    if limit:
        df = df.head(limit)
    return df


def load_edges(path, known_ids, limit):
    df = pd.read_csv(path)
    df = df[df["source_id"].isin(known_ids) & df["target_id"].isin(known_ids)].copy()
    if limit:
        df = df.head(limit)
    return df


def write_root(output_dir):
    (output_dir / "ROOT").write_text(
        """session TZPID = HOL +
  options [document = false]
  theories
    TZPID_Manifest
    TZPID_Axioms
""",
        encoding="utf-8",
    )


def numeric_id_map(inventory):
    return {str(row.get("id", "")): i + 1 for i, (_, row) in enumerate(inventory.iterrows())}


def write_id_map(output_dir, inventory):
    path = output_dir / "statement_id_map.csv"
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["isabelle_sid", "source_id", "kind", "label", "source", "line", "digest"],
        )
        writer.writeheader()
        for i, (_, row) in enumerate(inventory.iterrows(), start=1):
            writer.writerow(
                {
                    "isabelle_sid": i,
                    "source_id": row.get("id", ""),
                    "kind": row.get("kind", ""),
                    "label": row.get("label", ""),
                    "source": row.get("source", ""),
                    "line": row.get("line", ""),
                    "digest": statement_hash(row),
                }
            )


def write_theory(output_dir, inventory, edges, inventory_path, edges_path):
    kind_counts = inventory["kind"].value_counts().to_dict()
    lines = [
        "theory TZPID_Manifest",
        "  imports Main",
        "begin",
        "",
        "datatype statement_kind =",
        "  AxiomKind",
        "  | DefinitionKind",
        "  | TheoremKind",
        "  | LemmaKind",
        "  | PropositionKind",
        "  | CorollaryKind",
        "  | PostulateKind",
        "  | AssumptionKind",
        "  | InvariantKind",
        "  | PrincipleKind",
        "  | LawKind",
        "  | UnknownKind",
        "",
        "record tzpid_statement =",
        "  sid :: nat",
        "  skind :: statement_kind",
        "  source_line :: nat",
        "  digest :: string",
        "",
        "record dependency_edge =",
        "  source_id :: nat",
        "  target_id :: nat",
        "  relation :: string",
        "  weight :: nat",
        "",
    ]

    kind_lines = []
    for source_kind, isa_kind in KIND_MAP.items():
        count = int(kind_counts.get(source_kind, 0))
        kind_lines.append(f"    ({isa_kind}, {count})")
    lines.extend(
        [
            "definition manifest_inventory_sha1 :: string where",
            "  \"manifest_inventory_sha1 = " + isa_string(file_hash(inventory_path), 80) + "\"",
            "",
            "definition manifest_edges_sha1 :: string where",
            "  \"manifest_edges_sha1 = " + isa_string(file_hash(edges_path), 80) + "\"",
            "",
            "definition statement_kind_counts :: \"(statement_kind * nat) list\" where",
            "  \"statement_kind_counts = [",
            ",\n".join(kind_lines),
            "  ]\"",
            "",
            "definition statement_count :: nat where",
            f"  \"statement_count = {len(inventory)}\"",
            "",
            "definition dependency_count :: nat where",
            f"  \"dependency_count = {len(edges)}\"",
            "",
            "lemma statement_manifest_nonempty: \"statement_count > 0\"",
            "  by (simp add: statement_count_def)",
            "",
            "lemma dependency_manifest_wellformed: \"dependency_count >= 0\"",
            "  by (simp add: dependency_count_def)",
            "",
            "end",
            "",
        ]
    )

    (output_dir / "TZPID_Manifest.thy").write_text("\n".join(lines), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Generate an Isabelle/HOL manifest from TZPID extraction artifacts.")
    parser.add_argument("--inventory", default=DEFAULT_INVENTORY)
    parser.add_argument("--edges", default=DEFAULT_EDGES)
    parser.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--limit", type=int, default=0, help="Limit statements, 0 means all.")
    parser.add_argument("--edge-limit", type=int, default=0, help="Limit dependency edges, 0 means all known-ID edges.")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    inventory = load_inventory(args.inventory, args.limit)
    known_ids = set(inventory["id"].astype(str))
    edges = load_edges(args.edges, known_ids, args.edge_limit)

    write_root(output_dir)
    write_id_map(output_dir, inventory)
    write_theory(output_dir, inventory, edges, args.inventory, args.edges)
    print(f"Wrote {output_dir / 'ROOT'}")
    print(f"Wrote {output_dir / 'statement_id_map.csv'}")
    print(f"Wrote {output_dir / 'TZPID_Manifest.thy'}")
    print(f"Statements: {len(inventory)}")
    print(f"Edges: {len(edges)}")


if __name__ == "__main__":
    main()
