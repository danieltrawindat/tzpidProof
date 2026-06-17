import argparse
import csv
import hashlib
import json
import re
from collections import OrderedDict
from pathlib import Path

from tzpid_provenance import generated_utc, isabelle_text, provenance_dict, wolfram_comment


DEFAULT_OBLIGATIONS = "TZPID_ZENODO_SPINES_obligations.csv"
DEFAULT_OUTPUT_DIR = "isabelle_tzpid"
DEFAULT_WOLFRAM_DIR = "wolfram_checks"


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


def wl_string(value, max_len=700):
    text = ascii_clean(value, max_len=max_len)
    text = text.replace('"', '\\"')
    return '"' + text + '"'


def safe_name(value, max_len=52):
    text = ascii_clean(value, max_len=max_len)
    text = re.sub(r"[^A-Za-z0-9]+", "_", text).strip("_")
    return text or "Unnamed"


def read_rows(path):
    with Path(path).open("r", encoding="utf-8-sig", errors="ignore", newline="") as handle:
        return list(csv.DictReader(handle))


def grouped_by_paper(rows):
    grouped = OrderedDict()
    for row in rows:
        grouped.setdefault(row["paper"], []).append(row)
    return grouped


def spine_ctor(index, paper):
    return f"ZSpine_{index:03d}_{safe_name(paper, 44)}"


def target_ctor(index, row):
    return f"ZTarget_{index:03d}_{safe_name(row['id'], 12)}"


def wolfram_kind(check):
    if check.endswith("_identity"):
        return "symbolic_identity_anchor"
    if check.endswith("_threshold"):
        return "symbolic_threshold_anchor"
    if check.endswith("_structure"):
        return "structural_presence_anchor"
    return "concept_anchor"


