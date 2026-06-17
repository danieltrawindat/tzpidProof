# Zenodo Spine: step by step

Source aggregate: `../TZPID_ZENODO_SPINES.md`

**Thesis (from abstract).** The mathematical logistics of the Great Pyramid, built in the fashion of the step pyramids but utilizing winch-style cranes wrapping rope around a spool that workers would walk around, could provide a measurable way to place blocks within a crane’s turning radius. As each step grew from one layer to the next, blocks could be filled in step by step by hoisting one physical stone at a time into the next level.

**Spine targets**

| ID | Title | Obligation | Key equation |
|---|---|---|---|
| ID9819 | Definition of D | Core_Definition | `d = 2\lfloor\sqrt{N_{\max}\pi}\rfloor + 1` |
| ID9885 | Definition of N_max | Core_Definition | `N_{\max}=153600` |
| ID6459 | Practical Next Steps I Can Execute Now (Pick A | Core_Definition | `\arg\Psi` |
| ID3297 | Curvature Relation | Core_Definition | `\begin{equation} I_{4D} = \left( \frac{R}{ \lamb` |
| ID9896 | Relation: P < 1 - 1/π ≈ 0.682 | Derived_Theorem_Obligation | `p < 1 - 1/\pi \approx 0.682` |
| ID9915 | Relation: √(153600π)≈ 694 | Derived_Theorem_Obligation | `\sqrt{153600\pi}\approx 694` |
| ID0048 | Falsifiability as Core Design Constraint | Core_Axiom | `\exists D: \quad P(D\mid H) \neq P(D\mid \neg H)` |

**Dependency chain**

```text
ID9819 -> ID9885 -> ID6459 -> ID3297 -> ID9896 -> ID9915 -> ID0048
```

**Isabelle:** `isabelle_tzpid/TZPID_Spine_step_by_step.thy`  ·  **Wolfram:** `wolfram_checks/step_by_step_checks.wl`

---
