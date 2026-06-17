import argparse
import csv
import hashlib
import re
from dataclasses import dataclass
from pathlib import Path

import pdfplumber


DEFAULT_OUTPUT_DIR = Path("zenodo_tex_axiom_theory_scan")

TEXT_EXTENSIONS = {".tex", ".md", ".txt"}
EXCLUDED_DIR_NAMES = {
    ".venvs",
    "__pycache__",
    "texlive",
    "tmp",
    "_build_rendered_template",
    "bertopic_preserve_out",
}

KIND_PATTERNS = [
    ("Axiom", r"axiom"),
    ("Theorem", r"theorem"),
    ("Lemma", r"lemma"),
    ("Postulate", r"postulate"),
    ("Principle", r"principle"),
    ("Definition", r"definition"),
    ("Proposition", r"proposition"),
    ("Corollary", r"corollary"),
    ("Hypothesis", r"hypothesis"),
    ("Conjecture", r"conjecture"),
    ("Invariant", r"invariant"),
    ("Law", r"law"),
]

CORE_TERMS = {
    "trawin": 12,
    "tzp": 12,
    "zero point": 10,
    "tzpqvt": 9,
    "hamiltonian": 8,
    "master equation": 8,
    "helical": 7,
    "holographic": 7,
    "gyromagnetic": 7,
    "topological": 7,
    "unification": 7,
    "field theory": 7,
    "curvature": 6,
    "daansphere": 6,
    "invariant": 6,
    "coupling": 5,
    "kernel": 5,
    "manifold": 5,
    "projection": 4,
    "lindblad": 4,
    "kaluza": 4,
    "helicity": 4,
}

KIND_WEIGHT = {
    "Axiom": 50,
    "Theorem": 42,
    "Postulate": 38,
    "Principle": 34,
    "Lemma": 30,
    "Proposition": 27,
    "Corollary": 24,
    "Definition": 22,
    "Invariant": 21,
    "Law": 20,
    "Hypothesis": 16,
    "Conjecture": 14,
}

SOURCE_WEIGHT_TERMS = {
    "axiom": 18,
    "canonical": 14,
    "trawin": 12,
    "tzpid": 12,
    "tzp_oo": 10,
    "zero_point": 10,
    "unification": 9,
    "field_theory": 9,
    "gyromagnetic": 8,
    "hms": 7,
    "curvature": 6,
}


@dataclass
class Candidate:
    kind: str
    title: str
    body: str
    source: str
    line: int
    score: int
    digest: str


def clean_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def squash(text: str, limit: int = 900) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    return text[:limit] + ("..." if len(text) > limit else "")


def line_number(text: str, start: int) -> int:
    return text.count("\n", 0, max(0, start)) + 1


def classify_kind(label: str) -> str:
    low = label.lower()
    for kind, pattern in KIND_PATTERNS:
        if re.search(pattern, low):
            return kind
    return "Other"


def score_candidate(kind: str, title: str, body: str, source: str) -> int:
    title_low = title.lower()
    body_low = body.lower()
    source_low = source.lower().replace("\\", "/")
    score = KIND_WEIGHT.get(kind, 5)
    if str(source).lower().endswith(".pdf"):
        score += 8
    for term, weight in CORE_TERMS.items():
        if term in title_low:
            score += weight * 2
        elif term in body_low:
            score += weight
    for term, weight in SOURCE_WEIGHT_TERMS.items():
        if term in source_low:
            score += weight
    if re.search(r"\\begin\{(axiom|theorem|lemma|definition|proposition|hypothesis|corollary)\}", body, re.I):
        score += 8
    if re.search(r"\\(equation|frac|mathcal|mathbf|hat|partial|nabla|int|sum)", body):
        score += 6
    if "tbd" in body_low or "conversation" in source_low:
        score -= 12
    if len(body) < 40:
        score -= 8
    return score


def make_digest(*parts: str) -> str:
    return hashlib.sha1("|".join(parts).encode("utf-8", errors="ignore")).hexdigest()


def add_candidate(candidates, kind, title, body, source, line):
    title = squash(title, 220)
    body = squash(body, 1400)
    score = score_candidate(kind, title, body, source)
    digest = make_digest(kind, title, body, source, str(line))
    candidates.append(Candidate(kind, title, body, source, line, score, digest))


def extract_latex_blocks(text: str, source: str):
    candidates = []
    env_re = re.compile(
        r"\\begin\{(?P<env>axiom|theorem|lemma|definition|proposition|hypothesis|corollary)\}"
        r"(?:\[(?P<title>[^\]]+)\])?"
        r"(?P<body>.*?)\\end\{(?P=env)\}",
        re.I | re.S,
    )
    for match in env_re.finditer(text):
        env = match.group("env")
        title = match.group("title") or env.title()
        body = match.group("body")
        add_candidate(candidates, env.title(), title, body, source, line_number(text, match.start()))

    section_re = re.compile(
        r"\\(?:section|subsection|subsubsection|paragraph)\*?\{(?P<title>[^{}]*(?:Axiom|Theorem|Lemma|Postulate|Principle|Definition|Invariant|Law|Hypothesis|Conjecture)[^{}]*)\}"
        r"(?P<body>.*?)(?=\\(?:section|subsection|subsubsection|paragraph)\*?\{|\\begin\{|$)",
        re.I | re.S,
    )
    for match in section_re.finditer(text):
        title = match.group("title")
        kind = classify_kind(title)
        add_candidate(candidates, kind, title, match.group("body"), source, line_number(text, match.start()))

    bold_re = re.compile(
        r"\\textbf\{(?P<title>[^{}]*(?:Axiom|Theorem|Lemma|Postulate|Principle|Definition|Invariant|Law|Hypothesis|Conjecture)[^{}]*)\}"
        r"(?P<body>.{0,1800})",
        re.I | re.S,
    )
    for match in bold_re.finditer(text):
        title = match.group("title")
        kind = classify_kind(title)
        add_candidate(candidates, kind, title, match.group("body"), source, line_number(text, match.start()))
    return candidates


