theory TZPID_Bessel_External_Certificates
  imports TZPID_HypersphericalBesselResidualBridge_Phase2_Model
begin

text \<open>
  Project: TZPID Proof Pipeline
  Creator: Daniel Alexander Trawin
  ORCID: https://orcid.org/0009-0001-4630-3715
  Generated UTC: 2026-06-08T02:08:00Z

  Boundary-root policy for the Hyperspherical Bessel residual bridge.
  Isabelle2025/HOL-Analysis in this workspace does not expose a native Bessel
  zero library.  Therefore the analytic Bessel root values remain external
  Wolfram-certified numerics, while Isabelle proves the algebraic consequences
  of explicit rational interval certificates around those values.

  Certified source values used by the paper layer:
    j_{1,1} approximately 3.83170597
    j_{1/2,1} = pi approximately 3.14159265
    drop = (j_{1,1} - j_{1/2,1}) / j_{1,1} approximately 0.180106
\<close>

definition bessel_j11_lower :: real where
  "bessel_j11_lower = 383170597 / 100000000"

definition bessel_j11_upper :: real where
  "bessel_j11_upper = 383170598 / 100000000"

definition bessel_jhalf_lower :: real where
  "bessel_jhalf_lower = 314159265 / 100000000"

definition bessel_jhalf_upper :: real where
  "bessel_jhalf_upper = 314159266 / 100000000"

definition certified_bessel_zero_intervals :: "real \<Rightarrow> real \<Rightarrow> bool" where
  "certified_bessel_zero_intervals full_zero half_zero =
     (bessel_j11_lower \<le> full_zero
      \<and> full_zero \<le> bessel_j11_upper
      \<and> bessel_jhalf_lower \<le> half_zero
      \<and> half_zero \<le> bessel_jhalf_upper)"

definition bessel_zero_policy :: string where
  "bessel_zero_policy =
     ''external_wolfram_interval_certificate_no_native_isabelle_bessel_library''"

theorem bessel_external_interval_bounds_ordered:
  "0 < bessel_jhalf_lower
   \<and> bessel_jhalf_lower \<le> bessel_jhalf_upper
   \<and> bessel_jhalf_upper < bessel_j11_lower
   \<and> bessel_j11_lower \<le> bessel_j11_upper"
proof (intro conjI)
  show "0 < bessel_jhalf_lower"
    unfolding bessel_jhalf_lower_def
    by norm_num
  show "bessel_jhalf_lower \<le> bessel_jhalf_upper"
    unfolding bessel_jhalf_lower_def bessel_jhalf_upper_def
    by norm_num
  show "bessel_jhalf_upper < bessel_j11_lower"
    unfolding bessel_jhalf_upper_def bessel_j11_lower_def
    by norm_num
  show "bessel_j11_lower \<le> bessel_j11_upper"
    unfolding bessel_j11_lower_def bessel_j11_upper_def
    by norm_num
qed

theorem certified_bessel_intervals_imply_boundary_admissible:
  assumes intervals: "certified_bessel_zero_intervals full_zero half_zero"
  shows "boundary_drop_admissible full_zero half_zero"
proof -
  have lower_order:
    "0 < bessel_jhalf_lower
     \<and> bessel_jhalf_lower \<le> bessel_jhalf_upper
     \<and> bessel_jhalf_upper < bessel_j11_lower
     \<and> bessel_j11_lower \<le> bessel_j11_upper"
    using bessel_external_interval_bounds_ordered .
  have full_ge: "bessel_j11_lower \<le> full_zero"
    using intervals
    unfolding certified_bessel_zero_intervals_def
    by blast
  have half_ge: "bessel_jhalf_lower \<le> half_zero"
    using intervals
    unfolding certified_bessel_zero_intervals_def
    by blast
  have half_le: "half_zero \<le> bessel_jhalf_upper"
    using intervals
    unfolding certified_bessel_zero_intervals_def
    by blast
  have half_upper_lt_full_lower: "bessel_jhalf_upper < bessel_j11_lower"
    using lower_order
    by blast
  have half_lower_pos: "0 < bessel_jhalf_lower"
    using lower_order
    by blast
  have full_pos: "0 < full_zero"
    using full_ge half_upper_lt_full_lower half_lower_pos
    by linarith
  have half_pos: "0 < half_zero"
    using half_ge half_lower_pos
    by linarith
  have half_lt_full: "half_zero < full_zero"
    using half_le full_ge half_upper_lt_full_lower
    by linarith
  show ?thesis
    using full_pos half_pos half_lt_full
    by (rule tap002_boundary_quantization_admissible)
