theory TZPID_PhaseLockingResonance_KuramotoFiniteN
  imports TZPID_PhaseLockingResonance_CaptureBasin
begin

text \<open>
  Project: TZPID Proof Pipeline
  Creator: Daniel Alexander Trawin
  ORCID: https://orcid.org/0009-0001-4630-3715
  Generated UTC: 2026-06-09T00:00:00Z

  Nonlinear Kuramoto finite-N entrainment upgrade.

  This layer keeps the existing capture-basin semantics but lifts them from a
  single detuning into a finite scan contract.  A finite population is
  entrained when every detuning lies inside the same coupling window.  The
  order-parameter floor is a conservative algebraic certificate: it records the
  loss of coherence implied by the worst detuning radius D relative to coupling
  K, without claiming to solve every nonlinear oscillator trajectory.
\<close>

definition pl_finite_entrainment_scan :: "real \<Rightarrow> real list \<Rightarrow> bool" where
  "pl_finite_entrainment_scan coupling detunings \<longleftrightarrow>
    0 < coupling \<and> (\<forall>detuning \<in> set detunings. abs detuning \<le> coupling)"

definition pl_detuning_radius_admissible :: "real \<Rightarrow> real \<Rightarrow> bool" where
  "pl_detuning_radius_admissible coupling radius \<longleftrightarrow>
    0 < coupling \<and> 0 \<le> radius \<and> radius \<le> coupling"

definition pl_kuramoto_order_floor :: "real \<Rightarrow> real \<Rightarrow> real" where
  "pl_kuramoto_order_floor coupling radius =
    1 - (radius / coupling)\<^sup>2"

definition pl_finite_phase_witnesses :: "real \<Rightarrow> real list \<Rightarrow> real list" where
  "pl_finite_phase_witnesses coupling detunings =
    map (\<lambda>detuning. detuning / coupling) detunings"

definition pl_finite_scan_contract :: "real \<Rightarrow> real \<Rightarrow> real list \<Rightarrow> bool" where
  "pl_finite_scan_contract coupling radius detunings \<longleftrightarrow>
    pl_finite_entrainment_scan coupling detunings
    \<and> pl_detuning_radius_admissible coupling radius
    \<and> (\<forall>detuning \<in> set detunings. abs detuning \<le> radius)
    \<and> 0 \<le> pl_kuramoto_order_floor coupling radius
    \<and> pl_kuramoto_order_floor coupling radius \<le> 1"

lemma pl_finite_scan_implies_each_capture_basin:
  assumes "pl_finite_entrainment_scan coupling detunings"
    and "detuning \<in> set detunings"
  shows "pl_capture_basin coupling detuning"
proof -
  have positive: "0 < coupling"
    using assms(1)
    unfolding pl_finite_entrainment_scan_def
    by blast
  have threshold: "abs detuning \<le> coupling"
    using assms
    unfolding pl_finite_entrainment_scan_def
    by blast
  show ?thesis
    using positive threshold
    by (rule pl_capture_basin_from_threshold)
qed

lemma pl_finite_scan_witnesses_bounded:
  assumes "pl_finite_entrainment_scan coupling detunings"
    and "witness \<in> set (pl_finite_phase_witnesses coupling detunings)"
  shows "abs witness \<le> 1"
proof -
  obtain detuning where detuning_member: "detuning \<in> set detunings"
    and witness_eq: "witness = detuning / coupling"
    using assms(2)
    unfolding pl_finite_phase_witnesses_def
    by (metis image_iff set_map)
  have basin: "pl_capture_basin coupling detuning"
    using assms(1) detuning_member
    by (rule pl_finite_scan_implies_each_capture_basin)
  have "abs (pl_locking_phase_witness coupling detuning) \<le> 1"
    using basin
    by (rule pl_capture_witness_bounded)
  then show ?thesis
    unfolding pl_locking_phase_witness_def
    using witness_eq
    by blast
qed

lemma pl_order_floor_bounds:
  assumes "pl_detuning_radius_admissible coupling radius"
  shows "0 \<le> pl_kuramoto_order_floor coupling radius
    \<and> pl_kuramoto_order_floor coupling radius \<le> 1"
proof -
  have positive: "0 < coupling"
    using assms
    unfolding pl_detuning_radius_admissible_def
    by blast
  have radius_nonnegative: "0 \<le> radius"
    using assms
    unfolding pl_detuning_radius_admissible_def
    by blast
  have radius_le_coupling: "radius \<le> coupling"
    using assms
    unfolding pl_detuning_radius_admissible_def
    by blast
  have ratio_nonnegative: "0 \<le> radius / coupling"
    using radius_nonnegative positive
    by (meson divide_nonneg_pos)
  have ratio_le_one: "radius / coupling \<le> 1"
    using radius_le_coupling positive
    by (metis divide_le_eq_1_pos)
  have square_le_one: "(radius / coupling)\<^sup>2 \<le> 1"
    using ratio_nonnegative ratio_le_one
    by nlinarith
  have square_nonnegative: "0 \<le> (radius / coupling)\<^sup>2"
    by (rule zero_le_power2)
  show ?thesis
    unfolding pl_kuramoto_order_floor_def
    using square_le_one square_nonnegative
    by linarith
qed

theorem phase_locking_kuramoto_finite_n_scan_contract:
  assumes scan: "pl_finite_entrainment_scan coupling detunings"
    and radius: "pl_detuning_radius_admissible coupling radius"
    and covers: "\<forall>detuning \<in> set detunings. abs detuning \<le> radius"
  shows "pl_finite_scan_contract coupling radius detunings
    \<and> (\<forall>detuning \<in> set detunings. pl_capture_basin coupling detuning)
    \<and> (\<forall>witness \<in> set (pl_finite_phase_witnesses coupling detunings).
        abs witness \<le> 1)"
proof -
  have floor_bounds:
    "0 \<le> pl_kuramoto_order_floor coupling radius
      \<and> pl_kuramoto_order_floor coupling radius \<le> 1"
    using radius
    by (rule pl_order_floor_bounds)
  have each_capture:
    "\<forall>detuning \<in> set detunings. pl_capture_basin coupling detuning"
    using scan pl_finite_scan_implies_each_capture_basin
    by blast
  have witnesses:
    "\<forall>witness \<in> set (pl_finite_phase_witnesses coupling detunings).
      abs witness \<le> 1"
    using scan pl_finite_scan_witnesses_bounded
    by blast
  have contract: "pl_finite_scan_contract coupling radius detunings"
    unfolding pl_finite_scan_contract_def
    using scan radius covers floor_bounds
    by blast
  show ?thesis
    using contract each_capture witnesses
    by blast
qed

end
