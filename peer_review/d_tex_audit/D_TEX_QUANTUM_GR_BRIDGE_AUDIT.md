# D:\Tex Quantum-to-GR Source Audit

Generated: 2026-06-11T03:42:49

## Scope

- Authored TeX files scanned, excluding TeXLive/venv/vendor folders: 1909
- Quantum-to-GR bridge candidates: 1855

## Priority Counts

- high_quantum_gr_bridge: 212
- low_or_support: 54
- medium_candidate: 1643

## Highest-Scoring Bridge Candidates

| relative_path | title | bridge_score | id_count | equation_like_count | theorem_env_count | already_in_peer_review | promotion_priority |
| --- | --- | --- | --- | --- | --- | --- | --- |
| TEX_20260224_182530\TheorumInfinitum_full_with_ToE.tex | TheorumInfinitum full with ToE | 349 | 0 | 0 | 0 | no | high_quantum_gr_bridge |
| TEX_20260224_182530\theorum_infinitum_full.tex | Theorum Infinitum | 316 | 0 | 0 | 0 | no | high_quantum_gr_bridge |
| TEX_20260224_182530\Volume_02_Complete.tex | Volume 02 Complete | 267 | 0 | 0 | 0 | no | high_quantum_gr_bridge |
| TZPID.tex | TZPID | 256 | 401 | 104 | 0 | no | high_quantum_gr_bridge |
| 1000up.tex | Trawin Zero Point Opera Omnia | 249 | 241 | 1 | 0 | no | high_quantum_gr_bridge |
| TEX_20260224_182530\1000up.tex | Trawin Zero Point Opera Omnia | 249 | 241 | 1 | 0 | no | high_quantum_gr_bridge |
| Pomerium_Internum.tex | Trawin Zero Point Opera Omnia | 248 | 241 | 1 | 0 | no | high_quantum_gr_bridge |
| TEX_20260224_182530\Pomerium_Internum.tex | Trawin Zero Point Opera Omnia | 248 | 241 | 1 | 0 | no | high_quantum_gr_bridge |
| TZPID_before_proof_enrichment.tex | TZPID before proof enrichment | 246 | 401 | 39 | 0 | no | high_quantum_gr_bridge |
| TZPID_before_kdp_restore.tex | TZPID before kdp restore | 242 | 401 | 33 | 0 | no | high_quantum_gr_bridge |
| TEX_20260224_182530\Opera_Omia_Contextus_Canonicus_Trawin_Zero_Point.tex | Opera Omia Contextus Canonicus Trawin Zero Point | 236 | 399 | 46 | 0 | no | high_quantum_gr_bridge |
| TEX_20260224_182530\minimal_output_with_meta.tex | Trawin Zero Point Opera Omnia\ Canonicus — Volume 00 | 231 | 401 | 173 | 0 | no | high_quantum_gr_bridge |
| TEX_20260224_182530\minimal_output.tex | Trawin Zero Point Opera Omnia Contextus Canonicus — Volume 00 | 230 | 401 | 37 | 0 | no | high_quantum_gr_bridge |
| TEX_20260224_182530\emergent_curvature_theory.tex | The Theory of Emergent Curvature: | 229 | 0 | 31 | 12 | no | high_quantum_gr_bridge |
| Opera_Omia_Contextus_Canonicus_Trawin_Zero_Point.tex | Opera Omia Contextus Canonicus Trawin Zero Point | 221 | 401 | 37 | 0 | no | high_quantum_gr_bridge |
| Registriy00.tex | Registriy00 | 218 | 401 | 37 | 0 | no | high_quantum_gr_bridge |
| TEX_20260224_182530\Registriy00.tex | Registriy00 | 218 | 401 | 37 | 0 | no | high_quantum_gr_bridge |
| TEX_20260224_182530\opera_omnia_vol_00.tex | opera omnia vol 00 | 199 | 805 | 177 | 0 | no | high_quantum_gr_bridge |
| opera_omnia_vol_00.tex | opera omnia vol 00 | 198 | 805 | 177 | 0 | no | high_quantum_gr_bridge |
| opera_omnia_vol_0.tex | opera omnia vol 0 | 190 | 805 | 346 | 0 | no | high_quantum_gr_bridge |
| TEX_20260224_182530\equatorial_cosmology.tex | Equatorial Wave Forces, Quantum Interactions, and Non-Flat Cosmological Dynamics: A Unified Frame... | 166 | 0 | 28 | 0 | no | high_quantum_gr_bridge |
| trawin_zero_point_quantum_field_theory.tex | Trawin Zero Point Quantum Field Theory: Propagators, Degenerate Geometry, and TZP-Localized Dynamics | 154 | 0 | 47 | 17 | no | high_quantum_gr_bridge |
| TZP_in _depth.tex | phv | 149 | 0 | 0 | 0 | no | high_quantum_gr_bridge |
| All_tex\Universal_Field_via_Bridge_Tunnel_Theory_SECOND_PASS.tex | BaT | 148 | 0 | 6 | 4 | no | high_quantum_gr_bridge |
| TEX_20260224_182530\Universal_Field_via_Bridge_Tunnel_Theory_SECOND_PASS.tex | BaT | 148 | 0 | 6 | 4 | no | high_quantum_gr_bridge |
| 00_Engine_extractions\BaT.tex | BaT | 139 | 0 | 0 | 0 | no | high_quantum_gr_bridge |
| derivations500.tex | derivations500 | 136 | 106 | 427 | 0 | no | high_quantum_gr_bridge |
| CanonicalRegistryVol01.tex | CanonicalRegistryVol01 | 131 | 233 | 134 | 0 | no | high_quantum_gr_bridge |
| CanonicalRegistryVol01_1.tex | CanonicalRegistryVol01 1 | 131 | 233 | 134 | 0 | no | high_quantum_gr_bridge |
| TEX_20260224_182530\CanonicalRegistryVol01.tex | CanonicalRegistryVol01 | 131 | 233 | 134 | 0 | no | high_quantum_gr_bridge |
| ... | 1825 more rows omitted |  |  |  |  |  |  |

