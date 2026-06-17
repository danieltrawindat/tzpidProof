from __future__ import annotations

import csv
import re
from collections import Counter
from datetime import datetime
from pathlib import Path


ROOT = Path(r"D:\TZPIDProof")
PEER_REVIEW = ROOT / "peer_review"
TEX_DIR = PEER_REVIEW / "tex"
PDF_DIR = PEER_REVIEW / "pdf"
OUT_DIR = PEER_REVIEW / "coverage"
MASTER = ROOT / "TZPID_ALL_IDS_CANONICAL_EQUATION_MASTER_with_export.csv"
ISABELLE_DIR = ROOT / "tzpid_proof" / "isabelle_tzpid"


ID_RE = re.compile(r"\bID\s*[-:]?\s*(\d{1,5})\b", re.IGNORECASE)
DOI_RE = re.compile(r"10\.5281/zenodo\.\d+")
ENV_RE = re.compile(
    r"\\begin\{(theorem|lemma|definition|axiom|proposition|corollary)\}",
    re.IGNORECASE,
)
EQ_RE = re.compile(
    r"\\begin\{(?:equation|align|gather|multline|eqnarray)\*?\}|\\\[|\\\("
)


THEORY_HINTS = {
    "nested_hyperspherical": [
        "TZPID_NestedHypersphere_Focus",
        "TZPID_NestedHypersphere_Computational_Checks",
        "TZPID_NestedHypersphere_Typed_Projection",
        "TZPID_NestedHypersphere_S3_Spectrum",
    ],
    "phase_locking": [
        "TZPID_PhaseLockingResonance_Focus",
        "TZPID_PhaseLockingResonance_Computational_Checks",
        "TZPID_PhaseLockingResonance_Typed_RatioSelection",
        "TZPID_PhaseLockingResonance_CaptureBasin",
        "TZPID_PhaseLockingResonance_KuramotoFiniteN",
    ],
    "musical": [
        "TZPID_FifthFlip_CrystalScaleInvariance",
        "TZPID_Ripple_LogPeriodic_PhiBridge",
    ],
    "gyromagnetic": [
        "TZPID_GyromagneticMovement_Focus",
        "TZPID_GyromagneticMovement_Computational_Checks",
        "TZPID_GyromagneticMovement_Typed_PhaseGradient",
        "TZPID_GyromagneticMovement_VectorCalculus",
        "TZPID_GyromagneticMovement_MHD_Helicity",
        "TZPID_GyromagneticMovement_CirculationDiagnostic",
        "TZPID_GyromagneticMovement_CorrectedWinding",
        "TZPID_GyromagneticMovement_LoopIndex",
        "TZPID_GyroWave_Sky",
    ],
    "gravity": [
        "TZPID_Gravity_Focus",
        "TZPID_PeriodicTable_GravitationalCharge",
        "TZPID_FoldTime_Foundation",
        "TZPID_HubbleBreathing_Enclosure",
        "TZPID_HubbleBreathing_FriedmannComponents",
    ],
    "bessel": [
        "TZPID_HypersphericalBesselResidualBridge_Focus",
        "TZPID_HypersphericalBesselResidualBridge_Computational_Checks",
        "TZPID_HypersphericalBesselResidualBridge_Math_Checks",
        "TZPID_HypersphericalBesselResidualBridge_Phase2_Model",
        "TZPID_Bessel_External_Certificates",
    ],
    "energy_to_matter": [
        "TZPID_EnergyMatter_Focus",
        "TZPID_MatterCreation_ThresholdSpine",
        "TZPID_MatterCreation_TemporalFlow",
        "TZPID_MatterCreation_CriticalityBridge",
        "TZPID_MatterCreation_PressureEoS",
    ],
    "topological": [
        "TZPID_TopologicalUnification_Focus",
        "TZPID_Topology_Vector_Model",
        "TZPID_TopologyVector_Invariants",
        "TZPID_TopologyCategory_Carriers",
    ],
    "einstein": [
        "TZPID_Einstein_Focus",
        "TZPID_Einstein_Computational_Checks",
    ],
    "dag": [
        "TZPID_DerivationOrder",
    ],
    "zero_point": [
        "TZPID_ZenodoSpines_Focus",
        "TZPID_ZenodoSpines_Computational_Checks",
        "TZPID_Meta_Foundation_Model",
    ],
    "quantum": [
        "TZPID_Quantum_Open_System_Model",
        "TZPID_QuantumOpenSystem_Carriers",
        "TZPID_QuantumMatter_ProbabilityCarriers",
    ],
    "well_wall_wave": [
        "TZPID_PhaseLockingResonance_Focus",
        "TZPID_PhaseLockingResonance_KuramotoFiniteN",
        "TZPID_GyroWave_Sky",
    ],
    "elsasser": [
        "TZPID_GyromagneticMovement_MHD_Helicity",
        "TZPID_GyroWave_Sky",
    ],
    "magnetic": [
        "TZPID_Magnetic_Torsion_Model",
        "TZPID_MagneticTorsion_VectorMHD",
        "TZPID_GyromagneticMovement_MHD_Helicity",
    ],
    "information": [
        "TZPID_TopologicalUnification_Focus",
        "TZPID_QuantumMatter_ProbabilityCarriers",
    ],
}


