# Delta Alpha Array Bundle

Generated arrays:

- `delta_alpha.npy`: linear Bessel-derived radial phase.
- `delta_alpha_shell_cos.npy`: theorem-aligned shell field, `cos(scale * delta_alpha)`.
- `delta_alpha_osc.npy`: shell-generating sine field, `sin(2*pi*delta_alpha)`.
- `delta_alpha_log.npy`: log-periodic scale field.
- `delta_phi.npy`: EM/Lz phase driver, `A*pi*delta_alpha_osc`.
- `j_total_abs.npy`, `j_total_phase.npy`: coupled source-field observables.

## Constants

- `j11`: `3.83170597`
- `delta`: `0.18010602113350746`
- `domain_radius`: `1.4142135623730951`
- `oscillation_scale`: `10.0`
