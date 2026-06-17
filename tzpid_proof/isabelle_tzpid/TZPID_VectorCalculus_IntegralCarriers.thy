theory TZPID_VectorCalculus_IntegralCarriers
  imports
    TZPID_VectorCalculus_IsarSpineLayer
    TZPID_GyromagneticMovement_CorrectedWinding
begin

text \<open>
  Project: TZPID Proof Pipeline
  Creator: Daniel Alexander Trawin
  ORCID: https://orcid.org/0009-0001-4630-3715
  Generated UTC: 2026-06-11T00:00:00Z

  Finite vector-calculus carrier layer for the spine stack.

  This theory turns the paper-facing vector claims into checkable finite
  carriers: rectangular circulation, constant-curl flux, divergence balance,
  uniform helicity, and winding/flux quantization.  It is deliberately finite
  dimensional.  The next refinement can replace these algebraic carriers with
  fuller HOL-Analysis line and surface integrals where a paper needs that
  additional analytic strength.
\<close>

section \<open>Planar Rectangle Carriers\<close>

definition vc_rectangle_area :: "real \<Rightarrow> real \<Rightarrow> real" where
  "vc_rectangle_area width height = width * height"

definition vc_bottom_segment :: "real \<Rightarrow> real \<Rightarrow> real" where
  "vc_bottom_segment curl_strength width = 0"

definition vc_right_segment :: "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real" where
  "vc_right_segment curl_strength width height =
    (curl_strength * width / 2) * height"

definition vc_top_segment :: "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real" where
  "vc_top_segment curl_strength width height =
    (curl_strength * height / 2) * width"

definition vc_left_segment :: "real \<Rightarrow> real \<Rightarrow> real" where
  "vc_left_segment curl_strength height = 0"

definition vc_rect_boundary_circulation ::
  "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real" where
  "vc_rect_boundary_circulation curl_strength width height =
     vc_bottom_segment curl_strength width
   + vc_right_segment curl_strength width height
   + vc_top_segment curl_strength width height
   + vc_left_segment curl_strength height"

definition vc_rect_surface_flux :: "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real" where
  "vc_rect_surface_flux curl_strength width height =
    curl_strength * vc_rectangle_area width height"

definition vc_planar_divergence :: "real \<Rightarrow> real \<Rightarrow> real" where
  "vc_planar_divergence partial_x_Fx partial_y_Fy =
    partial_x_Fx + partial_y_Fy"

definition vc_incompressible_planar :: "real \<Rightarrow> real \<Rightarrow> bool" where
  "vc_incompressible_planar partial_x_Fx partial_y_Fy \<longleftrightarrow>
    vc_planar_divergence partial_x_Fx partial_y_Fy = 0"

theorem vc_rectangle_area_nonnegative:
  assumes "0 \<le> width"
    and "0 \<le> height"
  shows "0 \<le> vc_rectangle_area width height"
proof -
  have "0 \<le> width * height"
    using assms
    by (rule mult_nonneg_nonneg)
  thus ?thesis
    unfolding vc_rectangle_area_def .
qed

theorem vc_rect_boundary_circulation_simplifies:
  "vc_rect_boundary_circulation curl_strength width height =
   curl_strength * width * height"
proof -
  have "vc_rect_boundary_circulation curl_strength width height =
    0 + (curl_strength * width / 2) * height
      + (curl_strength * height / 2) * width + 0"
    unfolding vc_rect_boundary_circulation_def
      vc_bottom_segment_def vc_right_segment_def
      vc_top_segment_def vc_left_segment_def
    by (rule refl)
  also have "\<dots> = curl_strength * width * height"
    by algebra
  finally show ?thesis .
qed

theorem vc_green_rectangle_constant_curl:
  "vc_rect_boundary_circulation curl_strength width height =
   vc_rect_surface_flux curl_strength width height"
proof -
  have circ:
    "vc_rect_boundary_circulation curl_strength width height =
     curl_strength * width * height"
    by (rule vc_rect_boundary_circulation_simplifies)

  have flux:
    "vc_rect_surface_flux curl_strength width height =
     curl_strength * width * height"
    unfolding vc_rect_surface_flux_def vc_rectangle_area_def
    by (rule refl)

  from circ flux show ?thesis
    by algebra
qed

theorem vc_incompressible_from_opposite_partials:
  assumes "partial_y_Fy = - partial_x_Fx"
  shows "vc_incompressible_planar partial_x_Fx partial_y_Fy"
proof -
  have "vc_planar_divergence partial_x_Fx partial_y_Fy = 0"
    unfolding vc_planar_divergence_def
    using assms
    by algebra
  thus ?thesis
    unfolding vc_incompressible_planar_def .
qed

section \<open>Helicity and Flux Carriers\<close>

definition vc_uniform_helicity_density ::
  "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real" where
  "vc_uniform_helicity_density ax ay az bx by bz =
    tv_helicity_density3 ax ay az bx by bz"

definition vc_uniform_helicity_integral :: "real \<Rightarrow> real \<Rightarrow> real" where
  "vc_uniform_helicity_integral volume density =
    tv_uniform_helicity volume density"

definition vc_quantized_circulation :: "int \<Rightarrow> real" where
  "vc_quantized_circulation m = 2 * pi * of_int m"

definition vc_quantized_flux :: "real \<Rightarrow> int \<Rightarrow> real" where
  "vc_quantized_flux flux_quantum m =
    tv_flux_multiple flux_quantum m"

