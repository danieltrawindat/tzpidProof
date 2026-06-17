from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\TZPIDProof")
OPENAI2 = Path(r"D:\00_Engine\AI_Workspaces\OpenAI2")
MASTERS = [
    ROOT / "TZPID_ALL_IDS_CANONICAL_EQUATION_MASTER_with_export.csv",
    OPENAI2 / "TZPID_ALL_IDS_CANONICAL_EQUATION_MASTER_with_export.csv",
]
MD_MASTERS = [
    ROOT / "TZPID_ALL_IDS_CANONICAL_EQUATION_MASTER_with_export.md",
    OPENAI2 / "TZPID_ALL_IDS_CANONICAL_EQUATION_MASTER_with_export.md",
]
RESULT = ROOT / "peer_review" / "unification_intake" / "wolfram" / "topological_unification_carrier_mint_check_results.json"
IDS = {"ID11372", "ID11373", "ID11374", "ID11375", "ID11376"}
STATUS = "wolfram_symbolic_carrier_verified;artifact=peer_review/unification_intake/wolfram/topological_unification_carrier_mint_check_results.json"


def read_rows(path: Path):
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        return list(reader.fieldnames or []), list(reader)


def write_rows(path: Path, fields, rows) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(csv_path: Path, md_path: Path) -> None:
    fields, rows = read_rows(csv_path)
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    lines = [
        "# TZPID Canonical Equation Master With Export",
        "",
        f"Generated UTC: {now}",
        f"Rows: `{len(rows)}`",
        "",
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join(["---"] * len(fields)) + " |",
    ]
    for row in rows:
        vals = []
        for field in fields:
            vals.append((row.get(field, "") or "").replace("\n", " ").replace("|", "\\|"))
        lines.append("| " + " | ".join(vals) + " |")
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def update_master(path: Path) -> int:
    fields, rows = read_rows(path)
    count = 0
    for row in rows:
        if row.get("id") in IDS:
            row["wolfram_status"] = STATUS
            count += 1
    write_rows(path, fields, rows)
    return count


def update_source_truth() -> int:
    count = 0
    for mid in IDS:
        path = ROOT / "tzp_id" / mid / f"{mid}.source_truth.json"
        if not path.exists():
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        data.setdefault("proof_lane", {})["wolfram_status"] = STATUS
        data.setdefault("proof_lane", {})["wolfram_artifact"] = str(RESULT)
        data.setdefault("proof_lane", {})["wolfram_updated_at_utc"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
        path.write_text(json.dumps(data, indent=2), encoding="utf-8")
        count += 1
    return count


def main() -> None:
    if not RESULT.exists():
        raise FileNotFoundError(RESULT)
    updates = {}
    for master in MASTERS:
        if master.exists():
            updates[str(master)] = update_master(master)
    for csv_path, md_path in zip(MASTERS, MD_MASTERS):
        if csv_path.exists():
            write_markdown(csv_path, md_path)
    source_truth_count = update_source_truth()
    print(json.dumps({"master_updates": updates, "source_truth_updates": source_truth_count, "status": STATUS}, indent=2))


if __name__ == "__main__":
    main()
