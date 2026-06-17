from __future__ import annotations

import csv
import hashlib
import re
from collections import Counter
from datetime import datetime
from pathlib import Path


ROOT = Path(r"D:\TZPIDProof")
MASTER = ROOT / "TZPID_ALL_IDS_CANONICAL_EQUATION_MASTER_with_export.csv"
OUT_DIR = ROOT / "peer_review" / "unification_intake"
OUT_CSV = OUT_DIR / "PRIORITY_EQUATION_PROMOTION_QUEUE.csv"
OUT_MD = OUT_DIR / "PRIORITY_EQUATION_PROMOTION_QUEUE.md"
OUT_REVIEW_MD = OUT_DIR / "PRIORITY_MINTING_REVIEW.md"


PRIORITY_SOURCES = [
    {
        "source_group": "Trawin-Enlil Protocol",
        "isabelle_carrier": "Trawin_Enlil_Protocol_Source",
        "paths": [
            r"D:\TZPIDProof\peer_review\tex\companion24_trawin_enlil_protocol.tex",
            r"D:\Tex\trawin_enlil_protocol.tex",
        ],
    },
    {
        "source_group": "Topological Unification of QM and GR",
        "isabelle_carrier": "Topological_Unification_QM_GR_Source",
        "paths": [
            r"D:\TZPIDProof\peer_review\tex\companion27_topological_unification.tex",
            r"D:\TZPIDProof\peer_review\tex\paper8_topological_unification.tex",
            r"D:\Tex\topological_unification.tex",
        ],
    },
]


BLOCK_RE = re.compile(
    r"(?P<display>\\\[(?P<display_body>.*?)\\\])|"
    r"(?P<env>\\begin\{(?P<env_name>equation|align|aligned|gather|multline|eqnarray)\*?\}(?P<env_body>.*?)\\end\{(?P=env_name)\*?\})|"
    r"(?P<inline>(?<!\\)\$(?!\$)(?P<inline_body>.{3,220}?)(?<!\\)\$)",
    re.DOTALL,
)
THEOREM_ENV_RE = re.compile(
    r"\\begin\{(?P<kind>theorem|lemma|proposition|corollary|definition|remark)\*?\}(?P<body>.*?)\\end\{(?P=kind)\*?\}",
    re.DOTALL | re.IGNORECASE,
)
SECTION_RE = re.compile(r"\\(?:section|subsection|subsubsection)\*?\{(?P<title>.*?)\}", re.DOTALL)
ID_RE = re.compile(r"\bID(?P<num>\d{1,6})\b", re.IGNORECASE)
SPACE_RE = re.compile(r"\s+")
TEX_COMMAND_RE = re.compile(r"\\(?:text|mathrm|mathbf|mathcal|operatorname)\{([^{}]*)\}")


def normalize_id(raw: str) -> str:
    return f"ID{int(raw):04d}"


def load_master() -> dict[str, dict[str, str]]:
    with MASTER.open("r", encoding="utf-8-sig", newline="") as f:
        return {row["id"]: row for row in csv.DictReader(f)}


def line_number(text: str, pos: int) -> int:
    return text.count("\n", 0, pos) + 1


def one_line(text: str, limit: int = 900) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = SPACE_RE.sub(" ", text).strip()
    return text[:limit]


def soft_normalize_math(text: str) -> str:
    text = TEX_COMMAND_RE.sub(r"\1", text)
    text = re.sub(r"\\[a-zA-Z]+", "", text)
    text = re.sub(r"[^A-Za-z0-9=+\-*/^_().,<>|]+", "", text)
    return text.lower()


def current_section(text: str, pos: int) -> str:
    last = ""
    for match in SECTION_RE.finditer(text, 0, pos):
        last = one_line(match.group("title"), 160)
    return last


def surrounding_ids(text: str, start: int, end: int, radius: int = 1500) -> list[str]:
    window = text[max(0, start - radius): min(len(text), end + radius)]
    return sorted({normalize_id(m.group("num")) for m in ID_RE.finditer(window)})


