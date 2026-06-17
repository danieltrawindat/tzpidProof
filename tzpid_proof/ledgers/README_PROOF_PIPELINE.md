# TZPID Proof Pipeline Status

This workspace contains the current TZPID proof-pipeline artifacts built from the canonical equation master CSV, `TZPID_ENCYCLOPEDIA.md`, extracted axiom/theorem candidates, Isabelle/HOL theories, and Wolfram-backed symbolic checks.

The current focus is the Einstein/cosmology "gold spine":

```text
ID0958 unified operator action
  -> effective Einstein sector
  -> ID0394 TZP vacuum stress-energy tensor
  -> ID0167 conserved total stress-energy
  -> ID0335 modified Einstein equation
  -> classical Einstein limit far from TZP

ID0400 cosmological density
  -> normalized Hubble/dark-energy bridge
  -> vacuum density handoff into the same stress-energy chain
```

## Source Inputs

- `TZPID_ALL_IDS_CANONICAL_EQUATION_MASTER_with_export.csv`
  - Canonical registry CSV.
  - Main source for IDs, titles, statements, equations, classifications, variables, and UUIDs.
- `TZPID_ENCYCLOPEDIA.md`
  - Semantic source text used to ground focused registry IDs and interpretive roles.
- `D:\Zenodo` and `D:\Tex`
  - Scanned source corpora for axioms, definitions, theorems, lemmas, principles, laws, hypotheses, and source hints.
- `proof.txt`
  - Proof-pipeline intent and staging notes.
- `proof2.py`
  - CSV equation runner and cleanup classifier.

## Equation Pipeline

The CSV equation pipeline was run over the canonical equation master and produced:

| Status | Count |
|---|---:|
| Passed | 7,186 |
| Syntax Error | 1,893 |
| Approximated Parse | 398 |
| Partial Parse | 238 |
| Needs cleanup | 43 |

Main outputs:

- `toe_pipeline_results.csv`
- `toe_shortlist.csv`
- `toe_approximated_parse.csv`
- `toe_cleanup_queue.csv`
- `toe_shortlist_pipeline_results.csv`

The current proof work is based on the passed/shortlisted material plus targeted semantic promotion of important IDs.

## Axiom/Theorem Extraction

The source scan and graph extraction produced:

| Artifact | Count |
|---|---:|
| Statement inventory | 9,810 |
| Dependency edges | 5,285 |
| Zenodo/Tex axiom-theory candidates | 618 |

Main outputs:

- `axiom_theorem_extraction/statement_inventory.csv`
- `axiom_theorem_extraction/dependency_edges.csv`
- `axiom_theorem_extraction/axiom_theorem_dependency_graph.md`
- `axiom_theorem_extraction/axiom_theorem_dependency_graph.dot`
- `zenodo_tex_axiom_theory_scan/axiom_theory_candidates.csv`
- `zenodo_tex_axiom_theory_scan/important_axioms_theories.md`

## Isabelle Session

The Isabelle session lives in `isabelle_tzpid`.

Theories in build order:

```text
TZPID_Manifest
TZPID_Axioms
TZPID_Core
TZPID_Obligations
TZPID_Einstein_Focus
TZPID_Einstein_Computational_Checks
```

Main Isabelle artifacts:

- `isabelle_tzpid/ROOT`
- `isabelle_tzpid/TZPID_Manifest.thy`
- `isabelle_tzpid/TZPID_Axioms.thy`
- `isabelle_tzpid/TZPID_Core.thy`
- `isabelle_tzpid/TZPID_Obligations.thy`
- `isabelle_tzpid/TZPID_Einstein_Focus.thy`
- `isabelle_tzpid/TZPID_Einstein_Computational_Checks.thy`

Build command:

```powershell
& 'D:\Isabelle2025\Isabelle2025-2\contrib\cygwin\bin\bash.exe' -lc 'cd /cygdrive/d/tzpidNEW && /cygdrive/d/Isabelle2025/Isabelle2025-2/bin/isabelle build -c -D isabelle_tzpid'
```

Latest build status:

```text
Finished TZPID (0:00:28 elapsed time)
```

Note: the Isabelle launcher currently prints:

```text
/cygdrive/d/Isabelle2025/Isabelle2025-2/bin/isabelle: line 1: ok: command not found
```

