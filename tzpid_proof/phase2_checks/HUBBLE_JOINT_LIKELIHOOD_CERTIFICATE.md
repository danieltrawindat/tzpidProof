# Hubble/Friedmann Joint Likelihood Certificate

Generated UTC: `2026-06-09T20:48:58+00:00`

Creator: Daniel Alexander Trawin

ORCID: https://orcid.org/0009-0001-4630-3715

Engine: `Python standard library`

Overall status: `pass`

## Claim Boundary

This certificate sums the locked Pantheon+ raw-covariance, Planck
distance-prior, and DESI DR2 BAO chi-square lanes over their common scenario
set. It is not a new parameter minimization, refit, or full survey likelihood.

## Input Lanes

| Lane | Status | Scenario count | Best lane scenario | JSON SHA256 |
|---|---|---:|---|---|
| pantheon_plus_raw | pass | 4 | shoes_h0_lambda_cdm_flat | `e55c69cd776d540c54d83f687f5578d73da705d59a3ac00fde4ec8d8c73f9e7c` |
| planck_distance_prior | pass | 4 | closed_breathing_lambda_cdm | `0e065176e239905f5ce8eb3485f19368e8fb777bd8e81d109f0e4607061b397f` |
| desi_dr2_bao | pass | 4 | closed_breathing_lambda_cdm | `73984765c967d4bad4b7d8eb5dff058a02a4601eb607ce5fa2377d9e84d57c81` |

## Checks

| Check | Status |
|---|---|
| `input_certificates_pass` | `pass` |
| `common_scenario_set` | `pass` |
| `finite_joint_chi2` | `pass` |
| `positive_joint_dof` | `pass` |
| `joint_scenarios_computed` | `computed` |

## Joint Scenario Ranking

| Scenario | H0 | Omega_K | w0 | wa | Pantheon chi2 | Planck chi2 | DESI chi2 | Total chi2 | Reduced total | Delta chi2 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| closed_breathing_lambda_cdm | 67.4 | -0.001 | -1 | 0 | 230.62684 | 26.945454 | 37.617889 | 295.19018 | 1.0109253 | 0 |
| planck_lambda_cdm_flat | 67.4 | 0 | -1 | 0 | 230.62476 | 102.96519 | 38.636341 | 372.2263 | 1.2747476 | 77.036116 |
| observed_summary_best_fit | 69.154569 | 0.001 | -0.838 | -0.62954933 | 230.69278 | 970.38622 | 144.77104 | 1345.85 | 4.6090755 | 1050.6599 |
| shoes_h0_lambda_cdm_flat | 73.04 | 0 | -1 | 0 | 230.62476 | 17285.073 | 363.61447 | 17879.312 | 61.230521 | 17584.122 |

Best scenario by joint chi-square: `closed_breathing_lambda_cdm`

Best reduced joint chi-square: `1.0109253`

## Files

- JSON certificate: `phase2_checks/HUBBLE_JOINT_LIKELIHOOD_CERTIFICATE.json`
- Scenario CSV: `phase2_checks/HUBBLE_JOINT_SCENARIO_CHI2.csv`

## Next Use

Promote the scenario-sum certificate into a small parameter-search lane over
`H0`, `Omega_m`, `Omega_K`, `w0`, and `wa`, while keeping this file as the
locked reproducibility baseline.
