theory TZPID_HubbleBreathing_FriedmannComponents
  imports TZPID_HubbleBreathing_ClosedDistance
begin

text \<open>
  Project: TZPID Proof Pipeline
  Creator: Daniel Alexander Trawin
  ORCID: https://orcid.org/0009-0001-4630-3715
  Generated UTC: 2026-06-08T00:00:00Z

  Friedmann component layer for the Hubble-breathing enclosure bridge.
  This promotes the certificate equation

    H^2(a) = H0^2 [
      Omega_r a^-4 + Omega_m a^-3 + Omega_K a^-2 + Omega_X F(a)
    ]

  into typed HOL algebra.  The dynamic dark-energy factor F(a) remains an
  explicit input to avoid pretending the observational fit has been proved.
  The algebraic role is now formal: component decomposition, LambdaCDM
  reduction when F=1, present-epoch normalization at a=1, and negative closed
  curvature contribution when Omega_K < 0.
\<close>

definition hb_radiation_component :: "real \<Rightarrow> real \<Rightarrow> real" where
  "hb_radiation_component Omega_r a = Omega_r / a\<^sup>4"

definition hb_matter_component :: "real \<Rightarrow> real \<Rightarrow> real" where
  "hb_matter_component Omega_m a = Omega_m / a\<^sup>3"

definition hb_curvature_component :: "real \<Rightarrow> real \<Rightarrow> real" where
  "hb_curvature_component Omega_K a = Omega_K / a\<^sup>2"

definition hb_dynamic_dark_energy_component ::
  "real \<Rightarrow> real \<Rightarrow> real" where
  "hb_dynamic_dark_energy_component Omega_X F_a = Omega_X * F_a"

definition hb_friedmann_component_sum ::
  "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real" where
  "hb_friedmann_component_sum Omega_r Omega_m Omega_K Omega_X F_a a =
    hb_radiation_component Omega_r a +
    hb_matter_component Omega_m a +
    hb_curvature_component Omega_K a +
    hb_dynamic_dark_energy_component Omega_X F_a"

definition hb_friedmann_hubble_sq ::
  "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real" where
  "hb_friedmann_hubble_sq H0 Omega_r Omega_m Omega_K Omega_X F_a a =
    H0\<^sup>2 * hb_friedmann_component_sum Omega_r Omega_m Omega_K Omega_X F_a a"

definition hb_lambda_cdm_component_sum ::
  "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real" where
  "hb_lambda_cdm_component_sum Omega_r Omega_m Omega_K Omega_Lambda a =
    hb_friedmann_component_sum Omega_r Omega_m Omega_K Omega_Lambda 1 a"

definition hb_component_normalized_today ::
  "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> bool" where
  "hb_component_normalized_today Omega_r Omega_m Omega_K Omega_X \<longleftrightarrow>
    Omega_r + Omega_m + Omega_K + Omega_X = 1"

definition hb_closed_friedmann_curvature :: "real \<Rightarrow> bool" where
  "hb_closed_friedmann_curvature Omega_K \<longleftrightarrow> Omega_K < 0"

definition hb_dynamic_dark_energy_admissible :: "real \<Rightarrow> bool" where
  "hb_dynamic_dark_energy_admissible F_a \<longleftrightarrow> 0 \<le> F_a"

definition hb_cpl_equation_of_state :: "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real" where
  "hb_cpl_equation_of_state w0 wa a = w0 + wa * (1 - a)"

lemma hb_lambda_cdm_is_dynamic_case_F_one:
  "hb_lambda_cdm_component_sum Omega_r Omega_m Omega_K Omega_Lambda a =
    hb_friedmann_component_sum Omega_r Omega_m Omega_K Omega_Lambda 1 a"
  unfolding hb_lambda_cdm_component_sum_def
  by (rule refl)

