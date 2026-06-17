# TZPID Wolfram Numeric/Symbolic Representation Report

Generated for the proof package copy at `D:\TZPIDProof`.

## Result

- Source-truth IDs represented: `10,271 / 10,271`
- Representation blocks generated: `11,740`
- Wolfram representation parse pass: `11,740 / 11,740`
- IDs with parse-verified representation status: `10,271 / 10,271`
- Blocks with extracted numeric atoms: `7,149`
- Total extracted symbolic tokens: `71,856`
- Optional best-effort Wolfram candidate expressions parse-passing: `2,064`
- Optional candidates downgraded or not attempted: `9,676`
- Candidate parse failures left active: `0`

## Representation Model

Each ID now has a `wolfram_representation` object in its source-truth JSON. Each block contains:

- `latex`: the source canonical equation text.
- `numeric_atoms`: extracted numbers, fractions, and decimal atoms.
- `symbolic_tokens`: extracted symbols and symbolic roles.
- `wolfram_input`: a WolframScript-validated representation wrapper:

```wolfram
HoldForm[
  TZPIDWolframRepresentation[
    "IDxxxx",
    block_index,
    <|"kind" -> ..., "latex" -> ..., "numericAtoms" -> ..., "symbolicTokens" -> ...|>
  ]
]
```

Where the equation was simple enough to translate safely, the block also carries `candidate_wolfram_input`. Candidate expressions were validated with WolframScript. Any heuristic candidate that did not parse was downgraded into symbolic-token representation, with the rejected string retained under `rejected_candidate_wolfram_input` for audit.

## Artifacts

- Build report: `D:\TZPIDProof\wolfram_source_truth_verification\build_wolfram_representations_report_20260610_215538.json`
- Final validation summary: `D:\TZPIDProof\wolfram_source_truth_verification\representation_run_20260610_215643\WOLFRAM_REPRESENTATION_VALIDATION_SUMMARY.md`
- Final validation results: `D:\TZPIDProof\wolfram_source_truth_verification\representation_run_20260610_215643\wolfram_representation_validation_results.json`
- Final validation zip: `D:\TZPIDProof\wolfram_source_truth_verification\TZPID_Wolfram_Representation_Validation_representation_run_20260610_215643.zip`
- Fold report: `D:\TZPIDProof\wolfram_source_truth_verification\FOLD_WOLFRAM_REPRESENTATION_STATUS_REPORT.json`

## Interpretation

This is a complete Wolfram-readable numeric/symbolic representation layer, not a claim that every ID has a domain-specific numerical proof. It gives every entry a validated Wolfram carrier for its numerical and symbolic content, and it identifies the subset that can already be promoted into stronger semantic or computational Wolfram checks.