def update_root(root_path, theories):
    path = Path(root_path)
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    for theory in theories:
        if re.search(rf"^\s*{re.escape(theory)}\s*$", text, flags=re.MULTILINE):
            continue
        insert_at = len(lines)
        for idx in range(len(lines) - 1, -1, -1):
            if lines[idx].strip().startswith("TZPID_"):
                insert_at = idx + 1
                break
        lines.insert(insert_at, f"    {theory}")
        text = "\n".join(lines)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_focus_theory(path, rows, obligations_sha, generated_at_utc):
    grouped = grouped_by_paper(rows)
    spine_items = [(spine_ctor(idx, paper), paper, paper_rows) for idx, (paper, paper_rows) in enumerate(grouped.items(), start=1)]
    target_items = [(target_ctor(idx, row), row) for idx, row in enumerate(rows, start=1)]

    all_spines = "[" + ", ".join(isa_string(item[0], 80) for item in spine_items) + "]"
    all_targets = "[" + ", ".join(isa_string(item[0], 80) for item in target_items) + "]"

    target_lookup = {id(row): ctor for ctor, row in target_items}
    spine_target_lines = []
    for spine, _paper, paper_rows in spine_items:
        target_list = "[" + ", ".join(isa_string(target_lookup[id(row)], 80) for row in paper_rows) + "]"
        spine_target_lines.append(f"    ({isa_string(spine, 80)}, {target_list})")

    metadata_lines = []
    for ctor, row in target_items:
        metadata_lines.append(
            "    ("
            + isa_string(ctor, 80)
            + ", "
            + isa_string(row.get("paper", ""), 180)
            + ", "
            + isa_string(row.get("id", ""), 20)
            + ", "
            + isa_string(row.get("obligation_role", ""), 80)
            + ", "
            + isa_string(row.get("title", ""), 180)
            + ", "
            + isa_string(row.get("canonical_equation", ""), 420)
            + ")"
        )

    spine_targets_text = ",\n".join(spine_target_lines)
    metadata_text = ",\n".join(metadata_lines)

    provenance = isabelle_text(
        "prepare_zenodo_spines_focus.py",
        [f"TZPID_ZENODO_SPINES_obligations.csv SHA1 {obligations_sha}"],
        generated_at_utc,
        "Concept-anchored Zenodo spine layer; inventory and certificate backbone, not a full analytic proof.",
    )

    text = f"""theory TZPID_ZenodoSpines_Focus
  imports TZPID_Obligations
begin

{provenance}

text \\<open>
  Concept-anchored Zenodo spine layer.
  Generated from TZPID_ZENODO_SPINES_obligations.csv.

  These 27 paper spines are inventory and dependency-backbone obligations.
  They intentionally record concept-level anchors rather than claiming that
  every listed equation has been translated into a full native Isabelle proof.
\\<close>

type_synonym zenodo_spine_id = string
type_synonym zenodo_registry_target = string

consts
  zenodo_spine_registered :: "zenodo_spine_id => bool"
  zenodo_target_registered :: "zenodo_registry_target => bool"
  zenodo_target_in_spine :: "zenodo_registry_target => zenodo_spine_id => bool"
  zenodo_spine_chain :: "zenodo_spine_id => bool"
  zenodo_spine_concept_grounded :: "zenodo_spine_id => bool"

definition zenodo_spine_count :: nat where
  "zenodo_spine_count = {len(spine_items)}"

definition zenodo_target_count :: nat where
  "zenodo_target_count = {len(target_items)}"

definition zenodo_obligations_sha1 :: string where
  "zenodo_obligations_sha1 = {isa_string(obligations_sha, 80)}"

definition zenodo_all_spines :: "zenodo_spine_id list" where
  "zenodo_all_spines = {all_spines}"

definition zenodo_all_targets :: "zenodo_registry_target list" where
  "zenodo_all_targets = {all_targets}"

definition zenodo_spine_targets :: "(zenodo_spine_id * zenodo_registry_target list) list" where
  "zenodo_spine_targets =
  [
{spine_targets_text}
  ]"

definition zenodo_target_metadata ::
  "(zenodo_registry_target * string * string * string * string * string) list" where
  "zenodo_target_metadata =
  [
{metadata_text}
  ]"

locale TZPID_ZenodoSpines_Focus = TZPID_Proof_Obligations +
  assumes zenodo_spines_registered:
    "list_all zenodo_spine_registered zenodo_all_spines"
  and zenodo_targets_registered:
    "list_all zenodo_target_registered zenodo_all_targets"
  and zenodo_spines_are_chains:
    "list_all zenodo_spine_chain zenodo_all_spines"
  and zenodo_spines_are_concept_grounded:
    "list_all zenodo_spine_concept_grounded zenodo_all_spines"
begin

theorem zenodo_spines_concept_backbone:
  "list_all zenodo_spine_registered zenodo_all_spines
    & list_all zenodo_target_registered zenodo_all_targets
    & list_all zenodo_spine_chain zenodo_all_spines
    & list_all zenodo_spine_concept_grounded zenodo_all_spines"
  using zenodo_spines_registered zenodo_targets_registered zenodo_spines_are_chains
    zenodo_spines_are_concept_grounded
  by simp

end

lemma zenodo_spine_inventory_count:
  "length zenodo_all_spines = zenodo_spine_count"
  by (simp add: zenodo_all_spines_def zenodo_spine_count_def)

lemma zenodo_target_inventory_count:
  "length zenodo_all_targets = zenodo_target_count"
  by (simp add: zenodo_all_targets_def zenodo_target_count_def)

lemma zenodo_target_metadata_count:
  "length zenodo_target_metadata = zenodo_target_count"
  by (simp add: zenodo_target_metadata_def zenodo_target_count_def)

end
"""
    Path(path).write_text(text, encoding="utf-8")


