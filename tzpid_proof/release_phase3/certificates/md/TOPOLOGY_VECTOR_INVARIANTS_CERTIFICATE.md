# Topology/Vector Invariants Certificate

- Status: `pass`
- Isabelle theory: `isabelle_tzpid/TZPID_TopologyVector_Invariants.thy`
- Source batch: `Topology/vector batch 005`

| Check | Value | Expected | Pass |
|---|---:|---:|---|
| zero_magnetic_field_has_zero_helicity_density | 0 | 0 | True |
| nonzero_helicity_density_is_dot_product | 0.8 | 0.8 | True |
| flux_is_integer_quantum_multiple | 3 | 3 | True |
| oriented_area_swaps_sign | 0 | 0 | True |
| gauss_bonnet_boundary_balance_closes | 0 | 0 | True |
| winding_index_adds_one_turn | 25.1327412287 | 25.1327412287 | True |
| gap_exceeds_perturbation | 0.5 | 0.5 | True |

This certificate backs the finite HOL carriers for helicity density, flux quantization, oriented circulation area, Gauss-Bonnet boundary closure, winding increments, and gap protection.
