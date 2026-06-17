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
    failures = [
        row
        for row in results
        if row.get("candidate_status") == "candidate_parse_error"
    ]
    by_id = {}
    for row in failures:
        by_id.setdefault(row["id"], set()).add(int(row["block_index"]))

    changed = []
    for tzpid, block_indexes in sorted(by_id.items()):
        path = TZP_ID / tzpid / f"{tzpid}.source_truth.json"
        obj = json.loads(path.read_text(encoding="utf-8"))
        rep = obj.get("wolfram_representation", {})
        blocks = rep.get("blocks", [])
        touched = 0
        for block in blocks:
            if not isinstance(block, dict):
                continue
            if int(block.get("block_index", -1)) not in block_indexes:
                continue
            candidate = block.get("candidate_wolfram_input")
            if isinstance(candidate, str) and candidate:
                block["rejected_candidate_wolfram_input"] = candidate
            block["candidate_wolfram_input"] = ""
            block["candidate_parse_status"] = "not_attempted"
            block["candidate_method"] = (
                str(block.get("candidate_method", "heuristic_candidate"))
                + "_downgraded_after_parse_error"
            )
            block["candidate_downgraded_at_utc"] = stamp
            block["candidate_downgrade_reason"] = (
                "Heuristic candidate did not parse in WolframScript; numeric/symbolic token representation retained."
            )
            touched += 1
        rep["status"] = "candidate_parse_errors_downgraded_pending_revalidation"
        rep["candidate_downgrade_artifact"] = str(results_path)
        obj["wolfram_representation"] = rep
        path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        changed.append({"id": tzpid, "blocks_downgraded": touched})

    report = {
        "downgraded_at_utc": stamp,
        "results_artifact": str(results_path),
        "failed_candidates_downgraded": len(failures),
        "ids_touched": len(changed),
        "changed": changed,
    }
    report_path = ROOT / "wolfram_source_truth_verification" / "DOWNGRADE_FAILED_WOLFRAM_CANDIDATES_REPORT.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(report_path)


if __name__ == "__main__":
    main()
