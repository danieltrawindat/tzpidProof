theory TZPID_GeometryManifold_Carriers
  imports TZPID_Theorem_Semantic_Batch008_Geometry_Manifold
begin

text \<open>
  Project: TZPID Proof Pipeline
  Creator: Daniel Alexander Trawin
  ORCID: https://orcid.org/0009-0001-4630-3715
  Generated UTC: 2026-06-09

  Phase 2 geometry/manifold upgrade.

  This theory strengthens batch 008 with finite metric, chart,
  projection, curvature, holonomy, and action carriers.  It deliberately
  avoids claiming full smooth-manifold coverage; instead, it provides
  checked algebraic contracts that can be attached to the hyperspherical,
  topology/vector, and gyromagnetic spines while a deeper differential
  geometry layer is developed.
\<close>

section \<open>Finite Metric and Projection Carriers\<close>

definition gm_dist2_2 ::
  "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real" where
  "gm_dist2_2 x y u v = (x - u)\<^sup>2 + (y - v)\<^sup>2"

definition gm_norm2_2 :: "real \<Rightarrow> real \<Rightarrow> real" where
  "gm_norm2_2 x y = x\<^sup>2 + y\<^sup>2"

definition gm_norm2_3 :: "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real" where
  "gm_norm2_3 x y z = x\<^sup>2 + y\<^sup>2 + z\<^sup>2"

definition gm_project_xy_norm2 :: "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real" where
  "gm_project_xy_norm2 x y z = gm_norm2_2 x y"

definition gm_projection_residual_z :: "real \<Rightarrow> real" where
  "gm_projection_residual_z z = z"

definition gm_chart_inverse_residual :: "real \<Rightarrow> real \<Rightarrow> real" where
  "gm_chart_inverse_residual coordinate recovered = recovered - coordinate"

definition gm_local_chart_regular :: "real \<Rightarrow> bool" where
  "gm_local_chart_regular jacobian = (jacobian \<noteq> 0)"

section \<open>Curvature, Holonomy, and Action Carriers\<close>

definition gm_sphere_curvature :: "real \<Rightarrow> real" where
  "gm_sphere_curvature radius = 1 / radius\<^sup>2"

definition gm_curvature_field_match :: "real \<Rightarrow> real \<Rightarrow> bool" where
  "gm_curvature_field_match curvature field_strength = (curvature = field_strength)"

definition gm_phase_loop_closed :: "real \<Rightarrow> real \<Rightarrow> int \<Rightarrow> bool" where
  "gm_phase_loop_closed start finish winding =
     (finish - start = 2 * pi * of_int winding)"

definition gm_action_quadratic :: "real \<Rightarrow> real \<Rightarrow> real" where
  "gm_action_quadratic duration velocity = duration * velocity\<^sup>2 / 2"

definition gm_least_action_margin :: "real \<Rightarrow> real \<Rightarrow> real" where
  "gm_least_action_margin competitor action = competitor - action"

section \<open>Metric and Projection Laws\<close>

theorem gm_dist2_self_zero:
  "gm_dist2_2 x y x y = 0"
proof -
  show ?thesis
    unfolding gm_dist2_2_def
    by algebra
qed

theorem gm_dist2_symmetric:
  "gm_dist2_2 x y u v = gm_dist2_2 u v x y"
proof -
  show ?thesis
    unfolding gm_dist2_2_def
    by algebra
qed

theorem gm_projected_norm_not_above_lifted_norm:
  "gm_project_xy_norm2 x y z \<le> gm_norm2_3 x y z"
proof -
  have square_nonnegative: "z\<^sup>2 \<ge> 0"
    by (rule zero_le_power2)
  show ?thesis
    unfolding gm_project_xy_norm2_def gm_norm2_2_def gm_norm2_3_def
    using square_nonnegative
    by algebra
qed

theorem gm_zero_fiber_projection_preserves_norm:
  "gm_project_xy_norm2 x y 0 = gm_norm2_3 x y 0"
proof -
  show ?thesis
    unfolding gm_project_xy_norm2_def gm_norm2_2_def gm_norm2_3_def
    by algebra
qed

theorem gm_zero_projection_residual_matches_nullspace:
  "gm_projection_residual_z 0 = nullspace_projection_residual 0"
proof -
  show ?thesis
    unfolding gm_projection_residual_z_def nullspace_projection_residual_def
    by (rule refl)
qed

theorem gm_chart_inverse_equal_zero_residual:
  "gm_chart_inverse_residual coordinate coordinate = 0"
proof -
  show ?thesis
    unfolding gm_chart_inverse_residual_def
    by algebra
qed

theorem gm_regular_chart_from_nonzero_jacobian:
  assumes "jacobian \<noteq> 0"
  shows "gm_local_chart_regular jacobian"
proof -
  show ?thesis
    using assms
    unfolding gm_local_chart_regular_def .
qed

section \<open>Curvature, Holonomy, and Action Laws\<close>

theorem gm_sphere_curvature_recovers_radius_square:
  assumes "radius \<noteq> 0"
  shows "gm_sphere_curvature radius * radius\<^sup>2 = 1"
proof -
  have radius_square_nonzero: "radius\<^sup>2 \<noteq> 0"
    using assms
    by algebra
  have "gm_sphere_curvature radius * radius\<^sup>2 =
        (1 / radius\<^sup>2) * radius\<^sup>2"
    unfolding gm_sphere_curvature_def
    by (rule refl)
  also have "... = 1"
    using radius_square_nonzero
    by (field)
  finally show ?thesis .
