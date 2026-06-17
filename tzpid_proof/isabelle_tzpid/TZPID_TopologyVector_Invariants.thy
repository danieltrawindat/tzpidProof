theory TZPID_TopologyVector_Invariants
  imports TZPID_Theorem_Semantic_Batch005_Topology_Vector
begin

text \<open>
  Project: TZPID Proof Pipeline
  Creator: Daniel Alexander Trawin
  ORCID: https://orcid.org/0009-0001-4630-3715
  Generated UTC: 2026-06-09

  Phase 2 topology/vector upgrade.

  This theory strengthens batch 005 with concrete real-valued invariant
  carriers for helicity density, oriented circulation area, flux
  quantization, Gauss-Bonnet boundary closure, and topological gap
  protection.  These carriers are intentionally finite-dimensional:
  they give the paper-facing spine a checked HOL contract now, while
  leaving full manifold/vector-analysis imports as a later refinement.
\<close>

section \<open>Finite Vector Carriers\<close>

definition tv_dot3 ::
  "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real" where
  "tv_dot3 ax ay az bx by bz = ax * bx + ay * by + az * bz"

definition tv_cross_z ::
  "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real" where
  "tv_cross_z ax ay bx by = ax * by - ay * bx"

definition tv_oriented_area2 ::
  "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real" where
  "tv_oriented_area2 ax ay bx by = tv_cross_z ax ay bx by"

definition tv_helicity_density3 ::
  "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real" where
  "tv_helicity_density3 ax ay az bx by bz = tv_dot3 ax ay az bx by bz"

definition tv_uniform_helicity :: "real \<Rightarrow> real \<Rightarrow> real" where
  "tv_uniform_helicity volume density = volume * density"

definition tv_flux_multiple :: "real \<Rightarrow> int \<Rightarrow> real" where
  "tv_flux_multiple flux_quantum n = of_int n * flux_quantum"

definition tv_boundary_curvature_balance ::
  "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> bool" where
  "tv_boundary_curvature_balance surface_curvature boundary_curvature chi =
     (surface_curvature + boundary_curvature = 2 * pi * chi)"

definition tv_topological_gap_protected :: "real \<Rightarrow> real \<Rightarrow> bool" where
  "tv_topological_gap_protected gap perturbation =
     (0 < gap \<and> perturbation < gap)"

definition tv_discrete_winding_index :: "real \<Rightarrow> int \<Rightarrow> bool" where
  "tv_discrete_winding_index total_phase n =
     (total_phase = 2 * pi * of_int n)"

section \<open>Invariant Laws\<close>

theorem tv_dot3_zero_right:
  "tv_dot3 ax ay az 0 0 0 = 0"
proof -
  show ?thesis
    unfolding tv_dot3_def
    by algebra
qed

theorem tv_helicity_density_zero_magnetic_field:
  "tv_helicity_density3 ax ay az 0 0 0 = 0"
proof -
  have "tv_dot3 ax ay az 0 0 0 = 0"
    by (rule tv_dot3_zero_right)
  thus ?thesis
    unfolding tv_helicity_density3_def .
qed

theorem tv_uniform_helicity_zero_density:
  "tv_uniform_helicity volume 0 = 0"
proof -
  show ?thesis
    unfolding tv_uniform_helicity_def
    by algebra
qed

theorem tv_cross_z_antisymmetric:
  "tv_cross_z ax ay bx by = - tv_cross_z bx by ax ay"
proof -
  show ?thesis
    unfolding tv_cross_z_def
    by algebra
qed

theorem tv_oriented_area2_swaps_sign:
  "tv_oriented_area2 ax ay bx by = - tv_oriented_area2 bx by ax ay"
proof -
  have "tv_cross_z ax ay bx by = - tv_cross_z bx by ax ay"
    by (rule tv_cross_z_antisymmetric)
  thus ?thesis
    unfolding tv_oriented_area2_def .
qed

theorem tv_flux_multiple_is_quantized:
  "flux_quantized (tv_flux_multiple flux_quantum n) flux_quantum n"
proof -
  have "tv_flux_multiple flux_quantum n = of_int n * flux_quantum"
    unfolding tv_flux_multiple_def
    by (rule refl)
  thus ?thesis
    unfolding flux_quantized_def .
qed

theorem tv_flux_multiple_recovers_registered_form:
  "tv_flux_multiple flux_quantum n = macroscopic_flux_multiple (of_int n) flux_quantum"
