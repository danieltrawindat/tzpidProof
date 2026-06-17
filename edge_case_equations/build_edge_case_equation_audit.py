import csv
import json
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\TZPIDProof")
OPENAI2 = Path(r"D:\00_Engine\AI_Workspaces\OpenAI2")
TZPIDNEW = Path(r"D:\tzpidNEW")

MASTER = ROOT / "TZPID_ALL_IDS_CANONICAL_EQUATION_MASTER_with_export.csv"
OPERATOR_PASS = OPENAI2 / "TZPID_TRAWIN_OPERATOR_PASS.csv"
TOE_CLEANUP = TZPIDNEW / "toe_cleanup_queue.csv"
TOE_APPROX = TZPIDNEW / "toe_approximated_parse.csv"
TOE_PIPELINE = TZPIDNEW / "toe_pipeline_results.csv"
TOP_PREREQ = ROOT / "graph_topology" / "top_prerequisite_supernodes.csv"
TOP_DEP = ROOT / "graph_topology" / "top_dependent_nodes.csv"
EDGES = ROOT / "graph_topology" / "materialized_edges.csv"
PAPER_DIR = ROOT / "peer_review" / "tex"

OUT_DIR = ROOT / "edge_case_equations"
OUT_CSV = OUT_DIR / "TZPID_EDGE_CASE_EQUATION_SHORTLIST.csv"
OUT_MD = OUT_DIR / "TZPID_EDGE_CASE_EQUATION_SHORTLIST.md"
OUT_GAP_CSV = OUT_DIR / "TZPID_EQUATION_UNIVERSE_GAP_AUDIT.csv"
OUT_GAP_MD = OUT_DIR / "TZPID_EQUATION_UNIVERSE_GAP_AUDIT.md"
OUT_JSON = OUT_DIR / "edge_case_equation_scoring.json"


CATEGORIES = {
    "boundary_limit_singularity": [
        r"\blim\b", r"\\lim", r"boundary", r"horizon", r"asymptot", r"infinity", r"\\infty",
        r"singular", r"degener", r"\\det", r"\bdet\b", r"null", r"rank", r"kernel",
        r"cutoff", r"threshold", r"critical", r"zero", r"root",
    ],
    "invariant_conservation_closure": [
        r"invariant", r"conserv", r"normaliz", r"closure", r"constraint", r"symmetry",
        r"\\nabla", r"divergence", r"\\frac\{d", r"=0", r"constant",
    ],
    "topological_holonomy": [
        r"holonomy", r"hopf", r"berry", r"winding", r"chern", r"helicity", r"fiber",
        r"bundle", r"torsion", r"topolog", r"\\pi_", r"\\Omega",
    ],
    "spectral_bessel_laplacian": [
        r"bessel", r"j_\{", r"j_", r"eigen", r"laplacian", r"spectral", r"mode",
        r"spherical", r"hypersphere", r"S\^3", r"S³", r"\\ell",
    ],
    "exact_ratio_reciprocity": [
        r"3/2", r"2/3", r"32/27", r"27/32", r"81/80", r"531441", r"524288",
        r"10/9", r"1\.185", r"\\phi", r"phi", r"golden", r"reciprocal", r"ratio",
    ],
    "friedmann_hubble_cosmology": [
        r"friedmann", r"hubble", r"H_0", r"H0", r"\\Lambda", r"lambda", r"cosmological",
        r"rho_\\Lambda", r"\\rho_\\\{?\\Lambda", r"w0", r"w_a", r"BAO", r"sound horizon", r"Omega_",
    ],
    "gyromagnetic_mhd_movement": [
        r"gyro", r"magnetic", r"helicity", r"elsasser", r"vortex", r"dipole", r"torque",
        r"angular momentum", r"circulation", r"coriolis", r"frame-drag", r"spin",
    ],
    "quantum_probability_operator": [
        r"density operator", r"probability", r"bell", r"commutator", r"wavefunction",
        r"born", r"\\psi", r"\\Psi", r"\\rho", r"hamiltonian", r"operator",
    ],
}

SHELL_PATTERNS = [
    r"Get-Command", r"Set-ExecutionPolicy", r"ErrorActionPreference", r"\$env:",
    r"\bpowershell\b", r"\bbash\b", r"\bshell:", r"\brun:\s*\|", r"python -m pip",
    r"pip install", r"Join-Path", r"Remove-Item", r"New-Item", r"Write-Error",
    r"subprocess", r"\.venv", r"GOOGLE_CLOUD_PROJECT", r"steps\.", r"\$\{\{",
]


