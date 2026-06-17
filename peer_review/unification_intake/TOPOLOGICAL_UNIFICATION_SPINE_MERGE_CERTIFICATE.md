# Topological Unification Spine Merge Certificate

Generated: 2026-06-11

## Result

The two `Merge_With_Existing_Spine` candidates from the Topological Unification priority queue have been merged into existing proof lanes rather than minted as duplicate equations.

## Merge Targets

| Candidate | Source line | Existing lane | Existing IDs / anchors | Isabelle result |
| --- | ---: | --- | --- | --- |
| Elsasser Universality | 212 | Gyromagnetic / magnetic-torsion MHD | `ID0038`, `ID0040`, `ID8826`, `ID9081`, `ID9525` | MHD balance implies `elsasser_number = 1` and therefore lies within the source tolerance `1 ± 0.5`. |
| Topological Locking | 351 | Topology/vector flux quantization | `ID3386`, `ID8523`, `ID9723`, `ID4218` | Flux form `n * Phi_0` is consumed by the existing `flux_quantized` carrier. |

## Isabelle Evidence

Merge theory:

`D:\TZPIDProof\tzpid_proof\isabelle_tzpid\TZPID_TopologicalUnification_SpineMerges.thy`

It proves:

- `merge_target_count`: two merge targets are tracked.
- `merge_targets_trace_to_priority_candidates`: both targets trace to `Merge_With_Existing_Spine` review actions.
- `elsasser_merge_gives_unit_and_half_tolerance`: MHD balance gives unit Elsasser and the `1 ± 0.5` tolerance.
- `topological_locking_flux_is_quantized`: the locking flux is quantized by the existing topology/vector carrier.
- `topological_locking_recovers_registered_flux_multiple`: the locking carrier recovers the registered flux multiple.
- `topological_unification_merge_contract`: the combined merge contract.

The full Isabelle session builds cleanly with:

```powershell
D:\Isabelle2025\Isabelle2025-2\bin\isabelle build -D D:\TZPIDProof\tzpid_proof\isabelle_tzpid
```

## Consequence

No new registry IDs are required for these two candidates.  The correct publication-facing move is to cite them as strengthening evidence for the existing MHD/Elsasser and flux-quantization lanes.
