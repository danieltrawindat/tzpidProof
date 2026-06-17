# Zenodo Spine: emergent curvature theory

Source aggregate: `../TZPID_ZENODO_SPINES.md`

**Thesis (from abstract).** We present a comprehensive field-theoretic framework demonstrating that spacetime curvature emerges from the temporal accumulation of quantum information through entanglement dynamics. The central mechanism involves a non-local accumulation kernel K(t, t′ ) = exp[−(t − t′ )/τdec ] that integrates stress-energy contributions over time, generating persistent field configurations that manifest as geometric curvature.

**Spine targets**

| ID | Title | Obligation | Key equation |
|---|---|---|---|
| ID3672 | Magnetic Helicity Tensor Coupling | Core_Definition | `$\mathcal{M} = T^*(SO(3) \times \mathbb{R}^3) \o` |
| ID5818 | Kinetic Term Relation | Core_Definition | `$\mathcal{K}(t,t') = \exp[-(t-t')/\tau_{\text{de` |
| ID9965 | Accumulation Kernel: δ S/δ g^μν | Core_Definition | `\delta S/\delta g^{\mu\nu} = (c^4/16\pi G)G_{\mu` |
| ID9967 | Accumulation Kernel: I(A:B) | Core_Definition | `I(A:B) = S(A) + S(B) - S(AB)` |
| ID9106 | Definition of dcidlnµ | Core_Definition | `dcidlnµ=fi(cj,dimeff)\frac{\text{d}c_i}{\text{d}` |
| ID3673 | Grav Quantum Charge Functional | Derived_Theorem_Obligation | `$\hat{Q}_{\text{grav}} = (\hbar c^3/8\pi G)\int_` |
| ID9859 | Stress–Energy Tensor Relation | Derived_Theorem_Obligation | `\int_{\Sigma} \sqrt{|g|}, R^{\mu\nu} T_{\mu\nu},` |

**Dependency chain**

```text
ID3672 -> ID5818 -> ID9965 -> ID9967 -> ID9106 -> ID3673 -> ID9859
```

**Isabelle:** `isabelle_tzpid/TZPID_Spine_emergent_curvature_theory.thy`  ·  **Wolfram:** `wolfram_checks/emergent_curvature_theory_checks.wl`

---
