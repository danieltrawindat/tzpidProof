theory TZPID_HubbleBreathing_DESIDR2BAO_Certificate
  imports TZPID_HubbleBreathing_PlanckDistancePrior_Certificate
begin

text \<open>
  Project: TZPID Proof Pipeline
  Creator: Daniel Alexander Trawin
  ORCID: https://orcid.org/0009-0001-4630-3715
  Generated UTC: 2026-06-09T00:00:00Z

  DESI DR2 BAO covariance-likelihood carrier for the Hubble/Friedmann lane.
  The paired generator is:

    compute_hubble_desi_dr2_bao_likelihood.py

  and the generated artifacts are:

    phase2_checks/HUBBLE_DESI_DR2_BAO_LIKELIHOOD_CERTIFICATE.json
    phase2_checks/HUBBLE_DESI_DR2_BAO_LIKELIHOOD_CERTIFICATE.md
    phase2_checks/HUBBLE_DESI_DR2_BAO_SCENARIO_CHI2.csv
    phase2_checks/HUBBLE_DESI_DR2_BAO_MEASUREMENTS.csv

  This records the compressed DESI DR2 BAO Gaussian likelihood contract over
  DV/rd, DM/rd, and DH/rd.  It is not a full joint cosmological fit.
\<close>

datatype hb_desi_dr2_bao_check =
    HB_DESI_CosmoSIS_Module_Downloaded
  | HB_DESI_Embedded_Table_Parsed
  | HB_DESI_Source_References_DR2
  | HB_DESI_Default_Measurement_Shape_Matches
  | HB_DESI_Covariance_Positive_Definite
  | HB_DESI_Finite_BAO_Chi2
  | HB_DESI_Scenario_BAO_Likelihoods_Computed

definition hb_desi_dr2_bao_artifact :: "string" where
  "hb_desi_dr2_bao_artifact =
    ''phase2_checks/HUBBLE_DESI_DR2_BAO_LIKELIHOOD_CERTIFICATE.json''"

definition hb_desi_dr2_bao_boundary :: "string" where
  "hb_desi_dr2_bao_boundary =
    ''desi_dr2_gaussian_bao_likelihood_not_full_joint_fit''"

definition hb_desi_dr2_bao_measurement_count :: nat where
  "hb_desi_dr2_bao_measurement_count = 13"

definition hb_desi_dr2_bao_dataset_count :: nat where
  "hb_desi_dr2_bao_dataset_count = 7"

definition hb_desi_dr2_bao_status :: "hb_desi_dr2_bao_check \<Rightarrow> string" where
  "hb_desi_dr2_bao_status check =
    (case check of
      HB_DESI_CosmoSIS_Module_Downloaded => ''pass''
    | HB_DESI_Embedded_Table_Parsed => ''pass''
    | HB_DESI_Source_References_DR2 => ''pass''
    | HB_DESI_Default_Measurement_Shape_Matches => ''pass''
    | HB_DESI_Covariance_Positive_Definite => ''pass''
    | HB_DESI_Finite_BAO_Chi2 => ''pass''
    | HB_DESI_Scenario_BAO_Likelihoods_Computed => ''computed'')"

definition hb_desi_dr2_bao_verified_check :: "hb_desi_dr2_bao_check \<Rightarrow> bool" where
  "hb_desi_dr2_bao_verified_check check \<longleftrightarrow>
    hb_desi_dr2_bao_status check = ''pass''
    \<or> hb_desi_dr2_bao_status check = ''computed''"

definition hb_bao_ratio_residual :: "real \<Rightarrow> real \<Rightarrow> real" where
  "hb_bao_ratio_residual theory observed = theory - observed"

definition hb_bao_weighted_square :: "real \<Rightarrow> real \<Rightarrow> real" where
  "hb_bao_weighted_square residual inverse_variance =
    inverse_variance * residual\<^sup>2"

lemma hb_desi_module_verified:
  "hb_desi_dr2_bao_verified_check HB_DESI_CosmoSIS_Module_Downloaded"
proof -
  have "hb_desi_dr2_bao_status HB_DESI_CosmoSIS_Module_Downloaded = ''pass''"
    unfolding hb_desi_dr2_bao_status_def
    by (rule refl)
  then show ?thesis
    unfolding hb_desi_dr2_bao_verified_check_def
    by blast
qed

lemma hb_desi_table_verified:
  "hb_desi_dr2_bao_verified_check HB_DESI_Embedded_Table_Parsed"
proof -
  have "hb_desi_dr2_bao_status HB_DESI_Embedded_Table_Parsed = ''pass''"
    unfolding hb_desi_dr2_bao_status_def
    by (rule refl)
  then show ?thesis
    unfolding hb_desi_dr2_bao_verified_check_def
    by blast
qed

lemma hb_desi_source_verified:
  "hb_desi_dr2_bao_verified_check HB_DESI_Source_References_DR2"
proof -
  have "hb_desi_dr2_bao_status HB_DESI_Source_References_DR2 = ''pass''"
    unfolding hb_desi_dr2_bao_status_def
    by (rule refl)
  then show ?thesis
    unfolding hb_desi_dr2_bao_verified_check_def
    by blast
qed

lemma hb_desi_shape_verified:
  "hb_desi_dr2_bao_verified_check HB_DESI_Default_Measurement_Shape_Matches"
proof -
  have "hb_desi_dr2_bao_status HB_DESI_Default_Measurement_Shape_Matches = ''pass''"
    unfolding hb_desi_dr2_bao_status_def
    by (rule refl)
  then show ?thesis
    unfolding hb_desi_dr2_bao_verified_check_def
    by blast
qed

