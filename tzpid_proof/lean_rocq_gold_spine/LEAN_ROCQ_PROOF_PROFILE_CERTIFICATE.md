# Lean/Rocq Proof Profile Certificate

Generated: 2026-06-11

## Result

Lean and Rocq have been added to the proof profile as secondary checked lanes.
The primary formal lane remains Isabelle/HOL.  Lean and Rocq are used here as
portability checks for the finite carrier shape of the spine/vector-calculus
contracts and as checks for the existing all-ID mirror.

## Toolchains

| Lane | Tool | Version / note |
| --- | --- | --- |
| Lean | `lean.exe` | Lean 4.28.0, x86_64-w64-windows-gnu |
| Rocq | `coqc.exe` | Rocq Prover 9.0.1, OCaml 4.14.2 |

For this local Rocq installation, the library path must be set explicitly:

```powershell
$env:ROCQLIB='D:\01Tools\Coq\Rocq-Platform~9.0~2025.08\lib\coq'
```

The default environment pointed `ROCQLIB` at `lib\rocq-core`, where
`Init/Prelude.vo` was not present.

## New Proof-Profile Artifacts

`D:\TZPIDProof\tzpid_proof\lean_rocq_gold_spine\TZPIDProofProfile.lean`

`D:\TZPIDProof\tzpid_proof\lean_rocq_gold_spine\TZPIDProofProfile.v`

Machine-readable result:

`D:\TZPIDProof\tzpid_proof\lean_rocq_gold_spine\LEAN_ROCQ_PROOF_PROFILE_RESULTS.json`

## Contracts Mirrored

The Lean and Rocq proof-profile files mirror the finite carrier contracts from
the Isabelle/HOL spine layer:

| Contract | Meaning |
| --- | --- |
| `spine_backbone_count` | The vector-calculus spine profile has eight layers. |
| `mixed_partials_zero_curl` | Equal mixed partials collapse planar curl. |
| `green_rectangle_constant_curl` | Rectangular boundary circulation equals constant-curl flux. |
| `incompressible_from_opposite_partials` | Opposite planar partials give divergence balance. |
| `helicity_density_zero_when_b_zero` | Helicity density closes when magnetic field is zero. |
| `uniform_helicity_integral_zero_density` | Uniform helicity integral closes when density is zero. |
| `elsasser_balance_consumed` | Elsasser balance is consumed as equality of forces. |
| `opposite_twist_torsion_zero` | Opposite twist cancels torsion carrier. |
| `flux_multiple_is_quantized` | Flux multiple satisfies the quantization carrier. |
| `quantized_circulation_is_winding_index` | Quantized circulation is mirrored as winding index. |
| `proof_profile_spine_count` | The proof profile records the eight-layer count. |
| `proof_profile_has_secondary_lanes` | The profile records Lean and Rocq lanes. |

## Commands Run

Lean profile:

```powershell
D:\01Tools\Lean\lean-4.28.0-windows\bin\lean.exe D:\TZPIDProof\tzpid_proof\lean_rocq_gold_spine\TZPIDProofProfile.lean
```

Result: `pass`

Rocq profile:

```powershell
$env:ROCQLIB='D:\01Tools\Coq\Rocq-Platform~9.0~2025.08\lib\coq'
D:\01Tools\Coq\Rocq-Platform~9.0~2025.08\bin\coqc.exe D:\TZPIDProof\tzpid_proof\lean_rocq_gold_spine\TZPIDProofProfile.v
```

Result: `pass`

Legacy all-ID Lean mirror:

```powershell
D:\01Tools\Lean\lean-4.28.0-windows\bin\lean.exe D:\TZPIDProof\tzpid_proof\lean_rocq_gold_spine\TZPIDAllIDs.lean
```

Result: `pass`

Legacy all-ID Rocq mirror:

```powershell
$env:ROCQLIB='D:\01Tools\Coq\Rocq-Platform~9.0~2025.08\lib\coq'
D:\01Tools\Coq\Rocq-Platform~9.0~2025.08\bin\coqc.exe D:\TZPIDProof\tzpid_proof\lean_rocq_gold_spine\TZPIDAllIDs.v
```

Result: `pass_with_warnings`

Warning: Rocq reports that large `nat` literals are interpreted via
`Nat.of_num_uint` to avoid stack overflow.  This is expected for the legacy
all-ID mirror and does not indicate a failed check.

## Interpretation

The proof profile now has:

1. Isabelle/HOL as the primary formal proof lane;
2. Lean as a checked secondary portability lane;
3. Rocq as a checked secondary portability lane;
4. Wolfram/Python/HDF5 as computational certificate lanes.

The Lean/Rocq files are intentionally not presented as full independent
first-principles physics proofs.  They are checked carrier-shape mirrors that
make the proof package more portable and easier to audit across proof
assistants.
