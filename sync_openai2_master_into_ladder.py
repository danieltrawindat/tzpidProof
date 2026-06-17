import csv
import json
import re
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\TZPIDProof")
MASTER = ROOT / "TZPID_ALL_IDS_CANONICAL_EQUATION_MASTER_with_export.csv"
ID_SYSTEM = ROOT / "TZPID_ID_SYSTEM.csv"
OLD_LADDER = ROOT / "sync_backup_20260610_221012" / "TZPID_ALL_IDS_REASSEMBLED_PROOF_LADDER.md"
OUT_LADDER = ROOT / "TZPID_ALL_IDS_REASSEMBLED_PROOF_LADDER.md"
OUT_LADDER_EQ = ROOT / "TZPID_ALL_IDS_REASSEMBLED_PROOF_LADDER_WITH_EQUATIONS.md"
OUT_MASTER_MD = ROOT / "TZPID_ALL_IDS_CANONICAL_EQUATION_MASTER_with_export.md"
OUT_REPORT = ROOT / "MASTER_SYNC_REPORT.json"


def read_master():
    with MASTER.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    return rows


def read_id_system():
    if not ID_SYSTEM.exists():
        return {}
    with ID_SYSTEM.open(encoding="utf-8-sig", newline="") as handle:
        return {row["id"]: row for row in csv.DictReader(handle) if row.get("id")}


def md_escape(value):
    value = "" if value is None else str(value)
    return value.replace("\r", " ").replace("\n", " ").replace("|", "\\|").strip()


def old_ladder_order_and_rests():
    text = OLD_LADDER.read_text(encoding="utf-8", errors="replace")
    order = []
    rests = {}
    old_row = re.compile(r"^\|\s*(\d+)\s*\|\s*(ID\d{4,5})\s*\|(.+)$")
    for line in text.splitlines():
        m = old_row.match(line)
        if not m:
            continue
        parts = [part.strip() for part in line.strip().strip("|").split("|")]
        if len(parts) < 6:
            continue
        tzpid = parts[1]
        order.append(tzpid)
        rests[tzpid] = parts[5] or "—"
    return order, rests


def kind(row):
    return row.get("isabelle_kind") or row.get("obligation_role") or row.get("formation_method") or ""


def master_markdown(rows, generated):
    fields = list(rows[0].keys()) if rows else []
    lines = [
        "# TZPID Canonical Equation Master With Export",
        "",
        f"Generated UTC: {generated}",
        f"Rows: `{len(rows)}`",
        "",
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_escape(row.get(field, "")) for field in fields) + " |")
    return "\n".join(lines) + "\n"


def ladder_markdown(rows, ordered_ids, rests, generated, id_system, with_equations=False):
    by_id = {row["id"]: row for row in rows}
    headers = ["Rung", "ID", "Title", "Kind", "Gold Spine", "Rests on (rungs)", "PiID", "RTEID", "UUID"]
    if with_equations:
        headers += ["Canonical Statement", "Canonical Equation"]
    lines = [
        "# TZPID Reassembled Proof Ladder — All IDs in Derivation Order",
        "",
        "Creator: Daniel Alexander Trawin",
        "ORCID: https://orcid.org/0009-0001-4630-3715",
        f"Generated UTC: {generated}",
        "DOI: https://doi.org/10.5281/zenodo.20632000",
        "Source master: `TZPID_ALL_IDS_CANONICAL_EQUATION_MASTER_with_export.csv`",
        f"Rows: `{len(ordered_ids)}` (every synced canonical ID appears exactly once)",
        "",
        "## Method",
        "",
        "This synced ladder preserves the prior certified derivation order for the first 10,271 rungs and appends the newly synced master entries after that order.",
        "The appended block comes from the current OpenAI2 master copy and should be treated as an incremental derivation-ladder extension until its dependency edges are mined into the next full topology pass.",
        "",
        "Reading rule: entries in the preserved block retain their prior `Rests on` rung references. Newly appended entries use `—` until the next graph-topology rebuild materializes their dependency edges.",
        "",
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---:" if h == "Rung" else "---" for h in headers) + " |",
    ]
    for rung, tzpid in enumerate(ordered_ids, start=1):
        row = by_id[tzpid]
        id_row = id_system.get(tzpid, {})
        values = [
            str(rung),
            tzpid,
            row.get("title", ""),
            kind(row),
            row.get("gold_spine", ""),
            rests.get(tzpid, "—"),
            id_row.get("PiID", row.get("PiID", "")),
            id_row.get("RTEID", row.get("RTEID", "")),
            row.get("uuid", ""),
        ]
        if with_equations:
            values += [row.get("canonical_statement", ""), row.get("canonical_equation", "")]
        lines.append("| " + " | ".join(md_escape(v) for v in values) + " |")
    return "\n".join(lines) + "\n"


def main():
    generated = datetime.now(timezone.utc).isoformat()
    rows = read_master()
    id_system = read_id_system()
    by_id = {row["id"]: row for row in rows}
    old_order, rests = old_ladder_order_and_rests()
    preserved = [tzpid for tzpid in old_order if tzpid in by_id]
    appended = [row["id"] for row in rows if row["id"] not in set(preserved)]
    ordered_ids = preserved + appended

    OUT_MASTER_MD.write_text(master_markdown(rows, generated), encoding="utf-8")
    OUT_LADDER.write_text(ladder_markdown(rows, ordered_ids, rests, generated, id_system, False), encoding="utf-8")
    OUT_LADDER_EQ.write_text(ladder_markdown(rows, ordered_ids, rests, generated, id_system, True), encoding="utf-8")

    report = {
        "generated_utc": generated,
        "master": str(MASTER),
        "master_rows": len(rows),
        "old_ladder_rows_preserved": len(preserved),
        "appended_ids_count": len(appended),
        "appended_ids": appended,
        "id_system_rows": len(id_system),
        "output_ladder": str(OUT_LADDER),
        "output_ladder_with_equations": str(OUT_LADDER_EQ),
        "output_master_md": str(OUT_MASTER_MD),
        "note": "PiID/RTEID for newly synced IDs remain blank unless present in the master; regenerate TZPID_ID_SYSTEM.csv to fill them.",
    }
    OUT_REPORT.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
