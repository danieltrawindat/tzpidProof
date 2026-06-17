theory TZPID_TopologicalUnification_PriorityCandidates
  imports TZPID_QuantumGR_Unification_SourceLane
begin

section ‹Topological Unification Priority Candidate Review›

text ‹
  This theory records the first promotion-review slice extracted from the
  Topological Unification of QM and GR source.  It is deliberately a review
  ledger, not a registry mutation: candidates can be reused, carried as HOL
  structure, or minted only after semantic review against existing IDs.
›

datatype review_action =
    Reuse_Existing_ID
  | HOL_Carrier_First
  | Mint_After_Review
  | Merge_With_Existing_Spine

datatype priority_candidate =
    HigherTopos_ObjectDefinition
  | HigherTopos_HomMorphism
  | FQT_Metric_TensorSum
  | FQT_Metric_Product
  | HigherTopos_FormalDefinition
  | TZP_Vacuum_Divergence
  | Elsasser_Universality
  | Information_Manifold_Structure
  | Universal_Critical_Exponent
  | Topological_Field_Constraint
  | Topological_Locking
  | Universal_Criticality
  | Integrated_Information_Threshold
  | Discrete_Dark_Matter_Distribution

definition priority_candidates :: "priority_candidate list" where
  "priority_candidates =
    [HigherTopos_ObjectDefinition,
     HigherTopos_HomMorphism,
     FQT_Metric_TensorSum,
     FQT_Metric_Product,
     HigherTopos_FormalDefinition,
     TZP_Vacuum_Divergence,
     Elsasser_Universality,
     Information_Manifold_Structure,
     Universal_Critical_Exponent,
     Topological_Field_Constraint,
     Topological_Locking,
     Universal_Criticality,
     Integrated_Information_Threshold,
     Discrete_Dark_Matter_Distribution]"

fun candidate_source_line :: "priority_candidate ⇒ nat" where
  "candidate_source_line HigherTopos_ObjectDefinition = 105" |
  "candidate_source_line HigherTopos_HomMorphism = 133" |
  "candidate_source_line FQT_Metric_TensorSum = 284" |
  "candidate_source_line FQT_Metric_Product = 295" |
  "candidate_source_line HigherTopos_FormalDefinition = 84" |
  "candidate_source_line TZP_Vacuum_Divergence = 190" |
  "candidate_source_line Elsasser_Universality = 212" |
  "candidate_source_line Information_Manifold_Structure = 256" |
  "candidate_source_line Universal_Critical_Exponent = 306" |
  "candidate_source_line Topological_Field_Constraint = 338" |
  "candidate_source_line Topological_Locking = 351" |
  "candidate_source_line Universal_Criticality = 359" |
  "candidate_source_line Integrated_Information_Threshold = 397" |
  "candidate_source_line Discrete_Dark_Matter_Distribution = 406"

fun candidate_hash :: "priority_candidate ⇒ string" where
  "candidate_hash HigherTopos_ObjectDefinition = ''1205e9ba25965a99''" |
  "candidate_hash HigherTopos_HomMorphism = ''8bdb4a308b4c7745''" |
  "candidate_hash FQT_Metric_TensorSum = ''42cbc2c1cc1db942''" |
  "candidate_hash FQT_Metric_Product = ''3b4ba79e8c830be5''" |
  "candidate_hash HigherTopos_FormalDefinition = ''bd35f3642986a733''" |
  "candidate_hash TZP_Vacuum_Divergence = ''af1cae65ce435a9c''" |
  "candidate_hash Elsasser_Universality = ''87a127110afca265''" |
  "candidate_hash Information_Manifold_Structure = ''bbf6ecdcd074b3be''" |
  "candidate_hash Universal_Critical_Exponent = ''ee1a813d80dad971''" |
  "candidate_hash Topological_Field_Constraint = ''85ca76c6ee742972''" |
  "candidate_hash Topological_Locking = ''28920327c7d492dd''" |
  "candidate_hash Universal_Criticality = ''3b7bfd8741ee5dc4''" |
  "candidate_hash Integrated_Information_Threshold = ''6df8814d7d4f5bdb''" |
  "candidate_hash Discrete_Dark_Matter_Distribution = ''2787a900a46d9a72''"

fun review_action :: "priority_candidate ⇒ review_action" where
  "review_action HigherTopos_ObjectDefinition = HOL_Carrier_First" |
  "review_action HigherTopos_HomMorphism = HOL_Carrier_First" |
  "review_action FQT_Metric_TensorSum = HOL_Carrier_First" |
  "review_action FQT_Metric_Product = HOL_Carrier_First" |
  "review_action HigherTopos_FormalDefinition = HOL_Carrier_First" |
  "review_action TZP_Vacuum_Divergence = Reuse_Existing_ID" |
  "review_action Elsasser_Universality = Merge_With_Existing_Spine" |
  "review_action Information_Manifold_Structure = Reuse_Existing_ID" |
  "review_action Universal_Critical_Exponent = Reuse_Existing_ID" |
  "review_action Topological_Field_Constraint = Reuse_Existing_ID" |
  "review_action Topological_Locking = Merge_With_Existing_Spine" |
  "review_action Universal_Criticality = Reuse_Existing_ID" |
  "review_action Integrated_Information_Threshold = Reuse_Existing_ID" |
  "review_action Discrete_Dark_Matter_Distribution = Reuse_Existing_ID"

