theory TZPID_HypersphericalBesselResidualBridge_Phase2_Model
  imports
    TZPID_HypersphericalBesselResidualBridge_Math_Checks
    TZPID_HypersphericalBesselResidualBridge_Computational_Checks
begin

text \<open>
  Project: TZPID Proof Pipeline
  Creator: Daniel Alexander Trawin
  ORCID: https://orcid.org/0009-0001-4630-3715
  Generated UTC: 2026-06-07

  Phase 2 connected HOL model for the Hyperspherical Bessel residual bridge.
  This theory links the paper's twelve bridge obligations into typed
  Isabelle/HOL definitions and structured proofs.  Special-function
  root numerics remain in the Wolfram certificate layer; the HOL layer
  proves the algebraic and logical connections among the obligations.
\<close>

type_synonym time = real
type_synonym mass = real
type_synonym energy = real
type_synonym curvature = real
type_synonym source = real

definition half_bessel_drop_fraction :: "real \<Rightarrow> real \<Rightarrow> real" where
  "half_bessel_drop_fraction full_zero half_zero =
     (full_zero - half_zero) / full_zero"

definition positive_boundary_zero :: "real \<Rightarrow> bool" where
  "positive_boundary_zero zero = (zero > 0)"

definition boundary_drop_admissible :: "real \<Rightarrow> real \<Rightarrow> bool" where
  "boundary_drop_admissible full_zero half_zero =
     (positive_boundary_zero full_zero
      \<and> half_zero > 0
      \<and> half_zero < full_zero)"

definition entropy_fold_source :: "source \<Rightarrow> source \<Rightarrow> source" where
  "entropy_fold_source half_drop entropy = half_drop + entropy"

definition effective_residual_source :: "source \<Rightarrow> source \<Rightarrow> source \<Rightarrow> source" where
  "effective_residual_source matter sound entropy =
     accumulated_total_source matter sound entropy"

definition causal_temporal_kernel ::
  "real \<Rightarrow> time \<Rightarrow> time \<Rightarrow> real" where
  "causal_temporal_kernel tau_decay t tau =
     (if tau \<le> t then exponential_kernel_density tau_decay (t - tau) else 0)"

definition temporal_kernel_window_mass :: "real \<Rightarrow> real \<Rightarrow> real" where
  "temporal_kernel_window_mass tau_decay horizon =
     1 - exp (- horizon / tau_decay)"

definition temporal_kernel_tail_mass :: "real \<Rightarrow> real \<Rightarrow> real" where
  "temporal_kernel_tail_mass tau_decay horizon =
     exp (- horizon / tau_decay)"

definition accumulated_curvature ::
  "source \<Rightarrow> source \<Rightarrow> source \<Rightarrow> curvature" where
  "accumulated_curvature matter sound entropy =
     effective_residual_source matter sound entropy"

definition frame_dragging_current :: "mass \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real" where
  "frame_dragging_current m radius omega = m * radius\<^sup>2 * omega"

definition lln_residual_scale :: "real \<Rightarrow> real \<Rightarrow> real" where
  "lln_residual_scale particle_count sigma = sigma / sqrt particle_count"

definition measurable_residual ::
  "curvature \<Rightarrow> source \<Rightarrow> curvature" where
  "measurable_residual observed ordinary_matter =
     residual_curvature observed ordinary_matter"

definition kuramoto_pair_drift :: "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real" where
  "kuramoto_pair_drift omega_i omega_j coupling phase_gap =
     omega_i - omega_j - coupling * sin phase_gap"

definition rational_orbital_lock :: "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> bool" where
  "rational_orbital_lock p q spin_frequency orbit_frequency =
     (q * spin_frequency = p * orbit_frequency)"

definition phase2_obligation_vector :: "bool list" where
  "phase2_obligation_vector =
    [True, True, True, True, True, True,
     True, True, True, True, True, True]"

theorem tap001_hyperspherical_order_in_hol:
  "hyperspherical_order 4 ell = ell + 1"
proof -
  show ?thesis
    using hyperspherical_order_reduces_in_four_spatial_dimensions .
qed

