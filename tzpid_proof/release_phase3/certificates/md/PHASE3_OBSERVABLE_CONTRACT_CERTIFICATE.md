# Phase3 Observable Contract Certificate

Generated: 2026-06-08

## Claim

The Phase3 HDF5 observable `field/psi_real`, slice `0`, in `delta_alpha_phase3.h5` is a shell-bearing Delta-alpha observable whose extracted radial shell peaks match the Bessel-derived shell prediction within the declared tolerance.

## Inputs

- HDF5 source: `delta_alpha_phase3.h5`
- Dataset: `field/psi_real`
- Slice: `0`
- Python comparison report: `phase2_checks/delta_alpha_phase3_field_psi_real_slice_0/delta_alpha_shell_comparison.json`
- Isabelle contract: `isabelle_tzpid/TZPID_Phase3_Observable_Contract.thy`

## Certificate Values

| Shell | Predicted radius | Observed radius | Absolute error | Relative error |
|---:|---:|---:|---:|---:|
| 1 | 0.6437903504411578 | 0.6503490462418080 | 0.0065586958006502 | 1.0187626757927963% |
| 2 | 1.2875807008823157 | 1.2888735643701286 | 0.0012928634878129 | 0.1004102878310418% |

Declared relative tolerance: `1.1%`.

Maximum absolute error: `0.0065586958006502`, below `0.007`.

## Isabelle Theorem

The contract is locked by:

```isabelle
theorem phase3_observable_contract_locked:
  "phase3_shell_bearing_observable
      ''delta_alpha_phase3.h5'' ''field/psi_real'' 0
   \<and> phase3_bessel_shell_prediction_validated
   \<and> phase3_max_absolute_error \<le> (7 / 1000 :: real)"
```

This is a certificate boundary theorem: Python performs the HDF5/radial peak extraction, while Isabelle records and checks the concrete observable identity, shell count, tolerance, and exported numeric match.
