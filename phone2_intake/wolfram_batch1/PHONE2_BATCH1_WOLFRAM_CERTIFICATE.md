# Phone2 Batch 1 Wolfram Certificate

- Scope: `ID10872` through `ID11121`
- Total equations checked: `250`
- Current status source: synchronized master `wolfram_status` column

## Effective Status After All Rescue Passes

| Status | Count | Meaning |
|---|---:|---|
| `wolfram_equation_parse_verified` | 127 | Original generated Wolfram candidate parses under HoldComplete. |
| `wolfram_cleanup_fragment_carrier_verified` | 82 | Needs-cleanup row preserved as a parseable fragment carrier. |
| `wolfram_rescue_equation_parse_verified` | 14 | Parse-error rescue produced an equation-level Wolfram parse. |
| `wolfram_fragment_carrier_verified` | 9 | Fragment carrier parses for an incomplete source row. |
| `wolfram_cleanup_equation_parse_verified` | 9 | Needs-cleanup rescue produced an equation-level Wolfram parse. |
| `wolfram_symbolic_carrier_verified` | 8 | Symbolic carrier parses; semantic equation cleanup still needed. |
| `wolfram_cleanup_expression_parse_verified` | 1 | Needs-cleanup rescue produced a parseable expression, but not yet a full equation contract. |

## Rollup

- Equation-level parse verified: `150`
- Expression-level parse verified: `1`
- Carrier-preserved fragments/symbolic rows: `99`
- Raw `wolfram_parse_error` remaining: `0`
- Raw `wolfram_needs_cleanup` remaining: `0`

## Interpretation

This is an equation-specific Wolfram syntax certificate. Parse verification means the candidate is syntactically valid Wolfram under `HoldComplete`; it is not a semantic proof. Carrier verification preserves source material in a Wolfram-readable structure when the extracted row is not a complete equation.

## Artifacts

- `phone2_batch1_wolfram_candidates.json`
- `phone2_batch1_wolfram_certificate.wls`
- `phone2_batch1_wolfram_certificate_results.json`
- `phone2_batch1_wolfram_certificate_results.csv`
- `phone2_batch1_parse_error_rescue_candidates.json`
- `phone2_batch1_parse_error_rescue.wls`
- `phone2_batch1_parse_error_rescue_results.json`
- `phone2_batch1_parse_error_rescue_results.csv`
- `phone2_batch1_needs_cleanup_rescue_candidates.json`
- `phone2_batch1_needs_cleanup_rescue.wls`
- `phone2_batch1_needs_cleanup_rescue_results.json`
- `phone2_batch1_needs_cleanup_rescue_results.csv`
- `PHONE2_BATCH1_WOLFRAM_STATUS_FOLD_MANIFEST.json`
- `PHONE2_BATCH1_PARSE_ERROR_RESCUE_FOLD_MANIFEST.json`
- `PHONE2_BATCH1_NEEDS_CLEANUP_RESCUE_FOLD_MANIFEST.json`

## Next Cleanup Priority

1. Promote the `150` equation-level parse-verified rows toward semantic review and Isabelle obligation generation.
2. Inspect the single expression-level row and decide whether it should become an equation or remain an expression carrier.
3. Reconstruct the carrier rows from neighboring source context before treating them as formal equations.
