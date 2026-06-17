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

ATOMIC_QUEUE = INTAKE / "PHONE2_ATOMIC_EQUATION_QUEUE.csv"
ATOMIC_BATCHES = INTAKE / "PHONE2_ATOMIC_REGISTRATION_BATCHES.csv"

MASTER_NAME = "TZPID_ALL_IDS_CANONICAL_EQUATION_MASTER_with_export.csv"
DICTIONARY_NAME = "TZPID_DICTIONARY.csv"
ENCYCLOPEDIA_NAME = "TZPID_ENCYCLOPEDIA.md"
ID_SYSTEM_NAME = "TZPID_ID_SYSTEM.csv"

BATCH_SIZE = 250
CREATOR = "Daniel Alexander Trawin"
ORCID = "0009-0001-4630-3715"
ORCID_URL = f"https://orcid.org/{ORCID}"


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


STAMP = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
BACKUP_DIR = INTAKE / f"batch1_backup_{STAMP}"
MANIFEST = INTAKE / f"PHONE2_BATCH1_MINT_MANIFEST_{STAMP}.json"
REPORT = INTAKE / "PHONE2_BATCH1_MINT_REPORT.md"


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


def sha1(path: Path) -> str:
    h = hashlib.sha1()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
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


def title_case_slug(text: str, limit: int = 74) -> str:
    text = re.sub(r"[_{}\\$`]+", " ", text or "")
    text = re.sub(r"[^A-Za-z0-9 GreekA-Za-zα-ωΑ-Ω/+\- ]+", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        return "Phone2 Extracted Equation"
    words = text.split()
    out = []
    for word in words:
        out.append(word if any(ch.isupper() for ch in word[1:]) else word[:1].upper() + word[1:])
        if len(" ".join(out)) >= limit:
            break
    return " ".join(out)[:limit].strip()


def statement_for(row: dict) -> str:
    domain = row.get("domain_family", "general_math").replace("_", " ")
    semantic = row.get("semantic_kind", "") or "equation"
    return (
        f"Phone2 {semantic.lower()} candidate in the {domain} family, extracted from "
        f"{row.get('source_file')} line {row.get('line_number')}, with canonical equation "
        f"${row.get('atomic_equation', '')}$."
    )


def dictionary_for(row: dict) -> str:
    domain = row.get("domain_family", "general_math").replace("_", " ")
    return (
        f"Phone2 extracted {domain} equation candidate from {row.get('source_file')} "
        f"line {row.get('line_number')}. Staged from the Phone2 atomic extraction batch."
    )


def encyclopedia_for(row: dict, tzpid: str) -> str:
    context = row.get("semantic_context", "")
    equation = row.get("atomic_equation", "")
    domain = row.get("domain_family", "general_math").replace("_", " ")
    parts = [
        f"{tzpid} records a Phone2 corpus equation in the {domain} family.",
        f"The equation was atomized from {row.get('source_file')} line {row.get('line_number')}.",
    ]
    if context:
        parts.append(f"Nearest semantic context: {context}")
    parts.append(f"Equation grounding: {equation}")
    return " ".join(parts)


def isabelle_kind(row: dict) -> str:
    kind = (row.get("semantic_kind") or "").lower()
    if kind in {"theorem", "lemma", "corollary", "axiom", "definition"}:
        return kind.title()
    return "Equation"


def deterministic_uuid(tzpid: str, row: dict) -> str:
    seed = "|".join(
        [
            tzpid,
            row.get("source_file", ""),
            str(row.get("line_number", "")),
            row.get("atomic_equation", ""),
        ]
    )
    return str(uuid5(NAMESPACE_URL, "tzpid-phone2-batch1:" + seed))


def pi_digits(count: int) -> str:
    # Chudnovsky is overkill; mpmath is available in this environment from the existing pipeline.
    import mpmath as mp

    mp.mp.dps = count + 20
    return str(mp.pi).replace(".", "")[:count]


def pi_identity(n: int, digits: str) -> tuple[str, str, str]:
    piid = digits[n : n + 13]
    return piid, digits[n + 6], str(n + 7)


def rte_identity(n: int) -> tuple[str, str, str]:
    phi = (1 + math.sqrt(5)) / 2
    poloidal = n * (2 * math.pi / phi)
    toroidal = (n * (2 * math.pi / 982)) % (2 * math.pi)
    return f"{poloidal:.4f}", f"{toroidal:.4f}", f"RTE:P{poloidal:.4f}:T{toroidal:.4f}"


def load_batch_rows() -> list[dict]:
    queue = {row["atomic_index"]: row for row in read_csv(ATOMIC_QUEUE)}
    batch_rows = [
        row for row in read_csv(ATOMIC_BATCHES) if row.get("batch") == "1" and row.get("readiness") == "id_ready"
    ]
    batch_rows = sorted(batch_rows, key=lambda r: int(r["batch_position"]))[:BATCH_SIZE]
    return [queue[row["atomic_index"]] for row in batch_rows]


def backup(paths: list[Path]) -> dict:
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    out = {}
    for path in paths:
        if path.exists():
            target = BACKUP_DIR / (path.parent.name + "__" + path.name)
            shutil.copy2(path, target)
            out[str(path)] = {"backup": str(target), "sha1_before": sha1(path)}
    return out


def append_master(root: Path, new_rows: list[dict]) -> None:
    path = root / MASTER_NAME
    rows = read_csv(path)
    existing = {row["id"] for row in rows}
    collisions = [row["id"] for row in new_rows if row["id"] in existing]
    if collisions:
        raise RuntimeError(f"ID collisions in {path}: {collisions[:10]}")
    rows.extend(new_rows)
    write_csv(path, rows, MASTER_FIELDS)


def append_dictionary(root: Path, new_rows: list[dict]) -> None:
    path = root / DICTIONARY_NAME
    if not path.exists():
        return
    rows = read_csv(path)
    rows.extend(
        {
            "id": row["id"],
            "title": row["title"],
            "dictionary_definition": row["dictionary"],
        }
        for row in new_rows
    )
    write_csv(path, rows, ["id", "title", "dictionary_definition"])


def append_encyclopedia(root: Path, new_rows: list[dict]) -> None:
    path = root / ENCYCLOPEDIA_NAME
    if not path.exists():
        return
    with path.open("a", encoding="utf-8") as handle:
        handle.write("\n\n---\n\n# Phone2 Batch 1 Addendum\n\n")
        for row in new_rows:
            handle.write(f"### {row['id']} — {row['title']}\n\n")
            handle.write(f"$$ {row['canonical_equation']} $$\n\n")
            handle.write(row["encyclopedia"] + "\n\n")


def append_master_md(root: Path, new_rows: list[dict]) -> None:
    path = root / "TZPID_ALL_IDS_CANONICAL_EQUATION_MASTER_with_export.md"
    if not path.exists():
        return
    with path.open("a", encoding="utf-8") as handle:
        handle.write("\n\n---\n\n# Phone2 Batch 1 Master Addendum\n\n")
        for row in new_rows:
            handle.write(f"## {row['id']} — {row['title']}\n\n")
            handle.write(f"- Equation: `{row['canonical_equation']}`\n")
            handle.write(f"- Source: `{row['formation_inputs']}`\n")
            handle.write(f"- Wolfram status: `{row['wolfram_status']}`\n\n")


def append_id_system(root: Path, new_rows: list[dict]) -> list[dict]:
    path = root / ID_SYSTEM_NAME
    if not path.exists():
        return []
    rows = read_csv(path)
    existing = {row["id"] for row in rows}
    max_id = max(id_num(row["id"]) for row in new_rows)
    digits = pi_digits(max_id + 30)
    additions = []
    for row in new_rows:
        if row["id"] in existing:
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
    rows.extend(additions)
    write_csv(path, rows, ID_SYSTEM_FIELDS)
    return additions


def write_source_truth(new_rows: list[dict], id_system_rows: list[dict], basis_sha: str) -> None:
    id_system_by_id = {row["id"]: row for row in id_system_rows}
    for row in new_rows:
        tzpid = row["id"]
        folder = PROOF_ROOT / "tzp_id" / tzpid
        folder.mkdir(parents=True, exist_ok=True)
        id_system = id_system_by_id.get(tzpid, {})
        source_truth = {
            "schema": {
                "name": "TZPID Phone2 batch source truth",
                "version": "0.1.0",
                "generated_at": now_utc(),
                "non_destructive": False,
                "basis": "PHONE2_ATOMIC_EQUATION_QUEUE.csv",
                "basis_sha1": sha1(ATOMIC_QUEUE),
            },
            "identity": {
                "tzpid": tzpid,
                "uuid": row["uuid"],
                "registry_id": row["isabelle_sid"],
                "canonical_title": row["title"],
                "source_files": {
                    "master_csv": str(PROOF_ROOT / MASTER_NAME),
                    "source_truth": str(folder / f"{tzpid}.source_truth.json"),
                    "tex": str(folder / f"{tzpid}.tex"),
                    "id_system": str(folder / f"{tzpid}.id_system.json"),
                },
            },
            "classification": {
                "source_family": "Phone2",
                "category": "phone2-atomic-equation-intake",
                "formation_method": row["formation_method"],
                "isabelle_kind": row["isabelle_kind"],
                "gold_spine": row["gold_spine"],
            },
            "theory": {
                "canonical_statement": row["canonical_statement"],
                "technical_interpretation": row["encyclopedia"],
                "semantic_context": row.get("_semantic_context", ""),
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
                "phone2_atomic_queue_sha1": sha1(ATOMIC_QUEUE),
                "master_csv_sha1_after_batch": basis_sha,
            },
            "formal_derivations": {
                "isabelle": {"status": "pending_phone2_semantic_translation"},
                "lean": {"status": "pending_export"},
                "rocq": {"status": "pending_export"},
                "wolfram": {"status": row["wolfram_status"]},
            },
            "promotion_status": {
                "status": "minted_from_phone2_batch1",
                "needs_review": True,
            },
            "tzpid_id_system": id_system,
            "tzpid_provenance": {
                "project": "TZPID Proof Pipeline",
                "creator": CREATOR,
                "creator_orcid": ORCID,
                "creator_orcid_url": ORCID_URL,
                "generator": "mint_phone2_batch1.py",
                "generated_at_utc": now_utc(),
                "source_tag": "PHONE2",
            },
        }
        (folder / f"{tzpid}.source_truth.json").write_text(
            json.dumps(source_truth, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        if id_system:
            (folder / f"{tzpid}.id_system.json").write_text(
                json.dumps(
                    {
                        "schema": {
                            "name": "TZPID ID system sidecar",
                            "version": "0.1.0",
                            "generated_at_utc": now_utc(),
                            "basis": "TZPID_ID_SYSTEM.csv",
                        },
                        "identity": {
                            "tzpid": tzpid,
                            "title": row["title"],
                            "uuid": row["uuid"],
                        },
                        "trawin_geometry": {
                            "RTEID": id_system.get("RTEID", ""),
                            "poloidal_theta_rad": id_system.get("poloidal_theta_rad", ""),
                            "toroidal_phi_rad": id_system.get("toroidal_phi_rad", ""),
                            "rteid_source": id_system.get("rteid_source", ""),
                        },
                        "pi_identity": {
                            "PiID": id_system.get("PiID", ""),
                            "TZPi": id_system.get("TZPi", ""),
                            "PiPE_position": id_system.get("PiPE_position", ""),
                        },
                        "tzpid_provenance": {
                            "project": "TZPID Proof Pipeline",
                            "creator": CREATOR,
                            "creator_orcid": ORCID,
                            "creator_orcid_url": ORCID_URL,
                            "generator": "mint_phone2_batch1.py",
                            "generated_at_utc": now_utc(),
                        },
                    },
                    indent=2,
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )
        (folder / f"{tzpid}.metadata.json").write_text(
            json.dumps(
                {
                    "tzpid": tzpid,
                    "title": row["title"],
                    "uuid": row["uuid"],
                    "PiID": id_system.get("PiID", ""),
                    "RTEID": id_system.get("RTEID", ""),
                    "creator": CREATOR,
                    "creator_orcid": ORCID_URL,
                    "embedded_at_utc": now_utc(),
                    "source_tag": "PHONE2",
                },
                indent=2,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        (folder / f"{tzpid}.metadata.md").write_text(
            "\n".join(
                [
                    "---",
                    f"tzpid: {tzpid}",
                    f"title: {row['title']}",
                    f"uuid: {row['uuid']}",
                    f"PiID: {id_system.get('PiID', '')}",
                    f"RTEID: {id_system.get('RTEID', '')}",
                    f"creator: {CREATOR}",
                    f"creator_orcid: {ORCID_URL}",
                    f"source_tag: PHONE2",
                    "---",
                    "",
                ]
            ),
            encoding="utf-8",
        )
        tex = rf"""\documentclass[11pt]{{article}}
\usepackage{{amsmath,amssymb,hyperref}}
\hypersetup{{pdfauthor={{{CREATOR}}},pdfcreator={{Trawin, Daniel Alexander}},colorlinks=false}}
\title{{{row['title']}}}
\author{{{CREATOR}}}
\date{{{now_utc()}}}
\begin{{document}}
\maketitle
\section*{{Metadata}}
\begin{{itemize}}
\item TZPID: {tzpid}
\item UUID: {row['uuid']}
\item ORCID: \url{{{ORCID_URL}}}
\item Source: {row.get('_source_file', '')} line {row.get('_line_number', '')}
\end{{itemize}}
\section*{{Canonical Equation}}
\[
{row['canonical_equation']}
\]
\section*{{Statement}}
{row['canonical_statement']}
\section*{{Interpretation}}
{row['encyclopedia']}
\end{{document}}
"""
        (folder / f"{tzpid}.tex").write_text(tex, encoding="utf-8")


def main() -> None:
    selected = load_batch_rows()
    if len(selected) != BATCH_SIZE:
        raise RuntimeError(f"Expected {BATCH_SIZE} rows, got {len(selected)}")

    proof_master = PROOF_ROOT / MASTER_NAME
    existing = read_csv(proof_master)
    max_existing = max(id_num(row["id"]) for row in existing)
    start_num = max_existing + 1

    new_rows = []
    enriched_private = []
    for offset, source in enumerate(selected):
        tzpid = f"ID{start_num + offset:04d}"
        title = f"Phone2 {source.get('domain_family', 'General').replace('_', ' ').title()} {title_case_slug(source.get('atomic_equation', ''), 52)}"
        uuid = deterministic_uuid(tzpid, source)
        dictionary = dictionary_for(source)
        encyclopedia = encyclopedia_for(source, tzpid)
        wolfram_status = (
            "phone2_file_has_parse_clean_wolfram;needs_equation_specific_parse"
            if source.get("wolfram_status") == "file_has_parse_clean_wolfram"
            else "needs_wolfram_translation"
        )
        row = {
            "id": tzpid,
            "title": title,
            "canonical_statement": statement_for(source),
            "canonical_equation": source.get("atomic_equation", ""),
            "formation_method": "Phone2 atomic equation extraction",
            "formation_inputs": f"{source.get('source_file')} line {source.get('line_number')}",
            "formation_note": (
                f"Minted from Phone2 batch 1 atomic queue row {source.get('atomic_index')}; "
                f"semantic kind={source.get('semantic_kind')}; domain={source.get('domain_family')}."
            ),
            "dictionary": dictionary,
            "encyclopedia": encyclopedia,
            "isabelle_kind": isabelle_kind(source),
            "obligation_role": "Phone2_Staged_Equation",
            "proof_required_checks": "source_truth_json;semantic_grounding;wolfram_form_check;duplicate_review",
            "gold_spine": "phone2_intake",
            "lean_rocq": "export_pending",
            "wolfram_status": wolfram_status,
            "isabelle_sid": f"registry_{tzpid}",
            "uuid": uuid,
        }
        private = dict(row)
        private["_source_file"] = source.get("source_file", "")
        private["_line_number"] = source.get("line_number", "")
        private["_semantic_context"] = source.get("semantic_context", "")
        private["_wolfram_form_hint"] = source.get("wolfram_form_hint", "")
        new_rows.append(row)
        enriched_private.append(private)

    tracked_paths = []
    for root in (PROOF_ROOT, OPENAI2_ROOT):
        for name in (MASTER_NAME, DICTIONARY_NAME, ENCYCLOPEDIA_NAME, ID_SYSTEM_NAME):
            path = root / name
            if path.exists():
                tracked_paths.append(path)
    backups = backup(tracked_paths)

    for root in (PROOF_ROOT, OPENAI2_ROOT):
        append_master(root, new_rows)
        append_dictionary(root, new_rows)
        append_encyclopedia(root, new_rows)
        append_master_md(root, new_rows)
    id_system_rows = append_id_system(PROOF_ROOT, new_rows)
    append_id_system(OPENAI2_ROOT, new_rows)
    proof_master_sha = sha1(PROOF_ROOT / MASTER_NAME)
    write_source_truth(enriched_private, id_system_rows, proof_master_sha)

    manifest = {
        "generated_at_utc": now_utc(),
        "batch": "PHONE2 batch 1",
        "count": len(new_rows),
        "first_id": new_rows[0]["id"],
        "last_id": new_rows[-1]["id"],
        "source_queue": str(ATOMIC_QUEUE),
        "source_batches": str(ATOMIC_BATCHES),
        "backup_dir": str(BACKUP_DIR),
        "backups": backups,
        "roots_updated": [str(PROOF_ROOT), str(OPENAI2_ROOT)],
        "proof_master_sha1_after": proof_master_sha,
        "ids": [row["id"] for row in new_rows],
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")

    REPORT.write_text(
        "\n".join(
            [
                "# Phone2 Batch 1 Mint Report",
                "",
                f"- Generated UTC: `{manifest['generated_at_utc']}`",
                f"- New IDs minted: `{len(new_rows)}`",
                f"- ID range: `{new_rows[0]['id']}` to `{new_rows[-1]['id']}`",
                f"- Backup directory: `{BACKUP_DIR}`",
                f"- Roots updated: `D:\\TZPIDProof`, `D:\\00_Engine\\AI_Workspaces\\OpenAI2`",
                f"- Source-truth folders: `D:\\TZPIDProof\\tzp_id\\{new_rows[0]['id']}` ... `D:\\TZPIDProof\\tzp_id\\{new_rows[-1]['id']}`",
                "",
                "## Status",
                "",
                "Batch 1 has been minted from the Phone2 atomic equation queue. Rows remain tagged as staged equations and require downstream semantic review, Wolfram equation-specific parsing, and Isabelle obligation generation before being promoted to certified proof status.",
                "",
                "## Manifest",
                "",
                f"- `{MANIFEST}`",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    print(json.dumps({k: manifest[k] for k in ("count", "first_id", "last_id", "backup_dir")}, indent=2))


if __name__ == "__main__":
    main()
