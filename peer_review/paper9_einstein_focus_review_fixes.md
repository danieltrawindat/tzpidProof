# Paper V-A Einstein Focus: Review Fixes

Timestamp: 2026-06-10 11:45 America/New_York

Scope: `peer_review/tex/paper9_einstein_focus.tex` and rebuilt `peer_review/pdf/paper9_einstein_focus.pdf`.

## Issues Found

1. Long machine-readable role/check names produced overfull LaTeX boxes.
2. The computational verification table was too wide in its original `llll` layout.
3. A few phrases were too conversational or rhetorically strong for a peer-review-facing paper.
4. PDF metadata included author/title/keywords but not the requested creator metadata form.
5. The verification table could float above its own section heading.

## Fixes Applied

1. Added `tabularx`, `float`, and `microtype` for safer peer-review layout.
2. Replaced the wide verification table with a full-width `tabularx` table.
3. Shortened table check labels while preserving the underlying certificate identity in the surrounding text.
4. Softened peer-review-sensitive phrasing:
   - replaced colloquial peer-review language with internal-correction language;
   - replaced “kills the master equation” with “would falsify the master equation in its stated form”;
   - replaced “utterly negligible” with observation-constrained wording;
   - replaced “filing cabinet” language with “audit trail” language.
5. Added `pdfcreator={Trawin, Daniel Alexander}` to the hyperref metadata.
6. Pinned the two tables with `[H]` so the section/table order is stable.

## Verification

Command:

```powershell
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir='D:/TZPIDProof/peer_review/build/paper9_einstein_focus' 'D:/TZPIDProof/peer_review/tex/paper9_einstein_focus.tex'
```

Final log scan:

```text
No LaTeX warning/error/box hits in final log.
```

Rendered pages:

```text
D:\TZPIDProof\peer_review\build\paper9_einstein_focus\render_final\page-1.png ... page-8.png
```

Spot checks: title/abstract page, verification-table page, and references page render cleanly.

## Output

Rebuilt PDF:

```text
D:\TZPIDProof\peer_review\pdf\paper9_einstein_focus.pdf
```

Edited source:

```text
D:\TZPIDProof\peer_review\tex\paper9_einstein_focus.tex
```

No files in `d:\tzpidNEW` were changed.
