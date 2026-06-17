theory TZPID_PaperXVII_wa_Derivation
  imports Complex_Main "HOL-Analysis.Analysis"
begin

section \<open>Paper XVII: w(a) Derivation Carriers\<close>

text \<open>
  Source-truth carrier for missing equations minted from Paper XVII. The
  definitions formalize the equation-of-state identity, quartic breathing
  slope, threshold handoff, CPL carriers, negative-foundation sign theorem,
  and Gauss-Bonnet normalization used by the paper.
\<close>

definition p17_eos_from_log_slope :: "real => real" where
  "p17_eos_from_log_slope slope = -1 - slope / 3"

definition p17_weff :: "real => real => real" where
  "p17_weff kappa x = -1 + kappa * (x - 1)"

definition p17_w0 :: "real => real => real" where
  "p17_w0 kappa x0 = -1 + kappa * (x0 - 1)"

definition p17_wa :: "real => real => real" where
  "p17_wa kappa x0 = 4 * kappa * x0"

definition p17_creation_rate :: "real => real => real => real" where
  "p17_creation_rate H rho f = 3 * H * rho * f"

definition p17_vacuum_energy :: "real => real => real => real" where
  "p17_vacuum_energy hbar c R = hbar * c / R^4"

definition p17_quartic_ratio :: "real => real => real" where
  "p17_quartic_ratio coeff a = coeff / a^4"

definition p17_gamma_from_foundation :: "real => real => real" where
  "p17_gamma_from_foundation gamma1 S = gamma1 * (-S)"

definition p17_mass_deficit_energy :: "real => real => real" where
  "p17_mass_deficit_energy m c = - m * c^2"

definition p17_stable_sink_potential :: "real => real => real" where
  "p17_stable_sink_potential kappa r = abs kappa * r^2"

definition p17_gauss_bonnet_s2 :: real where
  "p17_gauss_bonnet_s2 = 4 * pi"

definition p17_curvature_normalization :: real where
  "p17_curvature_normalization = (1 / 2) * p17_gauss_bonnet_s2"

definition p17_hopf_charge_selector :: nat where
  "p17_hopf_charge_selector = 1"

definition p17_s3_coupling_candidate :: real where
  "p17_s3_coupling_candidate = -4 / 9"

definition p17_registered_ids :: "nat list" where
  "p17_registered_ids = [
  11693,
  11694,
  11695,
  11696,
  11697,
  11698,
  11699,
  11700,
  11701,
  11702,
  11703,
  11704,
  11705,
  11706,
  11707,
  11708,
  11709,
  11710,
  11711,
  11712,
  11713,
  11714,
  11715,
  11716,
  11717,
  11718,
  11719,
  11720,
  11721,
  11722,
  11723,
  11724,
  11725,
  11726,
  11727,
  11728
  ]"

lemma p17_inverse_quartic_branch_is_radiation_like:
  "p17_eos_from_log_slope (-4) = 1 / 3"
  by (simp add: p17_eos_from_log_slope_def)

lemma p17_constant_branch_is_cosmological_constant:
  "p17_eos_from_log_slope 0 = -1"
  by (simp add: p17_eos_from_log_slope_def)

lemma p17_weff_unfolds:
  "p17_weff kappa x = -1 + kappa * (x - 1)"
  by (simp add: p17_weff_def)

lemma p17_w0_is_weff_at_x0:
  "p17_w0 kappa x0 = p17_weff kappa x0"
  by (simp add: p17_w0_def p17_weff_def)

lemma p17_wa_formula_unfolds:
  "p17_wa kappa x0 = 4 * kappa * x0"
  by (simp add: p17_wa_def)

lemma p17_negative_kappa_negative_wa:
  assumes "kappa < 0" and "x0 > 0"
  shows "p17_wa kappa x0 < 0"
proof -
  have "kappa * x0 < 0"
    using assms by (simp add: mult_less_0_iff)
  then show ?thesis
    by (simp add: p17_wa_def)
qed

lemma p17_negative_kappa_w0_above_minus_one:
  assumes "kappa < 0" and "x0 < 1"
  shows "p17_w0 kappa x0 > -1"
proof -
  have "x0 - 1 < 0"
    using assms by simp
  then have "0 < kappa * (x0 - 1)"
    using assms by (simp add: mult_neg_neg)
  then show ?thesis
    by (simp add: p17_w0_def)
qed

lemma p17_creation_rate_zero_when_response_zero:
  "p17_creation_rate H rho 0 = 0"
  by (simp add: p17_creation_rate_def)

lemma p17_quartic_ratio_unit:
  "p17_quartic_ratio coeff 1 = coeff"
  by (simp add: p17_quartic_ratio_def)

lemma p17_mass_deficit_energy_nonpositive:
  assumes "m >= 0" and "c >= 0"
  shows "p17_mass_deficit_energy m c <= 0"
  using assms by (simp add: p17_mass_deficit_energy_def)

lemma p17_stable_sink_potential_nonnegative:
  "p17_stable_sink_potential kappa r >= 0"
  by (simp add: p17_stable_sink_potential_def)

lemma p17_gauss_bonnet_normalization:
  "p17_curvature_normalization = 2 * pi"
  by (simp add: p17_curvature_normalization_def p17_gauss_bonnet_s2_def)

lemma p17_hopf_charge_is_unit:
  "p17_hopf_charge_selector = 1"
  by (simp add: p17_hopf_charge_selector_def)

lemma p17_candidate_coupling:
  "p17_s3_coupling_candidate = -4 / 9"
  by (simp add: p17_s3_coupling_candidate_def)

lemma p17_registered_ids_nonempty:
  "p17_registered_ids \<noteq> []"
  by (simp add: p17_registered_ids_def)

end
