# TZPID Isabelle Theory Declaration Inventory

Generated from **155** `.thy` files across **2** source roots.

## Output Files

- `TZPID_ISABELLE_FULL_DECLARATION_INVENTORY.csv` (3662 rows)
- `TZPID_ISABELLE_THEORIES.csv` (155 rows)
- `TZPID_ISABELLE_THEOREMS_LEMMAS.csv` (1390 rows)
- `TZPID_ISABELLE_HYPOTHESES_LOCALES_ASSUMES.csv` (773 rows)
- `TZPID_ISABELLE_AXIOMS_CONSTANTS.csv` (0 rows)
- `TZPID_ISABELLE_OPERATORS_AND_CARRIERS.csv` (725 rows)
- `TZPID_ISABELLE_THEORY_DEPENDENCIES.csv` (155 rows)
- `TZPID_ISABELLE_CONSTANTS_DEFINITIONS_TYPES.csv` (1189 rows)
- `TZPID_ISABELLE_THEORY_LIST.md` (155 theories)

## Counts by Declaration Kind

| Kind | Count |
| --- | ---: |
| definition | 1098 |
| theorem | 915 |
| assumes | 731 |
| lemma | 475 |
| imports | 155 |
| theory | 155 |
| locale | 42 |
| datatype | 37 |
| type_synonym | 29 |
| fun | 21 |
| record | 4 |

## Counts by Semantic Subtype

| Subtype | Count |
| --- | ---: |
| proof_statement | 1161 |
| hypothesis_or_assumption | 731 |
| operator_or_carrier | 717 |
| constant_or_definition | 402 |
| formal_contract | 221 |
| theory | 155 |
| theory_dependency | 155 |
| hypothesis_context | 42 |
| datatype | 37 |
| type_synonym | 29 |
| axiom_contract | 8 |
| record | 4 |

## Operator-like / Carrier Declarations

- Operator-like declarations: **725**

## Source Roots

| Source root | Declarations |
| --- | ---: |
| `D:\00_Engine\AI_Workspaces\OpenAI2\new_zenodo_spines\isabelle` | 297 |
| `D:\TZPIDProof\tzpid_proof\isabelle_tzpid` | 3365 |

## Largest Theories by Declaration Count

| Theory | Declarations |
| --- | ---: |
| `TZPID_Theorem_Semantic_Batch003` | 66 |
| `TZPID_HypersphericalBesselResidualBridge_Phase2_Model` | 59 |
| `TZPID_Theorem_Semantic_Batch001` | 56 |
| `TZPID_EdgeCase_Strengthening` | 53 |
| `TZPID_Quantum_Open_System_Model` | 51 |
| `TZPID_Theorem_Semantic_Batch002` | 50 |
| `TZPID_Operator_Spectral_Model` | 45 |
| `TZPID_Theorem_Semantic_Batch005_Topology_Vector` | 45 |
| `TZPID_Phase2_Semantic_Translation` | 42 |
| `TZPID_Meta_Foundation_Model` | 40 |
| `TZPID_Theorem_Semantic_Batch006_Operator_Spectral` | 40 |
| `TZPID_PhysicalProofArchitecture` | 38 |
| `TZPID_Geometry_Manifold_Model` | 37 |
| `TZPID_Einstein_Computational_Checks` | 36 |
| `TZPID_SpartanStandingWave_Expansion` | 36 |
| `TZPID_Theorem_Semantic_Batch013_Topology_Category_Followup` | 36 |
| `TZPID_Einstein_Focus` | 35 |
| `TZPID_GeometryManifold_Carriers` | 35 |
| `TZPID_GyroWave_Sky` | 35 |
| `TZPID_NestedHypersphere_Typed_Projection` | 35 |
| `TZPID_Theorem_Semantic_Batch014_Dynamics_Stability_Followup` | 35 |
| `TZPID_MasterBatch003_Carriers` | 34 |
| `TZPID_PaperXV_TRAWIN_Closure` | 34 |
| `TZPID_PaperXVII_wa_Derivation` | 34 |
| `TZPID_Theorem_Semantic_Batch012_Operator_Spectral_Followup` | 34 |
| `TZPID_AA_Spines_Computational_Checks` | 33 |
| `TZPID_Magnetic_Torsion_Model` | 33 |
| `TZPID_NestedHypersphere_S3_Spectrum` | 32 |
| `TZPID_TRAWIN_Composition_GoldSpine` | 32 |
| `TZPID_FifthFlip_CrystalScaleInvariance` | 31 |

## Notes

- Explicit raw Isabelle `consts`/`axiomatization` declarations are absent in this scan; practical constants live as `definition`, `fun`, `datatype`, `record`, and `type_synonym` entries in `TZPID_ISABELLE_CONSTANTS_DEFINITIONS_TYPES.csv`.
- `hypotheses` are represented by Isabelle `locale`, `assumes`, and `fixes` declarations.
- `operators` are inferred from declarations whose names or excerpts contain operator/carrier terms such as `operator`, `composition`, `tensor`, `curl`, `flux`, `winding`, `holonomy`, `bessel`, `phase`, or `trawin`.
- The full declaration inventory CSV is the authoritative list; this Markdown file is a summary for review.
