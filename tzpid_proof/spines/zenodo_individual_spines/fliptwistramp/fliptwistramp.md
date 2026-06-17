# Zenodo Spine: FlipTwistRamp

Source aggregate: `../TZPID_ZENODO_SPINES.md`

**Thesis (from abstract).** This manuscript formalizes a dual-carrier signal architecture built from a rational bridge ratio and a localized phase-inversion seam. Starting from the pair (153,600, 129,600) and bridge ratio r = 32/27, we derive entrainment-scale realizations, define a Gaussian seam operator, and provide time-frequency and phase-space diagnostics for transient topological-like defects.

**Spine targets**

| ID | Title | Obligation | Key equation |
|---|---|---|---|
| ID0131 | Gaussian Window Insertion Operator | Core_Definition | `g(t)=\exp\!\left(-\frac{(t-t_0)^2}{2\sigma^2}\ri` |
| ID2354 | FlipTwistRamp | Core_Definition | `g(t)=\exp\!\big(-\frac{(t-t_0)^2}{2\sigma^2}\big` |
| ID8351 | How \(r\) Can Act as a Bridge / Flip / Twist f | Core_Definition | `f\mapsto f\cdot r` |
| ID3513 | Conductivity Relation | Core_Definition | `\[ g(t)=\exp\!\big(-\frac{(t-t_0)^2}{2\sigma^2}\` |
| ID3514 | Pi Relation | Core_Definition | `\[ s(t)=A_1\sin(2\pi f_A' t+\phi_1)+A_2\sin(2\pi` |
| ID8382 | Level 3 — Hamiltonian Micro Picture (HTZPtunne | Derived_Theorem_Obligation | `\epsilon(t) \sim A_3 g(t) e^{i\phi_3}` |
| ID8391 | Simulation Pipeline (Order): α | Derived_Theorem_Obligation | `\dot{\alpha} = -i\omega_a \alpha - \gamma_a \alp` |

**Dependency chain**

```text
ID0131 -> ID2354 -> ID8351 -> ID3513 -> ID3514 -> ID8382 -> ID8391
```

**Isabelle:** `isabelle_tzpid/TZPID_Spine_FlipTwistRamp.thy`  ·  **Wolfram:** `wolfram_checks/FlipTwistRamp_checks.wl`

---
