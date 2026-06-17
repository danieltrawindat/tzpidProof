theory TZPID_MatterCreation_TemporalFlow
  imports TZPID_MatterCreation_ThresholdSpine
begin

text \<open>
  Project: TZPID Proof Pipeline
  Creator: Daniel Alexander Trawin
  ORCID: https://orcid.org/0009-0001-4630-3715
  Generated UTC: 2026-06-09T00:00:00Z

  Matter creation temporal-flow upgrade.

  This layer adds a typed real-valued transfer carrier for the registry's
  emergence equations:

    rho_vac(t) = rho0 exp(-t / tau)
    J_emerge(t) = - d rho_vac / dt
    rho_matter(t) = A (1 - exp(-t / tau))

  The formal role is deliberately conservative: it records the closed-form
  transfer semantics needed by later executable certificates, while inheriting
  the pressure-threshold, density-gain, mass-energy, and curvature-source
  contract from TZPID_MatterCreation_ThresholdSpine.
\<close>

definition mc_vacuum_density_flow :: "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real" where
  "mc_vacuum_density_flow rho0 tau t = rho0 * exp (-(t / tau))"

definition mc_emergence_current :: "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real" where
  "mc_emergence_current rho0 tau t = (rho0 / tau) * exp (-(t / tau))"

definition mc_matter_density_flow :: "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real" where
  "mc_matter_density_flow amplitude tau t = amplitude * (1 - exp (-(t / tau)))"

definition mc_total_transfer_density ::
  "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real" where
  "mc_total_transfer_density rho0 amplitude tau t =
    mc_vacuum_density_flow rho0 tau t
    + mc_matter_density_flow amplitude tau t"

definition mc_closed_transfer_flow ::
  "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> bool" where
  "mc_closed_transfer_flow rho0 tau t \<longleftrightarrow>
    mc_total_transfer_density rho0 rho0 tau t = rho0"

lemma mc_vacuum_density_flow_positive:
  assumes "0 < rho0"
  shows "0 < mc_vacuum_density_flow rho0 tau t"
proof -
  have exp_positive: "0 < exp (-(t / tau))"
    by (rule exp_pos)
  show ?thesis
    unfolding mc_vacuum_density_flow_def
    using assms exp_positive
    by (rule mult_pos_pos)
qed

lemma mc_emergence_current_positive:
  assumes "0 < rho0"
    and "0 < tau"
  shows "0 < mc_emergence_current rho0 tau t"
proof -
  have ratio_positive: "0 < rho0 / tau"
    using assms
    by (rule divide_pos_pos)
  have exp_positive: "0 < exp (-(t / tau))"
    by (rule exp_pos)
  show ?thesis
    unfolding mc_emergence_current_def
    using ratio_positive exp_positive
    by (rule mult_pos_pos)
qed

lemma mc_equal_amplitude_transfer_conserved:
  shows "mc_total_transfer_density rho0 rho0 tau t = rho0"
proof -
  have "rho0 * exp (-(t / tau)) + rho0 * (1 - exp (-(t / tau))) = rho0"
    by algebra
  then show ?thesis
    unfolding mc_total_transfer_density_def
      mc_vacuum_density_flow_def
      mc_matter_density_flow_def .
qed

lemma mc_equal_amplitude_flow_closed:
  shows "mc_closed_transfer_flow rho0 tau t"
proof -
  have "mc_total_transfer_density rho0 rho0 tau t = rho0"
    by (rule mc_equal_amplitude_transfer_conserved)
  then show ?thesis
    unfolding mc_closed_transfer_flow_def .
qed

theorem matter_creation_temporal_flow_contract:
  assumes pressure_threshold: "p_crit \<le> p_vac"
    and density_order: "rho_before < rho_after"
    and mass_energy: "energy = mass * c\<^sup>2"
    and positive_g: "0 < g_eff"
    and positive_created_density: "0 < rho_after"
    and positive_rho0: "0 < rho0"
    and positive_tau: "0 < tau"
  shows "mc_thresholded_creation p_vac p_crit rho_before rho_after
    \<and> mc_mass_energy_locked energy mass c
    \<and> mc_created_density_sources_curvature g_eff rho_after
    \<and> 0 < mc_vacuum_density_flow rho0 tau t
    \<and> 0 < mc_emergence_current rho0 tau t
    \<and> mc_closed_transfer_flow rho0 tau t"
proof (intro conjI)
  show "mc_thresholded_creation p_vac p_crit rho_before rho_after"
    using pressure_threshold density_order
    by (rule mc_thresholded_creation_from_pressure_and_density)
  show "mc_mass_energy_locked energy mass c"
    using mass_energy
    by (rule mc_mass_energy_locked_from_identity)
  show "mc_created_density_sources_curvature g_eff rho_after"
    using positive_g positive_created_density
    by (rule mc_positive_curvature_source_from_positive_density)
  show "0 < mc_vacuum_density_flow rho0 tau t"
    using positive_rho0
    by (rule mc_vacuum_density_flow_positive)
  show "0 < mc_emergence_current rho0 tau t"
    using positive_rho0 positive_tau
    by (rule mc_emergence_current_positive)
  show "mc_closed_transfer_flow rho0 tau t"
    by (rule mc_equal_amplitude_flow_closed)
qed

context TZPID_EnergyMatter_Focus
begin

theorem temporal_flow_extends_energy_matter_spine:
  assumes pressure_threshold: "p_crit \<le> p_vac"
    and density_order: "rho_before < rho_after"
    and mass_energy: "energy = mass * c\<^sup>2"
    and positive_g: "0 < g_eff"
    and positive_created_density: "0 < rho_after"
    and positive_rho0: "0 < rho0"
    and positive_tau: "0 < tau"
  shows "energy_to_matter_spine_chain
    \<and> matter_creation_pressure_threshold EM_P_vac EM_P_crit
    \<and> mass_energy_equivalence EM_energy EM_mass
    \<and> created_matter_curvature_source EM_Phi EM_G_eff EM_rho_matter
    \<and> mc_thresholded_creation p_vac p_crit rho_before rho_after
    \<and> 0 < mc_emergence_current rho0 tau t
    \<and> mc_closed_transfer_flow rho0 tau t"
proof (intro conjI)
  show "energy_to_matter_spine_chain"
    using energy_to_matter_chain .
  show "matter_creation_pressure_threshold EM_P_vac EM_P_crit"
    using id0188_creation_threshold .
  show "mass_energy_equivalence EM_energy EM_mass"
    using id2846_mass_energy .
  show "created_matter_curvature_source EM_Phi EM_G_eff EM_rho_matter"
    using id1816_curvature_source .
  show "mc_thresholded_creation p_vac p_crit rho_before rho_after"
    using pressure_threshold density_order
    by (rule mc_thresholded_creation_from_pressure_and_density)
  show "0 < mc_emergence_current rho0 tau t"
    using positive_rho0 positive_tau
    by (rule mc_emergence_current_positive)
  show "mc_closed_transfer_flow rho0 tau t"
    by (rule mc_equal_amplitude_flow_closed)
qed

end

end
