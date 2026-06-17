# TZPID Phase 3 Release Notes

Generated UTC: 2026-06-09T20:56:50+00:00
Commit: `99303e1b22606b09ba32abc1706004cb3f609929`
Branch: `main`
Remote: `https://github.com/DanielAlexanderTrawin/tzpid-proof-pipeline.git`

## Scope

This package freezes the Phase 2 proof/certificate substrate as a Phase 3 publication-and-release bundle. It does not claim a first-principles proof of every physical interpretation; it packages the current semantic carriers, formal obligations, computational certificates, and paper-facing spine documents in a reproducible form.

## Included Release Lanes

- Isabelle/HOL session copy in `isabelle/`.
- Phase 2 completion and semantic matrices in `matrices/`.
- Python/Wolfram/HDF5 certificate artifacts in `certificates/`, `wolfram/`, and `HDF5_ARTIFACTS.*`.
- Paper-facing spine documents and obligations in `spines/`.
- Lean/Rocq exported scaffolds in `exports/`.
- Paper package index and available paper source/PDF in `papers/`.
- Zenodo and citation metadata in `ZENODO_METADATA.json` and `CITATION.cff`.

## Completion Snapshot

- Matrix rows: `29`
- Clean Isabelle rows: `29`
- Rows with certificate lane: `29`
- Rows with missing files: `0`

## Finalization Notes

A final release tag should be pushed only after running the commands in `VERIFY.md` and confirming the generated commit matches the intended archive state.
