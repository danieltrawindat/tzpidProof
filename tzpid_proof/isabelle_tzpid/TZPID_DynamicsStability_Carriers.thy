theory TZPID_DynamicsStability_Carriers
  imports TZPID_Theorem_Semantic_Batch014_Dynamics_Stability_Followup
begin

text \<open>
  Project: TZPID Proof Pipeline
  Creator: Daniel Alexander Trawin
  ORCID: https://orcid.org/0009-0001-4630-3715
  Generated UTC: 2026-06-09

  Phase 2 dynamics/stability follow-up batch 014 upgrade.

  This carrier layer packages the stability follow-up rows as explicit
  margins and residuals: accumulated-force linearity, stationary flow,
  accumulation balance, global weak horizon, dissipative energy drop,
  local uniqueness radius, numerical tolerance, linear spectral stability,
  Newtonian recovery, and nonlinear dispersion amplitude shift.
\<close>

section \<open>Accumulation and Flow Carriers\<close>

definition dst_force_linearity_residual :: "real \<Rightarrow> real \<Rightarrow> real" where
  "dst_force_linearity_residual kernel source =
     accumulated_force_functional kernel source - kernel * source"

definition dst_stationary_flow_margin :: "real \<Rightarrow> real \<Rightarrow> real" where
  "dst_stationary_flow_margin next_state current_state =
     - abs (geometric_flow_residual next_state current_state)"

definition dst_accumulation_balance_residual ::
  "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real" where
  "dst_accumulation_balance_residual accumulated rate time =
     accumulation_dynamics_residual accumulated rate time"

definition dst_horizon_margin :: "real \<Rightarrow> real" where
  "dst_horizon_margin horizon = horizon"

section \<open>Stability Margin Carriers\<close>

definition dst_energy_drop_margin :: "real \<Rightarrow> real \<Rightarrow> real" where
  "dst_energy_drop_margin energy_after energy_before =
     energy_before - energy_after"

definition dst_uniqueness_margin :: "real \<Rightarrow> real \<Rightarrow> real" where
  "dst_uniqueness_margin local_scale uniqueness_radius =
     uniqueness_radius - local_scale"

definition dst_numerical_margin :: "real \<Rightarrow> real \<Rightarrow> real" where
  "dst_numerical_margin error tolerance = tolerance - abs error"

definition dst_spectral_stability_margin :: "real \<Rightarrow> real" where
  "dst_spectral_stability_margin spectral_radius = 1 - spectral_radius"

section \<open>Limit and Dispersion Carriers\<close>

definition dst_newtonian_recovery_residual :: "real \<Rightarrow> real \<Rightarrow> real" where
  "dst_newtonian_recovery_residual relativistic_value newtonian_value =
     newtonian_limit_residual relativistic_value newtonian_value"

definition dst_dispersion_shift_residual ::
  "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real" where
  "dst_dispersion_shift_residual shifted linear_frequency coefficient amplitude =
     shifted - nonlinear_dispersion_shift linear_frequency coefficient amplitude"

section \<open>Carrier Laws\<close>

theorem dst_force_linearity_residual_zero:
  "dst_force_linearity_residual kernel source = 0"
proof -
  show ?thesis
    unfolding dst_force_linearity_residual_def accumulated_force_functional_def
    by algebra
qed

theorem dst_stationary_flow_margin_zero:
  "dst_stationary_flow_margin state state = 0"
proof -
  have "geometric_flow_residual state state = 0"
    using id9999_geometric_flow_stationary_zero_residual .
  thus ?thesis
    unfolding dst_stationary_flow_margin_def
    by algebra
qed

theorem dst_accumulation_balance_residual_zero:
  assumes "accumulated = rate * time"
  shows "dst_accumulation_balance_residual accumulated rate time = 0"
proof -
  have "accumulation_dynamics_residual accumulated rate time = 0"
    using assms
    by (rule id9999_accumulation_dynamics_residual_zero)
  thus ?thesis
    unfolding dst_accumulation_balance_residual_def .
qed

theorem dst_horizon_margin_nonnegative:
  assumes "global_weak_existence_guard horizon"
  shows "0 \<le> dst_horizon_margin horizon"
proof -
  have "horizon \<ge> 0"
    using assms
    unfolding global_weak_existence_guard_def .
  thus ?thesis
    unfolding dst_horizon_margin_def .
qed

theorem dst_energy_drop_margin_nonnegative:
  assumes "dissipative_stability_guard energy_after energy_before"
  shows "0 \<le> dst_energy_drop_margin energy_after energy_before"
proof -
  have "energy_after \<le> energy_before"
    using assms
    unfolding dissipative_stability_guard_def .
  thus ?thesis
    unfolding dst_energy_drop_margin_def
    by linarith
