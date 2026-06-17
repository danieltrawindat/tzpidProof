# Papers XI-XV HOL/Wolfram Verification Certificate

Generated: 2026-06-16

Creator: Daniel Alexander Trawin  
ORCID: https://orcid.org/0009-0001-4630-3715

## Scope

This certificate consolidates the formal and computational verification layer for Papers XI-XV:

- Paper XI: sound-before-light / BAO node carriers
- Paper XII: Spartan Dawn model-comparison carriers
- Paper XIII: S3/S4/S5 geometry carriers
- Paper XIV: nested-shell BAO carriers
- Paper XV: TRAWIN operator-closure carriers

The layer covers 135 registered IDs:

`ID11536` through `ID11670`

## Isabelle/HOL Certificate

Theory:

`D:\TZPIDProof\tzpid_proof\isabelle_tzpid\TZPID_PapersXI_XV_VerificationSuite.thy`

Imported through:

`D:\TZPIDProof\tzpid_proof\isabelle_tzpid\ROOT`

The theory imports the five paper theories and proves cross-paper compatibility:

- Paper XI BAO period aligns with Paper XIV BAO period.
- Paper XI/XIV BAO spacing divided by curvature mode spacing yields the Paper XIV modes-per-wiggle ratio.
- Paper XIII S3/S4/S5 degeneracies align with Paper XIV amplitude-envelope degeneracy carriers.
- Paper XIII S3 breathing law aligns with the Paper XV TRAWIN breathing closure.
- Paper XIII continuity balance aligns with the Paper XV vacuum fixed-point closure.
- Paper XV operator alphabet is sixfold.
- The combined registered-ID lane is nonempty and spans `ID11536` to `ID11670` with 135 IDs.

Build command:

```powershell
D:\Isabelle2025\Isabelle2025-2\bin\isabelle build -D D:\TZPIDProof\tzpid_proof\isabelle_tzpid
```

Status:

`build clean`

## Wolfram Certificate

Script:

`D:\TZPIDProof\peer_review\papers_xi_xv_verification\wolfram\papers_xi_xv_verification.wls`

Result JSON:

`D:\TZPIDProof\peer_review\papers_xi_xv_verification\wolfram\papers_xi_xv_verification_results.json`

Run command:

```powershell
cd D:\TZPIDProof\peer_review\papers_xi_xv_verification\wolfram
wolframscript -file papers_xi_xv_verification.wls
```

Result:

- Checks: `15`
- Passed: `15`
- Failed: `0`

The Wolfram checks cover BAO node arithmetic, BAO period alignment, modes-per-wiggle ratio, direct-shell inverse, beat-epsilon scale setting, Paper XII AIC arithmetic, Paper XIII dimension counter, plus-ell cascade, S3/S4/S5 degeneracy prefixes, breathing-volume closure, vacuum-continuity fixed point, far-field free-wave limit, and TRAWIN operator alphabet cardinality.

## Boundary

This is a certificate for the algebraic and symbolic carrier layer. It proves that the registered equations from Papers XI-XV are mutually compatible at the formal-carrier level and that the selected numeric/symbolic checks pass in Wolfram. Physical interpretation, observational adequacy, and the full registry-wide TRAWIN pass remain paper-facing synthesis and external empirical obligations.
