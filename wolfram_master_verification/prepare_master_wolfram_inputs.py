from __future__ import annotations

import csv
import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUN_ROOT = Path(__file__).resolve().parent
MASTER_CSV = ROOT / "TZPID_ALL_IDS_CANONICAL_EQUATION_MASTER_with_export.csv"
LADDER_MD = ROOT / "TZPID_ALL_IDS_REASSEMBLED_PROOF_LADDER_WITH_EQUATIONS.md"


def clean_equation(text: str) -> str:
    text = (text or "").strip()
    text = text.strip("`")
    text = text.replace("\u00a0", " ")
    return re.sub(r"\s+", " ", text)


def split_segments(equation: str) -> list[str]:
    parts: list[str] = []
    for chunk in re.split(r"\s*\|\|\s*", equation):
        chunk = chunk.strip()
        if not chunk:
            continue
        parts.append(chunk)
    return parts


def simple_class(segment: str) -> str:
    s = segment.strip()
    if not s:
        return "empty"
    if re.fullmatch(r"[0-9\s\.\+\-\*/\^\(\)=<>]+", s):
        return "numeric_ascii"
    if any(tok in s for tok in ["\\frac", "\\sqrt", "\\pi", "\\sin", "\\cos", "\\log"]):
        return "elementary_latex"
    if any(tok in s for tok in ["\\lim", "\\int", "\\oint", "\\sum", "\\prod"]):
        return "operator_latex"
    if any(tok in s for tok in ["\\forall", "\\exists", "\\in", "\\subset", "\\to", "\\mapsto"]):
        return "logical_latex"
    if "=" in s or "\\equiv" in s or "\\approx" in s or "\\sim" in s:
        return "relation_latex"
    return "symbolic_latex"


def main() -> None:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    run_dir = RUN_ROOT / f"run_{stamp}"
    copies = run_dir / "master_copy"
    copies.mkdir(parents=True, exist_ok=True)

    shutil.copy2(MASTER_CSV, copies / MASTER_CSV.name)
    if LADDER_MD.exists():
        shutil.copy2(LADDER_MD, copies / LADDER_MD.name)

    rows = []
    segments = []
    with MASTER_CSV.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for index, row in enumerate(reader, start=1):
            equation = clean_equation(row.get("canonical_equation", ""))
            entry = {
                "row": index,
                "id": row.get("id", ""),
                "title": row.get("title", ""),
                "isabelle_kind": row.get("isabelle_kind", ""),
                "obligation_role": row.get("obligation_role", ""),
                "gold_spine": row.get("gold_spine", ""),
                "wolfram_status_existing": row.get("wolfram_status", ""),
                "canonical_equation": equation,
                "has_equation": bool(equation),
                "segment_count": 0,
            }
            if equation:
                parts = split_segments(equation)
                entry["segment_count"] = len(parts)
                for seg_index, seg in enumerate(parts, start=1):
                    segments.append(
                        {
                            "row": index,
                            "id": entry["id"],
                            "title": entry["title"],
                            "segment_index": seg_index,
                            "segment": seg,
                            "class": simple_class(seg),
                            "length": len(seg),
                        }
                    )
            rows.append(entry)

    (run_dir / "master_equation_rows.json").write_text(
        json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (run_dir / "master_equation_segments.json").write_text(
        json.dumps(segments, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    with (run_dir / "master_equation_segments.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f, fieldnames=["row", "id", "title", "segment_index", "class", "length", "segment"]
        )
        writer.writeheader()
        writer.writerows(segments)

    summary = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "run_dir": str(run_dir),
        "source_master": str(MASTER_CSV),
        "source_ladder_with_equations": str(LADDER_MD),
        "master_copy": str(copies / MASTER_CSV.name),
        "row_count": len(rows),
        "rows_with_equation": sum(1 for r in rows if r["has_equation"]),
        "segment_count": len(segments),
    }
    (run_dir / "master_wolfram_input_summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
