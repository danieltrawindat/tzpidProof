from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent
INPUT = ROOT / "TZPID_THEOREM_NAMES.csv"
OUT_CSV = ROOT / "TZPID_THEOREM_SEMANTIC_QUEUE.csv"
OUT_MD = ROOT / "TZPID_THEOREM_SEMANTIC_QUEUE_SUMMARY.md"
OUT_TRIAGE_CSV = ROOT / "TZPID_TRIAGE_CLASSIFICATION.csv"
OUT_TRIAGE_MD = ROOT / "TZPID_TRIAGE_CLASSIFICATION.md"

PHASE2_IDS = {
    "ID7732", "ID7733", "ID6819", "ID7257", "ID7259", "ID7177", "ID7207",
    "ID0230", "ID0256", "ID6583", "ID0362", "ID0104", "ID8796",
    "ID10786", "ID10787", "ID10788", "ID10789", "ID10790",
    "ID0353", "ID0395", "ID0470", "ID10791", "ID10792",
    "ID0285", "ID0245", "ID1837",
    "ID10146", "ID0092", "ID0093", "ID0037", "ID0085", "ID0087",
    "ID0038", "ID0039", "ID0040", "ID0044", "ID0089", "ID0090",
    "ID9758", "ID9761", "ID10130", "ID10131", "ID10145", "ID10272",
    "ID10264", "ID9513", "ID0143", "ID0105", "ID0115", "ID0117",
    "ID0120", "ID0144", "ID9955", "ID0261", "ID9492", "ID9494",
    "ID0099", "ID0097",
}

BATCH001_IDS = {
    "ID0137", "ID0234", "ID0399", "ID0522", "ID1007", "ID1009",
    "ID1010", "ID1014", "ID1024", "ID1025", "ID1204", "ID1585",
    "ID1693", "ID1829", "ID1845", "ID1918", "ID1924", "ID2045",
    "ID2306", "ID2730", "ID2741", "ID2916", "ID2990", "ID2991",
    "ID2992",
}

BATCH002_IDS = {
    "ID3286", "ID3287", "ID3288", "ID3289", "ID3303", "ID3305",
    "ID3312", "ID3314", "ID3315", "ID3316", "ID3317", "ID3378",
    "ID3606", "ID3613", "ID3616", "ID3617", "ID3642", "ID3650",
    "ID3651", "ID3653", "ID3654", "ID3662", "ID3663", "ID3668",
    "ID3677", "ID3716", "ID3872", "ID3888", "ID4191", "ID4195",
}

BATCH003_IDS = {
    "ID4201", "ID4216", "ID4217", "ID4225", "ID4231", "ID4700",
    "ID5737", "ID5751", "ID5797", "ID5813", "ID5992", "ID6000",
    "ID6092", "ID9004", "ID9005", "ID9157", "ID9291", "ID9618",
    "ID9619", "ID9633", "ID9656", "ID9827", "ID9887", "ID9931",
    "ID9989", "ID10104",
}

BATCH004_IDS = {
    "ID0006", "ID0054", "ID9999",
}

BATCH005_IDS = {
    "ID0017", "ID0041", "ID0065", "ID0170", "ID10250", "ID1802",
    "ID4215", "ID4233", "ID4252", "ID4256", "ID4708", "ID5738",
    "ID6488", "ID7754", "ID8522", "ID8523", "ID9902", "ID9990",
    "ID9999",
}

BATCH006_IDS = {
    "ID0006", "ID10072", "ID10253", "ID4202", "ID4213", "ID4710",
    "ID4711", "ID4713", "ID5743", "ID5744", "ID5806", "ID5812",
    "ID6053", "ID8521", "ID9999",
}

BATCH007_IDS = {
    "ID0001", "ID0012", "ID0015", "ID0017", "ID0019", "ID0049",
    "ID0050", "ID0053", "ID0057", "ID0060", "ID0061", "ID0062",
    "ID0063", "ID0065", "ID0070", "ID0073",
}

BATCH008_IDS = {
    "ID0000", "ID0001", "ID0002", "ID0003", "ID0004", "ID0016",
    "ID0017", "ID0020", "ID0032", "ID0173", "ID0174",
}

BATCH009_IDS = {
    "ID0000", "ID0001", "ID0004", "ID0009", "ID0018", "ID0026",
    "ID0030", "ID0032", "ID0036", "ID0046", "ID0054", "ID0080",
}

BATCH010_IDS = {
    "ID0002", "ID0007", "ID0046", "ID0047", "ID0180", "ID0181",
    "ID0182", "ID0183", "ID0185", "ID0186", "ID0187",
}

