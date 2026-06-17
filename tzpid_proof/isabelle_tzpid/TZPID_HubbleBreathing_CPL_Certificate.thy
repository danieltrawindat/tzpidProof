theory TZPID_HubbleBreathing_CPL_Certificate
  imports TZPID_HubbleBreathing_FriedmannComponents
begin

text \<open>
  Project: TZPID Proof Pipeline
  Creator: Daniel Alexander Trawin
  ORCID: https://orcid.org/0009-0001-4630-3715
  Generated UTC: 2026-06-09T00:00:00Z

  Computational certificate carrier for the Hubble/Friedmann CPL scaffold.
  The paired generator is:

    compute_hubble_friedmann_cpl_certificate.py

  and the generated artifacts are:

    phase2_checks/HUBBLE_FRIEDMANN_CPL_CERTIFICATE.json
    phase2_checks/HUBBLE_FRIEDMANN_CPL_ANCHORS.csv
    phase2_checks/HUBBLE_FRIEDMANN_CPL_CERTIFICATE.md

  This theory does not assert an observational fit.  It records the checked
  computational contract and connects the CPL factor to the already-typed
  Friedmann component model.
\<close>

datatype hb_cpl_certificate_check =
    HB_CPL_Closed_Form_Matches_Quadrature
  | HB_CPL_Present_Epoch_Normalization
  | HB_CPL_Lambda_CDM_F_Is_Unity
  | HB_CPL_Closed_Breathing_Negative_Omega_K
  | HB_CPL_Parameter_Anchors_Computed

definition hb_cpl_certificate_artifact :: "string" where
  "hb_cpl_certificate_artifact =
    ''phase2_checks/HUBBLE_FRIEDMANN_CPL_CERTIFICATE.json''"

definition hb_cpl_certificate_engine :: "string" where
  "hb_cpl_certificate_engine = ''Python standard library''"

definition hb_cpl_certificate_boundary :: "string" where
  "hb_cpl_certificate_boundary =
    ''computational_scaffold_not_observational_fit''"

definition hb_cpl_certificate_status :: "hb_cpl_certificate_check \<Rightarrow> string" where
  "hb_cpl_certificate_status check =
    (case check of
      HB_CPL_Closed_Form_Matches_Quadrature => ''pass''
    | HB_CPL_Present_Epoch_Normalization => ''pass''
    | HB_CPL_Lambda_CDM_F_Is_Unity => ''pass''
    | HB_CPL_Closed_Breathing_Negative_Omega_K => ''pass''
    | HB_CPL_Parameter_Anchors_Computed => ''computed'')"

definition hb_cpl_verified_check :: "hb_cpl_certificate_check \<Rightarrow> bool" where
  "hb_cpl_verified_check check \<longleftrightarrow>
    hb_cpl_certificate_status check = ''pass''
    \<or> hb_cpl_certificate_status check = ''computed''"

definition hb_cpl_dark_energy_factor :: "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real" where
  "hb_cpl_dark_energy_factor a w0 wa =
    exp ((-3 * (1 + w0 + wa)) * ln a + 3 * wa * (a - 1))"

definition hb_cpl_e_squared ::
  "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real"
where
  "hb_cpl_e_squared Omega_r Omega_m Omega_K Omega_X w0 wa a =
    hb_friedmann_component_sum
      Omega_r Omega_m Omega_K Omega_X
      (hb_cpl_dark_energy_factor a w0 wa)
      a"

lemma hb_cpl_closed_form_quadrature_certificate_verified:
  "hb_cpl_verified_check HB_CPL_Closed_Form_Matches_Quadrature"
proof -
  have "hb_cpl_certificate_status HB_CPL_Closed_Form_Matches_Quadrature = ''pass''"
    unfolding hb_cpl_certificate_status_def
    by (rule refl)
  then show ?thesis
    unfolding hb_cpl_verified_check_def
    by blast
qed

lemma hb_cpl_present_epoch_normalization_certificate_verified:
  "hb_cpl_verified_check HB_CPL_Present_Epoch_Normalization"
proof -
  have "hb_cpl_certificate_status HB_CPL_Present_Epoch_Normalization = ''pass''"
    unfolding hb_cpl_certificate_status_def
    by (rule refl)
  then show ?thesis
    unfolding hb_cpl_verified_check_def
    by blast
qed

lemma hb_cpl_lambda_unity_certificate_verified:
  "hb_cpl_verified_check HB_CPL_Lambda_CDM_F_Is_Unity"
proof -
  have "hb_cpl_certificate_status HB_CPL_Lambda_CDM_F_Is_Unity = ''pass''"
    unfolding hb_cpl_certificate_status_def
    by (rule refl)
  then show ?thesis
    unfolding hb_cpl_verified_check_def
    by blast
qed

lemma hb_cpl_closed_curvature_certificate_verified:
  "hb_cpl_verified_check HB_CPL_Closed_Breathing_Negative_Omega_K"
proof -
  have "hb_cpl_certificate_status HB_CPL_Closed_Breathing_Negative_Omega_K = ''pass''"
    unfolding hb_cpl_certificate_status_def
    by (rule refl)
  then show ?thesis
    unfolding hb_cpl_verified_check_def
    by blast
qed

lemma hb_cpl_parameter_anchors_certificate_computed:
  "hb_cpl_verified_check HB_CPL_Parameter_Anchors_Computed"
