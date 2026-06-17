import csv
import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\TZPIDProof")
INTAKE = ROOT / "phone2_intake"
THEOREM_DIR = INTAKE / "theorem_toe"
ISABELLE_DIR = ROOT / "tzpid_proof" / "isabelle_tzpid"

THEOREM_QUEUE = THEOREM_DIR / "PHONE2_THEOREM_PRIORITY_QUEUE.csv"
MASTER = ROOT / "TZPID_ALL_IDS_CANONICAL_EQUATION_MASTER_with_export.csv"
ANCHORS = THEOREM_DIR / "PHONE2_THEOREM_ANCHOR_PACK.csv"
ANCHOR_MAP = THEOREM_DIR / "PHONE2_THEOREM_EQUATION_MAP.csv"
REPORT = THEOREM_DIR / "PHONE2_THEOREM_ANCHOR_PACK_REPORT.md"
SUMMARY = THEOREM_DIR / "phone2_theorem_anchor_pack_summary.json"
THY = ISABELLE_DIR / "TZPID_Phone2_Theorem_Anchors.thy"


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def parse_line(formation_inputs: str) -> tuple[str, int]:
    match = re.match(r"(.+?)\s+line\s+(\d+)", formation_inputs or "")
    if not match:
        return formation_inputs or "", 0
    return match.group(1), int(match.group(2))


def parse_domain(row: dict) -> str:
    note = row.get("formation_note", "")
    match = re.search(r"domain=([A-Za-z0-9_]+)", note)
    if match:
        return match.group(1)
    title = row.get("title", "").lower()
    if "quantum" in title:
        return "quantum_entanglement"
    if "category" in title or "type theory" in title:
        return "category_type_theory"
    return "general_semantics"


def status_head(row: dict) -> str:
    return (row.get("wolfram_status") or "").split(";")[0]


def anchor_status(score: int, rank: int) -> str:
    if rank <= 10:
        return "gold_anchor_candidate"
    if score >= 9:
        return "strong_anchor_candidate"
    return "supporting_anchor_candidate"


def choose_anchor(eq: dict, anchors: list[dict]) -> tuple[dict | None, str, int]:
    source = eq["source_file"]
    line = eq["line_number"]
    domain = eq["domain_family"]
    same_source = [a for a in anchors if a["source_file"] == source]
    prior = [a for a in same_source if a["line_number"] <= line]
    if prior:
        best = max(prior, key=lambda a: a["line_number"])
        return best, "nearest_prior_same_source", line - best["line_number"]
    if same_source:
        best = min(same_source, key=lambda a: abs(a["line_number"] - line))
        return best, "nearest_same_source", abs(line - best["line_number"])
    same_domain = [a for a in anchors if a["domain_family"] == domain]
    if same_domain:
        best = min(same_domain, key=lambda a: a["rank"])
        return best, "top_same_domain", -1
    if anchors:
        return anchors[0], "top_global_fallback", -1
    return None, "unmapped", -1


def is_equation_verified(status: str) -> bool:
    return status in {
        "wolfram_equation_parse_verified",
        "wolfram_rescue_equation_parse_verified",
        "wolfram_cleanup_equation_parse_verified",
        "wolfram_gold_anchor_equation_parse_verified",
    }


