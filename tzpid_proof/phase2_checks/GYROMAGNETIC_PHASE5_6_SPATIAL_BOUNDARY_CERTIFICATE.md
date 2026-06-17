# Gyromagnetic Phase 5.6 Spatial Boundary Certificate

Generated: 2026-06-08

## Isabelle Layer

- Theory: `isabelle_tzpid/TZPID_GyromagneticMovement_SpatialBoundary.thy`
- Imports: `TZPID_GyromagneticMovement_MHD_Helicity`
- Build command: `D:\Isabelle2025\Isabelle2025-2\bin\isabelle build -D .\isabelle_tzpid`
- Build status: `passed`
- Shortcut scan on new theory: no `by simp`, `sorry`, `oops`, or `admit`

## New Typed Semantics

- Spatial domain record: `gm_spatial_domain`
- Positive domain guard: `gm_positive_domain`
- Spatial helicity integral: `gm_spatial_helicity_integral`
- Boundary flux: `gm_boundary_flux`
- Closed-boundary guard: `gm_closed_boundary`
- Helicity balance rate: `gm_helicity_balance_rate`
- Boundary admissibility: `gm_boundary_condition_admissible`

## Locked Theorems

- `spatial_helicity_integral_recovers_uniform_density`
- `ideal_closed_domain_zero_helicity_rate`
- `admissible_ideal_domain_conserves_helicity_rate`
- `phase5_6_spatial_boundary_lift_locked`

## Interpretation

Phase 5.6 lifts the helicity/MHD bridge into domain and boundary language. It proves that an admissible closed boundary has zero boundary flux, and that ideal MHD plus a closed boundary gives zero helicity balance rate. This is still a finite/uniform-domain HOL bridge, but it establishes the correct proof interface for the later full spatial/PDE layer.
