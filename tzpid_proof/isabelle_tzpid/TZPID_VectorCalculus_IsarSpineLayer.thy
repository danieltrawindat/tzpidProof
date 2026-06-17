theory TZPID_VectorCalculus_IsarSpineLayer
  imports TZPID_TopologicalUnification_SpineMerges
begin

text \<open>
  Project: TZPID Proof Pipeline
  Creator: Daniel Alexander Trawin
  ORCID: https://orcid.org/0009-0001-4630-3715
  Generated UTC: 2026-06-11T00:00:00Z

  Isar-facing vector-calculus layer for the spine stack.

  This file does not mint new physics claims.  It makes the existing checked
  vector-calculus contracts readable as one paper-facing bridge:

    * Delta-alpha gradient: exact mixed partials give zero planar curl.
    * Gyromagnetic movement: active phase gradient plus asymmetric coupling
      gives a nonzero angular-momentum witness.
    * Magnetic/torsion MHD: helicity carriers, ideal-MHD dissipation, Elsasser
      balance, and torsion cancellation are consumed by the spine.
    * Topology/vector: flux quantization, oriented-area sign reversal,
      Gauss-Bonnet boundary closure, topological gap protection, and winding
      update are consumed by the spine.

  The purpose is proof readability: the earlier files provide the algebraic
  carriers; this layer gives an Isar derivation that reviewers can follow.
\<close>

section \<open>Spine Labels\<close>

datatype vector_calculus_spine =
    VC_DeltaAlpha_Gradient
  | VC_Gyromagnetic_Lz
  | VC_Magnetic_Helicity
  | VC_Elsasser_MHD
  | VC_Torsion_Cancellation
  | VC_Flux_Quantization
  | VC_Topological_Boundary
  | VC_Winding_Update

definition vector_calculus_spine_backbone :: "vector_calculus_spine list" where
  "vector_calculus_spine_backbone =
    [ VC_DeltaAlpha_Gradient
    , VC_Gyromagnetic_Lz
    , VC_Magnetic_Helicity
    , VC_Elsasser_MHD
    , VC_Torsion_Cancellation
    , VC_Flux_Quantization
    , VC_Topological_Boundary
    , VC_Winding_Update
    ]"

fun vector_calculus_spine_name :: "vector_calculus_spine \<Rightarrow> string" where
  "vector_calculus_spine_name VC_DeltaAlpha_Gradient = ''delta_alpha_gradient_curl''" |
  "vector_calculus_spine_name VC_Gyromagnetic_Lz = ''gyromagnetic_lz_witness''" |
  "vector_calculus_spine_name VC_Magnetic_Helicity = ''magnetic_helicity_carrier''" |
  "vector_calculus_spine_name VC_Elsasser_MHD = ''elsasser_mhd_balance''" |
  "vector_calculus_spine_name VC_Torsion_Cancellation = ''torsion_cancellation''" |
  "vector_calculus_spine_name VC_Flux_Quantization = ''flux_quantization''" |
  "vector_calculus_spine_name VC_Topological_Boundary = ''topological_boundary_closure''" |
  "vector_calculus_spine_name VC_Winding_Update = ''winding_update''"

theorem vector_calculus_spine_backbone_count:
  "length vector_calculus_spine_backbone = 8"
proof -
  show ?thesis
    unfolding vector_calculus_spine_backbone_def
    by eval
qed

theorem vector_calculus_spine_names_nonempty:
  assumes "s \<in> set vector_calculus_spine_backbone"
  shows "vector_calculus_spine_name s \<noteq> ''''"
proof -
  from assms show ?thesis
    unfolding vector_calculus_spine_backbone_def
    by (cases s; simp)
qed

section \<open>Readable Vector-Calculus Bridge\<close>

theorem isar_delta_alpha_gradient_curl_layer:
  assumes mixed_partials: "partial_x_grad_y = partial_y_grad_x"
  shows "gm_curl_z partial_x_grad_y partial_y_grad_x = 0"
proof -
  have cancellation:
    "gm_curl_z partial_x_grad_y partial_y_grad_x =
     partial_x_grad_y - partial_y_grad_x"
    unfolding gm_curl_z_def
    by (rule refl)

  have "partial_x_grad_y - partial_y_grad_x = 0"
    using mixed_partials
    by algebra

  with cancellation show ?thesis
    by algebra
qed

