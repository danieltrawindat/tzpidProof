from __future__ import annotations

import csv
import re
from collections import Counter
from datetime import datetime
from pathlib import Path


ROOTS = [
    Path(r"D:\Graphs"),
    Path(r"D:\Physical_Physics"),
    Path(r"D:\Proofs"),
]
OUT_DIR = Path(r"D:\TZPIDProof\peer_review\simulation_audit")

TERMS = [
    "quantum",
    "relativity",
    "einstein",
    "gravity",
    "gravit",
    "curvature",
    "metric",
    "stress",
    "energy",
    "matter",
    "bessel",
    "delta_alpha",
    "hubble",
    "friedmann",
    "topolog",
    "holonomy",
    "gyro",
    "magnet",
    "wave",
    "well",
    "wall",
    "www",
    "spin",
    "orbit",
    "simulation",
    "certificate",
    "proof",
]

EXTS = {".py", ".ipynb", ".json", ".csv", ".h5", ".hdf5", ".wl", ".wls", ".md", ".txt"}


def score(path: Path, text: str) -> int:
    hay = (str(path) + "\n" + text[:40000]).lower()
    return sum(hay.count(term) for term in TERMS)


def read_text(path: Path) -> str:
    if path.suffix.lower() in {".h5", ".hdf5"}:
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def kind(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix == ".py":
        return "python_script"
    if suffix == ".ipynb":
        return "notebook"
    if suffix in {".h5", ".hdf5"}:
        return "hdf5_certificate"
    if suffix == ".json":
        return "json_certificate"
    if suffix == ".csv":
        return "csv_certificate"
    if suffix in {".wl", ".wls"}:
        return "wolfram_script"
    return "notes_or_report"


def row_for(path: Path) -> dict[str, str]:
    text = read_text(path)
    s = score(path, text)
    imports = "; ".join(sorted(set(re.findall(r"^\s*(?:import|from)\s+([A-Za-z0-9_\.]+)", text, re.M))))[:500]
    priority = "high_simulation_proof" if s >= 15 else "medium_candidate" if s >= 5 else "low_or_support"
    return {
        "root": str(next(root for root in ROOTS if str(path).lower().startswith(str(root).lower()))),
        "file_name": path.name,
        "full_path": str(path),
        "extension": path.suffix.lower(),
        "artifact_kind": kind(path),
        "length": str(path.stat().st_size),
        "score": str(s),
        "priority": priority,
        "imports_or_modules": imports,
    }


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else [])
        writer.writeheader()
        writer.writerows(rows)


def md_table(rows: list[dict[str, str]], cols: list[str], limit: int = 35) -> str:
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
    paths = []
    for root in ROOTS:
        if root.exists():
            paths.extend(path for path in root.rglob("*") if path.is_file() and path.suffix.lower() in EXTS)
    rows = [row_for(path) for path in sorted(paths)]
    rows.sort(key=lambda r: (-int(r["score"]), r["full_path"]))
    candidates = [r for r in rows if r["priority"] != "low_or_support"]

    all_csv = OUT_DIR / "SIMULATION_SOURCE_INVENTORY.csv"
    candidates_csv = OUT_DIR / "QUANTUM_GR_SIMULATION_CANDIDATES.csv"
    write_csv(all_csv, rows)
    write_csv(candidates_csv, candidates)

    counts = Counter(r["priority"] for r in rows)
    kind_counts = Counter(r["artifact_kind"] for r in rows)
    report = []
    report.append("# Quantum-to-GR Simulation Source Audit\n")
    report.append(f"Generated: {datetime.now().isoformat(timespec='seconds')}\n")
    report.append("## Scope\n")
    report.append(f"- Files scanned: {len(rows)}")
    report.append(f"- Candidate simulation/certificate artifacts: {len(candidates)}")
    report.append("")
    report.append("## Priority Counts\n")
    for key in sorted(counts):
        report.append(f"- {key}: {counts[key]}")
    report.append("")
    report.append("## Artifact Kinds\n")
    for key in sorted(kind_counts):
        report.append(f"- {key}: {kind_counts[key]}")
    report.append("")
    report.append("## Highest-Scoring Simulation Sources\n")
    report.append(md_table(candidates, [
        "full_path",
        "artifact_kind",
        "score",
        "priority",
        "imports_or_modules",
    ]))
    report.append("")
    report.append("## Isabelle Simulation-Proof Integration Pattern\n")
    report.append("1. Python script computes a finite certificate: JSON/CSV/HDF5 with explicit parameters, hashes, thresholds, and results.")
    report.append("2. A verifier script checks schema, numeric tolerances, monotonicity/conservation/residual thresholds, and records pass/fail.")
    report.append("3. Isabelle imports the certificate as a small generated `.thy` carrier: constants for parameters/results plus assumptions only for measured facts.")
    report.append("4. Isabelle proves the domain theorem from those facts, e.g. `certificate_passes ⟹ residual_bound_holds ⟹ bridge_contract_holds`.")
    report.append("")
    report.append("## Output Files\n")
    report.append(f"- Full inventory: `{all_csv}`")
    report.append(f"- Candidate queue: `{candidates_csv}`")
    (OUT_DIR / "QUANTUM_GR_SIMULATION_SOURCE_AUDIT.md").write_text("\n".join(report), encoding="utf-8")
    print(f"files={len(rows)} candidates={len(candidates)}")
    print(f"wrote {OUT_DIR / 'QUANTUM_GR_SIMULATION_SOURCE_AUDIT.md'}")


if __name__ == "__main__":
    main()
