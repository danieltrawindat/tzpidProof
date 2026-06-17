theory TZPID_MatterCreation_CriticalityBridge
  imports TZPID_MatterCreation_TemporalFlow
begin

text \<open>
  Project: TZPID Proof Pipeline
  Creator: Daniel Alexander Trawin
  ORCID: https://orcid.org/0009-0001-4630-3715
  Generated UTC: 2026-06-09T00:00:00Z

  Matter creation criticality bridge.

  This layer connects the temporal-flow carrier to the registry's minimal
  criticality statement:

    ID10117: dp / d rho_vac = 0, Delta rho_vac -> rho_matter + rho_field.
    ID10122: p(rho_vac) is the pressure function evaluated on vacuum density.

  We represent the pressure derivative as an explicit real function p_deriv.
  That keeps the theorem honest: this is a typed stationarity/split contract,
  not yet a proof from a concrete pressure equation of state.
\<close>

definition mc_pressure_value :: "(real \<Rightarrow> real) \<Rightarrow> real \<Rightarrow> real" where
  "mc_pressure_value pressure rho_vac = pressure rho_vac"

definition mc_pressure_stationary ::
  "(real \<Rightarrow> real) \<Rightarrow> real \<Rightarrow> bool" where
  "mc_pressure_stationary pressure_derivative rho_vac \<longleftrightarrow>
    pressure_derivative rho_vac = 0"

definition mc_vacuum_density_split ::
  "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> bool" where
  "mc_vacuum_density_split delta_rho_vac rho_matter rho_field \<longleftrightarrow>
    delta_rho_vac = rho_matter + rho_field"

definition mc_minimal_criticality_condition ::
  "(real \<Rightarrow> real) \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> bool" where
  "mc_minimal_criticality_condition pressure_derivative rho_vac
      delta_rho_vac rho_matter rho_field \<longleftrightarrow>
    mc_pressure_stationary pressure_derivative rho_vac
    \<and> mc_vacuum_density_split delta_rho_vac rho_matter rho_field"

definition mc_temporal_vacuum_loss :: "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real" where
  "mc_temporal_vacuum_loss rho0 tau t =
    rho0 - mc_vacuum_density_flow rho0 tau t"

definition mc_temporal_split_condition ::
  "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> bool" where
  "mc_temporal_split_condition rho0 tau t rho_matter rho_field \<longleftrightarrow>
    mc_vacuum_density_split
      (mc_temporal_vacuum_loss rho0 tau t)
      rho_matter
      rho_field"

lemma mc_pressure_value_unfolds:
  shows "mc_pressure_value pressure rho_vac = pressure rho_vac"
proof -
  show ?thesis
    unfolding mc_pressure_value_def .
qed

lemma mc_pressure_stationary_from_zero_derivative:
  assumes "pressure_derivative rho_vac = 0"
  shows "mc_pressure_stationary pressure_derivative rho_vac"
proof -
  show ?thesis
    using assms
    unfolding mc_pressure_stationary_def .
qed

lemma mc_vacuum_density_split_from_sum:
  assumes "delta_rho_vac = rho_matter + rho_field"
  shows "mc_vacuum_density_split delta_rho_vac rho_matter rho_field"
proof -
  show ?thesis
    using assms
    unfolding mc_vacuum_density_split_def .
qed

lemma mc_minimal_criticality_from_stationary_split:
  assumes "pressure_derivative rho_vac = 0"
    and "delta_rho_vac = rho_matter + rho_field"
  shows "mc_minimal_criticality_condition pressure_derivative rho_vac
    delta_rho_vac rho_matter rho_field"
proof -
  have stationary: "mc_pressure_stationary pressure_derivative rho_vac"
    using assms(1)
    by (rule mc_pressure_stationary_from_zero_derivative)
  have split: "mc_vacuum_density_split delta_rho_vac rho_matter rho_field"
    using assms(2)
    by (rule mc_vacuum_density_split_from_sum)
  show ?thesis
    unfolding mc_minimal_criticality_condition_def
    using stationary split
    by blast
qed

lemma mc_temporal_loss_equals_equal_amplitude_matter_channel:
  shows "mc_temporal_vacuum_loss rho0 tau t =
    mc_matter_density_flow rho0 tau t"
proof -
  have "rho0 - rho0 * exp (-(t / tau)) =
    rho0 * (1 - exp (-(t / tau)))"
    by algebra
  then show ?thesis
    unfolding mc_temporal_vacuum_loss_def
      mc_vacuum_density_flow_def
      mc_matter_density_flow_def .
qed

lemma mc_temporal_split_into_matter_only:
  shows "mc_temporal_split_condition rho0 tau t
    (mc_matter_density_flow rho0 tau t) 0"
proof -
  have loss: "mc_temporal_vacuum_loss rho0 tau t =
    mc_matter_density_flow rho0 tau t"
    by (rule mc_temporal_loss_equals_equal_amplitude_matter_channel)
  have "mc_temporal_vacuum_loss rho0 tau t =
    mc_matter_density_flow rho0 tau t + 0"
    using loss
    by algebra
  then have "mc_vacuum_density_split
    (mc_temporal_vacuum_loss rho0 tau t)
    (mc_matter_density_flow rho0 tau t)
    0"
    by (rule mc_vacuum_density_split_from_sum)
  then show ?thesis
    unfolding mc_temporal_split_condition_def .
qed

theorem matter_creation_criticality_bridge_contract:
  assumes pressure_zero: "pressure_derivative rho_vac = 0"
    and pressure_threshold: "p_crit \<le> p_vac"
    and density_order: "rho_before < rho_after"
    and mass_energy: "energy = mass * c\<^sup>2"
    and positive_g: "0 < g_eff"
    and positive_created_density: "0 < rho_after"
    and positive_rho0: "0 < rho0"
    and positive_tau: "0 < tau"
  shows "mc_minimal_criticality_condition pressure_derivative rho_vac
      (mc_temporal_vacuum_loss rho0 tau t)
      (mc_matter_density_flow rho0 tau t)
      0
    \<and> matter_creation_temporal_flow_contract p_crit p_vac rho_before
      rho_after energy mass c g_eff rho0 tau t"
proof (intro conjI)
  have temporal_split:
    "mc_temporal_split_condition rho0 tau t
      (mc_matter_density_flow rho0 tau t) 0"
    by (rule mc_temporal_split_into_matter_only)
  have split:
    "mc_vacuum_density_split
      (mc_temporal_vacuum_loss rho0 tau t)
      (mc_matter_density_flow rho0 tau t)
      0"
    using temporal_split
    unfolding mc_temporal_split_condition_def .
  have stationary: "mc_pressure_stationary pressure_derivative rho_vac"
    using pressure_zero
    by (rule mc_pressure_stationary_from_zero_derivative)
  show "mc_minimal_criticality_condition pressure_derivative rho_vac
      (mc_temporal_vacuum_loss rho0 tau t)
      (mc_matter_density_flow rho0 tau t)
      0"
    unfolding mc_minimal_criticality_condition_def
    using stationary split
    by blast
  show "matter_creation_temporal_flow_contract p_crit p_vac rho_before
      rho_after energy mass c g_eff rho0 tau t"
    using pressure_threshold density_order mass_energy positive_g
      positive_created_density positive_rho0 positive_tau
    by (rule matter_creation_temporal_flow_contract)
qed

end
