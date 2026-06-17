# Hubble/Planck Distance-Prior Certificate

Generated UTC: `2026-06-09T20:49:12+00:00`

Creator: Daniel Alexander Trawin

ORCID: https://orcid.org/0009-0001-4630-3715

Engine: `Python + numpy`

Overall status: `pass`

## Claim Boundary

This is a compressed Planck 2018 CMB distance-prior likelihood. It is not the
full Planck likelihood and does not include TT/TE/EE spectra or nuisance
foreground parameters.

## Source

- Paper: Distance Priors from Planck Final Release
- arXiv: https://arxiv.org/abs/1808.05724
- TeX source SHA256: `b63854bd0fd48bd80d6bff224be64b3ab0bb0b8a730486da04bf2fc2883e2888`

## Distance Prior

Vector order: `R`, `l_A`, `Omega_b h^2`

```json
{
  "vector_order": [
    "R",
    "l_A",
    "Omega_b h^2"
  ],
  "mean": [
    1.750235,
    301.4707,
    0.02235976
  ],
  "inverse_covariance": [
    [
      94392.3971,
      -1360.4913,
      1664517.2916
    ],
    [
      -1360.4913,
      161.4349,
      3671.618
    ],
    [
      1664517.2916,
      3671.618,
      79719182.5162
    ]
  ],
  "min_inverse_covariance_eigenvalue": 126.5594530897572,
  "max_inverse_covariance_eigenvalue": 79753963.409895
}
```

## Checks

| Check | Status |
|---|---|
| `downloaded_arxiv_source` | `pass` |
| `tex_literals_match_distance_prior_values` | `pass` |
| `inverse_covariance_positive_definite` | `pass` |
| `finite_distance_prior_chi2` | `pass` |
| `scenario_distance_priors_computed` | `computed` |

## Scenario Distance-Prior Chi-Square

| Scenario | H0 | Omega_K | w0 | wa | R | l_A | Chi2 |
|---|---:|---:|---:|---:|---:|---:|---:|
| planck_lambda_cdm_flat | 67.4 | 0 | -1 | 0 | 1.7494952 | 302.26292 | 102.96519 |
| closed_breathing_lambda_cdm | 67.4 | -0.001 | -1 | 0 | 1.7470852 | 301.84642 | 26.945454 |
| observed_summary_best_fit | 69.154569 | 0.001 | -0.838 | -0.62954933 | 1.7526 | 299.03948 | 970.38622 |
| shoes_h0_lambda_cdm_flat | 73.04 | 0 | -1 | 0 | 1.7507458 | 291.12748 | 17285.073 |

Best scenario by chi-square: `closed_breathing_lambda_cdm`

## Files

- JSON certificate: `phase2_checks/HUBBLE_PLANCK_DISTANCE_PRIOR_CERTIFICATE.json`
- Scenario CSV: `phase2_checks/HUBBLE_PLANCK_DISTANCE_PRIOR_SCENARIO_CHI2.csv`
- Raw cache: `phase2_checks/raw_data_cache/planck_distance_prior/` (ignored by git)

## Next Use

Add the DESI DR2 BAO covariance likelihood lane, then combine Planck distance
priors, Pantheon+ raw covariance, and DESI BAO into one joint chi-square
certificate.