def normalize_id(match: str) -> str:
    return f"ID{int(match):04d}"


def load_master() -> dict[str, dict[str, str]]:
    with MASTER.open("r", encoding="utf-8-sig", newline="") as f:
        return {row["id"].strip(): row for row in csv.DictReader(f)}


def clean_latex_fragment(value: str) -> str:
    value = re.sub(r"%.*", "", value)
    value = value.replace("\n", " ")
    value = re.sub(r"\\(?:large|small|emph|textbf|textit|href)\b(?:\[[^\]]*\])?", "", value)
    value = value.replace("\\\\", " ")
    value = re.sub(r"\s+", " ", value)
    return value.strip(" {}")


def extract_title(text: str, fallback: str) -> str:
    m = re.search(r"\\title\{(.+?)\}\s*\\author", text, flags=re.DOTALL)
    if not m:
        m = re.search(r"\\title\{(.+?)\}", text, flags=re.DOTALL)
    return clean_latex_fragment(m.group(1)) if m else fallback


def find_pdf(stem: str) -> str:
    candidates = [
        PDF_DIR / f"{stem}.pdf",
        TEX_DIR / f"{stem}.pdf",
        TEX_DIR / f"{stem}.generated.pdf",
    ]
    for candidate in candidates:
        if candidate.exists():
            return str(candidate)
    return ""


def classify_file(path: Path) -> tuple[str, str, int | str]:
    name = path.name
    if m := re.match(r"paper(\d+)_", name):
        return "core", f"paper{int(m.group(1)):02d}", int(m.group(1))
    if m := re.match(r"companion(\d+)_", name):
        return "companion", f"companion{int(m.group(1)):02d}", int(m.group(1))
    return "other", path.stem, ""


def theory_matches(stem: str, available: set[str]) -> list[str]:
    key = stem.lower()
    selected: list[str] = []
    if stem.startswith("companion"):
        for theory in [
            "TZPID_Zenodo_MainStructures_Coverage",
            "TZPID_ZenodoSpines_Focus",
            "TZPID_ZenodoSpines_Computational_Checks",
        ]:
            if theory in available:
                selected.append(theory)
    for marker, theories in THEORY_HINTS.items():
        marker_words = marker.split("_")
        if marker in key or any(word in key for word in marker_words if len(word) >= 6):
            selected.extend(theory for theory in theories if theory in available)
    if stem.startswith("paper1_"):
        selected.extend(t for t in THEORY_HINTS["nested_hyperspherical"] if t in available)
    elif stem.startswith("paper2_"):
        selected.extend(t for t in THEORY_HINTS["phase_locking"] if t in available)
    elif stem.startswith("paper3_"):
        selected.extend(t for t in THEORY_HINTS["musical"] if t in available)
    elif stem.startswith("paper4_"):
        selected.extend(t for t in THEORY_HINTS["gyromagnetic"] if t in available)
    elif stem.startswith("paper5_"):
        selected.extend(t for t in THEORY_HINTS["gravity"] if t in available)
    elif stem.startswith("paper6_"):
        selected.extend(t for t in THEORY_HINTS["bessel"] if t in available)
    elif stem.startswith("paper7_"):
        selected.extend(t for t in THEORY_HINTS["energy_to_matter"] if t in available)
    elif stem.startswith("paper8_"):
        selected.extend(t for t in THEORY_HINTS["topological"] if t in available)
    elif stem.startswith("paper9_"):
        selected.extend(t for t in THEORY_HINTS["einstein"] if t in available)
    elif stem.startswith("paper10_"):
        selected.extend(t for t in THEORY_HINTS["dag"] if t in available)
    return sorted(set(selected))


def status_summary(ids: list[str], master: dict[str, dict[str, str]]) -> str:
    counts = Counter()
    for id_ in ids:
        row = master.get(id_)
        status = (row or {}).get("wolfram_status", "").strip() or "blank"
        counts[status] += 1
    return "; ".join(f"{key}:{counts[key]}" for key in sorted(counts))


