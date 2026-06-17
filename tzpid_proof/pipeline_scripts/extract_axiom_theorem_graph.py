import argparse
import csv
import hashlib
import re
from collections import defaultdict
from pathlib import Path

import pandas as pd


KINDS = {
    "axiom": "Axiom",
    "definition": "Definition",
    "theorem": "Theorem",
    "lemma": "Lemma",
    "proposition": "Proposition",
    "corollary": "Corollary",
    "postulate": "Postulate",
    "assumption": "Assumption",
    "invariant": "Invariant",
    "principle": "Principle",
    "law": "Law",
}

ID_PREFIX = {
    "Axiom": "A",
    "Postulate": "P",
    "Assumption": "AS",
    "Invariant": "I",
    "Principle": "PR",
    "Law": "LAW",
    "Definition": "D",
    "Theorem": "T",
    "Lemma": "L",
    "Proposition": "PROP",
    "Corollary": "C",
}

STOPWORDS = {
    "the",
    "and",
    "for",
    "with",
    "that",
    "this",
    "from",
    "into",
    "where",
    "which",
    "must",
    "will",
    "have",
    "your",
    "file",
    "files",
    "axiom",
    "axioms",
    "definition",
    "definitions",
    "theorem",
    "theorems",
    "lemma",
    "lemmas",
    "proposition",
    "propositions",
    "canonical",
    "chapter",
    "status",
    "source",
    "result",
}

DEFAULT_ROOTS = [
    r"d:\Obsidian\pdf_pipeline_runs\pdf_dual_run_20260311_022638\storyline_bertopic_run_20260311_022719\obsidian_edit",
    r"d:\tzpidNEW",
    r"d:\Publishing\Publishing\TZP_OO\01_Mathematical_Foundations\Curry_Howard_Validation",
]

DEFAULT_CSVS = [
    "TZPID_ALL_IDS_CANONICAL_EQUATION_MASTER_with_export.csv",
]


def stable_hash(text):
    return hashlib.sha1(text.encode("utf-8", errors="ignore")).hexdigest()[:10]


def normalize_space(text):
    return re.sub(r"\s+", " ", text).strip()


