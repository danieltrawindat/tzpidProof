from __future__ import annotations

import csv
import re
from collections import Counter
from datetime import datetime
from pathlib import Path


ROOT = Path(r"D:\TZPIDProof")
MASTER = ROOT / "TZPID_ALL_IDS_CANONICAL_EQUATION_MASTER_with_export.csv"
OUT_DIR = ROOT / "peer_review" / "unification_intake"
SOURCE_MATRIX = OUT_DIR / "UNIFICATION_SPINE_INTAKE_MATRIX.csv"
ID_CROSSWALK = OUT_DIR / "UNIFICATION_SPINE_ID_CROSSWALK.csv"
REPORT = OUT_DIR / "UNIFICATION_SPINE_INTAKE_PACK.md"


SOURCES = [
    {
        "source_label": "TZP Type C",
        "semantic_role": "negative-foundation convergence / divergence guard",
        "isabelle_carrier": "TZP_Type_C_Source",
        "paper_spine_target": "Nested Hyperspherical Enclosure; Energy-to-Matter; Topological Unification",
        "paths": [
            r"D:\TZPIDProof\peer_review\tex\companion03_tzp_type_c.tex",
        ],
    },
    {
        "source_label": "Trawin-Enlil Protocol",
        "semantic_role": "matter emergence from hyperspherical zero-point disharmony",
        "isabelle_carrier": "Trawin_Enlil_Protocol_Source",
        "paper_spine_target": "Energy-to-Matter; Gyromagnetic Movement; Bessel/Delta-Alpha Bridge",
        "paths": [
            r"D:\TZPIDProof\peer_review\tex\companion24_trawin_enlil_protocol.tex",
            r"D:\Tex\trawin_enlil_protocol.tex",
        ],
    },
    {
        "source_label": "Enlil-Trawin Isomorphism",
        "semantic_role": "kinematic/topological isomorphism bridge",
        "isabelle_carrier": "Enlil_Trawin_Isomorphism_Source",
        "paper_spine_target": "Gyromagnetic Movement; Topological Unification",
        "paths": [
            r"D:\Tex\TEX_20260224_182530\The_Enlil_Trawin_Isomorphism.tex",
            r"D:\Tex\TEX_20260224_182530\The_Kinematic_Origin.tex",
        ],
    },
    {
        "source_label": "Topological Unification of QM and GR",
        "semantic_role": "quantum-to-GR topological bridge",
        "isabelle_carrier": "Topological_Unification_QM_GR_Source",
        "paper_spine_target": "Topological Unification; Quantum Matter; Einstein Focus",
        "paths": [
            r"D:\TZPIDProof\peer_review\tex\companion27_topological_unification.tex",
            r"D:\TZPIDProof\peer_review\tex\paper8_topological_unification.tex",
            r"D:\Tex\topological_unification.tex",
        ],
    },
    {
        "source_label": "Entrainment Through a DAANSsphere Axis",
        "semantic_role": "axis control / entrainment / closed-loop mode steering",
        "isabelle_carrier": "Entrainment_DAANSsphere_Axis_Source",
        "paper_spine_target": "Phase Locking Resonance; Nested Hyperspherical Enclosure",
        "paths": [
            r"D:\TZPIDProof\peer_review\tex\companion14_entrainment_and_daanssphere_axis.tex",
            r"D:\Tex\Entrainment and DAANSsphere axis.tex",
        ],
    },
    {
        "source_label": "Theory of It All: Tides and Waves",
        "semantic_role": "large unification narrative / tides-waves topology",
        "isabelle_carrier": "Theory_It_All_Tides_Waves_Source",
        "paper_spine_target": "Topological Unification; WWW; Nested Hyperspherical Enclosure",
        "paths": [
            r"D:\TZPIDProof\peer_review\tex\companion26_theory_of_it_all_trawin_topology.tex",
            r"D:\Tex\TEX_20260224_182530\theory_of_it_all_trawin_topology.tex",
        ],
    },
    {
        "source_label": "Well-Wall-Wave Theory",
        "semantic_role": "cavity / boundary / wave mechanism",
        "isabelle_carrier": "Well_Wall_Wave_Source",
        "paper_spine_target": "Phase Locking Resonance; Nested Hyperspherical Enclosure",
        "paths": [
            r"D:\TZPIDProof\peer_review\tex\companion07_well_wall_wave_theory.tex",
            r"D:\Tex\well_wall_wave_theory.tex",
        ],
    },
    {
        "source_label": "WWW Source",
        "semantic_role": "well-wall-wave compact source / core cavity semantics",
        "isabelle_carrier": "WWW_Source",
        "paper_spine_target": "Phase Locking Resonance; Bessel/Delta-Alpha Bridge",
        "paths": [
            r"D:\TZPIDProof\peer_review\tex\companion08_www.tex",
            r"D:\Tex\www.tex",
        ],
    },
    {
        "source_label": "TuT / Theorum Infinitum",
        "semantic_role": "full ToE/TuT source corpus and symbolic glossary",
        "isabelle_carrier": "Theorum_Infinitum_ToE; TUT_Glossary",
        "paper_spine_target": "Master Spine Backbone; Quantum-to-GR Source Lane",
        "paths": [
            r"D:\Tex\TEX_20260224_182530\TheorumInfinitum_full_with_ToE.tex",
            r"D:\Tex\TEX_20260224_182530\theorum_infinitum_full.tex",
            r"D:\Tex\TEX_20260224_182530\TuTsybolicGlossary.tex",
            r"D:\Tex\TuTsybolicGlossary.tex",
            r"D:\Tex\TZP-THZ-TUT.tex",
        ],
    },
]


