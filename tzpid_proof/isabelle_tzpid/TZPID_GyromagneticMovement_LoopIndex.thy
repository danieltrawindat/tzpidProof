theory TZPID_GyromagneticMovement_LoopIndex
  imports TZPID_GyromagneticMovement_CorrectedWinding
begin

text \<open>
  Project: TZPID Proof Pipeline
  Creator: Daniel Alexander Trawin
  ORCID: https://orcid.org/0009-0001-4630-3715
  Generated UTC: 2026-06-09T00:00:00Z

  Reusable Phase 6+ gyromagnetic movement layer.

  The corrected Phase 6 HDF5 artifact certifies four enclosing loops with
  circulation approximately 2*pi and winding m = 1.  This file lifts that
  artifact-specific fact into a general loop-index contract for wrapped phase
  fields: if a loop circulation is within tolerance of k times the circulation
  quantum, then the normalized winding estimate is within tolerance/quantum of
  the integer index k.
\<close>

definition gm_loop_index_error ::
  "real \<Rightarrow> int \<Rightarrow> real \<Rightarrow> real" where
  "gm_loop_index_error circulation k quantum =
    abs (circulation - real_of_int k * quantum)"

definition gm_loop_index_locked ::
  "real \<Rightarrow> int \<Rightarrow> real \<Rightarrow> real \<Rightarrow> bool" where
  "gm_loop_index_locked circulation k quantum tolerance \<longleftrightarrow>
    0 < quantum
    \<and> 0 \<le> tolerance
    \<and> gm_loop_index_error circulation k quantum \<le> tolerance"

definition gm_normalized_winding ::
  "real \<Rightarrow> real \<Rightarrow> real" where
  "gm_normalized_winding circulation quantum = circulation / quantum"

definition gm_winding_index_error ::
  "real \<Rightarrow> int \<Rightarrow> real \<Rightarrow> real" where
  "gm_winding_index_error circulation k quantum =
    abs (gm_normalized_winding circulation quantum - real_of_int k)"

lemma gm_loop_index_quantum_positive:
  assumes "gm_loop_index_locked circulation k quantum tolerance"
  shows "0 < quantum"
  using assms
  unfolding gm_loop_index_locked_def
  by blast

lemma gm_loop_index_tolerance_nonnegative:
  assumes "gm_loop_index_locked circulation k quantum tolerance"
  shows "0 \<le> tolerance"
  using assms
  unfolding gm_loop_index_locked_def
  by blast

lemma gm_loop_index_error_within_tolerance:
  assumes "gm_loop_index_locked circulation k quantum tolerance"
  shows "gm_loop_index_error circulation k quantum \<le> tolerance"
  using assms
  unfolding gm_loop_index_locked_def
  by blast

lemma gm_loop_index_error_scales_to_winding_error:
  assumes locked: "gm_loop_index_locked circulation k quantum tolerance"
  shows "gm_winding_index_error circulation k quantum \<le> tolerance / quantum"
proof -
  have quantum_pos: "0 < quantum"
    using locked
    by (rule gm_loop_index_quantum_positive)
  have error_bound:
    "abs (circulation - real_of_int k * quantum) \<le> tolerance"
    using locked
    unfolding gm_loop_index_locked_def gm_loop_index_error_def
    by blast
  have divide_bound:
    "abs (circulation - real_of_int k * quantum) / quantum \<le>
      tolerance / quantum"
    using error_bound quantum_pos
    by (metis divide_right_mono less_eq_real_def)
  have winding_identity:
    "gm_winding_index_error circulation k quantum =
      abs (circulation - real_of_int k * quantum) / quantum"
  proof -
    have "circulation / quantum - real_of_int k =
        (circulation - real_of_int k * quantum) / quantum"
      using quantum_pos
      by field
    then have "abs (circulation / quantum - real_of_int k) =
        abs ((circulation - real_of_int k * quantum) / quantum)"
      by presburger
    then have "abs (circulation / quantum - real_of_int k) =
        abs (circulation - real_of_int k * quantum) / abs quantum"
      by (metis abs_divide)
    then have "abs (circulation / quantum - real_of_int k) =
        abs (circulation - real_of_int k * quantum) / quantum"
      using quantum_pos
      by (metis abs_of_pos)
    then show ?thesis
      unfolding gm_winding_index_error_def gm_normalized_winding_def
      by blast
  qed
  show ?thesis
    using winding_identity divide_bound
    by linarith
