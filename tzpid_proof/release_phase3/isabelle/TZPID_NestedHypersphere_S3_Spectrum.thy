theory TZPID_NestedHypersphere_S3_Spectrum
  imports TZPID_NestedHypersphere_Typed_Projection
begin

text \<open>
  Project: TZPID Proof Pipeline
  Creator: Daniel Alexander Trawin
  ORCID: https://orcid.org/0009-0001-4630-3715
  Generated UTC: 2026-06-08T00:00:00Z

  Global S3 spectrum layer for the nested-hypersphere spine.
  The Bessel bridge records radial boundary roots for cavity/ball modes;
  this theory records the closed S3 scalar Laplacian eigenvalue law
  lambda_n = n(n+2)/R^2.
\<close>

definition hs_s3_laplacian_eigenvalue :: "nat \<Rightarrow> hs_radius \<Rightarrow> real" where
  "hs_s3_laplacian_eigenvalue n R =
    real n * (real n + 2) / R\<^sup>2"

definition hs_s3_spectral_gap :: "nat \<Rightarrow> hs_radius \<Rightarrow> real" where
  "hs_s3_spectral_gap n R =
    hs_s3_laplacian_eigenvalue (Suc n) R -
    hs_s3_laplacian_eigenvalue n R"

definition hs_s3_mode_ratio :: "nat \<Rightarrow> nat \<Rightarrow> hs_radius \<Rightarrow> real" where
  "hs_s3_mode_ratio m n R =
    hs_s3_laplacian_eigenvalue m R /
    hs_s3_laplacian_eigenvalue n R"

definition hs_fractal_hopf_frequency :: "real \<Rightarrow> hs_frequency \<Rightarrow> nat \<Rightarrow> hs_frequency" where
  "hs_fractal_hopf_frequency alpha fundamental k =
    fundamental * alpha ^ k"

definition hs_fractal_hopf_radius :: "real \<Rightarrow> hs_radius \<Rightarrow> nat \<Rightarrow> hs_radius" where
  "hs_fractal_hopf_radius alpha R k =
    R * alpha ^ k"

definition hs_projected_log_periodic_shell :: "real \<Rightarrow> hs_radius \<Rightarrow> nat \<Rightarrow> hs_radius" where
  "hs_projected_log_periodic_shell alpha base_radius k =
    base_radius * alpha ^ k"

definition hs_inward_hopf_contraction :: "real \<Rightarrow> bool" where
  "hs_inward_hopf_contraction alpha \<longleftrightarrow> 0 < alpha \<and> alpha < 1"

lemma hs_s3_eigenvalue_zero_mode:
  "hs_s3_laplacian_eigenvalue 0 R = 0"
  unfolding hs_s3_laplacian_eigenvalue_def
  by algebra

lemma hs_s3_eigenvalue_nonnegative:
  assumes "R \<noteq> 0"
  shows "0 \<le> hs_s3_laplacian_eigenvalue n R"
proof -
  have numerator_nonnegative: "0 \<le> real n * (real n + 2)"
    by positivity
  have denominator_positive: "0 < R\<^sup>2"
    using assms
    by positivity
  show ?thesis
    unfolding hs_s3_laplacian_eigenvalue_def
    using numerator_nonnegative denominator_positive
    by (metis divide_nonneg_pos)
qed

lemma hs_s3_eigenvalue_scales_inverse_radius_squared:
  assumes "R \<noteq> 0"
    and "scale \<noteq> 0"
  shows "hs_s3_laplacian_eigenvalue n (scale * R) =
    hs_s3_laplacian_eigenvalue n R / scale\<^sup>2"
proof -
  have scale_sq_nonzero: "scale\<^sup>2 \<noteq> 0"
    using assms(2)
    by positivity
  have radius_sq_nonzero: "R\<^sup>2 \<noteq> 0"
    using assms(1)
    by positivity
  show ?thesis
    unfolding hs_s3_laplacian_eigenvalue_def
    using scale_sq_nonzero radius_sq_nonzero
    by field
qed

lemma hs_s3_mode_ratio_scale_free:
  assumes "R \<noteq> 0"
    and "scale \<noteq> 0"
    and "hs_s3_laplacian_eigenvalue n R \<noteq> 0"
  shows "hs_s3_mode_ratio m n (scale * R) =
    hs_s3_mode_ratio m n R"
