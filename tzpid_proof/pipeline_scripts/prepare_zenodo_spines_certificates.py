import argparse
import hashlib
import json
import re
from pathlib import Path

from tzpid_provenance import generated_utc, isabelle_text, provenance_dict


DEFAULT_RESULTS = "wolfram_checks/zenodo_spines_results.json"
DEFAULT_OUTPUT_DIR = "isabelle_tzpid"


def file_sha1(path):
    digest = hashlib.sha1()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def ascii_clean(value, max_len=700):
    text = "" if value is None else str(value)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = text.replace("\\", "/")
    text = text.replace('"', "")
    text = text.replace("'", "")
    text = text.replace("''", "'")
    text = re.sub(r"\s+", " ", text).strip()
    return text[:max_len]


def isa_string(value, max_len=700):
    return "''" + ascii_clean(value, max_len=max_len) + "''"


def safe_name(value, max_len=32):
    text = ascii_clean(value, max_len=max_len)
    text = re.sub(r"[^A-Za-z0-9]+", "_", text).strip("_")
    return text or "Unnamed"


def check_ctor(index, row):
    return f"ZCheck_{index:03d}_{safe_name(row.get('id', ''), 12)}"


def update_root(root_path, theories):
    path = Path(root_path)
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    for theory in theories:
        if re.search(rf"^\s*{re.escape(theory)}\s*$", "\n".join(lines), flags=re.MULTILINE):
            continue
        insert_at = len(lines)
        for idx in range(len(lines) - 1, -1, -1):
            if lines[idx].strip().startswith("TZPID_"):
                insert_at = idx + 1
                break
        lines.insert(insert_at, f"    {theory}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_theory(path, rows, results_sha, generated_at_utc):
    check_items = [(check_ctor(idx, row), row) for idx, row in enumerate(rows, start=1)]
    all_checks = "[" + ", ".join(isa_string(ctor, 80) for ctor, _row in check_items) + "]"

    metadata_lines = []
    for ctor, row in check_items:
        metadata_lines.append(
            "    ("
            + isa_string(ctor, 80)
            + ", "
            + isa_string(row.get("paper", ""), 180)
            + ", "
            + isa_string(row.get("id", ""), 20)
            + ", "
            + isa_string(row.get("check", ""), 180)
            + ", "
            + isa_string(row.get("kind", ""), 80)
            + ", "
            + isa_string(row.get("status", ""), 80)
            + ")"
        )

    metadata_text = ",\n".join(metadata_lines)

    provenance = isabelle_text(
        "prepare_zenodo_spines_certificates.py",
        [f"wolfram_checks/zenodo_spines_results.json SHA1 {results_sha}"],
        generated_at_utc,
        "Wolfram-backed concept-anchor certificate layer for Zenodo spines.",
    )

    text = f"""theory TZPID_ZenodoSpines_Computational_Checks
  imports TZPID_ZenodoSpines_Focus
begin

{provenance}

text \\<open>
  Wolfram-backed concept-anchor certificate layer for the Zenodo spines.
  The checks are generated inventory checkpoints over the 189 Zenodo spine
  obligations, not full native analytic proofs of every source equation.
\\<close>

type_synonym zenodo_wolfram_check = string

definition zenodo_wolfram_results_sha1 :: string where
  "zenodo_wolfram_results_sha1 = {isa_string(results_sha, 80)}"

definition zenodo_wolfram_check_count :: nat where
  "zenodo_wolfram_check_count = {len(check_items)}"

definition zenodo_wolfram_pass_count :: nat where
  "zenodo_wolfram_pass_count = {sum(1 for _ctor, row in check_items if row.get('status') == 'pass')}"

definition zenodo_all_wolfram_checks :: "zenodo_wolfram_check list" where
  "zenodo_all_wolfram_checks = {all_checks}"

definition zenodo_wolfram_check_metadata ::
  "(zenodo_wolfram_check * string * string * string * string * string) list" where
  "zenodo_wolfram_check_metadata =
  [
{metadata_text}
  ]"

lemma zenodo_wolfram_inventory_count:
  "length zenodo_all_wolfram_checks = zenodo_wolfram_check_count"
  by (simp add: zenodo_all_wolfram_checks_def zenodo_wolfram_check_count_def)

lemma zenodo_wolfram_metadata_count:
  "length zenodo_wolfram_check_metadata = zenodo_wolfram_check_count"
  by (simp add: zenodo_wolfram_check_metadata_def zenodo_wolfram_check_count_def)

lemma zenodo_wolfram_pass_count_complete:
  "zenodo_wolfram_pass_count = zenodo_wolfram_check_count"
  by (simp add: zenodo_wolfram_pass_count_def zenodo_wolfram_check_count_def)

lemma zenodo_wolfram_checks_match_targets:
  "zenodo_wolfram_check_count = zenodo_target_count"
  by (simp add: zenodo_wolfram_check_count_def zenodo_target_count_def)

context TZPID_ZenodoSpines_Focus
begin

theorem zenodo_spines_have_wolfram_certificate:
  "zenodo_wolfram_pass_count = zenodo_target_count
    & zenodo_wolfram_check_count = zenodo_target_count
    & zenodo_spine_count = {len({row.get('paper', '') for _ctor, row in check_items})}
    & zenodo_target_count = {len(check_items)}
    & list_all zenodo_spine_registered zenodo_all_spines
    & list_all zenodo_target_registered zenodo_all_targets"
  using zenodo_spines_concept_backbone
  by (simp add: zenodo_wolfram_pass_count_def zenodo_wolfram_check_count_def
      zenodo_spine_count_def zenodo_target_count_def)

end

end
"""
    Path(path).write_text(text, encoding="utf-8")


def write_summary(path, rows, results_sha, generated_at_utc):
    pass_count = sum(1 for row in rows if row.get("status") == "pass")
    lines = [
        "# Zenodo Spine Wolfram Certificates",
        "",
        f"Project: TZPID Proof Pipeline",
        f"Creator: Daniel Alexander Trawin",
        f"ORCID: https://orcid.org/0009-0001-4630-3715",
        f"Generator: prepare_zenodo_spines_certificates.py",
        f"Generated UTC: {generated_at_utc}",
        "",
        f"Results SHA1: `{results_sha}`",
        f"Checks: `{len(rows)}`",
        f"Passes: `{pass_count}`",
        "",
        "| Paper | ID | Check | Kind | Status |",
        "|---|---|---|---|---|",
    ]
    for row in rows:
        lines.append(
            "| "
            + ascii_clean(row.get("paper", ""), 120)
            + " | "
            + ascii_clean(row.get("id", ""), 20)
            + " | `"
            + ascii_clean(row.get("check", ""), 140)
            + "` | `"
            + ascii_clean(row.get("kind", ""), 80)
            + "` | `"
            + ascii_clean(row.get("status", ""), 40)
            + "` |"
        )
    Path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--results", default=DEFAULT_RESULTS)
    parser.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    rows = json.loads(Path(args.results).read_text(encoding="utf-8"))
    results_sha = file_sha1(args.results)
    generated_at_utc = generated_utc()

    write_theory(output_dir / "TZPID_ZenodoSpines_Computational_Checks.thy", rows, results_sha, generated_at_utc)
    write_summary(output_dir / "zenodo_spines_wolfram_certificate_summary.md", rows, results_sha, generated_at_utc)
    update_root(output_dir / "ROOT", ["TZPID_ZenodoSpines_Computational_Checks"])

    print(f"Wrote {output_dir / 'TZPID_ZenodoSpines_Computational_Checks.thy'}")
    print(f"Wrote {output_dir / 'zenodo_spines_wolfram_certificate_summary.md'}")


if __name__ == "__main__":
    main()
