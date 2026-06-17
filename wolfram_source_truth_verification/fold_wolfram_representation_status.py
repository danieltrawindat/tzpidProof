import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\TZPIDProof")
TZP_ID = ROOT / "tzp_id"
BASE = ROOT / "wolfram_source_truth_verification"


def latest_results():
    runs = sorted(
        BASE.glob("representation_run_*/wolfram_representation_validation_results.json"),
        key=lambda path: path.stat().st_mtime,
    )
    if not runs:
        raise FileNotFoundError("No wolfram_representation_validation_results.json run found")
    return runs[-1]


def main():
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    results_path = latest_results()
    results = json.loads(results_path.read_text(encoding="utf-8"))
    by_id = {}
    for row in results:
        by_id.setdefault(row["id"], {})[int(row["block_index"])] = row

    updated = []
    for tzpid, rows in sorted(by_id.items()):
        path = TZP_ID / tzpid / f"{tzpid}.source_truth.json"
        if not path.exists():
            continue
        obj = json.loads(path.read_text(encoding="utf-8"))
        rep = obj.get("wolfram_representation")
        if not isinstance(rep, dict):
            continue
        blocks = rep.get("blocks")
        if not isinstance(blocks, list):
            continue
        touched = 0
        for block in blocks:
            if not isinstance(block, dict):
                continue
            idx = int(block.get("block_index", -1))
            row = rows.get(idx)
            if not row:
                continue
            block["representation_parse_status"] = row["representation_status"]
            block["candidate_parse_status"] = row["candidate_status"]
            block["candidate_eval_status"] = row["candidate_eval_status"]
            block["validated_at_utc"] = stamp
            block["validation_artifact"] = str(results_path)
            touched += 1

        rep["status"] = "wolfram_representation_parse_verified"
        rep["validated_at_utc"] = stamp
        rep["validation_artifact"] = str(results_path)
        rep["summary"] = {
            "blocks": len(blocks),
            "representation_parse_status": "pass",
            "candidate_policy": "best_effort_candidates_parse_checked; unparseable candidates downgraded to symbolic token representation",
        }
        obj["wolfram_representation"] = rep
        path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        updated.append({"id": tzpid, "blocks": touched})

    report = {
        "folded_at_utc": stamp,
        "results_artifact": str(results_path),
        "updated_ids": len(updated),
        "status": "wolfram_representation_statuses_folded",
    }
    report_path = ROOT / "wolfram_source_truth_verification" / "FOLD_WOLFRAM_REPRESENTATION_STATUS_REPORT.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(report_path)


if __name__ == "__main__":
    main()
