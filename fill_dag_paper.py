from __future__ import annotations

import csv
import json
import re
from collections import Counter, defaultdict, deque
from pathlib import Path


ROOT = Path(__file__).resolve().parent
EDGE_CSV = ROOT / "graph_topology" / "materialized_edges.csv"
TOPOLOGY_REPORT = ROOT / "graph_topology" / "GRAPH_TOPOLOGY_REPORT.md"
LADDER_MD = ROOT / "TZPID_ALL_IDS_REASSEMBLED_PROOF_LADDER.md"
TEMPLATE_TEX = ROOT / "peer_review" / "tex" / "paper10_dag_breakthrough.tex.tpl"
GENERATED_TEX = ROOT / "peer_review" / "tex" / "paper10_dag_breakthrough.generated.tex"
GENERATED_THY = ROOT / "tzpid_proof" / "isabelle_tzpid" / "TZPID_DerivationOrder.thy"
METRICS_JSON = ROOT / "graph_topology" / "dag_paper_metrics.json"
TOPOLOGY_SUMMARY_JSON = ROOT / "graph_topology" / "graph_topology_summary.json"


def read_edges() -> list[tuple[int, str, int, str]]:
    with EDGE_CSV.open(newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    return [
        (
            int(row["dep_rung"]),
            row["dep_id"],
            int(row["dependent_rung"]),
            row["dependent_id"],
        )
        for row in rows
    ]


def read_ladder_rows() -> dict[int, dict[str, str]]:
    rows: dict[int, dict[str, str]] = {}
    pattern = re.compile(r"^\|\s*(\d+)\s*\|\s*(ID\d+)\s*\|\s*(.*?)\s*\|")
    for line in LADDER_MD.read_text(encoding="utf-8").splitlines():
        match = pattern.match(line)
        if not match:
            continue
        rung = int(match.group(1))
        rows[rung] = {"id": match.group(2), "title": match.group(3).strip()}
    return rows


def read_report_metric(label: str) -> int | None:
    text = TOPOLOGY_REPORT.read_text(encoding="utf-8")
    match = re.search(rf"{re.escape(label)}:\s*`?([0-9,]+)", text)
    if not match:
        return None
    return int(match.group(1).replace(",", ""))


def longest_path_and_depths(nodes: set[int], edges: list[tuple[int, int]]):
    out: dict[int, list[int]] = defaultdict(list)
    indeg = Counter({n: 0 for n in nodes})
    for a, b in edges:
        out[a].append(b)
        indeg[b] += 1

    q = deque(sorted(n for n in nodes if indeg[n] == 0))
    topo: list[int] = []
    indeg_work = indeg.copy()
    while q:
        n = q.popleft()
        topo.append(n)
        for m in sorted(out[n]):
            indeg_work[m] -= 1
            if indeg_work[m] == 0:
                q.append(m)

    if len(topo) != len(nodes):
        raise RuntimeError("Materialized graph is cyclic or missing nodes in topological pass.")

    depth = {n: 0 for n in nodes}
    parent: dict[int, int | None] = {n: None for n in nodes}
    for n in topo:
        for m in out[n]:
            if depth[n] + 1 > depth[m]:
                depth[m] = depth[n] + 1
                parent[m] = n

    end = max(nodes, key=lambda n: depth[n])
    chain = []
    cur: int | None = end
    while cur is not None:
        chain.append(cur)
        cur = parent[cur]
    chain.reverse()
    return chain, depth


def latex_escape(text: str) -> str:
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    return "".join(replacements.get(ch, ch) for ch in text)


def table_rows_for_degree_csv(path: Path, degree_col: str, limit: int = 7) -> str:
    with path.open(newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))[:limit]
    return "\n".join(
        f"{row['rung']} & {latex_escape(row['id'])} & {row[degree_col]} & {latex_escape(row['title'])} \\\\"
        for row in rows
    )


