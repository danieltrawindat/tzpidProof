# TZPIDProof Repo Snapshot Readiness Report

Generated: 2026-06-11

## Refresh Run

The proof package audit artifacts were refreshed for the GitHub repository snapshot.

## Graph Topology And Heatmap

Command:

```powershell
python D:\TZPIDProof\rebuild_graph_topology_from_synced_ladder.py
```

Current graph summary:

| Metric | Value |
|---|---:|
| Total ladder nodes | 10,357 |
| Materialized dependency edges | 2,080 |
| Cut/downward audit edges | 71 |
| Isolated nodes | 8,387 |
| Non-isolated nodes | 1,970 |
| Connected components | 8,618 |
| Nontrivial connected clusters | 231 |
| Largest connected cluster | 1,046 nodes / 1,363 edges |
| Maximum dependency depth | 67 edges / 68 sequential layers |
| Cyclicity | acyclic |

Primary outputs:

- `graph_topology/GRAPH_TOPOLOGY_REPORT.md`
- `graph_topology/graph_topology_summary.json`
- `graph_topology/materialized_edges.csv`
- `graph_topology/connected_components.csv`
- `graph_topology/critical_path.csv`
- `graph_topology/depth_layers.csv`
- `graph_topology/cut_edge_transitive_audit.csv`
- `graph_topology/dependency_heatmap_nonisolated.dot`
- `graph_topology/dependency_heatmap_nonisolated.png`
- `graph_topology/dependency_heatmap_nonisolated.svg`
- `graph_topology/dependency_heatmap_render_summary.json`
- `graph_topology/tzpid_graph_layer.py`
- `graph_topology/GRAPH_VISUAL_LAYER.md`
- `graph_topology/python_graph_layer_summary.json`

Graphviz `dot` was not available on PATH, so the refreshed image heatmap was generated as a Matplotlib log-density heatmap from `materialized_edges.csv`.

Reusable Python graph-layer command:

```powershell
python D:\TZPIDProof\graph_topology\tzpid_graph_layer.py --render
```

## Edge-Case Equation Audit

Command:

```powershell
python D:\TZPIDProof\edge_case_equations\build_edge_case_equation_audit.py
```

Current edge-case summary:

| Metric | Value |
|---|---:|
| Master rows scanned | 10,862 |
| Operator-pass rows | 10,356 |
| Cleanup rows scanned | 1,936 |
| Math-rescue candidates | 1,298 |
| Cleanup shell/code artifacts | 21 |
| Cleanup low-priority rows | 617 |
| Master shell-artifact signals | 48 |

Primary outputs:

- `edge_case_equations/TZPID_EDGE_CASE_EQUATION_SHORTLIST.csv`
- `edge_case_equations/TZPID_EDGE_CASE_EQUATION_SHORTLIST.md`
- `edge_case_equations/TZPID_EQUATION_UNIVERSE_GAP_AUDIT.csv`
- `edge_case_equations/TZPID_EQUATION_UNIVERSE_GAP_AUDIT.md`
- `edge_case_equations/edge_case_equation_scoring.json`

## Shell-Artifact Signal Scrap / Quarantine

Command:

```powershell
python D:\TZPIDProof\edge_case_equations\scrap_shell_artifact_signals.py
```

Current proof-clean summary:

| Metric | Value |
|---|---:|
| Original master rows | 10,862 |
| Proof-clean master rows | 10,814 |
| Scrapped shell-artifact signal rows | 48 |
| Original edge-case shortlist rows | 10,862 |
| Proof-clean edge-case shortlist rows | 10,814 |

Primary outputs:

- `TZPID_ALL_IDS_CANONICAL_EQUATION_MASTER_PROOF_CLEAN_NO_SHELL_SIGNALS.csv`
- `edge_case_equations/TZPID_MASTER_SHELL_ARTIFACT_SIGNAL_QUARANTINE.csv`
- `edge_case_equations/TZPID_MASTER_SHELL_ARTIFACT_SIGNAL_QUARANTINE.md`
- `edge_case_equations/TZPID_EDGE_CASE_EQUATION_SHORTLIST_PROOF_CLEAN.csv`
- `edge_case_equations/TZPID_EDGE_CASE_EQUATION_SHORTLIST_PROOF_CLEAN.md`
- `edge_case_equations/shell_artifact_signal_scrap_report.json`

The original master remains intact as provenance. The proof-clean master is the recommended input for proof-facing claims that should exclude shell/code-like artifacts.

## ID-System Sync

Command:

```powershell
python D:\TZPIDProof\extend_tzpid_id_system.py
```

Current identity summary:

| Metric | Value |
|---|---:|
| Master rows | 10,862 |
| Previous ID-system rows | 10,857 |
| New ID-system rows | 10,862 |
| Added rows | 5 |

Added IDs:

- `ID11372`
- `ID11373`
- `ID11374`
- `ID11375`
- `ID11376`

Report:

- `TZPID_ID_SYSTEM_EXTENSION_REPORT.json`

## Edge-Case Strengthening Batch

Command:

```powershell
python D:\TZPIDProof\edge_case_equations\build_edge_case_strengthening_batch.py
```