def classify_candidate(body: str, nearby_ids: list[str], exact_ids: list[str]) -> str:
    normalized = soft_normalize_math(body)
    if exact_ids:
        return "existing_master_equation_exact_or_near_match"
    if nearby_ids:
        return "id_backed_equation_context_review"
    if any(token in normalized for token in ["eta", "functor", "quantum", "gravity", "rho", "lambda", "phi", "sigma"]):
        return "new_or_unmapped_spine_candidate"
    return "supporting_math_review"


def infer_math_role(body: str) -> str:
    low = body.lower()
    if "\\sum" in body or "sum_" in low:
        return "series_or_spectral_expansion"
    if "\\int" in body or "oint" in low:
        return "integral_or_action"
    if "\\to" in body or "rightarrow" in low or "\\mapsto" in body:
        return "map_or_limit_relation"
    if "\\frac" in body or "/" in body:
        return "ratio_or_fractional_relation"
    if "=" in body:
        return "definition_or_identity"
    if "\\le" in body or "\\ge" in body or "<" in body or ">" in body:
        return "bound_or_threshold"
    return "symbolic_expression"


def master_exact_matches(master: dict[str, dict[str, str]], body: str) -> list[str]:
    norm_body = soft_normalize_math(body)
    if len(norm_body) < 8:
        return []
    hits: list[str] = []
    for mid, row in master.items():
        eq = row.get("canonical_equation", "")
        stmt = row.get("canonical_statement", "")
        for candidate in [eq, stmt]:
            norm_candidate = soft_normalize_math(candidate)
            if len(norm_candidate) >= 8 and (norm_body in norm_candidate or norm_candidate in norm_body):
                hits.append(mid)
                break
    return sorted(set(hits))[:12]


def keyword_master_suggestions(master: dict[str, dict[str, str]], body: str) -> list[str]:
    low = body.lower()
    keyword_groups = [
        ["elsasser", "lambda", "magnetic"],
        ["avalanche", "tau", "3}{2", "3/2", "critical exponent"],
        ["flux", "phi_0", "h}{2e", "closed surface"],
        ["bessel", "gamma", "k_n", "vacuum"],
        ["information manifold", "153600", "tangent bundle"],
        ["dipole", "mu_0", "toroidal"],
        ["topos", "functor", "natural transformation", "quantum", "gravity"],
        ["fisher", "quantum", "topological"],
        ["hubble", "rho_lambda", "lambda", "dark energy"],
    ]
    active = [group for group in keyword_groups if any(k in low for k in group)]
    if not active:
        return []
    scored: list[tuple[int, str]] = []
    for mid, row in master.items():
        hay = " ".join([
            row.get("id", ""),
            row.get("title", ""),
            row.get("canonical_equation", ""),
            row.get("canonical_statement", ""),
            row.get("dictionary", ""),
            row.get("encyclopedia", ""),
            row.get("gold_spine", ""),
        ]).lower()
        score = 0
        for group in active:
            score += sum(1 for keyword in group if keyword in hay)
        if score:
            scored.append((score, mid))
    scored.sort(key=lambda item: (-item[0], item[1]))
    return [mid for _, mid in scored[:10]]


def iter_math_blocks(text: str):
    for match in BLOCK_RE.finditer(text):
        body = match.group("display_body") or match.group("env_body") or match.group("inline_body") or ""
        if not body.strip():
            continue
        if match.group("display"):
            kind = "display_math"
        elif match.group("env"):
            kind = f"{match.group('env_name')}_environment"
        else:
            kind = "inline_math"
            if not any(sym in body for sym in ["=", "\\", "^", "_", "\\frac", "\\int", "\\sum", "\\to"]):
                continue
        yield kind, body, match.start(), match.end()


