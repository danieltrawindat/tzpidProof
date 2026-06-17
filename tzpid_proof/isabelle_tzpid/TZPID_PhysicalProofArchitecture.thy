theory TZPID_PhysicalProofArchitecture
  imports
    TZPID_VectorCalculus_IntegralCarriers
    TZPID_TopologyCategory_Carriers
    TZPID_TopologicalUnification_MintedCarriers
begin

text \<open>
  Project: TZPID Proof Pipeline
  Creator: Daniel Alexander Trawin
  ORCID: https://orcid.org/0009-0001-4630-3715
  Generated UTC: 2026-06-11T00:00:00Z

  Physical proof architecture.

  This layer records the Curry-Howard-Lambek/TQFT architecture used by the
  proof package:

    Logic propositions and proofs
      -> Types/programs/carriers
      -> Monoidal categorical processes
      -> Geometric/TQFT-style physical witnesses.

  The point is representational discipline.  It does not replace theorem
  proving with metaphor.  A spine is paper-ready only when its logical claim,
  typed carrier, categorical composition, and physical/computational witness
  are all present at the right strength.
\<close>

section \<open>Architecture Nodes and Edges\<close>

datatype proof_architecture_node =
    Logic_Proposition
  | Type_Program
  | Monoidal_Category
  | Geometry_TQFT

datatype proof_architecture_edge =
    Curry_Howard
  | Lambek_Logic_Category
  | Lambek_Type_Category
  | TQFT_Realization

definition proof_architecture_nodes :: "proof_architecture_node list" where
  "proof_architecture_nodes =
    [Logic_Proposition, Type_Program, Monoidal_Category, Geometry_TQFT]"

definition proof_architecture_edges :: "proof_architecture_edge list" where
  "proof_architecture_edges =
    [Curry_Howard, Lambek_Logic_Category, Lambek_Type_Category, TQFT_Realization]"

fun edge_source :: "proof_architecture_edge \<Rightarrow> proof_architecture_node" where
  "edge_source Curry_Howard = Logic_Proposition" |
  "edge_source Lambek_Logic_Category = Logic_Proposition" |
  "edge_source Lambek_Type_Category = Type_Program" |
  "edge_source TQFT_Realization = Monoidal_Category"

fun edge_target :: "proof_architecture_edge \<Rightarrow> proof_architecture_node" where
  "edge_target Curry_Howard = Type_Program" |
  "edge_target Lambek_Logic_Category = Monoidal_Category" |
  "edge_target Lambek_Type_Category = Monoidal_Category" |
  "edge_target TQFT_Realization = Geometry_TQFT"

theorem physical_architecture_node_count:
  "length proof_architecture_nodes = 4"
  unfolding proof_architecture_nodes_def
  by eval

theorem physical_architecture_edge_count:
  "length proof_architecture_edges = 4"
  unfolding proof_architecture_edges_def
  by eval

theorem physical_architecture_edges_are_well_typed:
  assumes "e \<in> set proof_architecture_edges"
  shows "edge_source e \<in> set proof_architecture_nodes
    \<and> edge_target e \<in> set proof_architecture_nodes"
  using assms
  unfolding proof_architecture_edges_def proof_architecture_nodes_def
  by (cases e; simp)

section \<open>Proof Objects as Physical Architecture\<close>

record physical_proof_object =
  logic_view :: category_object
  type_view :: category_object
  process_view :: category_object
  geometry_view :: category_object

definition curry_howard_witness :: "physical_proof_object \<Rightarrow> bool" where
  "curry_howard_witness p \<longleftrightarrow>
    logic_view p = type_view p"

definition lambek_witness :: "physical_proof_object \<Rightarrow> bool" where
  "lambek_witness p \<longleftrightarrow>
    logic_view p = process_view p \<and> type_view p = process_view p"

definition tqft_witness :: "physical_proof_object \<Rightarrow> bool" where
  "tqft_witness p \<longleftrightarrow>
    process_view p = geometry_view p"