BATCH011_IDS = {
    "ID4214", "ID4223", "ID4224", "ID4229", "ID4363", "ID4698",
    "ID5802", "ID5803", "ID5758", "ID9999",
}

BATCH012_IDS = {
    "ID4206", "ID8520", "ID9595", "ID9973", "ID3902",
    "ID10247", "ID9999",
}

BATCH013_IDS = {
    "ID0239", "ID9579", "ID3322", "ID10098", "ID10099", "ID9999",
}

BATCH014_IDS = {
    "ID9999",
}

BATCH015_IDS = {
    "ID9529", "ID9999",
}

BATCH016_IDS = {
    "ID9999", "ID10244", "ID10257",
}

BATCH017_IDS = {
    "ID9999", "ID10147",
}

BATCH018_IDS = {
    "ID9999",
}

BATCH019_IDS = {
    "ID9999",
}


TRIAGE_ACTIONS = {
    "emergence_bifurcation_triage": "Batch 011 candidate: bifurcation and emergence semantics.",
    "operator_spectral_triage": "Promote into an operator/spectral follow-up or merge with Batch006.",
    "field_magnetic_torsion_triage": "Promote into a vector, magnetic, or torsion follow-up or merge with Batch005.",
    "orbital_gyromagnetic_triage": "Promote into an orbital and gyromagnetic movement follow-up.",
    "geometry_curvature_triage": "Promote into a geometry/curvature follow-up or merge with Batch008.",
    "topology_category_triage": "Promote into a topology/category follow-up.",
    "dynamics_stability_triage": "Promote into a dynamics/stability follow-up or merge with Batch009.",
    "resonance_locking_triage": "Promote into a phase-locking and resonance follow-up.",
    "quantum_matter_triage": "Promote into a quantum/matter follow-up.",
    "misc_source_review_triage": "Manual source review required before semantic translation.",
}


