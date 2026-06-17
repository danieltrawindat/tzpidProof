# Phase Locking / Orbital Ratio Selection Certificate

Generated: 2026-06-08

## Isabelle Layer

- Theory: `isabelle_tzpid/TZPID_PhaseLockingResonance_Typed_RatioSelection.thy`
- Imports:
  - `TZPID_PhaseLockingResonance_Computational_Checks`
  - `TZPID_Theorem_Semantic_Batch018_Resonance_Locking_Followup`
- Build command: `D:\Isabelle2025\Isabelle2025-2\bin\isabelle build -D .\isabelle_tzpid`
- Build status: `passed`
- Shortcut scan on new theory: no `by simp`, `sorry`, `oops`, or `admit`

## New Typed Semantics

- Detuning: `pl_detuning`
- Lock admissibility: `pl_lock_admissible`
- Phase velocity residual: `pl_phase_velocity_residual`
- Rational ratio: `pl_rational_ratio`
- Reciprocal ratio: `pl_reciprocal_ratio`
- Harmonic frequency: `pl_harmonic_frequency`
- Beat window: `pl_beat_window`
- Ratio selector guard: `pl_ratio_selector_locked`

## Locked Theorems

- `lock_witness_zeroes_linear_phase_residual`
- `admissible_lock_witness_bounded`
- `spin_orbit_three_two_reciprocal`
- `cavity_harmonic_two_one_ratio`
- `bridge_ratio_exact_reciprocal`
- `reciprocal_flip_involutive`
- `beat_window_spacing`
- `phase_locking_orbital_ratio_selection_locked`

## Interpretation

This layer formalizes the ratio-selection mechanism between gyromagnetic movement and orbital/cavity resonance. A detuning threshold gives an admissible lock witness, 3:2 spin-orbit resonance has exact reciprocal 2:3, the 2:1 harmonic cavity ratio is recovered from the frequency ladder, the 32/27 bridge ratio has reciprocal 27/32, and beat windows have uniform spacing.
