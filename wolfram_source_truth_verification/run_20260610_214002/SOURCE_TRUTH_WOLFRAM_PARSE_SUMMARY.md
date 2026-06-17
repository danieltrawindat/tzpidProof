# TZPID Source-Truth Wolfram Parse Check

This check reads source-truth Wolfram blocks from `wolfram_form.audit.blocks[]`, accepting `wolfram_input` and reviewed `holdform_inputform` entries.
Expressions are parsed under `HoldComplete`; this verifies Wolfram Language syntax without requiring domain-specific symbols to evaluate numerically.

## Summary

- IDs checked: `10271`
- Blocks checked: `12177`

## Status Counts

- `wolfram_source_truth_parse_pass`: `12177`

## ID Counts By Status

- `wolfram_source_truth_parse_pass`: `10271`