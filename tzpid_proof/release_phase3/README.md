# TZPID Phase 3 Release Package

Creator: Daniel Alexander Trawin
ORCID: https://orcid.org/0009-0001-4630-3715
Generated UTC: 2026-06-09T20:56:49+00:00
Generated from commit: `99303e1b22606b09ba32abc1706004cb3f609929`
Branch: `main`
Remote: `https://github.com/DanielAlexanderTrawin/tzpid-proof-pipeline.git`

## Purpose

This folder is the Phase 3 publication/release package for the TZPID proof pipeline. It bundles the checked Isabelle/HOL session, semantic matrix, computational certificates, paper-facing spines, export scaffolds, and verification instructions needed to reproduce the current proof state.

## Core Status

- Matrix rows: `29`
- Clean Isabelle rows: `29`
- Rows with certificate lane: `29`
- Rows with missing files: `0`

## Entry Points

- Verification commands: `VERIFY.md`
- Verification appendix: `VERIFICATION_APPENDIX.md`
- Spine pack index: `SPINE_PACK.md`
- Certificate manifest: `CERTIFICATE_MANIFEST.md`
- HDF5 artifact manifest: `HDF5_ARTIFACTS.md`
- Release notes: `RELEASE_NOTES.md`
- Paper package index: `papers/PAPER_PACKAGE_INDEX.md`
- Export lane notes: `exports/EXPORT_NOTES.md`
- Zenodo metadata: `ZENODO_METADATA.json`
- Citation metadata: `CITATION.cff`

## Release Folder Layout

- `matrices/`: copied Phase 2 completion and semantic-translation matrices.
- `certificates/`: copied certificate JSON, Markdown, and CSV outputs.
- `isabelle/`: copied Isabelle theories and session `ROOT`.
- `spines/`: copied paper-facing spine Markdown and obligations CSV files.
- `wolfram/`: copied Wolfram check scripts from the spine workspace.
- `wolfram_results/`: copied Wolfram result JSON files.
- `exports/`: copied Lean/Rocq export lane artifacts.
- `papers/`: paper-facing index plus available root `.tex`/`.pdf` manuscript files.
