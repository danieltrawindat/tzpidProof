theory TZPID_GyromagneticMovement_SpatialBoundary
  imports TZPID_GyromagneticMovement_MHD_Helicity
begin

text \<open>
  Project: TZPID Proof Pipeline
  Creator: Daniel Alexander Trawin
  ORCID: https://orcid.org/0009-0001-4630-3715
  Generated UTC: 2026-06-08T00:00:00Z

  Phase 5.6 lift: spatial integral domains and boundary-condition
  semantics.  This is a finite/uniform-domain bridge, not yet a full
  PDE theorem over smooth manifolds.  It gives the proof pipeline a typed
  place for volume, boundary flux, closed-boundary guards, and helicity
  conservation rate.
\<close>

record gm_spatial_domain =
  gm_domain_volume :: real
  gm_boundary_area :: real

definition gm_positive_domain :: "gm_spatial_domain \<Rightarrow> bool" where
  "gm_positive_domain D \<longleftrightarrow>
    0 < gm_domain_volume D \<and> 0 \<le> gm_boundary_area D"

definition gm_spatial_helicity_integral ::
  "gm_spatial_domain \<Rightarrow> real \<Rightarrow> real" where
  "gm_spatial_helicity_integral D helicity_density =
    gm_domain_volume D * helicity_density"

definition gm_boundary_flux :: "gm_spatial_domain \<Rightarrow> real \<Rightarrow> real" where
  "gm_boundary_flux D normal_flux_density =
    gm_boundary_area D * normal_flux_density"

definition gm_closed_boundary :: "gm_spatial_domain \<Rightarrow> real \<Rightarrow> bool" where
  "gm_closed_boundary D normal_flux_density \<longleftrightarrow>
    gm_boundary_flux D normal_flux_density = 0"

definition gm_helicity_balance_rate :: "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real" where
  "gm_helicity_balance_rate eta current_norm_sq boundary_flux =
    - gm_resistive_helicity_dissipation eta current_norm_sq - boundary_flux"

definition gm_boundary_condition_admissible ::
  "gm_spatial_domain \<Rightarrow> real \<Rightarrow> bool" where
  "gm_boundary_condition_admissible D normal_flux_density \<longleftrightarrow>
    gm_positive_domain D \<and> gm_closed_boundary D normal_flux_density"

lemma positive_domain_has_nonzero_volume:
  assumes "gm_positive_domain D"
  shows "gm_domain_volume D \<noteq> 0"
proof -
  have "0 < gm_domain_volume D"
    using assms
    unfolding gm_positive_domain_def
    by blast
  then show ?thesis
    by linarith
qed

lemma spatial_helicity_integral_recovers_uniform_density:
  assumes "gm_domain_volume D \<noteq> 0"
  shows "gm_spatial_helicity_integral D density / gm_domain_volume D = density"
  unfolding gm_spatial_helicity_integral_def
  using assms
  by field

lemma closed_boundary_has_zero_flux:
  assumes "gm_closed_boundary D normal_flux_density"
  shows "gm_boundary_flux D normal_flux_density = 0"
  using assms
  unfolding gm_closed_boundary_def
  by blast

lemma admissible_boundary_has_zero_flux:
  assumes "gm_boundary_condition_admissible D normal_flux_density"
  shows "gm_boundary_flux D normal_flux_density = 0"
proof -
  have closed: "gm_closed_boundary D normal_flux_density"
    using assms
    unfolding gm_boundary_condition_admissible_def
    by blast
  show ?thesis
    using closed closed_boundary_has_zero_flux
    by blast
qed

lemma ideal_closed_domain_zero_helicity_rate:
  assumes "gm_ideal_mhd eta"
    and "gm_closed_boundary D normal_flux_density"
  shows "gm_helicity_balance_rate eta current_norm_sq
    (gm_boundary_flux D normal_flux_density) = 0"
proof -
  have dissipation_zero:
    "gm_resistive_helicity_dissipation eta current_norm_sq = 0"
    using assms(1) gm_ideal_mhd_zero_resistive_helicity_dissipation
    by blast
  have boundary_zero: "gm_boundary_flux D normal_flux_density = 0"
    using assms(2) closed_boundary_has_zero_flux
    by blast
  show ?thesis
    unfolding gm_helicity_balance_rate_def
    using dissipation_zero boundary_zero
    by algebra
qed

lemma admissible_ideal_domain_conserves_helicity_rate:
  assumes "gm_ideal_mhd eta"
    and "gm_boundary_condition_admissible D normal_flux_density"
  shows "gm_helicity_balance_rate eta current_norm_sq
    (gm_boundary_flux D normal_flux_density) = 0"
proof -
  have closed: "gm_closed_boundary D normal_flux_density"
    using assms(2)
    unfolding gm_boundary_condition_admissible_def
    by blast
  show ?thesis
    using assms(1) closed ideal_closed_domain_zero_helicity_rate
    by blast
qed

theorem phase5_6_spatial_boundary_lift_locked:
  assumes "partial_x_grad_y = partial_y_grad_x"
    and "gm_phase_vector_active gx gy"
    and "coupling \<noteq> 0"
    and "source_offset \<noteq> 0"
    and "phase_gradient = sqrt (gm_grad_mag_sq gx gy)"
    and "phase_gradient \<noteq> 0"
    and "gm_ideal_mhd eta"
    and "gm_mhd_elsasser_balance magnetic_force coriolis_force"
    and "energy = multiplier * abs helicity"
    and "gm_boundary_condition_admissible D normal_flux_density"
  shows "gm_curl_z partial_x_grad_y partial_y_grad_x = 0
    \<and> gm_Lz_witness phase_gradient source_offset coupling \<noteq> 0
    \<and> gm_helicity_balance_rate eta current_norm_sq
        (gm_boundary_flux D normal_flux_density) = 0
    \<and> elsasser_number magnetic_force coriolis_force = 1
    \<and> gm_woltjer_energy_guard energy multiplier helicity
    \<and> woltjer_helicity_residual energy helicity multiplier = 0
    \<and> gm_boundary_flux D normal_flux_density = 0
    \<and> phase5_curl_max_abs < 0.000000001"
proof -
  have mhd_lift:
    "gm_curl_z partial_x_grad_y partial_y_grad_x = 0
     \<and> gm_Lz_witness phase_gradient source_offset coupling \<noteq> 0
     \<and> gm_resistive_helicity_dissipation eta current_norm_sq = 0
     \<and> elsasser_number magnetic_force coriolis_force = 1
     \<and> gm_woltjer_energy_guard energy multiplier helicity
     \<and> woltjer_helicity_residual energy helicity multiplier = 0
     \<and> phase5_curl_max_abs < 0.000000001
     \<and> phase5_psi_unit_norm_max_error < 0.000000001"
    using assms(1-9) phase5_5_helicity_mhd_lift_locked
    by blast
  have conservation:
    "gm_helicity_balance_rate eta current_norm_sq
      (gm_boundary_flux D normal_flux_density) = 0"
    using assms(7,10) admissible_ideal_domain_conserves_helicity_rate
    by blast
  have boundary_zero: "gm_boundary_flux D normal_flux_density = 0"
    using assms(10) admissible_boundary_has_zero_flux
    by blast
  show ?thesis
    using mhd_lift conservation boundary_zero
    by blast
qed

end
