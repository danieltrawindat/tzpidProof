theory TZPID_TRAWIN_Composition_GoldSpine
  imports TZPID_PhysicalProofArchitecture
begin

text \<open>
  Project: TZPID Proof Pipeline
  Creator: Daniel Alexander Trawin
  ORCID: https://orcid.org/0009-0001-4630-3715
  Generated UTC: 2026-06-11T00:00:00Z

  TRAWIN composition gold-spine carrier.

  This layer records the operator composition

    C_R = N o I o W o A o R o T

  from the TRAWIN operator pass as a finite HOL spine.  It connects the
  curated gold-spine keystones to the vector-calculus Isar carrier layer and
  the Curry-Howard-Lambek/TQFT physical proof architecture.

  The theory proves structural closure of the certificate layer.  It does not
  claim to prove the full manifold/tensor physics of the paper-facing claims;
  those remain stronger analytic obligations where marked.
\<close>

section \<open>Operator Alphabet\<close>

datatype trawin_operator =
    T_TimeDerivative
  | R_RotationCurl
  | A_Amplitude
  | W_WaveBox
  | I_Integral
  | N_Normalization

definition trawin_composition :: "trawin_operator list" where
  "trawin_composition =
    [N_Normalization, I_Integral, W_WaveBox,
     A_Amplitude, R_RotationCurl, T_TimeDerivative]"

theorem trawin_composition_operator_count:
  "length trawin_composition = 6"
  unfolding trawin_composition_def
  by eval

theorem trawin_composition_distinct:
  "distinct trawin_composition"
  unfolding trawin_composition_def
  by eval

theorem trawin_composition_head_is_normalization:
  "trawin_composition =
    N_Normalization # [I_Integral, W_WaveBox,
      A_Amplitude, R_RotationCurl, T_TimeDerivative]"
  unfolding trawin_composition_def
  by simp

section \<open>Gold-Spine Keystones\<close>

datatype trawin_keystone =
    ID0335_Einstein_Limit
  | ID0167_Conservation
  | ID0394_Vacuum_Tensor
  | ID0958_Wave_Carrier
  | ID0400_ID1392_Hubble_Normalization
  | ID10867_Volume_Breathing_Rate
  | ID10868_Lambda_Constancy
  | ID10869_Dark_Energy_Length
  | ID10870_Planck_Ratio
  | ID10871_Friedmann_Closure

datatype trawin_closure_status =
    Checked_Symbolic
  | Checked_Numeric
  | Wolfram_Backend_Checked
  | Open_Analytic_Obligation

definition trawin_goldspine_keystones :: "trawin_keystone list" where
  "trawin_goldspine_keystones =
    [ID0335_Einstein_Limit,
     ID0167_Conservation,
     ID0394_Vacuum_Tensor,
     ID0958_Wave_Carrier,
     ID0400_ID1392_Hubble_Normalization,
     ID10867_Volume_Breathing_Rate,
     ID10868_Lambda_Constancy,
     ID10869_Dark_Energy_Length,
     ID10870_Planck_Ratio,
     ID10871_Friedmann_Closure]"

fun trawin_status :: "trawin_keystone \<Rightarrow> trawin_closure_status" where
  "trawin_status ID0335_Einstein_Limit = Checked_Symbolic" |
  "trawin_status ID0167_Conservation = Checked_Symbolic" |
  "trawin_status ID0394_Vacuum_Tensor = Wolfram_Backend_Checked" |
  "trawin_status ID0958_Wave_Carrier = Checked_Symbolic" |
  "trawin_status ID0400_ID1392_Hubble_Normalization = Wolfram_Backend_Checked" |
  "trawin_status ID10867_Volume_Breathing_Rate = Checked_Numeric" |
  "trawin_status ID10868_Lambda_Constancy = Checked_Symbolic" |
  "trawin_status ID10869_Dark_Energy_Length = Checked_Numeric" |
  "trawin_status ID10870_Planck_Ratio = Checked_Numeric" |
  "trawin_status ID10871_Friedmann_Closure = Open_Analytic_Obligation"

