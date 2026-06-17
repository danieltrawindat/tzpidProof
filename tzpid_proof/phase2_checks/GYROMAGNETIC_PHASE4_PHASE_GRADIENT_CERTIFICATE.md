# Gyromagnetic Phase 4 Phase-Gradient Certificate

Generated: 2026-06-08

## Source Artifact

- HDF5: `delta_alpha_phase4_bridge.h5`
- Summary: `phase2_checks/PHASE4_GYROMAGNETIC_BRIDGE_SUMMARY.md`
- Best shell-bearing observable: `field/psi_real`, slice `0`
- Mean absolute shell-radius error: `0.0010169215212778027`
- Max absolute shell-radius error: `0.001710663481156116`

## Isabelle Layer

- Theory: `isabelle_tzpid/TZPID_GyromagneticMovement_Typed_PhaseGradient.thy`
- Build command: `D:\Isabelle2025\Isabelle2025-2\bin\isabelle build -D .\isabelle_tzpid`
- Build status: `passed`
- Shortcut scan on new theory: no `by simp`, `sorry`, `oops`, or `admit`

## Locked Theorems

- `gm_delta_alpha_is_linear_phase_driver`
- `nonzero_phase_source_generates_nonzero_Lz_witness`
- `gyromagnetic_ratio_recovers_angular_momentum`
- `phase4_bessel_to_gyromagnetic_movement_pin`

## Interpretation

The Phase 4 bridge keeps the Bessel drop contract as the radial phase-gradient driver, then proves that a nonzero phase gradient, nonzero source offset, and nonzero coupling generate a nonzero angular-momentum witness. The `Lz` dataset in the HDF5 file is effectively constant, so it is recorded as a gyromagnetic correspondence witness rather than as the shell-bearing radial observable.
