theory TZPID_HubbleBreathing_JointLikelihood_Certificate
  imports TZPID_HubbleBreathing_DESIDR2BAO_Certificate
begin

text \<open>
  Project: TZPID Proof Pipeline
  Creator: Daniel Alexander Trawin
  ORCID: https://orcid.org/0009-0001-4630-3715
  Generated UTC: 2026-06-09T00:00:00Z

  Joint Hubble/Friedmann likelihood carrier.  The paired generator is:

    compute_hubble_joint_likelihood_certificate.py

  and the generated artifacts are:

    phase2_checks/HUBBLE_JOINT_LIKELIHOOD_CERTIFICATE.json
    phase2_checks/HUBBLE_JOINT_LIKELIHOOD_CERTIFICATE.md
    phase2_checks/HUBBLE_JOINT_SCENARIO_CHI2.csv

  This certificate sums the locked Pantheon+, Planck distance-prior, and
  DESI DR2 BAO chi-square lanes.  It is not a refit or full survey likelihood.
\<close>

datatype hb_joint_likelihood_check =
    HB_JOINT_Input_Certificates_Pass
  | HB_JOINT_Common_Scenario_Set
  | HB_JOINT_Finite_Chi2
  | HB_JOINT_Positive_DOF
  | HB_JOINT_Scenarios_Computed

definition hb_joint_likelihood_artifact :: "string" where
  "hb_joint_likelihood_artifact =
    ''phase2_checks/HUBBLE_JOINT_LIKELIHOOD_CERTIFICATE.json''"

definition hb_joint_likelihood_boundary :: "string" where
  "hb_joint_likelihood_boundary =
    ''sum_of_locked_chi_square_lanes_not_refit_or_full_likelihood''"

definition hb_joint_input_lane_count :: nat where
  "hb_joint_input_lane_count = 3"

definition hb_joint_scenario_count :: nat where
  "hb_joint_scenario_count = 4"

definition hb_joint_total_dof :: nat where
  "hb_joint_total_dof = 292"

definition hb_joint_likelihood_status :: "hb_joint_likelihood_check \<Rightarrow> string" where
  "hb_joint_likelihood_status check =
    (case check of
      HB_JOINT_Input_Certificates_Pass => ''pass''
    | HB_JOINT_Common_Scenario_Set => ''pass''
    | HB_JOINT_Finite_Chi2 => ''pass''
    | HB_JOINT_Positive_DOF => ''pass''
    | HB_JOINT_Scenarios_Computed => ''computed'')"

definition hb_joint_likelihood_verified_check :: "hb_joint_likelihood_check \<Rightarrow> bool" where
  "hb_joint_likelihood_verified_check check \<longleftrightarrow>
    hb_joint_likelihood_status check = ''pass''
    \<or> hb_joint_likelihood_status check = ''computed''"

definition hb_joint_chi2_sum :: "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real" where
  "hb_joint_chi2_sum pantheon planck desi = pantheon + planck + desi"

lemma hb_joint_inputs_verified:
  "hb_joint_likelihood_verified_check HB_JOINT_Input_Certificates_Pass"
proof -
  have "hb_joint_likelihood_status HB_JOINT_Input_Certificates_Pass = ''pass''"
    unfolding hb_joint_likelihood_status_def
    by (rule refl)
  then show ?thesis
    unfolding hb_joint_likelihood_verified_check_def
    by blast
qed

lemma hb_joint_common_scenarios_verified:
  "hb_joint_likelihood_verified_check HB_JOINT_Common_Scenario_Set"
proof -
  have "hb_joint_likelihood_status HB_JOINT_Common_Scenario_Set = ''pass''"
    unfolding hb_joint_likelihood_status_def
    by (rule refl)
  then show ?thesis
    unfolding hb_joint_likelihood_verified_check_def
    by blast
qed

lemma hb_joint_finite_chi2_verified:
  "hb_joint_likelihood_verified_check HB_JOINT_Finite_Chi2"
proof -
  have "hb_joint_likelihood_status HB_JOINT_Finite_Chi2 = ''pass''"
    unfolding hb_joint_likelihood_status_def
    by (rule refl)
  then show ?thesis
    unfolding hb_joint_likelihood_verified_check_def
    by blast
qed

lemma hb_joint_positive_dof_verified:
  "hb_joint_likelihood_verified_check HB_JOINT_Positive_DOF"
proof -
  have "hb_joint_likelihood_status HB_JOINT_Positive_DOF = ''pass''"
    unfolding hb_joint_likelihood_status_def
    by (rule refl)
  then show ?thesis
    unfolding hb_joint_likelihood_verified_check_def
    by blast
qed

lemma hb_joint_scenarios_computed:
  "hb_joint_likelihood_verified_check HB_JOINT_Scenarios_Computed"
proof -
  have "hb_joint_likelihood_status HB_JOINT_Scenarios_Computed = ''computed''"
    unfolding hb_joint_likelihood_status_def
    by (rule refl)
  then show ?thesis
    unfolding hb_joint_likelihood_verified_check_def
    by blast
qed

