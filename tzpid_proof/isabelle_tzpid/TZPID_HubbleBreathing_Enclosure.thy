theory TZPID_HubbleBreathing_Enclosure
  imports
    TZPID_NestedHypersphere_S3_Spectrum
    TZPID_Einstein_Focus
begin

text \<open>
  Project: TZPID Proof Pipeline
  Creator: Daniel Alexander Trawin
  ORCID: https://orcid.org/0009-0001-4630-3715
  Generated UTC: 2026-06-08T00:00:00Z

  Hubble-breathing bridge for the nested hyperspherical enclosure spine.
  This file records the algebraic core of hyper-universality.txt and
  TZPID_HUBBLE_BREATHING_OF_THE_ENCLOSURE.md:

    H = Rdot / R
    D = R * chi
    Ddot = Rdot * chi = H * D
    V_S3 = 2*pi^2*R^3
    Vdot/V = 3*Rdot/R = 3H
    rho_Lambda scale law rho = k/R^4

  The observational cosmology claims remain certificate-level context.  This
  HOL layer proves the exact scale-radius algebra used by the spine.
\<close>

definition hb_hubble_rate :: "real \<Rightarrow> real \<Rightarrow> real" where
  "hb_hubble_rate R Rdot = Rdot / R"

definition hb_proper_distance :: "real \<Rightarrow> real \<Rightarrow> real" where
  "hb_proper_distance R chi = R * chi"

definition hb_recession_velocity :: "real \<Rightarrow> real \<Rightarrow> real" where
  "hb_recession_velocity Rdot chi = Rdot * chi"

definition hb_s3_volume :: "real \<Rightarrow> real" where
  "hb_s3_volume R = 2 * pi\<^sup>2 * R\<^sup>3"

definition hb_s3_volume_rate :: "real \<Rightarrow> real \<Rightarrow> real" where
  "hb_s3_volume_rate R Rdot = 6 * pi\<^sup>2 * R\<^sup>2 * Rdot"

definition hb_fractional_volume_rate :: "real \<Rightarrow> real \<Rightarrow> real" where
  "hb_fractional_volume_rate R Rdot =
    hb_s3_volume_rate R Rdot / hb_s3_volume R"

definition hb_inverse_fourth_density :: "real \<Rightarrow> real \<Rightarrow> real" where
  "hb_inverse_fourth_density k R = k / R\<^sup>4"

definition hb_vacuum_energy_rate :: "real \<Rightarrow> real \<Rightarrow> real" where
  "hb_vacuum_energy_rate rho volume_rate = rho * volume_rate"

definition hb_closed_curvature_parameter :: "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real" where
  "hb_closed_curvature_parameter k c R H =
    - k * c\<^sup>2 / (R\<^sup>2 * H\<^sup>2)"

lemma hb_hubble_law_from_breathing:
  assumes "R \<noteq> 0"
  shows "hb_recession_velocity Rdot chi =
    hb_hubble_rate R Rdot * hb_proper_distance R chi"
proof -
  show ?thesis
    unfolding hb_recession_velocity_def hb_hubble_rate_def
      hb_proper_distance_def
    using assms
    by field
qed

lemma hb_s3_volume_positive:
  assumes "0 < R"
  shows "0 < hb_s3_volume R"
proof -
  have pi_pos: "0 < pi"
    using pi_gt_zero .
  have "0 < 2 * pi\<^sup>2 * R\<^sup>3"
    using assms pi_pos
    by positivity
  then show ?thesis
    unfolding hb_s3_volume_def .
qed

lemma hb_s3_fractional_volume_rate:
  assumes "R \<noteq> 0"
  shows "hb_fractional_volume_rate R Rdot =
    3 * hb_hubble_rate R Rdot"
proof -
  have pi_nonzero: "pi \<noteq> 0"
    using pi_gt_zero
    by linarith
  show ?thesis
    unfolding hb_fractional_volume_rate_def hb_s3_volume_rate_def
      hb_s3_volume_def hb_hubble_rate_def
    using assms pi_nonzero
    by field
qed

lemma hb_breathing_expands_volume_when_Rdot_positive:
  assumes "0 < R"
    and "0 < Rdot"
  shows "0 < hb_s3_volume_rate R Rdot"
