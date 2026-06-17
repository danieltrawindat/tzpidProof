import argparse
import csv
import hashlib
import json
from pathlib import Path

from tzpid_provenance import (
    CREATOR_NAME,
    CREATOR_ORCID,
    CREATOR_ORCID_URL,
    PROJECT_NAME,
    generated_utc,
    provenance_dict,
)


DEFAULT_ID_SYSTEM = "TZPID_ID_SYSTEM.csv"
DEFAULT_TZPID_ROOT = r"D:\TZPID\TZPID"


def file_sha1(path):
    path = Path(path)
    digest = hashlib.sha1()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_rows(path):
    with Path(path).open("r", encoding="utf-8-sig", errors="ignore", newline="") as handle:
        return list(csv.DictReader(handle))


def parse_float(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def sidecar_record(row, csv_path, csv_sha1, generated_at_utc, sidecar_path):
    tzpid = row["id"]
    sources = [f"{Path(csv_path).resolve()} SHA1 {csv_sha1}"]
    return {
        "schema": {
            "name": "TZPID ID system sidecar",
            "version": "0.1.0",
            "generated_at_utc": generated_at_utc,
            "basis": "TZPID_ID_SYSTEM.csv",
            "basis_sha1": csv_sha1,
            "non_destructive": True,
        },
        "identity": {
            "tzpid": tzpid,
            "title": row.get("title", ""),
            "uuid": row.get("uuid", ""),
        },
        "classification": {
            "loc_class": row.get("loc_class", ""),
            "arxiv_class": row.get("arxiv_class", ""),
        },
        "trawin_geometry": {
            "RTEID": row.get("RTEID", ""),
            "poloidal_theta_rad": row.get("poloidal_theta_rad", ""),
            "toroidal_phi_rad": row.get("toroidal_phi_rad", ""),
            "poloidal_theta_rad_float": parse_float(row.get("poloidal_theta_rad", "")),
            "toroidal_phi_rad_float": parse_float(row.get("toroidal_phi_rad", "")),
            "rteid_source": row.get("rteid_source", ""),
        },
        "pi_identity": {
            "PiID": row.get("PiID", ""),
            "TZPi": row.get("TZPi", ""),
            "PiPE_position": row.get("PiPE_position", ""),
        },
        "raw_csv_row": dict(row),
        "source": {
            "csv": str(Path(csv_path).resolve()).replace("\\", "/"),
            "csv_sha1": csv_sha1,
            "sidecar_path": str(Path(sidecar_path)).replace("\\", "/"),
        },
        "tzpid_provenance": provenance_dict(
            "apply_tzpid_id_system_to_folders.py",
            sources,
            generated_at_utc,
            "Per-ID sidecar generated from TZPID_ID_SYSTEM.csv for folder-local ID-system navigation.",
        ),
    }


def source_truth_link(row, csv_path, csv_sha1, generated_at_utc, sidecar_path):
    return {
        "source": "TZPID_ID_SYSTEM.csv",
        "source_csv": str(Path(csv_path).resolve()).replace("\\", "/"),
        "source_csv_sha1": csv_sha1,
        "sidecar": str(Path(sidecar_path)).replace("\\", "/"),
        "linked_at_utc": generated_at_utc,
        "linked_by": "apply_tzpid_id_system_to_folders.py",
        "uuid": row.get("uuid", ""),
        "RTEID": row.get("RTEID", ""),
        "poloidal_theta_rad": row.get("poloidal_theta_rad", ""),
        "toroidal_phi_rad": row.get("toroidal_phi_rad", ""),
        "rteid_source": row.get("rteid_source", ""),
        "PiID": row.get("PiID", ""),
        "TZPi": row.get("TZPi", ""),
        "PiPE_position": row.get("PiPE_position", ""),
        "loc_class": row.get("loc_class", ""),
        "arxiv_class": row.get("arxiv_class", ""),
    }


def update_source_truth(source_truth_path, row, csv_path, csv_sha1, generated_at_utc, sidecar_path, dry_run):
    path = Path(source_truth_path)
    if not path.exists():
        return {"status": "missing_source_truth"}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return {"status": "error", "error": str(exc)}
    if not isinstance(data, dict):
        return {"status": "skipped", "reason": "top-level JSON is not an object"}

    data["id_system"] = source_truth_link(row, csv_path, csv_sha1, generated_at_utc, sidecar_path)
    identity = data.setdefault("identity", {})
    if isinstance(identity, dict):
        identity.setdefault("uuid", row.get("uuid", ""))
        source_files = identity.setdefault("source_files", {})
        if isinstance(source_files, dict):
            source_files["id_system"] = str(Path(sidecar_path)).replace("\\", "/")

    classification = data.setdefault("classification", {})
    if isinstance(classification, dict):
        if row.get("loc_class", ""):
            classification.setdefault("loc_class", row.get("loc_class", ""))
        if row.get("arxiv_class", ""):
            classification.setdefault("arxiv_class", row.get("arxiv_class", ""))

    if not dry_run:
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return {"status": "linked"}


def apply_id_system(csv_path, root, dry_run=False):
    rows = read_rows(csv_path)
    csv_sha1 = file_sha1(csv_path)
    generated_at_utc = generated_utc()
    root = Path(root)
    results = []
    for row in rows:
        tzpid = row["id"]
        folder = root / tzpid
        sidecar = folder / f"{tzpid}.id_system.json"
        source_truth = folder / f"{tzpid}.source_truth.json"
        if not folder.exists():
            results.append({"id": tzpid, "status": "missing_folder", "path": str(folder)})
            continue
        record = sidecar_record(row, csv_path, csv_sha1, generated_at_utc, sidecar)
        link_result = update_source_truth(source_truth, row, csv_path, csv_sha1, generated_at_utc, sidecar, dry_run)
        if not dry_run:
            sidecar.write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        results.append(
            {
                "id": tzpid,
                "status": "updated" if link_result["status"] == "linked" else link_result["status"],
                "sidecar": str(sidecar).replace("\\", "/"),
                "source_truth_status": link_result["status"],
            }
        )
    return {
        "project": PROJECT_NAME,
        "creator": CREATOR_NAME,
        "creator_orcid": CREATOR_ORCID,
        "creator_orcid_url": CREATOR_ORCID_URL,
        "generated_at_utc": generated_at_utc,
        "dry_run": dry_run,
        "csv": str(Path(csv_path).resolve()).replace("\\", "/"),
        "csv_sha1": csv_sha1,
        "root": str(root).replace("\\", "/"),
        "csv_rows": len(rows),
        "updated": sum(1 for result in results if result["status"] == "updated"),
        "missing_folder": sum(1 for result in results if result["status"] == "missing_folder"),
        "missing_source_truth": sum(1 for result in results if result["source_truth_status"] == "missing_source_truth"),
        "errors": [result for result in results if result["source_truth_status"] == "error"],
        "first_results": results[:10],
        "last_results": results[-10:],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", default=DEFAULT_ID_SYSTEM)
    parser.add_argument("--root", default=DEFAULT_TZPID_ROOT)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--summary", default="tzpid_id_system_apply_summary.json")
    args = parser.parse_args()
    summary = apply_id_system(args.csv, args.root, args.dry_run)
    Path(args.summary).write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
