theory TZPID_PaperXVI_VolumetricBuoyancy
  imports Complex_Main "HOL-Analysis.Analysis"
begin

section \<open>Paper XVI: Volumetric Buoyancy Carriers\<close>

text \<open>
  Source-truth carrier for missing equations minted from Paper XVI.  The
  definitions formalize the three-phase occupancy constraint, phase volume
  abstraction, exclusion energy, domain-wall profile, volumetric force balance,
  Elsasser criticality, Hodge/helicity diagnostics, and scaling boundary.
\<close>

definition p16_occupancy_sum :: "real => real => real => real" where
  "p16_occupancy_sum phi_b phi_T phi_E = phi_b + phi_T + phi_E"

definition p16_occupancy_closed :: "real => real => real => bool" where
  "p16_occupancy_closed phi_b phi_T phi_E = (p16_occupancy_sum phi_b phi_T phi_E = 1)"

definition p16_phase_volume :: "real => real => real" where
  "p16_phase_volume phi total_volume = phi * total_volume"

definition p16_quartic_exclusion :: "real => real => real => real => real => real => real" where
  "p16_quartic_exclusion chi12 chi13 chi23 phi1 phi2 phi3 =
    chi12 * phi1 * phi2 + chi13 * phi1 * phi3 + chi23 * phi2 * phi3"

definition p16_domain_wall_profile :: "real => real => real => real" where
  "p16_domain_wall_profile amp s ell = amp * (1 / cosh (s / ell))^2"

definition p16_force_balance :: "real => real => real => real => real => real => real" where
  "p16_force_balance lorentz coriolis grav pressure interface viscous =
    lorentz - coriolis + grav + pressure + interface - viscous"

definition p16_elsasser :: "real => real => real => real => real => real" where
  "p16_elsasser B mu0 rho eta Omega = B^2 / (mu0 * rho * eta * Omega)"

definition p16_elsasser_equilibrium_field :: "real => real => real => real => real" where
  "p16_elsasser_equilibrium_field mu0 rho eta Omega = sqrt (mu0 * rho * eta * Omega)"

definition p16_hodge_sum :: "real => real => real => real" where
  "p16_hodge_sum exact coexact harmonic = exact + coexact + harmonic"

definition p16_helicity_density :: "real => real => real" where
  "p16_helicity_density A B = A * B"

definition p16_recycling_invariant :: "real => real => real => real" where
  "p16_recycling_invariant HM lambda_g Hac = HM + (1 / lambda_g) * Hac"

definition p16_nested_mode_density :: "real => real => real => real" where
  "p16_nested_mode_density coeff R = coeff / R^4"

definition p16_vacuum_mode_density :: "real => real => real => real => real" where
  "p16_vacuum_mode_density hbar c R = hbar * c / R^4"

definition p16_registered_ids :: "nat list" where
  "p16_registered_ids = [
  11671,
  11672,
  11673,
  11674,
  11675,
  11676,
  11677,
  11678,
  11679,
  11680,
  11681,
  11682,
  11683,
  11684,
  11685,
  11686,
  11687,
  11688,
  11689,
  11690,
  11691,
  11692
  ]"

lemma p16_occupancy_closed_unfolds:
  "p16_occupancy_closed phi_b phi_T phi_E \<longleftrightarrow> phi_b + phi_T + phi_E = 1"
  by (simp add: p16_occupancy_closed_def p16_occupancy_sum_def)

lemma p16_phase_volume_partition:
  assumes "p16_occupancy_closed phi_b phi_T phi_E"
  shows "p16_phase_volume phi_b V + p16_phase_volume phi_T V + p16_phase_volume phi_E V = V"
  using assms by (simp add: p16_occupancy_closed_def p16_occupancy_sum_def p16_phase_volume_def algebra_simps)

lemma p16_quartic_exclusion_zero_for_single_phase:
  "p16_quartic_exclusion c12 c13 c23 1 0 0 = 0"
  by (simp add: p16_quartic_exclusion_def)

lemma p16_domain_wall_center_value:
  assumes "ell \<noteq> 0"
  shows "p16_domain_wall_profile amp 0 ell = amp"
  using assms by (simp add: p16_domain_wall_profile_def)

lemma p16_force_balance_closes:
  assumes "viscous = lorentz - coriolis + grav + pressure + interface"
  shows "p16_force_balance lorentz coriolis grav pressure interface viscous = 0"
  using assms by (simp add: p16_force_balance_def)

lemma p16_elsasser_critical_field:
  assumes "mu0 * rho * eta * Omega > 0"
  shows "p16_elsasser (p16_elsasser_equilibrium_field mu0 rho eta Omega) mu0 rho eta Omega = 1"
  using assms by (simp add: p16_elsasser_def p16_elsasser_equilibrium_field_def)

lemma p16_hodge_sum_unfolds:
  "p16_hodge_sum exact coexact harmonic = exact + coexact + harmonic"
  by (simp add: p16_hodge_sum_def)

lemma p16_recycling_invariant_unfolds:
  "p16_recycling_invariant HM lambda_g Hac = HM + (1 / lambda_g) * Hac"
  by (simp add: p16_recycling_invariant_def)

lemma p16_vacuum_mode_density_is_nested_density:
  "p16_vacuum_mode_density hbar c R = p16_nested_mode_density (hbar * c) R"
  by (simp add: p16_vacuum_mode_density_def p16_nested_mode_density_def)

lemma p16_registered_ids_nonempty:
  "p16_registered_ids \<noteq> []"
  by (simp add: p16_registered_ids_def)

end
