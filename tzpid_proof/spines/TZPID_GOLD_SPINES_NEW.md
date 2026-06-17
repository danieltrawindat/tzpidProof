---
creator: Daniel Alexander Trawin
orcid: https://orcid.org/0009-0001-4630-3715
---

# TZPID New Gold Spines

Three new focused gold spines built from the canonical registry, in the same shape as the Einstein/cosmology spine in `README_PROOF_PIPELINE.md`: a curated chain of registry targets, a dependency backbone, the key equations, proof-obligation roles, and Wolfram-checkable relations. Each is paired with an Isabelle focus-theory stub and a Wolfram check stub.

## Gold Spine: Gravity as an Accumulated Force

**Thesis.** Gravity is recovered not as a fundamental field but as the accumulated/integrated response of mass-energy transport, with the Newtonian field emerging as the far-field limit of an accumulated-force correction.

**Spine targets**

| ID | Role | Obligation | Key equation |
|---|---|---|---|
| ID7216 | Accumulated mass functional M_acc (source of the correction) | Core_Definition | `M_{\rm acc}` |
| ID7215 | Newtonian acceleration baseline a_N | Core_Definition | `\mathbf{a}_{\rm N}` |
| ID7214 | Accumulated-force modified acceleration a = a_N(1+alpha...) | Derived_Theorem_Obligation | `\mathbf{a} = \mathbf{a}_{\rm N} \Big(1 + \alpha \frac{M_{\rm acc}}{M_\oplus^{(0)}}\Big),` |
| ID7311 | Accumulated stress correction delta T_ij | Derived_Theorem_Obligation | `\delta T_{ij} = \alpha\, \frac{G M_{\rm acc}}{R^3} \hat n_i \hat n_j,` |
| ID7314 | Effective stress-energy T_ij^eff = T_ij^N + delta T_ij | Derived_Theorem_Obligation | `T_{ij}^{\rm eff} = T_{ij}^{\rm N} + \delta T_{ij}.` |
| ID7577 | Emergent gravity field Phi(x,t) | Derived_Theorem_Obligation | `\Phi(x,t)` |
| ID1816 | Newtonian/Poisson limit  nabla^2 Phi = 4 pi G_eff rho  (observable closure) | Derived_Theorem_Obligation | `\nabla^2\Phi = 4\pi G_\text{eff}\rho(\mathbf{x})` |

**Dependency chain**

```text
ID7216 -> ID7215 -> ID7214 -> ID7311 -> ID7314 -> ID7577 -> ID1816
ID7216  Accumulated mass functional M_acc (source of the correction)
ID7215  Newtonian acceleration baseline a_N
ID7214  Accumulated-force modified acceleration a = a_N(1+alpha...)
ID7311  Accumulated stress correction delta T_ij
ID7314  Effective stress-energy T_ij^eff = T_ij^N + delta T_ij
ID7577  Emergent gravity field Phi(x,t)
ID1816  Newtonian/Poisson limit  nabla^2 Phi = 4 pi G_eff rho  (observable closure)
```

**Wolfram-checkable relations**

- `grav_newtonian_recovery` — a -> a_N as alpha -> 0  ·  accumulated correction vanishes; Newtonian acceleration recovered
- `grav_stress_vanishes` — delta T_ij -> 0 as alpha -> 0  =>  T_ij^eff -> T_ij^N  ·  effective stress reduces to Newtonian stress in far field
- `grav_poisson_dim_balance` — [nabla^2 Phi] == [4 pi G rho]  ·  dimensional balance of the emergent Poisson closure

**Isabelle focus theory:** `isabelle_tzpid/TZPID_Gravity_Focus.thy`  ·  **Wolfram checks:** `wolfram_checks/gravity_spine_checks.wl`

---


## Spinal Tap: Bessel Residual Between Gravity and Energy-to-Matter

**Thesis.** The tap preserves ordinary mass-energy accounting while inserting a falsifiable residual layer: a hyperspherical half-Bessel mode drop creates an entropy-fold correction that accumulates causally into curvature beyond matter-only stress-energy.

```text
Gravity as an Accumulated Force -> Bessel Residual Spinal Tap -> Energy-to-Matter Logic
```

**Artifacts:** `TZPID_BESSEL_RESIDUAL_SPINAL_TAP.md`, `TZPID_BESSEL_RESIDUAL_SPINAL_TAP_obligations.csv`, `wolfram/bessel_residual_spinal_tap_checks.wl`, and the Isabelle theories `TZPID_BesselResidualSpinalTap_Focus.thy` / `TZPID_BesselResidualSpinalTap_Computational_Checks.thy`.

## Gold Spine: Energy-to-Matter Logic

**Thesis.** Matter is realized from vacuum energy when a regularized vacuum energy density builds a pressure that crosses a creation threshold, condenses into pairs, and is fixed in mass by E=mc^2 before sourcing curvature.

**Spine targets**

