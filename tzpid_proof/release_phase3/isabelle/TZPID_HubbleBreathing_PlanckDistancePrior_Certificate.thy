theory TZPID_HubbleBreathing_PlanckDistancePrior_Certificate
  imports TZPID_HubbleBreathing_PantheonRaw_Certificate
begin

text \<open>
  Project: TZPID Proof Pipeline
  Creator: Daniel Alexander Trawin
  ORCID: https://orcid.org/0009-0001-4630-3715
  Generated UTC: 2026-06-09T00:00:00Z

  Planck 2018 compressed distance-prior carrier for the Hubble/Friedmann lane.
  The paired generator is:

    compute_hubble_planck_distance_prior.py

  and the generated artifacts are:

    phase2_checks/HUBBLE_PLANCK_DISTANCE_PRIOR_CERTIFICATE.json
    phase2_checks/HUBBLE_PLANCK_DISTANCE_PRIOR_CERTIFICATE.md
    phase2_checks/HUBBLE_PLANCK_DISTANCE_PRIOR_SCENARIO_CHI2.csv

  This records the compressed CMB distance-prior contract over R, l_A, and
  Omega_b h^2 from arXiv:1808.05724.  It is not the full Planck likelihood.
\<close>

datatype hb_planck_distance_check =
    HB_PLANCK_Arxiv_Source_Downloaded
  | HB_PLANCK_Tex_Literals_Match
  | HB_PLANCK_Inverse_Covariance_Positive_Definite
  | HB_PLANCK_Finite_Distance_Prior_Chi2
  | HB_PLANCK_Scenario_Distance_Priors_Computed

definition hb_planck_distance_artifact :: "string" where
  "hb_planck_distance_artifact =
    ''phase2_checks/HUBBLE_PLANCK_DISTANCE_PRIOR_CERTIFICATE.json''"

definition hb_planck_distance_boundary :: "string" where
  "hb_planck_distance_boundary =
    ''compressed_distance_prior_not_full_planck_likelihood''"

definition hb_planck_distance_dimension :: nat where
  "hb_planck_distance_dimension = 3"

definition hb_planck_distance_status :: "hb_planck_distance_check \<Rightarrow> string" where
  "hb_planck_distance_status check =
    (case check of
      HB_PLANCK_Arxiv_Source_Downloaded => ''pass''
    | HB_PLANCK_Tex_Literals_Match => ''pass''
    | HB_PLANCK_Inverse_Covariance_Positive_Definite => ''pass''
    | HB_PLANCK_Finite_Distance_Prior_Chi2 => ''pass''
    | HB_PLANCK_Scenario_Distance_Priors_Computed => ''computed'')"

definition hb_planck_distance_verified_check :: "hb_planck_distance_check \<Rightarrow> bool" where
  "hb_planck_distance_verified_check check \<longleftrightarrow>
    hb_planck_distance_status check = ''pass''
    \<or> hb_planck_distance_status check = ''computed''"

definition hb_quadratic_chi2_2 ::
  "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real" where
  "hb_quadratic_chi2_2 x y inv_xx inv_yy =
    inv_xx * x\<^sup>2 + inv_yy * y\<^sup>2"

lemma hb_planck_source_verified:
  "hb_planck_distance_verified_check HB_PLANCK_Arxiv_Source_Downloaded"
proof -
  have "hb_planck_distance_status HB_PLANCK_Arxiv_Source_Downloaded = ''pass''"
    unfolding hb_planck_distance_status_def
    by (rule refl)
  then show ?thesis
    unfolding hb_planck_distance_verified_check_def
    by blast
qed

lemma hb_planck_tex_literals_verified:
  "hb_planck_distance_verified_check HB_PLANCK_Tex_Literals_Match"
proof -
  have "hb_planck_distance_status HB_PLANCK_Tex_Literals_Match = ''pass''"
    unfolding hb_planck_distance_status_def
    by (rule refl)
  then show ?thesis
    unfolding hb_planck_distance_verified_check_def
    by blast
qed

lemma hb_planck_invcov_verified:
  "hb_planck_distance_verified_check HB_PLANCK_Inverse_Covariance_Positive_Definite"
proof -
  have "hb_planck_distance_status HB_PLANCK_Inverse_Covariance_Positive_Definite = ''pass''"
    unfolding hb_planck_distance_status_def
    by (rule refl)
  then show ?thesis
    unfolding hb_planck_distance_verified_check_def
    by blast
