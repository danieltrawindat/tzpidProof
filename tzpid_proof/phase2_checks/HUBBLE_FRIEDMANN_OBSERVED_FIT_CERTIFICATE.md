# Hubble/Friedmann Observed-Fit Certificate

Generated UTC: `2026-06-09T20:49:11+00:00`

Creator: Daniel Alexander Trawin

ORCID: https://orcid.org/0009-0001-4630-3715

Engine: `Python standard library`

Overall status: `pass`

## Claim Boundary

This is a published-summary residual scaffold. It is not a raw likelihood and
does not include covariance matrices. It turns the prior CPL parameter anchor
lane into a concrete observed-data residual lane over `H0`, `Omega_m`,
`Omega_K`, `w0`, and `wa`.

## Checks

| Check | Status |
|---|---|
| `positive_uncertainties` | `pass` |
| `finite_residuals` | `pass` |
| `parameter_coverage_H0_Omega_m_Omega_K_w0_wa` | `pass` |
| `summary_fit_computed` | `computed` |

## Observed Summary Constraints

| Probe | Parameter | Observed | Sigma | Source |
|---|---|---:|---:|---|
| CMB | H0 | 67.4 | 0.5 | Planck 2018 VI base-LambdaCDM |
| CMB | Omega_m | 0.315 | 0.007 | Planck 2018 VI base-LambdaCDM |
| CMB+BAO | Omega_K | 0.001 | 0.002 | Planck 2018 VI joint curvature constraint |
| SN distance ladder | H0 | 73.04 | 1.04 | SH0ES 2022 |
| SN+Cepheid | H0 | 73.3 | 1.1 | Pantheon+ with SH0ES |
| DESI DR2+CMB+Pantheon+ | w0 | -0.838 | 0.055 | DESI DR2 summary constraint |
| DESI DR2+CMB+Pantheon+ | wa | -0.62 | 0.205 | DESI DR2 summary constraint |
| Pantheon+ CMB+BAO | wa | -0.65 | 0.3 | Pantheon+ cosmological constraints |

## Diagonal Weighted Parameter Summary

| Parameter | Fit value | Fit sigma | Constraints | Chi2 | DoF | Reduced chi2 |
|---|---:|---:|---:|---:|---:|---:|
| H0 | 69.154569 | 0.41699248 | 3 | 40.473828 | 2 | 20.236914 |
| Omega_m | 0.315 | 0.007 | 1 | 0 | 0 | n/a |
| Omega_K | 0.001 | 0.002 | 1 | 0 | 0 | n/a |
| w0 | -0.838 | 0.055 | 1 | 0 | 0 | n/a |
| wa | -0.62954933 | 0.16925715 | 2 | 0.0068168907 | 1 | 0.0068168907 |

## Locked Scenario Residuals

| Scenario | Chi2 | DoF | Reduced chi2 | Max abs pull sigma |
|---|---:|---:|---:|---:|
| planck_lambda_cdm_flat | 80.945442 | 8 | 10.11818 | 5.4230769 |
| closed_breathing_lambda_cdm | 81.695442 | 8 | 10.21193 | 5.4230769 |
| dynamic_cpl_demo | 86.602913 | 8 | 10.825364 | 5.4230769 |

## Best-Fit Summary Point

```json
{
  "H0": 69.15456889642843,
  "Omega_m": 0.315,
  "Omega_K": 0.001,
  "w0": -0.838,
  "wa": -0.6295493277788298
}
```

## Sources

- Planck 2018 VI base-LambdaCDM: https://arxiv.org/abs/1807.06209
- Planck 2018 VI base-LambdaCDM: https://arxiv.org/abs/1807.06209
- Planck 2018 VI joint curvature constraint: https://www.aanda.org/articles/aa/abs/2020/09/aa33910-18/aa33910-18.html
- SH0ES 2022: https://ui.adsabs.harvard.edu/abs/2022ApJ...934L...7R/abstract
- Pantheon+ with SH0ES: https://arxiv.org/abs/2202.04077
- DESI DR2 summary constraint: https://academic.oup.com/nsr/article/13/10/nwag115/8497412
- DESI DR2 summary constraint: https://academic.oup.com/nsr/article/13/10/nwag115/8497412
- Pantheon+ cosmological constraints: https://arxiv.org/abs/2202.04077

## Files

- Observed constraints: `phase2_checks/HUBBLE_FRIEDMANN_OBSERVED_SUMMARY_CONSTRAINTS.csv`
- Certificate JSON: `phase2_checks/HUBBLE_FRIEDMANN_OBSERVED_FIT_CERTIFICATE.json`

## Next Use

Replace these diagonal summary constraints with raw CMB distance priors, DESI
BAO distance-ratio covariance tables, and Pantheon+ supernova likelihood data.
That will promote this from a summary residual scaffold into a true joint
likelihood lane.
