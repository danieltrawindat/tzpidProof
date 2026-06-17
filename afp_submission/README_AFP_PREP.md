# AFP Submission Preparation: TZPID Derivation Order

Source checked: <https://isa-afp.org/submission/> on 2026-06-10.

## Submission Record

- Submitted URL: <https://isa-afp.org/webapp/submission?id=2026-06-11_09-19-53_968>
- Previous draft/submission URL: <https://isa-afp.org/webapp/submission?id=2026-06-10_19-21-17_411>
- AFP server build status: successfully built on 2026-06-11 at 05:23 America/New_York.
- Submitted/recorded date: 2026-06-10
- Submitted entry short name: `TZPID_Derivation_Order`
- Submitted artifact: `D:/TZPIDProof/afp_submission/TZPID_Derivation_Order_AFP_candidate.zip`
- Local preflight: passed with Isabelle2025-2 using AFP-style document build.

## Recommended First AFP Entry

Submit the focused formal artifact first:

- Entry directory: `TZPID_Derivation_Order`
- Session name: `TZPID_Derivation_Order`
- Formal contribution: a 753-edge derivation-order certificate for the 10,271-node proof ladder.
- DOI/source archive: <https://doi.org/10.5281/zenodo.20632000>

This is a better first AFP submission than the entire TZPIDProof archive because AFP entries are proof developments, not full research repositories. The DAG certificate is compact, reproducible, and has a precise theorem statement.

## AFP Requirements Mapped To Our Entry

- No `sorry` or `back`: satisfied in the staged entry.
- No `sledgehammer` or `smt_oracle` commands: satisfied in the staged entry.
- No `nitpick`, `quickcheck`, or `nunchaku` calls without `expect`: not used.
- ROOT file has one session in chapter `AFP`: satisfied.
- Session timeout divisible by 300: set to `timeout = 300`.
- Produces PDF document: staged with `document/root.tex`.
- Cites sources: root document cites the Zenodo DOI and Isabelle/HOL book.
- All theory files in the submission are included in the session: satisfied.

## Local Build Command

From PowerShell:

```powershell
D:\Isabelle2025\Isabelle2025-2\bin\isabelle build -v -o browser_info -o "document=pdf" -o "document_variants=document:outline=/proof,/ML" -D D:\TZPIDProof\afp_submission\TZPID_Derivation_Order
```

## Submission Form Fields Draft

Title:

```text
A Derivation-Order Certificate for a 10,271-Node Registry
```

Author:

```text
Daniel Alexander Trawin
```

Web abstract:

```text
This entry formalizes the derivation-order invariant for a reassembled proof ladder over a 10,271-entry registry. The submitted Isabelle/HOL theory encodes 753 concrete dependency edges as rung pairs and proves that each edge points from an earlier prerequisite rung to a later dependent rung. The result is a compact certificate for acyclicity with respect to the supplied ranking: every materialized dependency respects the strict upward-rung order. The wider registry, graph-topology report, and publication paper are cited as source documentation; the formal AFP contribution is the checked order invariant itself.
```

Suggested topics:

- Computer science / Data structures
- Computer science / Algorithms
- Logic / General logic

Comment to editors:

```text
This is a focused first submission from a larger proof-pipeline archive. The entry intentionally submits only the derivation-order certificate: a finite dependency-edge list and a checked strict-order invariant. The broader TZPIDProof repository and the Zenodo DOI are cited only as source documentation for the generated edge set, not as part of the formal AFP entry.
```

## Remaining Before Actual Submission

- Run the AFP-style PDF build command and inspect the generated PDF.
- If the linter warns about generated large list style, add a short comment explaining that the edge list is generated evidence.
- Decide whether to include the full generated edge list as a generated file notice in the theory header.
- Package only the `TZPID_Derivation_Order` directory, not the full `D:\TZPIDProof` archive.
