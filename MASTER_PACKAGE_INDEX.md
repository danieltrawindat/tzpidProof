---
title: TZPIDProof Master Package Index
creator: Daniel Alexander Trawin
orcid: https://orcid.org/0009-0001-4630-3715
generated: 2026-06-12
repository: https://github.com/danieltrawindat/tzpidProof.git
---

# TZPIDProof Master Package Index

This repository is the proof-and-provenance package for the TZPID registry. It is organized as a release bundle rather than a scratch workspace: the master registry, dictionary, encyclopedia, derivation ladder, formal proof lanes, computational certificate lanes, and per-ID source-truth folders are kept together for review and reproducibility.

## Package Counts

| Lane | Current count | Notes |
|---|---:|---|
| Master equation rows | 11,237 | `TZPID_ALL_IDS_CANONICAL_EQUATION_MASTER_with_export.csv` |
| Per-ID source folders | 11,237 | `tzp_id/ID####/` |
| ID-system rows | 11,237 | `TZPID_ID_SYSTEM.csv`; synced with master after adding `ID11372`-`ID11751` |
| Proof-clean master rows | 11,189 | `TZPID_ALL_IDS_CANONICAL_EQUATION_MASTER_PROOF_CLEAN_NO_SHELL_SIGNALS.csv`; shell/code-like signals removed from proof-facing view |
| Isabelle theories | 128 | `tzpid_proof/isabelle_tzpid/*.thy` |
| HDF5 certificates | 6 | `hdf5/*.h5` |

## Master Registry Lane

| Master artifact | Path | Purpose |
|---|---|---|
| Master CSV | `TZPID_ALL_IDS_CANONICAL_EQUATION_MASTER_with_export.csv` | Canonical equation registry and current master row set |
| Proof-clean master CSV | `TZPID_ALL_IDS_CANONICAL_EQUATION_MASTER_PROOF_CLEAN_NO_SHELL_SIGNALS.csv` | Proof-facing master view with shell-artifact signals removed |
| Master MD | `TZPID_ALL_IDS_CANONICAL_EQUATION_MASTER_with_export.md` | Human-readable master export |
| Dictionary | `TZPID_DICTIONARY.csv` | Canonical dictionary terms and definitions |
| Encyclopedia | `TZPID_ENCYCLOPEDIA.md` | Narrative semantic encyclopedia |
| ID system | `TZPID_ID_SYSTEM.csv` | UUID, PiID, RTEID, and provenance identity layer |

## Master Derivation Lane

| Artifact | Path | Purpose |
|---|---|---|
| Reassembled ladder | `TZPID_ALL_IDS_REASSEMBLED_PROOF_LADDER.md` | Derivation-order proof ladder |
| Ladder with equations | `TZPID_ALL_IDS_REASSEMBLED_PROOF_LADDER_WITH_EQUATIONS.md` | Derivation-order ladder plus equation content |
| Graph topology outputs | `graph_topology/` | Connected components, dependency depth, heatmap/export material |
| Python graph layer | `graph_topology/tzpid_graph_layer.py` | Reusable NetworkX/Matplotlib metric and visual-render layer |
| Graph visual report | `graph_topology/GRAPH_VISUAL_LAYER.md` | Visual heatmap report with reproduction command |
| Sledgehammer reports | `sledgehammer/` | Isabelle/Sledgehammer-facing audit outputs |
| DAG paper material | `peer_review/` and `fill_dag_paper.py` | Paper-facing derivation-order breakthrough material |

## Master Formal Lanes