proof -
  show ?thesis
    unfolding tv_flux_multiple_def macroscopic_flux_multiple_def
    by (rule refl)
qed

theorem tv_boundary_balance_closes_gauss_bonnet:
  assumes "tv_boundary_curvature_balance surface_curvature boundary_curvature chi"
  shows "gauss_bonnet_boundary_total surface_curvature boundary_curvature chi = 0"
proof -
  have balance:
    "surface_curvature + boundary_curvature = 2 * pi * chi"
    using assms
    unfolding tv_boundary_curvature_balance_def .
  show ?thesis
    using balance
    by (rule id9990_gauss_bonnet_constraint_guard)
qed

theorem tv_gap_protection_implies_batch005_guard:
  assumes "tv_topological_gap_protected gap perturbation"
  shows "topological_protection_guard gap perturbation"
proof -
  have "perturbation < gap"
    using assms
    unfolding tv_topological_gap_protected_def
    by blast
  thus ?thesis
    by (rule id1802_topological_protection_from_gap)
qed

theorem tv_gap_protection_implies_quantum_state_guard:
  assumes "tv_topological_gap_protected gap perturbation"
  shows "topological_quantum_state_guard gap"
proof -
  have "gap > 0"
    using assms
    unfolding tv_topological_gap_protected_def
    by linarith
  thus ?thesis
    by (rule id0065_positive_gap_topological_quantum_state_guard)
qed

theorem tv_winding_index_adds_full_turn:
  assumes "tv_discrete_winding_index phase n"
  shows "tv_discrete_winding_index (phase + 2 * pi) (n + 1)"
proof -
  have phase_eq: "phase = 2 * pi * of_int n"
    using assms
    unfolding tv_discrete_winding_index_def .
  have "phase + 2 * pi = 2 * pi * of_int (n + 1)"
    using phase_eq
    by algebra
  thus ?thesis
    unfolding tv_discrete_winding_index_def .
qed

section \<open>Batch 005 Upgrade Contract\<close>

theorem topology_vector_invariant_contract:
  assumes "tv_boundary_curvature_balance surface_curvature boundary_curvature chi"
    and "tv_topological_gap_protected gap perturbation"
    and "tv_discrete_winding_index phase n"
  shows
    "tv_helicity_density3 ax ay az 0 0 0 = 0
     \<and> tv_uniform_helicity volume 0 = 0
     \<and> tv_oriented_area2 ax ay bx by = - tv_oriented_area2 bx by ax ay
     \<and> flux_quantized (tv_flux_multiple flux_quantum n) flux_quantum n
     \<and> tv_flux_multiple flux_quantum n = macroscopic_flux_multiple (of_int n) flux_quantum
     \<and> gauss_bonnet_boundary_total surface_curvature boundary_curvature chi = 0
     \<and> topological_protection_guard gap perturbation
     \<and> topological_quantum_state_guard gap
     \<and> tv_discrete_winding_index (phase + 2 * pi) (n + 1)"
proof (intro conjI)
  show "tv_helicity_density3 ax ay az 0 0 0 = 0"
    using tv_helicity_density_zero_magnetic_field .
  show "tv_uniform_helicity volume 0 = 0"
    using tv_uniform_helicity_zero_density .
  show "tv_oriented_area2 ax ay bx by = - tv_oriented_area2 bx by ax ay"
    using tv_oriented_area2_swaps_sign .
  show "flux_quantized (tv_flux_multiple flux_quantum n) flux_quantum n"
    using tv_flux_multiple_is_quantized .
  show "tv_flux_multiple flux_quantum n = macroscopic_flux_multiple (of_int n) flux_quantum"
    using tv_flux_multiple_recovers_registered_form .
  show "gauss_bonnet_boundary_total surface_curvature boundary_curvature chi = 0"
    using assms(1)
    by (rule tv_boundary_balance_closes_gauss_bonnet)
  show "topological_protection_guard gap perturbation"
    using assms(2)
    by (rule tv_gap_protection_implies_batch005_guard)
  show "topological_quantum_state_guard gap"
    using assms(2)
    by (rule tv_gap_protection_implies_quantum_state_guard)
  show "tv_discrete_winding_index (phase + 2 * pi) (n + 1)"
    using assms(3)
    by (rule tv_winding_index_adds_full_turn)
qed

end
