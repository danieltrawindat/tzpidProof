theory TZPID_GeometryCurvature_Carriers
  imports TZPID_Theorem_Semantic_Batch019_Geometry_Curvature_Closeout
begin

text \<open>
  Project: TZPID Proof Pipeline
  Creator: Daniel Alexander Trawin
  ORCID: https://orcid.org/0009-0001-4630-3715
  Generated UTC: 2026-06-09

  Phase 2 geometry/curvature closeout batch 019 upgrade.

  This carrier layer closes the final triage row with explicit curvature
  coupling contracts: response equality, residual zeroing, nonnegative
  response under nonnegative inputs, and manifold-curvature residual closure.
\<close>

definition gc_response_residual :: "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real" where
  "gc_response_residual observed coupling curvature =
     curvature_coupling_residual observed coupling curvature"

definition gc_coupling_margin :: "real \<Rightarrow> real" where
  "gc_coupling_margin coupling = coupling"

definition gc_curvature_margin :: "real \<Rightarrow> real" where
  "gc_curvature_margin curvature = curvature"

definition gc_response_nonnegative_guard :: "real \<Rightarrow> real \<Rightarrow> bool" where
  "gc_response_nonnegative_guard coupling curvature \<longleftrightarrow>
     0 \<le> curvature_coupling_response coupling curvature"

definition gc_manifold_closeout_residual :: "real \<Rightarrow> real \<Rightarrow> real" where
  "gc_manifold_closeout_residual observed_curvature reference_curvature =
     manifold_curvature_residual observed_curvature reference_curvature"

theorem gc_response_residual_zero:
  assumes "observed = coupling * curvature"
  shows "gc_response_residual observed coupling curvature = 0"
proof -
  have "curvature_coupling_residual observed coupling curvature = 0"
    using assms
    by (rule id9999_curvature_coupling_residual_zero)
  thus ?thesis
    unfolding gc_response_residual_def .
qed

theorem gc_response_nonnegative_from_nonnegative_inputs:
  assumes "0 \<le> coupling"
    and "0 \<le> curvature"
  shows "gc_response_nonnegative_guard coupling curvature"
proof -
  have "0 \<le> coupling * curvature"
    using assms
    by (positivity)
  thus ?thesis
    unfolding gc_response_nonnegative_guard_def curvature_coupling_response_def .
qed

theorem gc_coupling_margin_nonnegative:
  assumes "0 \<le> coupling"
  shows "0 \<le> gc_coupling_margin coupling"
proof -
  show ?thesis
    unfolding gc_coupling_margin_def
    using assms .
qed

theorem gc_curvature_margin_nonnegative:
  assumes "0 \<le> curvature"
  shows "0 \<le> gc_curvature_margin curvature"
proof -
  show ?thesis
    unfolding gc_curvature_margin_def
    using assms .
qed

theorem gc_manifold_closeout_residual_zero:
  "gc_manifold_closeout_residual curvature curvature = 0"
proof -
  have "manifold_curvature_residual curvature curvature = 0"
    using equal_curvature_zero_residual .
  thus ?thesis
    unfolding gc_manifold_closeout_residual_def .
qed

theorem geometry_curvature_carrier_contract:
  assumes observed: "observed = coupling * curvature"
    and coupling_nonnegative: "0 \<le> coupling"
    and curvature_nonnegative: "0 \<le> curvature"
  shows
    "curvature_coupling_guard coupling curvature
     \<and> gc_response_residual observed coupling curvature = 0
     \<and> gc_response_nonnegative_guard coupling curvature
     \<and> 0 \<le> gc_coupling_margin coupling
     \<and> 0 \<le> gc_curvature_margin curvature
     \<and> gc_manifold_closeout_residual curvature curvature = 0"
proof (intro conjI)
  show "curvature_coupling_guard coupling curvature"
    using id9999_curvature_coupling_response_unfolds .
  show "gc_response_residual observed coupling curvature = 0"
    using observed
    by (rule gc_response_residual_zero)
  show "gc_response_nonnegative_guard coupling curvature"
    using coupling_nonnegative curvature_nonnegative
    by (rule gc_response_nonnegative_from_nonnegative_inputs)
  show "0 \<le> gc_coupling_margin coupling"
    using coupling_nonnegative
    by (rule gc_coupling_margin_nonnegative)
  show "0 \<le> gc_curvature_margin curvature"
    using curvature_nonnegative
    by (rule gc_curvature_margin_nonnegative)
  show "gc_manifold_closeout_residual curvature curvature = 0"
    using gc_manifold_closeout_residual_zero .
qed

end