qed

theorem bessel_drop_interval_for_certified_zeros:
  assumes intervals: "certified_bessel_zero_intervals full_zero half_zero"
  shows "(18 / 100 :: real) < half_bessel_drop_fraction full_zero half_zero
       \<and> half_bessel_drop_fraction full_zero half_zero < (19 / 100 :: real)"
proof -
  have admissible: "boundary_drop_admissible full_zero half_zero"
    using intervals
    by (rule certified_bessel_intervals_imply_boundary_admissible)
  have full_pos: "0 < full_zero"
    using admissible
    unfolding boundary_drop_admissible_def positive_boundary_zero_def
    by blast
  have full_ge: "bessel_j11_lower \<le> full_zero"
    using intervals
    unfolding certified_bessel_zero_intervals_def
    by blast
  have full_le: "full_zero \<le> bessel_j11_upper"
    using intervals
    unfolding certified_bessel_zero_intervals_def
    by blast
  have half_ge: "bessel_jhalf_lower \<le> half_zero"
    using intervals
    unfolding certified_bessel_zero_intervals_def
    by blast
  have half_le: "half_zero \<le> bessel_jhalf_upper"
    using intervals
    unfolding certified_bessel_zero_intervals_def
    by blast
  have lower_numeric:
    "bessel_jhalf_upper < (82 / 100 :: real) * bessel_j11_lower"
    unfolding bessel_jhalf_upper_def bessel_j11_lower_def
    by norm_num
  have upper_numeric:
    "(81 / 100 :: real) * bessel_j11_upper < bessel_jhalf_lower"
    unfolding bessel_j11_upper_def bessel_jhalf_lower_def
    by norm_num
  have lower_linear: "half_zero < (82 / 100 :: real) * full_zero"
    using half_le full_ge lower_numeric
    by linarith
  have upper_linear: "(81 / 100 :: real) * full_zero < half_zero"
    using full_le half_ge upper_numeric
    by linarith
  have lower_drop:
    "(18 / 100 :: real) < half_bessel_drop_fraction full_zero half_zero"
  proof -
    have "(18 / 100 :: real) < (full_zero - half_zero) / full_zero"
      using full_pos lower_linear
      by (field)
    thus ?thesis
      unfolding half_bessel_drop_fraction_def .
  qed
  have upper_drop:
    "half_bessel_drop_fraction full_zero half_zero < (19 / 100 :: real)"
  proof -
    have "(full_zero - half_zero) / full_zero < (19 / 100 :: real)"
      using full_pos upper_linear
      by (field)
    thus ?thesis
      unfolding half_bessel_drop_fraction_def .
  qed
  show ?thesis
  proof (intro conjI)
    show "(18 / 100 :: real) < half_bessel_drop_fraction full_zero half_zero"
      using lower_drop .
    show "half_bessel_drop_fraction full_zero half_zero < (19 / 100 :: real)"
      using upper_drop .
  qed
qed

theorem paper_bessel_representative_intervals_hold:
  "certified_bessel_zero_intervals
     (383170597 / 100000000)
     (314159265 / 100000000)"
proof -
  have "bessel_j11_lower \<le> (383170597 / 100000000 :: real)
      \<and> (383170597 / 100000000 :: real) \<le> bessel_j11_upper
      \<and> bessel_jhalf_lower \<le> (314159265 / 100000000 :: real)
      \<and> (314159265 / 100000000 :: real) \<le> bessel_jhalf_upper"
    unfolding bessel_j11_lower_def bessel_j11_upper_def
      bessel_jhalf_lower_def bessel_jhalf_upper_def
    by norm_num
  thus ?thesis
    unfolding certified_bessel_zero_intervals_def .
qed

definition radial_phase :: "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real" where
  "radial_phase zero R r = zero * (r / R)"

definition delta_alpha_phase :: "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real" where
  "delta_alpha_phase full_zero half_zero R r =
     radial_phase full_zero R r - radial_phase half_zero R r"

definition bessel_phase_gradient :: "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real" where
  "bessel_phase_gradient full_zero half_zero R =
     (full_zero / R) * half_bessel_drop_fraction full_zero half_zero"

