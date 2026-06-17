# Phone2 ID-Ready Registration Plan

This plan stages the `D:\Phone2` equation extraction for controlled registry promotion. It does not mint IDs and does not modify the master registry.

## Current Anchor

- Master rows seen: `10357`
- Highest existing master ID seen: `ID10871`
- Raw Phone2 equation candidates: `2341`
- Unique staged candidates: `2288`
- Phone2 internal duplicates removed: `51`

## Readiness

| Status | Count | Meaning |
|---|---:|---|
| review | 2242 | Likely usable, but needs boundary cleanup or citation/prose separation. |
| id_ready | 29 | Compact mathematical candidate with clear equation signal. |
| quarantine | 17 | Artifact/comment/weak candidate; do not mint without manual rescue. |

## Domain Families

| Domain | Count |
|---|---:|
| quantum_entanglement | 588 |
| general_math | 462 |
| category_type_theory | 445 |
| optimization_computation | 365 |
| geometry_topology | 196 |
| protocol_systems | 136 |
| field_topology_mhd | 50 |
| signal_wave | 35 |
| gravity_cosmology | 11 |

## Promotion Rule

1. Promote `id_ready` + `new_or_nonexact` rows first.
2. Review long mixed prose/equation rows by splitting them into atomic equations before minting.
3. Keep `quarantine` rows out of the registry unless a human intentionally rescues them.
4. Attach semantic context from `semantic_kind` / `semantic_context` during dictionary and encyclopedia creation.
5. Use `wolfram_form_hint` as a starting point only; parse-clean Wolfram status should be verified before marking a row computationally certified.

## Generated Files

- `PHONE2_ID_READY_EQUATION_QUEUE.csv`
- `PHONE2_REGISTRATION_BATCHES.csv`
- `PHONE2_REGISTRATION_QUEUE_SUMMARY.json`

## Suggested Next Batch

Start with batch 1 from `PHONE2_REGISTRATION_BATCHES.csv`; it sorts high-score, ID-ready, nonexact candidates first.
