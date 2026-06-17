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
- `detected_peaks`: `75`
- `predicted_shells_in_domain`: `2`
- `mean_absolute_error`: `0.00392577964423152`
- `max_absolute_error`: `0.0065586958006501606`
- `mean_relative_error`: `0.005595864818119191`
- `field_file`: `delta_alpha_phase3.h5`
- `hdf5_dataset`: `field/psi_real`
- `slice_index`: `0`

## Shells

| n | predicted radius | observed radius | absolute error | relative error |
|---:|---:|---:|---:|---:|
| 1 | 0.643790 | 0.650349 | 0.006559 | 1.018763% |
| 2 | 1.287581 | 1.288874 | 0.001293 | 0.100410% |