proof -
  have scaled_n_nonzero: "hs_s3_laplacian_eigenvalue n (scale * R) \<noteq> 0"
  proof -
    have "hs_s3_laplacian_eigenvalue n (scale * R) =
        hs_s3_laplacian_eigenvalue n R / scale\<^sup>2"
      using assms(1,2)
      by (rule hs_s3_eigenvalue_scales_inverse_radius_squared)
    moreover have "scale\<^sup>2 \<noteq> 0"
      using assms(2)
      by positivity
    ultimately show ?thesis
      using assms(3)
      by force
  qed
  have scaled_m:
    "hs_s3_laplacian_eigenvalue m (scale * R) =
      hs_s3_laplacian_eigenvalue m R / scale\<^sup>2"
    using assms(1,2)
    by (rule hs_s3_eigenvalue_scales_inverse_radius_squared)
  have scaled_n:
    "hs_s3_laplacian_eigenvalue n (scale * R) =
      hs_s3_laplacian_eigenvalue n R / scale\<^sup>2"
    using assms(1,2)
    by (rule hs_s3_eigenvalue_scales_inverse_radius_squared)
  have scale_sq_nonzero: "scale\<^sup>2 \<noteq> 0"
    using assms(2)
    by positivity
  show ?thesis
    unfolding hs_s3_mode_ratio_def
    using scaled_m scaled_n assms(3) scaled_n_nonzero scale_sq_nonzero
    by field
qed

lemma hs_s3_spectral_gap_closed_form:
  assumes "R \<noteq> 0"
  shows "hs_s3_spectral_gap n R = (2 * real n + 3) / R\<^sup>2"
proof -
  have radius_sq_nonzero: "R\<^sup>2 \<noteq> 0"
    using assms
    by positivity
  show ?thesis
    unfolding hs_s3_spectral_gap_def hs_s3_laplacian_eigenvalue_def
    using radius_sq_nonzero
    by field
qed

lemma hs_fractal_hopf_frequency_zero_level:
  "hs_fractal_hopf_frequency alpha fundamental 0 = fundamental"
  unfolding hs_fractal_hopf_frequency_def
  by algebra

lemma hs_fractal_hopf_frequency_successor_ratio:
  assumes "fundamental \<noteq> 0"
    and "alpha \<noteq> 0"
  shows "hs_fractal_hopf_frequency alpha fundamental (Suc k) /
    hs_fractal_hopf_frequency alpha fundamental k = alpha"
proof -
  have alpha_power_nonzero: "alpha ^ k \<noteq> 0"
    using assms(2)
    by (metis power_eq_0_iff)
  have denom_nonzero:
    "hs_fractal_hopf_frequency alpha fundamental k \<noteq> 0"
    unfolding hs_fractal_hopf_frequency_def
    using assms(1) alpha_power_nonzero
    by (metis mult_eq_0_iff)
  have successor:
    "hs_fractal_hopf_frequency alpha fundamental (Suc k) =
      alpha * hs_fractal_hopf_frequency alpha fundamental k"
    unfolding hs_fractal_hopf_frequency_def
    by (metis mult.assoc mult.commute power_Suc)
  show ?thesis
    using successor denom_nonzero
    by field
qed

lemma hs_projected_log_periodic_shell_successor_ratio:
  assumes "base_radius \<noteq> 0"
    and "alpha \<noteq> 0"
  shows "hs_projected_log_periodic_shell alpha base_radius (Suc k) /
    hs_projected_log_periodic_shell alpha base_radius k = alpha"
proof -
  have alpha_power_nonzero: "alpha ^ k \<noteq> 0"
    using assms(2)
    by (metis power_eq_0_iff)
  have denom_nonzero:
    "hs_projected_log_periodic_shell alpha base_radius k \<noteq> 0"
    unfolding hs_projected_log_periodic_shell_def
    using assms(1) alpha_power_nonzero
    by (metis mult_eq_0_iff)
  have successor:
    "hs_projected_log_periodic_shell alpha base_radius (Suc k) =
      alpha * hs_projected_log_periodic_shell alpha base_radius k"
    unfolding hs_projected_log_periodic_shell_def
    by (metis mult.assoc mult.commute power_Suc)
  show ?thesis
    using successor denom_nonzero
    by field
qed

