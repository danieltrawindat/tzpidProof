theory TZPID_TopologicalUnification_MintedCarriers
  imports TZPID_TopologicalUnification_PriorityCandidates
begin

section ‹Minted Topological Unification Carrier IDs›

text ‹
  This theory records the carrier-first Topological Unification structures that
  were minted as registry IDs after the deduplication pass.  These are
  addressable carrier definitions, not duplicate theorem claims.
›

datatype minted_carrier =
    ID11372_HigherTopos_PhysicalReality
  | ID11373_HigherTopos_ObjectClass
  | ID11374_HigherTopos_MorphismClass
  | ID11375_FQT_Metric_TensorSum
  | ID11376_FQT_Metric_Product

definition minted_topological_unification_carriers :: "minted_carrier list" where
  "minted_topological_unification_carriers =
    [ID11372_HigherTopos_PhysicalReality,
     ID11373_HigherTopos_ObjectClass,
     ID11374_HigherTopos_MorphismClass,
     ID11375_FQT_Metric_TensorSum,
     ID11376_FQT_Metric_Product]"

fun minted_carrier_tzpid :: "minted_carrier ⇒ string" where
  "minted_carrier_tzpid ID11372_HigherTopos_PhysicalReality = ''ID11372''" |
  "minted_carrier_tzpid ID11373_HigherTopos_ObjectClass = ''ID11373''" |
  "minted_carrier_tzpid ID11374_HigherTopos_MorphismClass = ''ID11374''" |
  "minted_carrier_tzpid ID11375_FQT_Metric_TensorSum = ''ID11375''" |
  "minted_carrier_tzpid ID11376_FQT_Metric_Product = ''ID11376''"

fun minted_carrier_source_candidate :: "minted_carrier ⇒ priority_candidate" where
  "minted_carrier_source_candidate ID11372_HigherTopos_PhysicalReality =
     HigherTopos_FormalDefinition" |
  "minted_carrier_source_candidate ID11373_HigherTopos_ObjectClass =
     HigherTopos_ObjectDefinition" |
  "minted_carrier_source_candidate ID11374_HigherTopos_MorphismClass =
     HigherTopos_HomMorphism" |
  "minted_carrier_source_candidate ID11375_FQT_Metric_TensorSum =
     FQT_Metric_TensorSum" |
  "minted_carrier_source_candidate ID11376_FQT_Metric_Product =
     FQT_Metric_Product"

definition minted_carrier_wolfram_artifact :: string where
  "minted_carrier_wolfram_artifact =
    ''peer_review/unification_intake/wolfram/topological_unification_carrier_mint_check_results.json''"

definition minted_carrier_source_truth_root :: string where
  "minted_carrier_source_truth_root = ''D:/TZPIDProof/tzp_id''"

definition minted_carrier_verified :: "minted_carrier ⇒ bool" where
  "minted_carrier_verified c ⟷
     minted_carrier_source_candidate c ∈ set carrier_first_candidates ∧
     review_action (minted_carrier_source_candidate c) = HOL_Carrier_First"

theorem minted_carrier_count:
  "length minted_topological_unification_carriers = 5"
  by (eval)

theorem minted_carriers_distinct:
  "distinct minted_topological_unification_carriers"
  by (eval)

theorem minted_carriers_have_tzpids:
  "map minted_carrier_tzpid minted_topological_unification_carriers =
   [''ID11372'', ''ID11373'', ''ID11374'', ''ID11375'', ''ID11376'']"
  by (eval)

theorem minted_carriers_trace_to_priority_candidates:
  "c ∈ set minted_topological_unification_carriers ⟹
   minted_carrier_source_candidate c ∈ set priority_candidates"
  by (cases c; eval)

theorem all_minted_carriers_verified:
  "c ∈ set minted_topological_unification_carriers ⟹ minted_carrier_verified c"
  by (cases c; simp add: minted_carrier_verified_def carrier_first_candidates_def priority_candidates_def)

theorem minted_carrier_artifact_recorded:
  "minted_carrier_wolfram_artifact =
   ''peer_review/unification_intake/wolfram/topological_unification_carrier_mint_check_results.json''"
  by (simp add: minted_carrier_wolfram_artifact_def)

text ‹
  Paper-facing meaning: ID11372--ID11376 provide stable registry addresses for
  the higher-topos and FQT metric carrier structures.  Their Wolfram status is
  symbolic-carrier verification; downstream theories may consume these as
  typed vocabulary before attempting stronger theorem obligations.
›

end
