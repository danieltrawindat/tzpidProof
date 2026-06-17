from __future__ import annotations

import csv
import hashlib
import json
import re
import shutil
import subprocess
import uuid
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parent
OUT = Path(r"D:\TZPIDProof")
PROOF_DIR = OUT / "tzpid_proof"
ID_DIR = OUT / "tzp_id"
HDF5_DIR = OUT / "hdf5"

MASTER_CSV = ROOT / "TZPID_ALL_IDS_CANONICAL_EQUATION_MASTER_with_export.csv"
ID_SYSTEM_CSV = ROOT / "TZPID_ID_SYSTEM.csv"
DICTIONARY_CSV = ROOT / "TZPID_DICTIONARY.csv"
ENCYCLOPEDIA_MD = ROOT / "TZPID_ENCYCLOPEDIA.md"
QUEUE_CSV = ROOT / "TZPID_THEOREM_SEMANTIC_QUEUE.csv"

SOURCE_ID_ROOT = Path(r"D:\TZPID\TZPID")
ALT_TEX_ROOT = Path(r"D:\tzpid2\entries")

CREATOR = "Daniel Alexander Trawin"
ORCID = "https://orcid.org/0009-0001-4630-3715"


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def git(args: list[str], default: str = "") -> str:
    try:
        return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()
    except Exception:
        return default


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", errors="ignore", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def copy_file(src: Path, dst: Path) -> dict[str, str | int]:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    return {
        "source": str(src),
        "path": str(dst.relative_to(OUT)).replace("\\", "/"),
        "bytes": dst.stat().st_size,
        "sha256": sha256(dst),
    }


def copy_tree(src: Path, dst: Path) -> dict[str, int | str]:
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__", ".git"))
    files = [path for path in dst.rglob("*") if path.is_file()]
    return {
        "source": str(src),
        "path": str(dst.relative_to(OUT)).replace("\\", "/"),
        "files": len(files),
        "bytes": sum(path.stat().st_size for path in files),
    }


def slug(text: str, limit: int = 72) -> str:
    text = re.sub(r"[^A-Za-z0-9]+", "_", text).strip("_").lower()
    return (text or "untitled")[:limit].strip("_") or "untitled"


def latex_escape(text: str) -> str:
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    return "".join(replacements.get(ch, ch) for ch in text)


def md_escape(text: str) -> str:
    return (text or "").replace("|", "\\|").replace("\n", "<br>")


def deterministic_uuid(prefix: str, parts: list[str]) -> str:
    seed = prefix + ":" + "|".join(parts)
    return str(uuid.uuid5(uuid.NAMESPACE_URL, seed))


def metadata_block(tzpid: str, master_row: dict[str, str], id_row: dict[str, str] | None) -> dict:
    id_row = id_row or {}
    return {
        "tzpid": tzpid,
        "title": master_row.get("title", ""),
        "uuid": id_row.get("uuid") or master_row.get("uuid") or deterministic_uuid(
            "tzpid", [tzpid, master_row.get("title", ""), master_row.get("canonical_equation", "")]
        ),
        "PiID": id_row.get("PiID", ""),
        "RTEID": id_row.get("RTEID", ""),
        "TZPi": id_row.get("TZPi", ""),
        "PiPE_position": id_row.get("PiPE_position", ""),
        "poloidal_theta_rad": id_row.get("poloidal_theta_rad", ""),
        "toroidal_phi_rad": id_row.get("toroidal_phi_rad", ""),
        "loc_class": id_row.get("loc_class", ""),
        "arxiv_class": id_row.get("arxiv_class", ""),
        "creator": CREATOR,
        "creator_orcid": ORCID,
        "embedded_at_utc": now_utc(),
    }


def existing_source_truth(tzpid: str) -> Path | None:
    candidates = [
        SOURCE_ID_ROOT / tzpid / f"{tzpid}.source_truth.json",
        SOURCE_ID_ROOT / tzpid / f"{tzpid}.id_system.json",
        SOURCE_ID_ROOT / tzpid / f"{tzpid}.JSON",
    ]
    for path in candidates:
        if path.exists():
            return path
    return None


def existing_tex(tzpid: str) -> Path | None:
    candidates = [
        SOURCE_ID_ROOT / tzpid / f"{tzpid}.TEX",
        SOURCE_ID_ROOT / tzpid / f"{tzpid}.tex",
        ALT_TEX_ROOT / f"{tzpid}.tex",
    ]
    for path in candidates:
        if path.exists():
            return path
    return None


