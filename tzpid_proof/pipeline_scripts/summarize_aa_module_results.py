import argparse
import csv
import json
from collections import Counter
from pathlib import Path

from tzpid_provenance import generated_utc, provenance_dict


DEFAULT_LIBRARY = r"D:\00_Engine\AI_Workspaces\OpenAI2\algorithmic_ambassador\TZPID_WOLFRAM_MODULE_LIBRARY.csv"
DEFAULT_RESULTS = "wolfram_checks/aa_module_library_results.json"
DEFAULT_OUTPUT_CSV = "TZPID_WOLFRAM_MODULE_LIBRARY_certified.csv"
DEFAULT_SUMMARY = "wolfram_checks/aa_module_library_certification_summary.json"


def read_csv(path):
    with Path(path).open("r", encoding="utf-8-sig", errors="ignore", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path, rows, fields):
    with Path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def result_key(row):
    return (
        row.get("module_name", ""),
        row.get("module_type", ""),
        row.get("source_report", ""),
        row.get("related_spine", ""),
        row.get("registry_ids_same_report", ""),
    )


def main():
    parser = argparse.ArgumentParser(description="Merge AA Wolfram module certification results back into a CSV copy.")
    parser.add_argument("--library", default=DEFAULT_LIBRARY)
    parser.add_argument("--results", default=DEFAULT_RESULTS)
    parser.add_argument("--output-csv", default=DEFAULT_OUTPUT_CSV)
    parser.add_argument("--summary", default=DEFAULT_SUMMARY)
    args = parser.parse_args()

    library_rows = read_csv(args.library)
    results = json.loads(Path(args.results).read_text(encoding="utf-8"))
    results_by_key = {result_key(row): row for row in results}
    merged = []
    missing_results = []
    for row in library_rows:
        result = results_by_key.get(result_key(row))
        out = dict(row)
        if result:
            out["wolfram_run_status"] = result.get("wolfram_run_status", row.get("wolfram_run_status", ""))
            out["parse_status"] = result.get("parse_status", "")
            out["result_excerpt"] = result.get("result_excerpt", "")
            out["certification_notes"] = result.get("notes", "")
            out["timeout_seconds"] = result.get("timeout_seconds", "")
        else:
            missing_results.append(row.get("module_name", ""))
            out["parse_status"] = "missing_result"
            out["result_excerpt"] = ""
            out["certification_notes"] = "No certification result was returned for this row."
            out["timeout_seconds"] = ""
        merged.append(out)

    fields = list(library_rows[0].keys()) + [
        "parse_status",
        "result_excerpt",
        "certification_notes",
        "timeout_seconds",
    ]
    write_csv(args.output_csv, merged, fields)
    generated_at = generated_utc()
    summary = {
        "provenance": provenance_dict(
            "summarize_aa_module_results.py",
            [str(Path(args.library)), str(Path(args.results))],
            generated_at,
            "Merged AA Wolfram module certification statuses into an auditable CSV copy.",
        ),
        "library_rows": len(library_rows),
        "result_rows": len(results),
        "missing_results": len(missing_results),
        "status_counts": dict(Counter(row.get("wolfram_run_status", "") for row in merged)),
        "parse_status_counts": dict(Counter(row.get("parse_status", "") for row in merged)),
        "related_spine_status_counts": {
            spine: dict(Counter(r.get("wolfram_run_status", "") for r in merged if r.get("related_spine", "") == spine))
            for spine in sorted({row.get("related_spine", "") for row in merged})
        },
        "output_csv": str(Path(args.output_csv).resolve()),
    }
    Path(args.summary).write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