qed

theorem dst_uniqueness_margin_nonnegative:
  assumes "logarithmic_local_uniqueness_guard local_scale uniqueness_radius"
  shows "0 \<le> dst_uniqueness_margin local_scale uniqueness_radius"
proof -
  have "local_scale \<le> uniqueness_radius"
    using assms
    unfolding logarithmic_local_uniqueness_guard_def .
  thus ?thesis
    unfolding dst_uniqueness_margin_def
    by linarith
qed

theorem dst_numerical_margin_nonnegative:
  assumes "numerical_stability_guard error tolerance"
  shows "0 \<le> dst_numerical_margin error tolerance"
proof -
  have "abs error \<le> tolerance"
    using assms
    unfolding numerical_stability_guard_def .
  thus ?thesis
    unfolding dst_numerical_margin_def
    by linarith
qed

theorem dst_spectral_stability_margin_nonnegative:
  assumes "linear_stability_guard spectral_radius"
  shows "0 \<le> dst_spectral_stability_margin spectral_radius"
proof -
  have "spectral_radius \<le> 1"
    using assms
    unfolding linear_stability_guard_def .
  thus ?thesis
    unfolding dst_spectral_stability_margin_def
    by linarith
qed

theorem dst_newtonian_recovery_residual_zero:
  "dst_newtonian_recovery_residual value value = 0"
proof -
  have "newtonian_limit_residual value value = 0"
    using id9999_newtonian_limit_recovery_zero_residual .
  thus ?thesis
    unfolding dst_newtonian_recovery_residual_def .
qed

theorem dst_zero_amplitude_dispersion_shift_residual_zero:
  "dst_dispersion_shift_residual linear_frequency linear_frequency coefficient 0 = 0"
proof -
  have "nonlinear_dispersion_shift linear_frequency coefficient 0 = linear_frequency"
    using id9999_nonlinear_dispersion_zero_amplitude .
  thus ?thesis
    unfolding dst_dispersion_shift_residual_def
    by algebra
qed

section \<open>Batch 014 Upgrade Contract\<close>

theorem dynamics_stability_carrier_contract:
  assumes accumulated_balance: "accumulated = rate * time"
    and horizon_guard: "global_weak_existence_guard horizon"
    and energy_guard: "dissipative_stability_guard energy_after energy_before"
    and uniqueness_guard:
      "logarithmic_local_uniqueness_guard local_scale uniqueness_radius"
    and numerical_guard: "numerical_stability_guard error tolerance"
    and spectral_guard: "linear_stability_guard spectral_radius"
  shows
    "dst_force_linearity_residual kernel source = 0
     \<and> dst_stationary_flow_margin state state = 0
     \<and> dst_accumulation_balance_residual accumulated rate time = 0
     \<and> 0 \<le> dst_horizon_margin horizon
     \<and> 0 \<le> dst_energy_drop_margin energy_after energy_before
     \<and> 0 \<le> dst_uniqueness_margin local_scale uniqueness_radius
     \<and> 0 \<le> dst_numerical_margin error tolerance
     \<and> 0 \<le> dst_spectral_stability_margin spectral_radius
     \<and> dst_newtonian_recovery_residual value value = 0
     \<and> dst_dispersion_shift_residual linear_frequency linear_frequency coefficient 0 = 0"
proof (intro conjI)
  show "dst_force_linearity_residual kernel source = 0"
    using dst_force_linearity_residual_zero .
  show "dst_stationary_flow_margin state state = 0"
    using dst_stationary_flow_margin_zero .
  show "dst_accumulation_balance_residual accumulated rate time = 0"
    using accumulated_balance
    by (rule dst_accumulation_balance_residual_zero)
  show "0 \<le> dst_horizon_margin horizon"
    using horizon_guard
    by (rule dst_horizon_margin_nonnegative)
  show "0 \<le> dst_energy_drop_margin energy_after energy_before"
    using energy_guard
    by (rule dst_energy_drop_margin_nonnegative)
  show "0 \<le> dst_uniqueness_margin local_scale uniqueness_radius"
    using uniqueness_guard
    by (rule dst_uniqueness_margin_nonnegative)
  show "0 \<le> dst_numerical_margin error tolerance"
    using numerical_guard
    by (rule dst_numerical_margin_nonnegative)
  show "0 \<le> dst_spectral_stability_margin spectral_radius"
    using spectral_guard
    by (rule dst_spectral_stability_margin_nonnegative)
  show "dst_newtonian_recovery_residual value value = 0"
    using dst_newtonian_recovery_residual_zero .
  show "dst_dispersion_shift_residual linear_frequency linear_frequency coefficient 0 = 0"
    using dst_zero_amplitude_dispersion_shift_residual_zero .
qed

end
