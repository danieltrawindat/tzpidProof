# Phase 3 Verification Appendix

Generated UTC: 2026-06-09T20:56:50+00:00
Commit: `99303e1b22606b09ba32abc1706004cb3f609929`

## Matrix Summary

- Matrix rows: `29`
- Clean Isabelle rows: `29`
- Rows with certificate lane: `29`
- Rows with missing files: `0`

## Row-Level Status

| Family | Kind | Completion | Isabelle | Certificate | Files |
|---|---|---|---|---|---|
| Hyperspherical Bessel residual bridge | paper_core | `phase2_5_phase3_observable_contract_locked` | `clean_build` | `yes` | TZPID_HypersphericalBesselResidualBridge_Math_Checks.thy; TZPID_HypersphericalBesselResidualBridge_Computational_Checks.thy; TZPID_HypersphericalBesselResidualBridge_Phase2_Model.thy; TZPID_Temporal_Kernel_HOL_Analysis.thy; TZPID_Bessel_External_Certificates.thy; TZPID_Phase3_Observable_Contract.thy |
| Nested hyperspherical enclosure | gold_spine | `s3_spectrum_locked` | `clean_build` | `yes` | TZPID_NestedHypersphere_Focus.thy; TZPID_NestedHypersphere_Computational_Checks.thy; TZPID_NestedHypersphere_Typed_Projection.thy; TZPID_NestedHypersphere_S3_Spectrum.thy |
| Hubble breathing enclosure | spine_bridge | `hubble_breathing_joint_likelihood_locked` | `clean_build` | `python_certificate` | TZPID_HubbleBreathing_Enclosure.thy; TZPID_HubbleBreathing_ClosedDistance.thy; TZPID_HubbleBreathing_FriedmannComponents.thy; TZPID_HubbleBreathing_CPL_Certificate.thy; TZPID_HubbleBreathing_ObservedFit_Certificate.thy; TZPID_HubbleBreathing_PantheonRaw_Certificate.thy; TZPID_HubbleBreathing_PlanckDistancePrior_Certificate.thy; TZPID_HubbleBreathing_DESIDR2BAO_Certificate.thy; TZPID_HubbleBreathing_JointLikelihood_Certificate.thy; TZPID_NestedHypersphere_S3_Spectrum.thy; TZPID_Einstein_Focus.thy |
| Matter creation spine | gold_spine | `matter_creation_pressure_eos_candidate_locked` | `clean_build` | `python_certificate` | TZPID_EnergyMatter_Focus.thy; TZPID_NewSpines_Computational_Checks.thy; TZPID_MatterCreation_ThresholdSpine.thy; TZPID_MatterCreation_TemporalFlow.thy; TZPID_MatterCreation_CriticalityBridge.thy; TZPID_MatterCreation_PressureEoS.thy; TZPID_Theorem_Semantic_Batch017_Quantum_Matter_Followup.thy |
| Gyromagnetic movement | movement_spine | `phase6_loop_index_theorem_locked` | `clean_build` | `yes` | TZPID_GyromagneticMovement_Focus.thy; TZPID_GyromagneticMovement_Computational_Checks.thy; TZPID_Theorem_Semantic_Batch016_Orbital_Gyromagnetic_Followup.thy; TZPID_GyromagneticMovement_Typed_PhaseGradient.thy; TZPID_GyromagneticMovement_VectorCalculus.thy; TZPID_GyromagneticMovement_MHD_Helicity.thy; TZPID_GyromagneticMovement_SpatialBoundary.thy; TZPID_GyromagneticMovement_CirculationDiagnostic.thy; TZPID_GyromagneticMovement_CorrectedWinding.thy; TZPID_GyromagneticMovement_LoopIndex.thy |
| Phase locking resonance | movement_spine | `finite_n_kuramoto_scan_locked` | `clean_build` | `python_certificate` | TZPID_PhaseLockingResonance_Focus.thy; TZPID_PhaseLockingResonance_Computational_Checks.thy; TZPID_Theorem_Semantic_Batch018_Resonance_Locking_Followup.thy; TZPID_PhaseLockingResonance_Typed_RatioSelection.thy; TZPID_PhaseLockingResonance_CaptureBasin.thy; TZPID_PhaseLockingResonance_KuramotoFiniteN.thy |
| Fifth flip crystal scale-invariance | spine_bridge | `fifth_flip_phi_ripple_bridge_locked` | `clean_build` | `python_certificate` | TZPID_FifthFlip_CrystalScaleInvariance.thy; TZPID_PhaseLockingResonance_Typed_RatioSelection.thy; TZPID_NestedHypersphere_S3_Spectrum.thy; TZPID_Ripple_LogPeriodic_PhiBridge.thy |
| Magnetic/torsion | domain_model | `vector_mhd_helicity_torsion_locked` | `clean_build` | `python_certificate` | TZPID_Magnetic_Torsion_Model.thy; TZPID_Theorem_Semantic_Batch011_Magnetic_Torsion.thy; TZPID_MagneticTorsion_VectorMHD.thy |
| Emergence/bifurcation | domain_model | `bifurcation_normal_forms_locked` | `clean_build` | `python_certificate` | TZPID_Theorem_Semantic_Batch015_Emergence_Bifurcation_Followup.thy; TZPID_EmergenceBifurcation_NormalForms.thy |
| Quantum/matter | domain_model | `probability_density_bell_conservation_locked` | `clean_build` | `python_certificate` | TZPID_Quantum_Open_System_Model.thy; TZPID_Theorem_Semantic_Batch017_Quantum_Matter_Followup.thy; TZPID_QuantumMatter_ProbabilityCarriers.thy |
| Master theorem batch 001 | batch | `master_batch001_carriers_locked` | `clean_build` | `python_certificate` | TZPID_Theorem_Semantic_Batch001.thy; TZPID_MasterBatch001_Carriers.thy |
| Master theorem batch 002 | batch | `master_batch002_carriers_locked` | `clean_build` | `python_certificate` | TZPID_Theorem_Semantic_Batch002.thy; TZPID_MasterBatch002_Carriers.thy |
| Master theorem batch 003 | batch | `master_batch003_carriers_locked` | `clean_build` | `python_certificate` | TZPID_Theorem_Semantic_Batch003.thy; TZPID_MasterBatch003_Carriers.thy |
| Master theorem batch 004 | batch | `master_batch004_carriers_locked` | `clean_build` | `python_certificate` | TZPID_Theorem_Semantic_Batch004.thy; TZPID_MasterBatch004_Carriers.thy |
| Topology/vector batch 005 | batch | `topology_vector_invariants_locked` | `clean_build` | `python_certificate` | TZPID_Topology_Vector_Model.thy; TZPID_Theorem_Semantic_Batch005_Topology_Vector.thy; TZPID_TopologyVector_Invariants.thy |
| Operator/spectral batch 006 | batch | `operator_spectral_carriers_locked` | `clean_build` | `python_certificate` | TZPID_Operator_Spectral_Model.thy; TZPID_Theorem_Semantic_Batch006_Operator_Spectral.thy; TZPID_OperatorSpectral_Carriers.thy |
| Quantum/open-system batch 007 | batch | `quantum_open_system_carriers_locked` | `clean_build` | `python_certificate` | TZPID_Quantum_Open_System_Model.thy; TZPID_Theorem_Semantic_Batch007_Quantum_Open_Systems.thy; TZPID_QuantumOpenSystem_Carriers.thy |
| Geometry/manifold batch 008 | batch | `geometry_manifold_carriers_locked` | `clean_build` | `python_certificate` | TZPID_Geometry_Manifold_Model.thy; TZPID_Theorem_Semantic_Batch008_Geometry_Manifold.thy; TZPID_GeometryManifold_Carriers.thy |
| Dynamics/scaling batch 009 | batch | `dynamics_scaling_carriers_locked` | `clean_build` | `python_certificate` | TZPID_Dynamics_Scaling_Model.thy; TZPID_Theorem_Semantic_Batch009_Dynamics_Scaling.thy; TZPID_DynamicsScaling_Carriers.thy |
| Meta-foundation batch 010 | batch | `meta_foundation_carriers_locked` | `clean_build` | `python_certificate` | TZPID_Meta_Foundation_Model.thy; TZPID_Theorem_Semantic_Batch010_Meta_Foundation.thy; TZPID_MetaFoundation_Carriers.thy |
| Magnetic/torsion batch 011 | batch | `vector_mhd_helicity_torsion_locked` | `clean_build` | `python_certificate` | TZPID_Magnetic_Torsion_Model.thy; TZPID_Theorem_Semantic_Batch011_Magnetic_Torsion.thy; TZPID_MagneticTorsion_VectorMHD.thy |
| Operator/spectral follow-up batch 012 | batch | `operator_spectral_followup_locked` | `clean_build` | `python_certificate` | TZPID_Theorem_Semantic_Batch012_Operator_Spectral_Followup.thy; TZPID_OperatorSpectral_FollowupCarriers.thy |
| Topology/category follow-up batch 013 | batch | `topology_category_carriers_locked` | `clean_build` | `python_certificate` | TZPID_Theorem_Semantic_Batch013_Topology_Category_Followup.thy; TZPID_TopologyCategory_Carriers.thy |
| Dynamics/stability follow-up batch 014 | batch | `dynamics_stability_carriers_locked` | `clean_build` | `python_certificate` | TZPID_Theorem_Semantic_Batch014_Dynamics_Stability_Followup.thy; TZPID_DynamicsStability_Carriers.thy |
| Emergence/bifurcation follow-up batch 015 | batch | `bifurcation_normal_forms_locked` | `clean_build` | `python_certificate` | TZPID_Theorem_Semantic_Batch015_Emergence_Bifurcation_Followup.thy; TZPID_EmergenceBifurcation_NormalForms.thy |
| Orbital/gyromagnetic follow-up batch 016 | batch | `gyromagnetic_vector_loop_semantics_locked` | `clean_build` | `python_certificate` | TZPID_Theorem_Semantic_Batch016_Orbital_Gyromagnetic_Followup.thy; TZPID_GyromagneticMovement_Typed_PhaseGradient.thy; TZPID_GyromagneticMovement_VectorCalculus.thy; TZPID_GyromagneticMovement_MHD_Helicity.thy; TZPID_GyromagneticMovement_LoopIndex.thy |
| Quantum/matter follow-up batch 017 | batch | `probability_density_bell_conservation_locked` | `clean_build` | `python_certificate` | TZPID_Theorem_Semantic_Batch017_Quantum_Matter_Followup.thy; TZPID_QuantumMatter_ProbabilityCarriers.thy |
| Resonance-locking follow-up batch 018 | batch | `ratio_capture_basin_finite_n_kuramoto_locked` | `clean_build` | `python_certificate` | TZPID_Theorem_Semantic_Batch018_Resonance_Locking_Followup.thy; TZPID_PhaseLockingResonance_Typed_RatioSelection.thy; TZPID_PhaseLockingResonance_CaptureBasin.thy; TZPID_PhaseLockingResonance_KuramotoFiniteN.thy |
| Geometry/curvature closeout batch 019 | batch | `geometry_curvature_carriers_locked` | `clean_build` | `python_certificate` | TZPID_Theorem_Semantic_Batch019_Geometry_Curvature_Closeout.thy; TZPID_GeometryCurvature_Carriers.thy |
