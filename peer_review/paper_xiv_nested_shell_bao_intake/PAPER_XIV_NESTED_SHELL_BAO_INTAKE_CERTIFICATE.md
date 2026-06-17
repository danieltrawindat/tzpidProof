# Paper XIV Nested Shell BAO Intake Certificate

Generated UTC: 2026-06-17T00:01:24+00:00

Creator: Daniel Alexander Trawin  
ORCID: https://orcid.org/0009-0001-4630-3715

## Source

- `D:\TZPIDProof\peer_review\TZPID_Papers_XI_XIX\Paper_XIV_Nested_Shell_BAO.tex`

## Minted IDs

This intake minted 27 missing Paper XIV nested-shell / BAO equations:

`ID11616` through `ID11642`

The entries cover:

- BAO phase-locking, acoustic node, and BAO wiggle period carriers
- projected curved-shell mode ladders for S3/S4/S5
- high-ell asymptotic spacing and unit-radius mode spacing
- observed BAO spacing, curvature-radius bound, and null direct-shell imprint test
- modes-per-BAO-wiggle separation between Hubble-scale curvature and the BAO ruler
- direct-shell exclusion radius and nested-shell beat-radius mechanism
- beat epsilon estimate near `3.7e-4`
- S3/S4/S5 degeneracy prefixes and asymptotic amplitude weighting
- falsifiable distinction between spacing imprint and amplitude-envelope imprint

## Registry Integration

- Master CSV rows: `11,128`
- ID-system rows: `11,128`
- Proof-clean master rows: `11,080`
- Quarantined shell/code artifact rows excluded from proof-clean view: `48`
- New per-ID source-truth JSON/TeX folders: `27`
- New source-truth folders: `D:\TZPIDProof\tzp_id\ID11616` through `D:\TZPIDProof\tzp_id\ID11642`

## Isabelle/HOL Certificate

Theory:

`D:\TZPIDProof\tzpid_proof\isabelle_tzpid\TZPID_PaperXIV_NestedShell_BAO.thy`

Imported through:

`D:\TZPIDProof\tzpid_proof\isabelle_tzpid\ROOT`

Build command:

```powershell
D:\Isabelle2025\Isabelle2025-2\bin\isabelle build -D D:\TZPIDProof\tzpid_proof\isabelle_tzpid
```

Status:

`build clean`

## Boundary

These entries formalize Paper XIV's BAO spacing, mode-spacing, beat-epsilon, direct-shell exclusion, and degeneracy-envelope carriers. The HOL lane checks the algebraic contracts for the registered equations. Claims that an upper shell physically imprints the BAO ruler remain framework synthesis and are carried as source-truth obligations rather than asserted as established observational physics.
