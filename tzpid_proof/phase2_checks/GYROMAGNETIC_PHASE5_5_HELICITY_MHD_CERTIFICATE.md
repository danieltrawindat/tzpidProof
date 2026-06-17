# Gyromagnetic Phase 5.5 Helicity/MHD Certificate

Generated: 2026-06-08

## Isabelle Layer

- Theory: `isabelle_tzpid/TZPID_GyromagneticMovement_MHD_Helicity.thy`
- Imports:
  - `TZPID_GyromagneticMovement_VectorCalculus`
  - `TZPID_Theorem_Semantic_Batch011_Magnetic_Torsion`
- Build command: `D:\Isabelle2025\Isabelle2025-2\bin\isabelle build -D .\isabelle_tzpid`
- Build status: `passed`
- Shortcut scan on new theory: no `by simp`, `sorry`, `oops`, or `admit`

## New Typed Semantics

- Vector dot product: `gm_dot3`
- Vector potential decomposition: `gm_vector_component_total`
- Helicity density: `gm_helicity_density`
- Uniform helicity integral: `gm_uniform_helicity_integral`
- Resistive helicity dissipation: `gm_resistive_helicity_dissipation`
- Ideal-MHD guard: `gm_ideal_mhd`
- Elsasser balance guard: `gm_mhd_elsasser_balance`
- Woltjer energy guard: `gm_woltjer_energy_guard`

## Locked Theorems

- `gm_helicity_density_zero_when_magnetic_field_zero`
- `gm_ideal_mhd_zero_resistive_helicity_dissipation`
- `gm_mhd_elsasser_balance_gives_unit_elsasser`
- `gm_woltjer_guard_nonnegative_residual`
- `gm_woltjer_guard_balanced_residual_zero`
- `phase5_5_helicity_mhd_lift_locked`

## Interpretation

This lift connects the Phase 5 exact-gradient curl bridge to the magnetic/torsion proof lane. It proves that ideal MHD zeroes the resistive helicity-dissipation term, Elsasser balance gives a unit Elsasser number, and a balanced Woltjer guard zeroes the helicity residual while preserving the Phase 5 curl and `Lz` witness contracts.