Current strengthening summary:

| Metric | Value |
|---|---:|
| Curated strengthening rows | 20 |
| Wolfram checks | 20 |
| Wolfram passes | 20 |
| Wolfram failures | 0 |

Primary outputs:

- `edge_case_equations/TZPID_EDGE_CASE_STRENGTHENING_BATCH.csv`
- `edge_case_equations/TZPID_EDGE_CASE_STRENGTHENING_BATCH.md`
- `edge_case_equations/TZPID_SHELL_CODE_ARTIFACT_QUARANTINE.csv`
- `edge_case_equations/TZPID_SHELL_CODE_ARTIFACT_QUARANTINE.md`
- `edge_case_equations/wolfram/edge_case_strengthening_check.wls`
- `edge_case_equations/wolfram/edge_case_strengthening_results.json`
- `tzpid_proof/isabelle_tzpid/TZPID_EdgeCase_Strengthening.thy`

Wolfram command:

```powershell
C:\Program Files\Wolfram Research\WolframScript\wolframscript.exe -file D:\TZPIDProof\edge_case_equations\wolfram\edge_case_strengthening_check.wls
```

## Formal Build

Command:

```powershell
D:\Isabelle2025\Isabelle2025-2\bin\isabelle build -D D:\TZPIDProof\tzpid_proof\isabelle_tzpid
```

Result: passed.

## DAG Paper And Derivation-Order Theory

Command:

```powershell
python D:\TZPIDProof\fill_dag_paper.py
```

Primary outputs:

- `peer_review/tex/paper10_dag_breakthrough.generated.tex`
- `tzpid_proof/isabelle_tzpid/TZPID_DerivationOrder.thy`
- `graph_topology/dag_paper_metrics.json`

The generated DAG paper metrics match the refreshed topology:

| Metric | Value |
|---|---:|
| Nodes | 10,357 |
| Materialized edges | 2,080 |
| Prose edge count | 2,151 |
| Cut edge count | 71 |
| Maximum depth | 67 edges / 68 nodes |

The Isabelle session was rebuilt after regenerating `TZPID_DerivationOrder.thy`.

## Spartan Dawn Empirical Lane

Command:

```powershell
python D:\TZPIDProof\this_is_SPARTA\TZPID_spartan_dawn_fit.py
```

Primary outputs:

- `this_is_SPARTA/TZPID_spartan_dawn_fit.py`
- `this_is_SPARTA/spartan_fit.json`
- `this_is_SPARTA/TZPID_SPARTAN_DAWN_CMB_BAO_SNE_TEST.md`
- `this_is_SPARTA/SPARTAN_DAWN_CERTIFICATE.md`

Current compressed-data result:

| Model | chi^2 | params | AIC |
|---|---:|---:|---:|
| flat LCDM | 16.1294 | 2 | 20.1294 |
| closed LCDM | 14.4434 | 3 | 20.4434 |
| flat w0waCDM breathing | 7.5085 | 4 | 15.5085 |
| closed breathing | 7.0541 | 5 | 17.0541 |

Sound horizon check:

| Quantity | Computed | Reference |
|---|---:|---:|
| `r_s(z*)` | 144.485 Mpc | 144.39 Mpc |
| `r_s(drag)` | 147.128 Mpc | 147.09 Mpc |

Hubble-as-breathing check:

| Case | `H0` as breathing rate | `V_dot/V` |
|---|---:|---:|
| Planck-like `67.4 km/s/Mpc` | `0.0689/Gyr` | `0.2068/Gyr` |
| Local-like `73.50 km/s/Mpc` | `0.0752/Gyr` | `0.2255/Gyr` |
| Best closed-breathing fit | `0.0664/Gyr` | `0.1993/Gyr` |

Curvature radius:

| Case | Radius |
|---|---:|
| Best closed-breathing fit `Omega_K=-0.0046` | `222.9 Gly` |
| Reference `|Omega_K|=0.002`, `H0=67.4` | `324.4 Gly` |

Interpretation: the compressed CMB+BAO+SNe test supports the dynamic breathing term as empirically viable and better-fitting than flat LCDM in this simplified comparison. It does not force closed curvature, and it is not a full Boltzmann-code likelihood.

## Snapshot Opinion

The repository is looking strong as a proof package. The best signs are:

- the dependency graph is acyclic after refresh;
- the package now has a real connected topology rather than only isolated rows;
- the shell/code artifacts are explicitly quarantined instead of silently mixed into the equation universe;
- the edge-case strengthening batch has a clean 20/20 Wolfram pass result;
- the Isabelle session builds after the recent TRAWIN, physical-architecture, and vector-calculus additions.

The main remaining release risks are manageable:

- the graph depth is now 68 sequential layers, which is credible but should be explained as a richer derivation graph than the earlier 753-edge prototype;
- the original master still retains the 48 shell-artifact signals for provenance, so proof-facing claims should use the proof-clean master or the quarantine report;
- any quarantined row can still be manually rescued later if it is genuine mathematics rather than operational code.

Recommended next move: commit the current package as a first provenance snapshot.
