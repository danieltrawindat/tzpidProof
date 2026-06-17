# TZPIDProof

Proof, provenance, and certificate package for the TZPID registry and paper series.

Creator: Daniel Alexander Trawin  
ORCID: https://orcid.org/0009-0001-4630-3715  
Repository target: https://github.com/danieltrawindat/tzpidProof.git

## What This Repository Contains

This repository is a reproducible proof-and-provenance bundle for the TZPID project. It collects the master registry, derivation ladder, per-ID source-truth records, Isabelle/HOL theories, Wolfram/Python/HDF5 certificates, gold spines, peer-review papers, and release/audit reports.

The package is meant to be reviewable in layers:

- `TZPID_ALL_IDS_CANONICAL_EQUATION_MASTER_with_export.csv` - current canonical master registry.
- `TZPID_ALL_IDS_CANONICAL_EQUATION_MASTER_PROOF_CLEAN_NO_SHELL_SIGNALS.csv` - proof-facing master view with shell/code-like artifacts quarantined.
- `TZPID_DICTIONARY.csv` and `TZPID_ENCYCLOPEDIA.md` - dictionary and semantic encyclopedia.
- `TZPID_ID_SYSTEM.csv` - PiID/RTEID/UUID identity layer.
- `TZPID_ALL_IDS_REASSEMBLED_PROOF_LADDER.md` - derivation-order proof ladder.
- `tzp_id/` - per-ID source-truth JSON/TeX folders.
- `tzpid_proof/isabelle_tzpid/` - primary Isabelle/HOL proof lane.
- `tzpid_proof/lean_rocq_gold_spine/` - Lean/Rocq portability scaffolds.
- `wolfram_master_verification/`, `wolfram_source_truth_verification/`, and `wolfram_submission/` - Wolfram verification lanes.
- `hdf5/` - numerical certificate artifacts.
- `graph_topology/` - dependency topology, edge lists, depth layers, and heatmap outputs.
- `edge_case_equations/` - edge-case strengthening and shell-artifact quarantine.
- `peer_review/` - paper drafts, DOI updates, intake reports, and paper-facing certificates.
- `theory_inventory/` - full Isabelle theory/declaration inventory.

See also:

- `MASTER_PACKAGE_INDEX.md`
- `REPO_SNAPSHOT_READINESS_REPORT.md`
- `MASTER_SYNC_REPORT.md`
- `theory_inventory/TZPID_ISABELLE_DECLARATION_INVENTORY_SUMMARY.md`

## Verification

Primary Isabelle build:

```powershell
D:\Isabelle2025\Isabelle2025-2\bin\isabelle build -D D:\tzpidProof\tzpid_proof\isabelle_tzpid
```

Graph topology refresh:

```powershell
python D:\tzpidProof\rebuild_graph_topology_from_synced_ladder.py
python D:\tzpidProof\graph_topology\tzpid_graph_layer.py --render
```

Edge-case audit:

```powershell
python D:\tzpidProof\edge_case_equations\build_edge_case_equation_audit.py
```

Wolfram verification packages are staged under:

```text
wolfram_master_verification/
wolfram_source_truth_verification/
wolfram_submission/
```

## Licensing

This repository uses a project-specific dual licensing model:

- Academic, scholarly, archival, teaching, review, quotation, and non-commercial research reuse is intended to be open under a CC BY 4.0-style attribution framework.
- Commercial technology implementation, productization, or monetized deployment is governed by the project-specific RL50 terms described in `LICENSING_RL50_CC40.md`.

Short version: cite and attribute the work for academic use; contact the creator before commercial technology use. The RL50 term is intended to reserve a 50 percent share of net commercial gains from commercial exploitation of project-derived technology.

This is a project license notice, not legal advice. See:

- `LICENSE`
- `LICENSING_RL50_CC40.md`

## Citation / Attribution

Recommended attribution:

> Trawin, Daniel Alexander. TZPIDProof: Proof, provenance, and certificate package for the TZPID registry and gold-spine proof architecture. 2026.

Include ORCID where possible:

```text
Daniel Alexander Trawin
ORCID: 0009-0001-4630-3715
```

## Repository Notes

This repository is large because it includes source-truth folders, formal theories, CSV/Markdown master files, and certificate artifacts. At the time of setup the package is under GitHub's single-file hard limit, but the total checkout is close to 1 GB. If GitHub rejects a push due to repository-size policy, move generated/release artifacts to GitHub Releases or Zenodo and keep lightweight pointers here.