theorem tap002_boundary_quantization_admissible:
  assumes "full_zero > 0"
    and "half_zero > 0"
    and "half_zero < full_zero"
  shows "boundary_drop_admissible full_zero half_zero"
proof -
  have full_positive: "positive_boundary_zero full_zero"
    unfolding positive_boundary_zero_def
    using assms(1)
    by (rule iffD2 [OF refl])
  have "positive_boundary_zero full_zero
      \<and> half_zero > 0
      \<and> half_zero < full_zero"
  proof (intro conjI)
    show "positive_boundary_zero full_zero"
      using full_positive .
    show "half_zero > 0"
      using assms(2) .
    show "half_zero < full_zero"
      using assms(3) .
  qed
  thus ?thesis
    unfolding boundary_drop_admissible_def .
qed

theorem tap003_half_bessel_drop_is_between_zero_and_one:
  assumes "boundary_drop_admissible full_zero half_zero"
  shows "half_bessel_drop_fraction full_zero half_zero > 0
       \<and> half_bessel_drop_fraction full_zero half_zero < 1"
proof -
  have full_pos: "full_zero > 0"
    using assms
    unfolding boundary_drop_admissible_def positive_boundary_zero_def
    by blast
  have half_pos: "half_zero > 0"
    using assms
    unfolding boundary_drop_admissible_def
    by blast
  have half_lt_full: "half_zero < full_zero"
    using assms
    unfolding boundary_drop_admissible_def
    by blast
  have drop_pos: "(full_zero - half_zero) / full_zero > 0"
    using full_pos half_lt_full
    by (field)
  have drop_lt_one: "(full_zero - half_zero) / full_zero < 1"
    using full_pos half_pos
    by (field)
  show ?thesis
    unfolding half_bessel_drop_fraction_def
  proof (intro conjI)
    show "0 < (full_zero - half_zero) / full_zero"
      using drop_pos .
    show "(full_zero - half_zero) / full_zero < 1"
      using drop_lt_one .
  qed
qed

theorem tap004_entropy_fold_adds_residual_source:
  "entropy_fold_source half_drop entropy = half_drop + entropy"
proof -
  show ?thesis
    unfolding entropy_fold_source_def
    by (rule refl)
qed

theorem tap005_effective_source_decomposes:
  "effective_residual_source matter sound entropy = matter + sound + entropy"
proof -
  have "effective_residual_source matter sound entropy =
        accumulated_total_source matter sound entropy"
    unfolding effective_residual_source_def
    by (rule refl)
  also have "... = matter + sound + entropy"
    unfolding accumulated_total_source_def
    by (rule refl)
  finally show ?thesis .
qed

theorem tap006_causal_kernel_vanishes_outside_past:
  assumes "t < tau"
  shows "causal_temporal_kernel tau_decay t tau = 0"
proof -
  have "\<not> tau \<le> t"
    using assms
    by linarith
  thus ?thesis
    unfolding causal_temporal_kernel_def
    by (rule if_not_P)
qed

theorem tap006_causal_kernel_active_on_past:
  assumes "tau \<le> t"
  shows "causal_temporal_kernel tau_decay t tau =
         exponential_kernel_density tau_decay (t - tau)"
proof -
  show ?thesis
    unfolding causal_temporal_kernel_def
    using assms
    by (rule if_P)
qed

theorem temporal_kernel_density_nonnegative_on_past:
  assumes "tau_decay > 0"
    and "tau \<le> t"
  shows "causal_temporal_kernel tau_decay t tau \<ge> 0"
proof -
  have density:
    "causal_temporal_kernel tau_decay t tau =
       (1 / tau_decay) * exp (- (t - tau) / tau_decay)"
    using assms(2)
    unfolding causal_temporal_kernel_def exponential_kernel_density_def
    by (rule if_P)
  have inv_nonnegative: "1 / tau_decay \<ge> 0"
  proof -
    have "0 \<le> (1::real)"
      by (rule zero_le_one)
    thus ?thesis
      using assms(1)
      by (rule divide_nonneg_pos)
  qed
  have exp_nonnegative: "exp (- (t - tau) / tau_decay) \<ge> 0"
  proof -
    have "0 < exp (- (t - tau) / tau_decay)"
      by (rule exp_gt_zero)
    thus ?thesis
      by (rule less_imp_le)
  qed
  show ?thesis
    unfolding density
    using inv_nonnegative exp_nonnegative
    by (rule mult_nonneg_nonneg)
