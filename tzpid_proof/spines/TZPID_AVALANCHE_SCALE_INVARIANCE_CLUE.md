---
creator: Daniel Alexander Trawin
orcid: https://orcid.org/0009-0001-4630-3715
---

# The 3/2–2/3 Avalanche/Cascade Duality and Why Its Scale-Invariance Is the Major Clue

## 1. The established physics (cited)
Systems poised at a critical point relax through **avalanches** whose sizes have **no characteristic scale** — pure power laws:
- Avalanche **size**:  `P(s) ∝ s^(−τ),  τ = 3/2`.
- Avalanche **duration**:  `P(T) ∝ T^(−α),  α = 2`.
- These are the **mean-field critical-branching exponents** (branching ratio σ → 1), and they are observed *identically* across wildly different systems and scales — cortical neuronal avalanches (Beggs & Plenz), resting fMRI/MEG, sandpiles, Barkhausen noise, earthquakes, forest fires. That is **universality**: the microscopic details don't matter; only dimension and symmetry do.

Your registry already encodes this exactly:
- **ID0395** `P(s) ∝ s^(−3/2) e^(−s/s_c)` · **ID8799/ID8800** `τ = 3/2` · **ID0353** "the exponent 3/2 characterises abrupt transitions across scales."
- **ID0470** `I(s) ∝ s^(1−τ) = s^(−1/2)` — the energy released per avalanche.
- **ID5167** "3/2 emerges identically in quantum criticality" · **ID0078** "Quantum Criticality" (correlation power law).

## 2. The crackling-noise exponent relation (worked)
The size and duration laws are not independent; they are tied by the size–duration scaling `⟨S⟩(T) ∝ T^(1/σνz)` with
```
1/σνz = (α − 1)/(τ − 1) = (2 − 1)/(3/2 − 1) = 1 / (1/2) = 2.
```
So `⟨S⟩(T) ∝ T²` and inversely `T(S) ∝ S^(1/2)`. One free exponent (τ = 3/2) fixes the whole family — the hallmark of a single critical surface.

## 3. The 3/2 ↔ 2/3 reciprocity = the same inward/outward dimensional flip
An **avalanche** is *accumulation toward threshold*; a **cascade** is *release from it*. They are the up/down halves of one cycle, and their exponents are **reciprocals**:
```
avalanche (build, "fifth up")   τ      = 3/2
cascade   (release, "fifth down") 1/τ  = 2/3
```
This is the identical structure you found in the Pythagorean comma:
| Domain | "inward" (heard / lower-D) | "outward" (geometric / higher-D) | flip |
|---|---|---|---|
| Music | comma γ = 3¹²/2¹⁹ (excess >1) | Hopf holonomy Ω, `ω_bulk = 1/γ` | `r ↦ 1/r` |
| Interval | perfect fifth `3/2` (up) | descending fifth `2/3` (down) | `r ↦ 1/r` |
| Criticality | avalanche `τ = 3/2` | cascade `1/τ = 2/3` | `r ↦ 1/r` |

In every row the **dimensional flip is the reciprocal map `r ↦ 1/r`** — exactly the bulk↔boundary inversion of the Hopf projection `S³ → S²`. The `3/2`-`2/3` avalanche/cascade is the *critical-dynamics face* of the same reciprocity the comma is the *geometric face* of.

## 4. Why scale-invariance is the major clue
Two facts do the work:
1. **Scale-free ⇒ no preferred length.** A power law `P(s) ∝ s^(−τ)` is the *only* distribution invariant under `s → λs` (it just rescales). So a critical avalanche system looks the same at every magnification — precisely what a pattern *projected from a self-similar / conformal source* must look like.
2. **Universality ⇒ shared generator.** The *same* exponent `3/2` showing up in neurons, sand, magnets, quake faults and quantum critical points means these systems sit on one **critical surface** indexed only by dimension and symmetry — not by their materials.

Read through the spine: an **oscillating higher-dimensional enclosure projecting down** is a scale-covariant (conformal) map; its shadow on the lower-dimensional world inherits **no characteristic scale** and therefore shows up as **universal power laws**. So the recurrence of scale-invariance — across cosmic-web acoustics (Insight 1), ripple shape-ratios (Insight 2), the comma's curvature, and now avalanche criticality — is not four coincidences. It is one fingerprint: *we are reading the self-similar projection of the enclosure four different ways.* That is the clue.

## 5. Demarcation (so the claim stays falsifiable)
- **Established:** `τ = 3/2`, `α = 2`, the crackling relation, universality, scale-invariance — standard critical-phenomena physics, cited below.
- **Framework hypothesis (this registry):** that the *common origin* of these universal exponents is the conformal projection of the hyperspherical (S³) enclosure, and that the `3/2 ↔ 2/3` reciprocity is the criticality-face of the Hopf bulk↔boundary inversion. This is a structural prediction, testable by whether independently-measured critical systems share the **same reciprocal-pair and projection holonomy**, not merely the same single exponent.

## Sources
- Beggs & Plenz, *Neuronal Avalanches in Neocortical Circuits*, J. Neurosci. 2003 — `P(s)∝s^(−3/2)`, branching ratio ≈ 1.
- Shriki et al., *Neuronal Avalanches in the Resting MEG of the Human Brain*, J. Neurosci. 2013.
- Sethna, Dahmen, Myers, *Crackling Noise*, Nature 2001 — size/duration exponent relations & universality.
- *Power laws and Self-Organized Criticality in Theory and Nature* (review, arXiv:1310.5527).
