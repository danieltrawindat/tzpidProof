import argparse
import csv
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GRAPH_DIR = ROOT / "graph_topology"
EDGES_CSV = GRAPH_DIR / "materialized_edges.csv"
SUMMARY_JSON = GRAPH_DIR / "python_graph_layer_summary.json"
HEATMAP_PNG = GRAPH_DIR / "dependency_heatmap_nonisolated.png"
HEATMAP_SVG = GRAPH_DIR / "dependency_heatmap_nonisolated.svg"
VISUAL_MD = GRAPH_DIR / "GRAPH_VISUAL_LAYER.md"


def read_edges(path=EDGES_CSV):
    with path.open(encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            yield {
                "dep_rung": int(row["dep_rung"]),
                "dep_id": row["dep_id"],
                "dependent_rung": int(row["dependent_rung"]),
                "dependent_id": row["dependent_id"],
                "reason": row.get("reason", ""),
            }


def compute_networkx_metrics(edges):
    import networkx as nx

    graph = nx.DiGraph()
    for edge in edges:
        graph.add_edge(
            edge["dep_rung"],
            edge["dependent_rung"],
            dep_id=edge["dep_id"],
            dependent_id=edge["dependent_id"],
            reason=edge["reason"],
        )

    weak_components = list(nx.weakly_connected_components(graph))
    top_prereq = sorted(graph.out_degree(), key=lambda x: x[1], reverse=True)[:20]
    top_dependents = sorted(graph.in_degree(), key=lambda x: x[1], reverse=True)[:20]
    cyclic = not nx.is_directed_acyclic_graph(graph)
    if cyclic:
        longest_path = []
        longest_path_length = None
    else:
        longest_path = nx.dag_longest_path(graph)
        longest_path_length = nx.dag_longest_path_length(graph)

    return {
        "node_count_nonisolated": graph.number_of_nodes(),
        "edge_count": graph.number_of_edges(),
        "weak_component_count": len(weak_components),
        "nontrivial_component_count": sum(1 for c in weak_components if len(c) > 1),
        "largest_component_nodes": max((len(c) for c in weak_components), default=0),
        "cyclic": cyclic,
        "longest_path_edges": longest_path_length,
        "longest_path_nodes": len(longest_path),
        "longest_path": longest_path,
        "top_prerequisite_rungs": [{"rung": n, "out_degree": d} for n, d in top_prereq],
        "top_dependent_rungs": [{"rung": n, "in_degree": d} for n, d in top_dependents],
    }


def render_heatmap(edges):
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.colors import LogNorm

    xs = [edge["dep_rung"] for edge in edges]
    ys = [edge["dependent_rung"] for edge in edges]
    max_rung = max(xs + ys) if xs or ys else 1

    fig, ax = plt.subplots(figsize=(14, 10), dpi=160)
    hist = ax.hist2d(xs, ys, bins=120, norm=LogNorm(), cmap="magma")
    fig.colorbar(hist[3], ax=ax, label="edge density (log scale)")
    ax.plot([0, max_rung], [0, max_rung], color="white", linewidth=0.8, alpha=0.45, linestyle="--")
    ax.set_title("TZPID Derivation Dependency Heatmap\nMaterialized non-isolated edges")
    ax.set_xlabel("Prerequisite rung")
    ax.set_ylabel("Dependent rung")
    ax.grid(alpha=0.12)
    fig.tight_layout()
    fig.savefig(HEATMAP_PNG)
    fig.savefig(HEATMAP_SVG)
    plt.close(fig)


def write_visual_markdown(summary):
    depth_counter = Counter(summary.get("longest_path", []))
    lines = [
        "# TZPID Graph Visual Layer",
        "",
        f"Generated UTC: {summary['generated_utc']}",
        "",
        "This layer is the reusable Python renderer and metric checker for the derivation-order graph. It consumes `materialized_edges.csv`, verifies the directed graph with NetworkX, and renders the dependency heatmap as PNG/SVG.",
        "",
        "## Current Metrics",
        "",
        "| Metric | Value |",
        "|---|---:|",
        f"| Non-isolated graph nodes | {summary['node_count_nonisolated']} |",
        f"| Materialized edges | {summary['edge_count']} |",
        f"| Weak connected components | {summary['weak_component_count']} |",
        f"| Nontrivial components | {summary['nontrivial_component_count']} |",
        f"| Largest component nodes | {summary['largest_component_nodes']} |",
        f"| Cyclic | {str(summary['cyclic']).lower()} |",
        f"| Longest path depth | {summary['longest_path_edges']} edges / {summary['longest_path_nodes']} nodes |",
        "",
        "## Visual Outputs",
        "",
        "- `dependency_heatmap_nonisolated.png`",
        "- `dependency_heatmap_nonisolated.svg`",
        "",
        "![Dependency heatmap](dependency_heatmap_nonisolated.png)",
        "",
        "## Reproduce",
        "",
        "```powershell",
        "python D:\\TZPIDProof\\graph_topology\\tzpid_graph_layer.py --render",
        "```",
        "",
        "## Notes",
        "",
        "The heatmap is a density visualization, not a proof by itself. The formal derivation-order proof remains in `tzpid_proof/isabelle_tzpid/TZPID_DerivationOrder.thy`.",
    ]
    VISUAL_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--render", action="store_true", help="render PNG/SVG heatmap")
    args = parser.parse_args()

    edges = list(read_edges())
    metrics = compute_networkx_metrics(edges)
    summary = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "input_edges_csv": str(EDGES_CSV),
        **metrics,
        "outputs": {
            "summary_json": str(SUMMARY_JSON),
            "heatmap_png": str(HEATMAP_PNG),
            "heatmap_svg": str(HEATMAP_SVG),
            "visual_markdown": str(VISUAL_MD),
        },
    }

    if args.render:
        render_heatmap(edges)

    SUMMARY_JSON.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    write_visual_markdown(summary)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
