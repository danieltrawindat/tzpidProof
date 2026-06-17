theory TZPID_MatterCreation_PressureEoS
  imports TZPID_MatterCreation_CriticalityBridge
begin

text \<open>
  Project: TZPID Proof Pipeline
  Creator: Daniel Alexander Trawin
  ORCID: https://orcid.org/0009-0001-4630-3715
  Generated UTC: 2026-06-09T00:00:00Z

  Matter creation pressure equation-of-state candidate.

  This layer gives ID10122 a concrete, conservative pressure carrier:

    p(rho_vac) = p0 + a (rho_vac - rho_c)^2
    p'(rho_vac) = 2 a (rho_vac - rho_c)

  It is a local Landau-style quadratic stationarity model.  Its formal role is
  to turn ID10117's dp / d rho_vac = 0 condition into an explicit stationary
  point contract at rho_vac = rho_c.  It is not yet a final physical equation
  of state for the whole framework.
\<close>

definition mc_quadratic_pressure ::
  "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real" where
  "mc_quadratic_pressure p0 a rho_c rho_vac =
    p0 + a * (rho_vac - rho_c)\<^sup>2"

definition mc_quadratic_pressure_derivative ::
  "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real" where
  "mc_quadratic_pressure_derivative a rho_c rho_vac =
    2 * a * (rho_vac - rho_c)"

definition mc_quadratic_pressure_gap ::
  "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real" where
  "mc_quadratic_pressure_gap a rho_c rho_vac =
    a * (rho_vac - rho_c)\<^sup>2"

lemma mc_quadratic_pressure_at_critical_density:
  shows "mc_quadratic_pressure p0 a rho_c rho_c = p0"
proof -
  have "(rho_c - rho_c)\<^sup>2 = 0"
    by algebra
  then show ?thesis
    unfolding mc_quadratic_pressure_def
    by algebra
qed

lemma mc_quadratic_pressure_derivative_zero_at_critical_density:
  shows "mc_quadratic_pressure_derivative a rho_c rho_c = 0"
proof -
  have "2 * a * (rho_c - rho_c) = 0"
    by algebra
  then show ?thesis
    unfolding mc_quadratic_pressure_derivative_def .
qed

lemma mc_quadratic_pressure_stationary_at_critical_density:
  shows "mc_pressure_stationary
    (mc_quadratic_pressure_derivative a rho_c) rho_c"
proof -
  have "mc_quadratic_pressure_derivative a rho_c rho_c = 0"
    by (rule mc_quadratic_pressure_derivative_zero_at_critical_density)
  then show ?thesis
    by (rule mc_pressure_stationary_from_zero_derivative)
qed

lemma mc_quadratic_pressure_gap_nonnegative:
  assumes "0 \<le> a"
  shows "0 \<le> mc_quadratic_pressure_gap a rho_c rho_vac"
proof -
  have square_nonnegative: "0 \<le> (rho_vac - rho_c)\<^sup>2"
    by (rule zero_le_power2)
  show ?thesis
    unfolding mc_quadratic_pressure_gap_def
    using assms square_nonnegative
    by (rule mult_nonneg_nonneg)
qed

lemma mc_quadratic_pressure_not_below_p0:
  assumes "0 \<le> a"
  shows "p0 \<le> mc_quadratic_pressure p0 a rho_c rho_vac"
proof -
  have gap_nonnegative: "0 \<le> mc_quadratic_pressure_gap a rho_c rho_vac"
    using assms
    by (rule mc_quadratic_pressure_gap_nonnegative)
  have "mc_quadratic_pressure p0 a rho_c rho_vac =
    p0 + mc_quadratic_pressure_gap a rho_c rho_vac"
    unfolding mc_quadratic_pressure_def mc_quadratic_pressure_gap_def .
  then show ?thesis
    using gap_nonnegative
    by linarith
qed

lemma mc_quadratic_pressure_value_matches_bridge:
  shows "mc_pressure_value (mc_quadratic_pressure p0 a rho_c) rho_vac =
    mc_quadratic_pressure p0 a rho_c rho_vac"
proof -
  show ?thesis
    by (rule mc_pressure_value_unfolds)
qed

theorem matter_creation_pressure_eos_stationary_contract:
  assumes split:
      "delta_rho_vac = rho_matter + rho_field"
    and nonnegative_curvature: "0 \<le> a"
  shows "mc_minimal_criticality_condition
      (mc_quadratic_pressure_derivative a rho_c)
      rho_c
      delta_rho_vac
      rho_matter
      rho_field
    \<and> mc_pressure_value (mc_quadratic_pressure p0 a rho_c) rho_c = p0
    \<and> p0 \<le> mc_quadratic_pressure p0 a rho_c rho_vac"
proof (intro conjI)
  have zero_derivative: "mc_quadratic_pressure_derivative a rho_c rho_c = 0"
    by (rule mc_quadratic_pressure_derivative_zero_at_critical_density)
  show "mc_minimal_criticality_condition
      (mc_quadratic_pressure_derivative a rho_c)
      rho_c
      delta_rho_vac
      rho_matter
      rho_field"
    using zero_derivative split
    by (rule mc_minimal_criticality_from_stationary_split)
  show "mc_pressure_value (mc_quadratic_pressure p0 a rho_c) rho_c = p0"
  proof -
    have "mc_pressure_value (mc_quadratic_pressure p0 a rho_c) rho_c =
      mc_quadratic_pressure p0 a rho_c rho_c"
      by (rule mc_pressure_value_unfolds)
    also have "... = p0"
      by (rule mc_quadratic_pressure_at_critical_density)
    finally show ?thesis .
  qed
  show "p0 \<le> mc_quadratic_pressure p0 a rho_c rho_vac"
    using nonnegative_curvature
    by (rule mc_quadratic_pressure_not_below_p0)
qed

end
