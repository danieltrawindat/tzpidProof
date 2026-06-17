import csv
import hashlib
import json
import math
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path
from uuid import NAMESPACE_URL, uuid5


PROOF_ROOT = Path(r"D:\TZPIDProof")
OPENAI2_ROOT = Path(r"D:\00_Engine\AI_Workspaces\OpenAI2")
INTAKE = PROOF_ROOT / "phone2_intake"
THEOREM_DIR = INTAKE / "theorem_toe"

BACKFILL = THEOREM_DIR / "PHONE2_GOLD_ANCHOR_BACKFILL_QUEUE.csv"
ATOMIC_QUEUE_STATUS = INTAKE / "PHONE2_ATOMIC_EQUATION_QUEUE_WITH_MINT_STATUS.csv"

MASTER_NAME = "TZPID_ALL_IDS_CANONICAL_EQUATION_MASTER_with_export.csv"
DICTIONARY_NAME = "TZPID_DICTIONARY.csv"
ENCYCLOPEDIA_NAME = "TZPID_ENCYCLOPEDIA.md"
ID_SYSTEM_NAME = "TZPID_ID_SYSTEM.csv"

BATCH_LABEL = "PHONE2_GOLD_ANCHOR_BATCH2"
BATCH_SIZE = 250
CREATOR = "Daniel Alexander Trawin"
ORCID = "0009-0001-4630-3715"
ORCID_URL = f"https://orcid.org/{ORCID}"

STAMP = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
BACKUP_DIR = THEOREM_DIR / f"gold_anchor_batch2_backup_{STAMP}"
MANIFEST = THEOREM_DIR / f"PHONE2_GOLD_ANCHOR_BATCH2_MINT_MANIFEST_{STAMP}.json"
REPORT = THEOREM_DIR / "PHONE2_GOLD_ANCHOR_BATCH2_MINT_REPORT.md"
MINTED_IDS = THEOREM_DIR / "PHONE2_GOLD_ANCHOR_BATCH2_MINTED_IDS.csv"

MASTER_FIELDS = [
    "id",
    "title",
    "canonical_statement",
    "canonical_equation",
    "formation_method",
    "formation_inputs",
    "formation_note",
    "dictionary",
    "encyclopedia",
    "isabelle_kind",
    "obligation_role",
    "proof_required_checks",
    "gold_spine",
    "lean_rocq",
    "wolfram_status",
    "isabelle_sid",
    "uuid",
]

