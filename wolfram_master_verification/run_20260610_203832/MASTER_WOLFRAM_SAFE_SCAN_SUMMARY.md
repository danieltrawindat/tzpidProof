# Full Master Wolfram Safe Scan

- Generated UTC: 2026-06-10T20:56:27.5092355Z
- Source master copy: `D:\TZPIDProof\wolfram_master_verification\run_20260610_203832\master_copy\TZPID_ALL_IDS_CANONICAL_EQUATION_MASTER_with_export.csv`
- Source ladder copy: `D:\TZPIDProof\wolfram_master_verification\run_20260610_203832\master_copy\TZPID_ALL_IDS_REASSEMBLED_PROOF_LADDER_WITH_EQUATIONS.md`
- Rows processed: `10271`
- Rows with equations: `10271`
- Equation segments processed: `11757`
- Engine: `WolframScript`
- GPU detected: `NVIDIA GeForce RTX 4060 Laptop GPU`
- GPU note: symbolic/textual Wolfram scan was not GPU-accelerated; GPU is reserved for numeric array/HDF5 diagnostics.

## Status Counts

| Status | Count |
|---|---:|
| `classified_elementary_latex_candidate` | 3397 |
| `classified_logical_latex_needs_hol_translation` | 769 |
| `classified_operator_latex_needs_semantic_translation` | 863 |
| `classified_relation_latex_candidate` | 4578 |
| `classified_symbolic_latex_candidate` | 2119 |
| `wolfram_direct_numeric_fail` | 1 |
| `wolfram_direct_numeric_pass` | 5 |
| `wolfram_numeric_expression_computed` | 21 |
| `wolfram_numeric_parse_error` | 4 |

## Class Counts

| Class | Count |
|---|---:|
| `elementary_latex` | 3397 |
| `logical_latex` | 769 |
| `numeric_ascii` | 31 |
| `operator_latex` | 863 |
| `relation_latex` | 4578 |
| `symbolic_latex` | 2119 |

## Claim Boundary

This is a full-master Wolfram-safe scan, not a claim that Wolfram proved all 10,271 physics entries. Every equation segment was processed. Direct proof/evaluation statuses are used only for Wolfram-safe numeric relations. LaTeX-heavy operator, logical, elementary, relation, and symbolic formulas are classified into follow-up lanes for semantic translation, Isabelle/HOL formalization, or dedicated Wolfram notebooks.

## Key Result

The master copy contains `10,271` equation-bearing rows split into `11,757` segments. The scan completed over all segments without requiring mutation of the source master.

## Numeric Exceptions

The single `wolfram_direct_numeric_fail` is ID8657, segment `1.185=32/27`. This is a precision/rounding issue rather than a failed conceptual identity: `32/27 = 1.185185...`, so exact equality to the rounded decimal `1.185` is false. The four `wolfram_numeric_parse_error` rows are malformed numeric fragments (`^2`, `(-+++)`, `=2/36`, `=(3-5)`) and should be routed to source cleanup rather than treated as mathematical counterexamples.
