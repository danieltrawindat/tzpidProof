# Delta Alpha Shell Radius Comparison

External-field shell comparison:

`Delta alpha_s(r) = scale * j11 * delta * r / R`

`r_n = n*pi*R/(scale*j11*delta)`

## Summary

- `grid_size`: `500`
- `domain_half_width`: `1.0`
- `domain_radius`: `1.4142135623730951`
- `radial_bins`: `300`
- `oscillation_scale`: `10.0`
- `peak_height_fraction`: `0.1`
- `damping`: `2.0`
- `profile_mode`: `raw_abs`
- `field_source`: `external`
- `j11`: `3.83170597`
- `j_half`: `3.141592653589793`
- `delta`: `0.18010602113350746`
- `detected_peaks`: `2`
- `mean_absolute_error`: `0.0015608740215339867`
- `max_absolute_error`: `0.0018288845552550947`
- `mean_relative_error`: `0.0019224552662721038`
- `field_file`: `phase2_checks\delta_alpha_arrays\delta_alpha_shell_cos.npy`

## Shells

| n | predicted radius | observed radius | absolute error | relative error |
|---:|---:|---:|---:|---:|
| 1 | 0.643790 | 0.645619 | 0.001829 | 0.284081% |
| 2 | 1.287581 | 1.288874 | 0.001293 | 0.100410% |