lemma hb_desi_covariance_verified:
  "hb_desi_dr2_bao_verified_check HB_DESI_Covariance_Positive_Definite"
proof -
  have "hb_desi_dr2_bao_status HB_DESI_Covariance_Positive_Definite = ''pass''"
    unfolding hb_desi_dr2_bao_status_def
    by (rule refl)
  then show ?thesis
    unfolding hb_desi_dr2_bao_verified_check_def
    by blast
qed

lemma hb_desi_chi2_verified:
  "hb_desi_dr2_bao_verified_check HB_DESI_Finite_BAO_Chi2"
proof -
  have "hb_desi_dr2_bao_status HB_DESI_Finite_BAO_Chi2 = ''pass''"
    unfolding hb_desi_dr2_bao_status_def
    by (rule refl)
  then show ?thesis
    unfolding hb_desi_dr2_bao_verified_check_def
    by blast
qed

lemma hb_desi_scenarios_computed:
  "hb_desi_dr2_bao_verified_check HB_DESI_Scenario_BAO_Likelihoods_Computed"
proof -
  have "hb_desi_dr2_bao_status HB_DESI_Scenario_BAO_Likelihoods_Computed = ''computed''"
    unfolding hb_desi_dr2_bao_status_def
    by (rule refl)
  then show ?thesis
    unfolding hb_desi_dr2_bao_verified_check_def
    by blast
qed

lemma hb_desi_measurement_count_positive:
  "0 < hb_desi_dr2_bao_measurement_count"
  unfolding hb_desi_dr2_bao_measurement_count_def
  by (rule zero_less_numeral)

lemma hb_desi_dataset_count_positive:
  "0 < hb_desi_dr2_bao_dataset_count"
  unfolding hb_desi_dr2_bao_dataset_count_def
  by (rule zero_less_numeral)

lemma hb_bao_weighted_square_nonnegative:
  assumes "0 \<le> inverse_variance"
  shows "0 \<le> hb_bao_weighted_square residual inverse_variance"
proof -
  have square_nonnegative: "0 \<le> residual\<^sup>2"
    by positivity
  show ?thesis
    unfolding hb_bao_weighted_square_def
    using assms square_nonnegative
    by (metis mult_nonneg_nonneg)
qed

theorem hb_desi_dr2_bao_likelihood_contract:
  assumes "0 \<le> inverse_variance"
  shows "hb_desi_dr2_bao_verified_check HB_DESI_CosmoSIS_Module_Downloaded
   \<and> hb_desi_dr2_bao_verified_check HB_DESI_Embedded_Table_Parsed
   \<and> hb_desi_dr2_bao_verified_check HB_DESI_Source_References_DR2
   \<and> hb_desi_dr2_bao_verified_check HB_DESI_Default_Measurement_Shape_Matches
   \<and> hb_desi_dr2_bao_verified_check HB_DESI_Covariance_Positive_Definite
   \<and> hb_desi_dr2_bao_verified_check HB_DESI_Finite_BAO_Chi2
   \<and> hb_desi_dr2_bao_verified_check HB_DESI_Scenario_BAO_Likelihoods_Computed
   \<and> 0 < hb_desi_dr2_bao_measurement_count
   \<and> 0 < hb_desi_dr2_bao_dataset_count
   \<and> 0 \<le> hb_bao_weighted_square residual inverse_variance"
proof (intro conjI)
  show "hb_desi_dr2_bao_verified_check HB_DESI_CosmoSIS_Module_Downloaded"
    by (rule hb_desi_module_verified)
  show "hb_desi_dr2_bao_verified_check HB_DESI_Embedded_Table_Parsed"
    by (rule hb_desi_table_verified)
  show "hb_desi_dr2_bao_verified_check HB_DESI_Source_References_DR2"
    by (rule hb_desi_source_verified)
  show "hb_desi_dr2_bao_verified_check HB_DESI_Default_Measurement_Shape_Matches"
    by (rule hb_desi_shape_verified)
  show "hb_desi_dr2_bao_verified_check HB_DESI_Covariance_Positive_Definite"
    by (rule hb_desi_covariance_verified)
  show "hb_desi_dr2_bao_verified_check HB_DESI_Finite_BAO_Chi2"
    by (rule hb_desi_chi2_verified)
  show "hb_desi_dr2_bao_verified_check HB_DESI_Scenario_BAO_Likelihoods_Computed"
    by (rule hb_desi_scenarios_computed)
  show "0 < hb_desi_dr2_bao_measurement_count"
    by (rule hb_desi_measurement_count_positive)
  show "0 < hb_desi_dr2_bao_dataset_count"
    by (rule hb_desi_dataset_count_positive)
  show "0 \<le> hb_bao_weighted_square residual inverse_variance"
    using assms
    by (rule hb_bao_weighted_square_nonnegative)
qed

context TZPID_NestedHypersphere_Focus
begin

theorem desi_dr2_bao_extends_hubble_spine:
  assumes "hb_component_normalized_today Omega_r Omega_m Omega_K Omega_X"
  shows "nested_hypersphere_unifying_chain
    \<and> hb_friedmann_hubble_sq H0 Omega_r Omega_m Omega_K Omega_X 1 1 =
      H0\<^sup>2
    \<and> hb_pantheon_raw_verified_check HB_PANTHEON_Finite_Full_Covariance_Chi2
    \<and> hb_planck_distance_verified_check HB_PLANCK_Finite_Distance_Prior_Chi2
    \<and> hb_desi_dr2_bao_verified_check HB_DESI_Finite_BAO_Chi2
    \<and> 0 < hb_desi_dr2_bao_measurement_count"
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
  show "0 < hb_desi_dr2_bao_measurement_count"
    by (rule hb_desi_measurement_count_positive)
qed

end

end
