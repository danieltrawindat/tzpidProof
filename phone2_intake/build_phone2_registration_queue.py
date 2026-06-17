import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(r"D:\TZPIDProof")
INTAKE = ROOT / "phone2_intake"
MASTER = Path(r"D:\00_Engine\AI_Workspaces\OpenAI2\TZPID_ALL_IDS_CANONICAL_EQUATION_MASTER_with_export.csv")

EQUATIONS = INTAKE / "PHONE2_EQUATION_CANDIDATES.csv"
SEMANTICS = INTAKE / "PHONE2_SEMANTIC_CANDIDATES.csv"
WOLFRAM_PARSE = INTAKE / "PHONE2_WOLFRAM_PARSE_RESULTS.json"

QUEUE = INTAKE / "PHONE2_ID_READY_EQUATION_QUEUE.csv"
BATCHES = INTAKE / "PHONE2_REGISTRATION_BATCHES.csv"
PLAN = INTAKE / "PHONE2_REGISTRATION_PLAN.md"
SUMMARY = INTAKE / "PHONE2_REGISTRATION_QUEUE_SUMMARY.json"


MATH_SIGNAL = re.compile(
    r"(\\frac|\\int|\\sum|\\prod|\\nabla|\\partial|\\lim|\\sqrt|\\sin|\\cos|"
    r"\\theta|\\phi|\\mu|\\omega|\\alpha|\\beta|\\gamma|\\delta|\\lambda|"
    r"[=≈∝≤≥<>+\-*/^]|->|=>|:=|∀|∃|⊗|⊕|∘|∇|∂|∫|Σ|Π|√)"
)


def normalize(text: str) -> str:
    text = text or ""
    text = text.replace("\ufeff", "")
    text = re.sub(r":contentReference\[[^\]]+\]\{[^}]+\}", "", text)
    text = re.sub(r"\s+", " ", text.strip())
    return text


def key(text: str) -> str:
    text = normalize(text).lower()
    text = re.sub(r"[\s`$\\{}\[\](),.;:|]+", "", text)
    return text


def classify_domain(text: str, source_file: str) -> str:
    blob = f"{source_file} {text}".lower()
    rules = [
        ("category_type_theory", r"kleisli|monad|functor|topos|category|natural transformation|morphism|presheaf"),
        ("quantum_entanglement", r"quantum|entangle|bell|hilbert|qubit|density|tensor|operator|eigen"),
        ("field_topology_mhd", r"magnetic|helicity|vector potential|alfv|mhd|vortex|dipole|curl|nabla|∇|torsion"),
        ("optimization_computation", r"optimizer|fisher|gradient|loss|neural|module|algorithm|complexity"),
        ("geometry_topology", r"topolog|manifold|homology|cohomology|singular|fiber|bundle|sphere|curvature"),
        ("protocol_systems", r"protocol|byob|ifp|validation|schema|workflow"),
        ("gravity_cosmology", r"gravity|gravit|einstein|metric|friedmann|hubble|cosmolog|spacetime"),
        ("signal_wave", r"wave|frequency|phase|omega|resonance|fourier|spectral|bessel"),
    ]
    for name, pattern in rules:
        if re.search(pattern, blob):
            return name
    return "general_math"


def classify_readiness(text: str, source_type: str, score: int) -> tuple[str, str]:
    stripped = normalize(text)
    if not stripped:
        return "quarantine", "empty candidate"
    if stripped.startswith("(*") and stripped.endswith("*)"):
        return "quarantine", "wolfram/comment divider"
    if stripped.startswith("#") and not MATH_SIGNAL.search(stripped):
        return "review", "heading without standalone equation"
    if len(stripped) > 900:
        return "review", "large mixed prose/equation block"
    if "contentReference" in text or "oaicite" in text:
        return "review", "citation artifact present"
    if not MATH_SIGNAL.search(stripped):
        return "review", "weak equation signal"
    if score >= 8 and len(stripped) <= 500:
        return "id_ready", "compact mathematical candidate"
    return "review", "needs human equation boundary check"


