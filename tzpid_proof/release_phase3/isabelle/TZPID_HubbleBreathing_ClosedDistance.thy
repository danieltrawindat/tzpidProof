theory TZPID_HubbleBreathing_ClosedDistance
  imports TZPID_HubbleBreathing_Enclosure
begin

text \<open>
  Project: TZPID Proof Pipeline
  Creator: Daniel Alexander Trawin
  ORCID: https://orcid.org/0009-0001-4630-3715
  Generated UTC: 2026-06-08T00:00:00Z

  Closed-distance fingerprint for the Hubble-breathing enclosure bridge.
  The previous file locks the breathing algebra H = Rdot/R and Vdot/V = 3H.
  This file records the observational geometry:

    flat transverse distance   uses chi
    closed S3 transverse form uses sin chi

  The exact algebraic fingerprint is therefore the replacement:

    chi  ->  sin chi.

  Small-angle/local-flat convergence is kept in the certificate layer as an
  established analytic approximation; here we prove exact formula relations
  and residual identities.
\<close>

definition hb_flat_transverse_distance :: "real \<Rightarrow> real \<Rightarrow> real" where
  "hb_flat_transverse_distance a0 chi = a0 * chi"

definition hb_closed_transverse_distance :: "real \<Rightarrow> real \<Rightarrow> real" where
  "hb_closed_transverse_distance a0 chi = a0 * sin chi"

definition hb_flat_angular_diameter_distance ::
  "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real" where
  "hb_flat_angular_diameter_distance a0 chi z =
    hb_flat_transverse_distance a0 chi / (1 + z)"

definition hb_closed_angular_diameter_distance ::
  "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real" where
  "hb_closed_angular_diameter_distance a0 chi z =
    hb_closed_transverse_distance a0 chi / (1 + z)"

definition hb_closed_distance_residual ::
  "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real" where
  "hb_closed_distance_residual a0 chi z =
    hb_closed_angular_diameter_distance a0 chi z -
    hb_flat_angular_diameter_distance a0 chi z"

definition hb_curvature_fingerprint :: "real \<Rightarrow> real" where
  "hb_curvature_fingerprint chi = sin chi - chi"

definition hb_luminosity_distance_from_angular ::
  "real \<Rightarrow> real \<Rightarrow> real" where
  "hb_luminosity_distance_from_angular angular_distance z =
    (1 + z)\<^sup>2 * angular_distance"

lemma hb_closed_transverse_replaces_chi_by_sin:
  "hb_closed_transverse_distance a0 chi = a0 * sin chi"
  unfolding hb_closed_transverse_distance_def
  by (rule refl)

lemma hb_flat_transverse_uses_chi:
  "hb_flat_transverse_distance a0 chi = a0 * chi"
  unfolding hb_flat_transverse_distance_def
  by (rule refl)

lemma hb_closed_distance_residual_closed_form:
  assumes "1 + z \<noteq> 0"
  shows "hb_closed_distance_residual a0 chi z =
    a0 * (sin chi - chi) / (1 + z)"
proof -
  show ?thesis
    unfolding hb_closed_distance_residual_def
      hb_closed_angular_diameter_distance_def
      hb_flat_angular_diameter_distance_def
      hb_closed_transverse_distance_def
      hb_flat_transverse_distance_def
    using assms
    by field
qed

lemma hb_closed_equals_flat_when_sin_equals_chi:
  assumes "sin chi = chi"
  shows "hb_closed_angular_diameter_distance a0 chi z =
    hb_flat_angular_diameter_distance a0 chi z"
  unfolding hb_closed_angular_diameter_distance_def
    hb_flat_angular_diameter_distance_def
    hb_closed_transverse_distance_def
    hb_flat_transverse_distance_def
  using assms
  by algebra

lemma hb_closed_flat_ratio:
  assumes "a0 \<noteq> 0"
    and "chi \<noteq> 0"
    and "1 + z \<noteq> 0"
  shows "hb_closed_angular_diameter_distance a0 chi z /
    hb_flat_angular_diameter_distance a0 chi z = sin chi / chi"