proof -
  have pi_pos: "0 < pi"
    using pi_gt_zero .
  show ?thesis
    unfolding hb_s3_volume_rate_def
    using assms pi_pos
    by positivity
qed

lemma hb_inverse_fourth_density_scales:
  assumes "R \<noteq> 0"
    and "scale \<noteq> 0"
  shows "hb_inverse_fourth_density k (scale * R) =
    hb_inverse_fourth_density k R / scale\<^sup>4"
proof -
  have scale4_nonzero: "scale\<^sup>4 \<noteq> 0"
    using assms(2)
    by positivity
  have R4_nonzero: "R\<^sup>4 \<noteq> 0"
    using assms(1)
    by positivity
  show ?thesis
    unfolding hb_inverse_fourth_density_def
    using scale4_nonzero R4_nonzero
    by field
qed

lemma hb_vacuum_energy_rate_positive:
  assumes "0 < rho"
    and "0 < volume_rate"
  shows "0 < hb_vacuum_energy_rate rho volume_rate"
  unfolding hb_vacuum_energy_rate_def
  using assms
  by positivity

lemma hb_closed_positive_curvature_has_negative_omega_K:
  assumes "0 < k"
    and "c \<noteq> 0"
    and "R \<noteq> 0"
    and "H \<noteq> 0"
  shows "hb_closed_curvature_parameter k c R H < 0"
proof -
  have denom_pos: "0 < R\<^sup>2 * H\<^sup>2"
    using assms(3,4)
    by positivity
  have numer_pos: "0 < k * c\<^sup>2"
    using assms(1,2)
    by positivity
  show ?thesis
    unfolding hb_closed_curvature_parameter_def
    using denom_pos numer_pos
    by (metis divide_minus_left divide_pos_pos neg_0_less_iff_less)
qed

theorem hb_enclosure_breathing_contract:
  assumes "R \<noteq> 0"
    and "scale \<noteq> 0"
  shows "hb_recession_velocity Rdot chi =
      hb_hubble_rate R Rdot * hb_proper_distance R chi
    \<and> hb_fractional_volume_rate R Rdot =
      3 * hb_hubble_rate R Rdot
    \<and> hb_inverse_fourth_density k (scale * R) =
      hb_inverse_fourth_density k R / scale\<^sup>4"
proof (intro conjI)
  show "hb_recession_velocity Rdot chi =
      hb_hubble_rate R Rdot * hb_proper_distance R chi"
    using assms(1)
    by (rule hb_hubble_law_from_breathing)
  show "hb_fractional_volume_rate R Rdot =
      3 * hb_hubble_rate R Rdot"
    using assms(1)
    by (rule hb_s3_fractional_volume_rate)
  show "hb_inverse_fourth_density k (scale * R) =
      hb_inverse_fourth_density k R / scale\<^sup>4"
    using assms
    by (rule hb_inverse_fourth_density_scales)
qed

context TZPID_NestedHypersphere_Focus
begin

theorem hubble_breathing_extends_nested_hypersphere_spine:
  assumes "R \<noteq> 0"
    and "scale \<noteq> 0"
  shows "nested_hypersphere_unifying_chain
    \<and> hb_recession_velocity Rdot chi =
      hb_hubble_rate R Rdot * hb_proper_distance R chi
    \<and> hb_fractional_volume_rate R Rdot =
      3 * hb_hubble_rate R Rdot
    \<and> hb_inverse_fourth_density k (scale * R) =
      hb_inverse_fourth_density k R / scale\<^sup>4"
proof (intro conjI)
  show "nested_hypersphere_unifying_chain"
    using unifying_chain .
  show "hb_recession_velocity Rdot chi =
      hb_hubble_rate R Rdot * hb_proper_distance R chi"
    using assms(1)
    by (rule hb_hubble_law_from_breathing)
  show "hb_fractional_volume_rate R Rdot =
      3 * hb_hubble_rate R Rdot"
    using assms(1)
    by (rule hb_s3_fractional_volume_rate)
  show "hb_inverse_fourth_density k (scale * R) =
      hb_inverse_fourth_density k R / scale\<^sup>4"
    using assms
    by (rule hb_inverse_fourth_density_scales)
qed

end

end
