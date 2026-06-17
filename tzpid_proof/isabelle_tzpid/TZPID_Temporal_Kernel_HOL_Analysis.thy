theory TZPID_Temporal_Kernel_HOL_Analysis
  imports
    TZPID_HypersphericalBesselResidualBridge_Phase2_Model
    "HOL-Analysis.Henstock_Kurzweil_Integration"
begin

text \<open>
  Project: TZPID Proof Pipeline
  Creator: Daniel Alexander Trawin
  ORCID: https://orcid.org/0009-0001-4630-3715
  Generated UTC: 2026-06-08T01:59:19Z

  HOL-Analysis upgrade for the causal temporal accumulation kernel.  The
  preceding Phase 2.5 model proved the finite-window/tail normalization
  algebraically.  This theory proves the improper Henstock--Kurzweil integral
  of the same exponential kernel over the past elapsed-time ray.
\<close>

theorem exponential_decay_integral_to_infinity:
  assumes tau_pos: "tau_decay > 0"
  shows "((\<lambda>s::real. exp (-(1 / tau_decay) * s))
          has_integral tau_decay) {0..}"
proof -
  have inv_pos: "1 / tau_decay > 0"
  proof -
    have "0 < (1::real)"
      by (rule zero_less_one)
    thus ?thesis
      using tau_pos
      by (rule divide_pos_pos)
  qed
  have base:
    "((\<lambda>s::real. exp (-(1 / tau_decay) * s))
      has_integral exp (-(1 / tau_decay) * 0) / (1 / tau_decay)) {0..}"
    using has_integral_exp_minus_to_infinity[OF inv_pos, of 0] .
  have value: "exp (-(1 / tau_decay) * 0) / (1 / tau_decay) = tau_decay"
  proof -
    have exp_zero_term: "exp (-(1 / tau_decay) * 0) = 1"
    proof -
      have "-(1 / tau_decay) * 0 = (0::real)"
        by algebra
      hence "exp (-(1 / tau_decay) * 0) = exp 0"
        by presburger
      also have "... = 1"
        by (rule exp_zero)
      finally show ?thesis .
    qed
    have inv_nonzero: "1 / tau_decay \<noteq> 0"
    proof
      assume "1 / tau_decay = (0::real)"
      hence "1 = 0 * tau_decay"
        using tau_pos
        by (field)
      hence "1 = (0::real)"
        by algebra
      thus False
        by (rule one_neq_zero)
    qed
    have "exp (-(1 / tau_decay) * 0) / (1 / tau_decay)
        = 1 / (1 / tau_decay)"
      using exp_zero_term
      by presburger
    also have "... = tau_decay"
      using tau_pos inv_nonzero
      by (field)
    finally show ?thesis .
  qed
  show ?thesis
    using base value
    by (rule has_integral_eq_rhs)
qed

theorem exponential_kernel_density_has_integral_one:
  assumes tau_pos: "tau_decay > 0"
  shows "((\<lambda>s::real. exponential_kernel_density tau_decay s)
          has_integral 1) {0..}"
proof -
  have base:
    "((\<lambda>s::real. exp (-(1 / tau_decay) * s))
      has_integral tau_decay) {0..}"
    using tau_pos
    by (rule exponential_decay_integral_to_infinity)
  have scaled:
    "((\<lambda>s::real. (1 / tau_decay) * exp (-(1 / tau_decay) * s))
      has_integral (1 / tau_decay) * tau_decay) {0..}"
    using base
    by (rule has_integral_mult_right)
  have integral_value: "(1 / tau_decay) * tau_decay = 1"
    using tau_pos
    by (field)
  have density_eq:
    "\<And>s::real.
      s \<in> {0..} \<Longrightarrow>
      (1 / tau_decay) * exp (-(1 / tau_decay) * s)
      = exponential_kernel_density tau_decay s"
  proof -
    fix s::real
    assume "s \<in> {0..}"
    have "-(1 / tau_decay) * s = - s / tau_decay"
      using tau_pos
      by (field)
    hence "exp (-(1 / tau_decay) * s) = exp (- s / tau_decay)"
      by presburger
    thus "(1 / tau_decay) * exp (-(1 / tau_decay) * s)
        = exponential_kernel_density tau_decay s"
      unfolding exponential_kernel_density_def .
  qed
  have "((\<lambda>s::real. exponential_kernel_density tau_decay s)
        has_integral (1 / tau_decay) * tau_decay) {0..}"
    using density_eq scaled
    by (rule has_integral_eq)
  thus ?thesis
    using integral_value
    by (rule has_integral_eq_rhs)
qed

theorem exponential_kernel_density_integrable_on_past:
  assumes "tau_decay > 0"
  shows "(\<lambda>s::real. exponential_kernel_density tau_decay s)
         integrable_on {0..}"
proof -
  have "((\<lambda>s::real. exponential_kernel_density tau_decay s)
        has_integral 1) {0..}"
    using assms
    by (rule exponential_kernel_density_has_integral_one)
  thus ?thesis
    unfolding integrable_on_def
    by blast
qed

context TZPID_HypersphericalBesselResidualBridge_Focus
begin

theorem temporal_kernel_hol_analysis_certificate_connected:
  assumes "tau_decay > 0"
  shows
    "all_hyperspherical_bessel_residual_bridge_certificates_verified
     \<and> ((\<lambda>s::real. exponential_kernel_density tau_decay s)
          has_integral 1) {0..}"
proof (intro conjI)
  show "all_hyperspherical_bessel_residual_bridge_certificates_verified"
    using all_hyperspherical_bessel_residual_bridge_certificates_passed .
  show "((\<lambda>s::real. exponential_kernel_density tau_decay s)
        has_integral 1) {0..}"
    using assms
    by (rule exponential_kernel_density_has_integral_one)
qed

end

end
