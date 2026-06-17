---
creator: Daniel Alexander Trawin
orcid: https://orcid.org/0009-0001-4630-3715
---

# Worked Check — the cosmic filament web is spherical-enclosure acoustics

This hardens **Insight 1** of the nested-hyperspherical-enclosure spine with a concrete, verifiable computation. It links three registry IDs: **ID7733** (`j_ℓ(kr)`, the radial enclosure modes), **ID7257** (`δ_b = A·j₀(k·r_s)·T(k)`, the BAO standing wave), and **ID7259** (the sound horizon `r_s`).

## The single shared fact
A spherical acoustic enclosure of radius `R` has normal modes wherever the radial wave vanishes on the boundary:
`j_ℓ(k_{ℓn}·R) = 0`. So its allowed wavenumbers are the **zeros of the spherical Bessel function** `j_ℓ`. The early-universe baryon–photon fluid is exactly such a resonator, and its transfer function carries the `j₀(k·r_s)` modulation — whose **zeros sit at `k·r_s = nπ`**, the same harmonic ladder. The cosmic acoustic node *is* the fundamental enclosure mode.

## Verified numbers (computed here, independent of Wolfram)
Spherical-Bessel zeros = enclosure acoustic eigenvalues `k_{ℓn}·R`:

| ℓ | 1st | 2nd | 3rd | 4th |
|---|---|---|---|---|
| 0 | 3.14159 | 6.28319 | 9.42478 | 12.56637 |
| 1 | 4.49341 | 7.72525 | 10.90412 | 14.06619 |
| 2 | 5.76346 | 9.09501 | 12.32294 | 15.51460 |
| 3 | 6.98793 | 10.41712 | 13.69802 | 16.92362 |

The `ℓ=0` row is **exactly `nπ`** (checked to <10⁻⁶) — a perfectly harmonic acoustic ladder.

BAO acoustic scale (Planck 2018, sound horizon at the drag epoch `r_s = 147.05 Mpc`):
- First node of `j₀(k·r_s)`:  `k₁ = π/r_s = 0.02136 Mpc⁻¹`.
- BAO wiggle period in `P(k)`:  `Δk = 2π/r_s = 0.04273 Mpc⁻¹`.
- Real-space feature (filament/clustering scale):  `≈ r_s = 147.05 Mpc ≈ 99.6 h⁻¹ Mpc` — the famous **~100 h⁻¹ Mpc** BAO bump seen in galaxy surveys.

## Why this matters for the spine
Mainstream cosmology already agrees that the web's characteristic spacing is set by an **acoustic standing wave** frozen at recombination. The worked check shows that the very same object — *zeros of `j_ℓ`* — is what gives any spherical enclosure its tone. So reading the filament web as "the pattern acoustics in a spherical enclosure produce" is not a metaphor; it is the same eigenvalue problem evaluated at cosmological scale. That makes ID7257 → ID7259 the **most defensible, citable node** of the spine.

## Files
- `wolfram/bao_enclosure_acoustics_check.wl` — runnable check (uses `BesselJZero[ℓ+1/2, k]`), exports `bao_enclosure_acoustics_results.json`.
