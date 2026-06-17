# Lean/Rocq Export Lane

These files are exported scaffolds/mirrors for portability and independent-check lanes. Isabelle/HOL remains the primary checked proof lane for this release unless a Lean or Rocq compiler artifact is present beside the source.

## Included Files

- [.TZPIDAllIDs.aux](../exports/.TZPIDAllIDs.aux)
- [TZPIDAllIDs.glob](../exports/TZPIDAllIDs.glob)
- [TZPIDAllIDs.lean](../exports/TZPIDAllIDs.lean)
- [TZPIDAllIDs.v](../exports/TZPIDAllIDs.v)
- [TZPIDAllIDs.vo](../exports/TZPIDAllIDs.vo)
- [TZPIDAllIDs.vok](../exports/TZPIDAllIDs.vok)
- [TZPIDAllIDs.vos](../exports/TZPIDAllIDs.vos)
- [all_ids_export_summary.json](../exports/all_ids_export_summary.json)

## Status Convention

- `.lean` and `.v` files are source-level exports.
- `.vo`, `.vos`, `.vok`, and `.glob` files are Rocq/Coq compiler side artifacts when present.
- The export summary JSON records the source registry and generation context.
