# TZPID Proof Ladder Graph Topology Report

Generated UTC: 2026-06-11T10:53:58.290089+00:00

## Executive Summary

- Total ladder nodes: `10357`
- Materialized rung-to-rung dependency edges: `2080`
- Cut/downward references retained for audit: `71`
- Isolated nodes with 0 incoming and 0 outgoing edges: `8387`
- Non-isolated nodes touched by at least one edge: `1970`
- Connected components total: `8618`
- Nontrivial connected clusters: `231`
- Largest connected cluster: `1046` nodes / `1363` edges
- Maximum dependency depth: `67` edges, so `68` sequential layers are sufficient with unlimited parallel workers.
- DAG cyclicity check: `acyclic`

## Method

Edges were rebuilt from the synced derivation ladder by combining preserved `Rests on` rung references, explicit `ID####` mentions in master text fields, and ordered nonempty gold-spine chains. References that point downward or sideways in the current ladder are retained in `cut_edge_transitive_audit.csv` rather than materialized.

## Top Prerequisite Super-Nodes

| Rung | ID | Direct Dependents | Title |
|---:|---|---:|---|
| 16 | ID0017 | 32 | Trawinistic Connection |
| 180 | ID0200 | 23 | Alfv\'en Wave Dispersion Relation |
| 374 | ID0400 | 23 | Cosmological Constant and Master Unification Equation |
| 14 | ID0015 | 22 | Spectral Density Index (TZP-Weighted) |
| 5 | ID0006 | 19 | Trawin Base Unit |
| 22 | ID0023 | 19 | TZP Potential Term |
| 278 | ID0300 | 19 | Node Density Conversion Constant |
| 15 | ID0016 | 18 | Manifold Curvature (TZP Condition) |
| 1 | ID0000 | 15 | Existence and Uniqueness of the Trawin Zero Point |
| 8 | ID0009 | 15 | Hyper-Dimensional Span |
| 18 | ID0019 | 15 | Trawinistic D'Alembertian |
| 19 | ID0020 | 15 | Trawinistic Winding Number |
| 6 | ID0007 | 14 | Temporal Displacement Factor |
| 23 | ID0024 | 14 | TZP Vacuum Energy Density |
| 132 | ID0150 | 13 | Stress–Energy Conservation Constraint |
| 11 | ID0012 | 12 | Field Coherence Metric |
| 28 | ID0029 | 11 | Trawinistic Hamiltonian Density |
| 9 | ID0010 | 10 | Stochastic Drift Magnitude |
| 36 | ID0040 | 10 | Universality of Elsasser Criticality |
| 994 | ID1032 | 10 | Spatial Convolution of Omega |

## Top Dependent Nodes

| Rung | ID | Direct Prerequisites | Title |
|---:|---|---:|---|
| 9544 | ID1898 | 10 | Visual / Glyph Review Tranche |
| 10356 | ID10870 | 8 | Cosmological-constant hierarchy as a radius choice |
| 1816 | ID1876 | 7 | EID Cleanup Next Batch |
| 9543 | ID1888 | 7 | OO-TZP-00 Visual Provenance Packet |
| 1832 | ID1895 | 6 | TZP00 EID Ready Review Batch |
| 1834 | ID1897 | 6 | Registry Visual ID Review Queue |
| 8145 | ID8786 | 6 | Relation: G_T(x, X') |
| 10264 | ID6489 | 6 | \{Einstein–Rosen Bridge and Trawin Zero-Point Tunnel:}\ |
| 10353 | ID10867 | 6 | Hubble constant as enclosure breathing rate |
| 10354 | ID10868 | 6 | Λ–H₀ unification: two readouts of the enclosure radius |
| 10355 | ID10869 | 6 | Dark-energy length of the enclosure |
| 10357 | ID10871 | 6 | Closed breathing-enclosure Friedmann model |
| 1830 | ID1893 | 5 | TZP00 All MyAll Wolfram to TZPID Alignment Queue |
| 1831 | ID1894 | 5 | TZP 00 EID / Bessel Equation-Support Packet |
| 8765 | ID9399 | 5 | Definition of SDAAN |
| 860 | ID0896 | 4 | Temporal Harmonic Operator |
| 1813 | ID1872 | 4 | Canonical Lineage Conflict Audit |
| 4730 | ID5220 | 4 | Relation: η_texttotal [Relocated from [ID 0439]] η_U → T : \| U ⟩ Longmapsto e^iθ_methyl… |
| 4774 | ID5264 | 4 | Relocated Stress-Energy Tensor |
| 4775 | ID5265 | 4 | Relocated Stress-Energy Tensor |