def classify(name: str, role: str, id_: str) -> tuple[str, str]:
    text = f"{id_} {name} {role}".lower()
    if id_ in PHASE2_IDS:
        return "phase2_already_started", "existing_phase2_family"
    if id_ in BATCH001_IDS:
        return "batch001_started", "first_master_registry_segment"
    if id_ in BATCH002_IDS:
        return "batch002_started", "spectral_helicity_kk_segment"
    if id_ in BATCH003_IDS:
        return "batch003_started", "candidate_real_algebra_segment"
    if id_ in BATCH004_IDS and any(k in text for k in [
        "vacuumenergydensity", "boundaryquantumeffects", "vacuum energy extraction",
        "information-theoretic lower bound", "dissipative energy decay",
        "local uniqueness bound", "linear dispersion relation"
    ]):
        return "batch004_started", "remaining_candidate_real_algebra"
    if id_ in BATCH005_IDS and any(k in text for k in [
        "topological", "helicity", "chern", "flux quantization",
        "linking", "dipole topological", "macroscopic flux",
        "toroidal boundary", "quantum flux"
    ]):
        return "batch005_started", "topology_vector_segment"
    if id_ in BATCH006_IDS and any(k in text for k in [
        "eigenvalue", "frequency", "kaluza", "hamiltonian",
        "intermodal", "beat", "spectral", "modal"
    ]):
        return "batch006_started", "operator_spectral_segment"
    if id_ in BATCH007_IDS and any(k in text for k in [
        "quantum", "coherence", "decoherence", "cptp", "channel",
        "measurement", "noise", "commutator", "critical", "thermo",
        "entangle", "multipartite", "qubit", "spinor", "transport",
        "superselection", "fluctuation", "continuousvariable"
    ]):
        return "batch007_started", "quantum_open_system_segment"
    if id_ in BATCH008_IDS and any(k in text for k in [
        "manifold", "curvature", "causalloop", "dimensionalambiguity",
        "hyperdimensionalspan", "winding", "characteristicclass",
        "berryphase", "fieldequation", "laplacian", "actionfunctional",
        "leastaction", "nullspaceprojection", "lemniscatic", "holonomy"
    ]):
        return "batch008_started", "geometry_manifold_segment"
    if id_ in BATCH009_IDS and any(k in text for k in [
        "stability", "oscillator", "stochasticdrift", "nonlinearity",
        "temporaldisplacement", "confinedmode", "emergentrotation",
        "renormalization", "runningphysicalconstants", "zeropointfluctuations",
        "vacuumpolarization", "semiclassical", "casimir"
    ]):
        return "batch009_started", "dynamics_scaling_segment"
    if id_ in BATCH010_IDS and any(k in text for k in [
        "trawinbaseunit", "observerdependentstates", "bayesianevidence",
        "falsifiabilityconstraint", "0181_proof", "0182_proof",
        "0183_proof", "0184_proof", "0185_proof", "0186_proof",
        "0187_proof", "0188_proof", "0189_proof"
    ]):
        return "batch010_started", "meta_foundation_segment"
    if id_ in BATCH011_IDS and any(k in text for k in [
        "density", "magnetic field", "curl field", "magnetic flux",
        "quadrupole", "gyromagnetic berry", "torsion evolution",
        "pattern torsion", "woltjer", "magnon-phonon", "elsasser",
        "flux tunneling", "dipole non-annihilation"
    ]):
        return "batch011_started", "magnetic_torsion_segment"
    if id_ in BATCH012_IDS and any(k in text for k in [
        "solar laplacian", "tidal wavelength", "wavelength quantization",
        "4d effective theory", "massive field", "r_kk", "spectral inversion",
        "kk mode coupling", "hamilton", "alfvén mode", "alfven mode",
        "harmonic-kk", "spectral gap"
    ]):
        return "batch012_started", "operator_spectral_followup_segment"
    if id_ in BATCH013_IDS and any(k in text for k in [
        "borsuk", "buckingham", "dipole constraint topology",
        "fine structure from topology", "universal toroidal",
        "adjoint functor", "dimensional access", "global phase symmetry",
        "encoding-decoding", "surface dominance", "categorical framework"
    ]):
        return "batch013_started", "topology_category_followup_segment"
    if id_ in BATCH014_IDS and any(k in text for k in [
        "accumulated force", "geometric flow", "accumulation dynamics",
        "global weak existence", "dissipative stability",
        "logarithmic local uniqueness", "numerical stability",
        "linear stability", "newtonian limit", "nonlinear dispersion"
    ]):
        return "batch014_started", "dynamics_stability_followup_segment"
    if id_ in BATCH015_IDS and any(k in text for k in [
        "infinite-order phase", "phase transition", "r_tzp",
        "symmetry-fixed bifurcation", "tzp emergence", "emergence mechanism",
        "planck oscillations", "emergence criterion"
    ]):
        return "batch015_started", "emergence_bifurcation_followup_segment"
    if id_ in BATCH016_IDS and any(k in text for k in [
        "celestial gyromagnetic", "tidal deformation",
        "spiral pitch angle", "first-order orbital shift"
    ]):
        return "batch016_started", "orbital_gyromagnetic_followup_segment"
    if id_ in BATCH017_IDS and any(k in text for k in [
        "vacuum divergence", "electron conservation", "universal criticality",
        "dark matter distribution", "critical exponent", "quantum violation",
        "bell inequality"
    ]):
        return "batch017_started", "quantum_matter_followup_segment"
    if id_ in BATCH018_IDS and any(k in text for k in [
        "phase-locking bifurcation", "pitchfork bifurcation",
        "resonance capture", "sufficient condition for phase locking",
        "lemniscate saddle"
    ]):
        return "batch018_started", "resonance_locking_followup_segment"
    if id_ in BATCH019_IDS and any(k in text for k in [
        "curvature coupling"
    ]):
        return "batch019_started", "geometry_curvature_closeout_segment"
    if any(k in text for k in [
        "phase-locking", "phase locking", "resonance capture",
        "sufficient condition for phase locking", "pitchfork", "lemniscate saddle"
    ]):
        return "triaged_resonance_locking", "resonance_locking_triage"
    if any(k in text for k in [
        "bifurcation", "emergence", "infinite-order phase", "phase transition",
        "r_tzp", "creative singularity", "tzp emergence"
    ]):
        return "triaged_emergence_bifurcation", "emergence_bifurcation_triage"
    if any(k in text for k in [
        "4d effective theory", "massive field", "kk mode", "harmonic-kk",
        "spectral inversion", "spectral gap", "laplacian", "hamilton",
        "alfvén mode", "alfven mode", "wavelength quantization",
        "tidal wavelength", "wave equation", "eigenvalue", "frequency",
        "modal", "kaluza"
    ]):
        return "triaged_operator_spectral_mode", "operator_spectral_triage"
    if any(k in text for k in [
        "density", "magnetic field", "curl field", "magnetic flux",
        "quadrupole", "torsion", "woltjer", "elsasser",
        "gyromagnetic berry", "flux tunneling", "magnon-phonon",
        "helicity", "chern", "linking", "hopf", "flux quantization",
        "dipole non-annihilation"
    ]):
        return "triaged_field_magnetic_torsion", "field_magnetic_torsion_triage"
    if any(k in text for k in [
        "celestial gyromagnetic", "tidal deformation", "spiral pitch angle",
        "orbital", "gyromagnetic motion"
    ]):
        return "triaged_orbital_gyromagnetic", "orbital_gyromagnetic_triage"
    if any(k in text for k in [
        "curvature coupling", "accumulated curvature"
    ]):
        return "triaged_geometry_curvature", "geometry_curvature_triage"
    if any(k in text for k in [
        "borsuk", "buckingham", "dipole constraint topology",
        "fine structure from topology", "universal toroidal",
        "adjoint functor", "encoding-decoding", "categorical framework",
        "dimensional access", "global phase symmetry", "surface dominance",
        "topological", "topology"
    ]):
        return "triaged_topology_category", "topology_category_triage"
    if any(k in text for k in [
        "force functional", "geometric flow", "accumulation dynamics",
        "global weak existence", "dissipative stability", "numerical stability",
        "linear stability", "local uniqueness", "newtonian limit",
        "dispersion shift", "orbital shift", "stability", "oscillator",
        "renormalization", "semiclassical", "casimir"
    ]):
        return "triaged_dynamics_stability", "dynamics_stability_triage"
    if any(k in text for k in [
        "electron conservation", "quantum violation", "dark matter distribution",
        "vacuum divergence", "universal critical", "critical exponent",
        "quantum", "coherence", "decoherence", "channel", "measurement",
        "commutator", "entangle", "qubit", "spinor", "bell inequality"
    ]):
        return "triaged_quantum_matter", "quantum_matter_triage"
    if any(k in text for k in ["helicity", "chern", "linking", "hopf", "flux quantization", "topological"]):
        return "needs_vector_topology_semantics", "topology_or_helicity"
    if any(k in text for k in ["hamiltonian", "wave equation", "eigenvalue", "frequency", "modal", "kaluza"]):
        return "needs_operator_or_spectral_semantics", "operator_spectral"
    if any(k in text for k in ["relation", "scaling", "bound", "pressure", "energy"]):
        return "candidate_real_algebra", "algebra_or_inequality"
    if "needs_semantic_translation" in text:
        return "needs_semantic_translation", "unclassified_named_theorem"
    return "triaged_misc_source_review", "misc_source_review_triage"


