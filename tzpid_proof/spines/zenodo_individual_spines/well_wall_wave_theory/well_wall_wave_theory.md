# Zenodo Spine: well wall wave theory

Source aggregate: `../TZPID_ZENODO_SPINES.md`

**Thesis (from abstract).** We propose the Well–Wall–Wave (WWW) Theory, a composite field model in which orbital structure arises from the interaction of (i) a smooth inward potential basin (Well), (ii) an oscillatory radial eigenmode structure (Wave), and (iii) a derived set of dynamically stable shells (Wall). The Well is modeled by a Gaussian deficit envelope, while the Wave is modeled via Bessel functions representing radial resonances.

**Spine targets**

| ID | Title | Obligation | Key equation |
|---|---|---|---|
| ID9516 | Gravitation: Spacetime Curvature and Lensing A | Core_Definition | `\Phi_{\text{eff}} = (1+\epsilon)\Phi_{\text{Newt` |
| ID7732 | How This Ties into Your TZPQVS Superconducting | Core_Definition | `Y_{\ell m}(\theta,\phi)` |
| ID1863 | The Inward-Outward Cross | Core_Definition | `P(r) = P_\infty - \frac{1}{2}\rho v(r)^2` |
| ID0252 | Harmonic Bessel Standing Waves | Core_Definition | `u_{mn}(r,\theta)=J_m(k_{mn}r)e^{im\theta} || J_m` |
| ID6489 | \{Einstein–Rosen Bridge and Trawin Zero-Point  | Derived_Theorem_Obligation | `0.3em] \textit{A Theoretical Massless Transit Sy` |
| ID0261 | Bessel Standing Wave Quantization | Derived_Theorem_Obligation | `approx1.2024 || frac{R}{r}\approx2.46` |
| ID0148 | Phase Twist-Induced Domain Wall | Derived_Theorem_Obligation | `\phi(x)=\pi\left[\frac{1+\tanh((x-x_0)/w)}{2}\ri` |

**Dependency chain**

```text
ID9516 -> ID7732 -> ID1863 -> ID0252 -> ID6489 -> ID0261 -> ID0148
```

**Isabelle:** `isabelle_tzpid/TZPID_Spine_well_wall_wave_theory.thy`  ·  **Wolfram:** `wolfram_checks/well_wall_wave_theory_checks.wl`

---
