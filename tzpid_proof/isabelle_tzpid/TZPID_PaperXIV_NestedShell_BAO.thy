theory TZPID_PaperXIV_NestedShell_BAO
  imports Complex_Main "HOL-Analysis.Analysis"
begin

section \<open>Paper XIV: Nested Shell BAO Carriers\<close>

text \<open>
  Source-truth carrier for missing BAO/nested-shell equations minted from
  Paper XIV. The definitions formalize the BAO period, curvature mode
  spacing, modes-per-wiggle ratio, direct-shell exclusion radius, nested-shell
  beat epsilon, and degeneracy amplitude carriers.
\<close>

definition p14_bao_period :: "real => real" where
  "p14_bao_period rs = 2 * pi / rs"

definition p14_mode_spacing :: "real => real" where
  "p14_mode_spacing R = 1 / R"

definition p14_modes_per_wiggle :: "real => real => real" where
  "p14_modes_per_wiggle Rc rs = 2 * pi * Rc / rs"

definition p14_direct_shell_radius :: "real => real" where
  "p14_direct_shell_radius delta_k = 1 / delta_k"

definition p14_beat_spacing :: "real => real => real" where
  "p14_beat_spacing R epsilon = 1 / (R * epsilon)"

definition p14_beat_epsilon :: "real => real => real" where
  "p14_beat_epsilon Rc delta_k = 1 / (delta_k * Rc)"

definition p14_curved_ladder :: "real => real => real => real" where
  "p14_curved_ladder n ell R = sqrt (ell * (ell + n - 1)) / R"

definition p14_s3_degeneracy :: "real => real" where
  "p14_s3_degeneracy ell = (ell + 1)^2"

definition p14_s4_degeneracy :: "real => real" where
  "p14_s4_degeneracy ell = ((ell + 1) * (ell + 2) * (2 * ell + 3)) / 6"

definition p14_s5_degeneracy :: "real => real" where
  "p14_s5_degeneracy ell = ((ell + 1) * (ell + 2)^2 * (ell + 3)) / 12"

definition p14_power_envelope :: "real => real => real" where
  "p14_power_envelope amplitude degeneracy = amplitude * degeneracy"

definition p14_registered_ids :: "nat list" where
  "p14_registered_ids = [
  11616,
  11617,
  11618,
  11619,
  11620,
  11621,
  11622,
  11623,
  11624,
  11625,
  11626,
  11627,
  11628,
  11629,
  11630,
  11631,
  11632,
  11633,
  11634,
  11635,
  11636,
  11637,
  11638,
  11639,
  11640,
  11641,
  11642
  ]"

lemma p14_bao_over_mode_spacing:
  assumes "rs \<noteq> 0" "Rc \<noteq> 0"
  shows "p14_bao_period rs / p14_mode_spacing Rc = p14_modes_per_wiggle Rc rs"
  using assms by (simp add: p14_bao_period_def p14_mode_spacing_def p14_modes_per_wiggle_def)

lemma p14_direct_shell_radius_inverse:
  assumes "delta_k \<noteq> 0"
  shows "p14_direct_shell_radius delta_k * delta_k = 1"
  using assms by (simp add: p14_direct_shell_radius_def)

lemma p14_beat_spacing_epsilon_inverse:
  assumes "R \<noteq> 0" "epsilon \<noteq> 0"
  shows "p14_beat_spacing R epsilon * R * epsilon = 1"
  using assms by (simp add: p14_beat_spacing_def)

lemma p14_beat_epsilon_sets_bao_scale:
  assumes "Rc \<noteq> 0" "delta_k \<noteq> 0"
  shows "p14_beat_spacing Rc (p14_beat_epsilon Rc delta_k) = delta_k"
  using assms by (simp add: p14_beat_spacing_def p14_beat_epsilon_def)

lemma p14_s3_degeneracy_prefix:
  "map p14_s3_degeneracy [1,2,3,4,5] = [4,9,16,25,36]"
  by (simp add: p14_s3_degeneracy_def)

lemma p14_s4_degeneracy_prefix:
  "map p14_s4_degeneracy [1,2,3,4,5] = [5,14,30,55,91]"
  by (simp add: p14_s4_degeneracy_def)

lemma p14_s5_degeneracy_prefix:
  "map p14_s5_degeneracy [1,2,3,4,5] = [6,20,50,105,196]"
  by (simp add: p14_s5_degeneracy_def)

lemma p14_power_envelope_unfolds:
  "p14_power_envelope A d = A * d"
  by (simp add: p14_power_envelope_def)

lemma p14_registered_ids_nonempty:
  "p14_registered_ids \<noteq> []"
  by (simp add: p14_registered_ids_def)

end
