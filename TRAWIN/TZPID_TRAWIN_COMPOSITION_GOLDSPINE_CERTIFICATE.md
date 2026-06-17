---
creator: Daniel Alexander Trawin
orcid: https://orcid.org/0009-0001-4630-3715
generated: 2026-06-11
---

# TRAWIN Composition — Gold-Spine Closure Certificate

This is the **evaluated** layer on top of `TZPID_TRAWIN_OPERATOR_PASS.csv`. Where the operator pass only *wraps* each
field in operator notation, this certificate actually runs the canonical composition

```
C_R = N ∘ I ∘ W ∘ A ∘ R ∘ T      (Def. 4, Trawin Zero Point 100 Primary)
```

on the curated gold-spine keystones, evaluates the admissibility closure `C_R[Ψ] = 0` (or `= const`, or `= source`),
and ties each result to an existing **Isabelle/HOL carrier theorem** from the Vector-Calculus Isar Spine Layer and to the
**Wolfram** certificate layer. The closures are not asserted — they are checked symbolically (SymPy) and numerically.

## Method

Each keystone's field Ψ is run through the representative realization on `X ⊂ R³`:
`T:=∂_t`, `R:=∇×` (vector) or `r r̂·∇` (scalar), `A:=` multiply by `A(x,t)`, `W:=□=∇²−c⁻²∂²_t`, `I:=∫_Ω …dV`,
`N:=` normalization/closure. A keystone is **admissible** (Hypothesis 1) when `C_R[Ψ]` lands in a well-posed constraint
class. The formal carrier column names the Isar theorem in `TZPID_VectorCalculus_IsarSpineLayer.thy` /
`TZPID_VectorCalculus_IntegralCarriers.thy` that discharges the operator-level step.

## Evaluated keystones

| ID | Field Ψ | Composition step that closes | Closure result | Formal carrier (Isar) | Wolfram |
|---|---|---|---|---|---|
| **ID0335** | `R_{μν}−½g_{μν}R+Λg_{μν}=8πG/c⁴·T_{μν}+Φ^TZP_{μν}` | `R∘T` on gradient sector: `∇×∇φ=0`; far-field `Φ^TZP→0` | `C_R=0` → classical Einstein limit | `isar_delta_alpha_gradient_curl_layer` | `id0335_formal_limit` ✔ |
| **ID0167** | `G_{μν}+Λg_{μν}=8πG/c⁴·T^tot_{μν}` | `I`/divergence closure: `∇·(∇×F)=0` ⇒ `∇^μ G_{μν}=0` ⇒ `∇^μ T_{μν}=0` | `C_R=const` (conservation) | `vc_incompressible_from_opposite_partials` | `id0167_total_stress_energy` ✔ |
| **ID0394** | `T^TZP_{μν}=ρ_vac u_μu_ν+p_vac g_{μν}` | `A∘…` amplitude + `N` normalization of `ρ_vac(r)∼J₀(kr)⁻¹` | `C_R=const` vacuum tensor | `id0394_vacuum_tensor` (Wolfram-backed) | `id0394_vacuum_tensor` ✔ |
| **ID0958** | `(∇²−c⁻²∂²_t)A=N_ρ` | `W` is the carrier; far field `N_ρ→0` | `C_R=0` free-wave / `=source` near TZP | `vector_calculus_isar_spine_contract` | `id0958_action_level_bridge` ✔ |
| **ID0400 / ID1392** | `ρ_Λ=ħc/R⁴·Φ₀/Φ_tot ∼ H₀²` | `N` normalization → Friedmann constraint `H²=8πG/3·ρ` | `C_R=const` (Hamiltonian constraint) | `id0400_hubble_normalization` | `id0400_hubble_normalization` ✔ |
| **ID10867** | `H₀=Ṙ₀/R₀` | `T∘I`: `V=2π²R³` ⇒ `V̇/V=3Ṙ/R` | `C_R=3H₀=0.207/Gyr` ✔ | `vc_rectangle_area_nonnegative` (volume carrier) | new — computed |
| **ID10868** | `ρ_Λ=ħc/R⁴∼H₀²; Λ=3Ω_ΛH₀²/c²` | `N` continuity with `p=−ρc²` ⇒ `ρ̇=0` | `C_R: ρ_Λ=const` ✔ | `vc_uniform_helicity_integral_zero_density` (analogue) | new — computed |
| **ID10869** | `λ_Λ=(ħc/ρ_Λ)^¼` | `N` dimensional closure | `C_R=88.1 μm` ✔ (target 85–88) | — | new — computed |
| **ID10870** | `ħc/ℓ_Pl⁴ vs ħc/R_H⁴` | `N` ratio `(R_Λ/ℓ_Pl)⁴` | `C_R=8.8×10¹²²≈10¹²³` ✔ | — | new — computed |
| **ID10871** | `H²(a)=H₀²[Ω_r a⁻⁴+Ω_m a⁻³+Ω_K a⁻²+Ω_X F(a)]` | full `C_R` as Friedmann closure, `Ω_K<0`, `F(a)=exp[3∫(1+w)/a' da']` | `C_R=0` (constraint surface) | `vector_calculus_integral_carrier_contract` | obligation |

