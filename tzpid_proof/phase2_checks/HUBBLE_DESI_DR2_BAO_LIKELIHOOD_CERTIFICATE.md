# Hubble/DESI DR2 BAO Certificate

Generated UTC: `2026-06-09T20:49:11+00:00`

Creator: Daniel Alexander Trawin

ORCID: https://orcid.org/0009-0001-4630-3715

Engine: `Python + numpy`

Overall status: `pass`

## Claim Boundary

This is a Gaussian DESI DR2 BAO distance-ratio likelihood over `DV/rd`,
`DM/rd`, and `DH/rd`. It is not a full joint cosmological fit.

## Source

- CosmoSIS module: https://raw.githubusercontent.com/cosmosis-developers/cosmosis-standard-library/main/likelihood/bao/desi-dr2/desi_dr2.py
- CosmoSIS metadata: https://raw.githubusercontent.com/cosmosis-developers/cosmosis-standard-library/main/likelihood/bao/desi-dr2/module.yaml
- DESI DR2 BAO paper: https://arxiv.org/abs/2503.14738
- Module SHA256: `72052ff2def5c3350e01833bd8a0782d53d1712bda2c6aa17cdecb9f03b894b2`

## Checks

| Check | Status |
|---|---|
| `downloaded_cosmosis_module` | `pass` |
| `parsed_embedded_desi_dataset_table` | `pass` |
| `source_references_desi_dr2` | `pass` |
| `default_measurement_shape_matches` | `pass` |
| `covariance_positive_definite` | `pass` |
| `finite_bao_chi2` | `pass` |
| `scenario_bao_likelihoods_computed` | `computed` |

## DESI BAO Measurement Vector

| Dataset | Observable | z_eff | Mean | Sigma | Correlation partner | Correlation |
|---|---|---:|---:|---:|---|---:|
| BGS | DV_over_rd | 0.295 | 7.944 | 0.075 |  |  |
| LRG1 | DM_over_rd | 0.510 | 13.587 | 0.169 | DH_over_rd | -0.475 |
| LRG1 | DH_over_rd | 0.510 | 21.863 | 0.427 | DM_over_rd | -0.475 |
| LRG2 | DM_over_rd | 0.706 | 17.347 | 0.18 | DH_over_rd | -0.423 |
| LRG2 | DH_over_rd | 0.706 | 19.458 | 0.332 | DM_over_rd | -0.423 |
| LRG3+ELG1 | DM_over_rd | 0.934 | 21.574 | 0.153 | DH_over_rd | -0.425 |
| LRG3+ELG1 | DH_over_rd | 0.934 | 17.641 | 0.193 | DM_over_rd | -0.425 |
| ELG2 | DM_over_rd | 1.321 | 27.605 | 0.32 | DH_over_rd | -0.437 |
| ELG2 | DH_over_rd | 1.321 | 14.178 | 0.217 | DM_over_rd | -0.437 |
| QSO | DM_over_rd | 1.484 | 30.519 | 0.758 | DH_over_rd | -0.489 |
| QSO | DH_over_rd | 1.484 | 12.816 | 0.513 | DM_over_rd | -0.489 |
| Lya | DM_over_rd | 2.330 | 38.988 | 0.531 | DH_over_rd | -0.431 |
| Lya | DH_over_rd | 2.330 | 8.632 | 0.101 | DM_over_rd | -0.431 |

## Scenario BAO Chi-Square

| Scenario | H0 | Omega_K | w0 | wa | rd Mpc | Chi2 | Reduced Chi2 |
|---|---:|---:|---:|---:|---:|---:|---:|
| planck_lambda_cdm_flat | 67.4 | 0 | -1 | 0 | 150.57689 | 38.636341 | 2.9720262 |
| closed_breathing_lambda_cdm | 67.4 | -0.001 | -1 | 0 | 150.57695 | 37.617889 | 2.8936838 |
| observed_summary_best_fit | 69.154569 | 0.001 | -0.838 | -0.62954933 | 148.55909 | 144.77104 | 11.136234 |
| shoes_h0_lambda_cdm_flat | 73.04 | 0 | -1 | 0 | 144.26184 | 363.61447 | 27.970344 |

Best scenario by chi-square: `closed_breathing_lambda_cdm`

## Files

- JSON certificate: `phase2_checks/HUBBLE_DESI_DR2_BAO_LIKELIHOOD_CERTIFICATE.json`
- Scenario CSV: `phase2_checks/HUBBLE_DESI_DR2_BAO_SCENARIO_CHI2.csv`
- Measurement CSV: `phase2_checks/HUBBLE_DESI_DR2_BAO_MEASUREMENTS.csv`
- Raw cache: `phase2_checks/raw_data_cache/desi_dr2_bao/` (ignored by git)

## Next Use

Combine DESI DR2 BAO, Planck distance priors, and Pantheon+ raw covariance into
one joint Hubble/Friedmann chi-square certificate.