## Simulation-Proof Lane

Python/Wolfram/HDF5 simulations should enter Isabelle as certificate artifacts: the script computes a JSON/CSV/HDF5 result, a small verifier checks thresholds and hashes, and Isabelle imports the finite certificate facts as constants/definitions with explicit assumptions. Isabelle then proves the implication from certified numerical facts to the paper-facing theorem contract.

## Named Source Intake Added 2026-06-11

The following named structures have been promoted into the Isabelle/HOL source-lane carrier `TZPID_QuantumGR_Unification_SourceLane.thy`:

| Source label | Located file(s) | HOL source constructor |
| --- | --- | --- |
| TZP Type C | `D:\TZPIDProof\peer_review\tex\companion03_tzp_type_c.tex` | `TZP_Type_C_Source` |
| Trawin-Enlil Protocol | `D:\TZPIDProof\peer_review\tex\companion24_trawin_enlil_protocol.tex`; `D:\Tex\trawin_enlil_protocol.tex` | `Trawin_Enlil_Protocol_Source` |
| Enlil-Trawin Isomorphism | `D:\Tex\TEX_20260224_182530\The_Enlil_Trawin_Isomorphism.tex` | `Enlil_Trawin_Isomorphism_Source` |
| Topological Unification of quantum mechanics and general relativity | `D:\Tex\topological_unification.tex` | `Topological_Unification_QM_GR_Source` |
| Entrainment through a DAANSsphere axis | `D:\TZPIDProof\peer_review\tex\companion14_entrainment_and_daanssphere_axis.tex`; `D:\Tex\Entrainment and DAANSsphere axis.tex` | `Entrainment_DAANSsphere_Axis_Source` |

The session now records 15 named source carriers in the quantum-to-GR intake lane.  The added checks are `named_recent_sources_are_in_intake_lane` and `named_recent_sources_support_unification_bridge`, and the full Isabelle session builds cleanly after the update.

## Output Files

- Full authored TeX audit: `D:\TZPIDProof\peer_review\d_tex_audit\D_TEX_AUTHORED_TEX_AUDIT.csv`
- Quantum-GR bridge candidates: `D:\TZPIDProof\peer_review\d_tex_audit\D_TEX_QUANTUM_GR_BRIDGE_CANDIDATES.csv`
