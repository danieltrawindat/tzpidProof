import csv
import json
import re
import shutil
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


SOURCE = Path(r"D:\Phone2")
ROOT = Path(r"D:\TZPIDProof\phone2_intake\theorem_toe")
TEX_DIR = ROOT / "tex"
WOLFRAM_DIR = ROOT / "wolfram"

THEOREM_CSV = ROOT / "PHONE2_THEOREM_SEMANTIC_QUEUE.csv"
TOE_CSV = ROOT / "PHONE2_TOE_SOURCE_QUEUE.csv"
REPORT = ROOT / "PHONE2_THEOREM_TOE_INTAKE_REPORT.md"
SUMMARY = ROOT / "phone2_theorem_toe_summary.json"


LABEL_RE = re.compile(
    r"\b(theorem|lemma|corollary|definition|axiom|proposition|proof|validation|invariant)\b",
    re.IGNORECASE,
)
LATEX_ENV_RE = re.compile(
    r"\\begin\{(theorem|lemma|definition|corollary|proof|proposition|axiom)\}"
    r"(?:\[([^\]]+)\])?(.*?)\\end\{\1\}",
    re.IGNORECASE | re.DOTALL,
)
MD_HEADING_RE = re.compile(
    r"^(?P<heading>#{1,6}\s+.*?\b(?:Theorem|Lemma|Corollary|Definition|Axiom|Proposition|Proof|Invariant|Validation)\b.*?)$",
    re.IGNORECASE | re.MULTILINE,
)
WOLFRAM_NAMED_RE = re.compile(
    r"(?P<name>[A-Za-z][A-Za-z0-9]*?(?:Theorem|Lemma|Proof|Axiom|Invariant|Definition|Validation))\s*(?::=|=)\s*",
    re.IGNORECASE,
)
FENCE_RE = re.compile(r"```(?:wolfram|mathematica|wl)?\s*(.*?)```", re.IGNORECASE | re.DOTALL)


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def clean_text(text: str) -> str:
    replacements = {
        "âˆš": "√",
        "Ã—": "×",
        "â‰¤": "≤",
        "â‰¥": "≥",
        "â†’": "→",
        "â†’": "→",
        "âˆ‘": "∑",
        "â„‹": "ℋ",
        "Ï": "ρ",
        "Â": "",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text.replace("\r\n", "\n").replace("\r", "\n")


def strip_latex_fence(text: str) -> str:
    stripped = text.strip()
    if stripped.startswith("```latex"):
        stripped = re.sub(r"^```latex\s*", "", stripped)
        stripped = re.sub(r"\s*```\s*$", "", stripped)
    return stripped


def line_number(text: str, index: int) -> int:
    return text.count("\n", 0, index) + 1


def classify_kind(label: str) -> str:
    label = (label or "").lower()
    for kind in ["theorem", "lemma", "corollary", "definition", "axiom", "proposition", "proof", "validation", "invariant"]:
        if kind in label:
            return kind.title()
    return "SemanticBlock"


def domain_for(source_file: str, block: str) -> str:
    blob = f"{source_file} {block}".lower()
    rules = [
        ("toe_unification", r"theory of everything|unified field topology|unification|master unification"),
        ("category_type_theory", r"topos|category|functor|monad|morphism|hom|sheaf|univalence"),
        ("quantum_entanglement", r"quantum|entangle|hilbert|bell|qubit|density|operator"),
        ("gyromagnetic_gravity", r"elsasser|gyromagnetic|magnetic|parker|gravitational wave|helical|helicity"),
        ("information_consciousness", r"conscious|information manifold|integrated information|neural"),
        ("computation_protocol", r"protocol|ifp|cache|parser|complexity|algorithm|work-stealing|thread"),
        ("cosmology_topology", r"dark matter|vacuum|spacetime|s\\^3|black hole|tzp|manifold"),
    ]
    for name, pattern in rules:
        if re.search(pattern, blob):
            return name
    return "general_semantics"


def summarize(block: str, limit: int = 420) -> str:
    block = re.sub(r"\s+", " ", block.strip())
    return block[:limit].strip()


def capture_until_next_heading(text: str, start: int) -> str:
    next_match = re.search(r"\n#{1,6}\s+", text[start + 1 :])
    if next_match:
        end = start + 1 + next_match.start()
    else:
        end = min(len(text), start + 3000)
    return text[start:end].strip()


def extract_theorem_blocks(path: Path, text: str) -> list[dict]:
    rows = []
    seen = set()

    for match in LATEX_ENV_RE.finditer(text):
        env, title, body = match.group(1), match.group(2) or "", match.group(3)
        block = match.group(0).strip()
        key = ("latex", match.start(), env, title)
        seen.add(key)
        rows.append(
            {
                "source_file": path.name,
                "line_number": line_number(text, match.start()),
                "semantic_kind": classify_kind(env),
                "title": title or env.title(),
                "domain_family": domain_for(path.name, block),
                "extraction_method": "latex_environment",
                "block_summary": summarize(block),
                "full_block": block,
                "status": "theorem_semantic_staged",
            }
        )

    for match in MD_HEADING_RE.finditer(text):
        heading = match.group("heading").strip()
        block = capture_until_next_heading(text, match.start())
        key = ("md", match.start(), heading)
        if key in seen:
            continue
        rows.append(
            {
                "source_file": path.name,
                "line_number": line_number(text, match.start()),
                "semantic_kind": classify_kind(heading),
                "title": re.sub(r"^[#*\s]+|[*\s]+$", "", heading),
                "domain_family": domain_for(path.name, block),
                "extraction_method": "markdown_heading",
                "block_summary": summarize(block),
                "full_block": block,
                "status": "theorem_semantic_staged",
            }
        )

    for match in WOLFRAM_NAMED_RE.finditer(text):
        name = match.group("name")
        start = match.start()
        block = text[start : min(len(text), start + 2200)].strip()
        rows.append(
            {
                "source_file": path.name,
                "line_number": line_number(text, start),
                "semantic_kind": classify_kind(name),
                "title": name,
                "domain_family": domain_for(path.name, block),
                "extraction_method": "wolfram_named_block",
                "block_summary": summarize(block),
                "full_block": block,
                "status": "wolfram_theorem_block_staged",
            }
        )
    return rows


def extract_toe_blocks(path: Path, text: str) -> list[dict]:
    rows = []
    if not re.search(r"theory of everything|unified field topology|univision|trawin zero points", text, re.IGNORECASE):
        return rows
    headings = list(re.finditer(r"^(#{1,6}\s+.*|\\section\{.*?\}|\\subsection\{.*?\})$", text, re.MULTILINE))
    if not headings:
        rows.append(
            {
                "source_file": path.name,
                "line_number": 1,
                "section_title": path.stem,
                "domain_family": domain_for(path.name, text),
                "block_summary": summarize(text, 800),
                "status": "toe_source_staged",
            }
        )
        return rows
    for i, h in enumerate(headings):
        end = headings[i + 1].start() if i + 1 < len(headings) else min(len(text), h.start() + 5000)
        block = text[h.start() : end].strip()
        rows.append(
            {
                "source_file": path.name,
                "line_number": line_number(text, h.start()),
                "section_title": h.group(0).strip(),
                "domain_family": domain_for(path.name, block),
                "block_summary": summarize(block, 800),
                "status": "toe_source_staged",
            }
        )
    return rows


def write_tex_copy(path: Path, text: str) -> Path | None:
    if "\\documentclass" not in text and "\\begin{theorem}" not in text and "\\section" not in text:
        return None
    TEX_DIR.mkdir(parents=True, exist_ok=True)
    target = TEX_DIR / (path.stem.replace(" ", "_").replace("-", "_") + ".tex")
    tex = strip_latex_fence(text)
    if "\\hypersetup" not in tex and "\\usepackage{hyperref" in tex:
        tex = tex.replace(
            "\\usepackage{hyperref,cleveref}",
            "\\usepackage{hyperref,cleveref}\n\\hypersetup{pdfauthor={Daniel Alexander Trawin},pdfcreator={Trawin, Daniel Alexander},colorlinks=false}",
        )
    target.write_text(tex, encoding="utf-8")
    return target


def write_wolfram_fences(path: Path, text: str) -> list[Path]:
    WOLFRAM_DIR.mkdir(parents=True, exist_ok=True)
    out = []
    for i, match in enumerate(FENCE_RE.finditer(text), start=1):
        code = match.group(1).strip()
        if not code:
            continue
        target = WOLFRAM_DIR / f"{path.stem.replace(' ', '_').replace('-', '_')}_block_{i:02d}.wls"
        target.write_text(code, encoding="utf-8")
        out.append(target)
    return out


def main() -> None:
    ROOT.mkdir(parents=True, exist_ok=True)
    theorem_rows = []
    toe_rows = []
    tex_copies = []
    wolfram_blocks = []
    for path in sorted(SOURCE.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in {".txt", ".tex", ".md", ".ltx", ".latex"}:
            continue
        text = clean_text(path.read_text(encoding="utf-8", errors="replace"))
        theorem_rows.extend(extract_theorem_blocks(path, text))
        toe_rows.extend(extract_toe_blocks(path, text))
        tex_copy = write_tex_copy(path, text)
        if tex_copy:
            tex_copies.append(str(tex_copy))
        wolfram_blocks.extend(str(p) for p in write_wolfram_fences(path, text))

    with THEOREM_CSV.open("w", encoding="utf-8", newline="") as handle:
        fields = [
            "source_file",
            "line_number",
            "semantic_kind",
            "title",
            "domain_family",
            "extraction_method",
            "block_summary",
            "full_block",
            "status",
        ]
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(theorem_rows)

    with TOE_CSV.open("w", encoding="utf-8", newline="") as handle:
        fields = ["source_file", "line_number", "section_title", "domain_family", "block_summary", "status"]
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(toe_rows)

    counts = {
        "generated_utc": now_utc(),
        "source": str(SOURCE),
        "theorem_semantic_blocks": len(theorem_rows),
        "toe_source_blocks": len(toe_rows),
        "tex_copies": tex_copies,
        "wolfram_fence_blocks": wolfram_blocks,
        "semantic_kind_counts": Counter(row["semantic_kind"] for row in theorem_rows),
        "domain_counts": Counter(row["domain_family"] for row in theorem_rows),
        "toe_files": sorted(set(row["source_file"] for row in toe_rows)),
    }
    SUMMARY.write_text(json.dumps(json.loads(json.dumps(counts, default=dict)), indent=2), encoding="utf-8")

    lines = [
        "# Phone2 Theorem and ToE Intake Report",
        "",
        f"- Generated UTC: `{counts['generated_utc']}`",
        f"- Source: `{SOURCE}`",
        f"- Theorem/semantic blocks staged: `{len(theorem_rows)}`",
        f"- ToE/source sections staged: `{len(toe_rows)}`",
        f"- TeX-normalized copies: `{len(tex_copies)}`",
        f"- Wolfram fenced blocks extracted: `{len(wolfram_blocks)}`",
        "",
        "## Semantic Kinds",
        "",
        "| Kind | Count |",
        "|---|---:|",
    ]
    for kind, count in Counter(row["semantic_kind"] for row in theorem_rows).most_common():
        lines.append(f"| {kind} | {count} |")
    lines.extend(["", "## Domain Families", "", "| Domain | Count |", "|---|---:|"])
    for domain, count in Counter(row["domain_family"] for row in theorem_rows).most_common():
        lines.append(f"| {domain} | {count} |")
    lines.extend(["", "## ToE Files", ""])
    for filename in counts["toe_files"]:
        lines.append(f"- `{filename}`")
    lines.extend(["", "## Generated Artifacts", ""])
    for artifact in [THEOREM_CSV, TOE_CSV, SUMMARY]:
        lines.append(f"- `{artifact}`")
    for tex in tex_copies:
        lines.append(f"- `{tex}`")
    lines.extend(
        [
            "",
            "## Recommendation",
            "",
            "Use this theorem/ToE queue before minting the remaining Phone2 equation batches. These rows provide proof roles, theorem names, and document-level context for equations already staged or minted.",
        ]
    )
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(json.loads(json.dumps(counts, default=dict)), indent=2))


if __name__ == "__main__":
    main()