lemma hs_s3_nested_radius_eigenvalue_scales:
  assumes "R \<noteq> 0"
    and "alpha \<noteq> 0"
  shows "hs_s3_laplacian_eigenvalue n (hs_fractal_hopf_radius alpha R k) =
    hs_s3_laplacian_eigenvalue n R / (alpha ^ k)\<^sup>2"
proof -
  have radius_eq:
    "hs_fractal_hopf_radius alpha R k = alpha ^ k * R"
    unfolding hs_fractal_hopf_radius_def
    by algebra
  have alpha_power_nonzero: "alpha ^ k \<noteq> 0"
    using assms(2)
    by (metis power_eq_0_iff)
  have scaled:
    "hs_s3_laplacian_eigenvalue n ((alpha ^ k) * R) =
      hs_s3_laplacian_eigenvalue n R / (alpha ^ k)\<^sup>2"
    using assms(1) alpha_power_nonzero
    by (rule hs_s3_eigenvalue_scales_inverse_radius_squared)
  show ?thesis
    using radius_eq scaled
    by presburger
qed

theorem hs_s3_global_spectrum_contract:
  assumes "R \<noteq> 0"
    and "scale \<noteq> 0"
    and "hs_s3_laplacian_eigenvalue n R \<noteq> 0"
  shows "0 \<le> hs_s3_laplacian_eigenvalue m R
    \<and> hs_s3_laplacian_eigenvalue 0 R = 0
    \<and> hs_s3_laplacian_eigenvalue m (scale * R) =
        hs_s3_laplacian_eigenvalue m R / scale\<^sup>2
    \<and> hs_s3_mode_ratio m n (scale * R) =
        hs_s3_mode_ratio m n R
    \<and> hs_s3_spectral_gap m R = (2 * real m + 3) / R\<^sup>2"
proof (intro conjI)
  show "0 \<le> hs_s3_laplacian_eigenvalue m R"
    using assms(1)
    by (rule hs_s3_eigenvalue_nonnegative)
  show "hs_s3_laplacian_eigenvalue 0 R = 0"
    using hs_s3_eigenvalue_zero_mode .
  show "hs_s3_laplacian_eigenvalue m (scale * R) =
      hs_s3_laplacian_eigenvalue m R / scale\<^sup>2"
    using assms(1,2)
    by (rule hs_s3_eigenvalue_scales_inverse_radius_squared)
  show "hs_s3_mode_ratio m n (scale * R) =
      hs_s3_mode_ratio m n R"
    using assms
    by (rule hs_s3_mode_ratio_scale_free)
  show "hs_s3_spectral_gap m R = (2 * real m + 3) / R\<^sup>2"
    using assms(1)
    by (rule hs_s3_spectral_gap_closed_form)
qed

theorem hs_fractal_inward_hopf_vibration_contract:
  assumes "R \<noteq> 0"
    and "fundamental \<noteq> 0"
    and "base_radius \<noteq> 0"
    and "hs_inward_hopf_contraction alpha"
  shows "hs_fractal_hopf_frequency alpha fundamental 0 = fundamental
    \<and> hs_fractal_hopf_frequency alpha fundamental (Suc k) /
        hs_fractal_hopf_frequency alpha fundamental k = alpha
    \<and> hs_projected_log_periodic_shell alpha base_radius (Suc k) /
        hs_projected_log_periodic_shell alpha base_radius k = alpha
    \<and> hs_s3_laplacian_eigenvalue n (hs_fractal_hopf_radius alpha R k) =
        hs_s3_laplacian_eigenvalue n R / (alpha ^ k)\<^sup>2"
proof (intro conjI)
  have alpha_nonzero: "alpha \<noteq> 0"
    using assms(4)
    unfolding hs_inward_hopf_contraction_def
    by linarith
  show "hs_fractal_hopf_frequency alpha fundamental 0 = fundamental"
    using hs_fractal_hopf_frequency_zero_level .
  show "hs_fractal_hopf_frequency alpha fundamental (Suc k) /
      hs_fractal_hopf_frequency alpha fundamental k = alpha"
    using assms(2) alpha_nonzero
    by (rule hs_fractal_hopf_frequency_successor_ratio)
  show "hs_projected_log_periodic_shell alpha base_radius (Suc k) /
      hs_projected_log_periodic_shell alpha base_radius k = alpha"
    using assms(3) alpha_nonzero
    by (rule hs_projected_log_periodic_shell_successor_ratio)
  show "hs_s3_laplacian_eigenvalue n (hs_fractal_hopf_radius alpha R k) =
      hs_s3_laplacian_eigenvalue n R / (alpha ^ k)\<^sup>2"
    using assms(1) alpha_nonzero
    by (rule hs_s3_nested_radius_eigenvalue_scales)
