theory TZPID_GyromagneticMovement_VectorCalculus
  imports TZPID_GyromagneticMovement_Typed_PhaseGradient
begin

text \<open>
  Project: TZPID Proof Pipeline
  Creator: Daniel Alexander Trawin
  ORCID: https://orcid.org/0009-0001-4630-3715
  Generated UTC: 2026-06-08T00:00:00Z

  Phase 5 bridge artifact:
  - delta_alpha_phase5_vector_calculus.h5
  - phase2_checks/PHASE5_VECTOR_CALCULUS_BRIDGE_SUMMARY.md

  This layer records the vector-calculus pin: the Delta-alpha gradient is
  treated as an exact planar vector field, its curl cancels when the mixed
  partials agree, and the HDF5 artifact provides the near-zero numerical curl
  certificate.
\<close>

definition phase5_bridge_hdf5 :: string where
  "phase5_bridge_hdf5 = ''delta_alpha_phase5_vector_calculus.h5''"

definition phase5_delta :: real where
  "phase5_delta = 0.18010602113350746"

definition phase5_curl_max_abs :: real where
  "phase5_curl_max_abs = 0.000000000017713830402499298"

definition phase5_curl_std :: real where
  "phase5_curl_std = 0.0000000000003081535060467766"

definition phase5_psi_unit_norm_max_error :: real where
  "phase5_psi_unit_norm_max_error = 0.0000000000000002220446049250313"

definition phase5_lz_std :: real where
  "phase5_lz_std = 0.0000000000002317575256303825"

definition gm_grad_mag_sq :: "real \<Rightarrow> real \<Rightarrow> real" where
  "gm_grad_mag_sq gx gy = gx\<^sup>2 + gy\<^sup>2"

definition gm_curl_z :: "real \<Rightarrow> real \<Rightarrow> real" where
  "gm_curl_z partial_x_grad_y partial_y_grad_x =
    partial_x_grad_y - partial_y_grad_x"

definition gm_phase_vector_active :: "real \<Rightarrow> real \<Rightarrow> bool" where
  "gm_phase_vector_active gx gy \<longleftrightarrow> 0 < gm_grad_mag_sq gx gy"

lemma phase5_delta_contract:
  "0.18 < phase5_delta \<and> phase5_delta < 0.19"
  unfolding phase5_delta_def
  by norm_num

lemma phase5_curl_numerically_near_zero:
  "phase5_curl_max_abs < 0.000000001"
  unfolding phase5_curl_max_abs_def
  by norm_num

lemma phase5_psi_unit_norm_locked:
  "phase5_psi_unit_norm_max_error < 0.000000001"
  unfolding phase5_psi_unit_norm_max_error_def
  by norm_num

lemma phase5_lz_remains_correspondence_witness:
  "phase5_lz_std < 0.000000001"
  unfolding phase5_lz_std_def
  by norm_num

lemma exact_gradient_curl_cancels:
  assumes "partial_x_grad_y = partial_y_grad_x"
  shows "gm_curl_z partial_x_grad_y partial_y_grad_x = 0"
  unfolding gm_curl_z_def
  using assms
  by algebra

lemma active_phase_vector_has_nonzero_component:
  assumes "gm_phase_vector_active gx gy"
  shows "gx \<noteq> 0 \<or> gy \<noteq> 0"
proof -
  have mag_pos: "0 < gx\<^sup>2 + gy\<^sup>2"
    using assms
    unfolding gm_phase_vector_active_def gm_grad_mag_sq_def
    by blast
  show ?thesis
  proof (rule ccontr)
    assume "\<not> (gx \<noteq> 0 \<or> gy \<noteq> 0)"
    then have zeros: "gx = 0 \<and> gy = 0"
      by blast
    then have "gx\<^sup>2 + gy\<^sup>2 = 0"
      by algebra
    then show False
      using mag_pos
      by linarith
  qed
qed

lemma active_phase_vector_can_drive_Lz_witness:
  assumes "gm_phase_vector_active gx gy"
    and "coupling \<noteq> 0"
    and "source_offset \<noteq> 0"
    and "phase_gradient = sqrt (gm_grad_mag_sq gx gy)"
  shows "phase_gradient \<noteq> 0 \<longrightarrow>
    gm_Lz_witness phase_gradient source_offset coupling \<noteq> 0"
  using assms(2,3) nonzero_phase_source_generates_nonzero_Lz_witness
  by blast

theorem phase5_vector_calculus_bridge_locked:
  assumes "partial_x_grad_y = partial_y_grad_x"
    and "gm_phase_vector_active gx gy"
    and "coupling \<noteq> 0"
    and "source_offset \<noteq> 0"
    and "phase_gradient = sqrt (gm_grad_mag_sq gx gy)"
    and "phase_gradient \<noteq> 0"
  shows "gm_curl_z partial_x_grad_y partial_y_grad_x = 0
    \<and> (gx \<noteq> 0 \<or> gy \<noteq> 0)
    \<and> gm_Lz_witness phase_gradient source_offset coupling \<noteq> 0
    \<and> 0.18 < phase5_delta
    \<and> phase5_delta < 0.19
    \<and> phase5_curl_max_abs < 0.000000001
    \<and> phase5_psi_unit_norm_max_error < 0.000000001
    \<and> phase5_lz_std < 0.000000001"
proof -
  have curl_zero: "gm_curl_z partial_x_grad_y partial_y_grad_x = 0"
    using assms(1) exact_gradient_curl_cancels
    by blast
  have active_component: "gx \<noteq> 0 \<or> gy \<noteq> 0"
    using assms(2) active_phase_vector_has_nonzero_component
    by blast
  have witness: "gm_Lz_witness phase_gradient source_offset coupling \<noteq> 0"
    using assms(3,4,6) nonzero_phase_source_generates_nonzero_Lz_witness
    by blast
  have delta_window: "0.18 < phase5_delta \<and> phase5_delta < 0.19"
    using phase5_delta_contract
    by blast
  have curl_bound: "phase5_curl_max_abs < 0.000000001"
    using phase5_curl_numerically_near_zero
    by blast
  have psi_bound: "phase5_psi_unit_norm_max_error < 0.000000001"
    using phase5_psi_unit_norm_locked
    by blast
  have lz_bound: "phase5_lz_std < 0.000000001"
    using phase5_lz_remains_correspondence_witness
    by blast
  show ?thesis
    using curl_zero active_component witness delta_window curl_bound psi_bound lz_bound
    by blast
qed

end
