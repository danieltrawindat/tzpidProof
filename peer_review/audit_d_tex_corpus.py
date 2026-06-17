from __future__ import annotations

import csv
import hashlib
import re
from collections import Counter
from datetime import datetime
from pathlib import Path


TEX_ROOT = Path(r"D:\Tex")
PROOF_ROOT = Path(r"D:\TZPIDProof")
PEER_TEX = PROOF_ROOT / "peer_review" / "tex"
OUT_DIR = PROOF_ROOT / "peer_review" / "d_tex_audit"

EXCLUDE_PARTS = {
    ".venvs",
    ".venv",
    "texlive",
    "tlpkg",
    "texmf-dist",
    "__pycache__",
    "node_modules",
    ".git",
}

BRIDGE_TERMS = [
    "quantum",
    "general relativity",
    "relativity",
    "einstein",
    "gravity",
    "gravitational",
    "curvature",
    "metric",
    "stress-energy",
    "stress energy",
    "field equation",
    "unification",
    "topological",
    "toe",
    "theory of it all",
    "theorum",
    "well wall wave",
    "www",
    "tut",
    "trawin unification",
    "tzp",
]

ID_RE = re.compile(r"\bID\s*[-:]?\s*(\d{1,5})\b", re.IGNORECASE)
DOI_RE = re.compile(r"10\.5281/zenodo\.\d+")
EQ_RE = re.compile(r"\\begin\{(?:equation|align|gather|multline|eqnarray)\*?\}|\\\[|\\\(")
THEOREM_RE = re.compile(r"\\begin\{(?:theorem|lemma|definition|axiom|proposition|corollary)\}", re.I)


def is_authored_path(path: Path) -> bool:
    parts = {part.lower() for part in path.parts}
    return not any(excluded.lower() in parts for excluded in EXCLUDE_PARTS)


def normalize_id(value: str) -> str:
    return f"ID{int(value):04d}"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def title_from_tex(text: str, fallback: str) -> str:
    m = re.search(r"\\title\{(.+?)\}", text, re.S)
    if not m:
        return fallback
    title = re.sub(r"\\[a-zA-Z]+\*?(?:\[[^\]]*\])?", "", m.group(1))
    title = title.replace("\\\\", " ")
    title = re.sub(r"\s+", " ", title).strip(" {}")
    return title or fallback


def peer_review_hashes() -> set[str]:
    return {sha256(path) for path in PEER_TEX.glob("*.tex") if path.is_file()}


def peer_review_stems() -> set[str]:
    return {path.stem.lower() for path in PEER_TEX.glob("*.tex") if path.is_file()}


def bridge_score(path: Path, text: str) -> int:
    hay = (str(path.relative_to(TEX_ROOT)) + "\n" + text[:50000]).lower()
    return sum(hay.count(term) for term in BRIDGE_TERMS)


def row_for_tex(path: Path, peer_hashes: set[str], peer_stems: set[str]) -> dict[str, str]:
    text = path.read_text(encoding="utf-8", errors="replace")
    ids = sorted({normalize_id(v) for v in ID_RE.findall(text)})
    dois = sorted(set(DOI_RE.findall(text)))
    file_hash = sha256(path)
    already = file_hash in peer_hashes or path.stem.lower() in peer_stems
    score = bridge_score(path, text)
    eq_count = len(EQ_RE.findall(text))
    thm_count = len(THEOREM_RE.findall(text))
    if already:
        priority = "already_packaged"
    elif score >= 12 or dois:
        priority = "high_quantum_gr_bridge"
    elif score >= 5 or ids or eq_count >= 5 or thm_count:
        priority = "medium_candidate"
    else:
        priority = "low_or_support"
    return {
        "file_name": path.name,
        "stem": path.stem,
        "full_path": str(path),
        "relative_path": str(path.relative_to(TEX_ROOT)),
        "length": str(path.stat().st_size),
        "title": title_from_tex(text, path.stem.replace("_", " ")),
        "doi_count": str(len(dois)),
        "doi_list": "; ".join(dois),
        "id_count": str(len(ids)),
        "ids": "; ".join(ids),
        "equation_like_count": str(eq_count),
        "theorem_env_count": str(thm_count),
        "bridge_score": str(score),
        "sha256": file_hash,
        "already_in_peer_review": "yes" if already else "no",
        "promotion_priority": priority,
    }


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else [])
        writer.writeheader()
        writer.writerows(rows)


