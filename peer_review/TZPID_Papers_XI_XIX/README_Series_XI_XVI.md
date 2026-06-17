---
creator: Daniel Alexander Trawin
orcid: https://orcid.org/0009-0001-4630-3715
generated: 2026-06-16
---

# TZPID Paper Series XI–XVI

A six-paper formal set extending the established TZPID paper format (I–VIII), covering the verified results from the
Spartan Dawn line of work. Each `.tex` is standalone (self-contained `thebibliography`, compiles with `pdflatex`).

| # | File | Core verified result |
|---|---|---|
| **XI** | `Paper_XI_Sound_Before_Light.tex` | Sound horizon from first principles: `r_s(z*) = 144.2 Mpc` (Planck 144.4, 0.1%). The BAO ruler is frozen sound, set before light. |
| **XII** | `Paper_XII_Spartan_Dawn_Test.tex` | 4-model χ² fit to DESI DR2 BAO + Planck θ* + Pantheon+: static closed cosmos rejected, breathing (evolving w) favored Δχ²≈−9, hypersphere permitted not forced. |
| **XIII** | `Paper_XIII_S3_S4_S5_Geometry.tex` | Exact S³/S⁴/S⁵ geometry; nesting rule `λ_ℓ(Sⁿ)=λ_ℓ(Sⁿ⁻¹)+ℓ`; `3:4:5` triad; breathing dimension-counter `V̇/V=nH → n=3`. |
| **XIV** | `Paper_XIV_Nested_Shell_BAO.tex` | Higher shells cannot shift the BAO (~2700× too fine); one falsifiable beat at `ε≈3.7×10⁻⁴`; dimension fingerprint is amplitude `~ℓ^{n−1}`. |
| **XV** | `Paper_XV_TRAWIN_Closure.tex` | TRAWIN composition `C_R=N∘I∘W∘A∘R∘T`; type-tagged pass over 10,356 equations; 5 closure identities verified, tied to Isabelle carriers. |
| **XVI** | `Paper_XVI_Volumetric_Buoyancy.tex` | Three-phase occupancy / Elsasser model; two falsifiable threads isolated; honest limits (Λ symbol collision, R⁻⁴ radiation-like, dark-matter bars unmet). |

## Build

```
pdflatex Paper_XI_Sound_Before_Light.tex   # run twice for table of contents / refs
```

All six confirmed compiling to 3-page PDFs (XI is 3pp). Status of claims is demarcated in each paper: verified results vs.
open obligations are stated explicitly, consistent with the proof-pipeline README.

## Lineage

Built on the source files `TZPID_SPARTAN_DAWN_CMB_BAO_SNE_TEST.md`, `TZPID_S3_S4_S5_NESTED_SPHERES.md`,
`TZPID_BAO_NESTED_SHELL_PROJECTION.md`, `TZPID_TRAWIN_OPERATOR_PASS.csv`, `TZPID_TRAWIN_COMPOSITION_GOLDSPINE_CERTIFICATE.md`,
and `vp.txt`; registry master `TZPID_ALL_IDS_CANONICAL_EQUATION_MASTER_with_export.csv`. Format follows
`trawin_hyperspherical_s4_s5_bessel_breathing.tex`.
