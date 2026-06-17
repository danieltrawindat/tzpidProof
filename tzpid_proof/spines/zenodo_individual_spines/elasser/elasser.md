# Zenodo Spine: Elasser

Source aggregate: `../TZPID_ZENODO_SPINES.md`

**Thesis (from abstract).** This manuscript develops a cross-scale framework in which persistent rotational structure is treated as an actively maintained gyromagnetic state rather than a purely passive remnant of initial conditions. The model is organized around three components: (i) a shared geometric phase space for laboratory and astrophysical rotating systems, (ii) an Elsasser attractor manifold with characteristic Λ ∼ O(1), and (iii) scal

**Spine targets**

| ID | Title | Obligation | Key equation |
|---|---|---|---|
| ID0500 | Self-Sustaining Dynamo Ignition | Core_Definition | `\begin{adjustbox}{max width=\linewidth,center} $` |
| ID9086 | Definition of µ | Core_Definition | `µ=kMR2Ω\mu` |
| ID9087 | Definition of k,M,Rˆ2,Ωµ | Core_Definition | `k,M,Rˆ2,\Omegaµ=kMR2Ω,` |
| ID9084 | Definition of Lk | Core_Definition | `Lk=14πC1C2(r1r2)(dr1×` |
| ID2269 | First Exact Alignment Sidecar - Elasser and DA | Derived_Theorem_Obligation | `\displaystyle \rho_{\mathrm{bio}}=\mathcal{E}(\r` |
| ID8826 | UNIVERSAL ELSASSER CRITICALITY (AXIOM 3) Canon | Derived_Theorem_Obligation | `|E_B - E_{rot}| < \epsilon \implies \Lambda \sim` |
| ID9081 | Relation: Λ_crit≈1Λ_crit≈1Λ_crit≈1 | Derived_Theorem_Obligation | `Λ_crit≈1\Lambda_{\text{crit}}\approx1Λ_crit≈1` |

**Dependency chain**

```text
ID0500 -> ID9086 -> ID9087 -> ID9084 -> ID2269 -> ID8826 -> ID9081
```

**Isabelle:** `isabelle_tzpid/TZPID_Spine_Elasser.thy`  ·  **Wolfram:** `wolfram_checks/Elasser_checks.wl`

---