The warning appears to come from a stray `ok` line in the launcher file. It has not blocked successful builds.

## Broad Proof Obligations

The 618 extracted candidates are classified in `isabelle_tzpid/proof_obligations.csv`.

| Obligation role | Count |
|---|---:|
| Core_Axiom | 43 |
| Core_Definition | 199 |
| Derived_Theorem_Obligation | 269 |
| Hypothesis_Only | 16 |
| Needs_Semantic_Translation | 91 |

Summary:

- `TZPID_Manifest.thy` records registry manifest counts and digests.
- `TZPID_Axioms.thy` promotes high-confidence axioms.
- `TZPID_Core.thy` gives typed TZPID core objects and registers all 618 candidates.
- `TZPID_Obligations.thy` classifies proof work without pretending all physics is proved.

## Focused Gold Spine

The focused gold spine currently uses six registry targets:

| ID | Role |
|---|---|
| ID0958 | Unified operator action / action-level effective Einstein sector |
| ID0400 | Cosmological constant and master unification equation |
| ID0394 | TZP bridge-tunnel energy-momentum tensor |
| ID0167 | Unified total stress-energy equation |
| ID0335 | Modified Einstein equation with TZP source |
| ID1392 | Normalized duplicate of ID0400 |

Focus artifacts:

- `prepare_isabelle_einstein_focus.py`
- `isabelle_tzpid/einstein_focus_obligations.csv`
- `isabelle_tzpid/einstein_focus_summary.md`
- `isabelle_tzpid/TZPID_Einstein_Focus.thy`

Core focused Isabelle theorems:

- `id0400_three_part_density_obligation`
- `id0335_recovers_classical_einstein_far_from_tzp`
- `id0394_id0167_stress_energy_bridge`
- `id0958_action_level_einstein_bridge`

These theorems are typed and structured, but many predicates are still abstract locale assumptions. The pipeline is now ready to replace selected predicates with deeper definitions incrementally.

## Wolfram Certificates

Wolfram checks live in:

- `wolfram_checks/einstein_focus_checks.wl`
- `wolfram_checks/einstein_focus_results.json`
- `isabelle_tzpid/wolfram_certificate_summary.md`

Certificate generator:

- `prepare_isabelle_wolfram_certificates.py`

Current Wolfram status:

| Status | Count |
|---|---:|
| pass | 13 |
| computed | 1 |
| needs_normalization | 1 |

The only intentional `needs_normalization` result is the direct comparison:

```text
rho_Lambda ~ H0^2
```

The normalized form passes:

```text
rho_Lambda = Omega_Lambda * (3 c^2 / (8 pi G)) * H0^2
```

Wolfram-backed Isabelle certificate theorems:

- `id0335_formal_limit_has_wolfram_certificate`
- `id0400_density_handoff_has_wolfram_certificate`
- `id0400_hubble_comparison_left_as_normalization_obligation`
- `id0400_hubble_normalization_has_wolfram_certificate`
- `id0394_vacuum_tensor_has_wolfram_certificate`
- `id0167_total_stress_energy_has_wolfram_certificate`
- `id0394_id0167_stress_energy_bridge_has_wolfram_certificate`
- `id0958_action_level_bridge_has_wolfram_certificate`
- `id0958_to_id0335_focused_chain_has_wolfram_certificate`

## Reproducible Regeneration

Run these from `d:\tzpidNEW`.

Regenerate the focused Isabelle layer:

```powershell
python prepare_isabelle_einstein_focus.py
```

Run Wolfram checks:

```powershell
wolframscript -file wolfram_checks\einstein_focus_checks.wl wolfram_checks\einstein_focus_results.json
```

Regenerate Isabelle certificate layer:

```powershell
python prepare_isabelle_wolfram_certificates.py
```

Build Isabelle:

```powershell
& 'D:\Isabelle2025\Isabelle2025-2\contrib\cygwin\bin\bash.exe' -lc 'cd /cygdrive/d/tzpidNEW && /cygdrive/d/Isabelle2025/Isabelle2025-2/bin/isabelle build -c -D isabelle_tzpid'
```

Full focused refresh:

