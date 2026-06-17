# Nested Hypersphere Typed Projection Certificate

Generated: 2026-06-08

## Claim

The nested-hypersphere spine now has an explicit typed projection-map layer in Isabelle/HOL.

The older focus file records the registry-backed abstract spine. The new typed theory gives the projection mechanism concrete finite-coordinate semantics:

- bulk carrier: four real coordinates, interpreted as the algebraic S3 carrier boundary
- boundary carrier: three real coordinates
- projection map: `hs_project_down scale point = map (\<lambda>x. scale * x) (take 3 point)`
- dimensionless-ratio preservation under nonzero projection scale
- harmonic ladder ratio preservation
- reciprocal bulk-boundary flip
- Hopf-style phase-lift equality

## Isabelle Entry Point

`isabelle_tzpid/TZPID_NestedHypersphere_Typed_Projection.thy`

Main theorem:

```isabelle
theorem hs_typed_projection_contract:
  assumes carrier: "hs_s3_carrier radius point"
    and admissible: "hs_projection_admissible scale radius"
    and fundamental_nonzero: "fundamental \<noteq> 0"
    and flip: "hs_fiber_reciprocal_flip boundary_ratio bulk_ratio"
    and lift: "hs_hopf_phase_lift boundary_holonomy fiber_rotation"
  shows
    "hs_boundary_carrier (hs_project_down scale point)
     \<and> hs_bulk_boundary_mode_preserved scale wavelength height
     \<and> hs_harmonic_frequency n fundamental / fundamental = n
     \<and> boundary_ratio * bulk_ratio = 1
     \<and> fiber_rotation - boundary_holonomy = 0"
```

Spine-extension theorem:

```isabelle
theorem nested_hypersphere_typed_projection_extends_spine
```

## Verification

Command:

```powershell
isabelle build -D .\isabelle_tzpid
```

Status: passed.

The new typed theory avoids `sorry`, `oops`, and `by simp` shortcuts.
