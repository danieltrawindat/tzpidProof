# Hubble/Friedmann CPL Certificate

Generated UTC: `2026-06-09T20:48:58+00:00`

Creator: Daniel Alexander Trawin

ORCID: https://orcid.org/0009-0001-4630-3715

Engine: `Python standard library`

Overall status: `pass`

## Claim Boundary

This is a computational scaffold and parameter-style anchor set. It does not
claim an observational fit. It locks the dynamic dark-energy carrier used by
the Hubble-breathing Friedmann bridge.

## Equations

```text
w(a) = w0 + wa(1 - a)
F(a) = exp(3 integral_a^1 (1 + w(a'))/a' da')
F(a) = a^(-3(1+w0+wa)) exp(3 wa (a-1))
E(z)^2 = Omega_r a^-4 + Omega_m a^-3 + Omega_K a^-2 + Omega_X F(a)
```

## Checks

| Check | Status |
|---|---|
| `cpl_closed_form_matches_quadrature` | `pass` |
| `present_epoch_component_normalization` | `pass` |
| `lambda_cdm_F_is_unity` | `pass` |
| `closed_breathing_has_negative_omega_k` | `pass` |

## Scenarios

| Scenario | Role | Omega_r | Omega_m | Omega_K | Omega_X | w0 | wa |
|---|---|---:|---:|---:|---:|---:|---:|
| lambda_cdm_flat_anchor | Planck-style flat LambdaCDM reference carrier | 9.2e-05 | 0.315 | 0 | 0.684908 | -1 | 0 |
| closed_breathing_anchor | Closed-enclosure Friedmann carrier with small negative Omega_K | 9.2e-05 | 0.315 | -0.001 | 0.685908 | -1 | 0 |
| dynamic_cpl_demo | Non-fit CPL scaffold for future CMB/BAO/SN parameter scans | 9.2e-05 | 0.315 | 0 | 0.684908 | -0.95 | 0.2 |

## Parameter-Style Anchors

| Scenario | Anchor | z | a | F(a) | E(z) | H(z) km/s/Mpc |
|---|---|---:|---:|---:|---:|---:|
| lambda_cdm_flat_anchor | local_sn_low_z | 0.1 | 0.90909091 | 1 | 1.0508605 | 70.827995 |
| lambda_cdm_flat_anchor | bao_boss_like_mid_z | 0.57 | 0.63694268 | 1 | 1.3800302 | 93.014033 |
| lambda_cdm_flat_anchor | cmb_last_scattering_proxy | 1089 | 0.00091743119 | 1 | 23190.508 | 1563040.2 |
| closed_breathing_anchor | local_sn_low_z | 0.1 | 0.90909091 | 1 | 1.0507605 | 70.82126 |
| closed_breathing_anchor | bao_boss_like_mid_z | 0.57 | 0.63694268 | 1 | 1.3794993 | 92.978254 |
| closed_breathing_anchor | cmb_last_scattering_proxy | 1089 | 0.00091743119 | 1 | 23190.482 | 1563038.5 |
| dynamic_cpl_demo | local_sn_low_z | 0.1 | 0.90909091 | 1.0170814 | 1.0564123 | 71.202188 |
| dynamic_cpl_demo | bao_boss_like_mid_z | 0.57 | 0.63694268 | 1.1280295 | 1.4114431 | 95.131267 |
| dynamic_cpl_demo | cmb_last_scattering_proxy | 1089 | 0.00091743119 | 104.1675 | 23190.509 | 1563040.3 |

## Files

- JSON: `phase2_checks/HUBBLE_FRIEDMANN_CPL_CERTIFICATE.json`
- CSV: `phase2_checks/HUBBLE_FRIEDMANN_CPL_ANCHORS.csv`

## Next Use

This certificate can be promoted into a real fit lane by replacing the anchor
redshifts with an observed CMB/BAO/SN data table and minimizing residuals over
`H0`, `Omega_m`, `Omega_K`, `w0`, and `wa`.