```powershell
python prepare_isabelle_einstein_focus.py
wolframscript -file wolfram_checks\einstein_focus_checks.wl wolfram_checks\einstein_focus_results.json
python prepare_isabelle_wolfram_certificates.py
& 'D:\Isabelle2025\Isabelle2025-2\contrib\cygwin\bin\bash.exe' -lc 'cd /cygdrive/d/tzpidNEW && /cygdrive/d/Isabelle2025/Isabelle2025-2/bin/isabelle build -c -D isabelle_tzpid'
```

## What Is Proved vs. What Is Still Obligational

Proved in Isabelle:

- The generated Isabelle theories are syntactically and logically accepted by Isabelle/HOL.
- The focused locale theorems follow from named typed assumptions.
- The computational certificate layer correctly records Wolfram pass/computed/normalization statuses.
- The gold-spine theorem chain is internally consistent at the typed-predicate level.

Checked by Wolfram:

- ID0335 far-field reduction when the TZP correction term vanishes.
- ID0400 energy-density dimensional balance and normalized Hubble density bridge.
- ID0394 vacuum tensor form and inverse Bessel density profile representation.
- ID0167 total stress-energy decomposition, vacuum handoff, and conservation linearity.
- ID0958 wave-source, effective Einstein sector, Lagrangian decomposition, and action-sector carrier relations.

Still obligations, not fully discharged physics:

- Concrete tensor calculus is not yet formalized in Isabelle.
- Differential geometry objects are represented by typed predicates, not full manifolds/connections/curvature definitions.
- Wolfram certificates are external computational evidence, not native Isabelle proofs of analytic tensor identities.
- The full 618-candidate corpus remains classified, not fully proved.
- The 91 `Needs_Semantic_Translation` obligations still need manual/semantic promotion before serious proof work.

## Next Step: Lean/Rocq Gold-Spine Export

The next planned step is to mirror the gold spine into Lean and Rocq as small certificate sets, not to port all 618 candidates.

Recommended export scope:

```text
ID0958 action_level_einstein_bridge
ID0400 three_part_density_obligation
ID0394 vacuum_tensor
ID0167 total_stress_energy
ID0394 -> ID0167 stress_energy_bridge
ID0335 far_field_classical_limit
ID0958 -> ID0335 focused_chain
```

Lean/Rocq should initially mirror the typed-predicate structure:

- declare abstract types
- declare predicates
- declare assumptions corresponding to the Isabelle locale
- prove the same chain lemmas by assumption composition
- attach the Wolfram result SHA/status table as comments or constants

After the mirror builds, the next upgrade is replacing one abstract predicate at a time with native definitions.

## Algorithmic-Ambassador AA Spines

The AA range is now curated into four additional gold spines:

- Vortex-Core Topological Fluid Dynamics
- DNA-TZPQVS Isomorphism
- Neutrino-Piezoelectric Coupling
- Quantum-Information Genesis of Curvature

Primary artifacts:

- `TZPID_AA_GOLD_SPINES.md`
- `TZPID_AA_SPINES_obligations.csv`
- `isabelle_tzpid/TZPID_AA_Spines_Focus.thy`
- `isabelle_tzpid/TZPID_AA_Spines_Computational_Checks.thy`
- `wolfram_checks/aa_spines_checks.wl`
- `wolfram_checks/aa_spines_results.json`
- `wolfram_checks/aa_module_library_runner.wl`
- `wolfram_checks/aa_module_library_results.json`
- `TZPID_WOLFRAM_MODULE_LIBRARY_certified.csv`

Regenerate and check:

```powershell
python prepare_aa_spines_focus.py
wolframscript -file wolfram_checks\aa_spines_checks.wl wolfram_checks\aa_spines_results.json
wolframscript -file wolfram_checks\aa_module_library_runner.wl 'D:\00_Engine\AI_Workspaces\OpenAI2\algorithmic_ambassador\TZPID_WOLFRAM_MODULE_LIBRARY.csv' wolfram_checks\aa_module_library_results.json 1.0 parse
python summarize_aa_module_results.py
python prepare_aa_spines_certificates.py
& 'D:\Isabelle2025\Isabelle2025-2\bin\isabelle' build -D isabelle_tzpid
```

Current AA computational status:

- Focused spine checks: 12/12 pass.
- Module library parse lane: 57 executable parse-passes, 135 normalized source packets, 0 raw parse failures, 0 missing results.
- Full evaluation mode exists in `aa_module_library_runner.wl`, but parse mode is the safe default because report excerpts may still need dependency and pseudocode normalization before execution.
