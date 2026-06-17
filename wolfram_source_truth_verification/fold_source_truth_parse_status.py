import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\TZPIDProof")
TZP_ID = ROOT / "tzp_id"
BASE = ROOT / "wolfram_source_truth_verification"


def latest_results():
    runs = sorted(
        BASE.glob("run_*/source_truth_wolfram_parse_results.json"),
        key=lambda path: path.stat().st_mtime,
    )
    if not runs:
        raise FileNotFoundError("No source_truth_wolfram_parse_results.json run found")
    return runs[-1]


def main():
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    results_path = latest_results()
    results = json.loads(results_path.read_text(encoding="utf-8"))
    by_id = {}
    for row in results:
        by_id.setdefault(row["id"], []).append(row)

    updated = []
    for tzpid, rows in sorted(by_id.items()):
        path = TZP_ID / tzpid / f"{tzpid}.source_truth.json"
        if not path.exists():
            continue
        obj = json.loads(path.read_text(encoding="utf-8"))
        wf = obj.get("wolfram_form")
        if not isinstance(wf, dict):
            continue
        audit = wf.get("audit")
        if not isinstance(audit, dict):
            continue

        statuses = {row.get("status") for row in rows}
        if statuses == {"wolfram_source_truth_parse_pass"}:
            audit["parse_verification_status"] = "pass"
            audit["parse_verified_at_utc"] = stamp
            audit["parse_verification_artifact"] = str(results_path)
            if audit.get("status") == "minted_source_truth_latex_carrier_pending_parse_verification":
                audit["status"] = "minted_source_truth_latex_carrier_parse_verified"

            blocks = audit.get("blocks")
            if isinstance(blocks, list):
                for block in blocks:
                    if isinstance(block, dict) and block.get("parse_status") == "pending_wolfram_parse_check":
                        block["parse_status"] = "pass"
                        block["parse_verified_at_utc"] = stamp

            formal = obj.get("formal_derivations")
            if isinstance(formal, dict):
                wolfram = formal.get("wolfram")
                if not isinstance(wolfram, dict):
                    wolfram = {}
                if wolfram.get("status") == "wolfram_form_carrier_minted_pending_parse_verification":
                    wolfram["status"] = "wolfram_form_carrier_parse_verified"
                    wolfram["parse_verified_at_utc"] = stamp
                    wolfram["parse_verification_artifact"] = str(results_path)
                    formal["wolfram"] = wolfram
                    obj["formal_derivations"] = formal

            obj["wolfram_form"] = wf
            path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            updated.append(tzpid)

    report = {
        "folded_at_utc": stamp,
        "results_artifact": str(results_path),
        "updated_ids": len(updated),
        "status": "all_parse_pass_statuses_folded",
    }
    report_path = ROOT / "wolfram_source_truth_verification" / "FOLD_SOURCE_TRUTH_PARSE_STATUS_REPORT.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(report_path)


if __name__ == "__main__":
    main()
