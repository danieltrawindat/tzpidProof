# TZPID Proof Ladder Sledgehammer Report

Generated UTC: 2026-06-10T14:56:01+00:00
Updated UTC: 2026-06-10
Creator: Daniel Alexander Trawin
ORCID: https://orcid.org/0009-0001-4630-3715
DOI: https://doi.org/10.5281/zenodo.20632000

## Inputs

- Materialized edge list: `D:/TZPIDProof/graph_topology/materialized_edges.csv`
- Graph topology report: `D:/TZPIDProof/graph_topology/GRAPH_TOPOLOGY_REPORT.md`
- Isabelle theory: `D:/TZPIDProof/sledgehammer/TZPID_Proof_Ladder_Sledgehammer.thy`
- Reassembled derivation-order ladder: `D:/TZPIDProof/TZPID_ALL_IDS_REASSEMBLED_PROOF_LADDER.md`

## Derivation-Order Authority

The reorganized proof ladder is the registry-wide derivation order for the TZPID proof package. It reorders all `10271` canonical entries into a topological sequence: every materialized dependency points from an earlier prerequisite rung to a later dependent rung. The Sledgehammer harness therefore establishes the global ordering condition used by the publication package: the reassembled list is not merely a display order, but the dependency-respecting derivation order against which downstream proof, certificate, and peer-review artifacts are indexed.

The graph layer distinguishes three related counts:

- `753` concrete materialized rung-to-rung dependency edges. These are the edge cases encoded in Isabelle and checked here.
- `754` numeric table tokens when the single parenthetical summary marker `(+1)` is counted as a number. That marker is documentation, not a concrete edge.
- `763` prose-level dependency edges before cycle handling. Of these, `9` cycle-partner edges were cut to linearize the ladder while retaining them for refinement/audit.

Thus, the formal derivation-order claim certified by this report is: all `753` concrete materialized edge cases respect the upward-rung invariant in the reorganized ladder.

## What Was Checked

The corrected generated Isabelle theory checks the structural proof-ladder invariant:

```isabelle
edge_points_upward e == fst e < snd e
list_all edge_points_upward explicit_ladder_edges
```

This means every materialized dependency rung is strictly above the rung that depends on it. Parenthetical summary markers such as `(+1)` are not encoded as concrete rung-to-rung edges.

## Counts

- Ladder rows: `10271`
- Materialized dependency edges checked: `753`
- Prose dependency edges before cycle handling: `763`
- Cut cycle edges retained for audit: `9`
- Non-isolated nodes touched by at least one edge: `811`
- Isolated nodes with 0 incoming and 0 outgoing edges: `9460`
- Connected components total: `9598`
- Nontrivial connected clusters: `138`
- Largest connected cluster: `330` nodes / `385` edges
- Maximum dependency depth: `21` edges / `22` sequential layers
- Build exit code: `0`

## Sledgehammer Scope

The theory includes a Sledgehammer call on the generic edge-introduction lemma, then Isabelle checks the full generated edge list:

```isabelle
lemma edge_points_upward_intro:
  assumes "dep < rung"
  shows "edge_points_upward (dep, rung)"
  sledgehammer [timeout = 10]
  using assms unfolding edge_points_upward_def by simp
```

## Result

`PASS`: Isabelle accepted the corrected Sledgehammer harness and proved that every materialized dependency edge in the reassembled ladder points upward in derivation order.

## Pertinent Audit Artifacts

- `D:/TZPIDProof/graph_topology/materialized_edges.csv` — the 753 concrete dependency edge cases checked by Isabelle.
- `D:/TZPIDProof/graph_topology/connected_components.csv` — connected-component topology for the full registry graph.
- `D:/TZPIDProof/graph_topology/top_prerequisite_supernodes.csv` — entries with the largest number of direct dependents.
- `D:/TZPIDProof/graph_topology/top_dependent_nodes.csv` — entries with the largest number of direct prerequisites.
- `D:/TZPIDProof/graph_topology/cut_edge_transitive_audit.csv` — the 9 cycle-cut edges retained for refinement.
- `D:/TZPIDProof/graph_topology/dependency_heatmap_nonisolated.svg` and `.png` — visual graph of the non-isolated dependency structure.

## Citation

Daniel Alexander Trawin, *TZPID Reassembled Proof Ladder and Sledgehammer Derivation-Order Certificate*, TZPIDProof archive, 2026. DOI: [10.5281/zenodo.20632000](https://doi.org/10.5281/zenodo.20632000).
