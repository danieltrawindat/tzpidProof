# Operator/Spectral Carriers Certificate

- Status: `pass`
- Isabelle theory: `isabelle_tzpid/TZPID_OperatorSpectral_Carriers.thy`
- Source batch: `Operator/spectral batch 006`

| Check | Value | Expected | Pass |
|---|---:|---:|---|
| ordered_two_mode_gap_nonnegative | 2.5 | 2.5 | True |
| harmonic_ladder_adjacent_step | 2.5 | 2.5 | True |
| curvature_shift_monotone | 0.6 | 0.6 | True |
| kk_access_frequency_recovers_mode | 1199169832 | 1199169832 | True |
| full_beat_period_recovers_turn | 6.28318530718 | 6.28318530718 | True |
| semidiurnal_is_half_full_period | 5.23598775598 | 5.23598775598 | True |
| detuning_denominator_positive | 3.25 | 3.25 | True |
| transfer_rate_uses_denominator | 0.206769230769 | 0.206769230769 | True |
| gap_exceeds_perturbation | 2.1 | 2.1 | True |

This certificate backs finite spectral carriers for mode gaps, harmonic ladders, curvature shifts, Kaluza-Klein access frequencies, beat periods, detuning denominators, and transfer-rate normalization.
