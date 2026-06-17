theory TZPID_S4S5_Hypersphere_Mix_Laws
  imports TZPID_PortalEquilibrium_Laws
begin

text \<open>
  S4/S5 hypersphere-breathing extension and folded source-mix carriers.
  These are algebraic carriers extracted from the saved "restart from the
  original hypersphere" note.
\<close>

definition s45_volume_power :: "real \<Rightarrow> nat \<Rightarrow> real" where
  "s45_volume_power R n = R ^ n"

definition s45_fractional_rate :: "real \<Rightarrow> real \<Rightarrow> nat \<Rightarrow> real" where
  "s45_fractional_rate R Rdot n = real n * Rdot / R"

definition s45_redshift_ratio :: "real \<Rightarrow> real" where
  "s45_redshift_ratio z = 1 + z"

definition s45_present_emission_volume_ratio :: "real \<Rightarrow> nat \<Rightarrow> real" where
  "s45_present_emission_volume_ratio z n = (1 + z) ^ n"

definition s45_density_scaling :: "real \<Rightarrow> nat \<Rightarrow> real" where
  "s45_density_scaling R n = R powr (-(real n))"

definition s45_radiation_density_scaling :: "real \<Rightarrow> nat \<Rightarrow> real" where
  "s45_radiation_density_scaling R n = R powr (-(real n + 1))"

definition s45_occupancy_radius_ratio :: "real \<Rightarrow> nat \<Rightarrow> real" where
  "s45_occupancy_radius_ratio phi n = phi powr (1 / real n)"

definition s45_folded_source ::
  "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real" where
  "s45_folded_source eta_b phi_T phi_E K_TE G_res D_DAT A_B C_cap R_mode R_FFT I_E Gamma_b phi_b =
    eta_b * phi_T * phi_E * K_TE * G_res * D_DAT * A_B * C_cap * R_mode * R_FFT * I_E -
    Gamma_b * phi_b"

definition s45_gaussian_gate :: "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real" where
  "s45_gaussian_gate r center sigma = exp (- ((r - center)\<^sup>2) / (2 * sigma\<^sup>2))"

definition s45_energy_inversion_sign :: "real \<Rightarrow> real \<Rightarrow> real" where
  "s45_energy_inversion_sign E_TZP E = sgn (E_TZP / E)"

definition s45_bessel_z :: "real \<Rightarrow> real" where
  "s45_bessel_z s = (s - 2.5055) / 0.2167"

lemma s45_s3_fractional_rate:
  assumes "R \<noteq> 0"
  shows "s45_fractional_rate R Rdot 3 = 3 * Rdot / R"
  unfolding s45_fractional_rate_def
  by simp

lemma s45_s4_fractional_rate:
  assumes "R \<noteq> 0"
  shows "s45_fractional_rate R Rdot 4 = 4 * Rdot / R"
  unfolding s45_fractional_rate_def
  by simp

lemma s45_s5_fractional_rate:
  assumes "R \<noteq> 0"
  shows "s45_fractional_rate R Rdot 5 = 5 * Rdot / R"
  unfolding s45_fractional_rate_def
  by simp

lemma s45_redshift_volume_examples:
  shows "s45_present_emission_volume_ratio 1 3 = 8
    \<and> s45_present_emission_volume_ratio 1 4 = 16
    \<and> s45_present_emission_volume_ratio 1 5 = 32"
  unfolding s45_present_emission_volume_ratio_def
  by simp

lemma s45_gaussian_gate_at_center:
  assumes "sigma \<noteq> 0"
  shows "s45_gaussian_gate center center sigma = 1"
  unfolding s45_gaussian_gate_def
  using assms
  by simp

lemma s45_energy_inversion_sign_negative:
  assumes "0 < E"
  shows "s45_energy_inversion_sign (-E) E = -1"
  unfolding s45_energy_inversion_sign_def
  using assms
  by simp

lemma s45_bessel_z_center:
  shows "s45_bessel_z 2.5055 = 0"
  unfolding s45_bessel_z_def
  by simp

theorem s45_mix_contract:
  assumes "sigma_r \<noteq> 0"
    and "sigma_f \<noteq> 0"
    and "0 < E"
  shows "s45_fractional_rate R Rdot 4 = 4 * Rdot / R
    \<and> s45_fractional_rate R Rdot 5 = 5 * Rdot / R
    \<and> s45_present_emission_volume_ratio 1 5 = 32
    \<and> s45_gaussian_gate phi phi sigma_r = 1
    \<and> s45_gaussian_gate phi phi sigma_f = 1
    \<and> s45_energy_inversion_sign (-E) E = -1"
proof (intro conjI)
  show "s45_fractional_rate R Rdot 4 = 4 * Rdot / R"
    by (rule s45_s4_fractional_rate)
  show "s45_fractional_rate R Rdot 5 = 5 * Rdot / R"
    by (rule s45_s5_fractional_rate)
  show "s45_present_emission_volume_ratio 1 5 = 32"
    unfolding s45_present_emission_volume_ratio_def
    by simp
  show "s45_gaussian_gate phi phi sigma_r = 1"
    using assms(1)
    by (rule s45_gaussian_gate_at_center)
  show "s45_gaussian_gate phi phi sigma_f = 1"
    using assms(2)
    by (rule s45_gaussian_gate_at_center)
  show "s45_energy_inversion_sign (-E) E = -1"
    using assms(3)
    by (rule s45_energy_inversion_sign_negative)
qed

end