def strip_markup(text):
    text = re.sub(r"`{1,3}", "", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    return normalize_space(text)


def token_set(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9_\\]+", " ", text)
    return {t for t in text.split() if len(t) >= 3 and t not in STOPWORDS}


def confidence_for(statement, kind, source):
    score = 0.45
    lower = statement.lower()
    source_lower = str(source).lower()
    if re.search(r"\b(a\d+|hh-a\d+|t\d+|l\d+)\b", lower):
        score += 0.15
    if any(marker in lower for marker in ["=", "\\", "∀", "∃", "implies", "->", "=>"]):
        score += 0.10
    if kind in {"Axiom", "Definition", "Theorem", "Lemma", "Proposition"}:
        score += 0.10
    if "chapter_" in source_lower or "dialogue" in source_lower:
        score -= 0.10
    if any(chatter in lower for chatter in ["i will", "you can", "what happens next", "reply with", "missing file"]):
        score -= 0.25
    if len(statement) < 16:
        score -= 0.20
    if len(statement) > 420:
        score -= 0.10
    return max(0.0, min(1.0, score))


def should_keep(statement):
    lower = statement.lower()
    if len(statement) < 8:
        return False
    if lower.startswith(("what happens next", "your response", "reply with", "if you want")):
        return False
    if "download the pack" in lower or "thought for" in lower:
        return False
    return True


def source_label(path):
    try:
        cwd = Path.cwd()
        return str(path.resolve().relative_to(cwd))
    except ValueError:
        return str(path)


def iter_text_files(roots):
    seen = set()
    for root in roots:
        path = Path(root)
        if not path.exists():
            continue
        if path.is_file():
            candidates = [path]
        else:
            candidates = [
                p
                for p in path.rglob("*")
                if p.is_file() and p.suffix.lower() in {".md", ".txt", ".tex"}
            ]
        for candidate in candidates:
            resolved = str(candidate.resolve()).lower()
            if resolved in seen:
                continue
            seen.add(resolved)
            yield candidate


def classify_csv_row(title, statement, dictionary):
    text = f"{title} {statement} {dictionary}".lower()
    for key, kind in KINDS.items():
        if re.search(rf"\b{re.escape(key)}\b", text):
            return kind
    return "Definition"


def extract_from_equation_master(csv_path):
    path = Path(csv_path)
    if not path.exists():
        return []

    df = pd.read_csv(path)
    records = []
    for index, row in df.iterrows():
        row_id = str(row.get("id", f"row_{index}"))
        title = normalize_space(str(row.get("title", "")))
        statement = normalize_space(str(row.get("canonical_statement", "")))
        equation = normalize_space(str(row.get("canonical_equation", "")))
        dictionary = normalize_space(str(row.get("dictionary", "")))
        encyclopedia = normalize_space(str(row.get("encyclopedia", "")))

        kind = classify_csv_row(title, statement, dictionary)
        pieces = []
        if statement and statement.lower() != "nan":
            pieces.append(statement)
        if equation and equation.lower() != "nan":
            pieces.append(f"Equation: {equation}")
        if dictionary and dictionary.lower() != "nan":
            pieces.append(f"Definition: {dictionary}")
        if not pieces and encyclopedia and encyclopedia.lower() != "nan":
            pieces.append(encyclopedia[:500])
        if not pieces:
            continue

        statement_text = " | ".join(pieces)
        confidence = confidence_for(statement_text, kind, path)
        if kind == "Definition":
            confidence = max(confidence, 0.62)
        if row_id.startswith("ID"):
            confidence = min(1.0, confidence + 0.05)

        records.append(
            {
                "kind": kind,
                "label": f"{row_id}: {title}" if title else row_id,
                "statement": statement_text,
                "source": f"{source_label(path)}#{row_id}",
                "line": int(index) + 2,
                "extraction": "equation_master_row",
                "confidence": confidence,
            }
        )

    return records


def read_file(path):
    return path.read_text(encoding="utf-8", errors="ignore")


def line_number(text, offset):
    return text.count("\n", 0, offset) + 1


def next_context(lines, start_index):
    collected = []
    for line in lines[start_index + 1 : start_index + 8]:
        stripped = line.strip()
        if not stripped:
            if collected:
                break
            continue
        if stripped.startswith("#"):
            break
        collected.append(stripped)
        if len(" ".join(collected)) > 500:
            break
    return strip_markup(" ".join(collected))


def statement_with_context(body, lines, index):
    body = strip_markup(body or "")
    context = next_context(lines, index)
    if context and (len(body) < 80 or not re.search(r"[.=\\∫∑]", body)):
        return normalize_space(f"{body}. {context}" if body else context)
    return body


def extract_from_text(path, text):
    records = []
    lines = text.splitlines()

    heading_re = re.compile(
        r"^\s{0,3}#{1,6}\s*(?P<kind>"
        + "|".join(KINDS)
        + r")\b\s*(?P<label>[A-Za-z0-9_.()\- ]{0,80})[:.\-–—]?\s*(?P<title>.*)$",
        re.IGNORECASE,
    )
    explicit_line_re = re.compile(
        r"^\s*(?:[-*]\s*)?(?P<kind>"
        + "|".join(KINDS)
        + r")\s*(?P<label>(?:[A-Z]{1,4}-)?[A-Za-z0-9IVX_.-]{0,16})?\s*[:.\-–—]\s*(?P<body>.+)$",
        re.IGNORECASE,
    )
    bold_statement_re = re.compile(
        r"^\s*\*\*(?P<kind>"
        + "|".join(KINDS)
        + r")\s*(?P<label>[^*:]{0,60})?\*\*[:.\-–—]?\s*(?P<body>.*)$",
        re.IGNORECASE,
    )
    proposition_quote_re = re.compile(
        r"^\s*[-*]\s*Proposition:\s*[\"“](?P<body>[^\"”]+)[\"”]",
        re.IGNORECASE,
    )
    roman_inline_re = re.compile(
        r"\b(?P<kind>Axiom|Theorem|Lemma|Definition|Proposition|Corollary)\s+"
        r"(?P<label>[IVX]+|[A-Z]{1,4}-?\d+|\d+)\s+"
        r"(?P<body>.*?)(?=\s+\b(?:Axiom|Theorem|Lemma|Definition|Proposition|Corollary)\s+(?:[IVX]+|[A-Z]{1,4}-?\d+|\d+)\s+|$)",
        re.IGNORECASE,
    )

    def add(kind, label, statement, line, extraction):
        kind = KINDS.get(kind.lower(), kind.title())
        statement = strip_markup(statement)
        label = strip_markup(label or "")
        if not statement and label:
            statement = label
            label = ""
        if not should_keep(statement):
            return
        records.append(
            {
                "kind": kind,
                "label": label,
                "statement": statement,
                "source": source_label(path),
                "line": line,
                "extraction": extraction,
                "confidence": confidence_for(statement, kind, path),
            }
        )

    for i, line in enumerate(lines):
        if match := heading_re.match(line):
            kind = match.group("kind")
            label = match.group("label").strip()
            title = match.group("title").strip()
            statement = title or label or next_context(lines, i)
            add(kind, label, statement, i + 1, "markdown_heading")
            continue

        if match := bold_statement_re.match(line):
            add(
                match.group("kind"),
                match.group("label") or "",
                match.group("body") or next_context(lines, i),
                i + 1,
                "bold_statement",
            )
            continue

        if match := explicit_line_re.match(line):
            add(
                match.group("kind"),
                match.group("label") or "",
                statement_with_context(match.group("body"), lines, i),
                i + 1,
                "explicit_line",
            )
            continue

        if match := proposition_quote_re.match(line):
            add("Proposition", "", match.group("body"), i + 1, "proposition_quote")

    for match in roman_inline_re.finditer(text):
        body = match.group("body")
        if len(body) > 260:
            body = re.split(r"\.\s+", body, maxsplit=1)[0]
        add(
            match.group("kind"),
            match.group("label"),
            body,
            line_number(text, match.start()),
            "inline_enumeration",
        )

    return records


def dedupe_records(records):
    best = {}
    preserved = []
    for record in records:
        if record.get("extraction") == "equation_master_row":
            preserved.append(record)
            continue
        key = (
            record["kind"],
            re.sub(r"[^a-z0-9]+", "", record["statement"].lower())[:180],
        )
        existing = best.get(key)
        if existing is None or record["confidence"] > existing["confidence"]:
            best[key] = record
    return preserved + list(best.values())


def assign_ids(records):
    counters = defaultdict(int)
    ordered = sorted(
        records,
        key=lambda r: (
            ["Axiom", "Postulate", "Assumption", "Invariant", "Principle", "Law", "Definition", "Theorem", "Lemma", "Proposition", "Corollary"].index(r["kind"])
            if r["kind"] in ID_PREFIX
            else 99,
            r["source"],
            r["line"],
        ),
    )
    for record in ordered:
        prefix = ID_PREFIX.get(record["kind"], "S")
        counters[prefix] += 1
        record["id"] = f"{prefix}{counters[prefix]}"
        if not record["label"]:
            record["label"] = record["id"]
    return ordered


def build_dependencies(records):
    by_id = {r["id"]: r for r in records}
    token_cache = {r["id"]: token_set(f"{r['label']} {r['statement']}") for r in records}
    support_kinds = {"Axiom", "Postulate", "Assumption", "Invariant", "Principle", "Law", "Definition"}
    result_kinds = {"Theorem", "Lemma", "Proposition", "Corollary"}
    derived = [r for r in records if r["kind"] in result_kinds]
    supports = [r for r in records if r["kind"] in support_kinds]
    lemmas = [r for r in records if r["kind"] in {"Lemma", "Proposition", "Corollary"}]

    edges = []

    def add_edge(src, dst, relation, weight, evidence):
        if src == dst:
            return
        edges.append(
            {
                "source_id": src,
                "target_id": dst,
                "source_kind": by_id[src]["kind"],
                "target_kind": by_id[dst]["kind"],
                "relation": relation,
                "weight": weight,
                "evidence": evidence,
            }
        )

    explicit_ref = re.compile(r"\b(A\d+|P\d+|AS\d+|I\d+|PR\d+|LAW\d+|D\d+|T\d+|L\d+|PROP\d+|C\d+|HH-A\d+)\b")
    for record in records:
        refs = set(explicit_ref.findall(f"{record['label']} {record['statement']}"))
        for ref in refs:
            if ref in by_id:
                add_edge(ref, record["id"], "explicit_reference", 3, f"mentions {ref}")

    for target in derived:
        target_tokens = token_cache[target["id"]]
        scored = []
        for source in supports:
            source_tokens = token_cache[source["id"]]
            if not source_tokens or not target_tokens:
                continue
            overlap = target_tokens & source_tokens
            if not overlap:
                continue
            score = len(overlap) / max(6, min(len(source_tokens), len(target_tokens)))
            if score >= 0.16:
                scored.append((score, source, overlap))
        scored.sort(key=lambda x: x[0], reverse=True)
        for score, source, overlap in scored[:5]:
            weight = 2 if score >= 0.34 else 1
            add_edge(
                source["id"],
                target["id"],
                "semantic_overlap",
                weight,
                "tokens: " + ", ".join(sorted(overlap)[:8]),
            )

        for lemma in lemmas:
            if lemma["id"] == target["id"]:
                continue
            overlap = target_tokens & token_cache[lemma["id"]]
            if len(overlap) >= 3:
                add_edge(
                    lemma["id"],
                    target["id"],
                    "result_to_result_overlap",
                    1,
                    "tokens: " + ", ".join(sorted(overlap)[:8]),
                )

    unique = {}
    for edge in edges:
        key = (edge["source_id"], edge["target_id"], edge["relation"])
        if key not in unique or edge["weight"] > unique[key]["weight"]:
            unique[key] = edge
    return list(unique.values())


def write_outputs(records, edges, output_dir):
    output_dir.mkdir(parents=True, exist_ok=True)
    inventory_csv = output_dir / "statement_inventory.csv"
    edges_csv = output_dir / "dependency_edges.csv"
    binary_csv = output_dir / "dependency_matrix_binary.csv"
    weighted_csv = output_dir / "dependency_matrix_weighted.csv"
    graph_md = output_dir / "axiom_theorem_dependency_graph.md"
    graph_dot = output_dir / "axiom_theorem_dependency_graph.dot"
    summary_md = output_dir / "extraction_summary.md"

    fieldnames = ["id", "kind", "label", "statement", "source", "line", "extraction", "confidence"]
    with inventory_csv.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

    edge_fields = ["source_id", "target_id", "source_kind", "target_kind", "relation", "weight", "evidence"]
    with edges_csv.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=edge_fields)
        writer.writeheader()
        writer.writerows(edges)

    ids = [r["id"] for r in records]
    result_ids = [r["id"] for r in records if r["kind"] in {"Theorem", "Lemma", "Proposition", "Corollary"}]
    support_ids = [r["id"] for r in records if r["kind"] in {"Axiom", "Postulate", "Assumption", "Invariant", "Principle", "Law", "Definition"}]
    edge_lookup = {(e["source_id"], e["target_id"]): max(int(e["weight"]), 1) for e in edges}

    with binary_csv.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.writer(handle)
        writer.writerow(["source_id"] + result_ids)
        for src in support_ids:
            writer.writerow([src] + [1 if (src, dst) in edge_lookup else 0 for dst in result_ids])

    with weighted_csv.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.writer(handle)
        writer.writerow(["source_id"] + result_ids)
        for src in support_ids:
            writer.writerow([src] + [edge_lookup.get((src, dst), 0) for dst in result_ids])

    counts = defaultdict(int)
    for record in records:
        counts[record["kind"]] += 1

    connected_ids = {e["source_id"] for e in edges} | {e["target_id"] for e in edges}
    graph_records = [r for r in records if r["id"] in connected_ids]
    if len(graph_records) > 1200:
        edge_count = defaultdict(int)
        for edge in edges:
            edge_count[edge["source_id"]] += 1
            edge_count[edge["target_id"]] += 1
        top_ids = {node for node, _ in sorted(edge_count.items(), key=lambda item: item[1], reverse=True)[:1200]}
        graph_records = [r for r in records if r["id"] in top_ids]
        graph_edges = [e for e in edges if e["source_id"] in top_ids and e["target_id"] in top_ids]
    else:
        graph_edges = edges

    mermaid = ["```mermaid", "graph TD"]
    for record in graph_records:
        label = f"{record['id']}: {record['kind']}"
        if record["label"] and record["label"] != record["id"]:
            label += f" {record['label'][:40]}"
        mermaid.append(f"  {record['id'].replace('-', '_')}[{label}]")
    for edge in graph_edges:
        arrow = "-->" if int(edge["weight"]) >= 2 else "-.->"
        mermaid.append(f"  {edge['source_id'].replace('-', '_')} {arrow} {edge['target_id'].replace('-', '_')}")
    mermaid.append("```")

    graph_md.write_text(
        "# Granular Axiom-Theorem Dependency Graph\n\n"
        "Solid arrows are stronger inferred dependencies; dotted arrows are weaker/contextual dependencies.\n\n"
        f"Rendered graph subset: {len(graph_records)} connected/high-degree nodes, {len(graph_edges)} edges. Full edge list is in `dependency_edges.csv`.\n\n"
        + "\n".join(mermaid)
        + "\n",
        encoding="utf-8",
    )

    dot = ["digraph AxiomTheoremDependency {", "  rankdir=LR;", "  node [shape=box];"]
    for record in graph_records:
        label = f"{record['id']}\\n{record['kind']}\\n{record['label'][:45]}"
        dot.append(f'  "{record["id"]}" [label="{label}"];')
    for edge in graph_edges:
        style = "solid" if int(edge["weight"]) >= 2 else "dashed"
        dot.append(f'  "{edge["source_id"]}" -> "{edge["target_id"]}" [style={style}, label="{edge["relation"]}"];')
    dot.append("}")
    graph_dot.write_text("\n".join(dot), encoding="utf-8")

    summary_lines = [
        "# Axiom/Theorem Extraction Summary",
        "",
        f"- Statements extracted: **{len(records)}**",
        f"- Dependency edges: **{len(edges)}**",
        "",
        "## Counts By Kind",
        "",
    ]
    for kind in sorted(counts):
        summary_lines.append(f"- {kind}: {counts[kind]}")
    summary_lines.extend(
        [
            "",
            "## Files",
            "",
            f"- `statement_inventory.csv`",
            f"- `dependency_edges.csv`",
            f"- `dependency_matrix_binary.csv`",
            f"- `dependency_matrix_weighted.csv`",
            f"- `axiom_theorem_dependency_graph.md`",
            f"- `axiom_theorem_dependency_graph.dot`",
            "",
            "## Notes",
            "",
            "This extraction is intentionally auditable: use the source/line/confidence columns to confirm or reject candidates.",
            "Transcript-derived material is included, but confidence is reduced for chat/planning files.",
            "Equation-master rows are included as first-class Definition candidates unless their title/statement classifies them as an axiom, theorem, lemma, proposition, etc.",
            f"The Markdown/DOT graph files intentionally render a subset when the full graph is too large; the CSV edge and matrix files remain complete.",
        ]
    )
    summary_md.write_text("\n".join(summary_lines), encoding="utf-8")

    return {
        "inventory": inventory_csv,
        "edges": edges_csv,
        "binary": binary_csv,
        "weighted": weighted_csv,
        "graph_md": graph_md,
        "graph_dot": graph_dot,
        "summary": summary_md,
    }


