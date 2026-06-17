import argparse
import csv
import hashlib
import json
import uuid
from pathlib import Path

from add_tzpid_source_truth_provenance import artifact_manifest, provenance_for
from tzpid_provenance import generated_utc


DEFAULT_MASTER = "TZPID_ALL_IDS_CANONICAL_EQUATION_MASTER_with_export.csv"
DEFAULT_TZPID_ROOT = r"D:\TZPID\TZPID"


def file_sha1(path):
    path = Path(path)
    digest = hashlib.sha1()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_master(path):
    with Path(path).open("r", encoding="utf-8-sig", errors="ignore", newline="") as handle:
        return list(csv.DictReader(handle))


def registry_number(tzpid):
    return "".join(ch for ch in tzpid if ch.isdigit()).lstrip("0") or "0"


def registry_id(tzpid):
    return f"registry_id_{int(registry_number(tzpid)):04d}"


def deterministic_uuid(row):
    if row.get("uuid", "").strip():
        return row["uuid"].strip()
    seed = "|".join(
        [
            row.get("id", ""),
            row.get("title", ""),
            row.get("canonical_statement", ""),
            row.get("canonical_equation", ""),
        ]
    )
    return str(uuid.uuid5(uuid.NAMESPACE_URL, "tzpid-source-truth:" + seed))


def source_section_latex(equation):
    equation = (equation or "").strip()
    if not equation:
        return ""
    return "\\[\n" + equation + "\n\\]"


def source_truth_record(row, master_path, master_sha, generated_at_utc, target_path, artifacts):
    tzpid = row["id"]
    title = row.get("title", "").strip()
    statement = row.get("canonical_statement", "").strip()
    equation = row.get("canonical_equation", "").strip()
    formation_method = row.get("formation_method", "").strip()
    formation_inputs = row.get("formation_inputs", "").strip()
    formation_note = row.get("formation_note", "").strip()
    dictionary = row.get("dictionary", "").strip()
    encyclopedia = row.get("encyclopedia", "").strip()
    target_dir = Path(target_path).parent
    record = {
        "schema": {
            "name": "TZPID source truth generated from canonical equation master",
            "version": "0.3.0",
            "generated_at": generated_at_utc,
            "non_destructive": True,
            "basis": "TZPID_ALL_IDS_CANONICAL_EQUATION_MASTER_with_export.csv",
            "basis_sha1": master_sha,
        },
        "identity": {
            "tzpid": tzpid,
            "uuid": deterministic_uuid(row),
            "registry_id": registry_id(tzpid),
            "canonical_title": title,
            "previous_or_source_id": tzpid,
            "source_files": {
                "master_csv": str(Path(master_path).resolve()).replace("\\", "/"),
                "source_truth": str(Path(target_path)).replace("\\", "/"),
                "planned_tex": str(target_dir / f"{tzpid}.TEX").replace("\\", "/"),
                "planned_json": str(target_dir / f"{tzpid}.JSON").replace("\\", "/"),
            },
        },
        "classification": {
            "source_family": "TZPID_ALL_IDS_CANONICAL_EQUATION_MASTER_with_export",
            "category": "canonical-equation-master-intake",
            "formation_method": formation_method,
        },
        "theory": {
            "canonical_statement": statement,
            "technical_interpretation": encyclopedia or dictionary or statement,
        },
        "canonical_equation": {
            "latex_blocks": [equation] if equation else [],
            "source_section_latex": source_section_latex(equation),
        },
        "equation_progression": [
            {
                "slot": 1,
                "latex": equation,
                "source": "TZPID_ALL_IDS_CANONICAL_EQUATION_MASTER_with_export.csv",
                "source_path": str(Path(master_path).resolve()).replace("\\", "/"),
                "source_sha1": master_sha,
                "status": "canonical_master_source",
            }
        ]
        if equation
        else [],
        "formation": {
            "method": formation_method,
            "inputs": formation_inputs,
            "note": formation_note,
        },
        "source_evidence": {
            "dictionary": dictionary,
            "encyclopedia": encyclopedia,
            "master_csv_sha1": master_sha,
        },
        "symbol_index": {
            "reviewed_source_symbols": [],
            "status": "needs_symbol_extraction_from_canonical_master_entry",
        },
        "publication_overrides": {
            "dictionary_sections": {
                "definition": dictionary or f"{title} is a canonical TZPID registry entry.",
                "contextual_meaning": encyclopedia or statement,
                "formal_statement_latex": equation,
                "technical_interpretation": encyclopedia or statement,
                "equation_grounding": "Equation grounding source: TZPID_ALL_IDS_CANONICAL_EQUATION_MASTER_with_export.csv.",
                "tzp_thesaurus": title,
            },
            "equation_support_summary": "Generated from the canonical equation master and awaiting source-context expansion.",
        },
        "formal_derivations": {
            "isabelle": {"status": "pending_source_truth_formalization"},
            "lean": {"status": "pending_source_truth_formalization"},
            "rocq": {"status": "pending_source_truth_formalization"},
            "wolfram": {"status": "pending_source_truth_symbolic_check"},
        },
        "promotion_status": {
            "status": "source_truth_seeded_from_canonical_master",
            "needs_review": True,
        },
        "proof_support": {
            "status": "pending",
            "note": "Folder and source-truth JSON were created for registry coverage; deeper proof obligations should be generated downstream.",
        },
    }
    record["tzpid_provenance"] = provenance_for(target_path, record, generated_at_utc, artifacts)
    return record


def missing_rows(rows, root):
    root = Path(root)
    existing_folders = {path.name for path in root.glob("ID*") if path.is_dir()}
    return [row for row in rows if row["id"] not in existing_folders]


def create_records(master_path, root, dry_run=False):
    rows = read_master(master_path)
    root = Path(root)
    master_sha = file_sha1(master_path)
    artifacts = artifact_manifest()
    generated_at_utc = generated_utc()
    to_create = missing_rows(rows, root)
    results = []
    for row in to_create:
        tzpid = row["id"]
        target_dir = root / tzpid
        target_path = target_dir / f"{tzpid}.source_truth.json"
        if target_path.exists():
            results.append({"id": tzpid, "status": "skipped", "reason": "source_truth_exists"})
            continue
        record = source_truth_record(row, master_path, master_sha, generated_at_utc, target_path, artifacts)
        if not dry_run:
            target_dir.mkdir(parents=True, exist_ok=True)
            target_path.write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        results.append({"id": tzpid, "status": "created", "path": str(target_path).replace("\\", "/")})
    return {
        "generated_at_utc": generated_at_utc,
        "dry_run": dry_run,
        "root": str(root).replace("\\", "/"),
        "master": str(Path(master_path).resolve()).replace("\\", "/"),
        "master_sha1": master_sha,
        "master_rows": len(rows),
        "missing_folder_count": len(to_create),
        "created": sum(1 for row in results if row["status"] == "created"),
        "skipped": sum(1 for row in results if row["status"] == "skipped"),
        "artifact_count": len(artifacts),
        "first_created": results[:10],
        "last_created": results[-10:],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--master", default=DEFAULT_MASTER)
    parser.add_argument("--root", default=DEFAULT_TZPID_ROOT)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--summary", default="missing_tzpid_source_truth_creation_summary.json")
    args = parser.parse_args()
    summary = create_records(args.master, args.root, dry_run=args.dry_run)
    Path(args.summary).write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
