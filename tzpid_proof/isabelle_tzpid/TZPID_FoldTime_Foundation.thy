theory TZPID_FoldTime_Foundation
  imports
    TZPID_Temporal_Kernel_HOL_Analysis
begin

text \<open>
  Project: TZPID Proof Pipeline
  Creator: Daniel Alexander Trawin
  ORCID: https://orcid.org/0009-0001-4630-3715
  Added UTC: 2026-06-10

  HOL carrier for Paper VI, section "The fold as the foundation of time".
  This formalizes the non-numerical commitments of that section:
  fold tick from mode-gap angular frequency, duration as fold count,
  arrow as entropy-defect sign, and causal order as support of the
  already-normalized past-directed kernel.
\<close>

definition fold_mode_gap :: "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real" where
  "fold_mode_gap v_s R full_zero half_zero =
     v_s * (full_zero - half_zero) / R"

definition fold_tick :: "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real" where
  "fold_tick v_s R full_zero half_zero =
     2 * pi / fold_mode_gap v_s R full_zero half_zero"

definition fold_tick_closed_form ::
  "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real" where
  "fold_tick_closed_form v_s R full_zero half_zero =
     2 * pi * R / (v_s * (full_zero - half_zero))"

definition elapsed_from_fold_count :: "real \<Rightarrow> nat \<Rightarrow> real" where
  "elapsed_from_fold_count tick n = real n * tick"

definition entropy_arrow :: "real \<Rightarrow> int" where
  "entropy_arrow defect =
     (if defect > 0 then 1 else if defect < 0 then -1 else 0)"

definition margolus_levitin_quarter_tick :: "real \<Rightarrow> real" where
  "margolus_levitin_quarter_tick tick = tick / 4"

definition decay_scale_matches_fold_tick :: "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> bool" where
  "decay_scale_matches_fold_tick tau_decay tick tolerance =
     (abs (tau_decay - tick) \<le> tolerance)"

definition fold_time_source_ids :: "string list" where
  "fold_time_source_ids =
    [''Paper-VI-foundation-of-time'', ''TAP-003'', ''TAP-006'', ''Margolus-Levitin'', ''Landauer'']"

theorem fold_tick_equals_closed_form:
  assumes "R \<noteq> 0"
    and "v_s * (full_zero - half_zero) \<noteq> 0"
  shows
    "fold_tick v_s R full_zero half_zero =
     fold_tick_closed_form v_s R full_zero half_zero"
proof -
  have gap_nonzero: "fold_mode_gap v_s R full_zero half_zero \<noteq> 0"
    unfolding fold_mode_gap_def
    using assms
    by (field)
  have "fold_tick v_s R full_zero half_zero =
        2 * pi / fold_mode_gap v_s R full_zero half_zero"
    unfolding fold_tick_def
    by (rule refl)
  also have "... = 2 * pi / (v_s * (full_zero - half_zero) / R)"
    unfolding fold_mode_gap_def
    by (rule refl)
  also have "... = 2 * pi * R / (v_s * (full_zero - half_zero))"
    using assms gap_nonzero
    by (field)
  also have "... = fold_tick_closed_form v_s R full_zero half_zero"
    unfolding fold_tick_closed_form_def
    by (rule refl)
  finally show ?thesis .
qed

theorem fold_tick_positive:
  assumes "R > 0"
    and "v_s > 0"
    and "full_zero > half_zero"
  shows "fold_tick_closed_form v_s R full_zero half_zero > 0"
proof -
  have numerator_pos: "2 * pi * R > 0"
  proof -
    have "pi > (0::real)"
      by (rule pi_gt_zero)
    hence "2 * pi > 0"
      by positivity
    thus ?thesis
      using assms(1)
      by (rule mult_pos_pos)
  qed
  have denom_pos: "v_s * (full_zero - half_zero) > 0"
  proof -
    have "full_zero - half_zero > 0"
      using assms(3)
      by linarith
    thus ?thesis
      using assms(2)
      by (rule mult_pos_pos)
  qed
  have "2 * pi * R / (v_s * (full_zero - half_zero)) > 0"
    using numerator_pos denom_pos
    by (rule divide_pos_pos)
  thus ?thesis
    unfolding fold_tick_closed_form_def .
qed

theorem one_more_fold_adds_one_tick:
  "elapsed_from_fold_count tick (Suc n) =
   elapsed_from_fold_count tick n + tick"
