from __future__ import annotations

import csv
import re
from collections import Counter
from datetime import datetime
from pathlib import Path


ROOT = Path(r"D:\Proofs")
OUT_DIR = Path(r"D:\TZPIDProof\peer_review\external_evidence")

EXTS = {".md", ".txt", ".csv"}
ID_RE = re.compile(r"\bID\s*[-:]?\s*(\d{1,5})\b", re.IGNORECASE)
DOI_RE = re.compile(r"\b10\.\d{4,9}/[-._;()/:A-Z0-9]+", re.IGNORECASE)
ARXIV_RE = re.compile(r"\barXiv\s*[: ]\s*(\d{4}\.\d{4,5}(?:v\d+)?)|\b(\d{4}\.\d{4,5})(?:v\d+)?\b", re.IGNORECASE)
URL_RE = re.compile(r"https?://[^\s)\]}>,]+", re.IGNORECASE)

EVIDENCE_TERMS = [
    "experiment",
    "experimental",
    "lab",
    "laboratory",
    "measurement",
    "measured",
    "observed",
    "observation",
    "test",
    "verified",
    "validated",
    "data",
    "dataset",
    "mit",
    "quantum hall",
    "hall effect",
    "nobel",
    "nature",
    "science",
    "physical review",
    "prl",
    "journal",
    "doi",
    "arxiv",
]

DOMAIN_TERMS = {
    "quantum_hall": ["quantum hall", "hall effect", "integer hall", "fractional hall"],
    "quantum": ["quantum", "wavefunction", "hilbert", "bell", "entanglement"],
    "gravity_gr": ["gravity", "relativity", "einstein", "curvature", "metric", "spacetime"],
    "topology": ["topolog", "chern", "berry", "winding", "holonomy", "hopf"],
    "cosmology": ["hubble", "friedmann", "bao", "cmb", "dark energy", "cosmolog"],
    "bessel_wave": ["bessel", "standing wave", "wave", "eigenmode", "resonance"],
    "gyromagnetic": ["gyro", "magnetic", "magnet", "helicity", "elsasser", "vortex"],
}


def normalize_id(value: str) -> str:
    return f"ID{int(value):04d}"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def evidence_score(text: str, path: Path) -> int:
    hay = (str(path) + "\n" + text[:100000]).lower()
    return sum(hay.count(term) for term in EVIDENCE_TERMS)


def domains(text: str, path: Path) -> list[str]:
    hay = (str(path) + "\n" + text[:100000]).lower()
    out = []
    for domain, terms in DOMAIN_TERMS.items():
        if any(term in hay for term in terms):
            out.append(domain)
    return sorted(out)


def row_for(path: Path) -> dict[str, str]:
    text = read_text(path)
    ids = sorted({normalize_id(v) for v in ID_RE.findall(text)})
    dois = sorted(set(DOI_RE.findall(text)))
    arxiv_matches = ARXIV_RE.findall(text)
    arxivs = sorted({a or b for a, b in arxiv_matches if a or b})
    urls = sorted(set(URL_RE.findall(text)))
    score = evidence_score(text, path)
    domain_list = domains(text, path)
    if dois or arxivs or score >= 30:
        priority = "high_external_evidence"
    elif urls or score >= 10:
        priority = "medium_external_evidence"
    else:
        priority = "low_or_internal_notes"
    return {
        "file_name": path.name,
        "full_path": str(path),
        "extension": path.suffix.lower(),
        "length": str(path.stat().st_size),
        "evidence_score": str(score),
        "priority": priority,
        "domains": "; ".join(domain_list),
        "id_count": str(len(ids)),
        "ids": "; ".join(ids),
        "doi_count": str(len(dois)),
        "dois": "; ".join(dois[:20]),
        "arxiv_count": str(len(arxivs)),
        "arxiv_ids": "; ".join(arxivs[:20]),
        "url_count": str(len(urls)),
        "urls": "; ".join(urls[:20]),
    }


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else [])
        writer.writeheader()
        writer.writerows(rows)


def md_table(rows: list[dict[str, str]], cols: list[str], limit: int = 40) -> str:
    out = ["| " + " | ".join(cols) + " |", "| " + " | ".join("---" for _ in cols) + " |"]
    for row in rows[:limit]:
        vals = []
        for col in cols:
            val = row.get(col, "").replace("|", "\\|").replace("\n", " ")
            if len(val) > 110:
                val = val[:107] + "..."
            vals.append(val)
        out.append("| " + " | ".join(vals) + " |")
    if len(rows) > limit:
        vals = ["..."] + [f"{len(rows) - limit} more rows omitted"] + [""] * max(0, len(cols) - 2)
        out.append("| " + " | ".join(vals[: len(cols)]) + " |")
    return "\n".join(out)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    paths = [path for path in ROOT.rglob("*") if path.is_file() and path.suffix.lower() in EXTS]
    rows = [row_for(path) for path in sorted(paths)]
    rows.sort(key=lambda r: (-int(r["evidence_score"]), r["full_path"]))
    evidence_rows = [r for r in rows if r["priority"] != "low_or_internal_notes"]

    all_csv = OUT_DIR / "EXTERNAL_EVIDENCE_SOURCE_INVENTORY.csv"
    evidence_csv = OUT_DIR / "EXTERNAL_EVIDENCE_INDEX.csv"
    write_csv(all_csv, rows)
    write_csv(evidence_csv, evidence_rows)

    priority_counts = Counter(r["priority"] for r in rows)
    domain_counts = Counter()
    for row in evidence_rows:
        for d in row["domains"].split("; "):
            if d:
                domain_counts[d] += 1

    report = []
    report.append("# External Evidence Index\n")
    report.append(f"Generated: {datetime.now().isoformat(timespec='seconds')}\n")
    report.append("## Scope\n")
    report.append("- Source folder: `D:\\Proofs`")
    report.append(f"- Files scanned: {len(rows)}")
    report.append(f"- External-evidence candidates: {len(evidence_rows)}")
    report.append("")
    report.append("## Priority Counts\n")
    for key in sorted(priority_counts):
        report.append(f"- {key}: {priority_counts[key]}")
    report.append("")
    report.append("## Domain Counts\n")
    for key in sorted(domain_counts):
        report.append(f"- {key}: {domain_counts[key]}")
    report.append("")
    report.append("## Highest-Scoring Evidence Sources\n")
    report.append(md_table(evidence_rows, [
        "full_path",
        "evidence_score",
        "priority",
        "domains",
        "id_count",
        "doi_count",
        "arxiv_count",
        "url_count",
    ]))
    report.append("")
    report.append("## Isabelle Role\n")
    report.append(
        "These files should be represented as external evidence carriers: Isabelle "
        "does not prove the experiments, but it can prove that a registry or paper "
        "claim has a declared external evidence anchor and that the anchor belongs "
        "to the expected domain family."
    )
    report.append("")
    report.append("## Output Files\n")
    report.append(f"- Full inventory: `{all_csv}`")
    report.append(f"- Evidence index: `{evidence_csv}`")
    (OUT_DIR / "EXTERNAL_EVIDENCE_INDEX.md").write_text("\n".join(report), encoding="utf-8")
    print(f"files={len(rows)} evidence_candidates={len(evidence_rows)}")
    print(f"wrote {OUT_DIR / 'EXTERNAL_EVIDENCE_INDEX.md'}")


if __name__ == "__main__":
    main()
