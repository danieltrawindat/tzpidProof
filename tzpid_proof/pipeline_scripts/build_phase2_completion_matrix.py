from __future__ import annotations

import csv
import json
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent
ISABELLE = ROOT / "isabelle_tzpid"
QUEUE = ROOT / "TZPID_THEOREM_SEMANTIC_QUEUE.csv"
OUT_CSV = ROOT / "TZPID_PHASE2_COMPLETION_MATRIX.csv"
OUT_MD = ROOT / "TZPID_PHASE2_COMPLETION_MATRIX.md"
OUT_JSON = ROOT / "TZPID_PHASE2_COMPLETION_MATRIX.json"


def count_statuses() -> Counter[str]:
    with QUEUE.open(newline="", encoding="utf-8-sig") as f:
        return Counter(row["translation_status"] for row in csv.DictReader(f))


def file_metrics(files: list[str]) -> dict[str, int | str]:
    text_parts: list[str] = []
    missing: list[str] = []
    for file_name in files:
        path = ISABELLE / file_name
        if path.exists():
            text_parts.append(path.read_text(encoding="utf-8"))
        else:
            missing.append(file_name)
    text = "\n".join(text_parts)
    forbidden_hits = re.findall(r"by simp|by \(simp|simp add|\boops\b|\bsorry\b|\badmit\b", text)
    return {
        "definition_count": len(re.findall(r"(?m)^definition\s+", text)),
        "theorem_or_lemma_count": len(re.findall(r"(?m)^(theorem|lemma)\s+", text)),
        "assumes_count": len(re.findall(r"\bassumes\b", text)),
        "type_or_const_count": len(re.findall(r"(?m)^(typedecl|type_synonym|consts)\b", text)),
        "forbidden_shortcut_hits": len(forbidden_hits),
        "missing_files": "; ".join(missing),
    }


def row(
    *,
    family: str,
    kind: str,
    files: list[str],
    queue_status: str,
    level: str,
    typed_carrier: str,
    assumptions: str,
    isabelle: str,
    wolfram: str,
    priority: str,
    completion: str,
    next_upgrade: str,
    status_counts: Counter[str],
) -> dict[str, str | int]:
    metrics = file_metrics(files)
    covered_rows = status_counts.get(queue_status, "n/a") if queue_status else "n/a"
    result: dict[str, str | int] = {
        "family": family,
        "kind": kind,
        "queue_status": queue_status,
        "covered_queue_rows": covered_rows,
        "isabelle_files": "; ".join(files),
        "current_level": level,
        "typed_carrier_exists": typed_carrier,
        "explicit_assumptions": assumptions,
        "isabelle_checked": isabelle,
        "wolfram_certificate": wolfram,
        "paper_priority": priority,
        "completion_state": completion,
        "next_upgrade": next_upgrade,
    }
    result.update(metrics)
    return result