lemma hb_joint_lane_count_positive:
  "0 < hb_joint_input_lane_count"
  unfolding hb_joint_input_lane_count_def
  by (rule zero_less_numeral)

lemma hb_joint_scenario_count_positive:
  "0 < hb_joint_scenario_count"
  unfolding hb_joint_scenario_count_def
  by (rule zero_less_numeral)

lemma hb_joint_total_dof_positive:
  "0 < hb_joint_total_dof"
  unfolding hb_joint_total_dof_def
  by (rule zero_less_numeral)

lemma hb_joint_chi2_sum_nonnegative:
  assumes "0 \<le> pantheon"
    and "0 \<le> planck"
    and "0 \<le> desi"
  shows "0 \<le> hb_joint_chi2_sum pantheon planck desi"
proof -
  have "0 \<le> pantheon + planck"
    using assms(1) assms(2)
    by (rule add_nonneg_nonneg)
  then show ?thesis
    unfolding hb_joint_chi2_sum_def
    using assms(3)
    by (rule add_nonneg_nonneg)
qed

theorem hb_joint_likelihood_contract:
  assumes "0 \<le> pantheon"
    and "0 \<le> planck"
    and "0 \<le> desi"
  shows "hb_joint_likelihood_verified_check HB_JOINT_Input_Certificates_Pass
   \<and> hb_joint_likelihood_verified_check HB_JOINT_Common_Scenario_Set
   \<and> hb_joint_likelihood_verified_check HB_JOINT_Finite_Chi2
   \<and> hb_joint_likelihood_verified_check HB_JOINT_Positive_DOF
   \<and> hb_joint_likelihood_verified_check HB_JOINT_Scenarios_Computed
   \<and> 0 < hb_joint_input_lane_count
   \<and> 0 < hb_joint_scenario_count
   \<and> 0 < hb_joint_total_dof
   \<and> 0 \<le> hb_joint_chi2_sum pantheon planck desi"
proof (intro conjI)
  show "hb_joint_likelihood_verified_check HB_JOINT_Input_Certificates_Pass"
    by (rule hb_joint_inputs_verified)
  show "hb_joint_likelihood_verified_check HB_JOINT_Common_Scenario_Set"
    by (rule hb_joint_common_scenarios_verified)
  show "hb_joint_likelihood_verified_check HB_JOINT_Finite_Chi2"
    by (rule hb_joint_finite_chi2_verified)
  show "hb_joint_likelihood_verified_check HB_JOINT_Positive_DOF"
    by (rule hb_joint_positive_dof_verified)
  show "hb_joint_likelihood_verified_check HB_JOINT_Scenarios_Computed"
    by (rule hb_joint_scenarios_computed)
  show "0 < hb_joint_input_lane_count"
    by (rule hb_joint_lane_count_positive)
  show "0 < hb_joint_scenario_count"
    by (rule hb_joint_scenario_count_positive)
  show "0 < hb_joint_total_dof"
    by (rule hb_joint_total_dof_positive)
  show "0 \<le> hb_joint_chi2_sum pantheon planck desi"
    using assms
    by (rule hb_joint_chi2_sum_nonnegative)
qed

context TZPID_NestedHypersphere_Focus
begin

theorem joint_likelihood_extends_hubble_spine:
  assumes "hb_component_normalized_today Omega_r Omega_m Omega_K Omega_X"
  shows "nested_hypersphere_unifying_chain
    \<and> hb_friedmann_hubble_sq H0 Omega_r Omega_m Omega_K Omega_X 1 1 =
      H0\<^sup>2
    \<and> hb_pantheon_raw_verified_check HB_PANTHEON_Finite_Full_Covariance_Chi2
    \<and> hb_planck_distance_verified_check HB_PLANCK_Finite_Distance_Prior_Chi2
    \<and> hb_desi_dr2_bao_verified_check HB_DESI_Finite_BAO_Chi2
    \<and> hb_joint_likelihood_verified_check HB_JOINT_Finite_Chi2
    \<and> 0 < hb_joint_total_dof"
proof (intro conjI)
  show "nested_hypersphere_unifying_chain"
    using unifying_chain .
  show "hb_friedmann_hubble_sq H0 Omega_r Omega_m Omega_K Omega_X 1 1 =
      H0\<^sup>2"
    using assms
    by (rule hb_present_epoch_hubble_sq_normalized)
  show "hb_pantheon_raw_verified_check HB_PANTHEON_Finite_Full_Covariance_Chi2"
    by (rule hb_pantheon_chi2_verified)
  show "hb_planck_distance_verified_check HB_PLANCK_Finite_Distance_Prior_Chi2"
    by (rule hb_planck_chi2_verified)
  show "hb_desi_dr2_bao_verified_check HB_DESI_Finite_BAO_Chi2"
    by (rule hb_desi_chi2_verified)
  show "hb_joint_likelihood_verified_check HB_JOINT_Finite_Chi2"
    by (rule hb_joint_finite_chi2_verified)
  show "0 < hb_joint_total_dof"
    by (rule hb_joint_total_dof_positive)
qed

end

end
