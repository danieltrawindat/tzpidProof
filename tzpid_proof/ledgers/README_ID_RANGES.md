# TZPID Master — ID Range Provenance & Schema

Which source each block of IDs in
`TZPID_ALL_IDS_CANONICAL_EQUATION_MASTER_with_export.csv` came from (short source names only).

| ID range          | Count | Source | What it is |
|-------------------|-------|--------|------------|
| ID0000 – ID6158   | 5,644 | Registry | Original source-truth registry equations. |
| ID6159 – ID8460   | 2,302 | **OAI2** | OpenAI / ChatGPT data export. |
| ID8461 – ID9496   | 1,036 | **TOtzp** | Google Takeout — Gemini + NotebookLM "Trawin Zero Point" notebooks. |
| ID9497 – ID10272 | 776 | **ALL** | `D:\All` corpus — authored .tex / .md / .txt / .pdf source material (read-only; nothing was modified there). |
| (none)            | 0 | **TOwya** | Google Takeout — non-technical; no equations. |

Total rows: 9,758

## This pass (D:\All)
- **519** previously-TBD canonical statements were filled with real source text matched from the `D:\All` corpus.
- **776** new equations/concepts found in `D:\All` were added (deduped against the master; single letters, prose, code and JSON fragments filtered out).
- `D:\All` was treated strictly read-only — only read/copied, never modified.

## Columns (master)
`id, title, canonical_statement, canonical_equation, formation_method, formation_inputs, formation_note, dictionary, encyclopedia, uuid`

- **dictionary** — one-line definition of the entry (sourced where material exists, otherwise composed from the equation's structure).
- **encyclopedia** — longer descriptive paragraph (sourced where available, otherwise best-effort from physics/math logic).

## Companion files
- `TZPID_DICTIONARY.csv` — id, title, definition (Dictionary section).
- `TZPID_ENCYCLOPEDIA.md` — one descriptive article per ID (Encyclopedia section).
- `TZPID_TOtzp_DEFINITIONS.csv`, `TZPID_TOtzp_BOOK_NARRATIVE.md` — TOtzp block companions.