def build_rows() -> list[dict[str, str | int]]:
    counts = count_statuses()
    rows: list[dict[str, str | int]] = []

    core_rows = [
        dict(
            family="Hyperspherical Bessel residual bridge",
            kind="paper_core",
            files=[
                "TZPID_HypersphericalBesselResidualBridge_Math_Checks.thy",
                "TZPID_HypersphericalBesselResidualBridge_Computational_Checks.thy",
                "TZPID_HypersphericalBesselResidualBridge_Phase2_Model.thy",
                "TZPID_Temporal_Kernel_HOL_Analysis.thy",
                "TZPID_Bessel_External_Certificates.thy",
                "TZPID_Phase3_Observable_Contract.thy",
            ],
            queue_status="phase2_already_started",
            level="hol_analysis_integral_bessel_policy_delta_alpha_phase3_contract",
            typed_carrier="yes",
            assumptions="yes",
            isabelle="clean_build",
            wolfram="yes",
            priority="critical",
            completion="phase2_5_phase3_observable_contract_locked",
            next_upgrade="Next lift the nested hyperspherical enclosure spine from abstract S3/projection predicates into typed projection-map semantics.",
        ),
        dict(
            family="Nested hyperspherical enclosure",
            kind="gold_spine",
            files=[
                "TZPID_NestedHypersphere_Focus.thy",
                "TZPID_NestedHypersphere_Computational_Checks.thy",
                "TZPID_NestedHypersphere_Typed_Projection.thy",
                "TZPID_NestedHypersphere_S3_Spectrum.thy",
            ],
            queue_status="",
            level="focus_certificate_plus_typed_projection_map_plus_s3_spectrum",
            typed_carrier="yes",
            assumptions="locale_level",
            isabelle="clean_build",
            wolfram="yes",
            priority="critical",
            completion="s3_spectrum_locked",
            next_upgrade="Next enrich the projection carrier from finite-coordinate algebra into topology/continuity and explicit Hopf fibration semantics.",
        ),
        dict(
            family="Hubble breathing enclosure",
            kind="spine_bridge",
            files=[
                "TZPID_HubbleBreathing_Enclosure.thy",
                "TZPID_HubbleBreathing_ClosedDistance.thy",
                "TZPID_HubbleBreathing_FriedmannComponents.thy",
                "TZPID_HubbleBreathing_CPL_Certificate.thy",
                "TZPID_HubbleBreathing_ObservedFit_Certificate.thy",
                "TZPID_HubbleBreathing_PantheonRaw_Certificate.thy",
                "TZPID_HubbleBreathing_PlanckDistancePrior_Certificate.thy",
                "TZPID_HubbleBreathing_DESIDR2BAO_Certificate.thy",
                "TZPID_HubbleBreathing_JointLikelihood_Certificate.thy",
                "TZPID_NestedHypersphere_S3_Spectrum.thy",
                "TZPID_Einstein_Focus.thy",
            ],
            queue_status="",
            level="hubble_breathing_closed_distance_plus_friedmann_joint_likelihood",
            typed_carrier="yes",
            assumptions="yes",
            isabelle="clean_build",
            wolfram="python_certificate",
            priority="critical",
            completion="hubble_breathing_joint_likelihood_locked",
            next_upgrade="Next promote the scenario-sum certificate into a small parameter-search lane over H0, Omega_m, Omega_K, w0, and wa.",
        ),
        dict(
            family="Matter creation spine",
            kind="gold_spine",
            files=[
                "TZPID_EnergyMatter_Focus.thy",
                "TZPID_NewSpines_Computational_Checks.thy",
                "TZPID_MatterCreation_ThresholdSpine.thy",
                "TZPID_MatterCreation_TemporalFlow.thy",
                "TZPID_MatterCreation_CriticalityBridge.thy",
                "TZPID_MatterCreation_PressureEoS.thy",
                "TZPID_Theorem_Semantic_Batch017_Quantum_Matter_Followup.thy",
            ],
            queue_status="",
            level="energy_matter_focus_plus_threshold_density_mass_energy_curvature_carrier_plus_temporal_emergence_flow_plus_criticality_split_plus_pressure_eos_candidate",
            typed_carrier="yes",
            assumptions="yes",
            isabelle="clean_build",
            wolfram="python_certificate",
            priority="critical",
            completion="matter_creation_pressure_eos_candidate_locked",
            next_upgrade="Next connect the pressure EoS candidate to the temporal threshold gate Gamma(rho_vac) Theta(p-p_c) from ID10114.",
        ),
        dict(
            family="Gyromagnetic movement",
            kind="movement_spine",
            files=[
                "TZPID_GyromagneticMovement_Focus.thy",
                "TZPID_GyromagneticMovement_Computational_Checks.thy",
                "TZPID_Theorem_Semantic_Batch016_Orbital_Gyromagnetic_Followup.thy",
                "TZPID_GyromagneticMovement_Typed_PhaseGradient.thy",
                "TZPID_GyromagneticMovement_VectorCalculus.thy",
                "TZPID_GyromagneticMovement_MHD_Helicity.thy",
                "TZPID_GyromagneticMovement_SpatialBoundary.thy",
                "TZPID_GyromagneticMovement_CirculationDiagnostic.thy",
                "TZPID_GyromagneticMovement_CorrectedWinding.thy",
                "TZPID_GyromagneticMovement_LoopIndex.thy",
            ],
            queue_status="batch016_started",
            level="focus_certificate_plus_phase4_phase5_phase5_5_spatial_boundary_plus_phase6_corrected_winding_plus_loop_index_theorem",
            typed_carrier="yes",
            assumptions="yes",
            isabelle="clean_build",
            wolfram="yes",
            priority="critical",
            completion="phase6_loop_index_theorem_locked",
            next_upgrade="Next connect the loop-index theorem to vortex-core enclosure and MHD helicity conservation semantics.",
        ),
        dict(
            family="Phase locking resonance",
            kind="movement_spine",
            files=[
                "TZPID_PhaseLockingResonance_Focus.thy",
                "TZPID_PhaseLockingResonance_Computational_Checks.thy",
                "TZPID_Theorem_Semantic_Batch018_Resonance_Locking_Followup.thy",
                "TZPID_PhaseLockingResonance_Typed_RatioSelection.thy",
                "TZPID_PhaseLockingResonance_CaptureBasin.thy",
                "TZPID_PhaseLockingResonance_KuramotoFiniteN.thy",
            ],
            queue_status="batch018_started",
            level="focus_certificate_plus_typed_ratio_selection_plus_capture_basin_plus_finite_n_kuramoto_semantics",
            typed_carrier="yes",
            assumptions="yes",
            isabelle="clean_build",
            wolfram="python_certificate",
            priority="high",
            completion="finite_n_kuramoto_scan_locked",
            next_upgrade="Next extend the finite-N algebraic scan into a time-domain Kuramoto integration certificate and orbital capture examples.",
        ),
        dict(
            family="Fifth flip crystal scale-invariance",
            kind="spine_bridge",
            files=[
                "TZPID_FifthFlip_CrystalScaleInvariance.thy",
                "TZPID_PhaseLockingResonance_Typed_RatioSelection.thy",
                "TZPID_NestedHypersphere_S3_Spectrum.thy",
                "TZPID_Ripple_LogPeriodic_PhiBridge.thy",
            ],
            queue_status="",
            level="golden_reciprocal_fixed_point_plus_crystal_trace_hinge_plus_phi_log_periodic_ripple_bridge",
            typed_carrier="yes",
            assumptions="yes",
            isabelle="clean_build",
            wolfram="python_certificate",
            priority="high",
            completion="fifth_flip_phi_ripple_bridge_locked",
            next_upgrade="Next attach empirical ripple-index evidence rows to the bridge and separate measured spatial ratios from acoustic 32/27 ratios.",
        ),
        dict(
            family="Magnetic/torsion",
            kind="domain_model",
            files=[
                "TZPID_Magnetic_Torsion_Model.thy",
                "TZPID_Theorem_Semantic_Batch011_Magnetic_Torsion.thy",
                "TZPID_MagneticTorsion_VectorMHD.thy",
            ],
            queue_status="batch011_started",
            level="typed_residual_guard_plus_vector_mhd_helicity_torsion",
            typed_carrier="yes",
            assumptions="yes",
            isabelle="clean_build",
            wolfram="python_certificate",
            priority="high",
            completion="vector_mhd_helicity_torsion_locked",
            next_upgrade="Next connect vector-MHD torsion/helicity semantics to vortex-core enclosure and gyromagnetic loop-index certificates.",
        ),
        dict(
            family="Emergence/bifurcation",
            kind="domain_model",
            files=[
                "TZPID_Theorem_Semantic_Batch015_Emergence_Bifurcation_Followup.thy",
                "TZPID_EmergenceBifurcation_NormalForms.thy",
            ],
            queue_status="batch015_started",
            level="typed_residual_guard_plus_bifurcation_normal_forms",
            typed_carrier="yes",
            assumptions="yes",
            isabelle="clean_build",
            wolfram="python_certificate",
            priority="high",
            completion="bifurcation_normal_forms_locked",
            next_upgrade="Next connect the normal-form carriers to concrete source IDs and physical control-parameter candidates.",
        ),
        dict(
            family="Quantum/matter",
            kind="domain_model",
            files=[
                "TZPID_Quantum_Open_System_Model.thy",
                "TZPID_Theorem_Semantic_Batch017_Quantum_Matter_Followup.thy",
                "TZPID_QuantumMatter_ProbabilityCarriers.thy",
            ],
            queue_status="batch017_started",
            level="typed_residual_guard_plus_probability_density_bell_conservation",
            typed_carrier="yes",
            assumptions="yes",
            isabelle="clean_build",
            wolfram="python_certificate",
            priority="high",
            completion="probability_density_bell_conservation_locked",
            next_upgrade="Next lift diagonal probability carriers toward complex density matrices and CPTP channel composition.",
        ),
    ]

    for spec in core_rows:
        rows.append(row(**spec, status_counts=counts))

    batch_specs = [
        ("Master theorem batch 001", "batch", ["TZPID_Theorem_Semantic_Batch001.thy", "TZPID_MasterBatch001_Carriers.thy"], "batch001_started", "typed_residual_guard_plus_master_carriers", "high"),
        ("Master theorem batch 002", "batch", ["TZPID_Theorem_Semantic_Batch002.thy", "TZPID_MasterBatch002_Carriers.thy"], "batch002_started", "typed_residual_guard_plus_master_helicity_kk_carriers", "high"),
        ("Master theorem batch 003", "batch", ["TZPID_Theorem_Semantic_Batch003.thy", "TZPID_MasterBatch003_Carriers.thy"], "batch003_started", "typed_residual_guard_plus_balance_projection_carriers", "medium"),
        ("Master theorem batch 004", "batch", ["TZPID_Theorem_Semantic_Batch004.thy", "TZPID_MasterBatch004_Carriers.thy"], "batch004_started", "typed_residual_guard_plus_base_boundary_decay_carriers", "medium"),
        ("Topology/vector batch 005", "batch", ["TZPID_Topology_Vector_Model.thy", "TZPID_Theorem_Semantic_Batch005_Topology_Vector.thy", "TZPID_TopologyVector_Invariants.thy"], "batch005_started", "typed_scaffold_plus_topological_invariant_carriers", "high"),
        ("Operator/spectral batch 006", "batch", ["TZPID_Operator_Spectral_Model.thy", "TZPID_Theorem_Semantic_Batch006_Operator_Spectral.thy", "TZPID_OperatorSpectral_Carriers.thy"], "batch006_started", "typed_scaffold_plus_finite_spectral_carriers", "high"),
        ("Quantum/open-system batch 007", "batch", ["TZPID_Quantum_Open_System_Model.thy", "TZPID_Theorem_Semantic_Batch007_Quantum_Open_Systems.thy", "TZPID_QuantumOpenSystem_Carriers.thy"], "batch007_started", "typed_scaffold_plus_open_system_density_channel_carriers", "high"),
        ("Geometry/manifold batch 008", "batch", ["TZPID_Geometry_Manifold_Model.thy", "TZPID_Theorem_Semantic_Batch008_Geometry_Manifold.thy", "TZPID_GeometryManifold_Carriers.thy"], "batch008_started", "typed_scaffold_plus_metric_projection_curvature_carriers", "high"),
        ("Dynamics/scaling batch 009", "batch", ["TZPID_Dynamics_Scaling_Model.thy", "TZPID_Theorem_Semantic_Batch009_Dynamics_Scaling.thy", "TZPID_DynamicsScaling_Carriers.thy"], "batch009_started", "typed_scaffold_plus_dynamics_scaling_carriers", "medium"),
        ("Meta-foundation batch 010", "batch", ["TZPID_Meta_Foundation_Model.thy", "TZPID_Theorem_Semantic_Batch010_Meta_Foundation.thy", "TZPID_MetaFoundation_Carriers.thy"], "batch010_started", "typed_scaffold_plus_meta_foundation_carriers", "medium"),
        ("Magnetic/torsion batch 011", "batch", ["TZPID_Magnetic_Torsion_Model.thy", "TZPID_Theorem_Semantic_Batch011_Magnetic_Torsion.thy", "TZPID_MagneticTorsion_VectorMHD.thy"], "batch011_started", "typed_scaffold_plus_vector_mhd_helicity_torsion", "high"),
        ("Operator/spectral follow-up batch 012", "batch", ["TZPID_Theorem_Semantic_Batch012_Operator_Spectral_Followup.thy", "TZPID_OperatorSpectral_FollowupCarriers.thy"], "batch012_started", "typed_residual_guard_plus_followup_spectral_carriers", "high"),
        ("Topology/category follow-up batch 013", "batch", ["TZPID_Theorem_Semantic_Batch013_Topology_Category_Followup.thy", "TZPID_TopologyCategory_Carriers.thy"], "batch013_started", "typed_residual_guard_plus_finite_category_carriers", "medium"),
        ("Dynamics/stability follow-up batch 014", "batch", ["TZPID_Theorem_Semantic_Batch014_Dynamics_Stability_Followup.thy", "TZPID_DynamicsStability_Carriers.thy"], "batch014_started", "typed_residual_guard_plus_stability_margin_carriers", "medium"),
        ("Emergence/bifurcation follow-up batch 015", "batch", ["TZPID_Theorem_Semantic_Batch015_Emergence_Bifurcation_Followup.thy", "TZPID_EmergenceBifurcation_NormalForms.thy"], "batch015_started", "typed_residual_guard_plus_bifurcation_normal_forms", "high"),
        ("Orbital/gyromagnetic follow-up batch 016", "batch", ["TZPID_Theorem_Semantic_Batch016_Orbital_Gyromagnetic_Followup.thy", "TZPID_GyromagneticMovement_Typed_PhaseGradient.thy", "TZPID_GyromagneticMovement_VectorCalculus.thy", "TZPID_GyromagneticMovement_MHD_Helicity.thy", "TZPID_GyromagneticMovement_LoopIndex.thy"], "batch016_started", "typed_residual_guard_plus_gyromagnetic_vector_loop_semantics", "high"),
        ("Quantum/matter follow-up batch 017", "batch", ["TZPID_Theorem_Semantic_Batch017_Quantum_Matter_Followup.thy", "TZPID_QuantumMatter_ProbabilityCarriers.thy"], "batch017_started", "typed_residual_guard_plus_probability_density_bell_conservation", "high"),
        ("Resonance-locking follow-up batch 018", "batch", ["TZPID_Theorem_Semantic_Batch018_Resonance_Locking_Followup.thy", "TZPID_PhaseLockingResonance_Typed_RatioSelection.thy", "TZPID_PhaseLockingResonance_CaptureBasin.thy", "TZPID_PhaseLockingResonance_KuramotoFiniteN.thy"], "batch018_started", "typed_residual_guard_plus_ratio_capture_basin_finite_n_kuramoto_semantics", "high"),
        ("Geometry/curvature closeout batch 019", "batch", ["TZPID_Theorem_Semantic_Batch019_Geometry_Curvature_Closeout.thy", "TZPID_GeometryCurvature_Carriers.thy"], "batch019_started", "typed_residual_guard_plus_curvature_coupling_carriers", "medium"),
    ]
    batch_overrides = {
        "Master theorem batch 001": dict(
            wolfram="python_certificate",
            completion="master_batch001_carriers_locked",
            next_upgrade="Connect broad batch 001 carriers to specific spine documents and replace image placeholders as source artifacts mature.",
        ),
        "Master theorem batch 002": dict(
            wolfram="python_certificate",
            completion="master_batch002_carriers_locked",
            next_upgrade="Connect batch 002 helicity/KK/pressure carriers to magnetic-torsion, operator-spectral, and avalanche spine documents.",
        ),
        "Master theorem batch 003": dict(
            wolfram="python_certificate",
            completion="master_batch003_carriers_locked",
            next_upgrade="Connect batch 003 balance/projection carriers to Hopf, MHD, radius-ratio, and S3-boundary spine documents.",
        ),
        "Master theorem batch 004": dict(
            wolfram="python_certificate",
            completion="master_batch004_carriers_locked",
            next_upgrade="Connect batch 004 base-unit, boundary, information, decay, and dispersion carriers to publication-facing verification appendices.",
        ),
        "Topology/vector batch 005": dict(
            wolfram="python_certificate",
            completion="topology_vector_invariants_locked",
            next_upgrade="Connect topological invariant carriers to Hopf/continuity projection semantics and geometry/manifold batch 008.",
        ),
        "Operator/spectral batch 006": dict(
            wolfram="python_certificate",
            completion="operator_spectral_carriers_locked",
            next_upgrade="Connect finite spectral carriers to Bessel root certificates, S3 eigenvalue ladders, and operator/spectral follow-up batch 012.",
        ),
        "Quantum/open-system batch 007": dict(
            wolfram="python_certificate",
            completion="quantum_open_system_carriers_locked",
            next_upgrade="Connect diagonal open-system carriers to full density-matrix/CPTP semantics and quantum/matter probability carriers.",
        ),
        "Geometry/manifold batch 008": dict(
            wolfram="python_certificate",
            completion="geometry_manifold_carriers_locked",
            next_upgrade="Connect finite geometry carriers to Hopf projection continuity, S3 spectrum geometry, and curvature closeout batch 019.",
        ),
        "Dynamics/scaling batch 009": dict(
            wolfram="python_certificate",
            completion="dynamics_scaling_carriers_locked",
            next_upgrade="Connect dynamics/scaling carriers to time-domain simulations and paper-facing scaling-law appendices.",
        ),
        "Meta-foundation batch 010": dict(
            wolfram="python_certificate",
            completion="meta_foundation_carriers_locked",
            next_upgrade="Connect meta-foundation carriers to README provenance, falsifiability statements, and publication verification tables.",
        ),
        "Magnetic/torsion batch 011": dict(
            wolfram="python_certificate",
            completion="vector_mhd_helicity_torsion_locked",
            next_upgrade="Connect vector-MHD torsion/helicity semantics to vortex-core enclosure and gyromagnetic loop-index certificates.",
        ),
        "Operator/spectral follow-up batch 012": dict(
            wolfram="python_certificate",
            completion="operator_spectral_followup_locked",
            next_upgrade="Connect batch 012 follow-up carriers directly to Bessel root certificates and S3 eigenvalue geometry.",
        ),
        "Topology/category follow-up batch 013": dict(
            wolfram="python_certificate",
            completion="topology_category_carriers_locked",
            next_upgrade="Connect finite category carriers to Hopf projection continuity and source-level category documents.",
        ),
        "Dynamics/stability follow-up batch 014": dict(
            wolfram="python_certificate",
            completion="dynamics_stability_carriers_locked",
            next_upgrade="Connect stability margin carriers to time-domain numerical stability scans and paper-facing solver appendices.",
        ),
        "Emergence/bifurcation follow-up batch 015": dict(
            wolfram="python_certificate",
            completion="bifurcation_normal_forms_locked",
            next_upgrade="Connect normal-form carriers to concrete source IDs and physical control-parameter candidates.",
        ),
        "Orbital/gyromagnetic follow-up batch 016": dict(
            wolfram="python_certificate",
            completion="gyromagnetic_vector_loop_semantics_locked",
            next_upgrade="Connect loop-index semantics to vortex-core enclosure and MHD helicity conservation.",
        ),
        "Quantum/matter follow-up batch 017": dict(
            wolfram="python_certificate",
            completion="probability_density_bell_conservation_locked",
            next_upgrade="Lift diagonal probability carriers toward complex density matrices and CPTP channel composition.",
        ),
        "Resonance-locking follow-up batch 018": dict(
            wolfram="python_certificate",
            completion="ratio_capture_basin_finite_n_kuramoto_locked",
            next_upgrade="Extend the finite-N algebraic scan into a time-domain Kuramoto integration certificate and orbital capture examples.",
        ),
        "Geometry/curvature closeout batch 019": dict(
            wolfram="python_certificate",
            completion="geometry_curvature_carriers_locked",
            next_upgrade="Connect curvature coupling carriers to manifold/metric spine appendices and source-level curvature obligations.",
        ),
    }
    for family, kind, files, status, level, priority in batch_specs:
        override = batch_overrides.get(
            family,
            dict(
                wolfram="not_attached",
                completion="started_not_complete",
                next_upgrade="Promote from residual/guard semantics into domain-specific HOL-Analysis structures where this batch is paper-facing.",
            ),
        )
        rows.append(
            row(
                family=family,
                kind=kind,
                files=files,
                queue_status=status,
                level=level,
                typed_carrier="yes",
                assumptions="yes",
                isabelle="clean_build",
                wolfram=override["wolfram"],
                priority=priority,
                completion=override["completion"],
                next_upgrade=override["next_upgrade"],
                status_counts=counts,
            )
        )
    return rows