lemma hb_present_epoch_component_sum:
  "hb_friedmann_component_sum Omega_r Omega_m Omega_K Omega_X 1 1 =
    Omega_r + Omega_m + Omega_K + Omega_X"
  unfolding hb_friedmann_component_sum_def
    hb_radiation_component_def
    hb_matter_component_def
    hb_curvature_component_def
    hb_dynamic_dark_energy_component_def
  by norm_num

lemma hb_present_epoch_normalized_sum_is_one:
  assumes "hb_component_normalized_today Omega_r Omega_m Omega_K Omega_X"
  shows "hb_friedmann_component_sum Omega_r Omega_m Omega_K Omega_X 1 1 = 1"
proof -
  have sum_eq: "Omega_r + Omega_m + Omega_K + Omega_X = 1"
    using assms
    unfolding hb_component_normalized_today_def
    by blast
  show ?thesis
    using hb_present_epoch_component_sum sum_eq
    by presburger
qed

lemma hb_present_epoch_hubble_sq_normalized:
  assumes "hb_component_normalized_today Omega_r Omega_m Omega_K Omega_X"
  shows "hb_friedmann_hubble_sq H0 Omega_r Omega_m Omega_K Omega_X 1 1 =
    H0\<^sup>2"
proof -
  have component_one:
    "hb_friedmann_component_sum Omega_r Omega_m Omega_K Omega_X 1 1 = 1"
    using assms
    by (rule hb_present_epoch_normalized_sum_is_one)
  show ?thesis
    unfolding hb_friedmann_hubble_sq_def
    using component_one
    by algebra
qed

lemma hb_closed_curvature_component_negative:
  assumes "hb_closed_friedmann_curvature Omega_K"
    and "a \<noteq> 0"
  shows "hb_curvature_component Omega_K a < 0"
proof -
  have omega_negative: "Omega_K < 0"
    using assms(1)
    unfolding hb_closed_friedmann_curvature_def
    by blast
  have denom_positive: "0 < a\<^sup>2"
    using assms(2)
    by positivity
  show ?thesis
    unfolding hb_curvature_component_def
    using omega_negative denom_positive
    by (metis divide_neg_pos)
qed

lemma hb_components_nonnegative_for_positive_scale_factor:
  assumes "0 \<le> Omega_r"
    and "0 \<le> Omega_m"
    and "0 \<le> Omega_X"
    and "hb_dynamic_dark_energy_admissible F_a"
    and "0 < a"
  shows "0 \<le> hb_radiation_component Omega_r a
    \<and> 0 \<le> hb_matter_component Omega_m a
    \<and> 0 \<le> hb_dynamic_dark_energy_component Omega_X F_a"
proof (intro conjI)
  have a4_pos: "0 < a\<^sup>4"
    using assms(5)
    by positivity
  show "0 \<le> hb_radiation_component Omega_r a"
    unfolding hb_radiation_component_def
    using assms(1) a4_pos
    by (metis divide_nonneg_pos)
  have a3_pos: "0 < a\<^sup>3"
    using assms(5)
    by positivity
  show "0 \<le> hb_matter_component Omega_m a"
    unfolding hb_matter_component_def
    using assms(2) a3_pos
    by (metis divide_nonneg_pos)
  have F_nonnegative: "0 \<le> F_a"
    using assms(4)
    unfolding hb_dynamic_dark_energy_admissible_def
    by blast
  show "0 \<le> hb_dynamic_dark_energy_component Omega_X F_a"
    unfolding hb_dynamic_dark_energy_component_def
    using assms(3) F_nonnegative
    by positivity
qed

lemma hb_cpl_constant_when_wa_zero:
  "hb_cpl_equation_of_state w0 0 a = w0"
  unfolding hb_cpl_equation_of_state_def
  by algebra

lemma hb_cpl_present_epoch_value:
  "hb_cpl_equation_of_state w0 wa 1 = w0"
  unfolding hb_cpl_equation_of_state_def
  by algebra

