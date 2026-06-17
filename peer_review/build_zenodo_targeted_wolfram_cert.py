from __future__ import annotations

import csv
import json
import subprocess
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\TZPIDProof")
MATRIX = ROOT / "peer_review" / "coverage" / "ZENODO_27_MAIN_STRUCTURE_COVERAGE_MATRIX.csv"
MASTER_PATHS = [
    ROOT / "TZPID_ALL_IDS_CANONICAL_EQUATION_MASTER_with_export.csv",
    Path(r"D:\00_Engine\AI_Workspaces\OpenAI2\TZPID_ALL_IDS_CANONICAL_EQUATION_MASTER_with_export.csv"),
]
TZP_ID = ROOT / "tzp_id"
OUT_DIR = ROOT / "peer_review" / "coverage" / "zenodo_targeted_wolfram"


def load_master(path: Path) -> tuple[list[str], dict[str, dict[str, str]]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        return list(reader.fieldnames or []), {row["id"]: row for row in rows}


def write_master(path: Path, fieldnames: list[str], rows_by_id: dict[str, dict[str, str]]) -> None:
    # Preserve numeric ID ordering where possible.
    def key(item: tuple[str, dict[str, str]]) -> int:
        id_ = item[0]
        return int(id_[2:]) if id_.startswith("ID") and id_[2:].isdigit() else 10**9

    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for _, row in sorted(rows_by_id.items(), key=key):
            writer.writerow(row)


def source_truth_path(id_: str) -> Path:
    return TZP_ID / id_ / f"{id_}.source_truth.json"


def extract_blocks(id_: str) -> list[dict[str, object]]:
    path = source_truth_path(id_)
    if not path.exists():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    blocks = data.get("wolfram_form", {}).get("audit", {}).get("blocks", [])
    out = []
    for block in blocks:
        wolfram_input = block.get("wolfram_input", "")
        if wolfram_input:
            out.append(
                {
                    "id": id_,
                    "block_index": block.get("block_index", len(out) + 1),
                    "latex": block.get("latex", ""),
                    "wolfram_input": wolfram_input,
                    "source_truth": str(path),
                    "source_method": block.get("parse_method", ""),
                }
            )
    return out


def build_queue(master_rows: dict[str, dict[str, str]]) -> tuple[list[dict[str, object]], dict[str, set[str]]]:
    by_id_papers: dict[str, set[str]] = defaultdict(set)
    with MATRIX.open("r", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            if row["coverage_status"] != "partial_certificate":
                continue
            for id_ in [v.strip() for v in row["ids_cited"].split(";") if v.strip()]:
                status = (master_rows.get(id_, {}).get("wolfram_status", "") or "").strip()
                if status == "" or status.startswith("not_run"):
                    by_id_papers[id_].add(row["paper_key"])

    queue = []
    for id_ in sorted(by_id_papers, key=lambda value: int(value[2:])):
        for block in extract_blocks(id_):
            block["paper_keys"] = sorted(by_id_papers[id_])
            queue.append(block)
    return queue, by_id_papers


def write_runner(queue_path: Path, results_path: Path, runner_path: Path) -> None:
    runner_path.write_text(
        f'''
queue = Import["{str(queue_path).replace("\\", "\\\\")}", "RawJSON"];
verify[item_] := Module[{{expr, status, message = ""}},
  expr = Quiet @ Check[
     TimeConstrained[
       ToExpression[item["wolfram_input"], InputForm, HoldComplete],
       20,
       $TimedOut
     ],
     $Failed
   ];
  status = Which[
    expr === $TimedOut, "timeout",
    expr === $Failed, "parse_error",
    True, "pass"
  ];
  <|
    "id" -> item["id"],
    "block_index" -> item["block_index"],
    "status" -> status,
    "wolfram_input" -> item["wolfram_input"],
    "paper_keys" -> item["paper_keys"],
    "source_method" -> item["source_method"]
  |>
];
results = verify /@ queue;
Export["{str(results_path).replace("\\", "\\\\")}", results, "RawJSON"];
Print["verified ", Length[results], " Wolfram carrier blocks"];
'''.strip(),
        encoding="utf-8",
    )


def run_wolfram(runner_path: Path) -> tuple[int, str]:
    proc = subprocess.run(
        ["wolframscript", "-file", str(runner_path)],
        cwd=str(OUT_DIR),
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=120,
    )
    return proc.returncode, proc.stdout


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    fieldnames, master = load_master(MASTER_PATHS[0])
    queue, by_id_papers = build_queue(master)

    queue_path = OUT_DIR / "zenodo_targeted_wolfram_queue.json"
    results_path = OUT_DIR / "zenodo_targeted_wolfram_results.json"
    runner_path = OUT_DIR / "run_zenodo_targeted_wolfram.wls"
    queue_path.write_text(json.dumps(queue, ensure_ascii=False, indent=2), encoding="utf-8")
    write_runner(queue_path, results_path, runner_path)

    code, output = run_wolfram(runner_path)
    (OUT_DIR / "wolframscript_output.txt").write_text(output, encoding="utf-8")
    if code != 0:
        raise SystemExit(f"wolframscript failed with {code}; see {OUT_DIR / 'wolframscript_output.txt'}")

    results = json.loads(results_path.read_text(encoding="utf-8"))
    by_id_results: dict[str, list[dict[str, object]]] = defaultdict(list)
    for result in results:
        by_id_results[result["id"]].append(result)

    updates: dict[str, str] = {}
    for id_, id_results in by_id_results.items():
        passes = sum(1 for r in id_results if r["status"] == "pass")
        total = len(id_results)
        if passes == total and total > 0:
            updates[id_] = f"{passes}/{total} pass"

    updated_paths = []
    for path in MASTER_PATHS:
        if not path.exists():
            continue
        fields, rows = load_master(path)
        for id_, status in updates.items():
            if id_ in rows:
                rows[id_]["wolfram_status"] = status
        write_master(path, fields, rows)
        updated_paths.append(str(path))

    cert_rows = []
    for id_ in sorted(by_id_papers, key=lambda value: int(value[2:])):
        id_results = by_id_results.get(id_, [])
        passes = sum(1 for r in id_results if r["status"] == "pass")
        total = len(id_results)
        cert_rows.append(
            {
                "id": id_,
                "paper_keys": "; ".join(sorted(by_id_papers[id_])),
                "source_truth_exists": "yes" if source_truth_path(id_).exists() else "no",
                "blocks": str(total),
                "passes": str(passes),
                "status": updates.get(id_, "not_updated"),
            }
        )

    csv_path = OUT_DIR / "ZENODO_TARGETED_WOLFRAM_CERTIFICATE.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(cert_rows[0].keys()) if cert_rows else [])
        writer.writeheader()
        writer.writerows(cert_rows)

    md = []
    md.append("# Zenodo Targeted Wolfram Certificate\n")
    md.append(f"Generated: {datetime.now(timezone.utc).isoformat(timespec='seconds')}\n")
    md.append("## Scope\n")
    md.append("- Target: blank or not-run Wolfram statuses cited by the 11 partial Zenodo main structures.")
    md.append(f"- Target IDs: {len(by_id_papers)}")
    md.append(f"- Wolfram carrier blocks evaluated: {len(results)}")
    md.append(f"- IDs updated in master: {len(updates)}")
    md.append(f"- Master files updated: {', '.join(updated_paths)}")
    md.append("")
    md.append("## Result\n")
    md.append("| ID | Zenodo structures | Blocks | Passes | Folded status |")
    md.append("| --- | --- | ---: | ---: | --- |")
    for row in cert_rows:
        md.append(
            f"| {row['id']} | {row['paper_keys']} | {row['blocks']} | {row['passes']} | {row['status']} |"
        )
    md.append("")
    md.append("## Artifacts\n")
    md.append(f"- Queue: `{queue_path}`")
    md.append(f"- Runner: `{runner_path}`")
    md.append(f"- Raw results: `{results_path}`")
    md.append(f"- CSV certificate: `{csv_path}`")
    md.append(f"- Wolfram output: `{OUT_DIR / 'wolframscript_output.txt'}`")
    (OUT_DIR / "ZENODO_TARGETED_WOLFRAM_CERTIFICATE.md").write_text("\n".join(md), encoding="utf-8")

    print(f"target_ids={len(by_id_papers)} blocks={len(results)} updated={len(updates)}")
    print(f"wrote {OUT_DIR / 'ZENODO_TARGETED_WOLFRAM_CERTIFICATE.md'}")


if __name__ == "__main__":
    main()
