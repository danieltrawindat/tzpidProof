# TZPIDProof Master Sync Report

Generated UTC: 2026-06-11T02:30:00Z

## Source

- Source master copied from: `D:\00_Engine\AI_Workspaces\OpenAI2\TZPID_ALL_IDS_CANONICAL_EQUATION_MASTER_with_export.csv`
- Destination master: `D:\TZPIDProof\TZPID_ALL_IDS_CANONICAL_EQUATION_MASTER_with_export.csv`
- Backup folder: `D:\TZPIDProof\sync_backup_20260610_221012`

## Registry Coverage

- Synced master rows: `10,357`
- Previous proof-package rows: `10,271`
- Newly appended IDs in derivation ladder: `86`
- New appended range: `ID10786` through `ID10871`
- Missing source-truth folders created: `86`
- Current source-truth folders: `10,357`
- Current ID-system rows: `10,357`
- Master vs ladder ID gaps: `0`
- Master vs ID-system gaps: `0`
- Master vs source-truth folder gaps: `0`

## ID-System Coverage

- `TZPID_ID_SYSTEM.csv` extended from `9,758` rows to `10,357` rows.
- Added ID-system rows: `599`
- Current max ID-system row: `ID10871`
- ID-system sidecars updated/created: `10,357`
- Source-truth JSONs linked to ID-system sidecars: `10,357`
- Example high-ID metadata:
  - `ID10786`: PiID `9065287036650`, RTEID `RTE:P41884.4333:T6.1808`
  - `ID10871`: PiID `3992539944280`, RTEID `RTE:P42214.5072:T0.4415`

## Derivation Ladder

- Updated ladder: `D:\TZPIDProof\TZPID_ALL_IDS_REASSEMBLED_PROOF_LADDER.md`
- Updated equation ladder: `D:\TZPIDProof\TZPID_ALL_IDS_REASSEMBLED_PROOF_LADDER_WITH_EQUATIONS.md`
- Method: preserved prior certified order for the first `10,271` rungs and appended the `86` newly synced entries as an incremental block.
- Note: dependency mining has now been refreshed against the synced ladder; appended entries are included in the graph topology report.

## Graph Topology

- Total ladder nodes: `10,357`
- Materialized upward dependency edges: `2,080`
- Cut/downward references retained for audit: `71`
- Isolated nodes: `8,387`
- Non-isolated nodes: `1,970`
- Connected components total: `8,618`
- Nontrivial connected clusters: `231`
- Largest connected cluster: `1,046` nodes / `1,363` edges
- Maximum dependency depth: `67` edges / `68` sequential layers
- DAG cyclicity check: `acyclic`
- Updated report: `D:\TZPIDProof\graph_topology\GRAPH_TOPOLOGY_REPORT.md`

## Paper ID Audit

- Papers checked: `10`
- Unique explicit paper IDs: `125`
- Explicit paper IDs present in synced derivation ladder: `125`
- Explicit paper ID mismatches after sync: `0`
- New high-ID ranges verified:
  - `ID10786--ID10790`: `5 / 5` present
  - `ID10793--ID10860`: `68 / 68` present

## Wolfram Coverage

- Source-truth Wolfram carrier blocks parse-pass: `12,263 / 12,263`
- IDs with Wolfram carrier parse-pass: `10,357 / 10,357`
- Numeric/symbolic representation blocks parse-pass: `11,826 / 11,826`
- IDs with parse-verified numeric/symbolic representation: `10,357 / 10,357`
- Blocks with extracted numeric atoms: `7,207`
- Optional safe Wolfram candidate expressions: `2,082`
- Active candidate parse failures: `0`

## Isabelle

- Regenerated `TZPID_DerivationOrder.thy` against the refreshed `2,080` materialized-edge table.
- Isabelle build passed:

```powershell
D:\Isabelle2025\Isabelle2025-2\bin\isabelle build -D D:\TZPIDProof\tzpid_proof\isabelle_tzpid
```

## Remaining Follow-Up

- Optional: review the `71` cut/downward references in `D:\TZPIDProof\graph_topology\cut_edge_transitive_audit.csv` to decide whether any should become explicit reordered dependencies in a future ladder revision.
- Optional: if Paper 10 should use the refreshed `2,080`-edge theorem instead of the earlier `753`-edge theorem, promote `paper10_dag_breakthrough.generated.tex` into the live paper after review.
