---
creator: Daniel Alexander Trawin
orcid: https://orcid.org/0009-0001-4630-3715
generated: 2026-06-11
lane: empirical_cosmology_compressed_fit
registry_focus: ID10867, ID10868, ID10871
---

# Spartan Dawn Certificate

This folder is an empirical compressed-data test lane for the Hubble/Friedmann breathing spine.

It tests four cosmological models against:

- 13 DESI DR2 BAO distance measurements;
- the Planck CMB acoustic angle `100 theta_* = 1.04109`;
- a Pantheon+ supernova shape prior `Omega_m = 0.334 +/- 0.018`.

The executable certificate is:

```powershell
python D:\TZPIDProof\this_is_SPARTA\TZPID_spartan_dawn_fit.py
```

Run output is stored in:

```text
D:\TZPIDProof\this_is_SPARTA\spartan_fit.json
```

## Current Results

| Model | chi^2 | params | AIC | Best-fit summary |
|---|---:|---:|---:|---|
| A flat LCDM | 16.1294 | 2 | 20.1294 | H0=68.81, Omega_m=0.2975 |
| B closed LCDM | 14.4434 | 3 | 20.4434 | Omega_K=+0.0040 |
| C flat w0waCDM | 7.5085 | 4 | 15.5085 | w0=-0.6074, wa=-1.3614 |
| D closed breathing | 7.0541 | 5 | 17.0541 | Omega_K=-0.0046, w0=-0.5597, wa=-1.3744 |

Relative to flat LCDM:

- closed LCDM improves raw `chi^2` by `-1.69` but loses on AIC by `+0.31`;
- flat dynamic breathing improves raw `chi^2` by `-8.62` and AIC by `-4.62`;
- closed dynamic breathing gives the best raw `chi^2`, but the curvature term is small and does not carry the improvement.

## Sound-First Check

The script computes the sound horizon using the stable scale-factor integral with neutrino-corrected radiation:

```text
Omega_r = Omega_gamma * (1 + 0.2271 * N_eff), N_eff = 3.046
```

| Quantity | Computed | Reference |
|---|---:|---:|
| `r_s(z*)` | 144.485 Mpc | Planck `144.39 Mpc` |
| `r_s(drag)` | 147.128 Mpc | BAO ruler `147.09 Mpc` |

This supports the paper-facing phrase "sound before light" in the precise cosmological sense: the BAO standard ruler is an acoustic horizon formed before CMB photon decoupling.

## Hubble-As-Breathing Check

The pasted hypersphere framing has been applied directly to the executable lane:

```text
H(t) = R_dot(t)/R(t)
V_S3 = 2*pi^2*R^3
V_dot/V = 3H
```

| Hubble value | `H0` as breathing rate | `V_dot/V` |
|---|---:|---:|
| Planck-like `67.4 km/s/Mpc` | `0.0689/Gyr` | `0.2068/Gyr` |
| Local-distance-network-like `73.50 km/s/Mpc` | `0.0752/Gyr` | `0.2255/Gyr` |
| Best flat LCDM fit here | `0.0704/Gyr` | `0.2111/Gyr` |
| Best closed-breathing fit here | `0.0664/Gyr` | `0.1993/Gyr` |

The closed-hypersphere curvature radius carrier is:

```text
R_c = c/(H0*sqrt(|Omega_K|))
```

| Curvature case | Radius |
|---|---:|
| Best closed-breathing fit, `Omega_K=-0.0046` | `222.9 Gly` |
| Reference `|Omega_K|=0.0018`, `H0=67.4` | `341.9 Gly` |
| Reference `|Omega_K|=0.0020`, `H0=67.4` | `324.4 Gly` |
| Reference `|Omega_K|=0.0040`, `H0=67.4` | `229.4 Gly` |

This is the correct application of the hypersphere argument: the universe may be represented as metric breathing of an enormous, nearly flat-looking enclosure, but the data do not force closed curvature.

## Interpretation

The compressed-statistics test supports:

- ID10867: `H0 = Rdot/R` as a breathing-rate interpretation;
- ID10868: present dark-energy normalization as a present-value constraint;
- ID10871: dynamic Friedmann breathing via `F(a)` as empirically favored over flat LCDM in this compressed test.

The result does not prove a closed hypersphere is required. The curvature parameter remains small and weakly constrained. The improvement is carried by dynamic dark energy / breathing pressure, not by curvature alone.

## Limitations

This is not a full CMB likelihood or Boltzmann-code MCMC. It is a compressed-statistics fit intended to test whether the breathing Friedmann spine is empirically viable enough to keep in the proof package.

Paper-facing language should say:

> The compressed CMB+BAO+SNe test favors dynamic breathing over flat LCDM in this simplified fit, while leaving closed curvature permitted but not required.

It should not say:

> This proves the Big Bang is false.
