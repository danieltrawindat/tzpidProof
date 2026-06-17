theory TZPID_GyromagneticMovement_Typed_PhaseGradient
  imports TZPID_GyromagneticMovement_Computational_Checks
begin

text \<open>
  Project: TZPID Proof Pipeline
  Creator: Daniel Alexander Trawin
  ORCID: https://orcid.org/0009-0001-4630-3715
  Generated UTC: 2026-06-08T00:00:00Z

  Phase 4 bridge artifact:
  - delta_alpha_phase4_bridge.h5
  - phase2_checks/PHASE4_GYROMAGNETIC_BRIDGE_SUMMARY.md

  This layer connects the Bessel drop fraction to a typed radial phase
  gradient and then to a minimal gyromagnetic movement witness.  The older
  focus file remains the registry scaffold; this file is the algebraic HOL
  pin that can be extended later into vector calculus and MHD semantics.
\<close>

definition phase4_bridge_hdf5 :: string where
  "phase4_bridge_hdf5 = ''delta_alpha_phase4_bridge.h5''"

definition phase4_best_shell_dataset :: string where
  "phase4_best_shell_dataset = ''field/psi_real''"

definition phase4_best_shell_slice :: nat where
  "phase4_best_shell_slice = 0"

definition phase4_best_shell_mean_abs_error :: real where
  "phase4_best_shell_mean_abs_error = 0.0010169215212778027"

definition phase4_best_shell_max_abs_error :: real where
  "phase4_best_shell_max_abs_error = 0.001710663481156116"

definition phase4_lz_dataset_std :: real where
  "phase4_lz_dataset_std = 0.0000000000002330431"

definition gm_phase_gradient :: "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real" where
  "gm_phase_gradient j delta scale radius = j * delta * scale / radius"

definition gm_delta_alpha :: "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real" where
  "gm_delta_alpha j delta scale radius r = j * delta * scale * (r / radius)"

definition gm_Lz_witness :: "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real" where
  "gm_Lz_witness phase_gradient source_offset coupling =
    coupling * phase_gradient * source_offset"

definition gm_gyromagnetic_ratio :: "real \<Rightarrow> real \<Rightarrow> real" where
  "gm_gyromagnetic_ratio angular_momentum magnetic_moment =
    angular_momentum / magnetic_moment"

definition gm_bounded_half :: "real \<Rightarrow> bool" where
  "gm_bounded_half h \<longleftrightarrow> - (1 / 2) \<le> h \<and> h \<le> (1 / 2)"

lemma phase4_best_shell_error_below_two_milli:
  "phase4_best_shell_mean_abs_error < 0.002"
  unfolding phase4_best_shell_mean_abs_error_def
  by norm_num

lemma phase4_lz_is_correspondence_witness_not_shell_observable:
  "phase4_lz_dataset_std < 0.000000001"
  unfolding phase4_lz_dataset_std_def
  by norm_num

lemma gm_phase_gradient_positive:
  assumes "0 < j"
    and "0 < delta"
    and "0 < scale"
    and "0 < radius"
  shows "0 < gm_phase_gradient j delta scale radius"
  unfolding gm_phase_gradient_def
  using assms
  by (metis divide_pos_pos mult_pos_pos)

lemma gm_delta_alpha_is_linear_phase_driver:
  assumes "radius \<noteq> 0"
  shows "gm_delta_alpha j delta scale radius r =
    gm_phase_gradient j delta scale radius * r"
  unfolding gm_delta_alpha_def gm_phase_gradient_def
  using assms
  by field

lemma nonzero_phase_source_generates_nonzero_Lz_witness:
  assumes "coupling \<noteq> 0"
    and "phase_gradient \<noteq> 0"
    and "source_offset \<noteq> 0"
  shows "gm_Lz_witness phase_gradient source_offset coupling \<noteq> 0"
  unfolding gm_Lz_witness_def
  using assms
  by (metis mult_eq_0_iff)

lemma gyromagnetic_ratio_recovers_angular_momentum:
  assumes "magnetic_moment \<noteq> 0"
  shows "gm_gyromagnetic_ratio angular_momentum magnetic_moment * magnetic_moment =
    angular_momentum"
  unfolding gm_gyromagnetic_ratio_def
  using assms
  by field

lemma helicity_proxy_within_phase4_window:
  assumes "- (1 / 2) \<le> h"
    and "h \<le> (1 / 2)"
  shows "gm_bounded_half h"
  unfolding gm_bounded_half_def
  using assms
  by blast

theorem phase4_bessel_to_gyromagnetic_movement_pin:
  assumes "0 < j"
    and "0 < delta"
    and "0 < scale"
    and "0 < radius"
    and "source_offset \<noteq> 0"
    and "coupling \<noteq> 0"
    and "magnetic_moment \<noteq> 0"
  defines "k \<equiv> gm_phase_gradient j delta scale radius"
  defines "Lz \<equiv> gm_Lz_witness k source_offset coupling"
  shows "0 < k
    \<and> Lz \<noteq> 0
    \<and> gm_gyromagnetic_ratio Lz magnetic_moment * magnetic_moment = Lz
    \<and> phase4_best_shell_mean_abs_error < 0.002
    \<and> phase4_lz_dataset_std < 0.000000001"
proof -
  have k_pos: "0 < k"
    unfolding k_def
    using assms(1-4) gm_phase_gradient_positive
    by blast
  have k_nonzero: "k \<noteq> 0"
    using k_pos
    by linarith
  have Lz_nonzero: "Lz \<noteq> 0"
    unfolding Lz_def
    using assms(5,6) k_nonzero nonzero_phase_source_generates_nonzero_Lz_witness
    by blast
  have ratio: "gm_gyromagnetic_ratio Lz magnetic_moment * magnetic_moment = Lz"
    using assms(7) gyromagnetic_ratio_recovers_angular_momentum
    by blast
  have shell_error: "phase4_best_shell_mean_abs_error < 0.002"
    using phase4_best_shell_error_below_two_milli
    by blast
  have lz_const: "phase4_lz_dataset_std < 0.000000001"
    using phase4_lz_is_correspondence_witness_not_shell_observable
    by blast
  show ?thesis
    using k_pos Lz_nonzero ratio shell_error lz_const
    by blast
qed

end
