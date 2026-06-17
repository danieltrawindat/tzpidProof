# Running the Algorithmic-Ambassador Wolfram modules

186 modules were extracted from the 48 reports and cleaned into runnable Wolfram Language.

## Files
- `tzpid_aa_modules.json` — every module: name, source report, class, cleaned WL code.
- `tzpid_aa_stubs.wl` — a real `FibonacciSphere` plus safe placeholders for 40 domain functions
  (e.g. FiberBundle, FisherInformation, Functor, PathIntegral, Discovery, AccumulationFactor) so modules evaluate without undefined-symbol errors.
- `run_certify.wls` — wolframscript runner: loads stubs, evaluates each module, writes `wolfram_module_results.json`.

## How to run (Wolfram Engine 14.3)
```powershell
cd <this folder>
wolframscript -file run_certify.wls
```
Each module is recorded with a status: **computed** (numeric result), **evaluated_structure** (returned an Association),
**symbolic** (held expression — references domain functions left abstract), **syntax_error**, or **timeout**.
Mirror the passing ones into your `wolfram_checks/` certificate layer exactly like `einstein_focus_results.json`.

## What cleaning was applied
- Unicode operators -> ASCII WL ( -> for arrows, * for x/dot, <= >= , Infinity ).
- Subscripted variable names ( B_field, v_A ) -> `$` form ( B$field, v$A ) so they are valid symbols, while
  genuine patterns ( r_, _Real ) are preserved.
- docx mojibake repaired; bracket-balanced; whitespace flattened.

## Classes
- **computational** (104): use >=3 built-in WL functions; most likely to produce numbers.
- **notational** (82): mostly domain notation; evaluate to symbolic structure (still valid models).

Stubs are placeholders, not physics. Replace a stub with a real definition to turn a `symbolic` module into a `computed` one.
