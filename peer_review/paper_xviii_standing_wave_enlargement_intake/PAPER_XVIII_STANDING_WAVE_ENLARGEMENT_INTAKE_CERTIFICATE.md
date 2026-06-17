---
title: Paper XVIII Standing-Wave Enlargement Intake Certificate
creator: Daniel Alexander Trawin
orcid: https://orcid.org/0009-0001-4630-3715
generated_utc: 2026-06-17T04:43:53+00:00
source: D:\00_Engine\AI_Workspaces\OpenAI2\TZPID_Papers_XI_XIX\Paper_XVIII_Standing_Wave_Enlargement.tex
---

# Paper XVIII Standing-Wave Enlargement Intake Certificate

This certificate records the source-truth registry intake for Paper XVIII, "Standing-Wave Enlargement by Hyperspherical Breathing." The intake adds the missing formal equations, theorem carriers, diagnostic conditions, and framework predictions from the TeX source into the TZPIDProof registry.

## Minted Registry Range

| Field | Value |
|---|---:|
| Previous max ID | ID11728 |
| New ID range | ID11729-ID11751 |
| New entries | 23 |
| Master rows after intake | 11,237 |
| ID-system rows after intake | 11,237 |
| Per-ID folders after intake | 11,237 |
| Proof-clean master rows | 11,189 |
| Isabelle theories after intake | 128 |

## Registered Content

The intake covers the Paper XVIII standing-wave enlargement lane:

- comoving standing-node principle;
- photon-baryon sound speed and subluminal bound;
- frozen acoustic ruler carrier;
- breathing Hubble rate;
- proper node spacing and growth law;
- Hubble-radius condition and superluminal recession bookkeeping;
- hyperspherical boundary condition and comoving node freeze;
- no-signaling proposition;
- inflationary radius law and e-fold count;
- projection slice-element term;
- projection-as-dark-energy reading;
- rigid nesting limit;
- breathing-pressure and `F(a)` identifications;
- dimensionless shape preservation;
- slice-motion prediction for `w(a)`.

## Source-Truth Outputs

Each minted ID has a source-truth JSON and TeX companion under:

```text
D:\TZPIDProof\tzp_id\ID11729\
...
D:\TZPIDProof\tzp_id\ID11751\
```

The intake report is:

```text
D:\TZPIDProof\peer_review\paper_xviii_standing_wave_enlargement_intake\PAPER_XVIII_STANDING_WAVE_ENLARGEMENT_INTAKE_REPORT.json
```

## Isabelle/HOL Carrier

The formal carrier theory is:

```text
D:\TZPIDProof\tzpid_proof\isabelle_tzpid\TZPID_PaperXVIII_StandingWaveEnlargement.thy
```

It is imported through:

```text
D:\TZPIDProof\tzpid_proof\isabelle_tzpid\ROOT
```

The theory verifies the algebraic carrier facts needed for Paper XVIII:

- node spacing unfolds as `R * dchi`;
- node growth follows the fractional breathing-rate carrier;
- the super-Hubble condition unfolds to `lambda > c/H`;
- positive Hubble rate plus `D > c/H` gives recession speed above `c`;
- exponential radius ratio gives `exp N`;
- rigid slice motion makes the projection term vanish;
- rigid projection leaves effective expansion unchanged;
- dimensionless node shape is preserved when `lambda = R*dchi`;
- the registered ID list is nonempty.

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

Proof-clean row count after Paper XVIII: 11,189.
