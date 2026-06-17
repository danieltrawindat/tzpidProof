# Phase 4 Gyromagnetic Bridge Summary

- Source HDF5: `delta_alpha_phase4_bridge.h5`
- Description: Δα ↔ Bessel ↔ ψ ↔ Lz ↔ Gyromagnetic bridge dataset
- Creator: Daniel Alexander Trawin
- ORCID: https://orcid.org/0009-0001-4630-3715
- Formal property: `0.18 < delta < 0.19`
- Delta: `0.180106021133507`
- j11: `3.83170597`
- Scale: `10.000000`
- Domain radius: `1.414213562373`
- Predicted shell radii in-domain: `0.643790`, `1.287581`

## Best Shell-Bearing Observable

- Dataset: `field/psi_real`
- Slice: `0`
- Mean absolute shell error: `0.00101692`
- Max absolute shell error: `0.00171066`
- Mean relative shell error: `0.00091529`
- Observed radii sample: `0.0164991582;0.0306412939;0.0447834295;0.0589255651;0.0730677007;0.0872098363;0.0966379268;0.1107800624;0.1249221980;0.1390643336;0.1484924240;0.1673486049`

## Dataset Roles

| Dataset | Shape | Std | Role |
|---|---:|---:|---|
| `field/psi_real` | `(8, 400, 400)` | `7.071068e-01` | shell-bearing radial observable |
| `field/psi_imag` | `(8, 400, 400)` | `7.071068e-01` | shell-bearing radial observable |
| `field/helicity_proxy` | `(8, 400, 400)` | `3.508367e-01` | shell-bearing radial observable |
| `field/Lz` | `(8, 400, 400)` | `2.330431e-13` | constant gyromagnetic correspondence witness; not used for radial shell peaks |

## Pipeline Contract

This Phase 4 bridge keeps the Phase 3 Bessel drop contract (`0.18 < delta < 0.19`) and extends it into the gyromagnetic movement layer through `ψ`, helicity proxy, and `Lz` datasets. The radial-shell certificate should be read from `psi_real`, `psi_imag`, or `helicity_proxy`; `Lz` is effectively constant in this artifact and is therefore a correspondence/invariant witness rather than a shell extractor.