theorem isar_gyromagnetic_lz_layer:
  assumes active: "gm_phase_vector_active gx gy"
    and coupling_nonzero: "coupling \<noteq> 0"
    and offset_nonzero: "source_offset \<noteq> 0"
    and phase_gradient_def: "phase_gradient = sqrt (gm_grad_mag_sq gx gy)"
    and phase_gradient_nonzero: "phase_gradient \<noteq> 0"
  shows "(gx \<noteq> 0 \<or> gy \<noteq> 0) \<and>
         gm_Lz_witness phase_gradient source_offset coupling \<noteq> 0"
proof -
  have active_component: "gx \<noteq> 0 \<or> gy \<noteq> 0"
    using active
    by (rule active_phase_vector_has_nonzero_component)

  have lz_witness:
    "gm_Lz_witness phase_gradient source_offset coupling \<noteq> 0"
    using phase_gradient_nonzero offset_nonzero coupling_nonzero
    by (rule nonzero_phase_source_generates_nonzero_Lz_witness)

  from active_component lz_witness show ?thesis
    by blast
qed

theorem isar_magnetic_torsion_vector_layer:
  assumes ideal: "eta = 0"
    and elsasser: "mt_elsasser_balance magnetic_force coriolis_force"
  shows "mt_vector_helicity_density ax ay az 0 0 0 = 0
    \<and> mt_uniform_helicity_integral volume 0 = 0
    \<and> mt_ideal_mhd_helicity_conserved eta 0
    \<and> gm_resistive_helicity_dissipation eta current_norm_sq = 0
    \<and> elsasser_number magnetic_force coriolis_force = 1
    \<and> mt_torsion_density curvature (- curvature) = 0"
proof -
  have helicity_density_zero:
    "mt_vector_helicity_density ax ay az 0 0 0 = 0"
    by (rule mt_vector_helicity_density_zero_when_b_zero)

  have uniform_helicity_zero:
    "mt_uniform_helicity_integral volume 0 = 0"
    by (rule mt_uniform_helicity_integral_zero_density)

  have ideal_conservation:
    "mt_ideal_mhd_helicity_conserved eta 0"
    using ideal
    by (rule mt_ideal_mhd_conservation_from_zero_eta)

  have dissipation_zero:
    "gm_resistive_helicity_dissipation eta current_norm_sq = 0"
    using ideal_conservation
    by (rule mt_ideal_mhd_zero_resistive_dissipation)

  have elsasser_unit:
    "elsasser_number magnetic_force coriolis_force = 1"
    using elsasser
    by (rule mt_elsasser_balance_unit_number)

  have torsion_zero:
    "mt_torsion_density curvature (- curvature) = 0"
    by (rule mt_torsion_density_zero_for_opposite_twist)

  from helicity_density_zero uniform_helicity_zero ideal_conservation
    dissipation_zero elsasser_unit torsion_zero
  show ?thesis
    by blast
qed

theorem isar_topology_vector_layer:
  assumes boundary: "tv_boundary_curvature_balance surface_curvature boundary_curvature chi"
    and gap: "tv_topological_gap_protected gap perturbation"
    and winding: "tv_discrete_winding_index phase n"
  shows "flux_quantized (topological_locking_flux flux_quantum n) flux_quantum n
    \<and> topological_locking_flux flux_quantum n =
        macroscopic_flux_multiple (of_int n) flux_quantum
    \<and> tv_oriented_area2 ax ay bx by = - tv_oriented_area2 bx by ax ay
    \<and> gauss_bonnet_boundary_total surface_curvature boundary_curvature chi = 0
    \<and> topological_protection_guard gap perturbation
    \<and> topological_quantum_state_guard gap
    \<and> tv_discrete_winding_index (phase + 2 * pi) (n + 1)"
proof -
  have flux_quantized:
    "flux_quantized (topological_locking_flux flux_quantum n) flux_quantum n"
    by (rule topological_locking_flux_is_quantized)

  have flux_form:
    "topological_locking_flux flux_quantum n =
     macroscopic_flux_multiple (of_int n) flux_quantum"
    by (rule topological_locking_recovers_registered_flux_multiple)

  have area_sign:
    "tv_oriented_area2 ax ay bx by = - tv_oriented_area2 bx by ax ay"
    by (rule tv_oriented_area2_swaps_sign)

  have boundary_closed:
    "gauss_bonnet_boundary_total surface_curvature boundary_curvature chi = 0"
    using boundary
    by (rule tv_boundary_balance_closes_gauss_bonnet)

  have gap_guard:
    "topological_protection_guard gap perturbation"
    using gap
    by (rule tv_gap_protection_implies_batch005_guard)

  have state_guard:
    "topological_quantum_state_guard gap"
    using gap
    by (rule tv_gap_protection_implies_quantum_state_guard)

  have winding_update:
    "tv_discrete_winding_index (phase + 2 * pi) (n + 1)"
    using winding
    by (rule tv_winding_index_adds_full_turn)

  from flux_quantized flux_form area_sign boundary_closed
    gap_guard state_guard winding_update
  show ?thesis
    by blast
