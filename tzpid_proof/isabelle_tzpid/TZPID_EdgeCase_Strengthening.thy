theory TZPID_EdgeCase_Strengthening
  imports TZPID_GeometryCurvature_Carriers
begin

text \<open>
  Project: TZPID Proof Pipeline
  Creator: Daniel Alexander Trawin
  ORCID: https://orcid.org/0009-0001-4630-3715
  Generated UTC: 2026-06-11

  Curated edge-case strengthening carriers. These contracts deliberately
  quarantine shell/code artifacts and formalize only compact mathematical
  rescue equations. They are proof-package stress tests, not new physical
  axioms.
\<close>

section \<open>Scalar Boundary and Density Contracts\<close>

definition cosmological_density_contract ::
  "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> bool" where
  "cosmological_density_contract hbar c R phi0 phitotal rho =
     (R \<noteq> 0 \<and> phitotal \<noteq> 0 \<and> rho = (hbar * c / R\<^sup>4) * (phi0 / phitotal))"

theorem cosmological_density_contract_recovers_formula:
  assumes "cosmological_density_contract hbar c R phi0 phitotal rho"
  shows "rho = (hbar * c / R\<^sup>4) * (phi0 / phitotal)"
  using assms unfolding cosmological_density_contract_def by blast

definition vacuum_cutoff_admissible :: "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> bool" where
  "vacuum_cutoff_admissible uT omega_cut eta_bound =
     (uT > 0 \<and> omega_cut > 0 \<and> eta_bound \<ge> 0)"

theorem vacuum_cutoff_has_positive_scale:
  assumes "vacuum_cutoff_admissible uT omega_cut eta_bound"
  shows "uT\<^sup>4 > 0 \<and> omega_cut > 0"
  using assms unfolding vacuum_cutoff_admissible_def by simp

definition finite_cutoff_guard :: "real \<Rightarrow> bool" where
  "finite_cutoff_guard omega_cut = (omega_cut > 0)"

theorem finite_cutoff_guard_positive:
  assumes "finite_cutoff_guard omega_cut"
  shows "omega_cut > 0"
  using assms unfolding finite_cutoff_guard_def .

section \<open>Spectral and Closure Residuals\<close>

definition alfven_speed :: "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real" where
  "alfven_speed B mu0 rho = B / sqrt (mu0 * rho)"

definition alfven_mode_contract :: "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> nat \<Rightarrow> bool" where
  "alfven_mode_contract B mu0 rho R n =
     (mu0 * rho > 0 \<and> R \<noteq> 0 \<and> alfven_speed B mu0 rho = B / sqrt (mu0 * rho))"

theorem alfven_mode_contract_recovers_speed:
  assumes "alfven_mode_contract B mu0 rho R n"
  shows "alfven_speed B mu0 rho = B / sqrt (mu0 * rho)"
  using assms unfolding alfven_mode_contract_def by blast

definition poisson_residual :: "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real" where
  "poisson_residual lap_phi G_eff rho = lap_phi - 4 * pi * G_eff * rho"

theorem poisson_residual_zero:
  assumes "lap_phi = 4 * pi * G_eff * rho"
  shows "poisson_residual lap_phi G_eff rho = 0"
proof -
  have "poisson_residual lap_phi G_eff rho = lap_phi - 4 * pi * G_eff * rho"
    unfolding poisson_residual_def by (rule refl)
  also have "... = 0"
    using assms by algebra
  finally show ?thesis .
qed

definition helmholtz_residual :: "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real" where
  "helmholtz_residual lap_p k p = lap_p + k\<^sup>2 * p"

theorem helmholtz_residual_zero:
  assumes "lap_p = - k\<^sup>2 * p"
  shows "helmholtz_residual lap_p k p = 0"
  using assms unfolding helmholtz_residual_def by algebra

definition kk_massive_residual :: "real \<Rightarrow> int \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real" where
  "kk_massive_residual box4 n R phi = box4 + ((of_int n)\<^sup>2 / R\<^sup>2) * phi"

theorem kk_massive_residual_zero:
  assumes "box4 = - (((of_int n)\<^sup>2 / R\<^sup>2) * phi)"
  shows "kk_massive_residual box4 n R phi = 0"
  using assms unfolding kk_massive_residual_def by algebra

definition density_poisson_contract :: "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> bool" where
  "density_poisson_contract m0 n lap_phi G_eff rho =
     (rho = m0 * n \<and> lap_phi = 4 * pi * G_eff * rho)"

theorem density_poisson_contract_closes:
  assumes "density_poisson_contract m0 n lap_phi G_eff rho"
  shows "poisson_residual lap_phi G_eff rho = 0"
  using assms unfolding density_poisson_contract_def
  by (intro poisson_residual_zero) blast

