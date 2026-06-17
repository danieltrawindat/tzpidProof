import csv
import json
import re
from collections import Counter, defaultdict, deque
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\TZPIDProof")
MASTER = ROOT / "TZPID_ALL_IDS_CANONICAL_EQUATION_MASTER_with_export.csv"
LADDER = ROOT / "TZPID_ALL_IDS_REASSEMBLED_PROOF_LADDER.md"
OUT = ROOT / "graph_topology"

ID_RE = re.compile(r"\bID\s*0*(\d{1,5})\b", re.I)


def normalize_id(num):
    return f"ID{int(num):04d}"


def split_md_row(line):
    body = line.strip()
    if not body.startswith("|") or not body.endswith("|"):
        return []
    body = body[1:-1]
    parts = []
    cur = []
    escaped = False
    for ch in body:
        if ch == "\\" and not escaped:
            escaped = True
            cur.append(ch)
            continue
        if ch == "|" and not escaped:
            parts.append("".join(cur).strip())
            cur = []
            continue
        escaped = False
        cur.append(ch)
    parts.append("".join(cur).strip())
    return parts


def read_ladder():
    rows = {}
    order = []
    for line in LADDER.read_text(encoding="utf-8", errors="replace").splitlines():
        if not re.match(r"^\|\s*\d+\s*\|\s*ID\d{4,5}\s*\|", line):
            continue
        parts = split_md_row(line)
        if len(parts) < 6:
            continue
        rung = int(parts[0])
        tzpid = parts[1]
        rows[tzpid] = {
            "rung": rung,
            "id": tzpid,
            "title": parts[2],
            "kind": parts[3],
            "gold_spine": parts[4],
            "rests_on": parts[5],
        }
        order.append(tzpid)
    return rows, order


def read_master():
    with MASTER.open(encoding="utf-8-sig", newline="") as handle:
        return {row["id"]: row for row in csv.DictReader(handle)}


def ids_in_text(text):
    if not text:
        return set()
    return {normalize_id(match.group(1)) for match in ID_RE.finditer(text)}


def rests_on_rungs(value):
    if not value or value == "—":
        return []
    return [int(x) for x in re.findall(r"\d+", value)]


def add_edge(edges, cuts, source, target, reason, ladder_rows, rung_to_id):
    if source == target:
        return
    if source < target:
        dep_id = rung_to_id[source]
        target_id = rung_to_id[target]
        edges[(source, target)].add(reason)
    else:
        cuts.append(
            {
                "dep_rung": source,
                "dep_id": rung_to_id.get(source, ""),
                "dependent_rung": target,
                "dependent_id": rung_to_id.get(target, ""),
                "reason": reason,
                "cut_reason": "reference points downward_or_sideways_in_current_ladder",
            }
        )


def build_edges(ladder_rows, order, master):
    id_to_rung = {tzpid: row["rung"] for tzpid, row in ladder_rows.items()}
    rung_to_id = {row["rung"]: tzpid for tzpid, row in ladder_rows.items()}
    edges = defaultdict(set)
    cuts = []

    for tzpid in order:
        row = ladder_rows[tzpid]
        target = row["rung"]
        for dep in rests_on_rungs(row.get("rests_on", "")):
            if dep in rung_to_id:
                add_edge(edges, cuts, dep, target, "ladder_rests_on", ladder_rows, rung_to_id)

        master_row = master.get(tzpid, {})
        text = " ".join(
            str(master_row.get(field, ""))
            for field in [
                "canonical_statement",
                "canonical_equation",
                "formation_note",
                "dictionary",
                "encyclopedia",
                "proof_required_checks",
            ]
        )
        for ref_id in sorted(ids_in_text(text)):
            if ref_id == tzpid or ref_id not in id_to_rung:
                continue
            add_edge(edges, cuts, id_to_rung[ref_id], target, "explicit_id_reference", ladder_rows, rung_to_id)

    spine_groups = defaultdict(list)
    for tzpid in order:
        spine = (master.get(tzpid, {}).get("gold_spine") or ladder_rows[tzpid].get("gold_spine") or "").strip()
        if spine:
            spine_groups[spine].append(tzpid)
    for spine, ids in spine_groups.items():
        ids = sorted(ids, key=lambda x: id_to_rung[x])
        for a, b in zip(ids, ids[1:]):
            add_edge(edges, cuts, id_to_rung[a], id_to_rung[b], f"gold_spine_sequence:{spine}", ladder_rows, rung_to_id)

    return edges, cuts


