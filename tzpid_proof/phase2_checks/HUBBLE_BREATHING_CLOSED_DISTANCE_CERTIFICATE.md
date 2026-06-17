# Hubble Breathing Closed-Distance Certificate

Generated: 2026-06-08

Creator: Daniel Alexander Trawin  
ORCID: https://orcid.org/0009-0001-4630-3715

## Source Bridge

- Prior certificate: `phase2_checks/HUBBLE_BREATHING_ENCLOSURE_CERTIFICATE.md`
- HOL layer: `isabelle_tzpid/TZPID_HubbleBreathing_ClosedDistance.thy`
- Spine synthesis: `D:\00_Engine\AI_Workspaces\OpenAI2\new_gold_spines\TZPID_HUBBLE_BREATHING_OF_THE_ENCLOSURE.md`

## Purpose

This certificate locks the **observable closed-geometry fingerprint** of the
Hubble-breathing enclosure model.

The previous bridge proved the breathing clock:

```text
H = Rdot/R
Vdot/V = 3H
rho(R) scales as R^-4
```

This bridge adds the distance observable:

```text
flat transverse distance   = a0 * chi
closed transverse distance = a0 * sin(chi)
```

Therefore the angular-diameter distance changes from:

```text
D_A_flat   = a0 * chi      / (1 + z)
D_A_closed = a0 * sin chi  / (1 + z)
```

The `sin(chi)` replacement is the measurable curvature fingerprint.

## HOL-Proved Core

The Isabelle theory proves:

1. Closed transverse distance uses `sin chi`.
2. Flat transverse distance uses `chi`.
3. The residual has the closed form:

```text
D_A_closed - D_A_flat = a0 * (sin chi - chi)/(1 + z)
```

4. The ratio of closed to flat distance is:

```text
D_A_closed / D_A_flat = sin chi / chi
```

assuming `a0 != 0`, `chi != 0`, and `1 + z != 0`.

5. The residual vanishes exactly when the curvature fingerprint vanishes:

```text
sin chi - chi = 0
```

6. Etherington-style luminosity-distance conversion is represented algebraically:

```text
D_L = (1 + z)^2 * D_A
```

## Main Theorems

- `hb_closed_distance_residual_closed_form`
- `hb_closed_flat_ratio`
- `hb_closed_distance_residual_zero_iff_fingerprint_zero`
- `hb_closed_distance_fingerprint_contract`
- `closed_distance_extends_hubble_breathing_spine`

## Interpretation

This is the first test-facing layer after the Hubble-breathing algebra. It says:

```text
If the enclosure is globally closed S3, the distance-redshift relation carries
a sin(chi) curvature term.
```

This is where the breathing model becomes observational. CMB acoustic scale,
BAO distance ladders, supernova luminosity distances, and redshift drift all
probe this geometry through distance-redshift relations.

## Demarcation

- **Proved in HOL:** exact algebraic relation between flat and closed distance
  forms; residual; ratio; luminosity conversion formula.
- **Certificate-level mathematical context:** for small local `chi`,
  `sin chi approximately chi`, so a sufficiently large closed universe appears
  locally flat. This is standard analysis but not needed for the exact algebraic
  lock.
- **Physical interpretation:** if the universe is a very large closed S3, local
  observations can look nearly flat while global distance measurements may retain
  a small `sin chi` curvature fingerprint.

## Best Next Move

The next formal lift is a typed Friedmann component model:

```text
H^2(a) = H0^2[Omega_r a^-4 + Omega_m a^-3 + Omega_K a^-2 + Omega_X F(a)]
Omega_K < 0 for closed geometry
```

Then connect the distance fingerprint to the dynamic breathing / dark-energy
component `F(a)`.

