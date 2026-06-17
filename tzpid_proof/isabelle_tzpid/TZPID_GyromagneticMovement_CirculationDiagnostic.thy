theory TZPID_GyromagneticMovement_CirculationDiagnostic
  imports TZPID_GyromagneticMovement_SpatialBoundary
begin

text \<open>
  Project: TZPID Proof Pipeline
  Creator: Daniel Alexander Trawin
  ORCID: https://orcid.org/0009-0001-4630-3715
  Generated UTC: 2026-06-08T00:00:00Z

  Phase 6 candidate artifact:
  - delta_alpha_phase6_circulation.h5

  The HDF5 metadata describes a circulation-quantization check for
  integral grad(Delta-alpha) dot dl = 2*pi*m with m = 1.  The stored
  numerical values do not yet satisfy that contract:

    computed = 0.14419341536347438
    expected = 6.283185307179586
    error    = 6.1389918918161115

  This file intentionally records the candidate as a diagnostic, not as a
  locked proof certificate.  The earlier Phase 5/5.5/5.6 gyromagnetic
  vector-calculus, helicity, and spatial-boundary layers remain valid.
\<close>

definition phase6_circulation_hdf5 :: string where
  "phase6_circulation_hdf5 = ''delta_alpha_phase6_circulation.h5''"

definition phase6_circulation_mode_m :: nat where
  "phase6_circulation_mode_m = 1"

definition phase6_circulation_computed :: real where
  "phase6_circulation_computed = 0.14419341536347438"

definition phase6_circulation_expected :: real where
  "phase6_circulation_expected = 6.283185307179586"

definition phase6_circulation_error :: real where
  "phase6_circulation_error = 6.1389918918161115"

definition phase6_circulation_tolerance :: real where
  "phase6_circulation_tolerance = 0.000001"

definition gm_circulation_quantized_candidate :: "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> bool" where
  "gm_circulation_quantized_candidate computed expected tolerance \<longleftrightarrow>
    abs (computed - expected) \<le> tolerance"

lemma phase6_circulation_expected_positive:
  "0 < phase6_circulation_expected"
  unfolding phase6_circulation_expected_def
  by norm_num

lemma phase6_circulation_computed_positive:
  "0 < phase6_circulation_computed"
  unfolding phase6_circulation_computed_def
  by norm_num

lemma phase6_circulation_error_large:
  "1 < phase6_circulation_error"
  unfolding phase6_circulation_error_def
  by norm_num

lemma phase6_circulation_error_exceeds_tolerance:
  "phase6_circulation_tolerance < phase6_circulation_error"
  unfolding phase6_circulation_tolerance_def phase6_circulation_error_def
  by norm_num

lemma phase6_circulation_computed_below_expected:
  "phase6_circulation_computed < phase6_circulation_expected"
  unfolding phase6_circulation_computed_def phase6_circulation_expected_def
  by norm_num

lemma phase6_circulation_candidate_not_quantized:
  "\<not> gm_circulation_quantized_candidate
      phase6_circulation_computed
      phase6_circulation_expected
      phase6_circulation_tolerance"
proof -
  have diff_large:
    "phase6_circulation_tolerance <
      abs (phase6_circulation_computed - phase6_circulation_expected)"
    unfolding phase6_circulation_tolerance_def
      phase6_circulation_computed_def
      phase6_circulation_expected_def
    by norm_num
  show ?thesis
    unfolding gm_circulation_quantized_candidate_def
    using diff_large
    by linarith
qed

theorem phase6_circulation_diagnostic_locked:
  "\<not> gm_circulation_quantized_candidate
      phase6_circulation_computed
      phase6_circulation_expected
      phase6_circulation_tolerance
    \<and> phase6_circulation_computed < phase6_circulation_expected
    \<and> phase6_circulation_tolerance < phase6_circulation_error
    \<and> gm_closed_boundary_zero_flux 0"
proof (intro conjI)
  show "\<not> gm_circulation_quantized_candidate
      phase6_circulation_computed
      phase6_circulation_expected
      phase6_circulation_tolerance"
    using phase6_circulation_candidate_not_quantized .
  show "phase6_circulation_computed < phase6_circulation_expected"
    using phase6_circulation_computed_below_expected .
  show "phase6_circulation_tolerance < phase6_circulation_error"
    using phase6_circulation_error_exceeds_tolerance .
  show "gm_closed_boundary_zero_flux 0"
    using gm_closed_boundary_zero_flux_zero .
qed

end