def main() -> None:
    rows = list(csv.DictReader(INPUT.open(newline="", encoding="utf-8-sig")))
    out_rows = []
    seen = set()
    for idx, row in enumerate(rows, start=1):
        key = (row["source"], row["id"], row["name"])
        duplicate = key in seen
        seen.add(key)
        status, cls = classify(row["name"], row["obligation_role"], row["id"])
        out_rows.append({
            "queue_index": idx,
            "source": row["source"],
            "id": row["id"],
            "name": row["name"],
            "kind": row["kind"],
            "obligation_role": row["obligation_role"],
            "semantic_anchor_id": row["semantic_anchor_id"],
            "source_file": row["source_file"],
            "line": row["line"],
            "translation_status": status,
            "translation_class": cls,
            "duplicate_source_id_name": "yes" if duplicate else "no",
        })

    with OUT_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(out_rows[0].keys()))
        writer.writeheader()
        writer.writerows(out_rows)

    triage_rows = [
        {
            "queue_index": r["queue_index"],
            "source": r["source"],
            "id": r["id"],
            "name": r["name"],
            "triage_status": r["translation_status"],
            "triage_class": r["translation_class"],
            "suggested_next_action": TRIAGE_ACTIONS.get(r["translation_class"], "Review before promotion."),
            "source_file": r["source_file"],
            "line": r["line"],
        }
        for r in out_rows
        if r["translation_status"].startswith("triaged_")
    ]
    with OUT_TRIAGE_CSV.open("w", newline="", encoding="utf-8") as f:
        triage_fieldnames = [
            "queue_index",
            "source",
            "id",
            "name",
            "triage_status",
            "triage_class",
            "suggested_next_action",
            "source_file",
            "line",
        ]
        writer = csv.DictWriter(f, fieldnames=triage_fieldnames)
        writer.writeheader()
        writer.writerows(triage_rows)

    status_counts = Counter(r["translation_status"] for r in out_rows)
    class_counts = Counter(r["translation_class"] for r in out_rows)
    source_counts = Counter(r["source"] for r in out_rows)

    lines = [
        "# TZPID Theorem Semantic Queue Summary",
        "",
        "Generated: 2026-06-07",
        "",
        f"- Input rows: `{len(rows)}`",
        f"- Unique `(source, id, name)` rows: `{len(seen)}`",
        f"- Output: `{OUT_CSV.name}`",
        "",
        "## Translation Status Counts",
        "",
        "| Status | Count |",
        "|---|---:|",
    ]
    for status, count in status_counts.most_common():
        lines.append(f"| {status} | {count} |")
    lines.extend(["", "## Translation Class Counts", "", "| Class | Count |", "|---|---:|"])
    for cls, count in class_counts.most_common():
        lines.append(f"| {cls} | {count} |")
    lines.extend(["", "## Source Counts", "", "| Source | Count |", "|---|---:|"])
    for source, count in source_counts.most_common():
        lines.append(f"| {source} | {count} |")
    lines.extend([
        "",
        "## Operating Rule",
        "",
        "Rows marked `batch001_started` are the first master-registry segment now being translated into Isabelle/HOL.",
        "Rows marked `phase2_already_started` are covered by the current Phase 2 family files.",
        "Rows marked `batch005_started` are the vector/topology segment now translated through the shared topology-vector scaffold.",
        "Rows marked `batch006_started` are the operator/spectral segment now translated through the shared operator-spectral scaffold.",
        "Rows marked `batch007_started` are the quantum/open-system segment now translated through the shared quantum-open-system scaffold.",
        "Rows marked `batch008_started` are the geometry/manifold segment now translated through the shared geometry-manifold scaffold.",
        "Rows marked `batch009_started` are the dynamics/scaling segment now translated through the shared dynamics-scaling scaffold.",
        "Rows marked `batch010_started` are the meta-foundation segment now translated through the shared meta-foundation scaffold.",
        "Rows marked `batch011_started` are the magnetic/torsion segment now translated through the shared magnetic-torsion scaffold.",
        "Rows marked `batch012_started` are the operator/spectral follow-up rows now translated through the operator-spectral scaffold.",
        "Rows marked `batch013_started` are the topology/category follow-up rows now translated through the category/topology scaffold.",
        "Rows marked `batch014_started` are the dynamics/stability follow-up rows now translated through the dynamics-stability scaffold.",
        "Rows marked `batch015_started` are the emergence/bifurcation follow-up rows now translated through the TZP emergence scaffold.",
        "Rows marked `batch016_started` are the orbital/gyromagnetic follow-up rows now translated through the movement-mechanism scaffold.",
        "Rows marked `batch017_started` are the quantum/matter follow-up rows now translated through the quantum-matter scaffold.",
        "Rows marked `batch018_started` are the resonance-locking follow-up rows now translated through the phase-locking scaffold.",
        "Rows marked `batch019_started` are the geometry/curvature closeout rows now translated through the curvature-coupling scaffold.",
        "Rows marked `triaged_*` now have a family classification and should be promoted as named follow-up batches.",
    ])
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")

    triage_counts = Counter(r["triage_class"] for r in triage_rows)
    triage_source_counts = Counter(r["source"] for r in triage_rows)
    triage_lines = [
        "# TZPID Triage Classification",
        "",
        "Generated: 2026-06-07",
        "",
        f"- Triaged rows: `{len(triage_rows)}`",
        f"- Output CSV: `{OUT_TRIAGE_CSV.name}`",
        "",
        "## Class Counts",
        "",
        "| Triage Class | Count | Suggested Next Action |",
        "|---|---:|---|",
    ]
    for cls, count in triage_counts.most_common():
        triage_lines.append(f"| {cls} | {count} | {TRIAGE_ACTIONS.get(cls, 'Review before promotion.')} |")
    triage_lines.extend(["", "## Source Counts", "", "| Source | Count |", "|---|---:|"])
    for source, count in triage_source_counts.most_common():
        triage_lines.append(f"| {source} | {count} |")
    triage_lines.extend([
        "",
        "## Full Listing",
        "",
        "| Queue | Source | ID | Name | Triage Class | Suggested Next Action |",
        "|---:|---|---|---|---|---|",
    ])
    for row in sorted(triage_rows, key=lambda r: int(r["queue_index"])):
        name = row["name"].replace("|", "\\|")
        action = row["suggested_next_action"].replace("|", "\\|")
        triage_lines.append(
            f"| {row['queue_index']} | {row['source']} | {row['id']} | {name} | "
            f"{row['triage_class']} | {action} |"
        )
    OUT_TRIAGE_MD.write_text("\n".join(triage_lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
