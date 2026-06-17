import csv
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from uuid import NAMESPACE_URL, uuid5

import mpmath as mp


ROOT = Path(r"D:\TZPIDProof")
MASTER = ROOT / "TZPID_ALL_IDS_CANONICAL_EQUATION_MASTER_with_export.csv"
ID_SYSTEM = ROOT / "TZPID_ID_SYSTEM.csv"
BACKUP_DIR = ROOT / "sync_backup_20260610_221012"
REPORT = ROOT / "TZPID_ID_SYSTEM_EXTENSION_REPORT.json"

FIELDS = [
    "id",
    "title",
    "uuid",
    "loc_class",
    "arxiv_class",
    "RTEID",
    "poloidal_theta_rad",
    "toroidal_phi_rad",
    "rteid_source",
    "PiID",
    "TZPi",
    "PiPE_position",
]


def read_csv(path):
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def id_num(tzpid):
    return int(tzpid[2:])


def pi_digits(count):
    mp.mp.dps = count + 20
    return str(mp.pi).replace(".", "")[:count]


def pi_identity(n, digits):
    start = n
    end = start + 13
    if end > len(digits):
        raise ValueError("not enough pi digits")
    return digits[start:end], digits[start + 6], str(n + 7)


def rte_identity(n):
    phi = (1 + math.sqrt(5)) / 2
    poloidal = n * (2 * math.pi / phi)
    toroidal = (n * (2 * math.pi / 982)) % (2 * math.pi)
    return f"{poloidal:.4f}", f"{toroidal:.4f}", f"RTE:P{poloidal:.4f}:T{toroidal:.4f}"


def deterministic_uuid(row):
    existing = (row.get("uuid") or "").strip()
    if existing:
        return existing
    seed = "|".join(
        [
            row.get("id", ""),
            row.get("title", ""),
            row.get("canonical_statement", ""),
            row.get("canonical_equation", ""),
        ]
    )
    return str(uuid5(NAMESPACE_URL, "tzpid-source-truth:" + seed))


def build_row(master_row, existing=None, digits=None):
    tzpid = master_row["id"]
    n = id_num(tzpid)
    if existing:
        row = {field: existing.get(field, "") for field in FIELDS}
        row["title"] = master_row.get("title") or row.get("title", "")
        row["uuid"] = master_row.get("uuid") or row.get("uuid", "")
        return row
    piid, tzpi, pipe = pi_identity(n, digits)
    poloidal, toroidal, rteid = rte_identity(n)
    return {
        "id": tzpid,
        "title": master_row.get("title", ""),
        "uuid": deterministic_uuid(master_row),
        "loc_class": "",
        "arxiv_class": "",
        "RTEID": rteid,
        "poloidal_theta_rad": poloidal,
        "toroidal_phi_rad": toroidal,
        "rteid_source": "computed",
        "PiID": piid,
        "TZPi": tzpi,
        "PiPE_position": pipe,
    }


def main():
    stamp = datetime.now(timezone.utc).isoformat()
    if ID_SYSTEM.exists():
        BACKUP_DIR.mkdir(parents=True, exist_ok=True)
        backup = BACKUP_DIR / "TZPID_ID_SYSTEM.before_extension.csv"
        if not backup.exists():
            backup.write_bytes(ID_SYSTEM.read_bytes())

    master_rows = read_csv(MASTER)
    existing_rows = read_csv(ID_SYSTEM) if ID_SYSTEM.exists() else []
    existing_by_id = {row["id"]: row for row in existing_rows if row.get("id")}
    max_id = max(id_num(row["id"]) for row in master_rows)
    digits = pi_digits(max_id + 20)

    out_rows = []
    added = []
    preserved = []
    for master_row in master_rows:
        tzpid = master_row["id"]
        if tzpid in existing_by_id:
            out_rows.append(build_row(master_row, existing_by_id[tzpid], digits))
            preserved.append(tzpid)
        else:
            out_rows.append(build_row(master_row, None, digits))
            added.append(tzpid)

    with ID_SYSTEM.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        writer.writerows(out_rows)

    report = {
        "generated_utc": stamp,
        "master_rows": len(master_rows),
        "previous_id_system_rows": len(existing_rows),
        "new_id_system_rows": len(out_rows),
        "preserved_rows": len(preserved),
        "added_rows": len(added),
        "added_first": added[:20],
        "added_last": added[-20:],
        "max_id": f"ID{max_id:04d}",
        "backup": str(BACKUP_DIR / "TZPID_ID_SYSTEM.before_extension.csv"),
    }
    REPORT.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