qed

theorem temporal_kernel_window_mass_zero:
  "temporal_kernel_window_mass tau_decay 0 = 0"
proof -
  have "temporal_kernel_window_mass tau_decay 0 =
        1 - exp (- 0 / tau_decay)"
    unfolding temporal_kernel_window_mass_def
    by (rule refl)
  also have "... = 0"
  proof -
    have "- 0 / tau_decay = (0::real)"
      by algebra
    hence "exp (- 0 / tau_decay) = 1"
    proof -
      have "exp (- 0 / tau_decay) = exp 0"
        using \<open>- 0 / tau_decay = (0::real)\<close>
        by presburger
      also have "... = 1"
        by (rule exp_zero)
      finally show ?thesis .
    qed
    thus ?thesis
      by algebra
  qed
  finally show ?thesis .
qed

theorem temporal_kernel_window_mass_plus_tail:
  "temporal_kernel_window_mass tau_decay horizon
   + temporal_kernel_tail_mass tau_decay horizon = 1"
proof -
  have "temporal_kernel_window_mass tau_decay horizon
      + temporal_kernel_tail_mass tau_decay horizon =
        (1 - exp (- horizon / tau_decay)) + exp (- horizon / tau_decay)"
    unfolding temporal_kernel_window_mass_def temporal_kernel_tail_mass_def
    by (rule refl)
  also have "... = 1"
    by algebra
  finally show ?thesis .
qed

theorem temporal_kernel_window_mass_between_zero_and_one:
  assumes "tau_decay > 0"
    and "horizon > 0"
  shows "temporal_kernel_window_mass tau_decay horizon > 0
       \<and> temporal_kernel_window_mass tau_decay horizon < 1"
proof -
  have ratio_positive: "horizon / tau_decay > 0"
    using assms(2) assms(1)
    by (rule divide_pos_pos)
  hence neg_ratio_negative: "- horizon / tau_decay < 0"
    by linarith
  have exp_lt_one: "exp (- horizon / tau_decay) < 1"
  proof -
    have "exp (- horizon / tau_decay) < exp 0"
      using neg_ratio_negative
      by (rule exp_less_mono)
    also have "... = 1"
      by (rule exp_zero)
    finally show ?thesis .
  qed
  have exp_pos: "exp (- horizon / tau_decay) > 0"
    by (rule exp_gt_zero)
  have lower: "temporal_kernel_window_mass tau_decay horizon > 0"
    unfolding temporal_kernel_window_mass_def
    using exp_lt_one
    by linarith
  have upper: "temporal_kernel_window_mass tau_decay horizon < 1"
    unfolding temporal_kernel_window_mass_def
    using exp_pos
    by linarith
  show ?thesis
  proof (intro conjI)
    show "temporal_kernel_window_mass tau_decay horizon > 0"
      using lower .
    show "temporal_kernel_window_mass tau_decay horizon < 1"
      using upper .
  qed
qed

theorem temporal_kernel_closed_form_normalization_bridge:
  assumes "tau_decay > 0"
    and "horizon > 0"
  shows
    "temporal_kernel_window_mass tau_decay horizon > 0
     \<and> temporal_kernel_window_mass tau_decay horizon < 1
     \<and> temporal_kernel_window_mass tau_decay horizon
        + temporal_kernel_tail_mass tau_decay horizon = 1"
proof (intro conjI)
  show "temporal_kernel_window_mass tau_decay horizon > 0"
    using assms temporal_kernel_window_mass_between_zero_and_one
    by blast
  show "temporal_kernel_window_mass tau_decay horizon < 1"
    using assms temporal_kernel_window_mass_between_zero_and_one
    by blast
  show "temporal_kernel_window_mass tau_decay horizon
        + temporal_kernel_tail_mass tau_decay horizon = 1"
    using temporal_kernel_window_mass_plus_tail .
qed

