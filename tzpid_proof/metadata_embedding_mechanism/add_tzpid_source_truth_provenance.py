import argparse
import hashlib
import json
from pathlib import Path

from tzpid_provenance import (
    CREATOR_NAME,
    CREATOR_ORCID,
    CREATOR_ORCID_URL,
    PROJECT_NAME,
    generated_utc,
)


DEFAULT_TZPID_ROOT = r"D:\TZPID\TZPID"

PROOF_ARTIFACTS = [
    r"D:\tzpidNEW\README_PROOF_PIPELINE.md",
    r"D:\tzpidNEW\TZPID_NEW_SPINES_obligations.csv",
    r"D:\tzpidNEW\TZPID_ZENODO_SPINES_obligations.csv",
    r"D:\tzpidNEW\isabelle_tzpid\ROOT",
    r"D:\tzpidNEW\isabelle_tzpid\TZPID_Gravity_Focus.thy",
    r"D:\tzpidNEW\isabelle_tzpid\TZPID_EnergyMatter_Focus.thy",
    r"D:\tzpidNEW\isabelle_tzpid\TZPID_TopologicalUnification_Focus.thy",
    r"D:\tzpidNEW\isabelle_tzpid\TZPID_NewSpines_Computational_Checks.thy",
    r"D:\tzpidNEW\isabelle_tzpid\TZPID_ZenodoSpines_Focus.thy",
    r"D:\tzpidNEW\isabelle_tzpid\TZPID_ZenodoSpines_Computational_Checks.thy",
    r"D:\tzpidNEW\isabelle_tzpid\zenodo_spines_focus_summary.json",
    r"D:\tzpidNEW\isabelle_tzpid\zenodo_spines_wolfram_certificate_summary.md",
    r"D:\tzpidNEW\wolfram_checks\zenodo_spines_results.json",
    r"D:\tzpidNEW\lean_rocq_gold_spine\TZPIDAllIDs.lean",
    r"D:\tzpidNEW\lean_rocq_gold_spine\TZPIDAllIDs.v",
    r"D:\tzpidNEW\lean_rocq_gold_spine\all_ids_export_summary.json",
]


def file_sha1(path):
    path = Path(path)
    digest = hashlib.sha1()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def artifact_manifest():
    artifacts = []
    for raw_path in PROOF_ARTIFACTS:
        path = Path(raw_path)
        if path.exists():
            artifacts.append(
                {
                    "path": str(path).replace("\\", "/"),
                    "sha1": file_sha1(path),
                    "bytes": path.stat().st_size,
                }
            )
    return artifacts


def entry_id_from_path(path):
    name = Path(path).name
    return name.split(".")[0]


def provenance_for(path, data, generated_at_utc, artifacts):
    entry_id = entry_id_from_path(path)
    identity = data.get("identity", {}) if isinstance(data, dict) else {}
    return {
        "project": PROJECT_NAME,
        "creator": CREATOR_NAME,
        "creator_orcid": CREATOR_ORCID,
        "creator_orcid_url": CREATOR_ORCID_URL,
        "provenance_applied_at_utc": generated_at_utc,
        "provenance_applied_by": "add_tzpid_source_truth_provenance.py",
        "source_truth_file": str(Path(path)).replace("\\", "/"),
        "entry_id": identity.get("tzpid") or entry_id,
        "registry_id": identity.get("registry_id", ""),
        "canonical_title": identity.get("canonical_title", ""),
        "proof_pipeline": {
            "workspace": "D:/tzpidNEW",
            "status": "source-truth provenance linked to generated proof-obligation and certificate artifacts",
            "scope_note": "This metadata records authorship, lineage, and proof-pipeline artifact links. It does not by itself assert that the entry has a completed native analytic proof.",
            "formal_systems": ["Isabelle/HOL", "Lean", "Rocq/Coq", "Wolfram"],
            "verification_summary": {
                "isabelle_tzpid_session": "passed after provenance regeneration",
                "lean_all_ids_mirror": "passed after provenance regeneration",
                "rocq_all_ids_mirror": "passed after provenance regeneration",
                "wolfram_spine_checks": "passed for generated curated/Zenodo spine checks; energy-matter naive integral divergence warning is expected",
            },
            "artifacts": artifacts,
        },
    }


def source_truth_paths(root):
    return sorted(Path(root).glob("ID*/ID*.source_truth.json"))


def update_file(path, generated_at_utc, artifacts, dry_run=False):
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except Exception as exc:
        return {"path": str(path), "status": "error", "error": f"read/parse failed: {exc}"}

    if not isinstance(data, dict):
        return {"path": str(path), "status": "skipped", "reason": "top-level JSON is not an object"}

    data["tzpid_provenance"] = provenance_for(path, data, generated_at_utc, artifacts)
    if not dry_run:
        Path(path).write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return {"path": str(path), "status": "updated", "entry_id": data["tzpid_provenance"]["entry_id"]}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=DEFAULT_TZPID_ROOT)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--summary", default="tzpid_source_truth_provenance_update_summary.json")
    args = parser.parse_args()

    generated_at_utc = generated_utc()
    artifacts = artifact_manifest()
    paths = source_truth_paths(args.root)
    results = [update_file(path, generated_at_utc, artifacts, dry_run=args.dry_run) for path in paths]
    summary = {
        "project": PROJECT_NAME,
        "creator": CREATOR_NAME,
        "creator_orcid": CREATOR_ORCID,
        "creator_orcid_url": CREATOR_ORCID_URL,
        "generated_at_utc": generated_at_utc,
        "dry_run": args.dry_run,
        "root": str(Path(args.root)).replace("\\", "/"),
        "artifact_count": len(artifacts),
        "source_truth_files_seen": len(paths),
        "updated": sum(1 for row in results if row["status"] == "updated"),
        "skipped": sum(1 for row in results if row["status"] == "skipped"),
        "errors": [row for row in results if row["status"] == "error"],
        "sample_results": results[:10],
    }
    Path(args.summary).write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
