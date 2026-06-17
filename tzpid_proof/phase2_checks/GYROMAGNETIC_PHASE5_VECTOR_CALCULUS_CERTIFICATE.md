# Gyromagnetic Phase 5 Vector-Calculus Certificate

Generated: 2026-06-08

## Source Artifact

- HDF5: `delta_alpha_phase5_vector_calculus.h5`
- Summary: `phase2_checks/PHASE5_VECTOR_CALCULUS_BRIDGE_SUMMARY.md`
- Delta: `0.18010602113350746`
- Curl max absolute value: `1.7713830402499298e-11`
- `psi_real^2 + psi_imag^2 = 1` max absolute error: `2.220446049250313e-16`
- `Lz` standard deviation: `2.317575256303825e-13`

## Isabelle Layer

- Theory: `isabelle_tzpid/TZPID_GyromagneticMovement_VectorCalculus.thy`
- Build command: `D:\Isabelle2025\Isabelle2025-2\bin\isabelle build -D .\isabelle_tzpid`
- Build status: `passed`
- Shortcut scan on new theory: no `by simp`, `sorry`, `oops`, or `admit`

## Locked Theorems

- `exact_gradient_curl_cancels`
- `active_phase_vector_has_nonzero_component`
- `active_phase_vector_can_drive_Lz_witness`
- `phase5_vector_calculus_bridge_locked`

## Interpretation

Phase 5 upgrades the gyromagnetic bridge from scalar phase-gradient algebra into vector-calculus semantics. The exact-gradient curl identity is proved in HOL, and the HDF5 artifact supplies the numerical certificate that `curl_z` remains near zero to floating-point tolerance while the phase vector remains active.