definition bessel_shell_radius :: "nat \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real" where
  "bessel_shell_radius n R full_zero delta =
     (real n * pi * R) / (full_zero * delta)"

theorem delta_alpha_phase_difference:
  "delta_alpha_phase full_zero half_zero R r =
     (full_zero - half_zero) * r / R"
proof -
  have "delta_alpha_phase full_zero half_zero R r =
      full_zero * (r / R) - half_zero * (r / R)"
    unfolding delta_alpha_phase_def radial_phase_def
    by (rule refl)
  also have "... = (full_zero - half_zero) * r / R"
    by algebra
  finally show ?thesis .
qed

theorem drop_fraction_induces_phase_gradient:
  assumes admissible: "boundary_drop_admissible full_zero half_zero"
    and radius_nonzero: "R \<noteq> 0"
  shows "delta_alpha_phase full_zero half_zero R r =
     bessel_phase_gradient full_zero half_zero R * r"
proof -
  have full_pos: "0 < full_zero"
    using admissible
    unfolding boundary_drop_admissible_def positive_boundary_zero_def
    by blast
  have full_nonzero: "full_zero \<noteq> 0"
    using full_pos
    by linarith
  have "delta_alpha_phase full_zero half_zero R r =
      (full_zero - half_zero) * r / R"
    using delta_alpha_phase_difference .
  also have "... =
      ((full_zero / R) * ((full_zero - half_zero) / full_zero)) * r"
    using full_nonzero radius_nonzero
    by field
  also have "... = bessel_phase_gradient full_zero half_zero R * r"
    unfolding bessel_phase_gradient_def half_bessel_drop_fraction_def .
  finally show ?thesis .
qed

theorem drop_fraction_induces_phase_gradient_exists:
  assumes admissible: "boundary_drop_admissible full_zero half_zero"
    and radius_nonzero: "R \<noteq> 0"
  shows "\<exists>k_eff. \<forall>r.
     delta_alpha_phase full_zero half_zero R r = k_eff * r
     \<and> k_eff = (full_zero / R) *
          half_bessel_drop_fraction full_zero half_zero"
proof -
  let ?k = "bessel_phase_gradient full_zero half_zero R"
  have phase: "\<And>r. delta_alpha_phase full_zero half_zero R r = ?k * r"
    using admissible radius_nonzero
    by (rule drop_fraction_induces_phase_gradient)
  have k_eq:
    "?k = (full_zero / R) * half_bessel_drop_fraction full_zero half_zero"
    unfolding bessel_phase_gradient_def
    by (rule refl)
  show ?thesis
    using phase k_eq
    by blast
qed

theorem bessel_shell_radius_solves_delta_alpha_quantization:
  assumes admissible: "boundary_drop_admissible full_zero half_zero"
    and radius_nonzero: "R \<noteq> 0"
  defines "delta \<equiv> half_bessel_drop_fraction full_zero half_zero"
  shows "delta_alpha_phase full_zero half_zero R
      (bessel_shell_radius n R full_zero delta) = real n * pi"
proof -
  have drop_bounds:
    "0 < half_bessel_drop_fraction full_zero half_zero
     \<and> half_bessel_drop_fraction full_zero half_zero < 1"
    using admissible
    by (rule tap003_half_bessel_drop_is_between_zero_and_one)
  have drop_pos: "0 < delta"
    using drop_bounds
    unfolding delta_def
    by blast
  have full_pos: "0 < full_zero"
    using admissible
    unfolding boundary_drop_admissible_def positive_boundary_zero_def
    by blast
  have denom_nonzero: "full_zero * delta \<noteq> 0"
    using full_pos drop_pos
    by (metis less_irrefl mult_eq_0_iff)
  have phase:
    "delta_alpha_phase full_zero half_zero R
      (bessel_shell_radius n R full_zero delta) =
       ((full_zero / R) * delta) *
        bessel_shell_radius n R full_zero delta"
    using admissible radius_nonzero
    unfolding delta_def
    by (rule drop_fraction_induces_phase_gradient)
  also have "... = real n * pi"
    using radius_nonzero denom_nonzero
    unfolding bessel_shell_radius_def
    by field
  finally show ?thesis .
qed