theorem vc_helicity_density_zero_when_b_zero:
  "vc_uniform_helicity_density ax ay az 0 0 0 = 0"
proof -
  have "tv_helicity_density3 ax ay az 0 0 0 = 0"
    by (rule tv_helicity_density_zero_magnetic_field)
  thus ?thesis
    unfolding vc_uniform_helicity_density_def .
qed

theorem vc_uniform_helicity_integral_zero_density:
  "vc_uniform_helicity_integral volume 0 = 0"
proof -
  have "tv_uniform_helicity volume 0 = 0"
    by (rule tv_uniform_helicity_zero_density)
  thus ?thesis
    unfolding vc_uniform_helicity_integral_def .
qed

theorem vc_quantized_flux_is_topological_locking_flux:
  "vc_quantized_flux flux_quantum m =
   topological_locking_flux flux_quantum m"
proof -
  show ?thesis
    unfolding vc_quantized_flux_def topological_locking_flux_def
    by (rule refl)
qed

theorem vc_quantized_flux_is_quantized:
  "flux_quantized (vc_quantized_flux flux_quantum m) flux_quantum m"
proof -
  have "flux_quantized (topological_locking_flux flux_quantum m) flux_quantum m"
    by (rule topological_locking_flux_is_quantized)
  thus ?thesis
    unfolding vc_quantized_flux_def topological_locking_flux_def .
qed

theorem vc_quantized_circulation_is_winding_index:
  "tv_discrete_winding_index (vc_quantized_circulation m) m"
proof -
  have "vc_quantized_circulation m = 2 * pi * of_int m"
    unfolding vc_quantized_circulation_def
    by (rule refl)
  thus ?thesis
    unfolding tv_discrete_winding_index_def .
qed

theorem vc_corrected_winding_certificate_consumed:
  "gm_winding_quantization_locked
      phase6_corrected_error_max
      phase6_corrected_expected_circulation
      phase6_corrected_tolerance
   \<and> gm_winding_estimate_locked
      phase6_corrected_m_min
      phase6_corrected_m_max
      phase6_corrected_true_winding
      phase6_corrected_m_tolerance"
proof -
  have locked:
    "gm_winding_quantization_locked
      phase6_corrected_error_max
      phase6_corrected_expected_circulation
      phase6_corrected_tolerance
    \<and> gm_winding_estimate_locked
      phase6_corrected_m_min
      phase6_corrected_m_max
      phase6_corrected_true_winding
      phase6_corrected_m_tolerance
    \<and> phase6_corrected_loop_count = 4
    \<and> phase6_corrected_circulation_min \<le>
      phase6_corrected_expected_circulation
    \<and> phase6_corrected_expected_circulation \<le>
      phase6_corrected_circulation_max
    \<and> \<not> gm_circulation_quantized_candidate
      phase6_circulation_computed
      phase6_circulation_expected
      phase6_circulation_tolerance"
    by (rule phase6_corrected_winding_quantization_locked)
  thus ?thesis
    by blast
qed

section \<open>Integral Carrier Spine Contract\<close>

theorem vector_calculus_integral_carrier_contract:
  assumes "0 \<le> width"
    and "0 \<le> height"
    and "partial_y_Fy = - partial_x_Fx"
  shows "0 \<le> vc_rectangle_area width height
    \<and> vc_rect_boundary_circulation curl_strength width height =
        vc_rect_surface_flux curl_strength width height
    \<and> vc_incompressible_planar partial_x_Fx partial_y_Fy
    \<and> vc_uniform_helicity_density ax ay az 0 0 0 = 0
    \<and> vc_uniform_helicity_integral volume 0 = 0
    \<and> flux_quantized (vc_quantized_flux flux_quantum m) flux_quantum m
    \<and> tv_discrete_winding_index (vc_quantized_circulation m) m
    \<and> gm_winding_quantization_locked
      phase6_corrected_error_max
      phase6_corrected_expected_circulation
      phase6_corrected_tolerance"
proof (intro conjI)
  show "0 \<le> vc_rectangle_area width height"
    using assms(1,2)
    by (rule vc_rectangle_area_nonnegative)

  show "vc_rect_boundary_circulation curl_strength width height =
        vc_rect_surface_flux curl_strength width height"
    by (rule vc_green_rectangle_constant_curl)

  show "vc_incompressible_planar partial_x_Fx partial_y_Fy"
    using assms(3)
    by (rule vc_incompressible_from_opposite_partials)

  show "vc_uniform_helicity_density ax ay az 0 0 0 = 0"
    by (rule vc_helicity_density_zero_when_b_zero)

  show "vc_uniform_helicity_integral volume 0 = 0"
    by (rule vc_uniform_helicity_integral_zero_density)

  show "flux_quantized (vc_quantized_flux flux_quantum m) flux_quantum m"
    by (rule vc_quantized_flux_is_quantized)

  show "tv_discrete_winding_index (vc_quantized_circulation m) m"
    by (rule vc_quantized_circulation_is_winding_index)

  show "gm_winding_quantization_locked
      phase6_corrected_error_max
      phase6_corrected_expected_circulation
      phase6_corrected_tolerance"
    using vc_corrected_winding_certificate_consumed
    by blast
qed

text \<open>
  Paper-facing meaning: the spine now has a finite vector-calculus carrier
  for Green/Stokes-style circulation equals flux, helicity density and
  integral closure, incompressible divergence balance, and corrected winding
  quantization.  This is the bridge between the HDF5/Python certificates and
  the Isar-level spine contracts.
\<close>

end
