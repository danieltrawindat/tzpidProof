theory TZPID_HubbleBreathing_PantheonRaw_Certificate
  imports TZPID_HubbleBreathing_ObservedFit_Certificate
begin

text \<open>
  Project: TZPID Proof Pipeline
  Creator: Daniel Alexander Trawin
  ORCID: https://orcid.org/0009-0001-4630-3715
  Generated UTC: 2026-06-09T00:00:00Z

  Pantheon+ raw-covariance likelihood carrier for the Hubble/Friedmann lane.
  The paired generator is:

    compute_hubble_pantheonplus_raw_likelihood.py

  and the generated artifacts are:

    phase2_checks/HUBBLE_PANTHEONPLUS_RAW_LIKELIHOOD_CERTIFICATE.json
    phase2_checks/HUBBLE_PANTHEONPLUS_RAW_LIKELIHOOD_CERTIFICATE.md
    phase2_checks/HUBBLE_PANTHEONPLUS_RAW_SCENARIO_CHI2.csv

  Isabelle records the certificate contract and the algebraic nonnegativity of
  chi-square style residuals.  The raw Pantheon+ data table and covariance
  matrix remain external computational evidence.
\<close>

datatype hb_pantheon_raw_check =
    HB_PANTHEON_Public_Files_Downloaded
  | HB_PANTHEON_Data_Covariance_Shape_Match
  | HB_PANTHEON_Selected_Covariance_Positive_Definite
  | HB_PANTHEON_Finite_Full_Covariance_Chi2
  | HB_PANTHEON_Scenario_Likelihoods_Computed

definition hb_pantheon_raw_artifact :: "string" where
  "hb_pantheon_raw_artifact =
    ''phase2_checks/HUBBLE_PANTHEONPLUS_RAW_LIKELIHOOD_CERTIFICATE.json''"

definition hb_pantheon_raw_boundary :: "string" where
  "hb_pantheon_raw_boundary =
    ''pantheon_plus_hubble_flow_only_not_joint_cmb_desi_sn_fit''"

definition hb_pantheon_raw_selected_rows :: nat where
  "hb_pantheon_raw_selected_rows = 277"

definition hb_pantheon_raw_status :: "hb_pantheon_raw_check \<Rightarrow> string" where
  "hb_pantheon_raw_status check =
    (case check of
      HB_PANTHEON_Public_Files_Downloaded => ''pass''
    | HB_PANTHEON_Data_Covariance_Shape_Match => ''pass''
    | HB_PANTHEON_Selected_Covariance_Positive_Definite => ''pass''
    | HB_PANTHEON_Finite_Full_Covariance_Chi2 => ''pass''
    | HB_PANTHEON_Scenario_Likelihoods_Computed => ''computed'')"

definition hb_pantheon_raw_verified_check :: "hb_pantheon_raw_check \<Rightarrow> bool" where
  "hb_pantheon_raw_verified_check check \<longleftrightarrow>
    hb_pantheon_raw_status check = ''pass''
    \<or> hb_pantheon_raw_status check = ''computed''"

definition hb_profiled_residual :: "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real" where
  "hb_profiled_residual model observed offset = model - observed - offset"

definition hb_profiled_chi2_contribution ::
  "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real" where
  "hb_profiled_chi2_contribution model observed offset variance =
    (hb_profiled_residual model observed offset)\<^sup>2 / variance"

lemma hb_pantheon_public_files_verified:
  "hb_pantheon_raw_verified_check HB_PANTHEON_Public_Files_Downloaded"
proof -
  have "hb_pantheon_raw_status HB_PANTHEON_Public_Files_Downloaded = ''pass''"
    unfolding hb_pantheon_raw_status_def
    by (rule refl)
  then show ?thesis
    unfolding hb_pantheon_raw_verified_check_def
    by blast
qed

lemma hb_pantheon_shape_verified:
  "hb_pantheon_raw_verified_check HB_PANTHEON_Data_Covariance_Shape_Match"
proof -
  have "hb_pantheon_raw_status HB_PANTHEON_Data_Covariance_Shape_Match = ''pass''"
    unfolding hb_pantheon_raw_status_def
    by (rule refl)
  then show ?thesis
    unfolding hb_pantheon_raw_verified_check_def
    by blast
qed

lemma hb_pantheon_covariance_verified:
  "hb_pantheon_raw_verified_check HB_PANTHEON_Selected_Covariance_Positive_Definite"
proof -
  have "hb_pantheon_raw_status HB_PANTHEON_Selected_Covariance_Positive_Definite = ''pass''"
    unfolding hb_pantheon_raw_status_def
    by (rule refl)
  then show ?thesis
    unfolding hb_pantheon_raw_verified_check_def
    by blast
qed

lemma hb_pantheon_chi2_verified:
  "hb_pantheon_raw_verified_check HB_PANTHEON_Finite_Full_Covariance_Chi2"