ID_RE = re.compile(r"\bID(\d{1,6})\b", re.IGNORECASE)
DISPLAY_MATH_RE = re.compile(
    r"\\\[(.*?)\\\]|\\begin\{(?:equation|align|aligned|gather|multline)\*?\}(.*?)\\end\{(?:equation|align|aligned|gather|multline)\*?\}",
    re.DOTALL,
)
INLINE_MATH_RE = re.compile(r"(?<!\\)\$(?!\$)(.{3,180}?)(?<!\\)\$", re.DOTALL)
COMMAND_RE = re.compile(r"\\[a-zA-Z]+\*?(?:\[[^\]]*\])?(?:\{[^{}]*\})?")
SPACE_RE = re.compile(r"\s+")


def normalize_id(raw: str) -> str:
    return f"ID{int(raw):04d}"


def clean_text(text: str) -> str:
    text = text.replace("\r\n", "\n")
    text = re.sub(r"%.*", "", text)
    return text


def extract_title(text: str, fallback: str) -> str:
    match = re.search(r"\\title\{(.+?)\}", text, re.DOTALL)
    if not match:
        match = re.search(r"pdftitle=\{(.+?)\}", text, re.DOTALL)
    if not match:
        return fallback
    title = match.group(1)
    title = title.replace("\\\\", " ")
    title = COMMAND_RE.sub(" ", title)
    return SPACE_RE.sub(" ", title).strip()[:240] or fallback


def extract_equation_samples(text: str, limit: int = 4) -> list[str]:
    samples: list[str] = []
    for match in DISPLAY_MATH_RE.finditer(text):
        chunk = next((g for g in match.groups() if g), "")
        chunk = SPACE_RE.sub(" ", chunk).strip()
        if 3 <= len(chunk) <= 500:
            samples.append(chunk)
        if len(samples) >= limit:
            return samples
    for match in INLINE_MATH_RE.finditer(text):
        chunk = SPACE_RE.sub(" ", match.group(1)).strip()
        if any(sym in chunk for sym in ["=", "\\", "^", "_", "\\frac", "\\int", "\\sum"]):
            samples.append(chunk)
        if len(samples) >= limit:
            return samples
    return samples


def classify_promotion(ids: list[str], equation_like_count: int, theorem_word_count: int) -> str:
    if ids and equation_like_count >= 5:
        return "promote_to_equation_semantic_wolfram_queue"
    if ids:
        return "map_existing_ids_then_promote_selectively"
    if equation_like_count >= 5 or theorem_word_count >= 5:
        return "extract_candidate_equations_before_id_minting"
    return "narrative_support_or_background"