| Lane | Path | Purpose |
|---|---|---|
| Master Isabelle/HOL | `tzpid_proof/isabelle_tzpid/` | Primary checked formal lane |
| HOL/Isar spine layer | `tzpid_proof/isabelle_tzpid/TZPID_VectorCalculus_IsarSpineLayer.thy` | Structured Isar vector-calculus spine layer |
| Integral carriers | `tzpid_proof/isabelle_tzpid/TZPID_VectorCalculus_IntegralCarriers.thy` | Finite Green/Stokes/helicity/flux/winding carriers |
| Physical proof architecture | `tzpid_proof/isabelle_tzpid/TZPID_PhysicalProofArchitecture.thy` | Curry-Howard-Lambek/TQFT proof architecture |
| TRAWIN composition carrier | `tzpid_proof/isabelle_tzpid/TZPID_TRAWIN_Composition_GoldSpine.thy` | `N o I o W o A o R o T` gold-spine closure layer |
| Portal breathing / occupancy interface | `tzpid_proof/isabelle_tzpid/TZPID_PortalBreathing_OccupancyInterface.thy` | Redshift breathing, three-phase occupancy, nested frequency scaling, interface pressure, and portal force-balance carriers |
| Portal equilibrium laws | `tzpid_proof/isabelle_tzpid/TZPID_PortalEquilibrium_Laws.thy` | Force-vector components, five-force balance, phi ratio, golden portal state, and predicted acoustic/field pressure rearrangement |
| S4/S5 hypersphere mix laws | `tzpid_proof/isabelle_tzpid/TZPID_S4S5_Hypersphere_Mix_Laws.thy` | General `S^n`, `S^4`, and `S^5` breathing carriers; redshift/density scalings; folded phase-mix source and golden gate diagnostics |
| Spartan standing-wave expansion | `tzpid_proof/isabelle_tzpid/TZPID_SpartanStandingWave_Expansion.thy` | Metric breathing, Bessel standing nodes, S3/S4/S5 mode ladders, projection carriers, and Spartan Dawn fit diagnostics |
| Paper XI sound-before-light | `tzpid_proof/isabelle_tzpid/TZPID_PaperXI_SoundBeforeLight.thy` | Acoustic horizon, photon-baryon sound speed, BAO standing-node, and Paper XI sound-ruler carriers |
| Paper XII Spartan Dawn | `tzpid_proof/isabelle_tzpid/TZPID_PaperXII_SpartanDawn.thy` | Compressed CMB/BAO/SNe model-comparison carriers, CPL F(z), distance engine, AIC, curvature, and breathing diagnostics |
| Paper XIII S3/S4/S5 geometry | `tzpid_proof/isabelle_tzpid/TZPID_PaperXIII_S3_S4_S5_Geometry.thy` | Exact nested-sphere geometry carriers: volume breathing, spectra, degeneracies, scalar curvature, plus-ell cascade, 3:4:5 triad, and n-dimensional Friedmann scaling |
| Paper XIV nested-shell BAO | `tzpid_proof/isabelle_tzpid/TZPID_PaperXIV_NestedShell_BAO.thy` | BAO period, curvature mode-spacing, modes-per-wiggle ratio, direct-shell exclusion, nested-shell beat epsilon, and degeneracy amplitude carriers |
| Paper XV TRAWIN closure | `tzpid_proof/isabelle_tzpid/TZPID_PaperXV_TRAWIN_Closure.thy` | TRAWIN operator alphabet, type-admissibility census, reach carriers, symbolic closure identities, and keystone closure boundary |
| Papers XI-XV verification suite | `tzpid_proof/isabelle_tzpid/TZPID_PapersXI_XV_VerificationSuite.thy` | Cross-paper HOL certificate linking BAO period, model diagnostics, S3/S4/S5 geometry, nested-shell BAO, and TRAWIN closure carriers |
| Paper XVI volumetric buoyancy | `tzpid_proof/isabelle_tzpid/TZPID_PaperXVI_VolumetricBuoyancy.thy` | Three-phase occupancy, interface energy, domain wall, volumetric force balance, Elsasser criticality, Hodge/helicity diagnostics, and scaling-boundary carriers |
| Paper XVII w(a) derivation | `tzpid_proof/isabelle_tzpid/TZPID_PaperXVII_wa_Derivation.thy` | Equation-of-state identity, inverse-quartic branch, threshold handoff, CPL carriers, negative-foundation sign theorem, and Gauss-Bonnet normalization |
| Paper XVIII standing-wave enlargement | `tzpid_proof/isabelle_tzpid/TZPID_PaperXVIII_StandingWaveEnlargement.thy` | Comoving node enlargement, Hubble-radius recession, e-fold growth, no-signaling bookkeeping, and projection dark-energy carrier |
| Lean/Rocq exports | `tzpid_proof/lean_rocq_gold_spine/` | Secondary portability lane for Lean and Rocq/Coq |
| Semantic batches | `tzpid_proof/batches/` and `tzpid_proof/individual_theories.*` | 397-row theorem semantic translation lane |

## Master Computational Lanes