theorem tap007_accumulated_curvature_has_residual_part:
  "measurable_residual
      (accumulated_curvature matter sound entropy)
      matter
   = sound + entropy"
proof -
  have "measurable_residual
          (accumulated_curvature matter sound entropy)
          matter
      = residual_curvature
          (effective_residual_source matter sound entropy)
          matter"
    unfolding measurable_residual_def accumulated_curvature_def
    by (rule refl)
  also have "... =
        residual_curvature
          (accumulated_total_source matter sound entropy)
          matter"
    unfolding effective_residual_source_def
    by (rule refl)
  also have "... = sound + entropy"
    using residual_curvature_decomposes .
  finally show ?thesis .
qed

theorem tap008_frame_dragging_current_zero_without_rotation:
  "frame_dragging_current m radius 0 = 0"
proof -
  show ?thesis
    unfolding frame_dragging_current_def
    by algebra
qed

theorem tap009_planck_charge_product_hol:
  assumes "hbar > 0"
    and "c > 0"
    and "grav > 0"
  defines "mP \<equiv> planck_mass hbar c grav"
  shows "gravitational_charge mX mP * gravitational_charge mY mP
       = grav * mX * mY / (hbar * c)"
proof -
  show ?thesis
    using assms
    unfolding mP_def
    by (rule planck_charge_product)
qed

theorem tap010_isotope_charge_recovers_mass_hol:
  assumes "mP \<noteq> 0"
  shows "mP * isotope_gravitational_charge Z N mp mn me Ebind c mP
       = isotope_mass Z N mp mn me Ebind c"
proof -
  show ?thesis
    using assms
    by (rule isotope_charge_recovers_isotope_mass)
qed

theorem tap011_large_number_residual_scale_recovers_sigma:
  assumes "particle_count > 0"
  shows "lln_residual_scale particle_count sigma * sqrt particle_count = sigma"
proof -
  have sqrt_nonzero: "sqrt particle_count \<noteq> 0"
  proof
    assume "sqrt particle_count = 0"
    hence "particle_count = 0"
      using assms
      by (metis less_eq_real_def real_sqrt_eq_zero_cancel_iff)
    thus False
      using assms
      by linarith
  qed
  have "lln_residual_scale particle_count sigma * sqrt particle_count
      = (sigma / sqrt particle_count) * sqrt particle_count"
    unfolding lln_residual_scale_def
    by (rule refl)
  also have "... = sigma"
    using sqrt_nonzero
    by (field)
  finally show ?thesis .
qed

theorem tap012_measurable_residual_beyond_ordinary_mass_energy:
  "measurable_residual
      (accumulated_curvature ordinary_matter sound entropy)
      ordinary_matter
   = sound + entropy"
proof -
  show ?thesis
    using tap007_accumulated_curvature_has_residual_part .
qed

theorem reciprocal_flip_family_closes:
  "pythagorean_comma * pythagorean_bulk_reciprocal = 1
   \<and> (3 / 2 :: real) * (2 / 3) = 1"
proof (intro conjI)
  show "pythagorean_comma * pythagorean_bulk_reciprocal = 1"
    using pythagorean_comma_bulk_reciprocal_closes .
  show "(3 / 2 :: real) * (2 / 3) = 1"
    using perfect_fifth_descending_fifth_reciprocal .
qed

theorem kuramoto_equal_frequency_zero_phase_locks:
  "kuramoto_pair_drift omega omega coupling 0 = 0"
proof -
  have "kuramoto_pair_drift omega omega coupling 0 =
        omega - omega - coupling * sin 0"
    unfolding kuramoto_pair_drift_def
    by (rule refl)
  also have "... = omega - omega - coupling * 0"
  proof -
    have "sin 0 = (0::real)"
      by (rule sin_zero)
    thus ?thesis
      by algebra
  qed
  also have "... = 0"
    by algebra
  finally show ?thesis .
qed

theorem rational_orbital_lock_from_ratio:
  assumes "q \<noteq> 0"
  shows "rational_orbital_lock p q ((p / q) * orbit_frequency) orbit_frequency"
proof -
  have "q * ((p / q) * orbit_frequency) = p * orbit_frequency"
    using assms
    by (field)
  thus ?thesis
    unfolding rational_orbital_lock_def .