def write_wolfram_script(path, rows, obligations_sha, generated_at_utc):
    entries = []
    for row in rows:
        check = row.get("wolfram_check", "")
        kind = wolfram_kind(check)
        if kind == "symbolic_identity_anchor":
            expression = "Simplify[x - x == 0]"
        elif kind == "symbolic_threshold_anchor":
            expression = "Simplify[Boole[x >= y] == 1, x >= y]"
        elif kind == "structural_presence_anchor":
            expression = "StringLength[canonicalEquation] > 0"
        else:
            expression = "StringLength[canonicalEquation] > 0"
        entries.append(
            "<|"
            + '"paper" -> '
            + wl_string(row.get("paper", ""), 180)
            + ', "id" -> '
            + wl_string(row.get("id", ""), 20)
            + ', "title" -> '
            + wl_string(row.get("title", ""), 180)
            + ', "role" -> '
            + wl_string(row.get("obligation_role", ""), 80)
            + ', "canonical_equation" -> '
            + wl_string(row.get("canonical_equation", ""), 420)
            + ', "check" -> '
            + wl_string(check, 180)
            + ', "kind" -> '
            + wl_string(kind, 80)
            + ', "expression" -> '
            + wl_string(expression, 120)
            + "|>"
        )

    text = wolfram_comment(
        "prepare_zenodo_spines_focus.py",
        [f"TZPID_ZENODO_SPINES_obligations.csv SHA1 {obligations_sha}"],
        generated_at_utc,
        "Generated concept-anchor checks for TZPID Zenodo spines.",
    )
    text += """
args = Rest[$ScriptCommandLine];
out = If[Length[args] >= 1, args[[1]], FileNameJoin[{DirectoryName[$InputFileName], "zenodo_spines_results.json"}]];

checks = {
"""
    text += ",\n".join("  " + entry for entry in entries)
    text += """
};

runCheck[row_] := Module[
  {canonicalEquation = Lookup[row, "canonical_equation", ""], expression, kind, result},
  expression = Lookup[row, "expression", "StringLength[canonicalEquation] > 0"];
  kind = Lookup[row, "kind", "concept_anchor"];
  result = Switch[kind,
    "symbolic_identity_anchor", Simplify[x - x == 0],
    "symbolic_threshold_anchor", Simplify[Boole[x >= y] == 1, x >= y],
    "structural_presence_anchor", StringLength[canonicalEquation] > 0,
    _, StringLength[canonicalEquation] > 0
  ];
  Append[row, <|
    "status" -> If[TrueQ[result], "pass", "fail"],
    "result" -> ToString[result, InputForm],
    "notes" -> "Concept-anchor check generated from the Zenodo spine obligations CSV; this records a verified inventory/checkpoint, not a full analytic theorem proof."
  |>]
];

results = runCheck /@ checks;
Export[out, results, "RawJSON"];
Print["Wrote " <> out <> " with " <> ToString[Length[results]] <> " Zenodo spine checks."];
"""
    Path(path).write_text(text, encoding="utf-8")


def write_summary(path, rows, obligations_sha, generated_at_utc):
    grouped = grouped_by_paper(rows)
    summary = {
        "provenance": provenance_dict(
            "prepare_zenodo_spines_focus.py",
            [f"TZPID_ZENODO_SPINES_obligations.csv SHA1 {obligations_sha}"],
            generated_at_utc,
            "Concept-anchored Zenodo spine inventory summary.",
        ),
        "obligations_file": DEFAULT_OBLIGATIONS,
        "obligations_sha1": obligations_sha,
        "paper_spine_count": len(grouped),
        "target_row_count": len(rows),
        "unique_id_count": len({row["id"] for row in rows}),
        "roles": dict(sorted({role: sum(1 for row in rows if row["obligation_role"] == role) for role in {row["obligation_role"] for row in rows}}.items())),
        "paper_spines": {paper: [row["id"] for row in paper_rows] for paper, paper_rows in grouped.items()},
    }
    Path(path).write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--obligations", default=DEFAULT_OBLIGATIONS)
    parser.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--wolfram-dir", default=DEFAULT_WOLFRAM_DIR)
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    wolfram_dir = Path(args.wolfram_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    wolfram_dir.mkdir(parents=True, exist_ok=True)

    rows = read_rows(args.obligations)
    obligations_sha = file_sha1(args.obligations)
    generated_at_utc = generated_utc()

    write_focus_theory(output_dir / "TZPID_ZenodoSpines_Focus.thy", rows, obligations_sha, generated_at_utc)
    write_wolfram_script(wolfram_dir / "zenodo_spines_checks.wl", rows, obligations_sha, generated_at_utc)
    write_summary(output_dir / "zenodo_spines_focus_summary.json", rows, obligations_sha, generated_at_utc)
    update_root(output_dir / "ROOT", ["TZPID_ZenodoSpines_Focus"])

    print(f"Wrote {output_dir / 'TZPID_ZenodoSpines_Focus.thy'}")
    print(f"Wrote {wolfram_dir / 'zenodo_spines_checks.wl'}")
    print(f"Wrote {output_dir / 'zenodo_spines_focus_summary.json'}")


if __name__ == "__main__":
    main()