qed

context TZPID_NestedHypersphere_Focus
begin

theorem nested_hypersphere_s3_spectrum_extends_spine:
  assumes "R \<noteq> 0"
    and "scale \<noteq> 0"
    and "hs_s3_laplacian_eigenvalue n R \<noteq> 0"
  shows "nested_hypersphere_unifying_chain
    \<and> 0 \<le> hs_s3_laplacian_eigenvalue m R
    \<and> hs_s3_laplacian_eigenvalue m (scale * R) =
        hs_s3_laplacian_eigenvalue m R / scale\<^sup>2
    \<and> hs_s3_mode_ratio m n (scale * R) =
        hs_s3_mode_ratio m n R"
proof (intro conjI)
  show "nested_hypersphere_unifying_chain"
    using unifying_chain .
  show "0 \<le> hs_s3_laplacian_eigenvalue m R"
    using assms(1)
    by (rule hs_s3_eigenvalue_nonnegative)
  show "hs_s3_laplacian_eigenvalue m (scale * R) =
      hs_s3_laplacian_eigenvalue m R / scale\<^sup>2"
    using assms(1,2)
    by (rule hs_s3_eigenvalue_scales_inverse_radius_squared)
  show "hs_s3_mode_ratio m n (scale * R) =
      hs_s3_mode_ratio m n R"
    using assms
    by (rule hs_s3_mode_ratio_scale_free)
qed

theorem nested_hypersphere_fractal_hopf_vibration_extends_spine:
  assumes "R \<noteq> 0"
    and "fundamental \<noteq> 0"
    and "base_radius \<noteq> 0"
    and "hs_inward_hopf_contraction alpha"
  shows "nested_hypersphere_unifying_chain
    \<and> hs_fractal_hopf_frequency alpha fundamental 0 = fundamental
    \<and> hs_fractal_hopf_frequency alpha fundamental (Suc k) /
        hs_fractal_hopf_frequency alpha fundamental k = alpha
    \<and> hs_projected_log_periodic_shell alpha base_radius (Suc k) /
        hs_projected_log_periodic_shell alpha base_radius k = alpha
    \<and> hs_s3_laplacian_eigenvalue n (hs_fractal_hopf_radius alpha R k) =
        hs_s3_laplacian_eigenvalue n R / (alpha ^ k)\<^sup>2"
proof (intro conjI)
  show "nested_hypersphere_unifying_chain"
    using unifying_chain .
  have contract:
    "hs_fractal_hopf_frequency alpha fundamental 0 = fundamental
     \<and> hs_fractal_hopf_frequency alpha fundamental (Suc k) /
        hs_fractal_hopf_frequency alpha fundamental k = alpha
     \<and> hs_projected_log_periodic_shell alpha base_radius (Suc k) /
        hs_projected_log_periodic_shell alpha base_radius k = alpha
     \<and> hs_s3_laplacian_eigenvalue n (hs_fractal_hopf_radius alpha R k) =
        hs_s3_laplacian_eigenvalue n R / (alpha ^ k)\<^sup>2"
    using assms
    by (rule hs_fractal_inward_hopf_vibration_contract)
  show "hs_fractal_hopf_frequency alpha fundamental 0 = fundamental"
    using contract
    by blast
  show "hs_fractal_hopf_frequency alpha fundamental (Suc k) /
      hs_fractal_hopf_frequency alpha fundamental k = alpha"
    using contract
    by blast
  show "hs_projected_log_periodic_shell alpha base_radius (Suc k) /
      hs_projected_log_periodic_shell alpha base_radius k = alpha"
    using contract
    by blast
  show "hs_s3_laplacian_eigenvalue n (hs_fractal_hopf_radius alpha R k) =
      hs_s3_laplacian_eigenvalue n R / (alpha ^ k)\<^sup>2"
    using contract
    by blast
qed

end

end
