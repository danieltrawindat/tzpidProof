theory TZPID_ExternalEvidence_Certificates
  imports
    TZPID_QuantumGR_Unification_SourceLane
    TZPID_TopologicalUnification_Focus
    TZPID_Einstein_Focus
    TZPID_PhaseLockingResonance_Focus
begin

section ‹External Evidence Certificates›

text ‹
  D:\Proofs is treated as an external evidence lane: it contains citation,
  experiment, lab, lecture-note, DOI/arXiv, and proof-support tables.  Isabelle
  does not prove the external experiment itself.  It records that a registry
  claim or paper section has an external evidence anchor of the expected domain.
›

datatype evidence_domain =
    Evidence_Quantum
  | Evidence_GR
  | Evidence_Topology
  | Evidence_Cosmology
  | Evidence_BesselWave
  | Evidence_Gyromagnetic
  | Evidence_Synchronization

datatype evidence_source_kind =
    DOI_Source
  | Arxiv_Source
  | University_Lecture_Source
  | University_Project_Source
  | Journal_Source
  | Dataset_Source
  | ProofSupport_Table_Source
  | Internal_Report_Source

datatype external_evidence_anchor =
    MIT_Schwarzschild_Time_Dilation
  | MIT_Topological_Defect_Project
  | Arxiv_Quantum_Coriolis
  | Quantum_Hall_Evidence
  | Kuramoto_Order_Parameter_Source
  | Planetary_Data_Source
  | ProofSupport_ID0000_0099
  | ProofSupport_ID0200_0299
  | ProofSupport_ID0300_0399
  | ProofSearch_MasterChunks

fun anchor_kind :: "external_evidence_anchor ⇒ evidence_source_kind set" where
  "anchor_kind MIT_Schwarzschild_Time_Dilation = {University_Lecture_Source}" |
  "anchor_kind MIT_Topological_Defect_Project = {University_Project_Source}" |
  "anchor_kind Arxiv_Quantum_Coriolis = {Arxiv_Source, DOI_Source}" |
  "anchor_kind Quantum_Hall_Evidence = {Journal_Source, University_Lecture_Source}" |
  "anchor_kind Kuramoto_Order_Parameter_Source = {University_Project_Source}" |
  "anchor_kind Planetary_Data_Source = {Dataset_Source}" |
  "anchor_kind ProofSupport_ID0000_0099 = {ProofSupport_Table_Source}" |
  "anchor_kind ProofSupport_ID0200_0299 = {ProofSupport_Table_Source}" |
  "anchor_kind ProofSupport_ID0300_0399 = {ProofSupport_Table_Source}" |
  "anchor_kind ProofSearch_MasterChunks = {Internal_Report_Source, ProofSupport_Table_Source}"

fun anchor_domains :: "external_evidence_anchor ⇒ evidence_domain set" where
  "anchor_domains MIT_Schwarzschild_Time_Dilation = {Evidence_GR}" |
  "anchor_domains MIT_Topological_Defect_Project = {Evidence_Topology, Evidence_Quantum}" |
  "anchor_domains Arxiv_Quantum_Coriolis = {Evidence_Quantum, Evidence_Gyromagnetic}" |
  "anchor_domains Quantum_Hall_Evidence = {Evidence_Quantum, Evidence_Topology}" |
  "anchor_domains Kuramoto_Order_Parameter_Source = {Evidence_Synchronization}" |
  "anchor_domains Planetary_Data_Source = {Evidence_Cosmology, Evidence_Synchronization}" |
  "anchor_domains ProofSupport_ID0000_0099 =
     {Evidence_Quantum, Evidence_GR, Evidence_Topology, Evidence_BesselWave,
      Evidence_Gyromagnetic}" |
  "anchor_domains ProofSupport_ID0200_0299 =
     {Evidence_Quantum, Evidence_GR, Evidence_Topology, Evidence_BesselWave,
      Evidence_Gyromagnetic}" |
  "anchor_domains ProofSupport_ID0300_0399 =
     {Evidence_Quantum, Evidence_GR, Evidence_Topology, Evidence_BesselWave,
      Evidence_Gyromagnetic}" |
  "anchor_domains ProofSearch_MasterChunks =
     {Evidence_Quantum, Evidence_GR, Evidence_Topology, Evidence_BesselWave,
      Evidence_Gyromagnetic, Evidence_Cosmology}"

definition all_external_evidence_anchors :: "external_evidence_anchor list" where
  "all_external_evidence_anchors =
    [MIT_Schwarzschild_Time_Dilation,
     MIT_Topological_Defect_Project,
     Arxiv_Quantum_Coriolis,
     Quantum_Hall_Evidence,
     Kuramoto_Order_Parameter_Source,
     Planetary_Data_Source,
     ProofSupport_ID0000_0099,
     ProofSupport_ID0200_0299,
     ProofSupport_ID0300_0399,
     ProofSearch_MasterChunks]"

definition externally_supported_in_domain ::
  "external_evidence_anchor ⇒ evidence_domain ⇒ bool" where
  "externally_supported_in_domain a d ⟷ d ∈ anchor_domains a"

definition has_external_source_kind ::
  "external_evidence_anchor ⇒ evidence_source_kind ⇒ bool" where
  "has_external_source_kind a k ⟷ k ∈ anchor_kind a"

definition quantum_gr_external_bridge_anchor :: "external_evidence_anchor ⇒ bool" where
  "quantum_gr_external_bridge_anchor a ⟷
     Evidence_Quantum ∈ anchor_domains a ∧
     (Evidence_GR ∈ anchor_domains a ∨ Evidence_Topology ∈ anchor_domains a)"

theorem external_evidence_anchor_count:
  "length all_external_evidence_anchors = 10"
  by (eval)

theorem external_evidence_anchor_distinct:
  "distinct all_external_evidence_anchors"
  by (eval)

theorem every_anchor_has_kind:
  "a ∈ set all_external_evidence_anchors ⟹ anchor_kind a ≠ {}"
  by (cases a; simp add: all_external_evidence_anchors_def)

theorem every_anchor_has_domain:
  "a ∈ set all_external_evidence_anchors ⟹ anchor_domains a ≠ {}"
  by (cases a; simp add: all_external_evidence_anchors_def)

theorem mit_relativity_supports_gr:
  "externally_supported_in_domain MIT_Schwarzschild_Time_Dilation Evidence_GR"
  by (simp add: externally_supported_in_domain_def)

theorem mit_topological_project_supports_quantum_topology:
  "externally_supported_in_domain MIT_Topological_Defect_Project Evidence_Quantum ∧
   externally_supported_in_domain MIT_Topological_Defect_Project Evidence_Topology"
  by (simp add: externally_supported_in_domain_def)

theorem quantum_hall_is_quantum_topology_bridge:
  "quantum_gr_external_bridge_anchor Quantum_Hall_Evidence"
  by (simp add: quantum_gr_external_bridge_anchor_def)

theorem proof_support_tables_are_external_lane_anchors:
  "has_external_source_kind ProofSupport_ID0000_0099 ProofSupport_Table_Source ∧
   has_external_source_kind ProofSupport_ID0200_0299 ProofSupport_Table_Source ∧
   has_external_source_kind ProofSupport_ID0300_0399 ProofSupport_Table_Source"
  by (simp add: has_external_source_kind_def)

text ‹
  Use this lane in papers as: "externally supported" or "externally anchored",
  not as "formally proven by experiment".  The formal statement is that a claim
  has a declared evidence anchor in the expected physical domain.
›

end