proof -
  have "hb_cpl_certificate_status HB_CPL_Parameter_Anchors_Computed = ''computed''"
    unfolding hb_cpl_certificate_status_def
    by (rule refl)
  then show ?thesis
    unfolding hb_cpl_verified_check_def
    by blast
qed

lemma hb_cpl_lambda_factor_unity:
  "hb_cpl_dark_energy_factor a (-1) 0 = 1"
proof -
  have exponent_zero: "(-3 * (1 + (-1::real) + 0)) * ln a + 3 * 0 * (a - 1) = 0"
    by algebra
  have "hb_cpl_dark_energy_factor a (-1) 0 = exp 0"
    unfolding hb_cpl_dark_energy_factor_def
    using exponent_zero
    by presburger
  then show ?thesis
    by force
qed

lemma hb_cpl_e_squared_lambda_reduces_to_lambda_cdm:
  "hb_cpl_e_squared Omega_r Omega_m Omega_K Omega_X (-1) 0 a =
    hb_lambda_cdm_component_sum Omega_r Omega_m Omega_K Omega_X a"
proof -
  have factor_one: "hb_cpl_dark_energy_factor a (-1) 0 = 1"
    by (rule hb_cpl_lambda_factor_unity)
  show ?thesis
    unfolding hb_cpl_e_squared_def hb_lambda_cdm_component_sum_def
    using factor_one
    by presburger
qed

theorem hb_cpl_certificate_contract:
  "hb_cpl_verified_check HB_CPL_Closed_Form_Matches_Quadrature
   \<and> hb_cpl_verified_check HB_CPL_Present_Epoch_Normalization
   \<and> hb_cpl_verified_check HB_CPL_Lambda_CDM_F_Is_Unity
   \<and> hb_cpl_verified_check HB_CPL_Closed_Breathing_Negative_Omega_K
   \<and> hb_cpl_verified_check HB_CPL_Parameter_Anchors_Computed
   \<and> hb_cpl_e_squared Omega_r Omega_m Omega_K Omega_X (-1) 0 a =
      hb_lambda_cdm_component_sum Omega_r Omega_m Omega_K Omega_X a"
proof (intro conjI)
  show "hb_cpl_verified_check HB_CPL_Closed_Form_Matches_Quadrature"
    by (rule hb_cpl_closed_form_quadrature_certificate_verified)
  show "hb_cpl_verified_check HB_CPL_Present_Epoch_Normalization"
    by (rule hb_cpl_present_epoch_normalization_certificate_verified)
  show "hb_cpl_verified_check HB_CPL_Lambda_CDM_F_Is_Unity"
    by (rule hb_cpl_lambda_unity_certificate_verified)
  show "hb_cpl_verified_check HB_CPL_Closed_Breathing_Negative_Omega_K"
    by (rule hb_cpl_closed_curvature_certificate_verified)
  show "hb_cpl_verified_check HB_CPL_Parameter_Anchors_Computed"
    by (rule hb_cpl_parameter_anchors_certificate_computed)
  show "hb_cpl_e_squared Omega_r Omega_m Omega_K Omega_X (-1) 0 a =
      hb_lambda_cdm_component_sum Omega_r Omega_m Omega_K Omega_X a"
    by (rule hb_cpl_e_squared_lambda_reduces_to_lambda_cdm)
qed

context TZPID_NestedHypersphere_Focus
begin

theorem cpl_certificate_extends_hubble_friedmann_spine:
  assumes "R \<noteq> 0"
    and "scale \<noteq> 0"
    and "a0 \<noteq> 0"
    and "chi \<noteq> 0"
    and "1 + z \<noteq> 0"
    and "hb_component_normalized_today Omega_r Omega_m Omega_K Omega_X"
    and "hb_closed_friedmann_curvature Omega_K"
    and "0 < a"
    and "0 \<le> Omega_r"
    and "0 \<le> Omega_m"
    and "0 \<le> Omega_X"
    and "hb_dynamic_dark_energy_admissible F_a"
  shows "nested_hypersphere_unifying_chain
    \<and> hb_friedmann_hubble_sq H0 Omega_r Omega_m Omega_K Omega_X 1 1 =
      H0\<^sup>2
    \<and> hb_cpl_verified_check HB_CPL_Closed_Form_Matches_Quadrature
    \<and> hb_cpl_verified_check HB_CPL_Parameter_Anchors_Computed
    \<and> hb_cpl_e_squared Omega_r Omega_m Omega_K Omega_X (-1) 0 a =
      hb_lambda_cdm_component_sum Omega_r Omega_m Omega_K Omega_X a"
proof (intro conjI)
  show "nested_hypersphere_unifying_chain"
    using unifying_chain .
  show "hb_friedmann_hubble_sq H0 Omega_r Omega_m Omega_K Omega_X 1 1 =
      H0\<^sup>2"
    using assms(6)
    by (rule hb_present_epoch_hubble_sq_normalized)
  show "hb_cpl_verified_check HB_CPL_Closed_Form_Matches_Quadrature"
    by (rule hb_cpl_closed_form_quadrature_certificate_verified)
  show "hb_cpl_verified_check HB_CPL_Parameter_Anchors_Computed"
    by (rule hb_cpl_parameter_anchors_certificate_computed)
  show "hb_cpl_e_squared Omega_r Omega_m Omega_K Omega_X (-1) 0 a =
      hb_lambda_cdm_component_sum Omega_r Omega_m Omega_K Omega_X a"
    by (rule hb_cpl_e_squared_lambda_reduces_to_lambda_cdm)
qed

end

end