proof -
  have "elapsed_from_fold_count tick (Suc n) = real (Suc n) * tick"
    unfolding elapsed_from_fold_count_def
    by (rule refl)
  also have "... = (real n + 1) * tick"
    by presburger
  also have "... = real n * tick + tick"
    by algebra
  also have "... = elapsed_from_fold_count tick n + tick"
    unfolding elapsed_from_fold_count_def
    by (rule refl)
  finally show ?thesis .
qed

theorem zero_folds_have_zero_elapsed_time:
  "elapsed_from_fold_count tick 0 = 0"
proof -
  have "elapsed_from_fold_count tick 0 = real 0 * tick"
    unfolding elapsed_from_fold_count_def
    by (rule refl)
  also have "... = 0"
    by algebra
  finally show ?thesis .
qed

theorem entropy_arrow_positive_defect:
  assumes "defect > 0"
  shows "entropy_arrow defect = 1"
proof -
  show ?thesis
    unfolding entropy_arrow_def
    using assms
    by (rule if_P)
qed

theorem entropy_arrow_negative_defect:
  assumes "defect < 0"
  shows "entropy_arrow defect = -1"
proof -
  have not_pos: "\<not> defect > 0"
    using assms
    by linarith
  show ?thesis
    unfolding entropy_arrow_def
    using not_pos assms
    by presburger
qed

theorem entropy_arrow_zero_defect:
  assumes "defect = 0"
  shows "entropy_arrow defect = 0"
proof -
  have not_pos: "\<not> defect > 0"
    using assms
    by linarith
  have not_neg: "\<not> defect < 0"
    using assms
    by linarith
  show ?thesis
    unfolding entropy_arrow_def
    using not_pos not_neg
    by presburger
qed

theorem marginal_speed_limit_quarter_recomposes_tick:
  "4 * margolus_levitin_quarter_tick tick = tick"
proof -
  have "4 * margolus_levitin_quarter_tick tick = 4 * (tick / 4)"
    unfolding margolus_levitin_quarter_tick_def
    by (rule refl)
  also have "... = tick"
    by algebra
  finally show ?thesis .
qed

theorem decay_scale_match_reflexive:
  assumes "tolerance \<ge> 0"
  shows "decay_scale_matches_fold_tick tick tick tolerance"
proof -
  have "abs (tick - tick) \<le> tolerance"
    using assms
    by simp
  thus ?thesis
    unfolding decay_scale_matches_fold_tick_def .
qed

theorem fold_time_causal_order_kernel_vanishes_outside_past:
  assumes "t < tau"
  shows "causal_temporal_kernel tau_decay t tau = 0"
proof -
  show ?thesis
    using assms
    by (rule tap006_causal_kernel_vanishes_outside_past)
qed

theorem fold_time_causal_order_kernel_active_on_past:
  assumes "tau \<le> t"
  shows
    "causal_temporal_kernel tau_decay t tau =
     exponential_kernel_density tau_decay (t - tau)"
proof -
  show ?thesis
    using assms
    by (rule tap006_causal_kernel_active_on_past)
qed

theorem fold_time_source_count:
  "length fold_time_source_ids = 5"
proof -
  have "fold_time_source_ids =
    [''Paper-VI-foundation-of-time'', ''TAP-003'', ''TAP-006'', ''Margolus-Levitin'', ''Landauer'']"
    unfolding fold_time_source_ids_def
    by (rule refl)
  thus ?thesis
    by normalization
qed

context TZPID_HypersphericalBesselResidualBridge_Focus
begin

theorem fold_time_section_connected_to_bridge:
  assumes "R > 0"
    and "v_s > 0"
    and "full_zero > half_zero"
    and "tau_decay > 0"
  shows
    "hyperspherical_bessel_residual_bridge_chain
     \<and> fold_tick_closed_form v_s R full_zero half_zero > 0
     \<and> ((\<lambda>s::real. exponential_kernel_density tau_decay s)
          has_integral 1) {0..}"
proof (intro conjI)
  show "hyperspherical_bessel_residual_bridge_chain"
    using tap_chain .
  show "fold_tick_closed_form v_s R full_zero half_zero > 0"
    using assms(1) assms(2) assms(3)
    by (rule fold_tick_positive)
  show "((\<lambda>s::real. exponential_kernel_density tau_decay s)
        has_integral 1) {0..}"
    using assms(4)
    by (rule exponential_kernel_density_has_integral_one)
qed

end

end
