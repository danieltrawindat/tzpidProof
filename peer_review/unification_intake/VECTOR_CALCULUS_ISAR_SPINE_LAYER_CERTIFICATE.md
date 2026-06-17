# Vector Calculus Isar Spine Layer Certificate

Generated: 2026-06-11

## Result

An Isar-facing vector-calculus layer has been added to the Isabelle/HOL proof
package.  It does not mint new registry IDs and does not replace the existing
algebraic carrier theories.  Its purpose is to make the spine-level vector
calculus readable as a structured proof layer.

## New Isabelle Artifacts

`D:\TZPIDProof\tzpid_proof\isabelle_tzpid\TZPID_VectorCalculus_IsarSpineLayer.thy`

`D:\TZPIDProof\tzpid_proof\isabelle_tzpid\TZPID_VectorCalculus_IntegralCarriers.thy`

The theory is imported through:

`D:\TZPIDProof\tzpid_proof\isabelle_tzpid\ROOT`

## Spine Coverage

The layer defines an eight-part vector-calculus backbone:

| Layer | Meaning |
| --- | --- |
| `VC_DeltaAlpha_Gradient` | Delta-alpha gradient and zero-curl mixed-partial closure. |
| `VC_Gyromagnetic_Lz` | Active phase gradient and nonzero angular-momentum witness. |
| `VC_Magnetic_Helicity` | Helicity density and uniform-helicity carriers. |
| `VC_Elsasser_MHD` | Ideal-MHD dissipation and Elsasser balance. |
| `VC_Torsion_Cancellation` | Opposite-twist torsion cancellation. |
| `VC_Flux_Quantization` | Flux multiple consumed by the existing quantization carrier. |
| `VC_Topological_Boundary` | Gauss-Bonnet boundary closure and topological gap guards. |
| `VC_Winding_Update` | Discrete winding index update after one full turn. |

## Main Isar Theorems

- `vector_calculus_spine_backbone_count`
- `vector_calculus_spine_names_nonempty`
- `isar_delta_alpha_gradient_curl_layer`
- `isar_gyromagnetic_lz_layer`
- `isar_magnetic_torsion_vector_layer`
- `isar_topology_vector_layer`
- `vector_calculus_isar_spine_contract`

## Integral Carrier Theorems

- `vc_rectangle_area_nonnegative`
- `vc_rect_boundary_circulation_simplifies`
- `vc_green_rectangle_constant_curl`
- `vc_incompressible_from_opposite_partials`
- `vc_helicity_density_zero_when_b_zero`
- `vc_uniform_helicity_integral_zero_density`
- `vc_quantized_flux_is_topological_locking_flux`
- `vc_quantized_flux_is_quantized`
- `vc_quantized_circulation_is_winding_index`
- `vc_corrected_winding_certificate_consumed`
- `vector_calculus_integral_carrier_contract`

## Proof Meaning

The combined contract proves, in a readable Isar sequence, that:

1. exact mixed partials collapse the planar curl;
2. an active phase vector has a nonzero component;
3. nonzero phase gradient, source offset, and coupling give a nonzero `Lz`
   witness;
4. magnetic helicity carriers close under the zero-field and zero-density
   cases;
5. ideal MHD gives zero resistive helicity dissipation;
6. Elsasser balance gives unit Elsasser number;
7. opposite twist cancels the torsion carrier;
8. topological locking is consumed by the existing flux-quantization carrier;
9. boundary curvature balance closes the Gauss-Bonnet residual;
10. topological gap protection and winding update are preserved.

The integral carrier layer adds the finite vector-calculus semantics needed by
the spines:

1. rectangle area is nonnegative for nonnegative side lengths;
2. rectangular boundary circulation equals constant-curl surface flux;
3. opposite planar partial derivatives give an incompressible divergence
   balance;
4. uniform helicity density and integral carriers close in the zero-field and
   zero-density cases;
5. quantized flux is identified with the topological-locking flux carrier;
6. quantized circulation is identified with the discrete winding index;
7. the corrected Phase 6 winding HDF5 certificate is consumed as the locked
   circulation/winding artifact.

## Verification

The Isabelle session builds cleanly with:

```powershell
D:\Isabelle2025\Isabelle2025-2\bin\isabelle build -D D:\TZPIDProof\tzpid_proof\isabelle_tzpid
```

## Consequence

The vector-calculus pieces for the gyromagnetic, magnetic/torsion, topological
locking, and flux-quantization spine lanes now have both a paper-facing Isar
layer and a finite integral-carrier layer.  The next natural refinement is to
lift selected finite-dimensional dot/cross/curl carriers toward fuller
HOL-Analysis vector-field, line-integral, and surface-integral carriers where
the publication needs that extra strength.
