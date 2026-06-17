# Gyromagnetic Phase 6 Circulation Diagnostic Certificate

Generated: 2026-06-08

Creator: Daniel Alexander Trawin  
ORCID: https://orcid.org/0009-0001-4630-3715

## Source Artifact

- HDF5: `delta_alpha_phase6_circulation.h5`
- Project metadata: `TZPID Phase6 Circulation Quantization`
- Claimed check: `integral grad(Delta-alpha) dot dl = 2*pi*m`
- Stored mode: `m = 1`

## Stored Numerical Values

| Quantity | Value |
|---|---:|
| computed circulation | `0.14419341536347438` |
| expected circulation | `6.283185307179586` |
| stored error | `6.1389918918161115` |
| tolerance used by HOL diagnostic | `0.000001` |

## Result

This is **not yet a passing circulation-quantization certificate**.

The current artifact is far below the expected `2*pi` value for `m = 1`,
and its error exceeds the tolerance by several orders of magnitude.

## Isabelle Layer

- Theory: `isabelle_tzpid/TZPID_GyromagneticMovement_CirculationDiagnostic.thy`
- Status: diagnostic lock, not positive proof lock

## HOL-Proved Diagnostic Claims

- `phase6_circulation_computed < phase6_circulation_expected`
- `phase6_circulation_tolerance < phase6_circulation_error`
- `phase6_circulation_candidate_not_quantized`
- `phase6_circulation_diagnostic_locked`

## Interpretation

Phase 6 is the correct next conceptual direction: circulation should be the
topological lift after the vector-calculus and helicity layers. However, this
specific HDF5 file does not yet certify `2*pi*m` quantization. It should be
treated as a failed candidate / diagnostic artifact.

The likely next repair is to recompute the circulation around a loop that
encloses the phase singularity or winding core. For a globally exact smooth
gradient field on a simply connected region, closed-loop circulation should
cancel; quantized nonzero circulation requires the loop to enclose a branch
cut, vortex core, or explicitly wrapped phase.