def generated_source_truth(tzpid: str, master_row: dict[str, str], id_row: dict[str, str] | None) -> dict:
    meta = metadata_block(tzpid, master_row, id_row)
    return {
        "schema": {
            "name": "TZPIDProof packaged source truth",
            "version": "1.0.0",
            "generated_at_utc": meta["embedded_at_utc"],
            "basis": MASTER_CSV.name,
            "basis_sha256": sha256(MASTER_CSV),
        },
        "metadata": meta,
        "canonical": {
            "statement": master_row.get("canonical_statement", ""),
            "equation": master_row.get("canonical_equation", ""),
            "formation_method": master_row.get("formation_method", ""),
            "formation_inputs": master_row.get("formation_inputs", ""),
            "formation_note": master_row.get("formation_note", ""),
        },
        "registry": {
            "isabelle_kind": master_row.get("isabelle_kind", ""),
            "obligation_role": master_row.get("obligation_role", ""),
            "proof_required_checks": master_row.get("proof_required_checks", ""),
            "gold_spine": master_row.get("gold_spine", ""),
            "lean_rocq": master_row.get("lean_rocq", ""),
            "wolfram_status": master_row.get("wolfram_status", ""),
            "isabelle_sid": master_row.get("isabelle_sid", ""),
        },
        "dictionary": master_row.get("dictionary", ""),
        "encyclopedia": master_row.get("encyclopedia", ""),
        "source_note": "Generated because no existing source-truth JSON was found in D:/TZPID/TZPID for this ID.",
    }


def generated_tex(tzpid: str, master_row: dict[str, str], id_row: dict[str, str] | None) -> str:
    meta = metadata_block(tzpid, master_row, id_row)
    equation = master_row.get("canonical_equation", "").strip()
    statement = master_row.get("canonical_statement", "").strip()
    lines = [
        r"\section*{" + latex_escape(f"{tzpid}: {master_row.get('title', '')}") + "}",
        r"\paragraph{Metadata.}",
        latex_escape(f"PiID: {meta['PiID']} | RTEID: {meta['RTEID']} | UUID: {meta['uuid']}"),
        "",
        r"\paragraph{Canonical Statement.}",
        latex_escape(statement or "No canonical statement supplied in the master row."),
        "",
    ]
    if equation:
        lines.extend([r"\paragraph{Canonical Equation.}", r"\[", equation, r"\]", ""])
    lines.extend(
        [
            r"\paragraph{Dictionary.}",
            latex_escape(master_row.get("dictionary", "")),
            "",
            r"\paragraph{Encyclopedia.}",
            latex_escape(master_row.get("encyclopedia", "")),
            "",
        ]
    )
    return "\n".join(lines)


