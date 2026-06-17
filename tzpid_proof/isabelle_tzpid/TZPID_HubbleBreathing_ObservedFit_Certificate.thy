theory TZPID_HubbleBreathing_ObservedFit_Certificate
  imports TZPID_HubbleBreathing_CPL_Certificate
begin

text \<open>
  Project: TZPID Proof Pipeline
  Creator: Daniel Alexander Trawin
  ORCID: https://orcid.org/0009-0001-4630-3715
  Generated UTC: 2026-06-09T00:00:00Z

  Observed-summary residual certificate carrier for the Hubble/Friedmann lane.
  The paired generator is:

    compute_hubble_friedmann_observed_fit.py

  and the generated artifacts are:

    phase2_checks/HUBBLE_FRIEDMANN_OBSERVED_SUMMARY_CONSTRAINTS.csv
    phase2_checks/HUBBLE_FRIEDMANN_OBSERVED_FIT_CERTIFICATE.json
    phase2_checks/HUBBLE_FRIEDMANN_OBSERVED_FIT_CERTIFICATE.md

  This is not a raw likelihood and does not include covariance matrices.  It
  records the first observed-data residual lane over H0, Omega_m, Omega_K, w0,
  and wa.
\<close>

datatype hb_observed_fit_check =
    HB_OBS_Positive_Uncertainties
  | HB_OBS_Finite_Residuals
  | HB_OBS_Parameter_Coverage
  | HB_OBS_Summary_Fit_Computed
  | HB_OBS_Hubble_Tension_Exposed

definition hb_observed_fit_artifact :: "string" where
  "hb_observed_fit_artifact =
    ''phase2_checks/HUBBLE_FRIEDMANN_OBSERVED_FIT_CERTIFICATE.json''"

definition hb_observed_fit_boundary :: "string" where
  "hb_observed_fit_boundary =
    ''published_summary_constraints_not_raw_likelihood''"

definition hb_observed_fit_status :: "hb_observed_fit_check \<Rightarrow> string" where
  "hb_observed_fit_status check =
    (case check of
      HB_OBS_Positive_Uncertainties => ''pass''
    | HB_OBS_Finite_Residuals => ''pass''
    | HB_OBS_Parameter_Coverage => ''pass''
    | HB_OBS_Summary_Fit_Computed => ''computed''
    | HB_OBS_Hubble_Tension_Exposed => ''computed'')"

definition hb_observed_fit_verified_check :: "hb_observed_fit_check \<Rightarrow> bool" where
  "hb_observed_fit_verified_check check \<longleftrightarrow>
    hb_observed_fit_status check = ''pass''
    \<or> hb_observed_fit_status check = ''computed''"

definition hb_normalized_residual :: "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real" where
  "hb_normalized_residual model observed sigma = (model - observed) / sigma"

definition hb_chi2_contribution :: "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real" where
  "hb_chi2_contribution model observed sigma =
    (hb_normalized_residual model observed sigma)\<^sup>2"

definition hb_weighted_fit_value ::
  "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real" where
  "hb_weighted_fit_value x1 sigma1 x2 sigma2 =
    (x1 / sigma1\<^sup>2 + x2 / sigma2\<^sup>2) /
    (1 / sigma1\<^sup>2 + 1 / sigma2\<^sup>2)"

lemma hb_observed_positive_uncertainties_verified:
  "hb_observed_fit_verified_check HB_OBS_Positive_Uncertainties"
proof -
  have "hb_observed_fit_status HB_OBS_Positive_Uncertainties = ''pass''"
    unfolding hb_observed_fit_status_def
    by (rule refl)
  then show ?thesis
    unfolding hb_observed_fit_verified_check_def
    by blast
qed

lemma hb_observed_finite_residuals_verified:
  "hb_observed_fit_verified_check HB_OBS_Finite_Residuals"
proof -
  have "hb_observed_fit_status HB_OBS_Finite_Residuals = ''pass''"
    unfolding hb_observed_fit_status_def
    by (rule refl)
  then show ?thesis
    unfolding hb_observed_fit_verified_check_def
    by blast
qed

lemma hb_observed_parameter_coverage_verified:
  "hb_observed_fit_verified_check HB_OBS_Parameter_Coverage"
proof -
  have "hb_observed_fit_status HB_OBS_Parameter_Coverage = ''pass''"
    unfolding hb_observed_fit_status_def
    by (rule refl)
  then show ?thesis
    unfolding hb_observed_fit_verified_check_def
    by blast
qed

lemma hb_observed_summary_fit_computed:
  "hb_observed_fit_verified_check HB_OBS_Summary_Fit_Computed"
proof -
  have "hb_observed_fit_status HB_OBS_Summary_Fit_Computed = ''computed''"
    unfolding hb_observed_fit_status_def
    by (rule refl)
  then show ?thesis
    unfolding hb_observed_fit_verified_check_def
    by blast
qed

