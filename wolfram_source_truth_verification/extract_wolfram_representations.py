import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\TZPIDProof")
TZP_ID = ROOT / "tzp_id"
OUT_BASE = ROOT / "wolfram_source_truth_verification"


def title_of(obj, fallback):
    return (
        obj.get("title")
        or obj.get("canonical_title")
        or obj.get("identity", {}).get("canonical_title")
        or obj.get("tzpid_provenance", {}).get("canonical_title")
        or fallback
    )


def main():
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    run_dir = OUT_BASE / f"representation_run_{stamp}"
    run_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    coverage = {
        "source_truth_files": 0,
        "ids_with_wolfram_representation": 0,
        "representation_blocks": 0,
        "candidate_blocks": 0,
    }
    for path in sorted(TZP_ID.glob("ID*/ID*.source_truth.json")):
        coverage["source_truth_files"] += 1
        obj = json.loads(path.read_text(encoding="utf-8"))
        tzpid = path.parent.name
        rep = obj.get("wolfram_representation")
        if not isinstance(rep, dict):
            continue
        blocks = rep.get("blocks")
        if not isinstance(blocks, list):
            continue
        clean_blocks = []
        for block in blocks:
            if not isinstance(block, dict):
                continue
            wolfram_input = block.get("wolfram_input")
            if not isinstance(wolfram_input, str) or not wolfram_input.strip():
                continue
            clean_blocks.append(block)
            coverage["representation_blocks"] += 1
            if isinstance(block.get("candidate_wolfram_input"), str) and block["candidate_wolfram_input"].strip():
                coverage["candidate_blocks"] += 1
        if clean_blocks:
            coverage["ids_with_wolfram_representation"] += 1
            rows.append(
                {
                    "id": tzpid,
                    "title": title_of(obj, tzpid),
                    "source_truth_path": str(path),
                    "blocks": clean_blocks,
                }
            )

    (run_dir / "wolfram_representations.json").write_text(
        json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (run_dir / "wolfram_representation_coverage.json").write_text(
        json.dumps(coverage, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(run_dir)


if __name__ == "__main__":
    main()