def graph_metrics(node_count, edges):
    nodes = set(range(1, node_count + 1))
    undirected = defaultdict(set)
    out = defaultdict(set)
    indeg = Counter({n: 0 for n in nodes})
    outdeg = Counter({n: 0 for n in nodes})
    for a, b in edges:
        undirected[a].add(b)
        undirected[b].add(a)
        out[a].add(b)
        indeg[b] += 1
        outdeg[a] += 1

    seen = set()
    components = []
    for node in sorted(nodes):
        if node in seen:
            continue
        stack = [node]
        seen.add(node)
        comp = []
        edge_count = 0
        while stack:
            cur = stack.pop()
            comp.append(cur)
            edge_count += len(undirected[cur])
            for nxt in undirected[cur]:
                if nxt not in seen:
                    seen.add(nxt)
                    stack.append(nxt)
        components.append((sorted(comp), edge_count // 2))

    q = deque(sorted(n for n in nodes if indeg[n] == 0))
    topo = []
    indeg_work = indeg.copy()
    while q:
        n = q.popleft()
        topo.append(n)
        for m in sorted(out[n]):
            indeg_work[m] -= 1
            if indeg_work[m] == 0:
                q.append(m)
    cyclic = len(topo) != len(nodes)

    depth = {n: 0 for n in nodes}
    parent = {n: None for n in nodes}
    if not cyclic:
        for n in topo:
            for m in out[n]:
                if depth[n] + 1 > depth[m]:
                    depth[m] = depth[n] + 1
                    parent[m] = n
    end = max(nodes, key=lambda n: depth[n])
    chain = []
    cur = end
    while cur is not None:
        chain.append(cur)
        cur = parent[cur]
    chain.reverse()

    return {
        "indeg": indeg,
        "outdeg": outdeg,
        "components": components,
        "cyclic": cyclic,
        "depth": depth,
        "chain": chain,
    }


def write_csv(path, fields, rows):
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    generated = datetime.now(timezone.utc).isoformat()
    ladder_rows, order = read_ladder()
    master = read_master()
    rung_to_id = {row["rung"]: tzpid for tzpid, row in ladder_rows.items()}
    edges, cuts = build_edges(ladder_rows, order, master)
    edge_rows = []
    for (a, b), reasons in sorted(edges.items()):
        edge_rows.append(
            {
                "dep_rung": a,
                "dep_id": rung_to_id[a],
                "dependent_rung": b,
                "dependent_id": rung_to_id[b],
                "reason": ";".join(sorted(reasons)),
            }
        )
    write_csv(OUT / "materialized_edges.csv", ["dep_rung", "dep_id", "dependent_rung", "dependent_id", "reason"], edge_rows)
    write_csv(
        OUT / "cut_edge_transitive_audit.csv",
        ["dep_rung", "dep_id", "dependent_rung", "dependent_id", "reason", "cut_reason"],
        cuts,
    )

    metrics = graph_metrics(len(order), [(row["dep_rung"], row["dependent_rung"]) for row in edge_rows])
    indeg = metrics["indeg"]
    outdeg = metrics["outdeg"]
    edge_nodes = {n for row in edge_rows for n in (row["dep_rung"], row["dependent_rung"])}
    components = metrics["components"]
    nontrivial = [(c, e) for c, e in components if len(c) > 1]
    largest = max(nontrivial, key=lambda ce: (len(ce[0]), ce[1]), default=([], 0))

    comp_rows = []
    for idx, (comp, ecount) in enumerate(sorted(components, key=lambda ce: (-len(ce[0]), ce[0][0])), start=1):
        sample = "; ".join(rung_to_id[n] for n in comp[:12])
        comp_rows.append(
            {
                "component": idx,
                "nodes": len(comp),
                "edges": ecount,
                "rung_min": min(comp),
                "rung_max": max(comp),
                "sample_ids": sample,
            }
        )
    write_csv(OUT / "connected_components.csv", ["component", "nodes", "edges", "rung_min", "rung_max", "sample_ids"], comp_rows)

    top_prereq = sorted(edge_nodes, key=lambda n: (-outdeg[n], n))[:50]
    write_csv(
        OUT / "top_prerequisite_supernodes.csv",
        ["rung", "id", "out_degree", "title"],
        [{"rung": n, "id": rung_to_id[n], "out_degree": outdeg[n], "title": ladder_rows[rung_to_id[n]]["title"]} for n in top_prereq],
    )
    top_dep = sorted(edge_nodes, key=lambda n: (-indeg[n], n))[:50]
    write_csv(
        OUT / "top_dependent_nodes.csv",
        ["rung", "id", "in_degree", "title"],
        [{"rung": n, "id": rung_to_id[n], "in_degree": indeg[n], "title": ladder_rows[rung_to_id[n]]["title"]} for n in top_dep],
    )

    depth_hist = Counter(metrics["depth"].values())
    write_csv(
        OUT / "depth_layers.csv",
        ["depth", "node_count"],
        [{"depth": depth, "node_count": depth_hist[depth]} for depth in sorted(depth_hist)],
    )

    dot_lines = ["digraph TZPID {", "  rankdir=LR;"]
    for row in edge_rows:
        dot_lines.append(f'  "{row["dep_id"]}" -> "{row["dependent_id"]}";')
    dot_lines.append("}")
    (OUT / "dependency_heatmap_nonisolated.dot").write_text("\n".join(dot_lines) + "\n", encoding="utf-8")

    chain_rows = [
        {
            "position": i,
            "rung": rung,
            "id": rung_to_id[rung],
            "depth": metrics["depth"][rung],
            "title": ladder_rows[rung_to_id[rung]]["title"],
        }
        for i, rung in enumerate(metrics["chain"], start=1)
    ]
    write_csv(OUT / "critical_path.csv", ["position", "rung", "id", "depth", "title"], chain_rows)

    summary = {
        "generated_utc": generated,
        "total_ladder_nodes": len(order),
        "materialized_edges": len(edge_rows),
        "cut_edges": len(cuts),
        "isolated_nodes": len([n for n in range(1, len(order) + 1) if n not in edge_nodes]),
        "nonisolated_nodes": len(edge_nodes),
        "connected_components_total": len(components),
        "nontrivial_connected_clusters": len(nontrivial),
        "largest_component_nodes": len(largest[0]),
        "largest_component_edges": largest[1],
        "max_dependency_depth_edges": max(metrics["depth"].values()),
        "max_dependency_depth_nodes": max(metrics["depth"].values()) + 1,
        "cyclic": metrics["cyclic"],
    }
    (OUT / "graph_topology_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    md = [
        "# TZPID Proof Ladder Graph Topology Report",
        "",
        f"Generated UTC: {generated}",
        "",
        "## Executive Summary",
        "",
        f"- Total ladder nodes: `{summary['total_ladder_nodes']}`",
        f"- Materialized rung-to-rung dependency edges: `{summary['materialized_edges']}`",
        f"- Cut/downward references retained for audit: `{summary['cut_edges']}`",
        f"- Isolated nodes with 0 incoming and 0 outgoing edges: `{summary['isolated_nodes']}`",
        f"- Non-isolated nodes touched by at least one edge: `{summary['nonisolated_nodes']}`",
        f"- Connected components total: `{summary['connected_components_total']}`",
        f"- Nontrivial connected clusters: `{summary['nontrivial_connected_clusters']}`",
        f"- Largest connected cluster: `{summary['largest_component_nodes']}` nodes / `{summary['largest_component_edges']}` edges",
        f"- Maximum dependency depth: `{summary['max_dependency_depth_edges']}` edges, so `{summary['max_dependency_depth_nodes']}` sequential layers are sufficient with unlimited parallel workers.",
        f"- DAG cyclicity check: `{'cyclic' if summary['cyclic'] else 'acyclic'}`",
        "",
        "## Method",
        "",
        "Edges were rebuilt from the synced derivation ladder by combining preserved `Rests on` rung references, explicit `ID####` mentions in master text fields, and ordered nonempty gold-spine chains. References that point downward or sideways in the current ladder are retained in `cut_edge_transitive_audit.csv` rather than materialized.",
        "",
        "## Top Prerequisite Super-Nodes",
        "",
        "| Rung | ID | Direct Dependents | Title |",
        "|---:|---|---:|---|",
    ]
    for n in top_prereq[:20]:
        md.append(f"| {n} | {rung_to_id[n]} | {outdeg[n]} | {ladder_rows[rung_to_id[n]]['title']} |")
    md += ["", "## Top Dependent Nodes", "", "| Rung | ID | Direct Prerequisites | Title |", "|---:|---|---:|---|"]
    for n in top_dep[:20]:
        md.append(f"| {n} | {rung_to_id[n]} | {indeg[n]} | {ladder_rows[rung_to_id[n]]['title']} |")
    (OUT / "GRAPH_TOPOLOGY_REPORT.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
