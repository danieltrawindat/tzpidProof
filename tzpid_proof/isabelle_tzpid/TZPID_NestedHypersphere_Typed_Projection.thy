theory TZPID_NestedHypersphere_Typed_Projection
  imports TZPID_NestedHypersphere_Computational_Checks
begin

text \<open>
  Project: TZPID Proof Pipeline
  Creator: Daniel Alexander Trawin
  ORCID: https://orcid.org/0009-0001-4630-3715
  Generated UTC: 2026-06-08T04:05:00Z

  Typed projection-map lift for the nested-hypersphere spine.
  The older focus theory records registry-backed abstract predicates.
  This companion theory gives the projection mechanism explicit HOL
  carriers and functions: a finite-coordinate bulk point, a three-coordinate
  boundary image, common-scale projection, preserved ratios, harmonic mode
  ratios, and a typed reciprocal fiber flip.
\<close>

type_synonym hs_bulk_point = "real list"
type_synonym hs_boundary_point = "real list"
type_synonym hs_projection_scale = real
type_synonym hs_radius = real
type_synonym hs_mode_number = real
type_synonym hs_frequency = real
type_synonym hs_phase = real

definition hs_norm_sq :: "real list \<Rightarrow> real" where
  "hs_norm_sq xs = sum_list (map (\<lambda>x. x * x) xs)"

definition hs_s3_carrier :: "hs_radius \<Rightarrow> hs_bulk_point \<Rightarrow> bool" where
  "hs_s3_carrier radius point =
     (radius > 0 \<and> length point = 4 \<and> hs_norm_sq point = radius\<^sup>2)"

definition hs_boundary_carrier :: "hs_boundary_point \<Rightarrow> bool" where
  "hs_boundary_carrier point = (length point = 3)"

definition hs_project_down :: "hs_projection_scale \<Rightarrow> hs_bulk_point \<Rightarrow> hs_boundary_point" where
  "hs_project_down scale point = map (\<lambda>x. scale * x) (take 3 point)"

definition hs_projection_admissible :: "hs_projection_scale \<Rightarrow> hs_radius \<Rightarrow> bool" where
  "hs_projection_admissible scale radius = (scale \<noteq> 0 \<and> radius > 0)"

definition hs_dimensionless_ratio :: "real \<Rightarrow> real \<Rightarrow> real" where
  "hs_dimensionless_ratio x y = x / y"

definition hs_projected_length :: "hs_projection_scale \<Rightarrow> real \<Rightarrow> real" where
  "hs_projected_length scale length_value = scale * length_value"

definition hs_harmonic_frequency :: "hs_mode_number \<Rightarrow> hs_frequency \<Rightarrow> hs_frequency" where
  "hs_harmonic_frequency n fundamental = n * fundamental"

definition hs_bulk_boundary_mode_preserved ::
  "hs_projection_scale \<Rightarrow> real \<Rightarrow> real \<Rightarrow> bool" where
  "hs_bulk_boundary_mode_preserved scale wavelength height =
     (hs_dimensionless_ratio
        (hs_projected_length scale wavelength)
        (hs_projected_length scale height)
      = hs_dimensionless_ratio wavelength height)"

definition hs_fiber_reciprocal_flip :: "real \<Rightarrow> real \<Rightarrow> bool" where
  "hs_fiber_reciprocal_flip boundary_ratio bulk_ratio =
     (boundary_ratio \<noteq> 0 \<and> bulk_ratio = 1 / boundary_ratio)"

definition hs_hopf_phase_lift :: "hs_phase \<Rightarrow> hs_phase \<Rightarrow> bool" where
  "hs_hopf_phase_lift boundary_holonomy fiber_rotation =
     (fiber_rotation = boundary_holonomy)"

theorem hs_project_down_has_boundary_dimension:
  assumes carrier: "hs_s3_carrier radius point"
  shows "hs_boundary_carrier (hs_project_down scale point)"
proof -
  have point_length: "length point = 4"
    using carrier
    unfolding hs_s3_carrier_def
    by blast
  have take_length: "length (take 3 point) = 3"
    using point_length
    by (metis length_take min_absorb2 numeral_le_iff semiring_norm(68))
  have "length (hs_project_down scale point) =
      length (map (\<lambda>x. scale * x) (take 3 point))"
    unfolding hs_project_down_def
    by (rule refl)
  also have "... = length (take 3 point)"
    by (rule length_map)
  also have "... = 3"
    using take_length .
  finally show ?thesis
    unfolding hs_boundary_carrier_def .
qed

theorem hs_projection_preserves_dimensionless_ratio:
  assumes scale_nonzero: "scale \<noteq> 0"
  shows "hs_dimensionless_ratio
      (hs_projected_length scale x)
      (hs_projected_length scale y)
    = hs_dimensionless_ratio x y"
proof -
  have "hs_dimensionless_ratio
      (hs_projected_length scale x)
      (hs_projected_length scale y)
    = (scale * x) / (scale * y)"
    unfolding hs_dimensionless_ratio_def hs_projected_length_def
    by (rule refl)
  also have "... = x / y"
    using scale_nonzero
    by field
  finally show ?thesis
    unfolding hs_dimensionless_ratio_def .
qed

theorem hs_bulk_boundary_mode_ratio_preserved:
  assumes scale_nonzero: "scale \<noteq> 0"
  shows "hs_bulk_boundary_mode_preserved scale wavelength height"
