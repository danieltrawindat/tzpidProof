# TZPID Wolfram Numeric/Symbolic Representation Validation

This check validates the per-ID `wolfram_representation` layer generated from source-truth equations.
Each representation block contains numeric atoms, symbolic tokens, and an optional best-effort Wolfram candidate expression.

## Summary

- IDs checked: `10271`
- Blocks checked: `11740`

## Representation Parse Status

- `wolfram_representation_parse_pass`: `11740`

## Candidate Parse Status

- `candidate_parse_pass`: `2203`
- `candidate_not_attempted`: `8477`
- `candidate_parse_error`: `1060`

## Candidate Evaluation Status

- `symbolic_held`: `2201`
- `not_attempted`: `8477`
- `not_evaluable_parse_error`: `1060`
- `not_evaluable`: `2`