def coverage_status(
    ids: list[str],
    missing: list[str],
    equation_count: int,
    theory_count: int,
    wolfram_summary: str,
) -> str:
    if missing:
        return "needs_registry_sync"
    if not ids and equation_count:
        return "needs_id_extraction"
    if not ids:
        return "prose_only_or_needs_scan"
    if theory_count == 0:
        return "needs_isabelle_mapping"
    if "blank:" in wolfram_summary or not wolfram_summary:
        return "partial_certificate"
    return "covered"


def row_for_file(path: Path, master: dict[str, dict[str, str]], theories: set[str]) -> dict[str, str]:
    text = path.read_text(encoding="utf-8", errors="replace")
    kind, key, number = classify_file(path)
    structure_role = {
        "core": "numbered_core_series",
        "companion": "zenodo_main_structure",
    }.get(kind, "other")
    ids = sorted({normalize_id(m) for m in ID_RE.findall(text)})
    missing = [id_ for id_ in ids if id_ not in master]
    present = [id_ for id_ in ids if id_ in master]
    doi_list = sorted(set(DOI_RE.findall(text)))
    theorem_env_count = len(ENV_RE.findall(text))
    theorem_word_count = len(re.findall(r"\b(theorem|lemma|definition|axiom|proposition|corollary)\b", text, re.I))
    equation_count = len(EQ_RE.findall(text))
    matched_theories = theory_matches(path.stem, theories)
    wolfram_summary = status_summary(present, master)
    status = coverage_status(ids, missing, equation_count, len(matched_theories), wolfram_summary)
    return {
        "paper_key": key,
        "paper_number": str(number),
        "paper_kind": kind,
        "structure_role": structure_role,
        "file_name": path.name,
        "title": extract_title(text, path.stem.replace("_", " ")),
        "tex_path": str(path),
        "pdf_path": find_pdf(path.stem),
        "pdf_exists": "yes" if find_pdf(path.stem) else "no",
        "doi_count": str(len(doi_list)),
        "doi_list": "; ".join(doi_list),
        "ids_cited_count": str(len(ids)),
        "ids_cited": "; ".join(ids),
        "ids_in_master_count": str(len(present)),
        "missing_ids_count": str(len(missing)),
        "missing_ids": "; ".join(missing),
        "equation_like_count": str(equation_count),
        "theorem_env_count": str(theorem_env_count),
        "theorem_word_count": str(theorem_word_count),
        "wolfram_status_summary": wolfram_summary,
        "isabelle_theory_count": str(len(matched_theories)),
        "isabelle_theories": "; ".join(matched_theories),
        "coverage_status": status,
    }