def build_metrics() -> dict[str, object]:
    ladder = read_ladder_rows()
    edge_rows = read_edges()
    edges = [(a, b) for a, _, b, _ in edge_rows]
    edge_nodes = {n for edge in edges for n in edge}
    all_nodes = set(ladder)
    chain, depth = longest_path_and_depths(all_nodes, edges)

    depth_hist = Counter(depth.values())
    total_nodes = len(ladder)
    isolated = sum(1 for n in all_nodes if n not in edge_nodes)
    summary = {}
    if TOPOLOGY_SUMMARY_JSON.exists():
        summary = json.loads(TOPOLOGY_SUMMARY_JSON.read_text(encoding="utf-8"))

    return {
        "TOTAL_NODES": total_nodes,
        "EDGE_COUNT": len(edge_rows),
        "NUMERIC_TOKEN_COUNT": len(edge_rows),
        "PROSE_EDGE_COUNT": len(edge_rows) + int(summary.get("cut_edges", 0)),
        "CUT_EDGE_COUNT": int(summary.get("cut_edges", 0)),
        "ISOLATED_COUNT": isolated,
        "NONISOLATED_COUNT": len(edge_nodes),
        "COMPONENT_COUNT": summary.get("connected_components_total") or read_report_metric("Connected components total") or "",
        "NONTRIVIAL_COMPONENTS": summary.get("nontrivial_connected_clusters") or read_report_metric("Nontrivial connected clusters") or "",
        "LARGEST_COMPONENT_NODES": summary.get("largest_component_nodes", ""),
        "LARGEST_COMPONENT_EDGES": summary.get("largest_component_edges", ""),
        "MAX_DEPTH_EDGES": max(depth.values()),
        "MAX_DEPTH_NODES": max(depth.values()) + 1,
        "DEPTH_HISTOGRAM_ROWS": "\n".join(
            f"{layer} & {depth_hist[layer]} \\\\" for layer in sorted(depth_hist)
        ),
        "LONGEST_CHAIN_ROWS": "\n".join(
            f"{i} & {depth[rung]} & {rung} & {latex_escape(ladder[rung]['id'])} & {latex_escape(ladder[rung]['title'])} \\\\"
            for i, rung in enumerate(chain, 1)
        ),
        "TOP_PREREQ_ROWS": table_rows_for_degree_csv(
            ROOT / "graph_topology" / "top_prerequisite_supernodes.csv", "out_degree"
        ),
        "TOP_DEPENDENT_ROWS": table_rows_for_degree_csv(
            ROOT / "graph_topology" / "top_dependent_nodes.csv", "in_degree"
        ),
    }


def render_template(metrics: dict[str, object]) -> str:
    text = TEMPLATE_TEX.read_text(encoding="utf-8")
    for key, value in metrics.items():
        text = text.replace("{{" + key + "}}", str(value))
    return text


def write_isabelle_theory() -> None:
    edge_pairs = [(a, b) for a, _, b, _ in read_edges()]
    chunks = []
    for i in range(0, len(edge_pairs), 6):
        parts = [f"({a}, {b})" for a, b in edge_pairs[i : i + 6]]
        prefix = "    " if i == 0 else "    "
        chunks.append(prefix + ", ".join(parts))
    edge_list = ",\n".join(chunks)
    theory = f'''theory TZPID_DerivationOrder
  imports Main
begin

text \\<open>
  Generated from the materialized dependency edge CSV.
  The edge (d, r) means rung r depends on prerequisite rung d.
  DOI: 10.5281/zenodo.20632000
\\<close>

definition rung_before :: "nat => nat => bool"
  where "rung_before d r \\<longleftrightarrow> d < r"

definition edge_points_upward :: "(nat * nat) => bool"
  where "edge_points_upward e \\<longleftrightarrow> rung_before (fst e) (snd e)"

definition explicit_ladder_edges :: "(nat * nat) list"
  where "explicit_ladder_edges = [
{edge_list}
  ]"

lemma derivation_order_strictly_upward:
  "list_all edge_points_upward explicit_ladder_edges"
  by eval

lemma derivation_order_no_self_edges:
  "list_all (\\<lambda>e. fst e \\<noteq> snd e) explicit_ladder_edges"
  by eval

end
'''
    GENERATED_THY.write_text(theory, encoding="utf-8")


def main() -> None:
    metrics = build_metrics()
    METRICS_JSON.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    GENERATED_TEX.write_text(render_template(metrics), encoding="utf-8")
    write_isabelle_theory()
    print(f"Wrote {GENERATED_TEX}")
    print(f"Wrote {GENERATED_THY}")
    print(f"Wrote {METRICS_JSON}")


if __name__ == "__main__":
    main()
