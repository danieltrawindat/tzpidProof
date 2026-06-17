import csv
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\TZPIDProof")
MASTER = ROOT / "TZPID_ALL_IDS_CANONICAL_EQUATION_MASTER_with_export.csv"
SHORTLIST = ROOT / "edge_case_equations" / "TZPID_EDGE_CASE_EQUATION_SHORTLIST.csv"
OUT_DIR = ROOT / "edge_case_equations"

QUARANTINE_CSV = OUT_DIR / "TZPID_MASTER_SHELL_ARTIFACT_SIGNAL_QUARANTINE.csv"
QUARANTINE_MD = OUT_DIR / "TZPID_MASTER_SHELL_ARTIFACT_SIGNAL_QUARANTINE.md"
CLEAN_SHORTLIST_CSV = OUT_DIR / "TZPID_EDGE_CASE_EQUATION_SHORTLIST_PROOF_CLEAN.csv"
CLEAN_SHORTLIST_MD = OUT_DIR / "TZPID_EDGE_CASE_EQUATION_SHORTLIST_PROOF_CLEAN.md"
CLEAN_MASTER_CSV = ROOT / "TZPID_ALL_IDS_CANONICAL_EQUATION_MASTER_PROOF_CLEAN_NO_SHELL_SIGNALS.csv"
REPORT_JSON = OUT_DIR / "shell_artifact_signal_scrap_report.json"


def read_csv(path):
    with path.open(encoding="utf-8-sig", newline="", errors="replace") as handle:
        reader = csv.DictReader(handle)
        return list(reader), reader.fieldnames


def write_csv(path, rows, fields):
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        writer.writerows(rows)


def md_escape(value):
    return (value or "").replace("|", "\\|").replace("\n", " ").strip()


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    generated = datetime.now(timezone.utc).isoformat()

    shortlist, shortlist_fields = read_csv(SHORTLIST)
    master, master_fields = read_csv(MASTER)
    master_by_id = {row.get("id", ""): row for row in master}

    shell_rows = [row for row in shortlist if row.get("shell_artifact_signal") == "yes"]
    shell_ids = {row["id"] for row in shell_rows}
    clean_shortlist = [row for row in shortlist if row.get("shell_artifact_signal") != "yes"]
    clean_master = [row for row in master if row.get("id") not in shell_ids]

    quarantine_rows = []
    for row in shell_rows:
        master_row = master_by_id.get(row["id"], {})
        quarantine_rows.append(
            {
                "id": row.get("id", ""),
                "title": row.get("title", ""),
                "score": row.get("score", ""),
                "category_hits": row.get("category_hits", ""),
                "recommended_use": "scrapped from proof-facing clean outputs; retained only as source-provenance quarantine",
                "source": row.get("source", ""),
                "canonical_equation": row.get("canonical_equation", ""),
                "master_kind": master_row.get("kind", "") or master_row.get("isabelle_kind", ""),
                "master_source": master_row.get("source", ""),
            }
        )

    quarantine_fields = [
        "id",
        "title",
        "score",
        "category_hits",
        "recommended_use",
        "source",
        "canonical_equation",
        "master_kind",
        "master_source",
    ]
    write_csv(QUARANTINE_CSV, quarantine_rows, quarantine_fields)
    write_csv(CLEAN_SHORTLIST_CSV, clean_shortlist, shortlist_fields)
    write_csv(CLEAN_MASTER_CSV, clean_master, master_fields)

    clean_md = [
        "# Proof-Clean Edge-Case Equation Shortlist",
        "",
        f"Generated UTC: {generated}",
        "",
        f"- Original shortlist rows: `{len(shortlist)}`",
        f"- Scrapped shell-artifact signal rows: `{len(shell_rows)}`",
        f"- Proof-clean shortlist rows: `{len(clean_shortlist)}`",
        "",
        "Rows marked with `shell_artifact_signal=yes` were removed from this proof-facing shortlist and placed in the quarantine file.",
        "",
        "| ID | Score | Category Hits | Title | Candidate |",
        "|---|---:|---|---|---|",
    ]
    for row in clean_shortlist[:100]:
        clean_md.append(
            f"| {row['id']} | {row['score']} | {md_escape(row['category_hits'])} | "
            f"{md_escape(row['title'])} | {md_escape(row['canonical_equation'])[:260]} |"
        )
    CLEAN_SHORTLIST_MD.write_text("\n".join(clean_md) + "\n", encoding="utf-8")

    quarantine_md = [
        "# Master Shell-Artifact Signal Quarantine",
        "",
        f"Generated UTC: {generated}",
        "",
        "These rows were flagged by the edge-case audit as shell/code-like signals. They have been scrapped from proof-facing clean outputs and retained here only for provenance and manual rescue review.",
        "",
        f"- Quarantined rows: `{len(quarantine_rows)}`",
        f"- Original master rows: `{len(master)}`",
        f"- Proof-clean master rows: `{len(clean_master)}`",
        "",
        "| ID | Score | Title | Candidate |",
        "|---|---:|---|---|",
    ]
    for row in quarantine_rows:
        quarantine_md.append(
            f"| {row['id']} | {row['score']} | {md_escape(row['title'])} | "
            f"{md_escape(row['canonical_equation'])[:320]} |"
        )
    QUARANTINE_MD.write_text("\n".join(quarantine_md) + "\n", encoding="utf-8")

    report = {
        "generated_utc": generated,
        "original_master_rows": len(master),
        "proof_clean_master_rows": len(clean_master),
        "original_shortlist_rows": len(shortlist),
        "proof_clean_shortlist_rows": len(clean_shortlist),
        "scrapped_shell_artifact_signal_rows": len(shell_rows),
        "scrapped_ids": sorted(shell_ids, key=lambda x: int(x[2:])),
        "outputs": {
            "quarantine_csv": str(QUARANTINE_CSV),
            "quarantine_md": str(QUARANTINE_MD),
            "clean_shortlist_csv": str(CLEAN_SHORTLIST_CSV),
            "clean_shortlist_md": str(CLEAN_SHORTLIST_MD),
            "clean_master_csv": str(CLEAN_MASTER_CSV),
        },
    }
    REPORT_JSON.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