theorem certified_bessel_delta_alpha_phase_bridge:
  assumes intervals: "certified_bessel_zero_intervals full_zero half_zero"
    and radius_nonzero: "R \<noteq> 0"
  shows "\<exists>k_eff. \<forall>r.
     delta_alpha_phase full_zero half_zero R r = k_eff * r
     \<and> (18 / 100 :: real) <
          half_bessel_drop_fraction full_zero half_zero
     \<and> half_bessel_drop_fraction full_zero half_zero <
          (19 / 100 :: real)"
proof -
  have admissible: "boundary_drop_admissible full_zero half_zero"
    using intervals
    by (rule certified_bessel_intervals_imply_boundary_admissible)
  have drop_window:
    "(18 / 100 :: real) < half_bessel_drop_fraction full_zero half_zero
     \<and> half_bessel_drop_fraction full_zero half_zero < (19 / 100 :: real)"
    using intervals
    by (rule bessel_drop_interval_for_certified_zeros)
  obtain k_eff where phase:
    "\<forall>r. delta_alpha_phase full_zero half_zero R r = k_eff * r
       \<and> k_eff = (full_zero / R) *
          half_bessel_drop_fraction full_zero half_zero"
    using admissible radius_nonzero
    by (meson drop_fraction_induces_phase_gradient_exists)
  show ?thesis
    using phase drop_window
    by blast
qed

context TZPID_HypersphericalBesselResidualBridge_Focus
begin

theorem bessel_external_certificate_policy_connected:
  "all_hyperspherical_bessel_residual_bridge_certificates_verified
   \<and> bessel_zero_policy =
      ''external_wolfram_interval_certificate_no_native_isabelle_bessel_library''
   \<and> boundary_drop_admissible
      (383170597 / 100000000)
      (314159265 / 100000000)
   \<and> (18 / 100 :: real) <
      half_bessel_drop_fraction
        (383170597 / 100000000)
        (314159265 / 100000000)
   \<and> half_bessel_drop_fraction
        (383170597 / 100000000)
        (314159265 / 100000000)
      < (19 / 100 :: real)
   \<and> (\<exists>k_eff. \<forall>r.
      delta_alpha_phase
        (383170597 / 100000000)
        (314159265 / 100000000)
        (1 :: real) r = k_eff * r)"
proof (intro conjI)
  show "all_hyperspherical_bessel_residual_bridge_certificates_verified"
    using all_hyperspherical_bessel_residual_bridge_certificates_passed .
  show "bessel_zero_policy =
      ''external_wolfram_interval_certificate_no_native_isabelle_bessel_library''"
    unfolding bessel_zero_policy_def
    by (rule refl)
  show "boundary_drop_admissible
      (383170597 / 100000000)
      (314159265 / 100000000)"
    using paper_bessel_representative_intervals_hold
    by (rule certified_bessel_intervals_imply_boundary_admissible)
  have drop_window:
    "(18 / 100 :: real) <
      half_bessel_drop_fraction
        (383170597 / 100000000)
        (314159265 / 100000000)
     \<and> half_bessel_drop_fraction
        (383170597 / 100000000)
        (314159265 / 100000000)
      < (19 / 100 :: real)"
    using paper_bessel_representative_intervals_hold
    by (rule bessel_drop_interval_for_certified_zeros)
  show "(18 / 100 :: real) <
      half_bessel_drop_fraction
        (383170597 / 100000000)
        (314159265 / 100000000)"
    using drop_window
    by blast
  show "half_bessel_drop_fraction
        (383170597 / 100000000)
        (314159265 / 100000000)
      < (19 / 100 :: real)"
    using drop_window
    by blast
  have phase_bridge:
    "\<exists>k_eff. \<forall>r.
      delta_alpha_phase
        (383170597 / 100000000)
        (314159265 / 100000000)
        (1 :: real) r = k_eff * r
      \<and> (18 / 100 :: real) <
          half_bessel_drop_fraction
            (383170597 / 100000000)
            (314159265 / 100000000)
      \<and> half_bessel_drop_fraction
            (383170597 / 100000000)
            (314159265 / 100000000)
          < (19 / 100 :: real)"
    using paper_bessel_representative_intervals_hold
    by (rule certified_bessel_delta_alpha_phase_bridge, norm_num)
  thus "\<exists>k_eff. \<forall>r.
      delta_alpha_phase
        (383170597 / 100000000)
        (314159265 / 100000000)
        (1 :: real) r = k_eff * r"
    by blast
qed

end

end