def main() -> None:
    theorem_rows = []
    with THEOREM_QUEUE.open(encoding="utf-8-sig", newline="") as handle:
        for i, row in enumerate(csv.DictReader(handle), start=1):
            theorem_rows.append(
                {
                    "anchor_id": f"PHONE2_ANCHOR_{i:03d}",
                    "rank": i,
                    "priority_score": int(row.get("priority_score") or 0),
                    "semantic_kind": row.get("semantic_kind", ""),
                    "title": row.get("title", ""),
                    "domain_family": row.get("domain_family", ""),
                    "source_file": row.get("source_file", ""),
                    "line_number": int(row.get("line_number") or 0),
                    "extraction_method": row.get("extraction_method", ""),
                    "anchor_status": anchor_status(int(row.get("priority_score") or 0), i),
                    "block_summary": row.get("block_summary", ""),
                }
            )

    minted = []
    with MASTER.open(encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            try:
                n = int(row["id"][2:])
            except Exception:
                continue
            if 10872 <= n <= 11371:
                source_file, line = parse_line(row.get("formation_inputs", ""))
                minted.append(
                    {
                        "id": row["id"],
                        "title": row.get("title", ""),
                        "source_file": source_file,
                        "line_number": line,
                        "domain_family": parse_domain(row),
                        "wolfram_status": status_head(row),
                        "canonical_equation": row.get("canonical_equation", ""),
                    }
                )

    mappings = []
    anchor_counter = Counter()
    for eq in minted:
        anchor, method, distance = choose_anchor(eq, theorem_rows)
        if anchor:
            anchor_counter[anchor["anchor_id"]] += 1
            mappings.append(
                {
                    "equation_id": eq["id"],
                    "equation_title": eq["title"],
                    "equation_source_file": eq["source_file"],
                    "equation_line_number": eq["line_number"],
                    "equation_domain_family": eq["domain_family"],
                    "wolfram_status": eq["wolfram_status"],
                    "anchor_id": anchor["anchor_id"],
                    "anchor_title": anchor["title"],
                    "anchor_semantic_kind": anchor["semantic_kind"],
                    "anchor_domain_family": anchor["domain_family"],
                    "anchor_source_file": anchor["source_file"],
                    "anchor_line_number": anchor["line_number"],
                    "mapping_method": method,
                    "line_distance": distance,
                }
            )

    for anchor in theorem_rows:
        anchor["mapped_equation_count"] = anchor_counter[anchor["anchor_id"]]

    with ANCHORS.open("w", encoding="utf-8", newline="") as handle:
        fields = [
            "anchor_id",
            "rank",
            "priority_score",
            "semantic_kind",
            "title",
            "domain_family",
            "source_file",
            "line_number",
            "extraction_method",
            "anchor_status",
            "mapped_equation_count",
            "block_summary",
        ]
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(theorem_rows)

    with ANCHOR_MAP.open("w", encoding="utf-8", newline="") as handle:
        fields = [
            "equation_id",
            "equation_title",
            "equation_source_file",
            "equation_line_number",
            "equation_domain_family",
            "wolfram_status",
            "anchor_id",
            "anchor_title",
            "anchor_semantic_kind",
            "anchor_domain_family",
            "anchor_source_file",
            "anchor_line_number",
            "mapping_method",
            "line_distance",
        ]
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(mappings)

    status_counts = Counter(row["wolfram_status"] for row in minted)
    method_counts = Counter(row["mapping_method"] for row in mappings)
    verified = sum(1 for row in minted if is_equation_verified(row["wolfram_status"]))
    expression_verified = sum(1 for row in minted if "expression_parse_verified" in row["wolfram_status"])
    carriers = sum(1 for row in minted if "carrier" in row["wolfram_status"])
    summary = {
        "generated_utc": now_utc(),
        "theorem_anchors": len(theorem_rows),
        "gold_anchor_candidates": sum(1 for a in theorem_rows if a["anchor_status"] == "gold_anchor_candidate"),
        "minted_phone2_equations": len(minted),
        "mapped_equations": len(mappings),
        "equation_level_wolfram_verified": verified,
        "expression_level_wolfram_verified": expression_verified,
        "carrier_preserved_rows": carriers,
        "wolfram_status_counts": status_counts,
        "mapping_method_counts": method_counts,
        "anchors_with_equations": sum(1 for a in theorem_rows if a["mapped_equation_count"] > 0),
    }
    SUMMARY.write_text(json.dumps(json.loads(json.dumps(summary, default=dict)), indent=2), encoding="utf-8")

    lines = [
        "# Phone2 Theorem Anchor Pack",
        "",
        f"- Generated UTC: `{summary['generated_utc']}`",
        f"- Theorem anchors staged: `{summary['theorem_anchors']}`",
        f"- Gold anchor candidates: `{summary['gold_anchor_candidates']}`",
        f"- Minted Phone2 equations mapped: `{summary['mapped_equations']}` / `{summary['minted_phone2_equations']}`",
        f"- Equation-level Wolfram verified rows: `{summary['equation_level_wolfram_verified']}`",
        f"- Carrier-preserved rows: `{summary['carrier_preserved_rows']}`",
        f"- Anchors with mapped equations: `{summary['anchors_with_equations']}`",
        "",
        "## Top Anchors",
        "",
        "| Anchor | Kind | Title | Source | Mapped Eq |",
        "|---|---|---|---|---:|",
    ]
    for anchor in theorem_rows[:12]:
        lines.append(
            f"| `{anchor['anchor_id']}` | {anchor['semantic_kind']} | {anchor['title']} | `{anchor['source_file']}:{anchor['line_number']}` | {anchor['mapped_equation_count']} |"
        )
    lines.extend(["", "## Wolfram Status Counts", "", "| Status | Count |", "|---|---:|"])
    for status, count in status_counts.most_common():
        lines.append(f"| `{status}` | {count} |")
    lines.extend(["", "## Mapping Methods", "", "| Method | Count |", "|---|---:|"])
    for method, count in method_counts.most_common():
        lines.append(f"| `{method}` | {count} |")
    lines.extend(
        [
            "",
            "## Isabelle Carrier",
            "",
            "- `TZPID_Phone2_Theorem_Anchors.thy` records the theorem-anchor and equation-mapping counts as HOL carrier invariants.",
            "- This layer is deliberately a staging/formal bookkeeping layer, not yet a semantic proof of the theorem statements.",
        ]
    )
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")

    thy = f'''theory TZPID_Phone2_Theorem_Anchors
  imports Main
begin

section \<open>Phone2 Theorem Anchor Carrier Layer\<close>

text \<open>
  This theory records the Phone2 theorem-anchor staging layer generated from
  D:/Phone2.  It is a formal bookkeeping carrier: theorem statements remain
  semantic source claims until selected anchors are translated into stronger
  Isabelle/HOL models.
\<close>

datatype phone2_anchor_status =
    Gold_Anchor_Candidate
  | Strong_Anchor_Candidate
  | Supporting_Anchor_Candidate

datatype phone2_wolfram_lane =
    Equation_Parse_Verified
  | Expression_Parse_Verified
  | Symbolic_Carrier_Verified
  | Fragment_Carrier_Verified

definition phone2_theorem_anchor_count :: nat where
  "phone2_theorem_anchor_count = {len(theorem_rows)}"

definition phone2_gold_anchor_candidate_count :: nat where
  "phone2_gold_anchor_candidate_count = {summary['gold_anchor_candidates']}"

definition phone2_batch1_equation_count :: nat where
  "phone2_batch1_equation_count = {len(minted)}"

definition phone2_batch1_mapped_equation_count :: nat where
  "phone2_batch1_mapped_equation_count = {len(mappings)}"

definition phone2_equation_level_wolfram_verified_count :: nat where
  "phone2_equation_level_wolfram_verified_count = {verified}"

definition phone2_expression_level_wolfram_verified_count :: nat where
  "phone2_expression_level_wolfram_verified_count = {expression_verified}"

definition phone2_carrier_preserved_count :: nat where
  "phone2_carrier_preserved_count = {carriers}"

definition phone2_anchor_with_equations_count :: nat where
  "phone2_anchor_with_equations_count = {summary['anchors_with_equations']}"

theorem phone2_anchor_pack_nonempty:
  "phone2_theorem_anchor_count > 0"
  unfolding phone2_theorem_anchor_count_def by simp

theorem phone2_batch1_all_minted_equations_mapped:
  "phone2_batch1_mapped_equation_count = phone2_batch1_equation_count"
  unfolding phone2_batch1_mapped_equation_count_def
            phone2_batch1_equation_count_def
  by simp

theorem phone2_wolfram_status_partition:
  "phone2_equation_level_wolfram_verified_count
   + phone2_expression_level_wolfram_verified_count
   + phone2_carrier_preserved_count
   = phone2_batch1_equation_count"
  unfolding phone2_equation_level_wolfram_verified_count_def
            phone2_expression_level_wolfram_verified_count_def
            phone2_carrier_preserved_count_def
            phone2_batch1_equation_count_def
  by simp

theorem phone2_gold_anchor_subset:
  "phone2_gold_anchor_candidate_count \<le> phone2_theorem_anchor_count"
  unfolding phone2_gold_anchor_candidate_count_def
            phone2_theorem_anchor_count_def
  by simp

theorem phone2_anchor_coverage_bounded:
  "phone2_anchor_with_equations_count \<le> phone2_theorem_anchor_count"
  unfolding phone2_anchor_with_equations_count_def
            phone2_theorem_anchor_count_def
  by simp

end
'''
    THY.write_text(thy, encoding="utf-8")
    print(json.dumps(json.loads(json.dumps(summary, default=dict)), indent=2))


if __name__ == "__main__":
    main()
