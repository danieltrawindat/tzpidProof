import argparse
import csv
import hashlib
import json
import re
from pathlib import Path

from tzpid_provenance import (
    CREATOR_NAME,
    CREATOR_ORCID,
    CREATOR_ORCID_URL,
    PROJECT_NAME,
    generated_utc,
)


DEFAULT_ENCYCLOPEDIA = "TZPID_ENCYCLOPEDIA.md"
DEFAULT_MASTER = "TZPID_ALL_IDS_CANONICAL_EQUATION_MASTER_with_export.csv"
DEFAULT_TZPID_ROOT = r"D:\TZPID\TZPID"


ENTRY_RE = re.compile(r"(?m)^###\s+(ID\d{4,5})\s+[-\u2013\u2014]\s*(.*?)\s*$")


def file_sha1(path):
    path = Path(path)
    digest = hashlib.sha1()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_master_ids(path):
    with Path(path).open("r", encoding="utf-8-sig", errors="ignore", newline="") as handle:
        return [row["id"] for row in csv.DictReader(handle)]


def split_entries(text):
    matches = list(ENTRY_RE.finditer(text))
    entries = {}
    for index, match in enumerate(matches):
        start = match.start()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        tzpid = match.group(1)
        title = match.group(2).strip()
        body = text[start:end].strip()
        entries[tzpid] = {"title": title, "markdown": body}
    return entries


def front_matter(tzpid, title, encyclopedia_path, encyclopedia_sha, generated_at_utc):
    lines = [
        "---",
        f"tzpid: {tzpid}",
        f"title: {json.dumps(title, ensure_ascii=False)}",
        f"project: {json.dumps(PROJECT_NAME)}",
        f"creator: {json.dumps(CREATOR_NAME)}",
        f"creator_orcid: {CREATOR_ORCID}",
        f"creator_orcid_url: {CREATOR_ORCID_URL}",
        f"generated_at_utc: {generated_at_utc}",
        "generator: split_tzpid_encyclopedia_to_id_folders.py",
        f"source_encyclopedia: {str(Path(encyclopedia_path).resolve()).replace(chr(92), '/')}",
        f"source_encyclopedia_sha1: {encyclopedia_sha}",
        "note: Split from TZPID_ENCYCLOPEDIA.md for local per-ID source-of-truth navigation.",
        "---",
        "",
    ]
    return "\n".join(lines)


def write_entry(root, tzpid, entry, encyclopedia_path, encyclopedia_sha, generated_at_utc, dry_run=False):
    target_dir = Path(root) / tzpid
    target_path = target_dir / f"{tzpid}.encyclopedia.md"
    content = (
        front_matter(tzpid, entry["title"], encyclopedia_path, encyclopedia_sha, generated_at_utc)
        + entry["markdown"].strip()
        + "\n"
    )
    if not dry_run:
        target_dir.mkdir(parents=True, exist_ok=True)
        target_path.write_text(content, encoding="utf-8")
    return {"id": tzpid, "path": str(target_path).replace("\\", "/"), "bytes": len(content.encode("utf-8"))}


def run(encyclopedia_path, master_path, root, dry_run=False):
    text = Path(encyclopedia_path).read_text(encoding="utf-8", errors="ignore")
    entries = split_entries(text)
    master_ids = read_master_ids(master_path)
    encyclopedia_sha = file_sha1(encyclopedia_path)
    generated_at_utc = generated_utc()
    missing_from_encyclopedia = [tzpid for tzpid in master_ids if tzpid not in entries]
    extra_in_encyclopedia = [tzpid for tzpid in entries if tzpid not in set(master_ids)]
    written = []
    if not missing_from_encyclopedia:
        for tzpid in master_ids:
            written.append(
                write_entry(root, tzpid, entries[tzpid], encyclopedia_path, encyclopedia_sha, generated_at_utc, dry_run)
            )
    return {
        "project": PROJECT_NAME,
        "creator": CREATOR_NAME,
        "creator_orcid": CREATOR_ORCID,
        "creator_orcid_url": CREATOR_ORCID_URL,
        "generated_at_utc": generated_at_utc,
        "dry_run": dry_run,
        "root": str(Path(root)).replace("\\", "/"),
        "source_encyclopedia": str(Path(encyclopedia_path).resolve()).replace("\\", "/"),
        "source_encyclopedia_sha1": encyclopedia_sha,
        "master": str(Path(master_path).resolve()).replace("\\", "/"),
        "master_count": len(master_ids),
        "encyclopedia_entry_count": len(entries),
        "missing_from_encyclopedia": missing_from_encyclopedia,
        "extra_in_encyclopedia": extra_in_encyclopedia,
        "written": len(written),
        "first_written": written[:10],
        "last_written": written[-10:],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--encyclopedia", default=DEFAULT_ENCYCLOPEDIA)
    parser.add_argument("--master", default=DEFAULT_MASTER)
    parser.add_argument("--root", default=DEFAULT_TZPID_ROOT)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--summary", default="tzpid_encyclopedia_split_summary.json")
    args = parser.parse_args()
    summary = run(args.encyclopedia, args.master, args.root, args.dry_run)
    Path(args.summary).write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
