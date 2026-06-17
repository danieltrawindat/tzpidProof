theory TZPID_PhaseLockingResonance_CaptureBasin
  imports TZPID_PhaseLockingResonance_Typed_RatioSelection
begin

text \<open>
  Project: TZPID Proof Pipeline
  Creator: Daniel Alexander Trawin
  ORCID: https://orcid.org/0009-0001-4630-3715
  Generated UTC: 2026-06-09T00:00:00Z

  Phase-locking capture-basin upgrade.

  This layer strengthens the ratio-selection spine with coupled-oscillator
  threshold semantics.  For coupling K and detuning Delta, the capture basin is
  the interval |Delta| <= K.  Inside that basin the linearized phase witness
  Delta/K is bounded and zeroes the phase-velocity residual already defined in
  the typed ratio-selection layer.
\<close>

definition pl_capture_margin :: "real \<Rightarrow> real \<Rightarrow> real" where
  "pl_capture_margin coupling detuning = coupling - abs detuning"

definition pl_capture_basin :: "real \<Rightarrow> real \<Rightarrow> bool" where
  "pl_capture_basin coupling detuning \<longleftrightarrow>
    0 < coupling \<and> 0 \<le> pl_capture_margin coupling detuning"

definition pl_capture_basin_width :: "real \<Rightarrow> real" where
  "pl_capture_basin_width coupling = 2 * coupling"

definition pl_locking_phase_witness :: "real \<Rightarrow> real \<Rightarrow> real" where
  "pl_locking_phase_witness coupling detuning = detuning / coupling"

definition pl_capture_contract :: "real \<Rightarrow> real \<Rightarrow> bool" where
  "pl_capture_contract coupling detuning \<longleftrightarrow>
    pl_capture_basin coupling detuning
    \<and> abs (pl_locking_phase_witness coupling detuning) \<le> 1
    \<and> pl_phase_velocity_residual coupling
        (pl_locking_phase_witness coupling detuning)
        detuning = 0"

lemma pl_capture_margin_nonnegative_from_threshold:
  assumes "abs detuning \<le> coupling"
  shows "0 \<le> pl_capture_margin coupling detuning"
proof -
  show ?thesis
    using assms
    unfolding pl_capture_margin_def
    by linarith
qed

lemma pl_capture_basin_from_threshold:
  assumes "0 < coupling"
    and "abs detuning \<le> coupling"
  shows "pl_capture_basin coupling detuning"
proof -
  have margin: "0 \<le> pl_capture_margin coupling detuning"
    using assms(2)
    by (rule pl_capture_margin_nonnegative_from_threshold)
  show ?thesis
    unfolding pl_capture_basin_def
    using assms(1) margin
    by blast
qed

lemma pl_capture_basin_implies_lock_admissible:
  assumes "pl_capture_basin coupling detuning"
  shows "pl_lock_admissible coupling detuning"
proof -
  have margin: "0 \<le> pl_capture_margin coupling detuning"
    using assms
    unfolding pl_capture_basin_def
    by blast
  have "abs detuning \<le> coupling"
    using margin
    unfolding pl_capture_margin_def
    by linarith
  then show ?thesis
    by (rule lock_admissible_from_threshold)
qed

lemma pl_capture_basin_width_positive:
  assumes "0 < coupling"
  shows "0 < pl_capture_basin_width coupling"
proof -
  show ?thesis
    using assms
    unfolding pl_capture_basin_width_def
    by linarith
qed

lemma pl_capture_witness_bounded:
  assumes "pl_capture_basin coupling detuning"
  shows "abs (pl_locking_phase_witness coupling detuning) \<le> 1"
proof -
  have lock: "pl_lock_admissible coupling detuning"
    using assms
    by (rule pl_capture_basin_implies_lock_admissible)
  have positive: "0 < coupling"
    using assms
    unfolding pl_capture_basin_def
    by blast
  show ?thesis
    unfolding pl_locking_phase_witness_def
    using lock positive
    by (rule admissible_lock_witness_bounded)
qed

lemma pl_capture_witness_zeroes_residual:
  assumes "pl_capture_basin coupling detuning"
  shows "pl_phase_velocity_residual coupling
    (pl_locking_phase_witness coupling detuning)
    detuning = 0"
proof -
  have nonzero: "coupling \<noteq> 0"
    using assms
    unfolding pl_capture_basin_def
    by linarith
  show ?thesis
    unfolding pl_locking_phase_witness_def
    using nonzero
    by (rule lock_witness_zeroes_linear_phase_residual)
qed

theorem phase_locking_capture_basin_contract:
  assumes "0 < coupling"
    and "abs detuning \<le> coupling"
  shows "pl_capture_contract coupling detuning
    \<and> pl_capture_basin_width coupling = 2 * coupling
    \<and> pl_ratio_selector_locked coupling detuning"
proof (intro conjI)
  have basin: "pl_capture_basin coupling detuning"
    using assms
    by (rule pl_capture_basin_from_threshold)
  have bounded: "abs (pl_locking_phase_witness coupling detuning) \<le> 1"
    using basin
    by (rule pl_capture_witness_bounded)
  have residual: "pl_phase_velocity_residual coupling
      (pl_locking_phase_witness coupling detuning)
      detuning = 0"
    using basin
    by (rule pl_capture_witness_zeroes_residual)
  show "pl_capture_contract coupling detuning"
    unfolding pl_capture_contract_def
    using basin bounded residual
    by blast
  show "pl_capture_basin_width coupling = 2 * coupling"
    unfolding pl_capture_basin_width_def .
  show "pl_ratio_selector_locked coupling detuning"
    unfolding pl_ratio_selector_locked_def
    using assms lock_admissible_from_threshold
    by blast
qed

end