proof -
  have flat_nonzero:
    "hb_flat_angular_diameter_distance a0 chi z \<noteq> 0"
    unfolding hb_flat_angular_diameter_distance_def
      hb_flat_transverse_distance_def
    using assms
    by force
  show ?thesis
    unfolding hb_closed_angular_diameter_distance_def
      hb_flat_angular_diameter_distance_def
      hb_closed_transverse_distance_def
      hb_flat_transverse_distance_def
    using assms flat_nonzero
    by field
qed

lemma hb_curvature_fingerprint_zero_iff_sin_equals_chi:
  "hb_curvature_fingerprint chi = 0 \<longleftrightarrow> sin chi = chi"
  unfolding hb_curvature_fingerprint_def
  by algebra

lemma hb_closed_distance_residual_zero_iff_fingerprint_zero:
  assumes "a0 \<noteq> 0"
    and "1 + z \<noteq> 0"
  shows "hb_closed_distance_residual a0 chi z = 0 \<longleftrightarrow>
    hb_curvature_fingerprint chi = 0"
proof -
  have residual:
    "hb_closed_distance_residual a0 chi z =
      a0 * (sin chi - chi) / (1 + z)"
    using assms(2)
    by (rule hb_closed_distance_residual_closed_form)
  show ?thesis
    unfolding hb_curvature_fingerprint_def
    using residual assms
    by field
qed

lemma hb_distance_duality_relation:
  "hb_luminosity_distance_from_angular
      (hb_closed_angular_diameter_distance a0 chi z) z =
    (1 + z)\<^sup>2 * hb_closed_angular_diameter_distance a0 chi z"
  unfolding hb_luminosity_distance_from_angular_def
  by (rule refl)

theorem hb_closed_distance_fingerprint_contract:
  assumes "a0 \<noteq> 0"
    and "chi \<noteq> 0"
    and "1 + z \<noteq> 0"
  shows "hb_closed_distance_residual a0 chi z =
      a0 * hb_curvature_fingerprint chi / (1 + z)
    \<and> hb_closed_angular_diameter_distance a0 chi z /
      hb_flat_angular_diameter_distance a0 chi z = sin chi / chi
    \<and> (hb_closed_distance_residual a0 chi z = 0 \<longleftrightarrow>
      hb_curvature_fingerprint chi = 0)"
proof (intro conjI)
  show "hb_closed_distance_residual a0 chi z =
      a0 * hb_curvature_fingerprint chi / (1 + z)"
    unfolding hb_curvature_fingerprint_def
    using assms(3)
    by (rule hb_closed_distance_residual_closed_form)
  show "hb_closed_angular_diameter_distance a0 chi z /
      hb_flat_angular_diameter_distance a0 chi z = sin chi / chi"
    using assms
    by (rule hb_closed_flat_ratio)
  show "hb_closed_distance_residual a0 chi z = 0 \<longleftrightarrow>
      hb_curvature_fingerprint chi = 0"
    using assms(1,3)
    by (rule hb_closed_distance_residual_zero_iff_fingerprint_zero)
qed

context TZPID_NestedHypersphere_Focus
begin

theorem closed_distance_extends_hubble_breathing_spine:
  assumes "R \<noteq> 0"
    and "scale \<noteq> 0"
    and "a0 \<noteq> 0"
    and "chi \<noteq> 0"
    and "1 + z \<noteq> 0"
  shows "nested_hypersphere_unifying_chain
    \<and> hb_recession_velocity Rdot chi =
      hb_hubble_rate R Rdot * hb_proper_distance R chi
    \<and> hb_fractional_volume_rate R Rdot =
      3 * hb_hubble_rate R Rdot
    \<and> hb_closed_distance_residual a0 chi z =
      a0 * hb_curvature_fingerprint chi / (1 + z)
    \<and> hb_closed_angular_diameter_distance a0 chi z /
      hb_flat_angular_diameter_distance a0 chi z = sin chi / chi"
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
  show "hb_closed_distance_residual a0 chi z =
      a0 * hb_curvature_fingerprint chi / (1 + z)"
    unfolding hb_curvature_fingerprint_def
    using assms(5)
    by (rule hb_closed_distance_residual_closed_form)
  show "hb_closed_angular_diameter_distance a0 chi z /
      hb_flat_angular_diameter_distance a0 chi z = sin chi / chi"
    using assms(3,4,5)
    by (rule hb_closed_flat_ratio)
qed

end

end