qed

theorem gm_reusable_loop_index_theorem:
  assumes "gm_loop_index_locked circulation k quantum tolerance"
  shows "0 < quantum
    \<and> 0 \<le> tolerance
    \<and> gm_loop_index_error circulation k quantum \<le> tolerance
    \<and> gm_winding_index_error circulation k quantum \<le> tolerance / quantum"
proof (intro conjI)
  show "0 < quantum"
    using assms
    by (rule gm_loop_index_quantum_positive)
  show "0 \<le> tolerance"
    using assms
    by (rule gm_loop_index_tolerance_nonnegative)
  show "gm_loop_index_error circulation k quantum \<le> tolerance"
    using assms
    by (rule gm_loop_index_error_within_tolerance)
  show "gm_winding_index_error circulation k quantum \<le> tolerance / quantum"
    using assms
    by (rule gm_loop_index_error_scales_to_winding_error)
qed

lemma phase6_corrected_min_loop_index_locked:
  "gm_loop_index_locked
    phase6_corrected_circulation_min
    1
    phase6_corrected_expected_circulation
    phase6_corrected_tolerance"
  unfolding gm_loop_index_locked_def gm_loop_index_error_def
    phase6_corrected_circulation_min_def
    phase6_corrected_expected_circulation_def
    phase6_corrected_tolerance_def
  by norm_num

lemma phase6_corrected_max_loop_index_locked:
  "gm_loop_index_locked
    phase6_corrected_circulation_max
    1
    phase6_corrected_expected_circulation
    phase6_corrected_tolerance"
  unfolding gm_loop_index_locked_def gm_loop_index_error_def
    phase6_corrected_circulation_max_def
    phase6_corrected_expected_circulation_def
    phase6_corrected_tolerance_def
  by norm_num

theorem phase6_corrected_loop_index_layer_locked:
  "gm_loop_index_locked
      phase6_corrected_circulation_min
      1
      phase6_corrected_expected_circulation
      phase6_corrected_tolerance
    \<and> gm_loop_index_locked
      phase6_corrected_circulation_max
      1
      phase6_corrected_expected_circulation
      phase6_corrected_tolerance
    \<and> gm_winding_index_error
      phase6_corrected_circulation_max
      1
      phase6_corrected_expected_circulation
      \<le> phase6_corrected_tolerance /
        phase6_corrected_expected_circulation
    \<and> phase6_corrected_loop_count = 4"
proof (intro conjI)
  show "gm_loop_index_locked
      phase6_corrected_circulation_min
      1
      phase6_corrected_expected_circulation
      phase6_corrected_tolerance"
    by (rule phase6_corrected_min_loop_index_locked)
  show "gm_loop_index_locked
      phase6_corrected_circulation_max
      1
      phase6_corrected_expected_circulation
      phase6_corrected_tolerance"
    by (rule phase6_corrected_max_loop_index_locked)
  show "gm_winding_index_error
      phase6_corrected_circulation_max
      1
      phase6_corrected_expected_circulation
      \<le> phase6_corrected_tolerance /
        phase6_corrected_expected_circulation"
    using phase6_corrected_max_loop_index_locked
    by (rule gm_loop_index_error_scales_to_winding_error)
  show "phase6_corrected_loop_count = 4"
    unfolding phase6_corrected_loop_count_def
    by norm_num
qed

end