def iter_theorem_blocks(text: str):
    for match in THEOREM_ENV_RE.finditer(text):
        yield match.group("kind").lower(), match.group("body"), match.start(), match.end()


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    master = load_master()
    rows: list[dict[str, str]] = []

    for source in PRIORITY_SOURCES:
        for path_s in source["paths"]:
            path = Path(path_s)
            if not path.exists():
                continue
            text = path.read_text(encoding="utf-8", errors="replace")

            for idx, (kind, body, start, end) in enumerate(iter_math_blocks(text), start=1):
                nearby = surrounding_ids(text, start, end)
                exact = master_exact_matches(master, body)
                matched_ids = sorted(set(nearby + exact))
                titles = [master[i].get("title", "") for i in matched_ids if i in master]
                rows.append(
                    {
                        "source_group": source["source_group"],
                        "isabelle_carrier": source["isabelle_carrier"],
                        "source_path": str(path),
                        "candidate_kind": kind,
                        "candidate_index": str(idx),
                        "line": str(line_number(text, start)),
                        "section": current_section(text, start),
                        "candidate_hash": hashlib.sha256(body.encode("utf-8", errors="ignore")).hexdigest()[:16],
                        "math_role": infer_math_role(body),
                        "candidate_text": one_line(body, 1600),
                        "nearby_ids": "; ".join(nearby),
                        "exact_or_near_master_ids": "; ".join(exact),
                        "matched_master_ids": "; ".join(matched_ids),
                        "matched_master_titles": " | ".join(titles)[:1000],
                        "keyword_suggested_ids": "; ".join(keyword_master_suggestions(master, body)),
                        "promotion_status": classify_candidate(body, nearby, exact),
                    }
                )

            for idx, (kind, body, start, end) in enumerate(iter_theorem_blocks(text), start=1):
                nearby = surrounding_ids(text, start, end)
                rows.append(
                    {
                        "source_group": source["source_group"],
                        "isabelle_carrier": source["isabelle_carrier"],
                        "source_path": str(path),
                        "candidate_kind": f"{kind}_environment",
                        "candidate_index": str(idx),
                        "line": str(line_number(text, start)),
                        "section": current_section(text, start),
                        "candidate_hash": hashlib.sha256(body.encode("utf-8", errors="ignore")).hexdigest()[:16],
                        "math_role": "theorem_statement_or_definition_block",
                        "candidate_text": one_line(body, 1800),
                        "nearby_ids": "; ".join(nearby),
                        "exact_or_near_master_ids": "",
                        "matched_master_ids": "; ".join(nearby),
                        "matched_master_titles": " | ".join(master[i].get("title", "") for i in nearby if i in master)[:1000],
                        "keyword_suggested_ids": "; ".join(keyword_master_suggestions(master, body)),
                        "promotion_status": "theorem_semantic_translation_review" if nearby else "new_theorem_or_definition_candidate",
                    }
                )

    fields = [
        "source_group",
        "isabelle_carrier",
        "source_path",
        "candidate_kind",
        "candidate_index",
        "line",
        "section",
        "candidate_hash",
        "math_role",
        "candidate_text",
        "nearby_ids",
        "exact_or_near_master_ids",
        "matched_master_ids",
        "matched_master_titles",
        "keyword_suggested_ids",
        "promotion_status",
    ]
    with OUT_CSV.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    counts_by_source = Counter(row["source_group"] for row in rows)
    counts_by_status = Counter(row["promotion_status"] for row in rows)
    counts_by_kind = Counter(row["candidate_kind"] for row in rows)
    id_backed = sum(1 for row in rows if row["matched_master_ids"])
    unmapped = len(rows) - id_backed
    generated = datetime.now().isoformat(timespec="seconds")

    priority_rows = [
        row for row in rows
        if row["promotion_status"] in {
            "new_or_unmapped_spine_candidate",
            "new_theorem_or_definition_candidate",
            "id_backed_equation_context_review",
            "theorem_semantic_translation_review",
        }
    ]

    lines = [
        "# Priority Equation Promotion Queue",
        "",
        f"Generated: {generated}",
        "",
        "## Scope",
        "",
        "This queue extracts equation-like and theorem-like blocks from the two first-pass unification sources: `Topological Unification of QM and GR` and `Trawin-Enlil Protocol`.  It maps each candidate to nearby or exact master IDs where possible and labels unmapped material for review before any new IDs are minted.",
        "",
        f"- Candidate blocks extracted: {len(rows)}",
        f"- ID-backed or master-matched candidates: {id_backed}",
        f"- Unmapped candidates needing review: {unmapped}",
        f"- Machine-readable queue: `{OUT_CSV}`",
        "",
        "## Counts By Source",
        "",
    ]
    for source, count in sorted(counts_by_source.items()):
        lines.append(f"- {source}: {count}")
    lines.extend(["", "## Counts By Promotion Status", ""])
    for status, count in sorted(counts_by_status.items()):
        lines.append(f"- {status}: {count}")
    lines.extend(["", "## Counts By Candidate Kind", ""])
    for kind, count in sorted(counts_by_kind.items()):
        lines.append(f"- {kind}: {count}")

    lines.extend(
        [
            "",
            "## First Review Slice",
            "",
            "| Source | Kind | Line | Role | Matched IDs | Status | Candidate |",
            "| --- | --- | ---: | --- | --- | --- | --- |",
        ]
    )
    for row in priority_rows[:40]:
        candidate = row["candidate_text"].replace("|", "\\|")
        if len(candidate) > 180:
            candidate = candidate[:177] + "..."
        lines.append(
            f"| {row['source_group']} | {row['candidate_kind']} | {row['line']} | "
            f"{row['math_role']} | {row['matched_master_ids'] or '-'} | "
            f"{row['promotion_status']} | `{candidate}` |"
        )

    lines.extend(
        [
            "",
            "## Operating Rule",
            "",
            "Use this queue as a review layer, not as automatic registry mutation.  Existing IDs should be reused whenever the candidate is semantically equivalent.  New IDs should be minted only for clean formal statements that are absent from the master and useful for a paper-facing spine.",
        ]
    )
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")

    mint_review_rows = [
        row for row in rows
        if row["promotion_status"] in {
            "new_or_unmapped_spine_candidate",
            "new_theorem_or_definition_candidate",
        }
    ]
    review_lines = [
        "# Priority Minting Review",
        "",
        f"Generated: {generated}",
        "",
        "## Decision Rule",
        "",
        "Do not mint from this page automatically.  Each row is a clean review target: first compare it to `keyword_suggested_ids`; if no existing ID is semantically equivalent, then mint a new ID with dictionary, encyclopedia, Wolfram form, and source-truth JSON.",
        "",
        f"- Unmapped mint-review candidates: {len(mint_review_rows)}",
        "- Trawin-Enlil currently contributes no unmapped mint-review candidates in this pass; it is mainly an existing-ID refinement source.",
        "- Topological Unification contributes the new theorem/definition candidates that need human promotion judgment.",
        "",
        "## Candidate Table",
        "",
        "| Source | Kind | Line | Role | Suggested existing IDs | Candidate |",
        "| --- | --- | ---: | --- | --- | --- |",
    ]
    for row in mint_review_rows:
        candidate = row["candidate_text"].replace("|", "\\|")
        if len(candidate) > 500:
            candidate = candidate[:497] + "..."
        suggestions = row["keyword_suggested_ids"] or "-"
        review_lines.append(
            f"| {row['source_group']} | {row['candidate_kind']} | {row['line']} | "
            f"{row['math_role']} | {suggestions} | `{candidate}` |"
        )
    review_lines.extend(
        [
            "",
            "## First Recommended Promotions",
            "",
            "1. Review the `TZP Vacuum Divergence` theorem against existing vacuum/Bessel IDs before minting.",
            "2. Review the `Elsasser Universality` theorem against the gyromagnetic and magnetic-torsion carriers.",
            "3. Review the `Universal Critical Exponent` duplicates against existing avalanche IDs before minting; this may be a reuse, not a new ID.",
            "4. Review `Topological Locking` and flux quantization against existing quantum/magnetic flux IDs.",
            "5. Treat large categorical definitions as HOL carrier structure first; mint only the smallest formal equations needed for the spine.",
        ]
    )
    OUT_REVIEW_MD.write_text("\n".join(review_lines) + "\n", encoding="utf-8")

    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_MD}")
    print(f"Wrote {OUT_REVIEW_MD}")
    print(f"Candidate blocks: {len(rows)}")
    print(f"ID-backed/master-matched: {id_backed}")
    print(f"Unmapped: {unmapped}")


if __name__ == "__main__":
    main()