def wolfram_hint(text: str) -> str:
    t = normalize(text)
    replacements = [
        (r"\\frac\{([^{}]+)\}\{([^{}]+)\}", r"(\1)/(\2)"),
        (r"\\sqrt\{([^{}]+)\}", r"Sqrt[\1]"),
        (r"\\sin", "Sin"),
        (r"\\cos", "Cos"),
        (r"\\tan", "Tan"),
        (r"\\exp", "Exp"),
        (r"\\log", "Log"),
        (r"\\pi|π", "Pi"),
        (r"\\theta|θ", "theta"),
        (r"\\phi|φ", "phi"),
        (r"\\omega|ω", "omega"),
        (r"\\alpha|α", "alpha"),
        (r"\\beta|β", "beta"),
        (r"\\gamma|γ", "gamma"),
        (r"\\delta|δ", "delta"),
        (r"\\lambda|λ", "lambda"),
        (r"\\mu|μ", "mu"),
        ("^", "^"),
        ("≈", "=="),
        ("∝", "Proportional"),
        ("≤", "<="),
        ("≥", ">="),
    ]
    for old, new in replacements:
        t = re.sub(old, new, t)
    t = t.replace("\\", "")
    return t[:500]


def nearest_context(rows, source_file: str, line: int) -> dict:
    candidates = [r for r in rows.get(source_file, []) if r["line_number"] <= line]
    if not candidates:
        candidates = rows.get(source_file, [])[:1]
    if not candidates:
        return {"semantic_kind": "", "semantic_context": ""}
    best = max(candidates, key=lambda r: r["line_number"])
    return {"semantic_kind": best["semantic_kind"], "semantic_context": best["candidate"][:300]}