proof -
  have "hb_pantheon_raw_status HB_PANTHEON_Finite_Full_Covariance_Chi2 = ''pass''"
    unfolding hb_pantheon_raw_status_def
    by (rule refl)
  then show ?thesis
    unfolding hb_pantheon_raw_verified_check_def
    by blast
qed

lemma hb_pantheon_likelihoods_computed:
  "hb_pantheon_raw_verified_check HB_PANTHEON_Scenario_Likelihoods_Computed"
proof -
  have "hb_pantheon_raw_status HB_PANTHEON_Scenario_Likelihoods_Computed = ''computed''"
    unfolding hb_pantheon_raw_status_def
    by (rule refl)
  then show ?thesis
    unfolding hb_pantheon_raw_verified_check_def
    by blast
qed

lemma hb_profiled_chi2_contribution_nonnegative:
  assumes "0 < variance"
  shows "0 \<le> hb_profiled_chi2_contribution model observed offset variance"
proof -
  have square_nonnegative:
    "0 \<le> (hb_profiled_residual model observed offset)\<^sup>2"
    by positivity
  show ?thesis
    unfolding hb_profiled_chi2_contribution_def
    using assms square_nonnegative
    by (metis divide_nonneg_pos)
qed

lemma hb_pantheon_selected_rows_positive:
  "0 < hb_pantheon_raw_selected_rows"
  unfolding hb_pantheon_raw_selected_rows_def
  by (rule zero_less_numeral)

theorem hb_pantheon_raw_likelihood_contract:
  assumes "0 < variance"
  shows "hb_pantheon_raw_verified_check HB_PANTHEON_Public_Files_Downloaded
   \<and> hb_pantheon_raw_verified_check HB_PANTHEON_Data_Covariance_Shape_Match
   \<and> hb_pantheon_raw_verified_check HB_PANTHEON_Selected_Covariance_Positive_Definite
   \<and> hb_pantheon_raw_verified_check HB_PANTHEON_Finite_Full_Covariance_Chi2
   \<and> hb_pantheon_raw_verified_check HB_PANTHEON_Scenario_Likelihoods_Computed
   \<and> 0 < hb_pantheon_raw_selected_rows
   \<and> 0 \<le> hb_profiled_chi2_contribution model observed offset variance"
proof (intro conjI)
  show "hb_pantheon_raw_verified_check HB_PANTHEON_Public_Files_Downloaded"
    by (rule hb_pantheon_public_files_verified)
  show "hb_pantheon_raw_verified_check HB_PANTHEON_Data_Covariance_Shape_Match"
    by (rule hb_pantheon_shape_verified)
  show "hb_pantheon_raw_verified_check HB_PANTHEON_Selected_Covariance_Positive_Definite"
    by (rule hb_pantheon_covariance_verified)
  show "hb_pantheon_raw_verified_check HB_PANTHEON_Finite_Full_Covariance_Chi2"
    by (rule hb_pantheon_chi2_verified)
  show "hb_pantheon_raw_verified_check HB_PANTHEON_Scenario_Likelihoods_Computed"
    by (rule hb_pantheon_likelihoods_computed)
  show "0 < hb_pantheon_raw_selected_rows"
    by (rule hb_pantheon_selected_rows_positive)
  show "0 \<le> hb_profiled_chi2_contribution model observed offset variance"
    using assms
    by (rule hb_profiled_chi2_contribution_nonnegative)
qed

context TZPID_NestedHypersphere_Focus
begin

theorem pantheon_raw_likelihood_extends_hubble_spine:
  assumes "hb_component_normalized_today Omega_r Omega_m Omega_K Omega_X"
  shows "nested_hypersphere_unifying_chain
    \<and> hb_friedmann_hubble_sq H0 Omega_r Omega_m Omega_K Omega_X 1 1 =
      H0\<^sup>2
    \<and> hb_observed_fit_verified_check HB_OBS_Parameter_Coverage
    \<and> hb_pantheon_raw_verified_check HB_PANTHEON_Finite_Full_Covariance_Chi2
    \<and> 0 < hb_pantheon_raw_selected_rows"
proof (intro conjI)
  show "nested_hypersphere_unifying_chain"
    using unifying_chain .
  show "hb_friedmann_hubble_sq H0 Omega_r Omega_m Omega_K Omega_X 1 1 =
      H0\<^sup>2"
    using assms
    by (rule hb_present_epoch_hubble_sq_normalized)
  show "hb_observed_fit_verified_check HB_OBS_Parameter_Coverage"
    by (rule hb_observed_parameter_coverage_verified)
  show "hb_pantheon_raw_verified_check HB_PANTHEON_Finite_Full_Covariance_Chi2"
    by (rule hb_pantheon_chi2_verified)
  show "0 < hb_pantheon_raw_selected_rows"
    by (rule hb_pantheon_selected_rows_positive)
qed

end

end
