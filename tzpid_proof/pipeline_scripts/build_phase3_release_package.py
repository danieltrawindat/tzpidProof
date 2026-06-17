from __future__ import annotations

import csv
import hashlib
import json
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parent
RELEASE = ROOT / "release_phase3"
SPINE_SOURCE = Path(r"D:\00_Engine\AI_Workspaces\OpenAI2\new_gold_spines")
CREATOR = "Daniel Alexander Trawin"
ORCID = "https://orcid.org/0009-0001-4630-3715"
DOI = "10.5281/zenodo.20579476"


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def rel_from_release(path: str) -> str:
    return str(Path(path).relative_to("release_phase3")).replace("\\", "/")


def git(args: list[str]) -> str:
    return subprocess.check_output(["git", *args], text=True).strip()


def try_git(args: list[str], default: str = "") -> str:
    try:
        return git(args)
    except Exception:
        return default


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def copy_file(src: Path, dst: Path) -> dict[str, str | int]:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    return {
        "source": str(src),
        "release_path": rel(dst),
        "bytes": dst.stat().st_size,
    }


def register_release_file(path: Path, source_note: str = "generated_in_release") -> dict[str, str | int]:
    return {
        "source": source_note,
        "release_path": rel(path),
        "bytes": path.stat().st_size,
    }


def read_matrix() -> list[dict[str, str]]:
    with (ROOT / "TZPID_PHASE2_COMPLETION_MATRIX.csv").open(
        newline="", encoding="utf-8"
    ) as handle:
        return list(csv.DictReader(handle))