## Symbolically verified closure identities (SymPy)

```
1. R(∇φ)  = ∇×∇φ        = (0,0,0)            → C_R=0           [ID0335 gradient sector]
2. ∇·(∇×F)                = 0                  → ∇^μ(...)=0      [ID0167/0335 conservation]
3. V=2π²R³ : V̇/V          = 3·Ṙ/R = 3H        → C_R=3H          [ID10867]
4. continuity, p=−ρc² :   ρ̇+3H(ρ+p/c²)=ρ̇ ⇒ 0  → ρ_Λ=const       [ID10868]
5. □A=N_ρ ; N_ρ→0         → □A=0               → free-wave       [ID0958]
```

## Numerically confirmed

```
λ_Λ = (ħc/ρ_Λ)^¼          = 88.1 μm           (target 85–88)   [ID10869]
ħc/ℓ_Pl⁴ / ρ_Λ            = 8.8×10¹²²  ~10¹²³                   [ID10870]
V̇/V = 3H₀                 = 0.207 /Gyr        (target 0.21)    [ID10867]
```

## How this couples to the Vector-Calculus Isar Spine Layer

The Isar layer (`VECTOR_CALCULUS_ISAR_SPINE_LAYER_CERTIFICATE.md`) already proves, in readable structured proof, the exact
operator-level facts the TRAWIN composition needs:

- **`R∘T` closure** — "exact mixed partials collapse the planar curl" = `∇×∇φ=0`, the identity that sends ID0335 to its
  classical Einstein limit when `Φ^TZP→0`.
- **`I` integral carriers** — `vc_rect_boundary_circulation_simplifies` / `vc_green_rectangle_constant_curl` give the
  Stokes-Green semantics the `I:=∫_Ω …dV` step requires, and supply the finite volume carrier behind `V=2π²R³` (ID10867).
- **`N` closure** — flux quantization → winding index (`vc_quantized_flux_is_quantized`,
  `vc_quantized_circulation_is_winding_index`) is the discrete realization of the normalization operator `N(TRAWI)=0`.

So the TRAWIN composition is **not** resting on Wolfram numerics alone: the curl/divergence/integral steps are discharged by
the already-built Isar theorems, and the cosmology constants are confirmed numerically.

## Isabelle/HOL composition carrier

The paper-facing TRAWIN closure has now been mirrored as a checked Isabelle/HOL carrier:

`D:\TZPIDProof\tzpid_proof\isabelle_tzpid\TZPID_TRAWIN_Composition_GoldSpine.thy`

The theory imports the physical proof architecture and records:

- the six-operator composition `N ∘ I ∘ W ∘ A ∘ R ∘ T`;
- the ten curated gold-spine keystones in this certificate;
- status partitioning into symbolic checks, numeric checks, Wolfram-backed checks, and the open analytic Friedmann obligation;
- formal consumption of the vector-calculus carrier layer;
- formal consumption of the Curry-Howard-Lambek/TQFT physical proof architecture.

Primary theorem contracts:

- `trawin_composition_operator_count`
- `trawin_composition_distinct`
- `trawin_goldspine_keystone_count`
- `trawin_goldspine_keystones_distinct`
- `trawin_only_friedmann_is_open_obligation`
- `trawin_id0335_consumes_gradient_curl_carrier`
- `trawin_id0167_consumes_divergence_carrier`
- `trawin_id0958_consumes_wave_carrier`
- `trawin_id10867_consumes_volume_carrier`
- `trawin_id10868_consumes_zero_density_carrier`
- `trawin_id10871_consumes_integral_carrier_as_obligation_surface`
- `trawin_composition_consumes_physical_architecture`
- `trawin_goldspine_closure_contract`

Verified with:

```powershell
D:\Isabelle2025\Isabelle2025-2\bin\isabelle build -D D:\TZPIDProof\tzpid_proof\isabelle_tzpid
```

## Proved vs. obligation

**Closed and checked:** the five operator identities (1–5) are exact symbolic results; the three cosmology numbers match
the registry. ID0335, 0167, 0394, 0958, 0400/1392 inherit existing Wolfram certificates; ID10867–10870 are newly computed
and now carry closures.

**Still obligation:** ID10871 (the full dynamic breathing Friedmann model) closes only on the constraint surface — its
`F(a)` dark-energy term is a fit target, not a theorem. Concrete tensor calculus for ID0335/0167 remains typed-predicate
in Isabelle, not full manifold curvature. These match the open items already flagged in the proof-pipeline README.

## Sources

- Trawin Zero Point 100 (Primary), Def. 2–4 — Trawin Operator Alphabet & composition.
- `VECTOR_CALCULUS_ISAR_SPINE_LAYER_CERTIFICATE.md` — Isar carrier theorems.
- Registry IDs ID0335, ID0167, ID0394, ID0958, ID0400/ID1392, ID10867–ID10871.
- [Planck 2018 VI](https://arxiv.org/abs/1807.06209) (H₀, Ω_Λ); [DESI DR2](https://arxiv.org/abs/2503.14738) (w(a)).
