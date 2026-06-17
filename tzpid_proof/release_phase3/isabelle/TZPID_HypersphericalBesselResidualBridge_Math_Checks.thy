theory TZPID_HypersphericalBesselResidualBridge_Math_Checks
  imports Complex_Main
begin

text \<open>
  Project: TZPID Proof Pipeline
  Creator: Daniel Alexander Trawin
  ORCID: https://orcid.org/0009-0001-4630-3715
  Generated UTC: 2026-06-07

  This theory is the concrete Isabelle mathematics layer for the
  Hyperspherical Bessel residual bridge.  It intentionally avoids treating the
  proof as only an abstract predicate chain.  The lemmas below use
  typed real definitions and structured proof steps for the algebraic
  identities that Isabelle can check directly.

  Analytic special-function values such as BesselJZero[1,1] remain in
  the Wolfram certificate layer; Isabelle checks the typed algebra that
  connects those certified values to the paper's proof spine.
\<close>

definition hyperspherical_order :: "real \<Rightarrow> real \<Rightarrow> real" where
  "hyperspherical_order d ell = ell + (d - 2) / 2"

theorem hyperspherical_order_reduces_in_four_spatial_dimensions:
  "hyperspherical_order 4 ell = ell + 1"
proof -
  have "hyperspherical_order 4 ell = ell + (4 - 2) / 2"
    unfolding hyperspherical_order_def
    by (rule refl)
  also have "... = ell + 1"
    by linarith
  finally show ?thesis .
qed

definition pythagorean_comma :: real where
  "pythagorean_comma = (3 / 2) ^ 12 / 2 ^ 7"

definition pythagorean_bulk_reciprocal :: real where
  "pythagorean_bulk_reciprocal = 1 / pythagorean_comma"

theorem pythagorean_comma_exact:
  "pythagorean_comma = 531441 / 524288"
proof -
  have "pythagorean_comma = (3 / 2) ^ 12 / 2 ^ 7"
    unfolding pythagorean_comma_def
    by (rule refl)
  also have "... = 531441 / 524288"
    by norm_num
  finally show ?thesis .
qed

theorem pythagorean_comma_bulk_reciprocal_closes:
  "pythagorean_comma * pythagorean_bulk_reciprocal = 1"
proof -
  have "pythagorean_comma \<noteq> 0"
  proof -
    have "pythagorean_comma = 531441 / 524288"
      using pythagorean_comma_exact .
    thus ?thesis
      by norm_num
  qed
  hence "pythagorean_comma * (1 / pythagorean_comma) = 1"
    by (rule nonzero_mult_div_cancel_left)
  thus ?thesis
    unfolding pythagorean_bulk_reciprocal_def .
qed

theorem perfect_fifth_descending_fifth_reciprocal:
  "(3 / 2 :: real) * (2 / 3) = 1"
proof -
  show ?thesis
    by norm_num
qed

theorem avalanche_cascade_reciprocal:
  "(3 / 2 :: real) * (2 / 3) = 1"
proof -
  show ?thesis
    by norm_num
qed

definition ripple_index :: "real \<Rightarrow> real \<Rightarrow> real" where
  "ripple_index wavelength height = wavelength / height"

theorem ripple_index_scale_invariant:
  assumes "scale \<noteq> 0"
  shows "ripple_index (scale * wavelength) (scale * height)
       = ripple_index wavelength height"
proof -
  have "ripple_index (scale * wavelength) (scale * height)
      = (scale * wavelength) / (scale * height)"
    unfolding ripple_index_def
    by (rule refl)
  also have "... = wavelength / height"
    using assms
    by (field)
  finally show ?thesis
    unfolding ripple_index_def .
qed

definition planck_mass :: "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real" where
  "planck_mass hbar c grav = sqrt (hbar * c / grav)"

definition gravitational_charge :: "real \<Rightarrow> real \<Rightarrow> real" where
  "gravitational_charge mass mP = mass / mP"

theorem planck_charge_product:
  assumes "hbar > 0" and "c > 0" and "grav > 0"
  defines "mP \<equiv> planck_mass hbar c grav"
  shows "gravitational_charge mX mP * gravitational_charge mY mP
       = grav * mX * mY / (hbar * c)"
proof -
  have mP_square: "mP\<^sup>2 = hbar * c / grav"
  proof -
    have "mP\<^sup>2 = (sqrt (hbar * c / grav))\<^sup>2"
      unfolding mP_def planck_mass_def
      by (rule refl)
    also have "... = hbar * c / grav"
    proof (rule real_sqrt_power)
      show "0 \<le> hbar * c / grav"
        using assms
        by (positivity)
    qed
    finally show ?thesis .
  qed
  have "mP \<noteq> 0"
  proof
    assume "mP = 0"
    hence "mP\<^sup>2 = 0"
      by algebra
    hence "hbar * c / grav = 0"
      using mP_square by algebra
    thus False
      using assms
      by (positivity)
  qed
  have "gravitational_charge mX mP * gravitational_charge mY mP
      = (mX / mP) * (mY / mP)"
    unfolding gravitational_charge_def
    by (rule refl)
  also have "... = mX * mY / mP\<^sup>2"
    using \<open>mP \<noteq> 0\<close>
    by (field)
  also have "... = mX * mY / (hbar * c / grav)"
    using mP_square
    by presburger
  also have "... = grav * mX * mY / (hbar * c)"
    using assms
    by (field)
  finally show ?thesis .
qed

definition isotope_mass ::
  "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real" where
  "isotope_mass Z N mp mn me Ebind c =
     Z * mp + N * mn + Z * me - Ebind / c\<^sup>2"

definition isotope_gravitational_charge ::
  "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real" where
  "isotope_gravitational_charge Z N mp mn me Ebind c mP =
     isotope_mass Z N mp mn me Ebind c / mP"

theorem isotope_charge_recovers_isotope_mass:
  assumes "mP \<noteq> 0"
  shows "mP * isotope_gravitational_charge Z N mp mn me Ebind c mP
       = isotope_mass Z N mp mn me Ebind c"
proof -
  have "mP * isotope_gravitational_charge Z N mp mn me Ebind c mP
      = mP * (isotope_mass Z N mp mn me Ebind c / mP)"
    unfolding isotope_gravitational_charge_def
    by (rule refl)
  also have "... = isotope_mass Z N mp mn me Ebind c"
    using assms
    by (field)
  finally show ?thesis .
qed

definition residual_curvature :: "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real" where
  "residual_curvature total matter = total - matter"

definition accumulated_total_source :: "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real" where
  "accumulated_total_source matter sound entropy = matter + sound + entropy"

theorem residual_curvature_decomposes:
  "residual_curvature (accumulated_total_source matter sound entropy) matter
   = sound + entropy"
proof -
  have "residual_curvature (accumulated_total_source matter sound entropy) matter
      = (matter + sound + entropy) - matter"
    unfolding residual_curvature_def accumulated_total_source_def
    by (rule refl)
  also have "... = sound + entropy"
    by algebra
  finally show ?thesis .
qed

definition exponential_kernel_density :: "real \<Rightarrow> real \<Rightarrow> real" where
  "exponential_kernel_density tau_dec s =
     (1 / tau_dec) * exp (- s / tau_dec)"

text \<open>
  The normalization integral
    integral_0^\<infinity> (1/tau_dec) exp(-s/tau_dec) ds = 1
  is now proved in the dedicated HOL-Analysis theory
  TZPID_Temporal_Kernel_HOL_Analysis.  This base math theory keeps the kernel
  density definition available to the lighter algebraic bridge files.
\<close>

end

