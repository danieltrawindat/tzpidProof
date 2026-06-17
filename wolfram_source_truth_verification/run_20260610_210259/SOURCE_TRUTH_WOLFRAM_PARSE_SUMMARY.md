# TZPID Source-Truth Wolfram Parse Check

This check reads `wolfram_form.audit.blocks[].wolfram_input` from the per-ID source-truth JSON files.
Expressions are parsed under `HoldComplete`; this verifies Wolfram Language syntax without requiring domain-specific symbols to evaluate numerically.

## Summary

- IDs checked: `995`
- Blocks checked: `2775`

## Status Counts

- `wolfram_source_truth_parse_pass`: `2775`

## ID Counts By Status

- `wolfram_source_truth_parse_pass`: `995`