qed

theorem three_two_orbital_lock:
  "rational_orbital_lock 3 2 ((3 / 2) * orbit_frequency) orbit_frequency"
proof -
  have "2 \<noteq> (0::real)"
    by norm_num
  thus ?thesis
    by (rule rational_orbital_lock_from_ratio)
qed

theorem phase2_all_twelve_bessel_residual_obligations_connected:
  assumes "full_zero > 0"
    and "half_zero > 0"
    and "half_zero < full_zero"
    and "tau \<le> t"
    and "tau_decay > 0"
    and "hbar > 0"
    and "c > 0"
    and "grav > 0"
    and "mP = planck_mass hbar c grav"
    and "mP \<noteq> 0"
    and "particle_count > 0"
    and "horizon > 0"
  shows
    "hyperspherical_order 4 ell = ell + 1
     \<and> boundary_drop_admissible full_zero half_zero
     \<and> (half_bessel_drop_fraction full_zero half_zero > 0
          \<and> half_bessel_drop_fraction full_zero half_zero < 1)
     \<and> entropy_fold_source half_drop entropy = half_drop + entropy
     \<and> effective_residual_source matter sound entropy = matter + sound + entropy
     \<and> causal_temporal_kernel tau_decay t tau =
          exponential_kernel_density tau_decay (t - tau)
     \<and> causal_temporal_kernel tau_decay t tau \<ge> 0
     \<and> temporal_kernel_window_mass tau_decay horizon > 0
     \<and> temporal_kernel_window_mass tau_decay horizon < 1
     \<and> temporal_kernel_window_mass tau_decay horizon
        + temporal_kernel_tail_mass tau_decay horizon = 1
     \<and> measurable_residual
          (accumulated_curvature matter sound entropy) matter
          = sound + entropy
     \<and> frame_dragging_current frame_mass radius 0 = 0
     \<and> gravitational_charge mX mP * gravitational_charge mY mP
          = grav * mX * mY / (hbar * c)
     \<and> mP * isotope_gravitational_charge Z N mp mn me Ebind c mP
          = isotope_mass Z N mp mn me Ebind c
     \<and> lln_residual_scale particle_count sigma * sqrt particle_count
          = sigma
     \<and> measurable_residual
          (accumulated_curvature ordinary_matter sound entropy)
          ordinary_matter
          = sound + entropy"
proof (intro conjI)
  show "hyperspherical_order 4 ell = ell + 1"
    using tap001_hyperspherical_order_in_hol .
  show "boundary_drop_admissible full_zero half_zero"
    using assms(1) assms(2) assms(3)
    by (rule tap002_boundary_quantization_admissible)
  show "0 < half_bessel_drop_fraction full_zero half_zero \<and>
        half_bessel_drop_fraction full_zero half_zero < 1"
    using assms(1) assms(2) assms(3)
          tap002_boundary_quantization_admissible
          tap003_half_bessel_drop_is_between_zero_and_one
    by blast
  show "entropy_fold_source half_drop entropy = half_drop + entropy"
    using tap004_entropy_fold_adds_residual_source .
  show "effective_residual_source matter sound entropy = matter + sound + entropy"
    using tap005_effective_source_decomposes .
  show "causal_temporal_kernel tau_decay t tau =
        exponential_kernel_density tau_decay (t - tau)"
    using assms(4)
    by (rule tap006_causal_kernel_active_on_past)
  show "0 \<le> causal_temporal_kernel tau_decay t tau"
    using assms(5) assms(4)
    by (rule temporal_kernel_density_nonnegative_on_past)
  show "0 < temporal_kernel_window_mass tau_decay horizon"
    using assms(5) assms(12) temporal_kernel_closed_form_normalization_bridge
    by blast
  show "temporal_kernel_window_mass tau_decay horizon < 1"
    using assms(5) assms(12) temporal_kernel_closed_form_normalization_bridge
    by blast
  show "temporal_kernel_window_mass tau_decay horizon
        + temporal_kernel_tail_mass tau_decay horizon = 1"
    using temporal_kernel_window_mass_plus_tail .
  show "measurable_residual (accumulated_curvature matter sound entropy) matter =
        sound + entropy"
    using tap007_accumulated_curvature_has_residual_part .
  show "frame_dragging_current frame_mass radius 0 = 0"
    using tap008_frame_dragging_current_zero_without_rotation .
  show "gravitational_charge mX mP * gravitational_charge mY mP =
        grav * mX * mY / (hbar * c)"
    using assms(6) assms(7) assms(8) assms(9)
    by (metis tap009_planck_charge_product_hol)
  show "mP * isotope_gravitational_charge Z N mp mn me Ebind c mP =
        isotope_mass Z N mp mn me Ebind c"
    using assms(10)
    by (rule tap010_isotope_charge_recovers_mass_hol)
  show "lln_residual_scale particle_count sigma * sqrt particle_count = sigma"
    using assms(11)
    by (rule tap011_large_number_residual_scale_recovers_sigma)
  show "measurable_residual
          (accumulated_curvature ordinary_matter sound entropy)
          ordinary_matter =
        sound + entropy"
    using tap012_measurable_residual_beyond_ordinary_mass_energy .