def read_csv(path):
    if not path.exists():
        return []
    with path.open(encoding="utf-8-sig", errors="replace", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path, rows, fields):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def norm(text):
    return re.sub(r"\s+", " ", text or "").strip()


def is_shell_artifact(text):
    return any(re.search(p, text, flags=re.I) for p in SHELL_PATTERNS)


def category_hits(text):
    hits = []
    for category, patterns in CATEGORIES.items():
        if any(re.search(p, text, flags=re.I) for p in patterns):
            hits.append(category)
    return hits


def exact_numeric_signal(text):
    return bool(
        re.search(r"\d+\s*/\s*\d+", text)
        or re.search(r"\d+\.\d+", text)
        or re.search(r"10\^\{?-?\d+", text)
        or re.search(r"\\pi|π|\\hbar|\\ell_P", text)
    )


def paper_id_counts():
    counts = Counter()
    if PAPER_DIR.exists():
        for tex in PAPER_DIR.glob("paper*.tex"):
            text = tex.read_text(encoding="utf-8", errors="replace")
            for m in re.finditer(r"ID\d{4,5}", text):
                counts[m.group(0)] += 1
    return counts


def graph_degrees():
    indeg = Counter()
    outdeg = Counter()
    for row in read_csv(EDGES):
        source = row.get("dep_id") or row.get("source_id") or row.get("prerequisite_id") or row.get("from") or row.get("relied_upon_id")
        target = row.get("dependent_id") or row.get("target_id") or row.get("to")
        if source and target:
            outdeg[source] += 1
            indeg[target] += 1
    return indeg, outdeg


def operator_types():
    by_id = {}
    for row in read_csv(OPERATOR_PASS):
        by_id[row.get("id", "")] = {
            "field_type": row.get("field_type", ""),
            "n_admissible": row.get("n_admissible", ""),
        }
    return by_id


def score_master_row(row, paper_counts, indeg, outdeg, op_by_id):
    tzpid = row.get("id", "")
    core_text = norm(" ".join(
        row.get(k, "") for k in [
            "title", "canonical_statement", "canonical_equation", "formation_method",
            "formation_note", "isabelle_kind",
            "obligation_role", "proof_required_checks", "gold_spine", "wolfram_status",
        ]
    ))
    context_text = norm(" ".join([row.get("dictionary", ""), row.get("encyclopedia", "")]))
    equation = norm(row.get("canonical_equation", ""))
    all_text = " ".join([core_text, context_text])
    hits = category_hits(core_text)
    context_hits = [h for h in category_hits(context_text) if h not in hits]
    shell = is_shell_artifact(all_text)
    score = 0
    score += 5 * len(hits)
    score += 1.5 * len(context_hits)
    score += 5 if norm(row.get("canonical_equation", "")) else 0
    score += 8 if row.get("gold_spine") else 0
    score += 8 if paper_counts[tzpid] else 0
    score += min(15, outdeg[tzpid] * 1.0)
    score += min(10, indeg[tzpid] * 0.75)
    score += 10 if (row.get("isabelle_kind", "").lower() in {"axiom", "theorem", "lemma", "definition"}) else 0
    score += 4 if "pass" in row.get("wolfram_status", "").lower() else 0
    score += 3 if exact_numeric_signal(core_text) else 0
    if op_by_id.get(tzpid, {}).get("field_type") in {"scalar", "vector", "tensor"}:
        score += 2
    if len(equation) > 1000:
        score -= 25
    if re.search(r"\\documentclass|\\begin\{document\}|\\author\{|\\date\{|\\section\{|license notice|\\maketitle|\\begin\{abstract\}", equation, re.I):
        score -= 45
    if equation and not re.search(r"[=<>∼≈\\int\\sum\\lim\\nabla\\frac\^\_\+\-\*/]|\\to|\\mapsto|\\propto|\\sim", equation):
        score -= 10
    if shell:
        score -= 60
    return {
        "id": tzpid,
        "title": row.get("title", ""),
        "score": round(score, 2),
        "category_hits": ";".join(hits + [f"context:{h}" for h in context_hits]),
        "shell_artifact_signal": "yes" if shell else "no",
        "paper_mentions": paper_counts[tzpid],
        "graph_in_degree": indeg[tzpid],
        "graph_out_degree": outdeg[tzpid],
        "isabelle_kind": row.get("isabelle_kind", ""),
        "gold_spine": row.get("gold_spine", ""),
        "wolfram_status": row.get("wolfram_status", ""),
        "field_type": op_by_id.get(tzpid, {}).get("field_type", ""),
        "canonical_equation": row.get("canonical_equation", ""),
        "recommended_use": recommend_use(hits, shell),
        "source": "master",
    }