fun trawin_registry_id :: "trawin_keystone \<Rightarrow> string" where
  "trawin_registry_id ID0335_Einstein_Limit = ''ID0335''" |
  "trawin_registry_id ID0167_Conservation = ''ID0167''" |
  "trawin_registry_id ID0394_Vacuum_Tensor = ''ID0394''" |
  "trawin_registry_id ID0958_Wave_Carrier = ''ID0958''" |
  "trawin_registry_id ID0400_ID1392_Hubble_Normalization = ''ID0400/ID1392''" |
  "trawin_registry_id ID10867_Volume_Breathing_Rate = ''ID10867''" |
  "trawin_registry_id ID10868_Lambda_Constancy = ''ID10868''" |
  "trawin_registry_id ID10869_Dark_Energy_Length = ''ID10869''" |
  "trawin_registry_id ID10870_Planck_Ratio = ''ID10870''" |
  "trawin_registry_id ID10871_Friedmann_Closure = ''ID10871''"

theorem trawin_goldspine_keystone_count:
  "length trawin_goldspine_keystones = 10"
  unfolding trawin_goldspine_keystones_def
  by eval

theorem trawin_goldspine_keystones_distinct:
  "distinct trawin_goldspine_keystones"
  unfolding trawin_goldspine_keystones_def
  by eval

theorem trawin_registry_ids_nonempty:
  assumes "k \<in> set trawin_goldspine_keystones"
  shows "trawin_registry_id k \<noteq> ''''"
  using assms
  unfolding trawin_goldspine_keystones_def
  by (cases k; simp)

theorem trawin_only_friedmann_is_open_obligation:
  assumes "k \<in> set trawin_goldspine_keystones"
    and "trawin_status k = Open_Analytic_Obligation"
  shows "k = ID10871_Friedmann_Closure"
  using assms
  unfolding trawin_goldspine_keystones_def
  by (cases k; simp)

section \<open>Carrier Consumption\<close>

theorem trawin_id0335_consumes_gradient_curl_carrier:
  assumes "partial_x_grad_y = partial_y_grad_x"
  shows "gm_curl_z partial_x_grad_y partial_y_grad_x = 0"
  using assms
  by (rule isar_delta_alpha_gradient_curl_layer)

theorem trawin_id0167_consumes_divergence_carrier:
  assumes "partial_y_Fy = - partial_x_Fx"
  shows "vc_incompressible_planar partial_x_Fx partial_y_Fy"
  using assms
  by (rule vc_incompressible_from_opposite_partials)

theorem trawin_id0958_consumes_wave_carrier:
  assumes mixed_partials: "partial_x_grad_y = partial_y_grad_x"
    and active: "gm_phase_vector_active gx gy"
    and coupling_nonzero: "coupling \<noteq> 0"
    and offset_nonzero: "source_offset \<noteq> 0"
    and phase_gradient_def: "phase_gradient = sqrt (gm_grad_mag_sq gx gy)"
    and ideal: "eta = 0"
    and elsasser: "mt_elsasser_balance magnetic_force coriolis_force"
    and boundary: "tv_boundary_curvature_balance surface_curvature boundary_curvature chi"
    and gap: "tv_topological_gap_protected gap perturbation"
    and winding: "tv_discrete_winding_index phase n"
  shows "gm_curl_z partial_x_grad_y partial_y_grad_x = 0
    \<and> gm_angular_momentum_emerges coupling source_offset phase_gradient
    \<and> mt_vector_helicity_density ax ay az 0 0 0 = 0
    \<and> flux_quantized (topological_locking_flux flux_quantum n) flux_quantum n"
  using assms
  by (rule vector_calculus_isar_spine_contract)

theorem trawin_id10867_consumes_volume_carrier:
  assumes "0 \<le> width"
    and "0 \<le> height"
  shows "0 \<le> vc_rectangle_area width height"
  using assms
  by (rule vc_rectangle_area_nonnegative)

theorem trawin_id10868_consumes_zero_density_carrier:
  "vc_uniform_helicity_integral volume 0 = 0"
  by (rule vc_uniform_helicity_integral_zero_density)