section \<open>Topology, Ratios, and Locking\<close>

definition half_integer_winding_contract :: "real \<Rightarrow> bool" where
  "half_integer_winding_contract w = (\<exists>k::int. w = of_int k / 2)"

theorem integer_winding_is_half_integer:
  "half_integer_winding_contract (of_int k)"
proof -
  have "of_int k = of_int (2 * k) / 2"
    by simp
  thus ?thesis
    unfolding half_integer_winding_contract_def by blast
qed

definition ratio_gate_contract :: "real \<Rightarrow> real \<Rightarrow> bool" where
  "ratio_gate_contract numerator denominator =
     (denominator > 0 \<and> numerator / denominator > 1)"

theorem ten_ninths_ratio_gate:
  "ratio_gate_contract 10 9"
  unfolding ratio_gate_contract_def by norm_num

definition kuramoto_threshold_contract :: "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> bool" where
  "kuramoto_threshold_contract K omega1 omega2 = (K \<ge> abs (omega1 - omega2))"

theorem kuramoto_threshold_exact:
  "kuramoto_threshold_contract (abs (omega1 - omega2)) omega1 omega2"
  unfolding kuramoto_threshold_contract_def by simp

definition elsasser_contract :: "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real" where
  "elsasser_contract B rho mu Omega = B\<^sup>2 / (rho * mu * Omega\<^sup>2)"

theorem elsasser_unit_sample:
  "elsasser_contract 1 1 1 1 = 1"
  unfolding elsasser_contract_def by norm_num

definition pressure_threshold_contract :: "real \<Rightarrow> real \<Rightarrow> bool" where
  "pressure_threshold_contract P_vac P_crit = (P_vac \<ge> P_crit)"

theorem pressure_threshold_reflexive:
  "pressure_threshold_contract P P"
  unfolding pressure_threshold_contract_def by simp

section \<open>Gyromagnetic and Conservation Carriers\<close>

definition bessel_gyro_product_contract :: "real \<Rightarrow> real \<Rightarrow> real" where
  "bessel_gyro_product_contract bessel_part gyro_part = bessel_part * gyro_part"

theorem bessel_gyro_product_zero_left:
  "bessel_gyro_product_contract 0 gyro_part = 0"
  unfolding bessel_gyro_product_contract_def by simp

definition helicity_integral_contract :: "real \<Rightarrow> real \<Rightarrow> real" where
  "helicity_integral_contract A_dot_B volume = A_dot_B * volume"

theorem helicity_integral_zero_when_orthogonal:
  "helicity_integral_contract 0 volume = 0"
  unfolding helicity_integral_contract_def by simp

definition helicity_sum_conservation_contract :: "real \<Rightarrow> real \<Rightarrow> real" where
  "helicity_sum_conservation_contract dH_field_dt dH_mech_dt =
     dH_field_dt + dH_mech_dt"

theorem helicity_sum_conservation_zero:
  assumes "dH_mech_dt = - dH_field_dt"
  shows "helicity_sum_conservation_contract dH_field_dt dH_mech_dt = 0"
  using assms unfolding helicity_sum_conservation_contract_def by algebra

definition einstein_recovery_residual :: "real \<Rightarrow> real" where
  "einstein_recovery_residual phi_TZP = phi_TZP"

theorem einstein_recovery_residual_zero:
  assumes "phi_TZP = 0"
  shows "einstein_recovery_residual phi_TZP = 0"
  using assms unfolding einstein_recovery_residual_def by simp

definition friedmann_component_contract ::
  "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> bool" where
  "friedmann_component_contract a H0 Om Or Ok Ol =
     (a > 0 \<and> H0 \<ge> 0 \<and> Om \<ge> 0 \<and> Or \<ge> 0 \<and> Ol \<ge> 0)"

theorem friedmann_component_contract_has_positive_scale:
  assumes "friedmann_component_contract a H0 Om Or Ok Ol"
  shows "a > 0"
  using assms unfolding friedmann_component_contract_def by blast

definition spherical_mode_factor_contract :: "real \<Rightarrow> real \<Rightarrow> real" where
  "spherical_mode_factor_contract normalization angular_factor = normalization * angular_factor"

theorem spherical_mode_factor_zero:
  "spherical_mode_factor_contract 0 angular_factor = 0"
  unfolding spherical_mode_factor_contract_def by simp

definition finite_mode_sum_contract :: "nat \<Rightarrow> bool" where
  "finite_mode_sum_contract n = True"

theorem finite_mode_sum_contract_total:
  "finite_mode_sum_contract n"
  unfolding finite_mode_sum_contract_def by simp

end