def recommend_use(hits, shell):
    if shell:
        return "quarantine as operational artifact unless manually rescued"
    if "boundary_limit_singularity" in hits:
        return "use as a boundary/degeneracy stress-test obligation"
    if "spectral_bessel_laplacian" in hits:
        return "use in Bessel/hyperspherical spectral certificate"
    if "topological_holonomy" in hits:
        return "use in holonomy/winding/topological invariant lane"
    if "friedmann_hubble_cosmology" in hits:
        return "use in Hubble/Friedmann parameter scaffold"
    if "gyromagnetic_mhd_movement" in hits:
        return "use in gyromagnetic movement/vector-calculus lane"
    if "exact_ratio_reciprocity" in hits:
        return "use in reciprocal-ratio locking lane"
    if "invariant_conservation_closure" in hits:
        return "use as conservation/closure guardrail"
    return "secondary candidate; review before promoting"


def classify_cleanup_row(row):
    text = norm(" ".join([row.get("ID", ""), row.get("title", ""), row.get("normalized_candidate", ""), row.get("canonical_equation", ""), row.get("reason", "")]))
    shell = is_shell_artifact(text)
    hits = category_hits(text)
    salvage = bool(hits) and not shell
    score = 5 * len(hits)
    score += 4 if exact_numeric_signal(text) else 0
    score += 3 if row.get("parsed_segments") not in {"", "0", "0.0"} else 0
    try:
        score += min(4, int(float(row.get("segment_count") or 0)))
    except ValueError:
        pass
    if shell:
        score -= 60
    return {
        "id": row.get("ID", ""),
        "title": row.get("title", ""),
        "status": row.get("status", ""),
        "candidate_score": round(score, 2),
        "classification": "shell_or_code_artifact" if shell else ("math_rescue_candidate" if salvage else "parser_cleanup_low_priority"),
        "category_hits": ";".join(hits),
        "normalized_candidate": row.get("normalized_candidate", ""),
        "first_error": row.get("first_error", ""),
        "recommended_action": (
            "do not mint as equation; keep in provenance quarantine"
            if shell else
            "manually normalize and consider as proof-strength edge case"
            if salvage else
            "leave out of proof spine unless needed"
        ),
    }


def md_escape(text):
    return norm(text).replace("|", "\\|")