qed

theorem gm_curvature_field_match_zero_residual:
  assumes "gm_curvature_field_match curvature field_strength"
  shows "manifold_curvature_residual curvature field_strength = 0"
proof -
  have "curvature = field_strength"
    using assms
    unfolding gm_curvature_field_match_def .
  thus ?thesis
    unfolding manifold_curvature_residual_def
    by algebra
qed

theorem gm_phase_loop_zero_winding_matches_closed_holonomy:
  assumes "gm_phase_loop_closed phase phase 0"
  shows "holonomy_loop_residual phase phase = 0"
proof -
  show ?thesis
    using closed_holonomy_loop_zero_residual .
qed

theorem gm_phase_loop_adds_one_turn:
  assumes "gm_phase_loop_closed start finish winding"
  shows "gm_phase_loop_closed start (finish + 2 * pi) (winding + 1)"
proof -
  have loop: "finish - start = 2 * pi * of_int winding"
    using assms
    unfolding gm_phase_loop_closed_def .
  have "finish + 2 * pi - start = 2 * pi * of_int (winding + 1)"
    using loop
    by algebra
  thus ?thesis
    unfolding gm_phase_loop_closed_def .
qed

theorem gm_quadratic_action_nonnegative:
  assumes "duration \<ge> 0"
  shows "gm_action_quadratic duration velocity \<ge> 0"
proof -
  have square_nonnegative: "velocity\<^sup>2 \<ge> 0"
    by (rule zero_le_power2)
  have product_nonnegative: "duration * velocity\<^sup>2 \<ge> 0"
    using assms square_nonnegative
    by (rule mult_nonneg_nonneg)
  have "duration * velocity\<^sup>2 / 2 \<ge> 0"
    using product_nonnegative
    by linarith
  thus ?thesis
    unfolding gm_action_quadratic_def .
qed

theorem gm_least_action_from_nonnegative_margin:
  assumes "gm_least_action_margin competitor action \<ge> 0"
  shows "least_action_guard action competitor"
proof -
  have "competitor - action \<ge> 0"
    using assms
    unfolding gm_least_action_margin_def .
  hence "action \<le> competitor"
    by linarith
  thus ?thesis
    unfolding least_action_guard_def .
qed

section \<open>Batch 008 Upgrade Contract\<close>

theorem geometry_manifold_carrier_contract:
  assumes jacobian_nonzero: "jacobian \<noteq> 0"
    and radius_nonzero: "radius \<noteq> 0"
    and curvature_match: "gm_curvature_field_match curvature field_strength"
    and loop: "gm_phase_loop_closed start finish winding"
    and duration_nonnegative: "duration \<ge> 0"
    and margin_nonnegative: "gm_least_action_margin competitor action \<ge> 0"
  shows
    "gm_dist2_2 x y x y = 0
     \<and> gm_dist2_2 x y u v = gm_dist2_2 u v x y
     \<and> gm_project_xy_norm2 x y z \<le> gm_norm2_3 x y z
     \<and> gm_project_xy_norm2 x y 0 = gm_norm2_3 x y 0
     \<and> gm_projection_residual_z 0 = nullspace_projection_residual 0
     \<and> gm_chart_inverse_residual coordinate coordinate = 0
     \<and> gm_local_chart_regular jacobian
     \<and> gm_sphere_curvature radius * radius\<^sup>2 = 1
     \<and> manifold_curvature_residual curvature field_strength = 0
     \<and> gm_phase_loop_closed start (finish + 2 * pi) (winding + 1)
     \<and> gm_action_quadratic duration velocity \<ge> 0
     \<and> least_action_guard action competitor"
proof (intro conjI)
  show "gm_dist2_2 x y x y = 0"
    using gm_dist2_self_zero .
  show "gm_dist2_2 x y u v = gm_dist2_2 u v x y"
    using gm_dist2_symmetric .
  show "gm_project_xy_norm2 x y z \<le> gm_norm2_3 x y z"
    using gm_projected_norm_not_above_lifted_norm .
  show "gm_project_xy_norm2 x y 0 = gm_norm2_3 x y 0"
    using gm_zero_fiber_projection_preserves_norm .
  show "gm_projection_residual_z 0 = nullspace_projection_residual 0"
    using gm_zero_projection_residual_matches_nullspace .
  show "gm_chart_inverse_residual coordinate coordinate = 0"
    using gm_chart_inverse_equal_zero_residual .
  show "gm_local_chart_regular jacobian"
    using jacobian_nonzero
    by (rule gm_regular_chart_from_nonzero_jacobian)
  show "gm_sphere_curvature radius * radius\<^sup>2 = 1"
    using radius_nonzero
    by (rule gm_sphere_curvature_recovers_radius_square)
  show "manifold_curvature_residual curvature field_strength = 0"
    using curvature_match
    by (rule gm_curvature_field_match_zero_residual)
  show "gm_phase_loop_closed start (finish + 2 * pi) (winding + 1)"
    using loop
    by (rule gm_phase_loop_adds_one_turn)
  show "gm_action_quadratic duration velocity \<ge> 0"
    using duration_nonnegative
    by (rule gm_quadratic_action_nonnegative)
  show "least_action_guard action competitor"
    using margin_nonnegative
    by (rule gm_least_action_from_nonnegative_margin)
qed

end