def write_verification_appendix(rows: list[dict[str, str]]) -> None:
    lines = [
        "# Phase 3 Verification Appendix",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).replace(microsecond=0).isoformat()}",
        f"Commit: `{git(['rev-parse', 'HEAD'])}`",
        "",
        "## Matrix Summary",
        "",
        f"- Matrix rows: `{len(rows)}`",
        f"- Clean Isabelle rows: `{sum(row['isabelle_checked'] == 'clean_build' for row in rows)}`",
        f"- Rows with certificate lane: `{sum(bool(row['wolfram_certificate']) and row['wolfram_certificate'] != 'not_attached' for row in rows)}`",
        f"- Rows with missing files: `{sum(bool(row['missing_files']) for row in rows)}`",
        "",
        "## Row-Level Status",
        "",
        "| Family | Kind | Completion | Isabelle | Certificate | Files |",
        "|---|---|---|---|---|---|",
    ]
    for row in rows:
        files = row["isabelle_files"].replace("|", "\\|")
        lines.append(
            "| {family} | {kind} | `{completion}` | `{isabelle}` | `{cert}` | {files} |".format(
                family=row["family"],
                kind=row["kind"],
                completion=row["completion_state"],
                isabelle=row["isabelle_checked"],
                cert=row["wolfram_certificate"],
                files=files,
            )
        )
    lines.append("")
    (RELEASE / "VERIFICATION_APPENDIX.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )


def write_spine_pack(rows: list[dict[str, str]], copied_spines: list[dict]) -> None:
    non_batches = [row for row in rows if row["kind"] != "batch"]
    spine_files = {Path(item["release_path"]).name: item for item in copied_spines}
    lines = [
        "# Phase 3 Spine Pack",
        "",
        "This pack is the paper-facing index for the verified Phase 2 spines and domain families.",
        "",
        "## Verified Spine Families",
        "",
        "| Family | Kind | Completion | Primary Isabelle Files |",
        "|---|---|---|---|",
    ]
    for row in non_batches:
        files = row["isabelle_files"].replace("|", "\\|")
        lines.append(
            f"| {row['family']} | {row['kind']} | `{row['completion_state']}` | {files} |"
        )
    lines.extend(["", "## Copied Source Spine Documents", ""])
    for name in sorted(spine_files):
        item = spine_files[name]
        lines.append(f"- [{name}]({rel_from_release(item['release_path'])})")
    lines.extend(
        [
            "",
            "## Release Notes",
            "",
            "The Bessel residual bridge is named neutrally in this release package even where older source filenames still contain metaphorical wording. The verified matrix row is `Hyperspherical Bessel residual bridge`.",
            "",
            "Large HDF5 datasets are referenced in `HDF5_ARTIFACTS.md` instead of duplicated into this release folder.",
        ]
    )
    (RELEASE / "SPINE_PACK.md").write_text("\n".join(lines), encoding="utf-8")


def write_certificate_manifest(copied_certs: list[dict]) -> None:
    json_items = [item for item in copied_certs if item["release_path"].endswith(".json")]
    parsed = []
    for item in json_items:
        data = json.loads((ROOT / item["release_path"]).read_text(encoding="utf-8"))
        parsed.append(
            {
                "release_path": item["release_path"],
                "certificate": data.get("certificate", Path(item["release_path"]).stem),
                "status": data.get("status", "unknown"),
                "engine": data.get("engine", ""),
                "generated_utc": data.get("generated_utc", ""),
                "claim_boundary": data.get("claim_boundary", ""),
            }
        )
    manifest = {
        "generated_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "certificate_json_count": len(parsed),
        "all_status_fields_pass": all(item["status"] != "fail" for item in parsed),
        "certificates": parsed,
    }
    (RELEASE / "CERTIFICATE_MANIFEST.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )
    lines = [
        "# Phase 3 Certificate Manifest",
        "",
        f"Certificate JSON files: `{len(parsed)}`",
        f"All top-level statuses pass: `{manifest['all_status_fields_pass']}`",
        "",
        "| Certificate | Status | Engine | File |",
        "|---|---|---|---|",
    ]
    for item in parsed:
        lines.append(
            f"| {item['certificate']} | `{item['status']}` | {item['engine']} | [{Path(item['release_path']).name}]({rel_from_release(item['release_path'])}) |"
        )
    lines.append("")
    (RELEASE / "CERTIFICATE_MANIFEST.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )


def write_hdf5_manifest() -> None:
    rows = []
    for path in sorted(ROOT.glob("*.h5")):
        rows.append(
            {
                "path": str(path),
                "bytes": path.stat().st_size,
                "release_action": "referenced_not_duplicated",
            }
        )
    (RELEASE / "HDF5_ARTIFACTS.json").write_text(
        json.dumps({"artifacts": rows}, indent=2), encoding="utf-8"
    )
    lines = [
        "# HDF5 Artifacts",
        "",
        "Large numerical artifacts are referenced here and not duplicated into `release_phase3/`.",
        "",
        "| Path | Bytes | Release Action |",
        "|---|---:|---|",
    ]
    for row in rows:
        lines.append(
            f"| `{row['path']}` | {row['bytes']} | `{row['release_action']}` |"
        )
    lines.append("")
    (RELEASE / "HDF5_ARTIFACTS.md").write_text("\n".join(lines), encoding="utf-8")


def write_release_metadata(rows: list[dict[str, str]]) -> None:
    commit = try_git(["rev-parse", "HEAD"])
    branch = try_git(["branch", "--show-current"], "unknown")
    remote = try_git(["remote", "get-url", "origin"], "")
    generated = utc_now()

    release_notes = [
        "# TZPID Phase 3 Release Notes",
        "",
        f"Generated UTC: {generated}",
        f"Commit: `{commit}`",
        f"Branch: `{branch}`",
        f"Remote: `{remote or 'not configured'}`",
        "",
        "## Scope",
        "",
        "This package freezes the Phase 2 proof/certificate substrate as a Phase 3 publication-and-release bundle. It does not claim a first-principles proof of every physical interpretation; it packages the current semantic carriers, formal obligations, computational certificates, and paper-facing spine documents in a reproducible form.",
        "",
        "## Included Release Lanes",
        "",
        "- Isabelle/HOL session copy in `isabelle/`.",
        "- Phase 2 completion and semantic matrices in `matrices/`.",
        "- Python/Wolfram/HDF5 certificate artifacts in `certificates/`, `wolfram/`, and `HDF5_ARTIFACTS.*`.",
        "- Paper-facing spine documents and obligations in `spines/`.",
        "- Lean/Rocq exported scaffolds in `exports/`.",
        "- Paper package index and available paper source/PDF in `papers/`.",
        "- Zenodo and citation metadata in `ZENODO_METADATA.json` and `CITATION.cff`.",
        "",
        "## Completion Snapshot",
        "",
        f"- Matrix rows: `{len(rows)}`",
        f"- Clean Isabelle rows: `{sum(row['isabelle_checked'] == 'clean_build' for row in rows)}`",
        f"- Rows with certificate lane: `{sum(bool(row['wolfram_certificate']) and row['wolfram_certificate'] != 'not_attached' for row in rows)}`",
        f"- Rows with missing files: `{sum(bool(row['missing_files']) for row in rows)}`",
        "",
        "## Finalization Notes",
        "",
        "A final release tag should be pushed only after running the commands in `VERIFY.md` and confirming the generated commit matches the intended archive state.",
        "",
    ]
    (RELEASE / "RELEASE_NOTES.md").write_text("\n".join(release_notes), encoding="utf-8")

    zenodo = {
        "title": "TZPID Proof Pipeline Phase 3 Release Package",
        "upload_type": "publication",
        "publication_type": "other",
        "creators": [
            {
                "name": "Trawin, Daniel Alexander",
                "orcid": "0009-0001-4630-3715",
            }
        ],
        "description": (
            "Phase 3 reproducible proof package for the TZPID proof pipeline, "
            "including Isabelle/HOL theories, computational certificate artifacts, "
            "gold-spine publication notes, source matrices, and Lean/Rocq export scaffolds."
        ),
        "keywords": [
            "TZPID",
            "Isabelle/HOL",
            "formal verification",
            "computational certificates",
            "hyperspherical enclosure",
            "Bessel spectrum",
            "gyromagnetic movement",
            "Friedmann cosmology",
            "phase locking",
        ],
        "license": "other-open",
        "version": "phase3",
        "doi": DOI,
        "related_identifiers": [
            {
                "identifier": remote or "https://github.com/DanielAlexanderTrawin/tzpid-proof-pipeline",
                "relation": "isSupplementTo",
                "scheme": "url",
            }
        ],
        "generated_utc": generated,
        "git_commit": commit,
    }
    (RELEASE / "ZENODO_METADATA.json").write_text(
        json.dumps(zenodo, indent=2), encoding="utf-8"
    )

    citation = [
        "cff-version: 1.2.0",
        'message: "If you use this proof package, please cite it using this metadata."',
        'title: "TZPID Proof Pipeline Phase 3 Release Package"',
        "authors:",
        "  - family-names: Trawin",
        "    given-names: Daniel Alexander",
        "    orcid: https://orcid.org/0009-0001-4630-3715",
        f"doi: {DOI}",
        "version: phase3",
        "date-released: 2026-06-09",
        f"url: {remote or 'https://github.com/DanielAlexanderTrawin/tzpid-proof-pipeline'}",
        "repository-code: https://github.com/DanielAlexanderTrawin/tzpid-proof-pipeline",
        "",
    ]
    (RELEASE / "CITATION.cff").write_text("\n".join(citation), encoding="utf-8")


def write_paper_package_index(copied_papers: list[dict], rows: list[dict[str, str]]) -> None:
    lines = [
        "# Phase 3 Paper Package Index",
        "",
        "This folder collects paper-facing material available at release time. The spine documents in `../spines/` are the main manuscript-facing substrate; copied `.tex` and `.pdf` files are included when present in the repository root.",
        "",
        "## Included Paper Files",
        "",
    ]
    if copied_papers:
        for item in copied_papers:
            name = Path(item["release_path"]).name
            lines.append(f"- [{name}](../{rel_from_release(item['release_path'])})")
    else:
        lines.append("- No root paper `.tex` or `.pdf` files were present when the package was generated.")
    lines.extend(
        [
            "",
            "## Paper-Facing Spine Families",
            "",
            "| Family | Kind | Completion | Priority |",
            "|---|---|---|---|",
        ]
    )
    for row in rows:
        if row["kind"] != "batch":
            lines.append(
                f"| {row['family']} | {row['kind']} | `{row['completion_state']}` | {row['paper_priority']} |"
            )
    lines.append("")
    (RELEASE / "papers" / "PAPER_PACKAGE_INDEX.md").parent.mkdir(
        parents=True, exist_ok=True
    )
    (RELEASE / "papers" / "PAPER_PACKAGE_INDEX.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )


def write_export_notes(copied_exports: list[dict]) -> None:
    lines = [
        "# Lean/Rocq Export Lane",
        "",
        "These files are exported scaffolds/mirrors for portability and independent-check lanes. Isabelle/HOL remains the primary checked proof lane for this release unless a Lean or Rocq compiler artifact is present beside the source.",
        "",
        "## Included Files",
        "",
    ]
    if copied_exports:
        for item in sorted(copied_exports, key=lambda entry: entry["release_path"]):
            name = Path(item["release_path"]).name
            lines.append(f"- [{name}](../{rel_from_release(item['release_path'])})")
    else:
        lines.append("- No Lean/Rocq export files were found.")
    lines.extend(
        [
            "",
            "## Status Convention",
            "",
            "- `.lean` and `.v` files are source-level exports.",
            "- `.vo`, `.vos`, `.vok`, and `.glob` files are Rocq/Coq compiler side artifacts when present.",
            "- The export summary JSON records the source registry and generation context.",
            "",
        ]
    )
    (RELEASE / "exports" / "EXPORT_NOTES.md").parent.mkdir(parents=True, exist_ok=True)
    (RELEASE / "exports" / "EXPORT_NOTES.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )


def normalize_packaged_wolfram_scripts() -> None:
    replacements = {
        "If[!DirectoryQ[DirectoryName[outputPath]], CreateDirectory[DirectoryName[outputPath], CreateIntermediateDirectories -> True]];":
            "outputDir = DirectoryName[outputPath];\nIf[StringLength[outputDir] > 0 && ! DirectoryQ[outputDir], CreateDirectory[outputDir, CreateIntermediateDirectories -> True]];",
        "If[! DirectoryQ[DirectoryName[outputPath]], CreateDirectory[DirectoryName[outputPath], CreateIntermediateDirectories -> True]];":
            "outputDir = DirectoryName[outputPath];\nIf[StringLength[outputDir] > 0 && ! DirectoryQ[outputDir], CreateDirectory[outputDir, CreateIntermediateDirectories -> True]];",
    }
    for path in sorted((RELEASE / "wolfram").glob("*.wl")):
        text = path.read_text(encoding="utf-8")
        updated = text
        default_result_names = {
            "bessel_residual_spinal_tap_checks.wl": "bessel_residual_spinal_tap_results.json",
            "gyromagnetic_movement_checks.wl": "gyromagnetic_movement_results.json",
            "phase_locking_resonance_checks.wl": "phase_locking_resonance_results.json",
            "nested_hypersphere_checks.wl": "nested_hypersphere_results.json",
        }
        if path.name in default_result_names:
            old_default = f'"{default_result_names[path.name]}"'
            if path.name == "nested_hypersphere_checks.wl":
                old_default = '"wolfram_checks/nested_hypersphere_results.json"'
            new_default = (
                'FileNameJoin[{DirectoryName[$InputFileName], "..", '
                f'"wolfram_results", "{default_result_names[path.name]}"'
                "}]"
            )
            updated = updated.replace(old_default, new_default)
        for old, new in replacements.items():
            updated = updated.replace(old, new)
        if updated != text:
            path.write_text(updated, encoding="utf-8")
    for result_path in sorted((RELEASE / "wolfram").glob("*_results.json")):
        result_path.unlink()


def write_readme(rows: list[dict[str, str]]) -> None:
    commit = try_git(["rev-parse", "HEAD"])
    branch = try_git(["branch", "--show-current"], "unknown")
    remote = try_git(["remote", "get-url", "origin"], "")
    generated = utc_now()
    lines = [
        "# TZPID Phase 3 Release Package",
        "",
        f"Creator: {CREATOR}",
        f"ORCID: {ORCID}",
        f"Generated UTC: {generated}",
        f"Generated from commit: `{commit}`",
        f"Branch: `{branch}`",
        f"Remote: `{remote or 'not configured'}`",
        "",
        "## Purpose",
        "",
        "This folder is the Phase 3 publication/release package for the TZPID proof pipeline. It bundles the checked Isabelle/HOL session, semantic matrix, computational certificates, paper-facing spines, export scaffolds, and verification instructions needed to reproduce the current proof state.",
        "",
        "## Core Status",
        "",
        f"- Matrix rows: `{len(rows)}`",
        f"- Clean Isabelle rows: `{sum(row['isabelle_checked'] == 'clean_build' for row in rows)}`",
        f"- Rows with certificate lane: `{sum(bool(row['wolfram_certificate']) and row['wolfram_certificate'] != 'not_attached' for row in rows)}`",
        f"- Rows with missing files: `{sum(bool(row['missing_files']) for row in rows)}`",
        "",
        "## Entry Points",
        "",
        "- Verification commands: `VERIFY.md`",
        "- Verification appendix: `VERIFICATION_APPENDIX.md`",
        "- Spine pack index: `SPINE_PACK.md`",
        "- Certificate manifest: `CERTIFICATE_MANIFEST.md`",
        "- HDF5 artifact manifest: `HDF5_ARTIFACTS.md`",
        "- Release notes: `RELEASE_NOTES.md`",
        "- Paper package index: `papers/PAPER_PACKAGE_INDEX.md`",
        "- Export lane notes: `exports/EXPORT_NOTES.md`",
        "- Zenodo metadata: `ZENODO_METADATA.json`",
        "- Citation metadata: `CITATION.cff`",
        "",
        "## Release Folder Layout",
        "",
        "- `matrices/`: copied Phase 2 completion and semantic-translation matrices.",
        "- `certificates/`: copied certificate JSON, Markdown, and CSV outputs.",
        "- `isabelle/`: copied Isabelle theories and session `ROOT`.",
        "- `spines/`: copied paper-facing spine Markdown and obligations CSV files.",
        "- `wolfram/`: copied Wolfram check scripts from the spine workspace.",
        "- `wolfram_results/`: copied Wolfram result JSON files.",
        "- `exports/`: copied Lean/Rocq export lane artifacts.",
        "- `papers/`: paper-facing index plus available root `.tex`/`.pdf` manuscript files.",
        "",
    ]
    (RELEASE / "README.md").write_text("\n".join(lines), encoding="utf-8")


def write_verify() -> None:
    commit = try_git(["rev-parse", "HEAD"])
    generated = utc_now()
    lines = [
        "# TZPID Phase 3 Verification Guide",
        "",
        f"Generated UTC: {generated}",
        f"Generated from commit: `{commit}`",
        "",
        "Run these commands from `d:\\tzpidNEW`.",
        "",
        "## 1. Isabelle/HOL Build",
        "",
        "```powershell",
        "& 'D:\\Isabelle2025\\Isabelle2025-2\\bin\\isabelle' build -v -D 'd:\\tzpidNEW\\isabelle_tzpid'",
        "```",
        "",
        "Pass condition: command exits with code `0`.",
        "",
        "## 2. Regenerate The Phase 2 Matrix",
        "",
        "```powershell",
        "python .\\build_phase2_completion_matrix.py",
        "```",
        "",
        "Then verify there are no incomplete, missing, or unattached rows:",
        "",
        "```powershell",
        "Import-Csv .\\TZPID_PHASE2_COMPLETION_MATRIX.csv |",
        "  Where-Object { $_.completion_state -eq 'started_not_complete' -or $_.missing_files -ne '' -or $_.isabelle_checked -ne 'clean_build' -or $_.wolfram_certificate -eq 'not_attached' } |",
        "  Format-Table -AutoSize",
        "```",
        "",
        "Pass condition: no rows are printed.",
        "",
        "## 3. Regenerate Certificate Scripts",
        "",
        "```powershell",
        "$scripts = Get-ChildItem -File -Filter 'compute_*certificate*.py' | Sort-Object Name",
        "foreach ($s in $scripts) {",
        "  Write-Host \"RUN $($s.Name)\"",
        "  python $s.FullName",
        "  if ($LASTEXITCODE -ne 0) { throw \"Certificate failed: $($s.Name)\" }",
        "}",
        "```",
        "",
        "Pass condition: every script exits with code `0`.",
        "",
        "## 4. Check Certificate JSON Status Fields",
        "",
        "```powershell",
        "python -c \"import json; from pathlib import Path; bad=[]; count=0",
        "for path in Path('phase2_checks').glob('*CERTIFICATE.json'):",
        "    count += 1; data=json.loads(path.read_text(encoding='utf-8'))",
        "    def walk(obj, trail=''):",
        "        if isinstance(obj, dict):",
        "            for k,v in obj.items(): yield from walk(v, f'{trail}.{k}' if trail else k)",
        "        elif isinstance(obj, list):",
        "            for i,v in enumerate(obj): yield from walk(v, f'{trail}[{i}]')",
        "        else: yield trail, obj",
        "    for trail, value in walk(data):",
        "        if value == 'fail': bad.append((str(path), trail))",
        "print(f'certificate_json_files={count}')",
        "assert not bad, bad",
        "print('all certificate JSON status fields pass')\"",
        "```",
        "",
        "Pass condition: `all certificate JSON status fields pass`.",
        "",
        "## 5. Validate Release JSON",
        "",
        "```powershell",
        "python -m json.tool .\\release_phase3\\MANIFEST.json > $null",
        "python -m json.tool .\\release_phase3\\CERTIFICATE_MANIFEST.json > $null",
        "python -m json.tool .\\release_phase3\\HDF5_ARTIFACTS.json > $null",
        "python -m json.tool .\\release_phase3\\ZENODO_METADATA.json > $null",
        "```",
        "",
        "Pass condition: every command exits with code `0`.",
        "",
        "## 6. Git And Release Account Check",
        "",
        "```powershell",
        "git status --short --branch",
        "git remote -v",
        "git log -3 --oneline",
        "```",
        "",
        "Expected remote: `https://github.com/DanielAlexanderTrawin/tzpid-proof-pipeline.git`.",
        "",
        "Expected note: user working notes may remain untracked until intentionally added:",
        "",
        "- `fithflip.txt`",
        "- `hyper-universality.txt`",
        "- `key_nondimensional_numbers.txt`",
        "",
    ]
    (RELEASE / "VERIFY.md").write_text("\n".join(lines), encoding="utf-8")


def update_manifest(package_files: dict[str, list[dict]]) -> None:
    path = RELEASE / "MANIFEST.json"
    rows = read_matrix()
    commit = try_git(["rev-parse", "HEAD"])
    branch = try_git(["branch", "--show-current"], "unknown")
    remote = try_git(["remote", "get-url", "origin"], "")
    manifest = {
        "release": "TZPID Phase 3 proof package",
        "generated_utc": utc_now(),
        "creator": CREATOR,
        "orcid": ORCID,
        "doi": DOI,
        "repository": {
            "path": str(ROOT),
            "branch": branch,
            "generated_from_commit": commit,
            "remote": remote or None,
            "local_git_user": {
                "name": try_git(["config", "--get", "user.name"], ""),
                "email": try_git(["config", "--get", "user.email"], ""),
            },
        },
        "toolchain": {
            "isabelle_session": "isabelle_tzpid",
            "python_certificate_scripts": len(
                list(ROOT.glob("compute_*certificate*.py"))
            ),
            "wolfram_scripts": len(list((RELEASE / "wolfram").glob("*.wl"))),
        },
        "phase2_matrix": {
            "file": "TZPID_PHASE2_COMPLETION_MATRIX.csv",
            "row_count": len(rows),
            "completion_states": sorted(
                set(row["completion_state"] for row in rows)
            ),
            "all_rows_clean_build": all(
                row["isabelle_checked"] == "clean_build" for row in rows
            ),
            "all_rows_have_certificate_lane": all(
                bool(row["wolfram_certificate"])
                and row["wolfram_certificate"] != "not_attached"
                for row in rows
            ),
            "all_rows_have_files": all(not row["missing_files"] for row in rows),
        },
        "matrix_rows": rows,
    }
    manifest["phase3_package"] = {
        "generated_utc": utc_now(),
        "package_commit_source": commit,
        "directories": {
            "matrices": "release_phase3/matrices",
            "certificates": "release_phase3/certificates",
            "isabelle": "release_phase3/isabelle",
            "spines": "release_phase3/spines",
            "wolfram": "release_phase3/wolfram",
            "wolfram_results": "release_phase3/wolfram_results",
            "exports": "release_phase3/exports",
            "papers": "release_phase3/papers",
        },
        "files": package_files,
    }
    path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def main() -> None:
    RELEASE.mkdir(exist_ok=True)
    package_files: dict[str, list[dict]] = {
        "matrices": [],
        "certificates": [],
        "isabelle": [],
        "spines": [],
        "wolfram": [],
        "wolfram_results": [],
        "exports": [],
        "papers": [],
    }

    for name in [
        "TZPID_PHASE2_COMPLETION_MATRIX.csv",
        "TZPID_PHASE2_COMPLETION_MATRIX.json",
        "TZPID_PHASE2_COMPLETION_MATRIX.md",
        "TZPID_PHASE2_SEMANTIC_TRANSLATION.md",
    ]:
        src = ROOT / name
        if src.exists():
            package_files["matrices"].append(
                copy_file(src, RELEASE / "matrices" / src.name)
            )

    for src in sorted((ROOT / "phase2_checks").glob("*CERTIFICATE.*")):
        suffix_dir = src.suffix.lower().lstrip(".")
        package_files["certificates"].append(
            copy_file(src, RELEASE / "certificates" / suffix_dir / src.name)
        )
    for src in sorted((ROOT / "phase2_checks").glob("*_GRID.csv")):
        package_files["certificates"].append(
            copy_file(src, RELEASE / "certificates" / "csv" / src.name)
        )
    for src in sorted((ROOT / "phase2_checks").glob("*_ANCHORS.csv")):
        package_files["certificates"].append(
            copy_file(src, RELEASE / "certificates" / "csv" / src.name)
        )

    for src in sorted((ROOT / "isabelle_tzpid").glob("*.thy")):
        package_files["isabelle"].append(copy_file(src, RELEASE / "isabelle" / src.name))
    package_files["isabelle"].append(
        copy_file(ROOT / "isabelle_tzpid" / "ROOT", RELEASE / "isabelle" / "ROOT")
    )

    if SPINE_SOURCE.exists():
        for src in sorted(SPINE_SOURCE.glob("*.md")):
            package_files["spines"].append(copy_file(src, RELEASE / "spines" / src.name))
        for src in sorted(SPINE_SOURCE.glob("*obligations.csv")):
            package_files["spines"].append(copy_file(src, RELEASE / "spines" / src.name))
        for src in sorted((SPINE_SOURCE / "wolfram").glob("*.wl")):
            package_files["wolfram"].append(copy_file(src, RELEASE / "wolfram" / src.name))
    normalize_packaged_wolfram_scripts()

    wolfram_result_sources: list[Path] = []
    wolfram_result_sources.extend(sorted(ROOT.glob("*_results.json")))
    wolfram_result_sources.extend(sorted((ROOT / "wolfram_checks").glob("*_results.json")))
    wolfram_result_sources.extend(sorted((RELEASE / "wolfram").glob("*_results.json")))
    wolfram_result_sources.extend(sorted((RELEASE / "wolfram_results").glob("*_results.json")))
    seen_wolfram_results: set[str] = set()
    for src in wolfram_result_sources:
        if not src.exists() or src.name in seen_wolfram_results:
            continue
        seen_wolfram_results.add(src.name)
        dst = RELEASE / "wolfram_results" / src.name
        if src.resolve() == dst.resolve():
            package_files["wolfram_results"].append(register_release_file(src))
        else:
            package_files["wolfram_results"].append(copy_file(src, dst))

    export_source = ROOT / "lean_rocq_gold_spine"
    if export_source.exists():
        for src in sorted(export_source.glob("*")):
            if src.is_file():
                package_files["exports"].append(
                    copy_file(src, RELEASE / "exports" / src.name)
                )

    for src in [
        ROOT / "What_Matters_Most_Finding_Time_In_A_temporal_HyperSpherical_Zenith.tex",
        ROOT / "What_Matters_Most_Finding_Time_In_A_temporal_HyperSpherical_Zenith.pdf",
    ]:
        if src.exists():
            package_files["papers"].append(copy_file(src, RELEASE / "papers" / src.name))

    rows = read_matrix()
    write_readme(rows)
    write_verify()
    write_verification_appendix(rows)
    write_certificate_manifest(package_files["certificates"])
    write_hdf5_manifest()
    write_export_notes(package_files["exports"])
    write_paper_package_index(package_files["papers"], rows)
    write_release_metadata(rows)
    write_spine_pack(rows, package_files["spines"])
    update_manifest(package_files)
    print("phase3 release package refreshed")


if __name__ == "__main__":
    main()
