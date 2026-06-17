# Priority Promotion Decisions

Generated: 2026-06-11

## Scope

This file summarizes the first promotion review for the `Topological Unification of QM and GR` source.  The source produced 14 clean review candidates in `PRIORITY_MINTING_REVIEW.md`.  They are now mirrored in Isabelle/HOL by `TZPID_TopologicalUnification_PriorityCandidates.thy`.

The deduplication pass found existing registry homes for all five rows that were initially marked `Mint_After_Review`; no duplicate IDs were minted for those equations.  The five `HOL_Carrier_First` categorical structures were then minted as new carrier definitions `ID11372`--`ID11376`.

## Decision Summary

| Decision | Count | Meaning |
| --- | ---: | --- |
| `HOL_Carrier_First` | 5 | Minted as carrier definitions `ID11372`--`ID11376` so the categorical structure is addressable. |
| `Reuse_Existing_ID` | 7 | Already covered by existing registry IDs; attach as evidence/refinement rather than minting. |
| `Merge_With_Existing_Spine` | 2 | Promote by strengthening an existing spine lane, not by creating a standalone ID immediately. |
| `Mint_After_Review` | 0 | No surviving mint candidates after master deduplication. |

## Candidate Decisions

| Candidate | Line | Action | Review target |
| --- | ---: | --- | --- |
| HigherTopos_ObjectDefinition | 105 | `HOL_Carrier_First` | Minted as `ID11373`. |
| HigherTopos_HomMorphism | 133 | `HOL_Carrier_First` | Minted as `ID11374`. |
| FQT_Metric_TensorSum | 284 | `HOL_Carrier_First` | Minted as `ID11375`. |
| FQT_Metric_Product | 295 | `HOL_Carrier_First` | Minted as `ID11376`. |
| HigherTopos_FormalDefinition | 84 | `HOL_Carrier_First` | Minted as `ID11372`. |
| TZP_Vacuum_Divergence | 190 | `Reuse_Existing_ID` | Reuse `ID4214`; related compressed form `ID4227`. |
| Elsasser_Universality | 212 | `Merge_With_Existing_Spine` | Fold into gyromagnetic / magnetic-torsion lane if distinct from existing Elsasser entries. |
| Information_Manifold_Structure | 256 | `Reuse_Existing_ID` | Reuse `ID4192` and `ID4193`; related DAANS manifold support in `ID0245`, `ID0285`, `ID0396`. |
| Universal_Critical_Exponent | 306 | `Reuse_Existing_ID` | Likely reuse `ID0395` / avalanche critical exponent family. |
| Topological_Field_Constraint | 338 | `Reuse_Existing_ID` | Reuse `ID4195` or stronger parse-certified `ID11134`; related scaling in `ID10136`, `ID0140`, `ID4305`. |
| Topological_Locking | 351 | `Merge_With_Existing_Spine` | Merge with quantum/magnetic flux quantization entries if equivalent. |
| Universal_Criticality | 359 | `Reuse_Existing_ID` | Duplicate or refinement of avalanche criticality IDs. |
| Integrated_Information_Threshold | 397 | `Reuse_Existing_ID` | Reuse `ID4200` / `ID4218`; related support in `ID4364`, `ID0463`, `ID8488`. |
| Discrete_Dark_Matter_Distribution | 406 | `Reuse_Existing_ID` | Reuse `ID4201` and `ID4229`; related source rows include `ID4220`, `ID11143`, `ID0288`. |

## Isabelle Evidence

The typed review ledger is:

`D:\TZPIDProof\tzpid_proof\isabelle_tzpid\TZPID_TopologicalUnification_PriorityCandidates.thy`

It proves:

- `priority_candidate_count`: 14 candidates are tracked.
- `mint_review_count`: 0 require mint-after-review after deduplication.
- `reuse_or_merge_count`: 9 should reuse or merge with existing IDs/spines.
- `carrier_first_count`: 5 are carrier-first structures.
- `carrier_first_candidates_are_minted`: all carrier-first structures now have minted IDs.
- `minted_carrier_registry_ids`: links the carrier-first candidates to `ID11372`--`ID11376`.
- `reviewed_candidates_partition`: the three decision classes cover the full candidate set.

The full Isabelle session builds cleanly after adding this theory.

## Merge Certificate

The two `Merge_With_Existing_Spine` rows are now covered by:

`D:\TZPIDProof\peer_review\unification_intake\TOPOLOGICAL_UNIFICATION_SPINE_MERGE_CERTIFICATE.md`

The corresponding Isabelle theory is:

`D:\TZPIDProof\tzpid_proof\isabelle_tzpid\TZPID_TopologicalUnification_SpineMerges.thy`

It connects Elsasser universality to the existing MHD/Elsasser lane and topological locking to the existing flux-quantization lane.

## Wolfram Evidence

The existing-ID reuse set has a WolframScript review artifact:

`D:\TZPIDProof\peer_review\unification_intake\wolfram\topological_unification_existing_id_review_results.json`

It records five existing-ID checks: four symbolic carrier verifications and one computed pass for the opposing-dipole `d^{-4}` divergence.

The minted carrier set also has a WolframScript artifact:

`D:\TZPIDProof\peer_review\unification_intake\wolfram\topological_unification_carrier_mint_check_results.json`

It records five symbolic-carrier verifications for `ID11372`--`ID11376`.

## Next Work

1. Update the relevant spine notes to cite the resolved existing IDs rather than minting duplicates.
2. Consume `ID11372`--`ID11376` in the next typed HOL carrier theory for Topological Unification.
3. For the two `Merge_With_Existing_Spine` cases, strengthen the gyromagnetic/magnetic-flux and avalanche/criticality lanes rather than creating standalone rows.
