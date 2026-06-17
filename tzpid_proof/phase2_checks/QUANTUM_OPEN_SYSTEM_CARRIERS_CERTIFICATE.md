# Quantum/Open-System Carriers Certificate

- Status: `pass`
- Isabelle theory: `isabelle_tzpid/TZPID_QuantumOpenSystem_Carriers.thy`
- Source batch: `Quantum/open-system batch 007`

| Check | Value | Expected | Pass |
|---|---:|---:|---|
| density_trace_one | 1 | 1 | True |
| column_stochastic_trace_preserving | 1 | 1 | True |
| channel_output_trace_matches_sum | 1 | 1 | True |
| measurement_zero_weight_recovers_prior | 0.35 | 0.35 | True |
| measurement_unit_weight_recovers_outcome | 0.9 | 0.9 | True |
| commutator_residual_antisymmetric | 0 | 0 | True |
| noise_denominator_positive | 10 | 10 | True |
| noise_spectrum_uses_denominator | 0.4 | 0.4 | True |
| trace_distance_identical_zero | 0 | 0 | True |
| quantum_thermo_balance_zero | 0 | 0 | True |

This certificate backs finite diagonal-density and open-channel carriers for trace preservation, measurement endpoints, commutator residuals, noise normalization, trace distance, and thermodynamic balance.