def load_master() -> dict[str, dict[str, str]]:
    with MASTER.open("r", encoding="utf-8-sig", newline="") as f:
        return {row["id"]: row for row in csv.DictReader(f)}


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    master = load_master()
    source_rows: list[dict[str, str]] = []
    crosswalk_rows: list[dict[str, str]] = []

    for source in SOURCES:
        existing_paths: list[Path] = []
        all_ids: set[str] = set()
        all_equations: list[str] = []
        titles: list[str] = []
        equation_like_count = 0
        theorem_word_count = 0

        for path_s in source["paths"]:
            path = Path(path_s)
            if not path.exists():
                continue
            existing_paths.append(path)
            try:
                text = clean_text(path.read_text(encoding="utf-8", errors="replace"))
            except OSError:
                continue
            ids = sorted({normalize_id(m.group(1)) for m in ID_RE.finditer(text)})
            all_ids.update(ids)
            eq_samples = extract_equation_samples(text)
            all_equations.extend(eq_samples)
            titles.append(extract_title(text, path.stem))
            equation_like_count += len(DISPLAY_MATH_RE.findall(text)) + len(INLINE_MATH_RE.findall(text))
            theorem_word_count += len(re.findall(r"\b(?:theorem|lemma|corollary|proposition|axiom|definition)\b", text, re.I))

        ids_sorted = sorted(all_ids)
        ids_in_master = [i for i in ids_sorted if i in master]
        missing_ids = [i for i in ids_sorted if i not in master]
        wolfram_statuses = Counter((master[i].get("wolfram_status") or "blank") for i in ids_in_master)
        roles = Counter((master[i].get("obligation_role") or "unspecified") for i in ids_in_master)
        gold_spines = sorted({master[i].get("gold_spine", "") for i in ids_in_master if master[i].get("gold_spine", "")})

        source_rows.append(
            {
                "source_label": source["source_label"],
                "semantic_role": source["semantic_role"],
                "paper_spine_target": source["paper_spine_target"],
                "isabelle_carrier": source["isabelle_carrier"],
                "source_file_count": str(len(existing_paths)),
                "source_files": "; ".join(str(p) for p in existing_paths),
                "representative_titles": " | ".join(dict.fromkeys(titles))[:800],
                "ids_cited_count": str(len(ids_sorted)),
                "ids_cited": "; ".join(ids_sorted),
                "ids_in_master_count": str(len(ids_in_master)),
                "missing_ids_count": str(len(missing_ids)),
                "missing_ids": "; ".join(missing_ids),
                "equation_like_count": str(equation_like_count),
                "theorem_word_count": str(theorem_word_count),
                "equation_samples": " || ".join(dict.fromkeys(all_equations))[:1200],
                "master_obligation_roles": "; ".join(f"{k}:{v}" for k, v in sorted(roles.items())),
                "wolfram_status_summary": "; ".join(f"{k}:{v}" for k, v in sorted(wolfram_statuses.items())),
                "gold_spines": "; ".join(gold_spines),
                "promotion_priority": classify_promotion(ids_sorted, equation_like_count, theorem_word_count),
                "next_action": "map existing IDs first; mint only equations absent from master; then generate Wolfram forms and HOL carriers for spine-critical claims",
            }
        )

        for source_id in ids_sorted:
            row = master.get(source_id, {})
            crosswalk_rows.append(
                {
                    "source_label": source["source_label"],
                    "id": source_id,
                    "in_master": "yes" if source_id in master else "no",
                    "title": row.get("title", ""),
                    "canonical_equation": row.get("canonical_equation", ""),
                    "canonical_statement": row.get("canonical_statement", ""),
                    "obligation_role": row.get("obligation_role", ""),
                    "isabelle_kind": row.get("isabelle_kind", ""),
                    "gold_spine": row.get("gold_spine", ""),
                    "wolfram_status": row.get("wolfram_status", ""),
                    "semantic_role": source["semantic_role"],
                    "isabelle_carrier": source["isabelle_carrier"],
                    "paper_spine_target": source["paper_spine_target"],
                }
            )

    with SOURCE_MATRIX.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(source_rows[0]))
        writer.writeheader()
        writer.writerows(source_rows)

    cross_fields = [
        "source_label",
        "id",
        "in_master",
        "title",
        "canonical_equation",
        "canonical_statement",
        "obligation_role",
        "isabelle_kind",
        "gold_spine",
        "wolfram_status",
        "semantic_role",
        "isabelle_carrier",
        "paper_spine_target",
    ]
    with ID_CROSSWALK.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=cross_fields)
        writer.writeheader()
        writer.writerows(crosswalk_rows)

    generated = datetime.now().isoformat(timespec="seconds")
    total_sources = len(source_rows)
    total_files = sum(int(r["source_file_count"]) for r in source_rows)
    total_unique_ids = len({r["id"] for r in crosswalk_rows})
    total_missing_ids = sum(1 for r in crosswalk_rows if r["in_master"] == "no")
    promotion_counts = Counter(r["promotion_priority"] for r in source_rows)

    lines = [
        "# Unification Spine Intake Pack",
        "",
        f"Generated: {generated}",
        "",
        "## Purpose",
        "",
        "This pack turns the newly identified quantum-to-GR source structures into a controlled promotion queue.  The goal is to map source material to existing IDs first, then mint only genuinely absent equations, and finally promote the spine-critical claims into Wolfram and Isabelle/HOL certificate lanes.",
        "",
        "## Scope Summary",
        "",
        f"- Named source groups: {total_sources}",
        f"- Located source files: {total_files}",
        f"- Unique IDs cited across the intake set: {total_unique_ids}",
        f"- IDs missing from the synchronized master: {total_missing_ids}",
        f"- Source-level matrix: `{SOURCE_MATRIX}`",
        f"- ID-level crosswalk: `{ID_CROSSWALK}`",
        "",
        "## Promotion Counts",
        "",
    ]
    for key, value in sorted(promotion_counts.items()):
        lines.append(f"- {key}: {value}")

    lines.extend(
        [
            "",
            "## Intake Matrix",
            "",
            "| Source | Files | IDs | Missing IDs | Eq-like | Theorem words | HOL carrier | Promotion |",
            "| --- | ---: | ---: | ---: | ---: | ---: | --- | --- |",
        ]
    )
    for row in source_rows:
        lines.append(
            "| {source_label} | {source_file_count} | {ids_cited_count} | {missing_ids_count} | "
            "{equation_like_count} | {theorem_word_count} | `{isabelle_carrier}` | {promotion_priority} |".format(**row)
        )

    lines.extend(
        [
            "",
            "## Recommended Next Queue",
            "",
            "1. Start with `Topological Unification of QM and GR` and `Trawin-Enlil Protocol`, because these carry the densest quantum/GR/matter bridge semantics.",
            "2. For each cited ID, reuse the synchronized master equation and dictionary/encyclopedia text before minting new IDs.",
            "3. Promote only the paper-facing equations into Wolfram forms on the first pass; keep narrative-only claims as source evidence.",
            "4. Add HOL carriers for the promoted claims by extending `TZPID_QuantumGR_Unification_SourceLane.thy` or creating source-specific theories when the claims become theorem-level.",
            "",
            "## Notes",
            "",
            "- `DAANSsphere` is preserved as the spelling used in the located TeX sources.",
            "- Simulation scripts and external lab evidence remain separate certificate lanes; this pack only controls source-to-ID intake.",
        ]
    )
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"Wrote {SOURCE_MATRIX}")
    print(f"Wrote {ID_CROSSWALK}")
    print(f"Wrote {REPORT}")
    print(f"Named source groups: {total_sources}")
    print(f"Located source files: {total_files}")
    print(f"Unique IDs: {total_unique_ids}")
    print(f"Missing IDs: {total_missing_ids}")


if __name__ == "__main__":
    main()
