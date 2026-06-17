# Hubble/Pantheon+ Raw Likelihood Certificate

Generated UTC: `2026-06-09T20:49:12+00:00`

Creator: Daniel Alexander Trawin

ORCID: https://orcid.org/0009-0001-4630-3715

Engine: `Python + numpy`

Overall status: `pass`

## Claim Boundary

This is the first raw-likelihood lane for the Hubble/Friedmann branch. It uses
the public Pantheon+SH0ES distance table and the full STAT+SYS covariance
submatrix for the selected Hubble-flow rows. It does not yet include Planck
distance priors or DESI BAO covariance tables.

## Data Source

- Repository: `PantheonPlusSH0ES/DataRelease`
- Data: https://raw.githubusercontent.com/PantheonPlusSH0ES/DataRelease/main/Pantheon%2B_Data/4_DISTANCES_AND_COVAR/Pantheon%2BSH0ES.dat
- Covariance: https://raw.githubusercontent.com/PantheonPlusSH0ES/DataRelease/main/Pantheon%2B_Data/4_DISTANCES_AND_COVAR/Pantheon%2BSH0ES_STAT%2BSYS.cov
- README: https://raw.githubusercontent.com/PantheonPlusSH0ES/DataRelease/main/Pantheon%2B_Data/4_DISTANCES_AND_COVAR/README
- Data SHA256: `1cb0fc379ef066afdc2ffd1857681cc478024570d8a3eba284fb645775198cf8`
- Covariance SHA256: `abf806d966485e64afdb359c87bffc0ecc00d05eff0a31ced66f247385df0fdc`

## Data Shape

```json
{
  "columns": [
    "CID",
    "IDSURVEY",
    "zHD",
    "zHDERR",
    "zCMB",
    "zCMBERR",
    "zHEL",
    "zHELERR",
    "m_b_corr",
    "m_b_corr_err_DIAG",
    "MU_SH0ES",
    "MU_SH0ES_ERR_DIAG",
    "CEPH_DIST",
    "IS_CALIBRATOR",
    "USED_IN_SH0ES_HF",
    "c",
    "cERR",
    "x1",
    "x1ERR",
    "mB",
    "mBERR",
    "x0",
    "x0ERR",
    "COV_x1_c",
    "COV_x1_x0",
    "COV_c_x0",
    "RA",
    "DEC",
    "HOST_RA",
    "HOST_DEC",
    "HOST_ANGSEP",
    "VPEC",
    "VPECERR",
    "MWEBV",
    "HOST_LOGMASS",
    "HOST_LOGMASS_ERR",
    "PKMJD",
    "PKMJDERR",
    "NDOF",
    "FITCHI2",
    "FITPROB",
    "m_b_corr_err_RAW",
    "m_b_corr_err_VPEC",
    "biasCor_m_b",
    "biasCorErr_m_b",
    "biasCor_m_b_COVSCALE",
    "biasCor_m_b_COVADD"
  ],
  "total_rows": 1701,
  "covariance_rows": 1701,
  "selected_hubble_flow_rows": 277,
  "selection": "USED_IN_SH0ES_HF == 1 and zHD > 0.01 and MU_SH0ES > 0",
  "covariance": "STAT+SYS submatrix for selected rows",
  "min_covariance_eigenvalue": 0.005295993328634684,
  "max_covariance_eigenvalue": 0.21561464836811584
}
```

## Checks

| Check | Status |
|---|---|
| `downloaded_public_pantheonplus_files` | `pass` |
| `data_covariance_shape_match` | `pass` |
| `selected_covariance_positive_definite` | `pass` |
| `finite_full_covariance_chi2` | `pass` |
| `scenario_likelihoods_computed` | `computed` |

## Scenario Full-Covariance Chi-Square

| Scenario | H0 | Omega_K | w0 | wa | Chi2 | DoF | Reduced chi2 | Profiled offset mag |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| planck_lambda_cdm_flat | 67.4 | 0 | -1 | 0 | 230.62476 | 276 | 0.83559697 | 0.18214538 |
| closed_breathing_lambda_cdm | 67.4 | -0.001 | -1 | 0 | 230.62684 | 276 | 0.83560448 | 0.18220742 |
| observed_summary_best_fit | 69.154569 | 0.001 | -0.838 | -0.62954933 | 230.69278 | 276 | 0.83584342 | 0.11726047 |
| shoes_h0_lambda_cdm_flat | 73.04 | 0 | -1 | 0 | 230.62476 | 276 | 0.83559697 | 0.0076410404 |

Best scenario by chi-square: `shoes_h0_lambda_cdm_flat`

## Files

- JSON certificate: `phase2_checks/HUBBLE_PANTHEONPLUS_RAW_LIKELIHOOD_CERTIFICATE.json`
- Scenario CSV: `phase2_checks/HUBBLE_PANTHEONPLUS_RAW_SCENARIO_CHI2.csv`
- Raw cache: `phase2_checks/raw_data_cache/pantheon_plus/` (ignored by git)

## Next Use

Add companion raw lanes for Planck/CMB distance priors and DESI DR2 BAO
covariance tables, then combine their chi-square terms with this Pantheon+
likelihood in one joint certificate.
