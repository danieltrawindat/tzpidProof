# TZPID Edge-Case Strengthening Certificate

Generated UTC: 2026-06-11T03:17:00Z

## Scope

This certificate records the first curated edge-case strengthening pass.
It keeps shell/code artifacts quarantined and promotes only compact mathematical candidates into a proof-facing batch.

## Artifacts

- Curated batch: `D:\TZPIDProof\edge_case_equations\TZPID_EDGE_CASE_STRENGTHENING_BATCH.csv`
- Curated report: `D:\TZPIDProof\edge_case_equations\TZPID_EDGE_CASE_STRENGTHENING_BATCH.md`
- Quarantine CSV: `D:\TZPIDProof\edge_case_equations\TZPID_SHELL_CODE_ARTIFACT_QUARANTINE.csv`
- Quarantine report: `D:\TZPIDProof\edge_case_equations\TZPID_SHELL_CODE_ARTIFACT_QUARANTINE.md`
- Isabelle theory: `D:\TZPIDProof\tzpid_proof\isabelle_tzpid\TZPID_EdgeCase_Strengthening.thy`
- Wolfram script: `D:\TZPIDProof\edge_case_equations\wolfram\edge_case_strengthening_check.wls`
- Wolfram results: `D:\TZPIDProof\edge_case_equations\wolfram\edge_case_strengthening_results.json`

## Results

- Curated strengthening rows: `20`
- Quarantined shell/code artifacts: `21`
- Wolfram checks: `20 / 20 pass`
- Isabelle build: `passed`

## Isabelle Command

```powershell
D:\Isabelle2025\Isabelle2025-2\bin\isabelle build -D D:\TZPIDProof\tzpid_proof\isabelle_tzpid
```

## Wolfram Command

```powershell
wolframscript -file D:\TZPIDProof\edge_case_equations\wolfram\edge_case_strengthening_check.wls
```

## Interpretation

The quarantined rows are not treated as equation gaps. They remain provenance-only unless a real mathematical expression is manually extracted from them.

The curated rows strengthen the proof package at the high-risk edges: cosmological density scaling, vacuum cutoff, Alfven/gyromagnetic spectral modes, half-integer winding, Bessel zeros, Einstein recovery, Friedmann components, Poisson closure, Kuramoto threshold, helicity, Helmholtz boundary conditions, spherical harmonics, Elsasser criticality, pressure thresholds, exact ratio gates, KK residuals, and density-to-Poisson closure.