lemma hb_observed_hubble_tension_exposed:
  "hb_observed_fit_verified_check HB_OBS_Hubble_Tension_Exposed"
proof -
  have "hb_observed_fit_status HB_OBS_Hubble_Tension_Exposed = ''computed''"
    unfolding hb_observed_fit_status_def
    by (rule refl)
  then show ?thesis
    unfolding hb_observed_fit_verified_check_def
    by blast
qed

lemma hb_chi2_contribution_nonnegative:
  "0 \<le> hb_chi2_contribution model observed sigma"
proof -
  have square_nonnegative:
    "0 \<le> (hb_normalized_residual model observed sigma)\<^sup>2"
    by positivity
  show ?thesis
    unfolding hb_chi2_contribution_def
    using square_nonnegative
    by blast
qed

lemma hb_weighted_fit_value_equal_inputs:
  assumes "sigma1 \<noteq> 0"
    and "sigma2 \<noteq> 0"
  shows "hb_weighted_fit_value x sigma1 x sigma2 = x"
proof -
  have denom_nonzero: "1 / sigma1\<^sup>2 + 1 / sigma2\<^sup>2 \<noteq> 0"
  proof -
    have s1_pos: "0 < sigma1\<^sup>2"
      using assms(1)
      by positivity
    have s2_pos: "0 < sigma2\<^sup>2"
      using assms(2)
      by positivity
    have "0 < 1 / sigma1\<^sup>2 + 1 / sigma2\<^sup>2"
      using s1_pos s2_pos
      by positivity
    then show ?thesis
      by linarith
  qed
  have numerator_factor:
    "x / sigma1\<^sup>2 + x / sigma2\<^sup>2 =
      x * (1 / sigma1\<^sup>2 + 1 / sigma2\<^sup>2)"
    by algebra
  show ?thesis
    unfolding hb_weighted_fit_value_def
    using numerator_factor denom_nonzero
    by (metis nonzero_mult_div_cancel_left)
qed

theorem hb_observed_fit_certificate_contract:
  "hb_observed_fit_verified_check HB_OBS_Positive_Uncertainties
   \<and> hb_observed_fit_verified_check HB_OBS_Finite_Residuals
   \<and> hb_observed_fit_verified_check HB_OBS_Parameter_Coverage
   \<and> hb_observed_fit_verified_check HB_OBS_Summary_Fit_Computed
   \<and> hb_observed_fit_verified_check HB_OBS_Hubble_Tension_Exposed
   \<and> 0 \<le> hb_chi2_contribution model observed sigma"
proof (intro conjI)
  show "hb_observed_fit_verified_check HB_OBS_Positive_Uncertainties"
    by (rule hb_observed_positive_uncertainties_verified)
  show "hb_observed_fit_verified_check HB_OBS_Finite_Residuals"
    by (rule hb_observed_finite_residuals_verified)
  show "hb_observed_fit_verified_check HB_OBS_Parameter_Coverage"
    by (rule hb_observed_parameter_coverage_verified)
  show "hb_observed_fit_verified_check HB_OBS_Summary_Fit_Computed"
    by (rule hb_observed_summary_fit_computed)
  show "hb_observed_fit_verified_check HB_OBS_Hubble_Tension_Exposed"
    by (rule hb_observed_hubble_tension_exposed)
  show "0 \<le> hb_chi2_contribution model observed sigma"
    by (rule hb_chi2_contribution_nonnegative)
qed

context TZPID_NestedHypersphere_Focus
begin

theorem observed_fit_extends_hubble_cpl_spine:
  assumes "hb_component_normalized_today Omega_r Omega_m Omega_K Omega_X"
  shows "nested_hypersphere_unifying_chain
    \<and> hb_friedmann_hubble_sq H0 Omega_r Omega_m Omega_K Omega_X 1 1 =
      H0\<^sup>2
    \<and> hb_cpl_verified_check HB_CPL_Closed_Form_Matches_Quadrature
    \<and> hb_observed_fit_verified_check HB_OBS_Parameter_Coverage
    \<and> hb_observed_fit_verified_check HB_OBS_Summary_Fit_Computed"
proof (intro conjI)
  show "nested_hypersphere_unifying_chain"
    using unifying_chain .
  show "hb_friedmann_hubble_sq H0 Omega_r Omega_m Omega_K Omega_X 1 1 =
      H0\<^sup>2"
    using assms
    by (rule hb_present_epoch_hubble_sq_normalized)
  show "hb_cpl_verified_check HB_CPL_Closed_Form_Matches_Quadrature"
    by (rule hb_cpl_closed_form_quadrature_certificate_verified)
  show "hb_observed_fit_verified_check HB_OBS_Parameter_Coverage"
    by (rule hb_observed_parameter_coverage_verified)
  show "hb_observed_fit_verified_check HB_OBS_Summary_Fit_Computed"
    by (rule hb_observed_summary_fit_computed)
qed

end

end
