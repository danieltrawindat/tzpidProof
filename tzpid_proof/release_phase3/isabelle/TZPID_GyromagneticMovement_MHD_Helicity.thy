theory TZPID_GyromagneticMovement_MHD_Helicity
  imports
    TZPID_GyromagneticMovement_VectorCalculus
    TZPID_Theorem_Semantic_Batch011_Magnetic_Torsion
begin

text \<open>
  Project: TZPID Proof Pipeline
  Creator: Daniel Alexander Trawin
  ORCID: https://orcid.org/0009-0001-4630-3715
  Generated UTC: 2026-06-08T00:00:00Z

  This is the Phase 5.5 lift from exact-gradient vector calculus into
  helicity and MHD-style gyromagnetic semantics.  It remains algebraic,
  but it introduces the correct typed objects: vector potential, magnetic
  field, helicity density, resistive helicity dissipation, and Elsasser
  balance.
\<close>

definition gm_dot3 ::
  "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real" where
  "gm_dot3 ax ay az bx by bz = ax * bx + ay * by + az * bz"

definition gm_vector_component_total :: "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real" where
  "gm_vector_component_total dipole gyro induced = dipole + gyro + induced"

definition gm_helicity_density ::
  "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real" where
  "gm_helicity_density ax ay az bx by bz = gm_dot3 ax ay az bx by bz"

definition gm_uniform_helicity_integral :: "real \<Rightarrow> real \<Rightarrow> real" where
  "gm_uniform_helicity_integral volume density = volume * density"

definition gm_resistive_helicity_dissipation :: "real \<Rightarrow> real \<Rightarrow> real" where
  "gm_resistive_helicity_dissipation eta current_norm_sq = 2 * eta * current_norm_sq"

definition gm_ideal_mhd :: "real \<Rightarrow> bool" where
  "gm_ideal_mhd eta \<longleftrightarrow> eta = 0"

definition gm_mhd_elsasser_balance :: "real \<Rightarrow> real \<Rightarrow> bool" where
  "gm_mhd_elsasser_balance magnetic_force coriolis_force \<longleftrightarrow>
    magnetic_force = coriolis_force \<and> coriolis_force \<noteq> 0"

definition gm_woltjer_energy_guard :: "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> bool" where
  "gm_woltjer_energy_guard energy multiplier helicity \<longleftrightarrow>
    multiplier * abs helicity \<le> energy"

lemma gm_dot3_zero_magnetic_field:
  "gm_dot3 ax ay az 0 0 0 = 0"
  unfolding gm_dot3_def
  by algebra

lemma gm_helicity_density_zero_when_magnetic_field_zero:
  "gm_helicity_density ax ay az 0 0 0 = 0"
  unfolding gm_helicity_density_def
  using gm_dot3_zero_magnetic_field
  by blast

lemma gm_total_vector_component_decomposition_recovers_sum:
  "gm_vector_component_total dipole gyro induced - dipole - gyro = induced"
  unfolding gm_vector_component_total_def
  by algebra

lemma gm_uniform_helicity_integral_zero_density:
  "gm_uniform_helicity_integral volume 0 = 0"
  unfolding gm_uniform_helicity_integral_def
  by algebra

lemma gm_ideal_mhd_zero_resistive_helicity_dissipation:
  assumes "gm_ideal_mhd eta"
  shows "gm_resistive_helicity_dissipation eta current_norm_sq = 0"
  unfolding gm_ideal_mhd_def gm_resistive_helicity_dissipation_def
  using assms
  by algebra

lemma gm_mhd_elsasser_balance_gives_unit_elsasser:
  assumes "gm_mhd_elsasser_balance magnetic_force coriolis_force"
  shows "elsasser_number magnetic_force coriolis_force = 1"
proof -
  have eq_force: "magnetic_force = coriolis_force"
    using assms
    unfolding gm_mhd_elsasser_balance_def
    by blast
  have nonzero: "coriolis_force \<noteq> 0"
    using assms
    unfolding gm_mhd_elsasser_balance_def
    by blast
  show ?thesis
    unfolding elsasser_number_def
    using eq_force nonzero
    by field
qed

lemma gm_woltjer_guard_nonnegative_residual:
  assumes "gm_woltjer_energy_guard energy multiplier helicity"
  shows "0 \<le> woltjer_helicity_residual energy helicity multiplier"
  unfolding gm_woltjer_energy_guard_def woltjer_helicity_residual_def
  using assms
  by linarith

lemma gm_woltjer_guard_balanced_residual_zero:
  assumes "energy = multiplier * abs helicity"
  shows "gm_woltjer_energy_guard energy multiplier helicity
    \<and> woltjer_helicity_residual energy helicity multiplier = 0"
proof -
  have guard: "gm_woltjer_energy_guard energy multiplier helicity"
    unfolding gm_woltjer_energy_guard_def
    using assms
    by linarith
  have residual_zero: "woltjer_helicity_residual energy helicity multiplier = 0"
    using assms woltjer_helicity_residual_balanced_zero
    by blast
  show ?thesis
    using guard residual_zero
    by blast
qed

theorem phase5_5_helicity_mhd_lift_locked:
  assumes "partial_x_grad_y = partial_y_grad_x"
    and "gm_phase_vector_active gx gy"
    and "coupling \<noteq> 0"
    and "source_offset \<noteq> 0"
    and "phase_gradient = sqrt (gm_grad_mag_sq gx gy)"
    and "phase_gradient \<noteq> 0"
    and "gm_ideal_mhd eta"
    and "gm_mhd_elsasser_balance magnetic_force coriolis_force"
    and "energy = multiplier * abs helicity"
  shows "gm_curl_z partial_x_grad_y partial_y_grad_x = 0
    \<and> gm_Lz_witness phase_gradient source_offset coupling \<noteq> 0
    \<and> gm_resistive_helicity_dissipation eta current_norm_sq = 0
    \<and> elsasser_number magnetic_force coriolis_force = 1
    \<and> gm_woltjer_energy_guard energy multiplier helicity
    \<and> woltjer_helicity_residual energy helicity multiplier = 0
    \<and> phase5_curl_max_abs < 0.000000001
    \<and> phase5_psi_unit_norm_max_error < 0.000000001"
proof -
  have phase5_lock:
    "gm_curl_z partial_x_grad_y partial_y_grad_x = 0
     \<and> (gx \<noteq> 0 \<or> gy \<noteq> 0)
     \<and> gm_Lz_witness phase_gradient source_offset coupling \<noteq> 0
     \<and> 0.18 < phase5_delta
     \<and> phase5_delta < 0.19
     \<and> phase5_curl_max_abs < 0.000000001
     \<and> phase5_psi_unit_norm_max_error < 0.000000001
     \<and> phase5_lz_std < 0.000000001"
    using assms(1-6) phase5_vector_calculus_bridge_locked
    by blast
  have dissipation_zero:
    "gm_resistive_helicity_dissipation eta current_norm_sq = 0"
    using assms(7) gm_ideal_mhd_zero_resistive_helicity_dissipation
    by blast
  have unit_elsasser: "elsasser_number magnetic_force coriolis_force = 1"
    using assms(8) gm_mhd_elsasser_balance_gives_unit_elsasser
    by blast
  have woltjer:
    "gm_woltjer_energy_guard energy multiplier helicity
     \<and> woltjer_helicity_residual energy helicity multiplier = 0"
    using assms(9) gm_woltjer_guard_balanced_residual_zero
    by blast
  show ?thesis
    using phase5_lock dissipation_zero unit_elsasser woltjer
    by blast
qed

end
