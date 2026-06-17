---
title: Paper XVII w(a) Derivation Intake Certificate
creator: Daniel Alexander Trawin
orcid: https://orcid.org/0009-0001-4630-3715
generated_utc: 2026-06-17T04:22:25+00:00
source: D:\TZPIDProof\peer_review\TZPID_Papers_XI_XIX\Paper_XVII_wa_Derivation.tex
---

# Paper XVII w(a) Derivation Intake Certificate

This certificate records the source-truth registry intake for Paper XVII, "Deriving the Dark-Energy Equation of State." The intake adds the missing formal equations, diagnostic definitions, framework predictions, and theorem carriers from the TeX source into the TZPIDProof registry.

## Minted Registry Range

| Field | Value |
|---|---:|
| Previous max ID | ID11692 |
| New ID range | ID11693-ID11728 |
| New entries | 36 |
| Master rows after intake | 11,214 |
| ID-system rows after intake | 11,214 |
| Per-ID folders after intake | 11,214 |
| Proof-clean master rows | 11,166 |
| Isabelle theories after intake | 127 |

## Registered Content

The intake covers the Paper XVII derivation lane:

- exact equation-of-state identity;
- naive inverse-quartic branch and radiation-like value;
- pure breathing-vacuum branch and cosmological-constant value;
- threshold vacuum-to-matter handoff law;
- enclosure vacuum-energy law and breathing radius scaling;
- quartic logarithmic slope;
- threshold response conditions;
- effective EoS, `w0`, and `wa` formulas;
- order-unity slope and thawing-quintessence comparison;
- negative-foundation damping, matter-deficit energy, and stable sink potential;
- matter-stability sign theorem and quintom-B inequalities;
- crossing-redshift diagnostics;
- Gauss-Bonnet normalization on the Hopf base;
- Hopf charge selector and deficit half-coupling;
- coupling bracket, candidate coupling, DESI diagnostic values, and precision boundary.

## Source-Truth Outputs

Each minted ID has a source-truth JSON and TeX companion under:

```text
D:\TZPIDProof\tzp_id\ID11693\
...
D:\TZPIDProof\tzp_id\ID11728\
```

The intake report is:

```text
D:\TZPIDProof\peer_review\paper_xvii_wa_derivation_intake\PAPER_XVII_WA_DERIVATION_INTAKE_REPORT.json
```

## Isabelle/HOL Carrier

The formal carrier theory is:

```text
D:\TZPIDProof\tzpid_proof\isabelle_tzpid\TZPID_PaperXVII_wa_Derivation.thy
```

It is imported through:

```text
D:\TZPIDProof\tzpid_proof\isabelle_tzpid\ROOT
```

The theory verifies the algebraic carrier facts needed for Paper XVII:

- inverse-quartic branch gives `w = 1/3`;
- constant-density branch gives `w = -1`;
- `w0` is the threshold `weff` evaluated at `x0`;
- negative `kappa` and positive `x0` imply negative `wa`;
- negative `kappa` and `x0 < 1` imply `w0 > -1`;
- zero threshold response gives zero creation rate;
- mass-deficit energy is non-positive for non-negative mass and light-speed parameter;
- stable sink potential is non-negative;
- Gauss-Bonnet normalization reduces to `2*pi`;
- Hopf charge selector and S3 coupling candidate unfold as registered.

## Verification

The Isabelle session was rebuilt after intake with:

```powershell
D:\Isabelle2025\Isabelle2025-2\bin\isabelle build -D D:\TZPIDProof\tzpid_proof\isabelle_tzpid
```

Build result: passed.

The shell-artifact quarantine pass was refreshed after intake. It retained 48 shell/code-like signal rows outside the proof-facing clean master and produced:

```text
D:\TZPIDProof\TZPID_ALL_IDS_CANONICAL_EQUATION_MASTER_PROOF_CLEAN_NO_SHELL_SIGNALS.csv
```

Proof-clean row count after Paper XVII: 11,166.