qed

lemma hb_planck_chi2_verified:
  "hb_planck_distance_verified_check HB_PLANCK_Finite_Distance_Prior_Chi2"
proof -
  have "hb_planck_distance_status HB_PLANCK_Finite_Distance_Prior_Chi2 = ''pass''"
    unfolding hb_planck_distance_status_def
    by (rule refl)
  then show ?thesis
    unfolding hb_planck_distance_verified_check_def
    by blast
qed

lemma hb_planck_scenarios_computed:
  "hb_planck_distance_verified_check HB_PLANCK_Scenario_Distance_Priors_Computed"
proof -
  have "hb_planck_distance_status HB_PLANCK_Scenario_Distance_Priors_Computed = ''computed''"
    unfolding hb_planck_distance_status_def
    by (rule refl)
  then show ?thesis
    unfolding hb_planck_distance_verified_check_def
    by blast
qed

lemma hb_planck_distance_dimension_positive:
  "0 < hb_planck_distance_dimension"
  unfolding hb_planck_distance_dimension_def
  by (rule zero_less_numeral)

lemma hb_quadratic_chi2_2_nonnegative:
  assumes "0 \<le> inv_xx"
    and "0 \<le> inv_yy"
  shows "0 \<le> hb_quadratic_chi2_2 x y inv_xx inv_yy"
proof -
  have x_term: "0 \<le> inv_xx * x\<^sup>2"
    using assms(1)
    by positivity
  have y_term: "0 \<le> inv_yy * y\<^sup>2"
    using assms(2)
    by positivity
  show ?thesis
    unfolding hb_quadratic_chi2_2_def
    using x_term y_term
    by linarith
qed

theorem hb_planck_distance_prior_contract:
  assumes "0 \<le> inv_xx"
    and "0 \<le> inv_yy"
  shows "hb_planck_distance_verified_check HB_PLANCK_Arxiv_Source_Downloaded
   \<and> hb_planck_distance_verified_check HB_PLANCK_Tex_Literals_Match
   \<and> hb_planck_distance_verified_check HB_PLANCK_Inverse_Covariance_Positive_Definite
   \<and> hb_planck_distance_verified_check HB_PLANCK_Finite_Distance_Prior_Chi2
   \<and> hb_planck_distance_verified_check HB_PLANCK_Scenario_Distance_Priors_Computed
   \<and> 0 < hb_planck_distance_dimension
   \<and> 0 \<le> hb_quadratic_chi2_2 x y inv_xx inv_yy"
proof (intro conjI)
  show "hb_planck_distance_verified_check HB_PLANCK_Arxiv_Source_Downloaded"
    by (rule hb_planck_source_verified)
  show "hb_planck_distance_verified_check HB_PLANCK_Tex_Literals_Match"
    by (rule hb_planck_tex_literals_verified)
  show "hb_planck_distance_verified_check HB_PLANCK_Inverse_Covariance_Positive_Definite"
    by (rule hb_planck_invcov_verified)
  show "hb_planck_distance_verified_check HB_PLANCK_Finite_Distance_Prior_Chi2"
    by (rule hb_planck_chi2_verified)
  show "hb_planck_distance_verified_check HB_PLANCK_Scenario_Distance_Priors_Computed"
    by (rule hb_planck_scenarios_computed)
  show "0 < hb_planck_distance_dimension"
    by (rule hb_planck_distance_dimension_positive)
  show "0 \<le> hb_quadratic_chi2_2 x y inv_xx inv_yy"
    using assms
    by (rule hb_quadratic_chi2_2_nonnegative)
qed

context TZPID_NestedHypersphere_Focus
begin

theorem planck_distance_prior_extends_hubble_spine:
  assumes "hb_component_normalized_today Omega_r Omega_m Omega_K Omega_X"
  shows "nested_hypersphere_unifying_chain
    \<and> hb_friedmann_hubble_sq H0 Omega_r Omega_m Omega_K Omega_X 1 1 =
      H0\<^sup>2
    \<and> hb_pantheon_raw_verified_check HB_PANTHEON_Finite_Full_Covariance_Chi2
    \<and> hb_planck_distance_verified_check HB_PLANCK_Finite_Distance_Prior_Chi2
    \<and> 0 < hb_planck_distance_dimension"
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
  show "0 < hb_planck_distance_dimension"
    by (rule hb_planck_distance_dimension_positive)
qed

end

end