definition physical_proof_realized :: "physical_proof_object \<Rightarrow> bool" where
  "physical_proof_realized p \<longleftrightarrow>
    curry_howard_witness p \<and> lambek_witness p \<and> tqft_witness p"

definition physical_proof_object_of :: "category_object \<Rightarrow> physical_proof_object" where
  "physical_proof_object_of obj =
    \<lparr> logic_view = obj,
      type_view = obj,
      process_view = obj,
      geometry_view = obj \<rparr>"

theorem physical_proof_object_of_realized:
  "physical_proof_realized (physical_proof_object_of obj)"
proof -
  have ch: "curry_howard_witness (physical_proof_object_of obj)"
    unfolding curry_howard_witness_def physical_proof_object_of_def
    by simp
  have lambek: "lambek_witness (physical_proof_object_of obj)"
    unfolding lambek_witness_def physical_proof_object_of_def
    by simp
  have tqft: "tqft_witness (physical_proof_object_of obj)"
    unfolding tqft_witness_def physical_proof_object_of_def
    by simp
  show ?thesis
    unfolding physical_proof_realized_def
    using ch lambek tqft
    by blast
qed

theorem physical_proof_realized_collapses_views:
  assumes "physical_proof_realized p"
  shows "logic_view p = geometry_view p
    \<and> type_view p = geometry_view p
    \<and> process_view p = geometry_view p"
proof -
  have ch: "logic_view p = type_view p"
    using assms
    unfolding physical_proof_realized_def curry_howard_witness_def
    by blast
  have lambek:
    "logic_view p = process_view p \<and> type_view p = process_view p"
    using assms
    unfolding physical_proof_realized_def lambek_witness_def
    by blast
  have tqft: "process_view p = geometry_view p"
    using assms
    unfolding physical_proof_realized_def tqft_witness_def
    by blast
  show ?thesis
    using ch lambek tqft
    by blast
qed

section \<open>Monoidal Composition Carriers\<close>

definition proof_tensor_object :: "category_object \<Rightarrow> category_object \<Rightarrow> category_object" where
  "proof_tensor_object left right = left + right"

definition proof_tensor_arrow :: "category_arrow \<Rightarrow> category_arrow \<Rightarrow> category_arrow" where
  "proof_tensor_arrow left right =
    (proof_tensor_object (arrow_domain left) (arrow_domain right),
     proof_tensor_object (arrow_codomain left) (arrow_codomain right))"

definition physical_proof_tensor ::
  "physical_proof_object \<Rightarrow> physical_proof_object \<Rightarrow> physical_proof_object" where
  "physical_proof_tensor left right =
    \<lparr> logic_view =
        proof_tensor_object (logic_view left) (logic_view right),
      type_view =
        proof_tensor_object (type_view left) (type_view right),
      process_view =
        proof_tensor_object (process_view left) (process_view right),
      geometry_view =
        proof_tensor_object (geometry_view left) (geometry_view right) \<rparr>"

theorem proof_tensor_object_associative:
  "proof_tensor_object (proof_tensor_object a b) c =
   proof_tensor_object a (proof_tensor_object b c)"
  unfolding proof_tensor_object_def
  by simp

theorem proof_tensor_object_unit_left:
  "proof_tensor_object 0 obj = obj"
  unfolding proof_tensor_object_def
  by simp

theorem proof_tensor_object_unit_right:
  "proof_tensor_object obj 0 = obj"
  unfolding proof_tensor_object_def
  by simp

theorem proof_tensor_arrow_domain:
  "arrow_domain (proof_tensor_arrow left right) =
   proof_tensor_object (arrow_domain left) (arrow_domain right)"
  unfolding proof_tensor_arrow_def arrow_domain_def
  by simp