| Lane | Path | Purpose |
|---|---|---|
| Master Wolfram verification | `wolfram_master_verification/` | Master-equation Wolfram scan scripts and run archives |
| Wolfram source-truth verification | `wolfram_source_truth_verification/` | Per-ID/source-truth Wolfram form verification |
| Wolfram submission package | `wolfram_submission/` | Submission-ready Wolfram verification summaries |
| HDF5 certificates | `hdf5/` | Delta-alpha, bridge, vector-calculus, circulation, winding, and resonance data |
| Edge-case equations | `edge_case_equations/` | Strengthening certificates and quarantined shell-code artifacts |
| Shell-artifact quarantine | `edge_case_equations/TZPID_MASTER_SHELL_ARTIFACT_SIGNAL_QUARANTINE.md` | Rows scrapped from proof-facing clean outputs |
| Portal breathing intake | `peer_review/portal_breathing_intake/` | 56 minted equations from `the_portal_equation.txt`, `hypersphere_idea.txt`, and `ll restart from the original hypersphere.txt`, with Wolfram and Isabelle certificates |
| Spartan Dawn empirical lane | `this_is_SPARTA/` | Compressed CMB+BAO+SNe test for the Hubble/Friedmann breathing spine |
| Spartan standing-wave intake | `peer_review/spartan_standing_wave_intake/` | 103 minted equations from `standing_wave_expaansion.txt` and `TZPID_SPARTAN_DAWN_CMB_BAO_SNE_TEST.md`, with Wolfram and Isabelle certificates |
| Paper XI sound-before-light intake | `peer_review/paper_xi_sound_before_light_intake/` | 13 minted equations from `Paper_XI_Sound_Before_Light.tex`, with source-truth folders and Isabelle certificate |
| Paper XII Spartan Dawn intake | `peer_review/paper_xii_spartan_dawn_intake/` | 27 minted equations from `Paper_XII_Spartan_Dawn_Test.tex`, with source-truth folders and Isabelle certificate |
| Paper XIII S3/S4/S5 geometry intake | `peer_review/paper_xiii_s3_s4_s5_geometry_intake/` | 40 minted equations from `Paper_XIII_S3_S4_S5_Geometry.tex`, with source-truth folders and Isabelle certificate |
| Paper XIV nested-shell BAO intake | `peer_review/paper_xiv_nested_shell_bao_intake/` | 27 minted equations from `Paper_XIV_Nested_Shell_BAO.tex`, with source-truth folders and Isabelle certificate |
| Paper XV TRAWIN closure intake | `peer_review/paper_xv_trawin_closure_intake/` | 28 minted equations from `Paper_XV_TRAWIN_Closure.tex`, with source-truth folders and Isabelle certificate |
| Papers XI-XV HOL/Wolfram verification | `peer_review/papers_xi_xv_verification/` | Consolidated HOL suite and Wolfram certificate for 135 registered IDs spanning `ID11536`-`ID11670` |
| Paper XVI volumetric buoyancy intake | `peer_review/paper_xvi_volumetric_buoyancy_intake/` | 22 minted equations from `Paper_XVI_Volumetric_Buoyancy.tex`, with source-truth folders and Isabelle certificate |
| Paper XVII w(a) derivation intake | `peer_review/paper_xvii_wa_derivation_intake/` | 36 minted equations from `Paper_XVII_wa_Derivation.tex`, with source-truth folders and Isabelle certificate |
| Paper XVIII standing-wave enlargement intake | `peer_review/paper_xviii_standing_wave_enlargement_intake/` | 23 minted equations from `Paper_XVIII_Standing_Wave_Enlargement.tex`, with source-truth folders and Isabelle certificate |

## Master PiID/RTEID And Source-Truth Lane

| Artifact | Path | Purpose |
|---|---|---|
| PiID/RTEID table | `TZPID_ID_SYSTEM.csv` | Master identity table with PiID and RTEID fields |
| Per-ID folders | `tzp_id/ID####/` | One folder per registry ID |
| Source-truth JSON | `tzp_id/ID####/*.json` | Per-ID source-truth and metadata blocks |
| Source TeX | `tzp_id/ID####/*.tex` | Per-ID TeX representation when available |
| Metadata embedding scripts | `tzpid_proof/metadata_embedding_mechanism/` | Scripts that create/fill/update per-ID source-truth metadata |
| Sync report | `MASTER_SYNC_REPORT.md`, `MASTER_SYNC_REPORT.json`, and `TZPID_ID_SYSTEM_EXTENSION_REPORT.json` | Master-to-proof package sync and identity extension reports |

## Master Spine And Paper Lanes

| Lane | Path | Purpose |
|---|---|---|
| Gold spines | `tzpid_proof/spines/` | Curated gold-spine proof documents and obligations |
| TRAWIN spine | `TRAWIN/` | TRAWIN operator and composition certificates |
| Spartan Dawn certificate | `this_is_SPARTA/SPARTAN_DAWN_CERTIFICATE.md` | Empirical model-comparison certificate for ID10867/ID10868/ID10871 |
| Peer review papers | `peer_review/` | Papers, DOI updates, review material, and intake certificates |
| AFP submission | `afp_submission/` | Isabelle AFP submission material |
| Release phase 3 | `tzpid_proof/release_phase3/` | Publication/release packaging area |

## Verification Commands

Primary Isabelle build:

```powershell
D:\Isabelle2025\Isabelle2025-2\bin\isabelle build -D D:\TZPIDProof\tzpid_proof\isabelle_tzpid
```

Lean/Rocq sources are in:

```text
D:\TZPIDProof\tzpid_proof\lean_rocq_gold_spine
```

Wolfram verification packages are in:

```text
D:\TZPIDProof\wolfram_master_verification
D:\TZPIDProof\wolfram_submission
```

## Release Discipline

- Keep the master CSV, dictionary, encyclopedia, derivation ladder, and ID-system table together.
- Keep per-ID JSON/TeX folders under `tzp_id/` as the source-truth identity layer.
- Keep Isabelle/HOL as the primary formal lane; Lean/Rocq are portability lanes.
- Keep Wolfram/Python/HDF5 as computational certificate lanes.
- Keep shell-code artifacts quarantined under `edge_case_equations/` unless manually reclassified.
- Use `TZPID_ALL_IDS_CANONICAL_EQUATION_MASTER_PROOF_CLEAN_NO_SHELL_SIGNALS.csv` for proof-facing claims when shell/code-like rows should be excluded.