| ID | Role | Obligation | Key equation |
|---|---|---|---|
| ID0024 | TZP vacuum energy density rho_vac^T | Core_Definition | `\rho_{\mathrm{vac}}^{T} = \frac{1}{u_{T}^{4}} \int_{0}^{\omega_{\mathrm{cut}}} \eta(\omega)\,\hbar\omega\,d\omega || \om` |
| ID10164 | Naive (divergent) vacuum energy E_vac^naive | Core_Definition | `E_{\text{vacuum}}^{\text{naive}} = \sum_{\vec{k}}\frac{\hbar\omega_{\vec{k}}}{2} = \sum_{\vec{k}}\frac{\hbar c |\vec{k}|` |
| ID10165 | Regularized vacuum energy E_vac^reg | Derived_Theorem_Obligation | `E_{\text{vacuum}}^{\text{reg}} = \sum_{\vec{k}}\frac{\hbar\omega_{\vec{k}}}{2}f\left(\frac{\omega_{\vec{k}}}{\Lambda}\ri` |
| ID0188 | Matter-creation pressure threshold  P_vac >= P_crit | Core_Axiom | `P_{\mathrm{vac}} \ge P_{\mathrm{crit}} || \rho_{\mathrm{matter}} \uparrow` |
| ID0409 | Superconducting pair-creation operator | Derived_Theorem_Obligation | `\begin{adjustbox}{max width=\linewidth,center} $\displaystyle \hat{H}_{\mathrm{SC}}=\Delta\,c_{\uparrow}^{\dagger}c_{\do` |
| ID2846 | Mass-energy equivalence  E = m c^2  (mass fixing) | Core_Axiom | `\( E = mc^2 \\)` |
| ID1816 | Created matter sources curvature  nabla^2 Phi = 4 pi G_eff rho  (closure) | Derived_Theorem_Obligation | `\nabla^2\Phi = 4\pi G_\text{eff}\rho(\mathbf{x})` |

**Dependency chain**

```text
ID0024 -> ID10164 -> ID10165 -> ID0188 -> ID0409 -> ID2846 -> ID1816
ID0024  TZP vacuum energy density rho_vac^T
ID10164  Naive (divergent) vacuum energy E_vac^naive
ID10165  Regularized vacuum energy E_vac^reg
ID0188  Matter-creation pressure threshold  P_vac >= P_crit
ID0409  Superconducting pair-creation operator
ID2846  Mass-energy equivalence  E = m c^2  (mass fixing)
ID1816  Created matter sources curvature  nabla^2 Phi = 4 pi G_eff rho  (closure)
```

**Wolfram-checkable relations**

- `em_regularization_finite` — E_vac^reg finite while E_vac^naive divergent  ·  subtraction scheme yields finite regularized vacuum energy
- `em_creation_threshold` — P_vac >= P_crit  is the matter-onset condition  ·  creation switches on exactly at the pressure threshold
- `em_mass_energy_identity` — E == m c^2  (dimensional/identity check)  ·  mass-energy equivalence fixes created rest mass

**Isabelle focus theory:** `isabelle_tzpid/TZPID_EnergyMatter_Focus.thy`  ·  **Wolfram checks:** `wolfram_checks/energy_matter_spine_checks.wl`

---

## Gold Spine: Topological Unification

**Thesis.** Distinct interaction sectors are unified by a single topological obstruction: a connection curvature builds a Chern-Simons action whose Chern/linking invariants assemble one topological charge Omega, whose non-vanishing obstruction is the unified field equation.

**Spine targets**

| ID | Role | Obligation | Key equation |
|---|---|---|---|
| ID9342 | Connection curvature F = dA + A wedge A ; CS(A)!=0 => O_top!=0 | Core_Definition | `𝐹=𝑑𝐴+𝐴∧𝐴 CS(𝐴)≠0 =⇒ Otop≠0` |
| ID8480 | Chern-Simons action S_CS | Core_Definition | `S_{CS} = \int_{M} A \wedge dA + \Gamma_{acoustic}` |
| ID8931 | Chern number C_1 in Z (quantized charge) | Derived_Theorem_Obligation | `C_1 = \frac{1}{2\pi} \int_{BZ} F \cdot dS \in \mathbb{Z}` |
| ID0643 | Gauss linking number Lk (poloidal/toroidal linkage) | Derived_Theorem_Obligation | `\tzpfitmath{Lk = \frac{1}{4\pi} \oint_{C_1} \oint_{C_2} \frac{ (\mathbf{r}_1-\mathbf{r}_2) \cdot (\mathrm{d}\mathbf{r}_1` |
| ID9892 | Assembled topological invariant Omega_top = C_1(T^2) + pi w(T^2) | Derived_Theorem_Obligation | `\Omega_{\mathrm{top}} = C_1(T^2) + \pi\,w(T^2) + \log \Pi_{\pi},` |
| ID9176 | Obstruction class for topological unification | Derived_Theorem_Obligation | `A_\mudxΘ{\mu}+B_{\text{gravitational}}+ C_{\text{electromagnetic}}Aµ= Aµdxµ+Bgravitational` |
| ID5773 | Trawin topology unified field equation h_mu nu | Derived_Theorem_Obligation | `\[ h_{\mu\nu} = A\,\psi^{*}\partial_{\mu}\partial_{\nu}\psi \]` |

**Dependency chain**

```text
ID9342 -> ID8480 -> ID8931 -> ID0643 -> ID9892 -> ID9176 -> ID5773
ID9342  Connection curvature F = dA + A wedge A ; CS(A)!=0 => O_top!=0
ID8480  Chern-Simons action S_CS
ID8931  Chern number C_1 in Z (quantized charge)
ID0643  Gauss linking number Lk (poloidal/toroidal linkage)
ID9892  Assembled topological invariant Omega_top = C_1(T^2) + pi w(T^2)
ID9176  Obstruction class for topological unification
ID5773  Trawin topology unified field equation h_mu nu
```

**Wolfram-checkable relations**

- `topo_chern_quantization` — C_1 = (1/2 pi) int F  in  Z  ·  Chern number is integer-quantized
- `topo_obstruction_nonvanishing` — CS(A) != 0  =>  O_top != 0  ·  non-trivial Chern-Simons forces a non-zero obstruction
- `topo_invariant_decomposition` — Omega_top == C_1(T^2) + pi w(T^2)  ·  unified charge decomposes into Chern + winding parts

**Isabelle focus theory:** `isabelle_tzpid/TZPID_TopologicalUnification_Focus.thy`  ·  **Wolfram checks:** `wolfram_checks/topo_unification_spine_checks.wl`

---