fun suggested_existing_ids :: "priority_candidate ⇒ string list" where
  "suggested_existing_ids Universal_Critical_Exponent =
     [''ID0395'', ''ID0470'', ''ID2283'']" |
  "suggested_existing_ids Universal_Criticality =
     [''ID0395'', ''ID0470'', ''ID9281'', ''ID9282'', ''ID9523'']" |
  "suggested_existing_ids Elsasser_Universality =
     [''ID0237'', ''ID0239'', ''ID0268'', ''ID0270'', ''ID0278'', ''ID0500'']" |
  "suggested_existing_ids Topological_Locking =
     [''ID3381'', ''ID4199'', ''ID5755'', ''ID5756'', ''ID4218'']" |
  "suggested_existing_ids TZP_Vacuum_Divergence =
     [''ID4214'', ''ID4227'', ''ID9529'']" |
  "suggested_existing_ids Information_Manifold_Structure =
     [''ID4192'', ''ID4193'', ''ID0245'', ''ID0285'', ''ID0396'']" |
  "suggested_existing_ids Topological_Field_Constraint =
     [''ID4195'', ''ID10136'', ''ID11134'', ''ID0140'', ''ID4305'']" |
  "suggested_existing_ids Integrated_Information_Threshold =
     [''ID4200'', ''ID4218'', ''ID4364'', ''ID0463'', ''ID8488'']" |
  "suggested_existing_ids Discrete_Dark_Matter_Distribution =
     [''ID4201'', ''ID4220'', ''ID4229'', ''ID11143'', ''ID0288'']" |
  "suggested_existing_ids _ = []"

fun minted_registry_id :: "priority_candidate ⇒ string option" where
  "minted_registry_id HigherTopos_ObjectDefinition = Some ''ID11373''" |
  "minted_registry_id HigherTopos_HomMorphism = Some ''ID11374''" |
  "minted_registry_id FQT_Metric_TensorSum = Some ''ID11375''" |
  "minted_registry_id FQT_Metric_Product = Some ''ID11376''" |
  "minted_registry_id HigherTopos_FormalDefinition = Some ''ID11372''" |
  "minted_registry_id _ = None"

definition mint_review_candidates :: "priority_candidate list" where
  "mint_review_candidates =
    filter (λc. review_action c = Mint_After_Review) priority_candidates"

definition reuse_or_merge_candidates :: "priority_candidate list" where
  "reuse_or_merge_candidates =
    filter (λc. review_action c = Reuse_Existing_ID ∨
               review_action c = Merge_With_Existing_Spine) priority_candidates"

definition carrier_first_candidates :: "priority_candidate list" where
  "carrier_first_candidates =
    filter (λc. review_action c = HOL_Carrier_First) priority_candidates"

theorem priority_candidate_count:
  "length priority_candidates = 14"
  by (eval)

theorem priority_candidates_distinct:
  "distinct priority_candidates"
  by (eval)

theorem mint_review_count:
  "length mint_review_candidates = 0"
  by (eval)

theorem reuse_or_merge_count:
  "length reuse_or_merge_candidates = 9"
  by (eval)

theorem carrier_first_count:
  "length carrier_first_candidates = 5"
  by (eval)

theorem carrier_first_candidates_are_minted:
  "c ∈ set carrier_first_candidates ⟹ minted_registry_id c ≠ None"
  by (cases c; eval)

theorem minted_carrier_registry_ids:
  "map minted_registry_id carrier_first_candidates =
   [Some ''ID11373'', Some ''ID11374'', Some ''ID11375'', Some ''ID11376'', Some ''ID11372'']"
  by (eval)

theorem reviewed_candidates_partition:
  "set mint_review_candidates ∪ set reuse_or_merge_candidates ∪ set carrier_first_candidates =
   set priority_candidates"
  by (eval)

theorem review_sources_are_topological_unification_lane:
  "Topological_Unification_QM_GR_Source ∈ set all_quantum_gr_bridge_sources"
  by (eval)

text ‹
  Paper-facing meaning: the priority candidates are now tracked as a typed
  promotion queue.  The first deduplication pass found existing registry homes
  for all five initial mint-review candidates.  The carrier-first categorical
  structures have now been minted as ID11372--ID11376 and linked back into this
  review ledger.
›

end