def extract_plain_blocks(text: str, source: str):
    candidates = []
    heading_re = re.compile(
        r"(?im)^(?P<title>(?:#+\s*)?(?:Axiom|Theorem|Lemma|Postulate|Principle|Definition|Invariant|Law|Hypothesis|Conjecture)"
        r"(?:\s+[IVXLCDM0-9A-Za-z_.-]+)?(?::|\s-\s|\s+of\b|\s+for\b|$).*)$"
    )
    matches = list(heading_re.finditer(text))
    for i, match in enumerate(matches):
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else min(len(text), start + 2200)
        title = match.group("title").strip("# ").strip()
        kind = classify_kind(title)
        add_candidate(candidates, kind, title, text[start:end], source, line_number(text, match.start()))
    return candidates


def extract_candidates_from_text(text: str, source: str):
    text = clean_text(text)
    candidates = []
    candidates.extend(extract_latex_blocks(text, source))
    candidates.extend(extract_plain_blocks(text, source))
    return candidates


def iter_text_files(tex_root: Path):
    for path in tex_root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in TEXT_EXTENSIONS:
            continue
        parts = {p.lower() for p in path.parts}
        if parts & EXCLUDED_DIR_NAMES:
            continue
        if path.stat().st_size > 8_000_000:
            continue
        yield path


def read_text_file(path: Path) -> str:
    for encoding in ("utf-8", "utf-8-sig", "latin-1"):
        try:
            return path.read_text(encoding=encoding, errors="ignore")
        except Exception:
            continue
    return ""


def read_pdf_text(path: Path) -> str:
    chunks = []
    try:
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                chunks.append(page.extract_text() or "")
    except Exception as exc:
        return f"[PDF extraction failed: {exc}]"
    return "\n\n".join(chunks)


def scan(zenodo_root: Path, tex_root: Path):
    candidates = []
    for pdf in sorted(zenodo_root.glob("*.pdf")):
        text = read_pdf_text(pdf)
        candidates.extend(extract_candidates_from_text(text, str(pdf)))

    for path in iter_text_files(tex_root):
        text = read_text_file(path)
        if not text:
            continue
        lower = text.lower()
        if not any(term in lower for term in ["axiom", "theorem", "lemma", "postulate", "principle", "definition"]):
            continue
        candidates.extend(extract_candidates_from_text(text, str(path)))

    deduped = {}
    for cand in candidates:
        key = (cand.kind, cand.title.lower(), cand.body[:300].lower())
        existing = deduped.get(key)
        if existing is None or cand.score > existing.score:
            deduped[key] = cand
    return sorted(deduped.values(), key=lambda c: (-c.score, c.kind, c.title))


def write_csv(candidates, output_dir: Path):
    path = output_dir / "axiom_theory_candidates.csv"
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["rank", "score", "kind", "title", "source", "line", "digest", "body"],
        )
        writer.writeheader()
        for i, cand in enumerate(candidates, start=1):
            writer.writerow(
                {
                    "rank": i,
                    "score": cand.score,
                    "kind": cand.kind,
                    "title": cand.title,
                    "source": cand.source,
                    "line": cand.line,
                    "digest": cand.digest,
                    "body": cand.body,
                }
            )
    return path


def write_report(candidates, output_dir: Path, top_n: int):
    path = output_dir / "important_axioms_theories.md"
    by_kind = {}
    for cand in candidates:
        by_kind[cand.kind] = by_kind.get(cand.kind, 0) + 1
    lines = [
        "# Important Axioms and Theories from D:\\Zenodo and D:\\Tex",
        "",
        f"- Candidates extracted: **{len(candidates)}**",
        "- Ranking favors explicit axioms/theorems/postulates, TZP/TRAWIN centrality, source centrality, and mathematical density.",
        "- Full machine-readable inventory: `axiom_theory_candidates.csv`",
        "",
        "## Counts by Kind",
        "",
    ]
    for kind, count in sorted(by_kind.items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"- {kind}: {count}")
    lines.extend(["", f"## Top {top_n}", ""])
    for i, cand in enumerate(candidates[:top_n], start=1):
        lines.extend(
            [
                f"### {i}. {cand.kind}: {cand.title}",
                "",
                f"- Score: `{cand.score}`",
                f"- Source: `{cand.source}`",
                f"- Line/Page anchor: `{cand.line}`",
                f"- Digest: `{cand.digest}`",
                "",
                cand.body,
                "",
            ]
        )
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def main():
    parser = argparse.ArgumentParser(description="Scan D:\\Zenodo and D:\\Tex for important axioms/theories.")
    parser.add_argument("--zenodo-root", default="D:/Zenodo")
    parser.add_argument("--tex-root", default="D:/Tex")
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR))
    parser.add_argument("--top-n", type=int, default=80)
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    candidates = scan(Path(args.zenodo_root), Path(args.tex_root))
    csv_path = write_csv(candidates, output_dir)
    report_path = write_report(candidates, output_dir, args.top_n)

    print(f"Candidates: {len(candidates)}")
    print(f"Wrote {csv_path}")
    print(f"Wrote {report_path}")
    for cand in candidates[:15]:
        print(f"{cand.score:>3} {cand.kind:<11} {cand.title[:80]} :: {cand.source}")


if __name__ == "__main__":
    main()
