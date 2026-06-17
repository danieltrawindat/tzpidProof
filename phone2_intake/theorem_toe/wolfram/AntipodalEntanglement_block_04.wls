AntipodalInvolutionLemma := Module[
  {
    τ: 𝕊 → 𝕊,
    τ[point[i]] = point[153601 - i] for i ∈ {1, ..., 76800},
    τ[point[i]] = point[i - 76800] for i ∈ {76801, ..., 153600}
  },
  
  Prove[
    τ ∘ τ = Identity ∧
    FixedPoints[τ] = ∅ ∧
    ∀ p ∈ 𝕊: GeodesicDistance[p, τ(p)] = π
  ]
]