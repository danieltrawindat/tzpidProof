# Gyromagnetic Phase 6 Corrected Winding Certificate

Generated: 2026-06-08

Creator: Daniel Alexander Trawin  
ORCID: https://orcid.org/0009-0001-4630-3715

## Source Artifact

- HDF5: `delta_alpha_phase6_corrected_winding.h5`
- Project metadata: `TZPID Phase6 Corrected Winding Quantization`
- Method: `phase_unwrap_winding`
- Theory metadata: `Delta-alpha phase winding gives quantized circulation 2*pi*m`
- True winding: `m = 1`

## Numerical Values

| Quantity | Value |
|---|---:|
| loop radii | `0.2, 0.4, 0.6, 0.8` |
| circulation values | `6.283185307179586, 6.283185307179586, 6.283185307179587, 6.283185307179587` |
| expected circulation | `6.283185307179586` |
| max error | `8.881784197001252e-16` |
| winding estimates | `1.0, 1.0, 1.0000000000000002, 1.0000000000000002` |
| HOL tolerance | `1e-12` |

## Result

This is a **passing Phase 6 winding-quantization certificate**.

The corrected method replaces the failed smooth-gradient circulation check
with a phase-unwrapped winding calculation. Four enclosing loops recover
`2*pi` for `m = 1` to floating-point precision.

## Isabelle Layer

- Theory: `isabelle_tzpid/TZPID_GyromagneticMovement_CorrectedWinding.thy`
- Imports: `TZPID_GyromagneticMovement_CirculationDiagnostic`
- Status: positive winding lock

## HOL-Proved Claims

- `phase6_corrected_error_within_tolerance`
- `phase6_corrected_winding_estimates_near_one`
- `phase6_corrected_quantization_candidate_passes`
- `phase6_corrected_replaces_failed_gradient_candidate`
- `phase6_corrected_winding_quantization_locked`

## Interpretation

The previous artifact correctly failed because a smooth exact gradient on a
simply connected loop should not produce nonzero closed circulation. The
corrected artifact measures the topological phase winding instead. That is
the right object for quantization:

```text
wrapped phase winding m = 1
circulation = 2*pi*m
```

This locks Phase 6 as the topological movement bridge after the Phase 5
vector-calculus and Phase 5.5/5.6 helicity-boundary layers.

