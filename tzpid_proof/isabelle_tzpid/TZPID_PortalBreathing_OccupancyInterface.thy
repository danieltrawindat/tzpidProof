theory TZPID_PortalBreathing_OccupancyInterface
  imports
    TZPID_HubbleBreathing_Enclosure
    TZPID_MatterCreation_PressureEoS
begin

text \<open>
  Project: TZPID Proof Pipeline
  Creator: Daniel Alexander Trawin
  ORCID: https://orcid.org/0009-0001-4630-3715

  Source lane: portal-breathing intake from the_portal_equation.txt and
  hypersphere_idea.txt.

  This file keeps the claims conservative: it formalizes algebraic carriers,
  normalized occupancy, nested inverse-radius scaling, interface pressure, and
  portal force balance. It does not assert empirical truth of the physical
  interpretation.
\<close>

definition pb_redshift_wavelength :: "real \<Rightarrow> real \<Rightarrow> real" where
  "pb_redshift_wavelength z lambda_emit = (1 + z) * lambda_emit"

definition pb_redshift_frequency :: "real \<Rightarrow> real \<Rightarrow> real" where
  "pb_redshift_frequency z freq_emit = freq_emit / (1 + z)"

definition pb_three_phase_closed :: "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> bool" where
  "pb_three_phase_closed phi_b phi_T phi_E \<longleftrightarrow> phi_b + phi_T + phi_E = 1"

definition pb_interface_phi_E :: "real \<Rightarrow> real \<Rightarrow> real" where
  "pb_interface_phi_E s ell = (1 + tanh (s / ell)) / 2"

definition pb_interface_phi_T :: "real \<Rightarrow> real \<Rightarrow> real" where
  "pb_interface_phi_T s ell = (1 - tanh (s / ell)) / 2"

definition pb_nested_radius :: "real \<Rightarrow> real \<Rightarrow> real" where
  "pb_nested_radius lambda R = lambda * R"

definition pb_mode_frequency :: "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real" where
  "pb_mode_frequency c j R = c * j / R"

definition pb_mode_energy_density :: "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real" where
  "pb_mode_energy_density hbar c R = hbar * c / R\<^sup>4"

definition pb_interface_pressure :: "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real" where
  "pb_interface_pressure sigma R_T R_E = sigma * (1 / R_T + 1 / R_E)"

definition pb_total_stress_energy :: "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real" where
  "pb_total_stress_energy T_b T_T T_E T_I = T_b + T_T + T_E + T_I"

definition pb_portal_force_balance :: "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> bool" where
  "pb_portal_force_balance F_g F_i F_sigma F_EM F_ZPF \<longleftrightarrow>
    F_g + F_i + F_sigma + F_EM + F_ZPF = 0"

lemma pb_redshift_color_not_speed_carrier:
  assumes "z \<noteq> -1"
  shows "pb_redshift_wavelength z lambda_emit *
      pb_redshift_frequency z freq_emit =
    lambda_emit * freq_emit"
proof -
  show ?thesis
    unfolding pb_redshift_wavelength_def pb_redshift_frequency_def
    using assms
    by field
qed

lemma pb_interface_profiles_partition:
  shows "pb_interface_phi_E s ell + pb_interface_phi_T s ell = 1"
proof -
  show ?thesis
    unfolding pb_interface_phi_E_def pb_interface_phi_T_def
    by algebra
qed

lemma pb_interface_profiles_close_three_phase_without_matter:
  shows "pb_three_phase_closed 0 (pb_interface_phi_T s ell) (pb_interface_phi_E s ell)"
proof -
  have "0 + pb_interface_phi_T s ell + pb_interface_phi_E s ell = 1"
    using pb_interface_profiles_partition[of s ell]
    by linarith
  then show ?thesis
    unfolding pb_three_phase_closed_def .
qed

lemma pb_nested_frequency_ratio:
  assumes "lambda \<noteq> 0"
    and "R \<noteq> 0"
    and "c \<noteq> 0"
    and "j \<noteq> 0"
  shows "pb_mode_frequency c j (pb_nested_radius lambda R) /
      pb_mode_frequency c j R = 1 / lambda"
proof -
  show ?thesis
    unfolding pb_mode_frequency_def pb_nested_radius_def
    using assms
    by field
qed

lemma pb_nested_density_ratio:
  assumes "lambda \<noteq> 0"
    and "R \<noteq> 0"
    and "hbar \<noteq> 0"
    and "c \<noteq> 0"
  shows "pb_mode_energy_density hbar c (pb_nested_radius lambda R) /
      pb_mode_energy_density hbar c R = 1 / lambda\<^sup>4"
proof -
  have lambda4_nonzero: "lambda\<^sup>4 \<noteq> 0"
    using assms(1)
    by positivity
  show ?thesis
    unfolding pb_mode_energy_density_def pb_nested_radius_def
    using assms lambda4_nonzero
    by field
qed

lemma pb_interface_pressure_positive:
  assumes "0 < sigma"
    and "0 < R_T"
    and "0 < R_E"
  shows "0 < pb_interface_pressure sigma R_T R_E"
proof -
  have reciprocal_sum_pos: "0 < 1 / R_T + 1 / R_E"
    using assms
    by positivity
  show ?thesis
    unfolding pb_interface_pressure_def
    using assms reciprocal_sum_pos
    by positivity
qed

lemma pb_total_stress_energy_unfolds:
  shows "pb_total_stress_energy T_b T_T T_E T_I =
    T_b + T_T + T_E + T_I"
  unfolding pb_total_stress_energy_def .

lemma pb_portal_balance_by_counterterm:
  shows "pb_portal_force_balance
    F_g F_i F_sigma F_EM (-(F_g + F_i + F_sigma + F_EM))"
proof -
  show ?thesis
    unfolding pb_portal_force_balance_def
    by algebra
qed

theorem pb_portal_breathing_interface_contract:
  assumes "lambda \<noteq> 0"
    and "R \<noteq> 0"
    and "c \<noteq> 0"
    and "j \<noteq> 0"
    and "hbar \<noteq> 0"
  shows "pb_interface_phi_E s ell + pb_interface_phi_T s ell = 1
    \<and> pb_mode_frequency c j (pb_nested_radius lambda R) /
        pb_mode_frequency c j R = 1 / lambda
    \<and> pb_mode_energy_density hbar c (pb_nested_radius lambda R) /
        pb_mode_energy_density hbar c R = 1 / lambda\<^sup>4
    \<and> pb_portal_force_balance
        F_g F_i F_sigma F_EM (-(F_g + F_i + F_sigma + F_EM))"
proof (intro conjI)
  show "pb_interface_phi_E s ell + pb_interface_phi_T s ell = 1"
    by (rule pb_interface_profiles_partition)
  show "pb_mode_frequency c j (pb_nested_radius lambda R) /
        pb_mode_frequency c j R = 1 / lambda"
    using assms(1,2,3,4)
    by (rule pb_nested_frequency_ratio)
  show "pb_mode_energy_density hbar c (pb_nested_radius lambda R) /
        pb_mode_energy_density hbar c R = 1 / lambda\<^sup>4"
    using assms(1,2,5,3)
    by (rule pb_nested_density_ratio)
  show "pb_portal_force_balance
        F_g F_i F_sigma F_EM (-(F_g + F_i + F_sigma + F_EM))"
    by (rule pb_portal_balance_by_counterterm)
qed

end