qed

section \<open>Combined Spine Contract\<close>

theorem vector_calculus_isar_spine_contract:
  assumes mixed_partials: "partial_x_grad_y = partial_y_grad_x"
    and active: "gm_phase_vector_active gx gy"
    and coupling_nonzero: "coupling \<noteq> 0"
    and offset_nonzero: "source_offset \<noteq> 0"
    and phase_gradient_def: "phase_gradient = sqrt (gm_grad_mag_sq gx gy)"
    and phase_gradient_nonzero: "phase_gradient \<noteq> 0"
    and ideal: "eta = 0"
    and elsasser: "mt_elsasser_balance magnetic_force coriolis_force"
    and boundary: "tv_boundary_curvature_balance surface_curvature boundary_curvature chi"
    and gap: "tv_topological_gap_protected gap perturbation"
    and winding: "tv_discrete_winding_index phase n"
  shows "gm_curl_z partial_x_grad_y partial_y_grad_x = 0
    \<and> (gx \<noteq> 0 \<or> gy \<noteq> 0)
    \<and> gm_Lz_witness phase_gradient source_offset coupling \<noteq> 0
    \<and> mt_vector_helicity_density ax ay az 0 0 0 = 0
    \<and> mt_uniform_helicity_integral volume 0 = 0
    \<and> mt_ideal_mhd_helicity_conserved eta 0
    \<and> gm_resistive_helicity_dissipation eta current_norm_sq = 0
    \<and> elsasser_number magnetic_force coriolis_force = 1
    \<and> mt_torsion_density curvature (- curvature) = 0
    \<and> flux_quantized (topological_locking_flux flux_quantum n) flux_quantum n
    \<and> topological_locking_flux flux_quantum n =
        macroscopic_flux_multiple (of_int n) flux_quantum
    \<and> tv_oriented_area2 ax ay bx by = - tv_oriented_area2 bx by ax ay
    \<and> gauss_bonnet_boundary_total surface_curvature boundary_curvature chi = 0
    \<and> topological_protection_guard gap perturbation
    \<and> topological_quantum_state_guard gap
    \<and> tv_discrete_winding_index (phase + 2 * pi) (n + 1)"
proof -
  have curl_layer:
    "gm_curl_z partial_x_grad_y partial_y_grad_x = 0"
    using mixed_partials
    by (rule isar_delta_alpha_gradient_curl_layer)

  have gyro_layer:
    "(gx \<noteq> 0 \<or> gy \<noteq> 0) \<and>
     gm_Lz_witness phase_gradient source_offset coupling \<noteq> 0"
    using active coupling_nonzero offset_nonzero phase_gradient_def phase_gradient_nonzero
    by (rule isar_gyromagnetic_lz_layer)

  have magnetic_layer:
    "mt_vector_helicity_density ax ay az 0 0 0 = 0
     \<and> mt_uniform_helicity_integral volume 0 = 0
     \<and> mt_ideal_mhd_helicity_conserved eta 0
     \<and> gm_resistive_helicity_dissipation eta current_norm_sq = 0
     \<and> elsasser_number magnetic_force coriolis_force = 1
     \<and> mt_torsion_density curvature (- curvature) = 0"
    using ideal elsasser
    by (rule isar_magnetic_torsion_vector_layer)

  have topology_layer:
    "flux_quantized (topological_locking_flux flux_quantum n) flux_quantum n
     \<and> topological_locking_flux flux_quantum n =
         macroscopic_flux_multiple (of_int n) flux_quantum
     \<and> tv_oriented_area2 ax ay bx by = - tv_oriented_area2 bx by ax ay
     \<and> gauss_bonnet_boundary_total surface_curvature boundary_curvature chi = 0
     \<and> topological_protection_guard gap perturbation
     \<and> topological_quantum_state_guard gap
     \<and> tv_discrete_winding_index (phase + 2 * pi) (n + 1)"
    using boundary gap winding
    by (rule isar_topology_vector_layer)

  from curl_layer gyro_layer magnetic_layer topology_layer
  show ?thesis
    by blast
qed

text \<open>
  Paper-facing meaning: this Isar layer is the readable vector-calculus bridge
  over the spine stack.  It keeps the exact finite carriers already accepted
  by the session, but exposes the proof as four named layers rather than as a
  single algebraic closure: gradient/curl, gyromagnetic Lz, magnetic-torsion
  MHD, and topology/vector quantization.
\<close>

end