theorem hb_friedmann_dynamic_component_contract:
  assumes "hb_component_normalized_today Omega_r Omega_m Omega_K Omega_X"
    and "hb_closed_friedmann_curvature Omega_K"
    and "0 < a"
    and "0 \<le> Omega_r"
    and "0 \<le> Omega_m"
    and "0 \<le> Omega_X"
    and "hb_dynamic_dark_energy_admissible F_a"
  shows "hb_friedmann_hubble_sq H0 Omega_r Omega_m Omega_K Omega_X 1 1 =
      H0\<^sup>2
    \<and> hb_curvature_component Omega_K a < 0
    \<and> 0 \<le> hb_radiation_component Omega_r a
    \<and> 0 \<le> hb_matter_component Omega_m a
    \<and> 0 \<le> hb_dynamic_dark_energy_component Omega_X F_a
    \<and> hb_lambda_cdm_component_sum Omega_r Omega_m Omega_K Omega_X a =
      hb_friedmann_component_sum Omega_r Omega_m Omega_K Omega_X 1 a"
proof (intro conjI)
  show "hb_friedmann_hubble_sq H0 Omega_r Omega_m Omega_K Omega_X 1 1 =
      H0\<^sup>2"
    using assms(1)
    by (rule hb_present_epoch_hubble_sq_normalized)
  show "hb_curvature_component Omega_K a < 0"
    using assms(2) assms(3)
    unfolding hb_closed_friedmann_curvature_def
    by (metis hb_closed_curvature_component_negative less_irrefl zero_less_iff_neq_zero)
  have nonnegative_components:
    "0 \<le> hb_radiation_component Omega_r a
     \<and> 0 \<le> hb_matter_component Omega_m a
     \<and> 0 \<le> hb_dynamic_dark_energy_component Omega_X F_a"
    using assms(4,5,6,7,3)
    by (rule hb_components_nonnegative_for_positive_scale_factor)
  show "0 \<le> hb_radiation_component Omega_r a"
    using nonnegative_components
    by blast
  show "0 \<le> hb_matter_component Omega_m a"
    using nonnegative_components
    by blast
  show "0 \<le> hb_dynamic_dark_energy_component Omega_X F_a"
    using nonnegative_components
    by blast
  show "hb_lambda_cdm_component_sum Omega_r Omega_m Omega_K Omega_X a =
      hb_friedmann_component_sum Omega_r Omega_m Omega_K Omega_X 1 a"
    using hb_lambda_cdm_is_dynamic_case_F_one .
qed

context TZPID_NestedHypersphere_Focus
begin

theorem friedmann_components_extend_hubble_breathing_spine:
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
    \<and> hb_fractional_volume_rate R Rdot =
      3 * hb_hubble_rate R Rdot
    \<and> hb_closed_distance_residual a0 chi z =
      a0 * hb_curvature_fingerprint chi / (1 + z)
    \<and> hb_friedmann_hubble_sq H0 Omega_r Omega_m Omega_K Omega_X 1 1 =
      H0\<^sup>2
    \<and> hb_curvature_component Omega_K a < 0"
proof (intro conjI)
  show "nested_hypersphere_unifying_chain"
    using unifying_chain .
  show "hb_fractional_volume_rate R Rdot =
      3 * hb_hubble_rate R Rdot"
    using assms(1)
    by (rule hb_s3_fractional_volume_rate)
  show "hb_closed_distance_residual a0 chi z =
      a0 * hb_curvature_fingerprint chi / (1 + z)"
    unfolding hb_curvature_fingerprint_def
    using assms(5)
    by (rule hb_closed_distance_residual_closed_form)
  show "hb_friedmann_hubble_sq H0 Omega_r Omega_m Omega_K Omega_X 1 1 =
      H0\<^sup>2"
    using assms(6)
    by (rule hb_present_epoch_hubble_sq_normalized)
  show "hb_curvature_component Omega_K a < 0"
    using assms(7) assms(8)
    unfolding hb_closed_friedmann_curvature_def
    by (metis hb_closed_curvature_component_negative less_irrefl zero_less_iff_neq_zero)
qed

end

end