def write_csv(rows: list[dict[str, str | int]]) -> None:
    fieldnames = list(rows[0].keys())
    with OUT_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_json(rows: list[dict[str, str | int]]) -> None:
    OUT_JSON.write_text(json.dumps(rows, indent=2), encoding="utf-8")


def write_md(rows: list[dict[str, str | int]]) -> None:
    counts = count_statuses()
    triage_remaining = sum(
        count for status, count in counts.items()
        if status.startswith("triaged_")
        or status in {"queued_for_triage", "needs_semantic_translation"}
    )
    total_queue_rows = sum(counts.values())
    clean_shortcut_rows = sum(1 for row in rows if int(row["forbidden_shortcut_hits"]) == 0)
    lines = [
        "# TZPID Phase 2 Completion Matrix",
        "",
        "Generated: 2026-06-08",
        "",
        "## Summary",
        "",
        f"- Queue rows represented: `{total_queue_rows}`",
        f"- Remaining triage rows: `{triage_remaining}`",
        f"- Matrix rows: `{len(rows)}`",
        f"- Rows with no shortcut/placeholders in listed files: `{clean_shortcut_rows}` of `{len(rows)}`",
        f"- CSV: `{OUT_CSV.name}`",
        f"- JSON: `{OUT_JSON.name}`",
        "",
        "## Queue Status Counts",
        "",
        "| Status | Count |",
        "|---|---:|",
    ]
    for status, count in counts.most_common():
        lines.append(f"| {status} | {count} |")

    lines.extend([
        "",
        "## Completion Matrix",
        "",
        "| Family | Kind | Rows | Level | Isabelle | Wolfram | Priority | Completion | Next Upgrade |",
        "|---|---|---:|---|---|---|---|---|---|",
    ])
    for row in rows:
        next_upgrade = str(row["next_upgrade"]).replace("|", "\\|")
        lines.append(
            f"| {row['family']} | {row['kind']} | {row['covered_queue_rows']} | "
            f"{row['current_level']} | {row['isabelle_checked']} | {row['wolfram_certificate']} | "
            f"{row['paper_priority']} | {row['completion_state']} | {next_upgrade} |"
        )

    lines.extend([
        "",
        "## Recommended Phase 2 Upgrade Order",
        "",
        "| Rank | Family | Reason | First Upgrade |",
        "|---:|---|---|---|",
    ])
    upgrade_order = [
        (
            "Hyperspherical Bessel residual bridge",
            "Paper core with concrete algebra and certificates already present.",
            "The kernel integral is proved in HOL-Analysis; Bessel roots are an explicit external Wolfram interval-certificate policy; the drop fraction induces a HOL-proved Delta-alpha phase-gradient and shell-radius prediction; exported Delta-alpha arrays reproduce the predicted shell radii; and the Phase3 HDF5 psi field is locked by an Isabelle observable contract.",
        ),
        (
            "Gyromagnetic movement",
            "Central movement-mechanism spine with Wolfram-backed checks plus Phase 4, Phase 5, Phase 5.5, Phase 5.6, corrected Phase 6 winding, and a reusable loop-index theorem.",
            "Connect the loop-index theorem to vortex-core enclosure and MHD helicity conservation semantics.",
        ),
        (
            "Hubble breathing enclosure",
            "Supplies the clock, observable distance fingerprint, typed Friedmann carrier, CPL certificate, observed-summary residual lane, Pantheon+ raw covariance likelihood, Planck compressed distance-prior likelihood, DESI DR2 BAO covariance likelihood, and a joint chi-square certificate.",
            "Promote the scenario-sum certificate into a small parameter-search lane over H0, Omega_m, Omega_K, w0, and wa.",
        ),
        (
            "Matter creation spine",
            "Locks the Energy-to-Matter Logic spine as a real-valued pressure-threshold, density-gain, mass-energy, curvature-source, temporal-transfer, ID10117 criticality-split, and quadratic pressure-EoS candidate carrier with Python certificates for temporal flow and pressure stationarity.",
            "Connect the pressure EoS candidate to the temporal threshold gate Gamma(rho_vac) Theta(p-p_c) from ID10114.",
        ),
        (
            "Phase locking resonance",
            "Connects the rational-ratio selection mechanism to orbital and acoustic dynamics; now includes coupled-oscillator capture-basin semantics with a Python grid certificate.",
            "Connect capture-basin semantics to nonlinear Kuramoto order-parameter stability and finite-N entrainment scans.",
        ),
        (
            "Fifth flip crystal scale-invariance",
            "Connects rational locking, crystal trace admissibility, the golden reciprocal fixed point, and the transition into scale-invariant quasicrystal behavior; now has Python certificates for 2*cos(72 degrees) = 1/phi and phi-scaled log-periodic ripple projection.",
            "Attach empirical ripple-index evidence rows to the bridge and separate measured spatial ratios from acoustic 32/27 ratios.",
        ),
        (
            "Emergence/bifurcation",
            "Core TZP emergence story; now upgraded from residual guards to pitchfork/saddle-node normal-form carriers with a Python certificate.",
            "Connect the normal-form carriers to concrete source IDs and physical control-parameter candidates.",
        ),
        (
            "Magnetic/torsion",
            "High-value bridge between gyromagnetic motion, helicity, Elsasser balance, and matter dynamics; now upgraded to vector-MHD helicity/torsion carriers with a Python certificate.",
            "Connect vector-MHD torsion/helicity semantics to vortex-core enclosure and gyromagnetic loop-index certificates.",
        ),
        (
            "Quantum/matter",
            "Matter-facing proof lane for conservation, criticality, Bell bounds, and dark distribution claims; now upgraded with diagonal density/probability carriers, Bell-window semantics, and conservation certificates.",
            "Lift diagonal probability carriers toward complex density matrices and CPTP channel composition.",
        ),
    ]
    for idx, (family, reason, upgrade) in enumerate(upgrade_order, start=1):
        lines.append(f"| {idx} | {family} | {reason} | {upgrade} |")

    lines.extend([
        "",
        "## Isabelle Metrics",
        "",
        "| Family | Definitions | Theorems/Lemmas | Assumes | Types/Consts | Shortcut Hits |",
        "|---|---:|---:|---:|---:|---:|",
    ])
    for row in rows:
        lines.append(
            f"| {row['family']} | {row['definition_count']} | "
            f"{row['theorem_or_lemma_count']} | {row['assumes_count']} | "
            f"{row['type_or_const_count']} | {row['forbidden_shortcut_hits']} |"
        )
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    rows = build_rows()
    write_csv(rows)
    write_json(rows)
    write_md(rows)


if __name__ == "__main__":
    main()