def package_ids(master_rows: list[dict[str, str]], id_rows: dict[str, dict[str, str]]) -> dict:
    copied_source_truth = 0
    generated_source_truth_count = 0
    copied_tex = 0
    generated_tex_count = 0
    for row in master_rows:
        tzpid = row["id"]
        dst = ID_DIR / tzpid
        dst.mkdir(parents=True, exist_ok=True)
        id_row = id_rows.get(tzpid)

        source_truth_path = existing_source_truth(tzpid)
        if source_truth_path:
            copy_file(source_truth_path, dst / f"{tzpid}.source_truth.json")
            copied_source_truth += 1
        else:
            record = generated_source_truth(tzpid, row, id_row)
            (dst / f"{tzpid}.source_truth.json").write_text(
                json.dumps(record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
            )
            generated_source_truth_count += 1

        tex_path = existing_tex(tzpid)
        if tex_path:
            copy_file(tex_path, dst / f"{tzpid}.tex")
            copied_tex += 1
        else:
            (dst / f"{tzpid}.tex").write_text(
                generated_tex(tzpid, row, id_row), encoding="utf-8"
            )
            generated_tex_count += 1

        meta = metadata_block(tzpid, row, id_row)
        (dst / f"{tzpid}.metadata.json").write_text(
            json.dumps(meta, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        (dst / f"{tzpid}.metadata.md").write_text(
            "\n".join(
                [
                    f"# {tzpid} Metadata",
                    "",
                    f"- Title: {md_escape(meta['title'])}",
                    f"- UUID: `{meta['uuid']}`",
                    f"- PiID: `{meta['PiID']}`",
                    f"- RTEID: `{meta['RTEID']}`",
                    f"- Creator: {CREATOR}",
                    f"- ORCID: {ORCID}",
                    "",
                ]
            ),
            encoding="utf-8",
        )
    return {
        "id_folders": len(master_rows),
        "copied_source_truth_json": copied_source_truth,
        "generated_source_truth_json": generated_source_truth_count,
        "copied_tex": copied_tex,
        "generated_tex": generated_tex_count,
    }


def write_master_markdown(master_rows: list[dict[str, str]], id_rows: dict[str, dict[str, str]]) -> None:
    path = OUT / "TZPID_ALL_IDS_CANONICAL_EQUATION_MASTER_with_export.md"
    lines = [
        "# TZPID Canonical Equation Master",
        "",
        f"Generated UTC: {now_utc()}",
        f"Rows: `{len(master_rows)}`",
        "",
        "| ID | Title | Kind | Gold Spine | PiID | RTEID | UUID |",
        "|---|---|---|---|---|---|---|",
    ]
    for row in master_rows:
        id_row = id_rows.get(row["id"], {})
        lines.append(
            "| {id} | {title} | {kind} | {spine} | `{piid}` | `{rteid}` | `{uuid}` |".format(
                id=row["id"],
                title=md_escape(row.get("title", "")),
                kind=md_escape(row.get("isabelle_kind", "")),
                spine=md_escape(row.get("gold_spine", "")),
                piid=id_row.get("PiID", ""),
                rteid=id_row.get("RTEID", ""),
                uuid=id_row.get("uuid") or row.get("uuid", ""),
            )
        )
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def package_theorem_proofs(
    queue_rows: list[dict[str, str]],
    master_by_id: dict[str, dict[str, str]],
    id_rows: dict[str, dict[str, str]],
) -> dict:
    proof_root = PROOF_DIR / "individual_theories"
    proof_root.mkdir(parents=True, exist_ok=True)
    for row in queue_rows:
        tzpid = row["id"]
        index = int(row["queue_index"])
        folder = proof_root / f"Q{index:03d}_{tzpid}_{slug(row['name'])}"
        folder.mkdir(parents=True, exist_ok=True)
        master_row = master_by_id.get(tzpid, {"id": tzpid, "title": row["name"]})
        id_row = id_rows.get(tzpid)
        meta = metadata_block(tzpid, master_row, id_row)
        proof_record = {
            "schema": "TZPIDProof individual theorem proof package",
            "generated_at_utc": now_utc(),
            "queue": row,
            "metadata": meta,
            "master_row": master_row,
            "source_truth_relative": f"../../tzp_id/{tzpid}/{tzpid}.source_truth.json",
            "tex_relative": f"../../tzp_id/{tzpid}/{tzpid}.tex",
            "formal_status": {
                "translation_status": row.get("translation_status", ""),
                "translation_class": row.get("translation_class", ""),
                "isabelle_batch_source": row.get("source_file", ""),
                "note": "Proof package captures the theorem row, metadata, source truth, TeX source, and current semantic translation status.",
            },
        }
        (folder / "proof.json").write_text(
            json.dumps(proof_record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        equation = master_row.get("canonical_equation", "").strip()
        lines = [
            r"\section*{" + latex_escape(f"Q{index:03d} {tzpid}: {row['name']}") + "}",
            r"\paragraph{Metadata.}",
            latex_escape(f"PiID: {meta['PiID']} | RTEID: {meta['RTEID']} | UUID: {meta['uuid']}"),
            "",
            r"\paragraph{Semantic Queue.}",
            latex_escape(
                f"Status: {row.get('translation_status', '')}; class: {row.get('translation_class', '')}; role: {row.get('obligation_role', '')}."
            ),
            "",
            r"\paragraph{Canonical Statement.}",
            latex_escape(master_row.get("canonical_statement", row["name"])),
            "",
        ]
        if equation:
            lines.extend([r"\paragraph{Canonical Equation.}", r"\[", equation, r"\]", ""])
        lines.extend(
            [
                r"\paragraph{Source Truth.}",
                latex_escape(f"See ../../tzp_id/{tzpid}/{tzpid}.source_truth.json and ../../tzp_id/{tzpid}/{tzpid}.tex."),
                "",
            ]
        )
        (folder / "proof.tex").write_text("\n".join(lines), encoding="utf-8")
        src_truth = ID_DIR / tzpid / f"{tzpid}.source_truth.json"
        src_tex = ID_DIR / tzpid / f"{tzpid}.tex"
        if src_truth.exists():
            copy_file(src_truth, folder / f"{tzpid}.source_truth.json")
        if src_tex.exists():
            copy_file(src_tex, folder / f"{tzpid}.tex")

    write_csv(
        PROOF_DIR / "individual_theories.csv",
        queue_rows,
        [
            "queue_index",
            "source",
            "id",
            "name",
            "kind",
            "obligation_role",
            "semantic_anchor_id",
            "source_file",
            "line",
            "translation_status",
            "translation_class",
            "duplicate_source_id_name",
        ],
    )
    lines = [
        "# Individual Theorem Proof Folders",
        "",
        f"Queue rows packaged: `{len(queue_rows)}`",
        "",
        "Note: the current authoritative queue contains 397 rows. This package preserves all 397 rows even though the working shorthand has sometimes referred to 394.",
        "",
        "| Queue | ID | Name | Status | Class | Folder |",
        "|---:|---|---|---|---|---|",
    ]
    for row in queue_rows:
        index = int(row["queue_index"])
        folder = f"individual_theories/Q{index:03d}_{row['id']}_{slug(row['name'])}"
        lines.append(
            f"| {index} | {row['id']} | {md_escape(row['name'])} | `{row['translation_status']}` | `{row['translation_class']}` | `{folder}` |"
        )
    lines.append("")
    (PROOF_DIR / "individual_theories.md").write_text("\n".join(lines), encoding="utf-8")
    return {"individual_theory_rows": len(queue_rows)}


def package_proof_pipeline() -> list[dict]:
    copied: list[dict] = []
    PROOF_DIR.mkdir(parents=True, exist_ok=True)
    for src in sorted(ROOT.glob("*.py")):
        copied.append(copy_file(src, PROOF_DIR / "pipeline_scripts" / src.name))
    for src in [
        QUEUE_CSV,
        ROOT / "TZPID_THEOREM_SEMANTIC_QUEUE_SUMMARY.md",
        ROOT / "TZPID_PHASE2_COMPLETION_MATRIX.csv",
        ROOT / "TZPID_PHASE2_COMPLETION_MATRIX.md",
        ROOT / "TZPID_PHASE2_COMPLETION_MATRIX.json",
        ROOT / "TZPID_PHASE2_SEMANTIC_TRANSLATION.md",
        ROOT / "README_PROOF_PIPELINE.md",
        ROOT / "README_RUN.md",
        ROOT / "README_ID_RANGES.md",
    ]:
        if src.exists():
            copied.append(copy_file(src, PROOF_DIR / "ledgers" / src.name))
    if (ROOT / "isabelle_tzpid").exists():
        copied.append(copy_tree(ROOT / "isabelle_tzpid", PROOF_DIR / "isabelle_tzpid"))
        batch_dir = PROOF_DIR / "batches"
        batch_dir.mkdir(parents=True, exist_ok=True)
        for src in sorted((ROOT / "isabelle_tzpid").glob("TZPID_Theorem_Semantic_Batch*.thy")):
            copied.append(copy_file(src, batch_dir / src.name))
    if (ROOT / "phase2_checks").exists():
        copied.append(copy_tree(ROOT / "phase2_checks", PROOF_DIR / "phase2_checks"))
    if (ROOT / "release_phase3").exists():
        copied.append(copy_tree(ROOT / "release_phase3", PROOF_DIR / "release_phase3"))
    if (ROOT / "lean_rocq_gold_spine").exists():
        copied.append(copy_tree(ROOT / "lean_rocq_gold_spine", PROOF_DIR / "lean_rocq_gold_spine"))
    for src in [
        ROOT / "add_tzpid_source_truth_provenance.py",
        ROOT / "tzpid_provenance.py",
        ROOT / "create_missing_tzpid_source_truth_folders.py",
        ROOT / "apply_tzpid_id_system_to_folders.py",
        ROOT / "split_tzpid_encyclopedia_to_id_folders.py",
        ROOT / "tzpid_source_truth_provenance_update_summary.json",
        ROOT / "missing_tzpid_source_truth_creation_summary.json",
        ROOT / "tzpid_id_system_apply_summary.json",
        ROOT / "tzpid_encyclopedia_split_summary.json",
    ]:
        if src.exists():
            copied.append(copy_file(src, PROOF_DIR / "metadata_embedding_mechanism" / src.name))
    spine_sources = [ROOT / "release_phase3" / "spines", Path(r"D:\00_Engine\AI_Workspaces\OpenAI2\new_gold_spines")]
    spine_dst = PROOF_DIR / "spines"
    spine_dst.mkdir(parents=True, exist_ok=True)
    seen = set()
    for source in spine_sources:
        if source.exists():
            for src in sorted(source.glob("*")):
                if src.is_file() and src.name not in seen:
                    seen.add(src.name)
                    copied.append(copy_file(src, spine_dst / src.name))
    return copied


def write_top_readme(summary: dict) -> None:
    lines = [
        "# TZPIDProof",
        "",
        f"Generated UTC: {summary['generated_at_utc']}",
        f"Creator: {CREATOR}",
        f"ORCID: {ORCID}",
        f"Source commit: `{summary['git_commit']}`",
        "",
        "## Layout",
        "",
        "- `tzpid_proof/`: proof pipeline files, Isabelle theories, semantic batches, spines, certificates, Lean/Rocq exports, metadata embedding scripts, and individual theorem proof folders.",
        "- `tzp_id/`: one folder per master registry ID, each containing source-truth JSON, TeX, and PiID/RTEID metadata.",
        "- `hdf5/`: copied HDF5 numerical artifacts.",
        "",
        "## Counts",
        "",
        f"- Master rows / ID folders: `{summary['id_package']['id_folders']}`",
        f"- Theorem proof folders: `{summary['proof_package']['individual_theory_rows']}`",
        f"- Copied source-truth JSON files: `{summary['id_package']['copied_source_truth_json']}`",
        f"- Generated source-truth JSON files: `{summary['id_package']['generated_source_truth_json']}`",
        f"- Copied TeX files: `{summary['id_package']['copied_tex']}`",
        f"- Generated TeX files: `{summary['id_package']['generated_tex']}`",
        f"- HDF5 files: `{summary['hdf5_files']}`",
        "",
        "The authoritative theorem semantic queue contains 397 rows. This package preserves all rows and notes the count mismatch with the informal 394 shorthand in `tzpid_proof/individual_theories.md`.",
        "",
    ]
    (OUT / "README.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    if OUT.exists():
        marker = OUT / "TZPIDProof_MANIFEST.json"
        if not marker.exists():
            raise SystemExit(
                f"Refusing to overwrite {OUT}: TZPIDProof_MANIFEST.json not found."
            )
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)

    master_rows = read_csv(MASTER_CSV)
    id_rows_list = read_csv(ID_SYSTEM_CSV)
    id_rows = {row["id"]: row for row in id_rows_list}
    master_by_id = {row["id"]: row for row in master_rows}
    queue_rows = read_csv(QUEUE_CSV)

    copied_top = []
    for src in [MASTER_CSV, ID_SYSTEM_CSV, DICTIONARY_CSV, ENCYCLOPEDIA_MD]:
        copied_top.append(copy_file(src, OUT / src.name))
    write_master_markdown(master_rows, id_rows)

    hdf5_count = 0
    for src in sorted(ROOT.glob("*.h5")):
        copy_file(src, HDF5_DIR / src.name)
        hdf5_count += 1

    id_summary = package_ids(master_rows, id_rows)
    proof_copies = package_proof_pipeline()
    proof_summary = package_theorem_proofs(queue_rows, master_by_id, id_rows)

    summary = {
        "generated_at_utc": now_utc(),
        "creator": CREATOR,
        "orcid": ORCID,
        "git_commit": git(["rev-parse", "HEAD"]),
        "git_branch": git(["branch", "--show-current"]),
        "git_remote": git(["remote", "get-url", "origin"]),
        "master_csv": str(MASTER_CSV),
        "master_sha256": sha256(MASTER_CSV),
        "top_level_files": copied_top,
        "id_package": id_summary,
        "proof_package": proof_summary,
        "proof_pipeline_copied_items": len(proof_copies),
        "hdf5_files": hdf5_count,
        "output": str(OUT),
    }
    (OUT / "TZPIDProof_MANIFEST.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    write_top_readme(summary)
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
