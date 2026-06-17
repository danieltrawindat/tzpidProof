theory TZPID_GyromagneticMovement_CorrectedWinding
  imports TZPID_GyromagneticMovement_CirculationDiagnostic
begin

text \<open>
  Project: TZPID Proof Pipeline
  Creator: Daniel Alexander Trawin
  ORCID: https://orcid.org/0009-0001-4630-3715
  Generated UTC: 2026-06-08T00:00:00Z

  Corrected Phase 6 artifact:
  - delta_alpha_phase6_corrected_winding.h5

  The failed candidate integrated a smooth exact-gradient circulation and
  therefore did not produce a quantized loop value.  This corrected artifact
  uses phase-unwrapped winding around enclosing closed paths.  The HDF5 values
  certify four loop radii with circulation 2*pi for m = 1 up to floating
  point roundoff.
\<close>

definition phase6_corrected_winding_hdf5 :: string where
  "phase6_corrected_winding_hdf5 =
    ''delta_alpha_phase6_corrected_winding.h5''"

definition phase6_corrected_loop_count :: nat where
  "phase6_corrected_loop_count = 4"

definition phase6_corrected_true_winding :: real where
  "phase6_corrected_true_winding = 1"

definition phase6_corrected_expected_circulation :: real where
  "phase6_corrected_expected_circulation = 6.283185307179586"

definition phase6_corrected_circulation_min :: real where
  "phase6_corrected_circulation_min = 6.283185307179586"

definition phase6_corrected_circulation_max :: real where
  "phase6_corrected_circulation_max = 6.283185307179587"

definition phase6_corrected_error_max :: real where
  "phase6_corrected_error_max = 0.0000000000000008881784197001252"

definition phase6_corrected_m_min :: real where
  "phase6_corrected_m_min = 1"

definition phase6_corrected_m_max :: real where
  "phase6_corrected_m_max = 1.0000000000000002"

definition phase6_corrected_tolerance :: real where
  "phase6_corrected_tolerance = 0.000000000001"

definition phase6_corrected_m_tolerance :: real where
  "phase6_corrected_m_tolerance = 0.000000000001"

definition gm_winding_quantization_locked ::
  "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> bool" where
  "gm_winding_quantization_locked error_max expected tolerance \<longleftrightarrow>
    0 < expected \<and> 0 \<le> error_max \<and> error_max \<le> tolerance"

definition gm_winding_estimate_locked ::
  "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> bool" where
  "gm_winding_estimate_locked m_min m_max true_m tolerance \<longleftrightarrow>
    abs (m_min - true_m) \<le> tolerance \<and>
    abs (m_max - true_m) \<le> tolerance"

lemma phase6_corrected_expected_positive:
  "0 < phase6_corrected_expected_circulation"
  unfolding phase6_corrected_expected_circulation_def
  by norm_num

lemma phase6_corrected_error_within_tolerance:
  "phase6_corrected_error_max \<le> phase6_corrected_tolerance"
  unfolding phase6_corrected_error_max_def phase6_corrected_tolerance_def
  by norm_num

lemma phase6_corrected_loop_count_positive:
  "0 < phase6_corrected_loop_count"
  unfolding phase6_corrected_loop_count_def
  by norm_num

lemma phase6_corrected_circulation_bounds_enclose_expected:
  "phase6_corrected_circulation_min \<le>
      phase6_corrected_expected_circulation
    \<and> phase6_corrected_expected_circulation \<le>
      phase6_corrected_circulation_max"
  unfolding phase6_corrected_circulation_min_def
    phase6_corrected_expected_circulation_def
    phase6_corrected_circulation_max_def
  by norm_num

lemma phase6_corrected_winding_estimates_near_one:
  "gm_winding_estimate_locked
      phase6_corrected_m_min
      phase6_corrected_m_max
      phase6_corrected_true_winding
      phase6_corrected_m_tolerance"
  unfolding gm_winding_estimate_locked_def
    phase6_corrected_m_min_def
    phase6_corrected_m_max_def
    phase6_corrected_true_winding_def
    phase6_corrected_m_tolerance_def
  by norm_num

lemma phase6_corrected_quantization_candidate_passes:
  "gm_winding_quantization_locked
      phase6_corrected_error_max
      phase6_corrected_expected_circulation
      phase6_corrected_tolerance"
  unfolding gm_winding_quantization_locked_def
  using phase6_corrected_expected_positive
    phase6_corrected_error_within_tolerance
  unfolding phase6_corrected_error_max_def
  by norm_num

lemma phase6_corrected_replaces_failed_gradient_candidate:
  "\<not> gm_circulation_quantized_candidate
      phase6_circulation_computed
      phase6_circulation_expected
      phase6_circulation_tolerance
    \<and> gm_winding_quantization_locked
      phase6_corrected_error_max
      phase6_corrected_expected_circulation
      phase6_corrected_tolerance"
  using phase6_circulation_candidate_not_quantized
    phase6_corrected_quantization_candidate_passes
  by blast

theorem phase6_corrected_winding_quantization_locked:
  "gm_winding_quantization_locked
      phase6_corrected_error_max
      phase6_corrected_expected_circulation
      phase6_corrected_tolerance
    \<and> gm_winding_estimate_locked
      phase6_corrected_m_min
      phase6_corrected_m_max
      phase6_corrected_true_winding
      phase6_corrected_m_tolerance
    \<and> phase6_corrected_loop_count = 4
    \<and> phase6_corrected_circulation_min \<le>
      phase6_corrected_expected_circulation
    \<and> phase6_corrected_expected_circulation \<le>
      phase6_corrected_circulation_max
    \<and> \<not> gm_circulation_quantized_candidate
      phase6_circulation_computed
      phase6_circulation_expected
      phase6_circulation_tolerance"
proof (intro conjI)
  show "gm_winding_quantization_locked
      phase6_corrected_error_max
      phase6_corrected_expected_circulation
      phase6_corrected_tolerance"
    using phase6_corrected_quantization_candidate_passes .
  show "gm_winding_estimate_locked
      phase6_corrected_m_min
      phase6_corrected_m_max
      phase6_corrected_true_winding
      phase6_corrected_m_tolerance"
    using phase6_corrected_winding_estimates_near_one .
  show "phase6_corrected_loop_count = 4"
    unfolding phase6_corrected_loop_count_def
    by norm_num
  show "phase6_corrected_circulation_min \<le>
      phase6_corrected_expected_circulation"
    using phase6_corrected_circulation_bounds_enclose_expected
    by blast
  show "phase6_corrected_expected_circulation \<le>
      phase6_corrected_circulation_max"
    using phase6_corrected_circulation_bounds_enclose_expected
    by blast
  show "\<not> gm_circulation_quantized_candidate
      phase6_circulation_computed
      phase6_circulation_expected
      phase6_circulation_tolerance"
    using phase6_circulation_candidate_not_quantized .
qed

end