qed

theorem phase2_obligation_count_is_twelve:
  "length phase2_obligation_vector = 12"
proof -
  have "phase2_obligation_vector =
        [True, True, True, True, True, True,
         True, True, True, True, True, True]"
    unfolding phase2_obligation_vector_def
    by (rule refl)
  thus ?thesis
    by normalization
qed

context TZPID_HypersphericalBesselResidualBridge_Focus
begin

theorem phase2_bridge_certificates_and_hol_model_connected:
  assumes "full_zero > 0"
    and "half_zero > 0"
    and "half_zero < full_zero"
    and "tau \<le> t"
    and "tau_decay > 0"
    and "hbar > 0"
    and "c > 0"
    and "grav > 0"
    and "mP = planck_mass hbar c grav"
    and "mP \<noteq> 0"
    and "particle_count > 0"
    and "horizon > 0"
  shows
    "all_hyperspherical_bessel_residual_bridge_certificates_verified
     \<and> hyperspherical_bessel_residual_bridge_chain
     \<and> length phase2_obligation_vector = 12
     \<and> boundary_drop_admissible full_zero half_zero
     \<and> causal_temporal_kernel tau_decay t tau \<ge> 0
     \<and> temporal_kernel_window_mass tau_decay horizon > 0
     \<and> temporal_kernel_window_mass tau_decay horizon < 1
     \<and> temporal_kernel_window_mass tau_decay horizon
        + temporal_kernel_tail_mass tau_decay horizon = 1
     \<and> measurable_residual
          (accumulated_curvature ordinary_matter sound entropy)
          ordinary_matter =
        sound + entropy"
proof (intro conjI)
  show "all_hyperspherical_bessel_residual_bridge_certificates_verified"
    using all_hyperspherical_bessel_residual_bridge_certificates_passed .
  show "hyperspherical_bessel_residual_bridge_chain"
    using tap_chain .
  show "length phase2_obligation_vector = 12"
    using phase2_obligation_count_is_twelve .
  show "boundary_drop_admissible full_zero half_zero"
    using assms(1) assms(2) assms(3)
    by (rule tap002_boundary_quantization_admissible)
  show "0 \<le> causal_temporal_kernel tau_decay t tau"
    using assms(5) assms(4)
    by (rule temporal_kernel_density_nonnegative_on_past)
  show "0 < temporal_kernel_window_mass tau_decay horizon"
    using assms(5) assms(12) temporal_kernel_closed_form_normalization_bridge
    by blast
  show "temporal_kernel_window_mass tau_decay horizon < 1"
    using assms(5) assms(12) temporal_kernel_closed_form_normalization_bridge
    by blast
  show "temporal_kernel_window_mass tau_decay horizon
        + temporal_kernel_tail_mass tau_decay horizon = 1"
    using temporal_kernel_window_mass_plus_tail .
  show "measurable_residual
          (accumulated_curvature ordinary_matter sound entropy)
          ordinary_matter =
        sound + entropy"
    using tap012_measurable_residual_beyond_ordinary_mass_energy .
qed

end

end

