theory TZPID_PaperXVIII_StandingWaveEnlargement
  imports Complex_Main "HOL-Analysis.Analysis"
begin

section \<open>Paper XVIII: Standing-Wave Enlargement Carriers\<close>

text \<open>
  Source-truth carrier for missing equations minted from Paper XVIII. The
  definitions formalize comoving node enlargement, Hubble-radius recession,
  e-fold growth, no-signaling bookkeeping, and the projection term that is
  read as a dynamical dark-energy contribution.
\<close>

definition p18_sound_speed :: "real => real => real" where
  "p18_sound_speed c Rb = c / sqrt (3 * (1 + Rb))"

definition p18_hubble_rate :: "real => real => real" where
  "p18_hubble_rate Rdot R = Rdot / R"

definition p18_node_spacing :: "real => real => real" where
  "p18_node_spacing R dchi = R * dchi"

definition p18_node_growth :: "real => real => real" where
  "p18_node_growth H lambda = H * lambda"

definition p18_hubble_radius :: "real => real => real" where
  "p18_hubble_radius c H = c / H"

definition p18_superhubble_node :: "real => real => real => bool" where
  "p18_superhubble_node lambda c H = (lambda > p18_hubble_radius c H)"

definition p18_recession_speed :: "real => real => real" where
  "p18_recession_speed H D = H * D"

definition p18_exponential_radius :: "real => real => real" where
  "p18_exponential_radius Ri N = Ri * exp N"

definition p18_efolds :: "real => real => real" where
  "p18_efolds Rf Ri = ln (Rf / Ri)"

definition p18_projection_term :: "real => real => real" where
  "p18_projection_term alpha_dot cot_alpha = alpha_dot * cot_alpha"

definition p18_effective_expansion :: "real => real => real" where
  "p18_effective_expansion H projection = H + projection"

definition p18_dimensionless_node_ratio :: "real => real => real" where
  "p18_dimensionless_node_ratio lambda R = lambda / R"

definition p18_registered_ids :: "nat list" where
  "p18_registered_ids = [
  11729,
  11730,
  11731,
  11732,
  11733,
  11734,
  11735,
  11736,
  11737,
  11738,
  11739,
  11740,
  11741,
  11742,
  11743,
  11744,
  11745,
  11746,
  11747,
  11748,
  11749,
  11750,
  11751
  ]"

lemma p18_node_spacing_unfolds:
  "p18_node_spacing R dchi = R * dchi"
  by (simp add: p18_node_spacing_def)

lemma p18_node_growth_from_breathing:
  "p18_node_growth (p18_hubble_rate Rdot R) lambda = (Rdot / R) * lambda"
  by (simp add: p18_node_growth_def p18_hubble_rate_def)

lemma p18_superhubble_unfolds:
  "p18_superhubble_node lambda c H \<longleftrightarrow> lambda > c / H"
  by (simp add: p18_superhubble_node_def p18_hubble_radius_def)

lemma p18_superhubble_recession_exceeds_c:
  assumes "H > 0" and "D > c / H"
  shows "p18_recession_speed H D > c"
proof -
  have "H * D > H * (c / H)"
    using assms by (simp add: mult_strict_left_mono)
  then show ?thesis
    using assms by (simp add: p18_recession_speed_def)
qed

lemma p18_exponential_radius_ratio:
  assumes "Ri \<noteq> 0"
  shows "p18_exponential_radius Ri N / Ri = exp N"
  using assms by (simp add: p18_exponential_radius_def)

lemma p18_projection_zero_for_rigid_slice:
  "p18_projection_term 0 cot_alpha = 0"
  by (simp add: p18_projection_term_def)

lemma p18_effective_expansion_rigid_slice:
  "p18_effective_expansion H (p18_projection_term 0 cot_alpha) = H"
  by (simp add: p18_effective_expansion_def p18_projection_term_def)

lemma p18_dimensionless_shape_preserved:
  assumes "lambda = R * dchi" and "R \<noteq> 0"
  shows "p18_dimensionless_node_ratio lambda R = dchi"
  using assms by (simp add: p18_dimensionless_node_ratio_def)

lemma p18_registered_ids_nonempty:
  "p18_registered_ids \<noteq> []"
  by (simp add: p18_registered_ids_def)

end