theorem proof_tensor_arrow_codomain:
  "arrow_codomain (proof_tensor_arrow left right) =
   proof_tensor_object (arrow_codomain left) (arrow_codomain right)"
  unfolding proof_tensor_arrow_def arrow_codomain_def
  by simp

theorem physical_proof_tensor_preserves_realization:
  assumes "physical_proof_realized left"
    and "physical_proof_realized right"
  shows "physical_proof_realized (physical_proof_tensor left right)"
proof -
  have left_eq:
    "logic_view left = geometry_view left
     \<and> type_view left = geometry_view left
     \<and> process_view left = geometry_view left"
    using assms(1)
    by (rule physical_proof_realized_collapses_views)
  have right_eq:
    "logic_view right = geometry_view right
     \<and> type_view right = geometry_view right
     \<and> process_view right = geometry_view right"
    using assms(2)
    by (rule physical_proof_realized_collapses_views)
  show ?thesis
    unfolding physical_proof_realized_def curry_howard_witness_def
      lambek_witness_def tqft_witness_def physical_proof_tensor_def
      proof_tensor_object_def
    using left_eq right_eq
    by simp
qed

section \<open>Spine Bridge Contract\<close>

definition physical_architecture_registry_anchor :: "string list" where
  "physical_architecture_registry_anchor =
    [''ID2631'', ''ID11372'', ''ID11373'', ''ID11374'', ''ID11375'', ''ID11376'']"

definition physical_architecture_document :: string where
  "physical_architecture_document =
    ''peer_review/unification_intake/PHYSICAL_PROOF_ARCHITECTURE.md''"

theorem physical_architecture_registry_anchor_count:
  "length physical_architecture_registry_anchor = 6"
  unfolding physical_architecture_registry_anchor_def
  by eval

theorem physical_architecture_consumes_minted_topos_carriers:
  "map minted_carrier_tzpid minted_topological_unification_carriers =
   [''ID11372'', ''ID11373'', ''ID11374'', ''ID11375'', ''ID11376'']"
  using minted_carriers_have_tzpids .

theorem physical_architecture_consumes_vector_calculus_carrier:
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

theorem physical_proof_architecture_contract:
  assumes "physical_proof_realized left"
    and "physical_proof_realized right"
    and "0 \<le> width"
    and "0 \<le> height"
    and "partial_y_Fy = - partial_x_Fx"
  shows "physical_proof_realized (physical_proof_tensor left right)
    \<and> length proof_architecture_nodes = 4
    \<and> length proof_architecture_edges = 4
    \<and> length physical_architecture_registry_anchor = 6
    \<and> vc_rect_boundary_circulation curl_strength width height =
        vc_rect_surface_flux curl_strength width height
    \<and> flux_quantized (vc_quantized_flux flux_quantum m) flux_quantum m"
proof (intro conjI)
  show "physical_proof_realized (physical_proof_tensor left right)"
    using assms(1,2)
    by (rule physical_proof_tensor_preserves_realization)
  show "length proof_architecture_nodes = 4"
    using physical_architecture_node_count .
  show "length proof_architecture_edges = 4"
    using physical_architecture_edge_count .
  show "length physical_architecture_registry_anchor = 6"
    using physical_architecture_registry_anchor_count .
  show "vc_rect_boundary_circulation curl_strength width height =
        vc_rect_surface_flux curl_strength width height"
    using assms(3,4,5)
      physical_architecture_consumes_vector_calculus_carrier
    by blast
  show "flux_quantized (vc_quantized_flux flux_quantum m) flux_quantum m"
    using assms(3,4,5)
      physical_architecture_consumes_vector_calculus_carrier
    by blast
qed

text \<open>
  Paper-facing meaning: a proof spine can now be represented physically as a
  four-view object.  Logic, type/program, categorical process, and geometric
  witness are not competing explanations; they are typed views of the same
  architecture.  Composition is represented by the monoidal tensor carrier,
  and checked physical witnesses such as circulation/flux/winding are consumed
  through the vector-calculus carrier layer.
\<close>

end