def main() -> None:
    master_keys = set()
    max_id = -1
    master_rows = 0
    with MASTER.open(encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            master_rows += 1
            for col in ("canonical_equation", "canonical_statement", "title"):
                if row.get(col):
                    master_keys.add(key(row[col]))
            m = re.search(r"ID(\d+)", row.get("id", ""))
            if m:
                max_id = max(max_id, int(m.group(1)))

    semantic_by_file = defaultdict(list)
    with SEMANTICS.open(encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            try:
                line = int(row.get("line_number") or 0)
            except ValueError:
                line = 0
            semantic_by_file[row.get("source_file", "")].append(
                {
                    "line_number": line,
                    "semantic_kind": row.get("semantic_kind", ""),
                    "candidate": normalize(row.get("candidate", "")),
                }
            )
    for items in semantic_by_file.values():
        items.sort(key=lambda r: r["line_number"])

    parse_clean_by_file = Counter()
    if WOLFRAM_PARSE.exists():
        parse = json.loads(WOLFRAM_PARSE.read_text(encoding="utf-8"))
        for row in parse.get("results", []):
            if row.get("status") == "parse_ok":
                parse_clean_by_file[row.get("source_file", "")] += 1

    seen = set()
    queue = []
    duplicate_in_phone2 = 0
    with EQUATIONS.open(encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            candidate = normalize(row.get("candidate", ""))
            candidate_key = key(candidate)
            if not candidate_key:
                continue
            if candidate_key in seen:
                duplicate_in_phone2 += 1
                continue
            seen.add(candidate_key)
            try:
                line = int(row.get("line_number") or 0)
            except ValueError:
                line = 0
            try:
                score = int(float(row.get("score") or 0))
            except ValueError:
                score = 0
            readiness, reason = classify_readiness(candidate, row.get("source_type", ""), score)
            context = nearest_context(semantic_by_file, row.get("source_file", ""), line)
            domain = classify_domain(candidate, row.get("source_file", ""))
            duplicate_status = "possible_master_duplicate" if candidate_key in master_keys else "new_or_nonexact"
            wl_status = (
                "file_has_parse_clean_wolfram"
                if parse_clean_by_file[row.get("source_file", "")] > 0
                else "needs_wolfram_translation"
            )
            queue.append(
                {
                    "queue_index": len(queue) + 1,
                    "proposed_id": f"NEXT+{len(queue) + 1:04d}",
                    "source_file": row.get("source_file", ""),
                    "line_number": line,
                    "source_type": row.get("source_type", ""),
                    "score": score,
                    "readiness": readiness,
                    "readiness_reason": reason,
                    "domain_family": domain,
                    "semantic_kind": context["semantic_kind"],
                    "semantic_context": context["semantic_context"],
                    "duplicate_status": duplicate_status,
                    "wolfram_status": wl_status,
                    "candidate_equation": candidate,
                    "wolfram_form_hint": wolfram_hint(candidate),
                    "formation_method": "Phone2 corpus extraction",
                    "formation_inputs": row.get("source_file", ""),
                    "formation_note": f"Extracted from D:\\Phone2 line {line}; staged only, not minted.",
                    "source_tag": "PHONE2",
                }
            )

    with QUEUE.open("w", encoding="utf-8", newline="") as handle:
        fieldnames = list(queue[0].keys()) if queue else ["queue_index"]
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(queue)

    batch_rows = []
    sorted_queue = sorted(
        queue,
        key=lambda r: (
            r["readiness"] != "id_ready",
            r["duplicate_status"] != "new_or_nonexact",
            -int(r["score"]),
            r["source_file"],
            int(r["line_number"]),
        ),
    )
    for i, row in enumerate(sorted_queue, start=1):
        batch_rows.append(
            {
                "batch": (i - 1) // 250 + 1,
                "batch_position": (i - 1) % 250 + 1,
                "queue_index": row["queue_index"],
                "proposed_id": row["proposed_id"],
                "source_file": row["source_file"],
                "line_number": row["line_number"],
                "readiness": row["readiness"],
                "domain_family": row["domain_family"],
                "duplicate_status": row["duplicate_status"],
                "wolfram_status": row["wolfram_status"],
            }
        )
    with BATCHES.open("w", encoding="utf-8", newline="") as handle:
        fieldnames = list(batch_rows[0].keys()) if batch_rows else ["batch"]
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(batch_rows)

    counts = {
        "generated_utc": __import__("datetime").datetime.now(__import__("datetime").timezone.utc).isoformat(),
        "master_rows_seen": master_rows,
        "master_max_id_seen": f"ID{max_id:04d}" if max_id >= 0 else "",
        "raw_equation_candidates": sum(1 for _ in EQUATIONS.open(encoding="utf-8-sig")) - 1,
        "unique_staged_candidates": len(queue),
        "duplicate_inside_phone2_removed": duplicate_in_phone2,
        "readiness_counts": Counter(r["readiness"] for r in queue),
        "domain_counts": Counter(r["domain_family"] for r in queue),
        "duplicate_status_counts": Counter(r["duplicate_status"] for r in queue),
        "wolfram_status_counts": Counter(r["wolfram_status"] for r in queue),
    }
    serializable = json.loads(json.dumps(counts, default=dict))
    SUMMARY.write_text(json.dumps(serializable, indent=2), encoding="utf-8")

    lines = [
        "# Phone2 ID-Ready Registration Plan",
        "",
        "This plan stages the `D:\\Phone2` equation extraction for controlled registry promotion. It does not mint IDs and does not modify the master registry.",
        "",
        "## Current Anchor",
        "",
        f"- Master rows seen: `{master_rows}`",
        f"- Highest existing master ID seen: `{counts['master_max_id_seen']}`",
        f"- Raw Phone2 equation candidates: `{counts['raw_equation_candidates']}`",
        f"- Unique staged candidates: `{len(queue)}`",
        f"- Phone2 internal duplicates removed: `{duplicate_in_phone2}`",
        "",
        "## Readiness",
        "",
        "| Status | Count | Meaning |",
        "|---|---:|---|",
    ]
    meaning = {
        "id_ready": "Compact mathematical candidate with clear equation signal.",
        "review": "Likely usable, but needs boundary cleanup or citation/prose separation.",
        "quarantine": "Artifact/comment/weak candidate; do not mint without manual rescue.",
    }
    for status, count in Counter(r["readiness"] for r in queue).most_common():
        lines.append(f"| {status} | {count} | {meaning.get(status, '')} |")
    lines.extend(["", "## Domain Families", "", "| Domain | Count |", "|---|---:|"])
    for domain, count in Counter(r["domain_family"] for r in queue).most_common():
        lines.append(f"| {domain} | {count} |")
    lines.extend(
        [
            "",
            "## Promotion Rule",
            "",
            "1. Promote `id_ready` + `new_or_nonexact` rows first.",
            "2. Review long mixed prose/equation rows by splitting them into atomic equations before minting.",
            "3. Keep `quarantine` rows out of the registry unless a human intentionally rescues them.",
            "4. Attach semantic context from `semantic_kind` / `semantic_context` during dictionary and encyclopedia creation.",
            "5. Use `wolfram_form_hint` as a starting point only; parse-clean Wolfram status should be verified before marking a row computationally certified.",
            "",
            "## Generated Files",
            "",
            f"- `{QUEUE.name}`",
            f"- `{BATCHES.name}`",
            f"- `{SUMMARY.name}`",
            "",
            "## Suggested Next Batch",
            "",
            "Start with batch 1 from `PHONE2_REGISTRATION_BATCHES.csv`; it sorts high-score, ID-ready, nonexact candidates first.",
        ]
    )
    PLAN.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(serializable, indent=2))


if __name__ == "__main__":
    main()