ID_SYSTEM_FIELDS = [
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


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha1(path: Path) -> str:
    h = hashlib.sha1()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def read_csv(path: Path) -> list[dict]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        writer.writerows([{field: row.get(field, "") for field in fields} for row in rows])


def id_num(tzpid: str) -> int:
    return int(tzpid[2:])


def deterministic_uuid(tzpid: str, row: dict) -> str:
    seed = "|".join([tzpid, row.get("atomic_index", ""), row.get("source_file", ""), row.get("candidate_equation", "")])
    return str(uuid5(NAMESPACE_URL, "tzpid-phone2-gold-anchor-batch2:" + seed))


def title_slug(text: str, limit: int = 54) -> str:
    text = re.sub(r"[_{}\\$`]+", " ", text or "")
    text = re.sub(r"[^A-Za-z0-9α-ωΑ-Ω/+\- ]+", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        return "Equation Candidate"
    return text[:limit].strip().title()


def isabelle_kind(row: dict) -> str:
    title = row.get("anchor_title", "").lower()
    if "lemma" in title:
        return "Lemma"
    if "definition" in title:
        return "Definition"
    if "corollary" in title:
        return "Corollary"
    if "axiom" in title:
        return "Axiom"
    return "Theorem"


def pi_digits(count: int) -> str:
    import mpmath as mp

    mp.mp.dps = count + 20
    return str(mp.pi).replace(".", "")[:count]


def pi_identity(n: int, digits: str) -> tuple[str, str, str]:
    return digits[n : n + 13], digits[n + 6], str(n + 7)


def rte_identity(n: int) -> tuple[str, str, str]:
    phi = (1 + math.sqrt(5)) / 2
    poloidal = n * (2 * math.pi / phi)
    toroidal = (n * (2 * math.pi / 982)) % (2 * math.pi)
    return f"{poloidal:.4f}", f"{toroidal:.4f}", f"RTE:P{poloidal:.4f}:T{toroidal:.4f}"


def backup(paths: list[Path]) -> dict:
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    out = {}
    for path in paths:
        if path.exists():
            target = BACKUP_DIR / (path.parent.name + "__" + path.name)
            shutil.copy2(path, target)
            out[str(path)] = {"backup": str(target), "sha1_before": sha1(path)}
    return out


def selected_backfill_rows() -> list[dict]:
    rows = read_csv(BACKFILL)
    rows = [row for row in rows if row.get("mint_status") != "minted"]
    rows.sort(key=lambda r: (-int(r.get("backfill_priority") or 0), r.get("source_file", ""), int(r.get("line_number") or 0)))
    return rows[:BATCH_SIZE]


def make_master_rows(selected: list[dict], start_num: int) -> tuple[list[dict], list[dict]]:
    new_rows = []
    private = []
    for offset, source in enumerate(selected):
        tzpid = f"ID{start_num + offset:04d}"
        title = f"Phone2 {source.get('anchor_title', 'Gold Anchor')} — {title_slug(source.get('candidate_equation', ''))}"
        uuid = deterministic_uuid(tzpid, source)
        equation = source.get("candidate_equation", "")
        source_line = f"{source.get('source_file')} line {source.get('line_number')}"
        anchor_label = f"{source.get('anchor_id')} {source.get('anchor_title')}"
        statement = (
            f"Phone2 gold-anchor equation supporting {anchor_label}, extracted from {source_line}, "
            f"with canonical equation ${equation}$."
        )
        dictionary = (
            f"Phone2 equation candidate selected from the gold-anchor backfill queue for {anchor_label}. "
            f"Source: {source_line}."
        )
        encyclopedia = (
            f"{tzpid} supports theorem anchor {anchor_label}. "
            f"The equation was selected from the Phone2 gold-anchor backfill queue using {source.get('mapping_method')} "
            f"against source {source_line}. Equation grounding: {equation}"
        )
        row = {
            "id": tzpid,
            "title": title,
            "canonical_statement": statement,
            "canonical_equation": equation,
            "formation_method": "Phone2 theorem-anchor backfill extraction",
            "formation_inputs": source_line,
            "formation_note": (
                f"Minted from {BATCH_LABEL}; atomic_index={source.get('atomic_index')}; "
                f"anchor={anchor_label}; domain={source.get('domain_family')}; mapping={source.get('mapping_method')}."
            ),
            "dictionary": dictionary,
            "encyclopedia": encyclopedia,
            "isabelle_kind": isabelle_kind(source),
            "obligation_role": "Phone2_Gold_Anchor_Backfill",
            "proof_required_checks": "source_truth_json;theorem_anchor_mapping;wolfram_form_check;semantic_grounding",
            "gold_spine": "phone2_theorem_anchor_backfill",
            "lean_rocq": "export_pending",
            "wolfram_status": "needs_wolfram_equation_specific_parse",
            "isabelle_sid": f"registry_{tzpid}",
            "uuid": uuid,
        }
        row_private = dict(row)
        row_private.update({f"_{k}": v for k, v in source.items()})
        new_rows.append(row)
        private.append(row_private)
    return new_rows, private


def append_master(root: Path, rows: list[dict]) -> None:
    path = root / MASTER_NAME
    existing = read_csv(path)
    ids = {row["id"] for row in existing}
    collisions = [row["id"] for row in rows if row["id"] in ids]
    if collisions:
        raise RuntimeError(f"ID collisions in {path}: {collisions[:5]}")
    existing.extend(rows)
    write_csv(path, existing, MASTER_FIELDS)


def append_dictionary(root: Path, rows: list[dict]) -> None:
    path = root / DICTIONARY_NAME
    if not path.exists():
        return
    existing = read_csv(path)
    existing.extend({"id": row["id"], "title": row["title"], "dictionary_definition": row["dictionary"]} for row in rows)
    write_csv(path, existing, ["id", "title", "dictionary_definition"])


def append_encyclopedia(root: Path, rows: list[dict]) -> None:
    path = root / ENCYCLOPEDIA_NAME
    if not path.exists():
        return
    with path.open("a", encoding="utf-8") as handle:
        handle.write("\n\n---\n\n# Phone2 Gold Anchor Batch 2 Addendum\n\n")
        for row in rows:
            handle.write(f"### {row['id']} — {row['title']}\n\n")
            handle.write(f"$$ {row['canonical_equation']} $$\n\n")
            handle.write(row["encyclopedia"] + "\n\n")


def append_master_md(root: Path, rows: list[dict]) -> None:
    path = root / "TZPID_ALL_IDS_CANONICAL_EQUATION_MASTER_with_export.md"
    if not path.exists():
        return
    with path.open("a", encoding="utf-8") as handle:
        handle.write("\n\n---\n\n# Phone2 Gold Anchor Batch 2 Master Addendum\n\n")
        for row in rows:
            handle.write(f"## {row['id']} — {row['title']}\n\n")
            handle.write(f"- Equation: `{row['canonical_equation']}`\n")
            handle.write(f"- Source: `{row['formation_inputs']}`\n")
            handle.write(f"- Wolfram status: `{row['wolfram_status']}`\n\n")


def append_id_system(root: Path, rows: list[dict]) -> list[dict]:
    path = root / ID_SYSTEM_NAME
    if not path.exists():
        return []
    existing = read_csv(path)
    ids = {row["id"] for row in existing}
    max_id = max(id_num(row["id"]) for row in rows)
    digits = pi_digits(max_id + 30)
    additions = []
    for row in rows:
        if row["id"] in ids:
            continue
        n = id_num(row["id"])
        poloidal, toroidal, rteid = rte_identity(n)
        piid, tzpi, pipe = pi_identity(n, digits)
        additions.append(
            {
                "id": row["id"],
                "title": row["title"],
                "uuid": row["uuid"],
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
        )
    existing.extend(additions)
    write_csv(path, existing, ID_SYSTEM_FIELDS)
    return additions


def write_source_truth(rows_private: list[dict], id_system_rows: list[dict]) -> None:
    id_system = {row["id"]: row for row in id_system_rows}
    for row in rows_private:
        tzpid = row["id"]
        folder = PROOF_ROOT / "tzp_id" / tzpid
        folder.mkdir(parents=True, exist_ok=True)
        sidecar = id_system.get(tzpid, {})
        source_truth = {
            "schema": {
                "name": "TZPID Phone2 gold-anchor batch source truth",
                "version": "0.1.0",
                "generated_at": now_utc(),
                "basis": "PHONE2_GOLD_ANCHOR_BACKFILL_QUEUE.csv",
                "basis_sha1": sha1(BACKFILL),
            },
            "identity": {
                "tzpid": tzpid,
                "uuid": row["uuid"],
                "registry_id": row["isabelle_sid"],
                "canonical_title": row["title"],
            },
            "classification": {
                "source_family": "Phone2",
                "category": "phone2-gold-anchor-backfill",
                "isabelle_kind": row["isabelle_kind"],
                "gold_spine": row["gold_spine"],
            },
            "theorem_anchor": {
                "anchor_id": row.get("_anchor_id", ""),
                "anchor_title": row.get("_anchor_title", ""),
                "anchor_source_file": row.get("_anchor_source_file", ""),
                "anchor_line_number": row.get("_anchor_line_number", ""),
                "mapping_method": row.get("_mapping_method", ""),
                "line_distance": row.get("_line_distance", ""),
            },
            "theory": {
                "canonical_statement": row["canonical_statement"],
                "technical_interpretation": row["encyclopedia"],
            },
            "canonical_equation": {
                "latex_blocks": [row["canonical_equation"]],
                "source_section_latex": "\\[\n" + row["canonical_equation"] + "\n\\]",
                "wolfram_form_hint": row.get("_wolfram_form_hint", ""),
            },
            "formation": {
                "method": row["formation_method"],
                "inputs": row["formation_inputs"],
                "note": row["formation_note"],
            },
            "source_evidence": {
                "dictionary": row["dictionary"],
                "encyclopedia": row["encyclopedia"],
                "source_file": row.get("_source_file", ""),
                "line_number": row.get("_line_number", ""),
                "phone2_backfill_queue_sha1": sha1(BACKFILL),
            },
            "formal_derivations": {
                "isabelle": {"status": "pending_phone2_anchor_semantic_translation"},
                "wolfram": {"status": row["wolfram_status"]},
                "lean": {"status": "pending_export"},
                "rocq": {"status": "pending_export"},
            },
            "promotion_status": {
                "status": "minted_from_phone2_gold_anchor_batch2",
                "needs_review": True,
            },
            "tzpid_id_system": sidecar,
            "tzpid_provenance": {
                "project": "TZPID Proof Pipeline",
                "creator": CREATOR,
                "creator_orcid": ORCID,
                "creator_orcid_url": ORCID_URL,
                "generator": "mint_phone2_gold_anchor_batch2.py",
                "generated_at_utc": now_utc(),
                "source_tag": "PHONE2",
            },
        }
        (folder / f"{tzpid}.source_truth.json").write_text(json.dumps(source_truth, indent=2, ensure_ascii=False), encoding="utf-8")
        (folder / f"{tzpid}.metadata.json").write_text(
            json.dumps(
                {
                    "tzpid": tzpid,
                    "title": row["title"],
                    "uuid": row["uuid"],
                    "PiID": sidecar.get("PiID", ""),
                    "RTEID": sidecar.get("RTEID", ""),
                    "creator": CREATOR,
                    "creator_orcid": ORCID_URL,
                    "embedded_at_utc": now_utc(),
                    "source_tag": "PHONE2",
                    "theorem_anchor": row.get("_anchor_id", ""),
                },
                indent=2,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        (folder / f"{tzpid}.tex").write_text(
            "\\documentclass[11pt]{article}\n"
            "\\usepackage{amsmath,amssymb,hyperref}\n"
            "\\hypersetup{pdfauthor={Daniel Alexander Trawin},pdfcreator={Trawin, Daniel Alexander},colorlinks=false}\n"
            f"\\title{{{row['title']}}}\n"
            f"\\author{{{CREATOR}}}\n"
            f"\\date{{{now_utc()}}}\n"
            "\\begin{document}\n\\maketitle\n"
            "\\section*{Theorem Anchor}\n"
            f"{row.get('_anchor_id', '')}: {row.get('_anchor_title', '')}\n"
            "\\section*{Canonical Equation}\n\\[\n"
            f"{row['canonical_equation']}\n"
            "\\]\n\\section*{Interpretation}\n"
            f"{row['encyclopedia']}\n"
            "\\end{document}\n",
            encoding="utf-8",
        )


def update_queue_status(rows_private: list[dict]) -> None:
    queue_rows = read_csv(ATOMIC_QUEUE_STATUS)
    by_atomic = {row.get("_atomic_index"): row["id"] for row in rows_private}
    for row in queue_rows:
        atomic = row.get("atomic_index")
        if atomic in by_atomic:
            row["mint_status"] = "minted"
            row["minted_id"] = by_atomic[atomic]
            row["mint_batch"] = BATCH_LABEL
    fields = list(queue_rows[0].keys())
    write_csv(ATOMIC_QUEUE_STATUS, queue_rows, fields)


def main() -> None:
    selected = selected_backfill_rows()
    if len(selected) != BATCH_SIZE:
        raise RuntimeError(f"Expected {BATCH_SIZE} rows, got {len(selected)}")
    proof_master = PROOF_ROOT / MASTER_NAME
    existing = read_csv(proof_master)
    start_num = max(id_num(row["id"]) for row in existing) + 1
    new_rows, private_rows = make_master_rows(selected, start_num)

    tracked = []
    for root in (PROOF_ROOT, OPENAI2_ROOT):
        for name in (MASTER_NAME, DICTIONARY_NAME, ENCYCLOPEDIA_NAME, ID_SYSTEM_NAME):
            path = root / name
            if path.exists():
                tracked.append(path)
    backups = backup(tracked)

    for root in (PROOF_ROOT, OPENAI2_ROOT):
        append_master(root, new_rows)
        append_dictionary(root, new_rows)
        append_encyclopedia(root, new_rows)
        append_master_md(root, new_rows)

    id_rows = append_id_system(PROOF_ROOT, new_rows)
    append_id_system(OPENAI2_ROOT, new_rows)
    write_source_truth(private_rows, id_rows)
    update_queue_status(private_rows)

    with MINTED_IDS.open("w", encoding="utf-8", newline="") as handle:
        fields = ["minted_id", "atomic_index", "anchor_id", "anchor_title", "source_file", "line_number", "candidate_equation"]
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in private_rows:
            writer.writerow(
                {
                    "minted_id": row["id"],
                    "atomic_index": row.get("_atomic_index", ""),
                    "anchor_id": row.get("_anchor_id", ""),
                    "anchor_title": row.get("_anchor_title", ""),
                    "source_file": row.get("_source_file", ""),
                    "line_number": row.get("_line_number", ""),
                    "candidate_equation": row["canonical_equation"],
                }
            )

    manifest = {
        "generated_at_utc": now_utc(),
        "batch": BATCH_LABEL,
        "count": len(new_rows),
        "first_id": new_rows[0]["id"],
        "last_id": new_rows[-1]["id"],
        "source_queue": str(BACKFILL),
        "backup_dir": str(BACKUP_DIR),
        "backups": backups,
        "roots_updated": [str(PROOF_ROOT), str(OPENAI2_ROOT)],
        "ids": [row["id"] for row in new_rows],
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    REPORT.write_text(
        "\n".join(
            [
                "# Phone2 Gold Anchor Batch 2 Mint Report",
                "",
                f"- Generated UTC: `{manifest['generated_at_utc']}`",
                f"- New IDs minted: `{len(new_rows)}`",
                f"- ID range: `{new_rows[0]['id']}` to `{new_rows[-1]['id']}`",
                f"- Backup directory: `{BACKUP_DIR}`",
                "- Source queue: `PHONE2_GOLD_ANCHOR_BACKFILL_QUEUE.csv`",
                "",
                "## Status",
                "",
                "Batch 2 was minted from the theorem/ToE gold-anchor backfill queue. Rows are anchor-aware staged equations and require equation-specific Wolfram certification next.",
                "",
                f"- Manifest: `{MANIFEST}`",
                f"- Minted IDs CSV: `{MINTED_IDS}`",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    print(json.dumps({k: manifest[k] for k in ("count", "first_id", "last_id", "backup_dir")}, indent=2))


if __name__ == "__main__":
    main()
