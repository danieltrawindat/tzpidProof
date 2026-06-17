import json
import re
from pathlib import Path


ROOT = Path(r"D:\TZPIDProof")
LADDER = ROOT / "TZPID_ALL_IDS_REASSEMBLED_PROOF_LADDER.md"
TEX = ROOT / "peer_review" / "tex"
OUT_DIR = ROOT / "peer_review" / "id_audit"


PAPERS = [
    TEX / "paper1_nested_hyperspherical_enclosures.tex",
    TEX / "paper2_phase_locking_resonance.tex",
    TEX / "paper3_musical_holonomy.tex",
    TEX / "paper4_gyromagnetic_movement.tex",
    TEX / "paper5_gravity_accumulated_force.tex",
    TEX / "paper6_bessel_residual_bridge.tex",
    TEX / "paper7_energy_to_matter.tex",
    TEX / "paper8_topological_unification.tex",
    TEX / "paper9_einstein_focus.tex",
    TEX / "paper10_dag_breakthrough.tex",
]


ID_RE = re.compile(r"\bID\d{4,5}\b")
LADDER_ROW_RE = re.compile(r"^\|\s*(\d+)\s*\|\s*(ID\d{4,5})\s*\|", re.MULTILINE)


def unique_in_order(items):
    seen = set()
    out = []
    for item in items:
        if item not in seen:
            seen.add(item)
            out.append(item)
    return out


def load_ladder():
    text = LADDER.read_text(encoding="utf-8", errors="replace")
    rung_by_id = {}
    for rung, tzpid in LADDER_ROW_RE.findall(text):
        rung_by_id[tzpid] = int(rung)
    return rung_by_id


def paper_number(path):
    m = re.search(r"paper(\d+)", path.name)
    return int(m.group(1)) if m else 999


def order_violations(ids, rung_by_id):
    violations = []
    last_id = None
    last_rung = None
    for pos, tzpid in enumerate(ids, start=1):
        rung = rung_by_id.get(tzpid)
        if rung is None:
            continue
        if last_rung is not None and rung < last_rung:
            violations.append(
                {
                    "position": pos,
                    "previous_id": last_id,
                    "previous_rung": last_rung,
                    "current_id": tzpid,
                    "current_rung": rung,
                    "drop": last_rung - rung,
                }
            )
        last_id = tzpid
        last_rung = rung
    return violations


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    rung_by_id = load_ladder()
    ladder_ids = set(rung_by_id)

    report = {
        "derivation_ladder": str(LADDER),
        "ladder_id_count": len(ladder_ids),
        "paper_count": len(PAPERS),
        "papers": [],
    }

    all_paper_ids = []
    missing_total = []
    for path in PAPERS:
        text = path.read_text(encoding="utf-8", errors="replace")
        all_mentions = ID_RE.findall(text)
        unique_ids = unique_in_order(all_mentions)
        missing = [tzpid for tzpid in unique_ids if tzpid not in ladder_ids]
        present = [tzpid for tzpid in unique_ids if tzpid in ladder_ids]
        violations = order_violations(unique_ids, rung_by_id)
        all_paper_ids.extend(unique_ids)
        missing_total.extend((path.name, tzpid) for tzpid in missing)
        report["papers"].append(
            {
                "paper": path.name,
                "path": str(path),
                "id_mentions_total": len(all_mentions),
                "unique_ids": len(unique_ids),
                "present_in_derivation_ladder": len(present),
                "missing_from_derivation_ladder": len(missing),
                "missing_ids": missing,
                "derivation_order_violations": len(violations),
                "derivation_order_violations_sample": violations[:25],
                "first_20_ids_with_rungs": [
                    {"id": tzpid, "rung": rung_by_id.get(tzpid)} for tzpid in unique_ids[:20]
                ],
            }
        )

    unique_all_paper_ids = unique_in_order(all_paper_ids)
    all_missing_unique = [tzpid for tzpid in unique_all_paper_ids if tzpid not in ladder_ids]
    report["totals"] = {
        "paper_id_mentions_total": sum(p["id_mentions_total"] for p in report["papers"]),
        "unique_ids_across_papers": len(unique_all_paper_ids),
        "unique_ids_present_in_derivation_ladder": len(
            [tzpid for tzpid in unique_all_paper_ids if tzpid in ladder_ids]
        ),
        "unique_ids_missing_from_derivation_ladder": len(all_missing_unique),
        "missing_ids": all_missing_unique,
        "paper_local_derivation_order_violations": sum(
            p["derivation_order_violations"] for p in report["papers"]
        ),
    }

    json_path = OUT_DIR / "paper_ids_vs_derivation_ladder_report.json"
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# Paper IDs vs Derivation Ladder Audit",
        "",
        f"- Derivation ladder: `{LADDER}`",
        f"- Ladder IDs parsed: `{len(ladder_ids)}`",
        f"- Papers checked: `{len(PAPERS)}`",
        f"- Total paper ID mentions: `{report['totals']['paper_id_mentions_total']}`",
        f"- Unique IDs across papers: `{report['totals']['unique_ids_across_papers']}`",
        f"- Unique IDs present in derivation ladder: `{report['totals']['unique_ids_present_in_derivation_ladder']}`",
        f"- Unique IDs missing from derivation ladder: `{report['totals']['unique_ids_missing_from_derivation_ladder']}`",
        f"- Paper-local derivation-order backsteps: `{report['totals']['paper_local_derivation_order_violations']}`",
        "",
        "A missing ID means the paper cites an `ID####` token that is not present as a rung in the reassembled derivation-order ladder.",
        "A derivation-order backstep means a paper mentions an ID whose ladder rung is above an ID mentioned immediately before it; this is not necessarily wrong prose, but it means the paper's local citation order is not strictly ladder order.",
        "",
        "## Per Paper",
        "",
        "| Paper | Mentions | Unique IDs | Missing | Local Backsteps |",
        "|---|---:|---:|---:|---:|",
    ]
    for p in report["papers"]:
        lines.append(
            f"| `{p['paper']}` | {p['id_mentions_total']} | {p['unique_ids']} | "
            f"{p['missing_from_derivation_ladder']} | {p['derivation_order_violations']} |"
        )
    if all_missing_unique:
        lines.extend(["", "## Missing IDs", ""])
        lines.extend(f"- `{tzpid}`" for tzpid in all_missing_unique)
    else:
        lines.extend(["", "## Missing IDs", "", "None."])

    md_path = OUT_DIR / "PAPER_IDS_VS_DERIVATION_LADDER_REPORT.md"
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(md_path)
    print(json_path)


if __name__ == "__main__":
    main()