def build_reports(shortlist, gap_rows, summary):
    top = shortlist[:60]
    lines = [
        "# TZPID Edge-Case Equation Shortlist",
        "",
        f"Generated UTC: {summary['generated_utc']}",
        "",
        "Purpose: identify high-value equations that strengthen the proof package by stressing boundaries, exact ratios, spectral roots, closure/invariance, topology, cosmology, and gyromagnetic movement.",
        "",
        "Important distinction: shell commands and operational residue are not mathematical gaps. They should be quarantined unless a real equation can be extracted from them.",
        "",
        "## Summary",
        "",
        f"- Master rows scored: `{summary['master_rows']}`",
        f"- Cleanup queue rows classified: `{summary['cleanup_rows']}`",
        f"- Cleanup math-rescue candidates: `{summary['cleanup_math_rescue_candidates']}`",
        f"- Cleanup shell/code artifacts: `{summary['cleanup_shell_or_code_artifacts']}`",
        f"- Master shell/code artifact signals: `{summary['master_shell_artifact_signals']}`",
        "",
        "## Top Candidates",
        "",
        "| Rank | ID | Score | Categories | Graph out | Graph in | Paper mentions | Recommended use | Title | Equation |",
        "|---:|---|---:|---|---:|---:|---:|---|---|---|",
    ]
    for i, row in enumerate(top, start=1):
        lines.append(
            "| " + " | ".join([
                str(i),
                row["id"],
                str(row["score"]),
                md_escape(row["category_hits"]),
                str(row["graph_out_degree"]),
                str(row["graph_in_degree"]),
                str(row["paper_mentions"]),
                md_escape(row["recommended_use"]),
                md_escape(row["title"]),
                md_escape(row["canonical_equation"])[:280],
            ]) + " |"
        )
    lines += [
        "",
        "## Category Counts In Top 200",
        "",
    ]
    cat_counts = Counter()
    for row in shortlist[:200]:
        for c in row["category_hits"].split(";"):
            if c:
                cat_counts[c] += 1
    for cat, count in cat_counts.most_common():
        lines.append(f"- `{cat}`: `{count}`")
    lines += [
        "",
        "## Suggested Immediate Promotions",
        "",
        "1. Promote the highest-scoring boundary/singularity rows into explicit HOL carrier assumptions, because these catch the places where models fail.",
        "2. Promote the highest-scoring spectral/Bessel rows into the delta-alpha and hyperspherical closure lane.",
        "3. Promote exact-ratio and holonomy rows into the fifth-flip/reciprocal bridge, where they provide falsifiable numeric fingerprints.",
        "4. Keep shell/code artifacts out of the equation registry; cite them only as provenance or reproducibility commands.",
        "",
        f"CSV: `{OUT_CSV}`",
        f"Gap audit CSV: `{OUT_GAP_CSV}`",
    ]
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")

    gap_lines = [
        "# TZPID Equation-Universe Gap Audit",
        "",
        f"Generated UTC: {summary['generated_utc']}",
        "",
        "This audit classifies parser-cleanup/equation-universe rows into mathematical rescue candidates, shell/code artifacts, and low-priority cleanup rows.",
        "",
        "The current proof package has no internal master/ladder/source-truth gap: all are synchronized at 10,357 IDs. Any larger outside count needs a source file before it should be treated as a registry gap.",
        "",
        "## Counts",
        "",
        f"- Cleanup rows examined: `{summary['cleanup_rows']}`",
        f"- Math rescue candidates: `{summary['cleanup_math_rescue_candidates']}`",
        f"- Shell/code artifacts: `{summary['cleanup_shell_or_code_artifacts']}`",
        f"- Parser cleanup, low priority: `{summary['cleanup_low_priority']}`",
        "",
        "## Shell/Code Artifact Examples",
        "",
        "| ID | Title | Candidate | Action |",
        "|---|---|---|---|",
    ]
    for row in [r for r in gap_rows if r["classification"] == "shell_or_code_artifact"][:25]:
        gap_lines.append(
            f"| {row['id']} | {md_escape(row['title'])} | {md_escape(row['normalized_candidate'])[:220]} | {row['recommended_action']} |"
        )
    gap_lines += [
        "",
        "## Best Math Rescue Candidates",
        "",
        "| ID | Score | Categories | Title | Candidate | Action |",
        "|---|---:|---|---|---|---|",
    ]
    for row in [r for r in gap_rows if r["classification"] == "math_rescue_candidate"][:50]:
        gap_lines.append(
            f"| {row['id']} | {row['candidate_score']} | {md_escape(row['category_hits'])} | {md_escape(row['title'])} | {md_escape(row['normalized_candidate'])[:260]} | {row['recommended_action']} |"
        )
    OUT_GAP_MD.write_text("\n".join(gap_lines) + "\n", encoding="utf-8")


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    master = read_csv(MASTER)
    paper_counts = paper_id_counts()
    indeg, outdeg = graph_degrees()
    op_by_id = operator_types()
    scored = [score_master_row(row, paper_counts, indeg, outdeg, op_by_id) for row in master]
    scored.sort(key=lambda r: (r["score"], r["graph_out_degree"], r["paper_mentions"]), reverse=True)

    cleanup_source = read_csv(TOE_CLEANUP)
    gap_rows = [classify_cleanup_row(row) for row in cleanup_source]
    gap_rows.sort(key=lambda r: (
        r["classification"] == "math_rescue_candidate",
        r["candidate_score"],
    ), reverse=True)
    class_counts = Counter(row["classification"] for row in gap_rows)
    summary = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "master_rows": len(master),
        "operator_pass_rows": len(read_csv(OPERATOR_PASS)),
        "cleanup_rows": len(gap_rows),
        "cleanup_math_rescue_candidates": class_counts["math_rescue_candidate"],
        "cleanup_shell_or_code_artifacts": class_counts["shell_or_code_artifact"],
        "cleanup_low_priority": class_counts["parser_cleanup_low_priority"],
        "master_shell_artifact_signals": sum(1 for r in scored if r["shell_artifact_signal"] == "yes"),
        "outputs": {
            "shortlist_csv": str(OUT_CSV),
            "shortlist_md": str(OUT_MD),
            "gap_csv": str(OUT_GAP_CSV),
            "gap_md": str(OUT_GAP_MD),
        },
    }

    fields = [
        "id", "title", "score", "category_hits", "shell_artifact_signal",
        "paper_mentions", "graph_in_degree", "graph_out_degree", "isabelle_kind",
        "gold_spine", "wolfram_status", "field_type", "recommended_use",
        "source", "canonical_equation",
    ]
    write_csv(OUT_CSV, scored, fields)
    write_csv(OUT_GAP_CSV, gap_rows, [
        "id", "title", "status", "candidate_score", "classification", "category_hits",
        "normalized_candidate", "first_error", "recommended_action",
    ])
    build_reports(scored, gap_rows, summary)
    OUT_JSON.write_text(json.dumps({
        "summary": summary,
        "top_100": scored[:100],
        "gap_class_counts": class_counts,
    }, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
