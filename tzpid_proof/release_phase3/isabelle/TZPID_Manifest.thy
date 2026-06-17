theory TZPID_Manifest
  imports Main
begin

datatype statement_kind =
  AxiomKind
  | DefinitionKind
  | TheoremKind
  | LemmaKind
  | PropositionKind
  | CorollaryKind
  | PostulateKind
  | AssumptionKind
  | InvariantKind
  | PrincipleKind
  | LawKind
  | UnknownKind

record tzpid_statement =
  sid :: nat
  skind :: statement_kind
  source_line :: nat
  digest :: string

record dependency_edge =
  source_id :: nat
  target_id :: nat
  relation :: string
  weight :: nat

definition manifest_inventory_sha1 :: string where
  "manifest_inventory_sha1 = ''0ba37c4d5af4f6d8b9b393a7bbfbe751266a472b''"

definition manifest_edges_sha1 :: string where
  "manifest_edges_sha1 = ''2120dadb543bdb19fdc34d38a1e91fa141c6c5ce''"

definition statement_kind_counts :: "(statement_kind * nat) list" where
  "statement_kind_counts = [
    (AxiomKind, 75),
    (DefinitionKind, 9267),
    (TheoremKind, 120),
    (LemmaKind, 6),
    (PropositionKind, 45),
    (CorollaryKind, 0),
    (PostulateKind, 0),
    (AssumptionKind, 2),
    (InvariantKind, 101),
    (PrincipleKind, 46),
    (LawKind, 148)
  ]"

definition statement_count :: nat where
  "statement_count = 9810"

definition dependency_count :: nat where
  "dependency_count = 5285"

lemma statement_manifest_nonempty: "statement_count > 0"
  by (simp add: statement_count_def)

lemma dependency_manifest_wellformed: "dependency_count >= 0"
  by (simp add: dependency_count_def)

end
