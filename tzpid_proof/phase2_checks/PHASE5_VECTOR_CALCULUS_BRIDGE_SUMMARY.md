# Phase 5 Vector Calculus Bridge Summary

- Source HDF5: `delta_alpha_phase5_vector_calculus.h5`
- Description: Δα phase gradient, vector calculus, curl (vorticity), and gyromagnetic correspondence
- Creator: Daniel Alexander Trawin
- ORCID: https://orcid.org/0009-0001-4630-3715
- Gradient definition: grad(Δα)
- Curl definition: ∇ × ∇Δα (expected 0 except singularity)
- Physical interpretation: curl reveals topological vorticity core
- Delta: `0.180106021133507`
- Delta contract `0.18 < delta < 0.19`: `True`

## Numerical Contracts

- Curl max absolute value: `1.771383e-11`
- Curl standard deviation: `3.081535e-13`
- Mean gradient magnitude: `6.870104`
- Max gradient magnitude: `625.779025`
- `psi_real^2 + psi_imag^2 = 1` mean absolute error: `3.038333e-17`
- `psi_real^2 + psi_imag^2 = 1` max absolute error: `2.220446e-16`
- `Lz` standard deviation: `2.317575e-13`

## Dataset Inventory

| Dataset | Shape | Min | Max | Mean | Std | Max Abs |
|---|---:|---:|---:|---:|---:|---:|
| `field/Delta_alpha` | `400x400` | `-2.920187e+00` | `9.257328e+00` | `3.743381e+00` | `2.280120e+00` | `9.257328e+00` |
| `field/Lz` | `400x400` | `9.999998e-01` | `9.999998e-01` | `9.999998e-01` | `2.317575e-13` | `9.999998e-01` |
| `field/psi_real` | `400x400` | `-1.000000e+00` | `1.000000e+00` | `-4.547474e-17` | `7.071068e-01` | `1.000000e+00` |
| `field/psi_imag` | `400x400` | `-1.000000e+00` | `1.000000e+00` | `-1.136868e-17` | `7.071068e-01` | `1.000000e+00` |
| `vector/grad_x` | `400x400` | `-2.050684e+02` | `2.050684e+02` | `1.818989e-16` | `4.126946e+00` | `2.050684e+02` |
| `vector/grad_y` | `400x400` | `-7.394115e+01` | `6.257600e+02` | `1.566869e+00` | `3.126538e+01` | `6.257600e+02` |
| `vector/curl_z` | `400x400` | `-1.771383e-11` | `1.523848e-11` | `1.939083e-17` | `3.081535e-13` | `1.771383e-11` |
| `grid/R` | `400x400` | `3.544395e-03` | `1.414214e+00` | `7.671117e-01` | `2.855662e-01` | `1.414214e+00` |

## Interpretation

This artifact advances the Phase 4 phase-gradient bridge into vector-calculus language. The gradient datasets give the local vector field induced by `Delta_alpha`; `curl_z` is numerically zero to floating-point tolerance, matching the HOL identity that the curl of an exact gradient cancels when mixed partials agree. The nonzero gradient magnitude keeps the movement witness active, while `Lz` remains a correspondence invariant rather than a shell extractor.