theorem trawin_id10871_consumes_integral_carrier_as_obligation_surface:
  assumes "0 \<le> width"
    and "0 \<le> height"
    and "partial_y_Fy = - partial_x_Fx"
  shows "vc_rect_boundary_circulation curl_strength width height =
        vc_rect_surface_flux curl_strength width height
    \<and> vc_incompressible_planar partial_x_Fx partial_y_Fy
    \<and> flux_quantized (vc_quantized_flux flux_quantum m) flux_quantum m
    \<and> tv_discrete_winding_index (vc_quantized_circulation m) m"
proof -
  have carrier:
    "0 \<le> vc_rectangle_area width height
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
    using assms
    by (rule vector_calculus_integral_carrier_contract)
  thus ?thesis
    by blast
qed

section \<open>Physical Architecture Bridge\<close>

theorem trawin_composition_consumes_physical_architecture:
  assumes "physical_proof_realized left"
    and "physical_proof_realized right"
    and "0 \<le> width"
    and "0 \<le> height"
    and "partial_y_Fy = - partial_x_Fx"
  shows "physical_proof_realized (physical_proof_tensor left right)
    \<and> length trawin_composition = 6
    \<and> length trawin_goldspine_keystones = 10
    \<and> length physical_architecture_nodes = 4
    \<and> vc_rect_boundary_circulation curl_strength width height =
        vc_rect_surface_flux curl_strength width height
    \<and> flux_quantized (vc_quantized_flux flux_quantum m) flux_quantum m"
proof (intro conjI)
  show "physical_proof_realized (physical_proof_tensor left right)"
    using assms(1,2)
    by (rule physical_proof_tensor_preserves_realization)
  show "length trawin_composition = 6"
    by (rule trawin_composition_operator_count)
  show "length trawin_goldspine_keystones = 10"
    by (rule trawin_goldspine_keystone_count)
  show "length physical_architecture_nodes = 4"
    by (rule physical_architecture_node_count)
  show "vc_rect_boundary_circulation curl_strength width height =
        vc_rect_surface_flux curl_strength width height"
    using assms(3,4)
    by (rule vc_green_rectangle_constant_curl)
  show "flux_quantized (vc_quantized_flux flux_quantum m) flux_quantum m"
    by (rule vc_quantized_flux_is_quantized)
qed

theorem trawin_goldspine_closure_contract:
  assumes "0 \<le> width"
    and "0 \<le> height"
    and "partial_y_Fy = - partial_x_Fx"
  shows "length trawin_composition = 6
    \<and> distinct trawin_composition
    \<and> length trawin_goldspine_keystones = 10
    \<and> distinct trawin_goldspine_keystones
    \<and> trawin_status ID10871_Friedmann_Closure = Open_Analytic_Obligation
    \<and> vc_rect_boundary_circulation curl_strength width height =
        vc_rect_surface_flux curl_strength width height
    \<and> vc_incompressible_planar partial_x_Fx partial_y_Fy"
proof (intro conjI)
  show "length trawin_composition = 6"
    by (rule trawin_composition_operator_count)
  show "distinct trawin_composition"
    by (rule trawin_composition_distinct)
  show "length trawin_goldspine_keystones = 10"
    by (rule trawin_goldspine_keystone_count)
  show "distinct trawin_goldspine_keystones"
    by (rule trawin_goldspine_keystones_distinct)
  show "trawin_status ID10871_Friedmann_Closure = Open_Analytic_Obligation"
    by simp
  show "vc_rect_boundary_circulation curl_strength width height =
        vc_rect_surface_flux curl_strength width height"
    by (rule vc_green_rectangle_constant_curl)
  show "vc_incompressible_planar partial_x_Fx partial_y_Fy"
    using assms(3)
    by (rule vc_incompressible_from_opposite_partials)
qed

text \<open>
  Paper-facing meaning: the TRAWIN composition is now represented as a
  six-operator HOL spine over ten curated registry keystones.  The checked
  symbolic/numeric layer is kept separate from the one open analytic
  Friedmann obligation, and the composition consumes both the vector-calculus
  Isar layer and the physical proof architecture.
\<close>

end