def markdown_table(rows: list[dict[str, str]], columns: list[str]) -> str:
    out = []
    out.append("| " + " | ".join(columns) + " |")
    out.append("| " + " | ".join("---" for _ in columns) + " |")
    for row in rows:
        values = []
        for col in columns:
            value = row.get(col, "").replace("|", "\\|").replace("\n", " ")
            if len(value) > 120:
                value = value[:117] + "..."
            values.append(value)
        out.append("| " + " | ".join(values) + " |")
    return "\n".join(out)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    master = load_master()
    theories = {path.stem for path in ISABELLE_DIR.glob("*.thy")}
    tex_files = sorted(
        path for path in TEX_DIR.glob("*.tex") if ".generated" not in path.name and not path.name.endswith(".tpl")
    )
    rows = [row_for_file(path, master, theories) for path in tex_files]

    fieldnames = list(rows[0].keys()) if rows else []
    matrix_path = OUT_DIR / "PEER_REVIEW_PAPER_COVERAGE_MATRIX.csv"
    with matrix_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    companion_rows = [row for row in rows if row["paper_kind"] == "companion"]
    core_rows = [row for row in rows if row["paper_kind"] == "core"]
    companion_path = OUT_DIR / "ZENODO_27_MAIN_STRUCTURE_COVERAGE_MATRIX.csv"
    with companion_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(companion_rows)

    missing_ids = sorted({id_ for row in rows for id_ in row["missing_ids"].split("; ") if id_})
    no_ids = [row for row in rows if row["ids_cited_count"] == "0"]
    needs_registry = [row for row in rows if row["coverage_status"] == "needs_registry_sync"]
    needs_id_extraction = [row for row in rows if row["coverage_status"] == "needs_id_extraction"]
    needs_isabelle = [row for row in rows if row["coverage_status"] == "needs_isabelle_mapping"]
    partial = [row for row in rows if row["coverage_status"] == "partial_certificate"]
    covered = [row for row in rows if row["coverage_status"] == "covered"]

    core_numbers = sorted(int(row["paper_number"]) for row in core_rows if row["paper_number"].isdigit())
    expected_core = list(range(1, max(core_numbers or [0]) + 1))
    missing_core = sorted(set(expected_core) - set(core_numbers))
    has_core_11 = any(row["paper_number"] == "11" and row["paper_kind"] == "core" for row in rows)

    status_counts = Counter(row["coverage_status"] for row in rows)
    companion_status_counts = Counter(row["coverage_status"] for row in companion_rows)
    id_total = sum(int(row["ids_cited_count"]) for row in rows)
    id_unique = sorted({id_ for row in rows for id_ in row["ids_cited"].split("; ") if id_})

    report = []
    report.append("# Peer Review Paper Coverage Audit\n")
    report.append(f"Generated: {datetime.now().isoformat(timespec='seconds')}\n")
    report.append("## Scope\n")
    report.append(f"- Core paper TeX files found: {len(core_rows)}")
    report.append(f"- Zenodo main-structure TeX files found with companion filenames: {len(companion_rows)}")
    report.append(f"- Total TeX files audited: {len(rows)}")
    report.append(f"- Core paper numbers found: {', '.join(str(n) for n in core_numbers) if core_numbers else 'none'}")
    report.append(f"- Missing core paper numbers inside found range: {', '.join(str(n) for n in missing_core) if missing_core else 'none'}")
    report.append(f"- Separate core `paper11_*.tex` present: {'yes' if has_core_11 else 'no'}")
    report.append("")
    report.append("## Registry Cross-Check\n")
    report.append(f"- Total ID citations across audited files: {id_total}")
    report.append(f"- Unique ID citations across audited files: {len(id_unique)}")
    report.append(f"- Unique cited IDs missing from master: {len(missing_ids)}")
    report.append(f"- Files with zero cited IDs: {len(no_ids)}")
    report.append("")
    report.append("## Coverage Status Counts\n")
    for key in sorted(status_counts):
        report.append(f"- {key}: {status_counts[key]}")
    report.append("")
    report.append("## 27 Zenodo Main-Structure Status Counts\n")
    for key in sorted(companion_status_counts):
        report.append(f"- {key}: {companion_status_counts[key]}")
    report.append("")
    report.append("## Core Papers\n")
    report.append(markdown_table(core_rows, [
        "paper_key",
        "file_name",
        "doi_count",
        "ids_cited_count",
        "missing_ids_count",
        "equation_like_count",
        "isabelle_theory_count",
        "coverage_status",
    ]))
    report.append("")
    report.append("## 27 Zenodo Main Structures\n")
    report.append(markdown_table(companion_rows, [
        "paper_key",
        "file_name",
        "doi_count",
        "ids_cited_count",
        "missing_ids_count",
        "equation_like_count",
        "isabelle_theory_count",
        "coverage_status",
    ]))
    report.append("")
    if missing_ids:
        report.append("## Missing IDs\n")
        report.append(", ".join(missing_ids))
        report.append("")
    if no_ids:
        report.append("## Files With No Registry IDs\n")
        report.append(markdown_table(no_ids, [
            "paper_key",
            "file_name",
            "equation_like_count",
            "theorem_word_count",
            "coverage_status",
        ]))
        report.append("")
    if needs_id_extraction:
        report.append("## Needs ID Extraction\n")
        report.append(markdown_table(needs_id_extraction, [
            "paper_key",
            "file_name",
            "equation_like_count",
            "theorem_word_count",
        ]))
        report.append("")
    if needs_isabelle:
        report.append("## Needs Isabelle Mapping\n")
        report.append(markdown_table(needs_isabelle, [
            "paper_key",
            "file_name",
            "ids_cited_count",
            "equation_like_count",
        ]))
        report.append("")
    if partial:
        report.append("## Partial Certificate Rows\n")
        report.append(markdown_table(partial, [
            "paper_key",
            "file_name",
            "ids_cited_count",
            "wolfram_status_summary",
            "isabelle_theory_count",
        ]))
        report.append("")
    report.append("## Output Files\n")
    report.append(f"- Full matrix: `{matrix_path}`")
    report.append(f"- 27 Zenodo main-structure matrix: `{companion_path}`")
    report.append("")
    (OUT_DIR / "PEER_REVIEW_COVERAGE_AUDIT.md").write_text("\n".join(report), encoding="utf-8")

    print(f"Wrote {matrix_path}")
    print(f"Wrote {companion_path}")
    print(f"Wrote {OUT_DIR / 'PEER_REVIEW_COVERAGE_AUDIT.md'}")
    print(f"core={len(core_rows)} zenodo_main_structures={len(companion_rows)} missing_ids={len(missing_ids)} no_ids={len(no_ids)}")


if __name__ == "__main__":
    main()
