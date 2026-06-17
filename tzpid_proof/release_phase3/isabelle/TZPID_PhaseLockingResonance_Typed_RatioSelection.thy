theory TZPID_PhaseLockingResonance_Typed_RatioSelection
  imports
    TZPID_PhaseLockingResonance_Computational_Checks
    TZPID_Theorem_Semantic_Batch018_Resonance_Locking_Followup
begin

text \<open>
  Project: TZPID Proof Pipeline
  Creator: Daniel Alexander Trawin
  ORCID: https://orcid.org/0009-0001-4630-3715
  Generated UTC: 2026-06-08T00:00:00Z

  Phase-locking/orbital-resonance lift.  This file promotes the resonance
  spine from abstract selectors into typed ratio-selection algebra:
  detuning threshold, rational spin-orbit ratios, harmonic cavity ratios,
  reciprocal flips, and beat-window spacing.
\<close>

definition pl_detuning :: "real \<Rightarrow> real \<Rightarrow> real" where
  "pl_detuning drive_frequency oscillator_frequency =
    drive_frequency - oscillator_frequency"

definition pl_lock_admissible :: "real \<Rightarrow> real \<Rightarrow> bool" where
  "pl_lock_admissible coupling detuning \<longleftrightarrow> abs detuning \<le> coupling"

definition pl_phase_velocity_residual :: "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real" where
  "pl_phase_velocity_residual coupling phase_lag detuning =
    coupling * phase_lag - detuning"

definition pl_rational_ratio :: "real \<Rightarrow> real \<Rightarrow> real" where
  "pl_rational_ratio numerator denominator = numerator / denominator"

definition pl_reciprocal_ratio :: "real \<Rightarrow> real" where
  "pl_reciprocal_ratio ratio = 1 / ratio"

definition pl_harmonic_frequency :: "real \<Rightarrow> real \<Rightarrow> real" where
  "pl_harmonic_frequency n fundamental = n * fundamental"

definition pl_beat_window :: "nat \<Rightarrow> real \<Rightarrow> real" where
  "pl_beat_window n delta_f = real n / (2 * delta_f)"

definition pl_ratio_selector_locked :: "real \<Rightarrow> real \<Rightarrow> bool" where
  "pl_ratio_selector_locked coupling detuning \<longleftrightarrow>
    pl_lock_admissible coupling detuning \<and> 0 \<le> coupling"

lemma lock_admissible_from_threshold:
  assumes "abs detuning \<le> coupling"
  shows "pl_lock_admissible coupling detuning"
  unfolding pl_lock_admissible_def
  using assms
  by blast

lemma lock_witness_zeroes_linear_phase_residual:
  assumes "coupling \<noteq> 0"
  defines "phase_lag \<equiv> detuning / coupling"
  shows "pl_phase_velocity_residual coupling phase_lag detuning = 0"
  unfolding pl_phase_velocity_residual_def phase_lag_def
  using assms(1)
  by field

lemma admissible_lock_witness_bounded:
  assumes "pl_lock_admissible coupling detuning"
    and "0 < coupling"
  shows "abs (detuning / coupling) \<le> 1"
proof -
  have bound: "abs detuning \<le> coupling"
    using assms(1)
    unfolding pl_lock_admissible_def
    by blast
  have "abs (detuning / coupling) = abs detuning / coupling"
    using assms(2)
    by (metis abs_divide abs_of_pos)
  also have "... \<le> coupling / coupling"
    using bound assms(2)
    by (metis divide_right_mono)
  also have "... = 1"
    using assms(2)
    by field
  finally show ?thesis .
qed

lemma spin_orbit_three_two_ratio:
  "pl_rational_ratio 3 2 = 3 / 2"
  unfolding pl_rational_ratio_def
  by (rule refl)

lemma spin_orbit_three_two_reciprocal:
  "pl_reciprocal_ratio (pl_rational_ratio 3 2) = 2 / 3"
  unfolding pl_reciprocal_ratio_def pl_rational_ratio_def
  by norm_num

lemma cavity_harmonic_two_one_ratio:
  assumes "fundamental \<noteq> 0"
  shows "pl_harmonic_frequency 2 fundamental /
    pl_harmonic_frequency 1 fundamental = 2"
  unfolding pl_harmonic_frequency_def
  using assms
  by field

lemma bridge_ratio_exact_reciprocal:
  "pl_reciprocal_ratio (32 / 27) = 27 / 32"
  unfolding pl_reciprocal_ratio_def
  by norm_num

lemma reciprocal_flip_involutive:
  assumes "ratio \<noteq> 0"
  shows "pl_reciprocal_ratio (pl_reciprocal_ratio ratio) = ratio"
  unfolding pl_reciprocal_ratio_def
  using assms
  by field

lemma beat_window_spacing:
  assumes "delta_f \<noteq> 0"
  shows "pl_beat_window (Suc n) delta_f - pl_beat_window n delta_f =
    1 / (2 * delta_f)"
proof -
  have nonzero: "2 * delta_f \<noteq> 0"
    using assms
    by algebra
  show ?thesis
    unfolding pl_beat_window_def
    using nonzero
    by field
qed

theorem phase_locking_orbital_ratio_selection_locked:
  assumes "abs detuning \<le> coupling"
    and "0 < coupling"
    and "fundamental \<noteq> 0"
    and "delta_f \<noteq> 0"
  defines "phase_lag \<equiv> detuning / coupling"
  shows "pl_lock_admissible coupling detuning
    \<and> abs phase_lag \<le> 1
    \<and> pl_phase_velocity_residual coupling phase_lag detuning = 0
    \<and> pl_rational_ratio 3 2 = 3 / 2
    \<and> pl_reciprocal_ratio (pl_rational_ratio 3 2) = 2 / 3
    \<and> pl_harmonic_frequency 2 fundamental /
        pl_harmonic_frequency 1 fundamental = 2
    \<and> pl_reciprocal_ratio (32 / 27) = 27 / 32
    \<and> pl_beat_window (Suc n) delta_f - pl_beat_window n delta_f =
        1 / (2 * delta_f)"
proof -
  have lock: "pl_lock_admissible coupling detuning"
    using assms(1) lock_admissible_from_threshold
    by blast
  have bounded: "abs phase_lag \<le> 1"
    unfolding phase_lag_def
    using lock assms(2) admissible_lock_witness_bounded
    by blast
  have residual: "pl_phase_velocity_residual coupling phase_lag detuning = 0"
    unfolding phase_lag_def
    using assms(2) lock_witness_zeroes_linear_phase_residual
    by fastforce
  have ratio32: "pl_rational_ratio 3 2 = 3 / 2"
    using spin_orbit_three_two_ratio
    by blast
  have recip32: "pl_reciprocal_ratio (pl_rational_ratio 3 2) = 2 / 3"
    using spin_orbit_three_two_reciprocal
    by blast
  have harmonic:
    "pl_harmonic_frequency 2 fundamental /
      pl_harmonic_frequency 1 fundamental = 2"
    using assms(3) cavity_harmonic_two_one_ratio
    by blast
  have bridge: "pl_reciprocal_ratio (32 / 27) = 27 / 32"
    using bridge_ratio_exact_reciprocal
    by blast
  have beat:
    "pl_beat_window (Suc n) delta_f - pl_beat_window n delta_f =
      1 / (2 * delta_f)"
    using assms(4) beat_window_spacing
    by blast
  show ?thesis
    using lock bounded residual ratio32 recip32 harmonic bridge beat
    by blast
qed

end