def md_table(rows: list[dict[str, str]], cols: list[str], limit: int = 30) -> str:
    out = ["| " + " | ".join(cols) + " |", "| " + " | ".join("---" for _ in cols) + " |"]
    for row in rows[:limit]:
        vals = []
        for col in cols:
            val = row.get(col, "").replace("|", "\\|").replace("\n", " ")
            if len(val) > 100:
                val = val[:97] + "..."
            vals.append(val)
        out.append("| " + " | ".join(vals) + " |")
    if len(rows) > limit:
        vals = ["..."] + [f"{len(rows) - limit} more rows omitted"] + [""] * max(0, len(cols) - 2)
        out.append("| " + " | ".join(vals[: len(cols)]) + " |")
    return "\n".join(out)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    peer_hashes = peer_review_hashes()
    peer_stems = peer_review_stems()
    tex_files = [p for p in TEX_ROOT.rglob("*.tex") if p.is_file() and is_authored_path(p)]
    rows = [row_for_tex(path, peer_hashes, peer_stems) for path in sorted(tex_files)]
    rows.sort(key=lambda r: (r["promotion_priority"], -int(r["bridge_score"]), r["relative_path"]))

    all_csv = OUT_DIR / "D_TEX_AUTHORED_TEX_AUDIT.csv"
    bridge_csv = OUT_DIR / "D_TEX_QUANTUM_GR_BRIDGE_CANDIDATES.csv"
    write_csv(all_csv, rows)
    bridge_rows = [r for r in rows if r["promotion_priority"] in {"high_quantum_gr_bridge", "medium_candidate"}]
    bridge_rows.sort(key=lambda r: (-int(r["bridge_score"]), r["already_in_peer_review"], r["relative_path"]))
    write_csv(bridge_csv, bridge_rows)

    counts = Counter(r["promotion_priority"] for r in rows)
    report = []
    report.append("# D:\\Tex Quantum-to-GR Source Audit\n")
    report.append(f"Generated: {datetime.now().isoformat(timespec='seconds')}\n")
    report.append("## Scope\n")
    report.append(f"- Authored TeX files scanned, excluding TeXLive/venv/vendor folders: {len(rows)}")
    report.append(f"- Quantum-to-GR bridge candidates: {len(bridge_rows)}")
    report.append("")
    report.append("## Priority Counts\n")
    for key in sorted(counts):
        report.append(f"- {key}: {counts[key]}")
    report.append("")
    report.append("## Highest-Scoring Bridge Candidates\n")
    report.append(md_table(bridge_rows, [
        "relative_path",
        "title",
        "bridge_score",
        "id_count",
        "equation_like_count",
        "theorem_env_count",
        "already_in_peer_review",
        "promotion_priority",
    ]))
    report.append("")
    report.append("## Simulation-Proof Lane\n")
    report.append(
        "Python/Wolfram/HDF5 simulations should enter Isabelle as certificate artifacts: "
        "the script computes a JSON/CSV/HDF5 result, a small verifier checks thresholds and hashes, "
        "and Isabelle imports the finite certificate facts as constants/definitions with explicit assumptions. "
        "Isabelle then proves the implication from certified numerical facts to the paper-facing theorem contract."
    )
    report.append("")
    report.append("## Output Files\n")
    report.append(f"- Full authored TeX audit: `{all_csv}`")
    report.append(f"- Quantum-GR bridge candidates: `{bridge_csv}`")
    (OUT_DIR / "D_TEX_QUANTUM_GR_BRIDGE_AUDIT.md").write_text("\n".join(report), encoding="utf-8")
    print(f"authored_tex={len(rows)} bridge_candidates={len(bridge_rows)}")
    print(f"wrote {OUT_DIR / 'D_TEX_QUANTUM_GR_BRIDGE_AUDIT.md'}")


if __name__ == "__main__":
    main()