proof -
  have "hs_dimensionless_ratio
        (hs_projected_length scale wavelength)
        (hs_projected_length scale height)
      = hs_dimensionless_ratio wavelength height"
    using scale_nonzero
    by (rule hs_projection_preserves_dimensionless_ratio)
  thus ?thesis
    unfolding hs_bulk_boundary_mode_preserved_def .
qed

theorem hs_harmonic_ladder_ratio_preserved:
  assumes fundamental_nonzero: "fundamental \<noteq> 0"
  shows "hs_harmonic_frequency n fundamental / fundamental = n"
proof -
  have "hs_harmonic_frequency n fundamental / fundamental =
      (n * fundamental) / fundamental"
    unfolding hs_harmonic_frequency_def
    by (rule refl)
  also have "... = n"
    using fundamental_nonzero
    by field
  finally show ?thesis .
qed

theorem hs_reciprocal_flip_closes:
  assumes flip: "hs_fiber_reciprocal_flip boundary_ratio bulk_ratio"
  shows "boundary_ratio * bulk_ratio = 1"
proof -
  have boundary_nonzero: "boundary_ratio \<noteq> 0"
    using flip
    unfolding hs_fiber_reciprocal_flip_def
    by blast
  have bulk_eq: "bulk_ratio = 1 / boundary_ratio"
    using flip
    unfolding hs_fiber_reciprocal_flip_def
    by blast
  have "boundary_ratio * bulk_ratio =
      boundary_ratio * (1 / boundary_ratio)"
    using bulk_eq
    by (rule arg_cong[where f="(\<lambda>x. boundary_ratio * x)"])
  also have "... = 1"
    using boundary_nonzero
    by field
  finally show ?thesis .
qed

theorem hs_hopf_phase_lift_preserves_holonomy:
  assumes lift: "hs_hopf_phase_lift boundary_holonomy fiber_rotation"
  shows "fiber_rotation - boundary_holonomy = 0"
proof -
  have "fiber_rotation = boundary_holonomy"
    using lift
    unfolding hs_hopf_phase_lift_def .
  hence "fiber_rotation - boundary_holonomy =
      boundary_holonomy - boundary_holonomy"
    by (rule arg_cong[where f="(\<lambda>x. x - boundary_holonomy)"])
  also have "... = 0"
    by algebra
  finally show ?thesis .
qed

theorem hs_typed_projection_contract:
  assumes carrier: "hs_s3_carrier radius point"
    and admissible: "hs_projection_admissible scale radius"
    and fundamental_nonzero: "fundamental \<noteq> 0"
    and flip: "hs_fiber_reciprocal_flip boundary_ratio bulk_ratio"
    and lift: "hs_hopf_phase_lift boundary_holonomy fiber_rotation"
  shows
    "hs_boundary_carrier (hs_project_down scale point)
     \<and> hs_bulk_boundary_mode_preserved scale wavelength height
     \<and> hs_harmonic_frequency n fundamental / fundamental = n
     \<and> boundary_ratio * bulk_ratio = 1
     \<and> fiber_rotation - boundary_holonomy = 0"
proof (intro conjI)
  show "hs_boundary_carrier (hs_project_down scale point)"
    using carrier
    by (rule hs_project_down_has_boundary_dimension)
  have scale_nonzero: "scale \<noteq> 0"
    using admissible
    unfolding hs_projection_admissible_def
    by blast
  show "hs_bulk_boundary_mode_preserved scale wavelength height"
    using scale_nonzero
    by (rule hs_bulk_boundary_mode_ratio_preserved)
  show "hs_harmonic_frequency n fundamental / fundamental = n"
    using fundamental_nonzero
    by (rule hs_harmonic_ladder_ratio_preserved)
  show "boundary_ratio * bulk_ratio = 1"
    using flip
    by (rule hs_reciprocal_flip_closes)
  show "fiber_rotation - boundary_holonomy = 0"
    using lift
    by (rule hs_hopf_phase_lift_preserves_holonomy)
qed

context TZPID_NestedHypersphere_Focus
begin

theorem nested_hypersphere_typed_projection_extends_spine:
  assumes carrier: "hs_s3_carrier radius point"
    and admissible: "hs_projection_admissible scale radius"
    and fundamental_nonzero: "fundamental \<noteq> 0"
    and flip: "hs_fiber_reciprocal_flip boundary_ratio bulk_ratio"
    and lift: "hs_hopf_phase_lift boundary_holonomy fiber_rotation"
  shows
    "nested_hypersphere_unifying_chain
     \<and> hs_boundary_carrier (hs_project_down scale point)
     \<and> hs_bulk_boundary_mode_preserved scale wavelength height
     \<and> boundary_ratio * bulk_ratio = 1
     \<and> fiber_rotation - boundary_holonomy = 0"
proof (intro conjI)
  show "nested_hypersphere_unifying_chain"
    using unifying_chain .
  show "hs_boundary_carrier (hs_project_down scale point)"
    using carrier
    by (rule hs_project_down_has_boundary_dimension)
  have scale_nonzero: "scale \<noteq> 0"
    using admissible
    unfolding hs_projection_admissible_def
    by blast
  show "hs_bulk_boundary_mode_preserved scale wavelength height"
    using scale_nonzero
    by (rule hs_bulk_boundary_mode_ratio_preserved)
  show "boundary_ratio * bulk_ratio = 1"
    using flip
    by (rule hs_reciprocal_flip_closes)
  show "fiber_rotation - boundary_holonomy = 0"
    using lift
    by (rule hs_hopf_phase_lift_preserves_holonomy)
qed

end

end