def main():
    parser = argparse.ArgumentParser(description="Extract axioms/definitions/theorems/lemmas and build dependency graphs.")
    parser.add_argument("--root", action="append", default=[], help="File or directory root to scan. Can be repeated.")
    parser.add_argument("--csv", action="append", default=[], help="Equation master CSV to include. Can be repeated.")
    parser.add_argument("--output-dir", default="axiom_theorem_extraction")
    parser.add_argument("--min-confidence", type=float, default=0.20)
    args = parser.parse_args()

    roots = args.root or DEFAULT_ROOTS
    records = []
    for path in iter_text_files(roots):
        text = read_file(path)
        records.extend(extract_from_text(path, text))
    for csv_path in args.csv or DEFAULT_CSVS:
        records.extend(extract_from_equation_master(csv_path))

    records = [r for r in dedupe_records(records) if r["confidence"] >= args.min_confidence]
    records = assign_ids(records)
    edges = build_dependencies(records)
    outputs = write_outputs(records, edges, Path(args.output_dir))

    print(f"Scanned roots: {len(roots)}")
    print(f"Statements extracted: {len(records)}")
    print(f"Dependency edges: {len(edges)}")
    for name, path in outputs.items():
        print(f"{name}: {path}")


if __name__ == "__main__":
    main()
