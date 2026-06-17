import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\TZPIDProof")
TZP_ID = ROOT / "tzp_id"
OUT_BASE = ROOT / "wolfram_source_truth_verification"


def iter_source_truth_files():
    yield from sorted(TZP_ID.glob("ID*/ID*.source_truth.json"))


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def get_blocks(obj):
    wolfram_form = obj.get("wolfram_form")
    if not isinstance(wolfram_form, dict):
        return []
    audit = wolfram_form.get("audit")
    if not isinstance(audit, dict):
        return []
    blocks = audit.get("blocks")
    if not isinstance(blocks, list):
        return []
    clean = []
    for index, block in enumerate(blocks, start=1):
        if not isinstance(block, dict):
            continue
        text = block.get("wolfram_input")
        source_field = "wolfram_input"
        if not isinstance(text, str) or not text.strip():
            text = block.get("holdform_inputform")
            source_field = "holdform_inputform"
        if not isinstance(text, str) or not text.strip():
            continue
        clean.append(
            {
                "block_index": index,
                "wolfram_input": text.strip(),
                "source_field": source_field,
                "latex": block.get("latex"),
                "normalized_latex": block.get("normalized_latex"),
            }
        )
    return clean


def main():
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    run_dir = OUT_BASE / f"run_{stamp}"
    run_dir.mkdir(parents=True, exist_ok=True)

    rows = []
    coverage = {
        "source_truth_files": 0,
        "ids_with_wolfram_form": 0,
        "ids_with_wolfram_input_blocks": 0,
        "wolfram_input_blocks": 0,
    }

    for path in iter_source_truth_files():
        coverage["source_truth_files"] += 1
        obj = load_json(path)
        tzpid = obj.get("id") or obj.get("tzpid") or path.parent.name
        title = (
            obj.get("title")
            or obj.get("canonical_title")
            or obj.get("identity", {}).get("canonical_title")
            or obj.get("tzpid_provenance", {}).get("canonical_title")
            or ""
        )
        if isinstance(obj.get("wolfram_form"), dict):
            coverage["ids_with_wolfram_form"] += 1
        blocks = get_blocks(obj)
        if blocks:
            coverage["ids_with_wolfram_input_blocks"] += 1
            coverage["wolfram_input_blocks"] += len(blocks)
            rows.append(
                {
                    "id": tzpid,
                    "title": title,
                    "source_truth_path": str(path),
                    "blocks": blocks,
                }
            )

    (run_dir / "source_truth_wolfram_blocks.json").write_text(
        json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (run_dir / "source_truth_wolfram_coverage.json").write_text(
        json.dumps(coverage, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    md = [
        "# TZPID Source-Truth Wolfram Form Extraction",
        "",
        f"- Extracted at UTC: `{stamp}`",
        f"- Source-truth JSON files scanned: `{coverage['source_truth_files']}`",
        f"- IDs with `wolfram_form`: `{coverage['ids_with_wolfram_form']}`",
        f"- IDs with executable Wolfram blocks: `{coverage['ids_with_wolfram_input_blocks']}`",
        f"- Total Wolfram blocks: `{coverage['wolfram_input_blocks']}`",
        "",
        "This lane uses the per-entry source-truth Wolfram forms, not the raw LaTeX equation text.",
    ]
    (run_dir / "SOURCE_TRUTH_WOLFRAM_EXTRACTION_SUMMARY.md").write_text(
        "\n".join(md) + "\n", encoding="utf-8"
    )
    print(run_dir)


if __name__ == "__main__":
    main()
