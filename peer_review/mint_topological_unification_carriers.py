from __future__ import annotations

import csv
import json
import uuid
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\TZPIDProof")
OPENAI2 = Path(r"D:\00_Engine\AI_Workspaces\OpenAI2")
MASTERS = [
    ROOT / "TZPID_ALL_IDS_CANONICAL_EQUATION_MASTER_with_export.csv",
    OPENAI2 / "TZPID_ALL_IDS_CANONICAL_EQUATION_MASTER_with_export.csv",
]
MD_MASTERS = [
    ROOT / "TZPID_ALL_IDS_CANONICAL_EQUATION_MASTER_with_export.md",
    OPENAI2 / "TZPID_ALL_IDS_CANONICAL_EQUATION_MASTER_with_export.md",
]
TZP_ID_DIR = ROOT / "tzp_id"
OUT_DIR = ROOT / "peer_review" / "unification_intake"
REPORT = OUT_DIR / "TOPOLOGICAL_UNIFICATION_CARRIER_MINT_REPORT.md"
MINT_JSON = OUT_DIR / "TOPOLOGICAL_UNIFICATION_CARRIER_MINTED_ROWS.json"


NAMESPACE = uuid.UUID("8b6f9d98-6266-50ce-b5c8-2f5c826bfe70")
CREATOR = "Daniel Alexander Trawin"
ORCID = "https://orcid.org/0009-0001-4630-3715"
SOURCE_PATH = r"D:\Tex\topological_unification.tex"


ROWS = [
    {
        "id": "ID11372",
        "title": "Higher-Topos Physical Reality Carrier",
        "canonical_statement": "The topological unification source defines the higher topos of physical reality as an inverse-limit carrier over simplicial-set stages.",
        "canonical_equation": r"\mathcal{T}_{\infty} := \varprojlim_{n\to\infty}\left[\mathbf{Set}_{\Delta^{op}}^{(n)}\right]",
        "formation_method": "Source-backed categorical carrier extraction",
        "formation_inputs": r"\mathcal{T}_{\infty}, \mathbf{Set}_{\Delta^{op}}, n",
        "formation_note": "Minted from D:\\Tex\\topological_unification.tex line 84 / carrier-first review. This is a HOL carrier equation, not a standalone physics proof.",
        "dictionary": "Higher-Topos Physical Reality Carrier — T_infty is defined as the inverse limit of staged simplicial-set structures.",
        "encyclopedia": "This entry gives the Topological Unification source a typed categorical carrier. It records the proposed ambient higher-topos object used to organize quantum, gravity, and information sectors before any stronger physical theorem is asserted.",
    },
    {
        "id": "ID11373",
        "title": "Higher-Topos Object Class",
        "canonical_statement": "The degree-zero objects of the higher-topos carrier include vacuum states, quantum fields, spacetime manifolds, information channels, and consciousness operators.",
        "canonical_equation": r"\mathrm{Ob}_{0}(\mathcal{T}_{\infty})=\{\mathrm{VacuumStates},\mathrm{QuantumFields},\mathrm{SpacetimeManifolds},\mathrm{InformationChannels},\mathrm{ConsciousnessOperators}\}",
        "formation_method": "Source-backed categorical object extraction",
        "formation_inputs": r"\mathrm{Ob}_{0}, \mathcal{T}_{\infty}",
        "formation_note": "Minted from D:\\Tex\\topological_unification.tex line 105 / carrier-first review. This row records source vocabulary for later HOL typing.",
        "dictionary": "Higher-Topos Object Class — the degree-zero objects of T_infty are the named physical and informational sectors.",
        "encyclopedia": "This entry records the object vocabulary used by the Topological Unification source. Its role is classificatory: it names the sectors to be related by later morphisms and functors without claiming that the sector identifications have already been proven.",
    },
    {
        "id": "ID11374",
        "title": "Higher-Topos Morphism Class",
        "canonical_statement": "The n-level morphisms of the higher-topos carrier are represented as higher hom objects spanning TZP, Einstein, quantum, and neural sectors.",
        "canonical_equation": r"\mathrm{Morphisms}_{n}:=\mathrm{Hom}^{(n)}[\mathrm{TZP},\mathrm{Einstein},\mathrm{Quantum},\mathrm{Neural}]",
        "formation_method": "Source-backed categorical morphism extraction",
        "formation_inputs": r"\mathrm{Morphisms}_{n}, \mathrm{Hom}^{(n)}",
        "formation_note": "Minted from D:\\Tex\\topological_unification.tex lines 84 and 133 / carrier-first review.",
        "dictionary": "Higher-Topos Morphism Class — morphisms_n are higher Hom objects linking TZP, Einstein, quantum, and neural sectors.",
        "encyclopedia": "This entry supplies the morphism vocabulary for the quantum-to-GR source lane. It is intended for later formalization as carrier structure and should not be read as a completed proof of sector equivalence.",
    },
    {
        "id": "ID11375",
        "title": "FQT Metric Tensor-Sum Carrier",
        "canonical_statement": "The FQT metric carrier is expressed as a tensor-indexed sum of Fisher, quantum, and topological metric components.",
        "canonical_equation": r"g^{\mathrm{FQT}}_{ij}=\sum_{k,l,m,n}g^{\mathrm{Fisher}}_{ij}\otimes g^{\mathrm{Quantum}}_{kl}\otimes g^{\mathrm{Topological}}_{mn}",
        "formation_method": "Source-backed tensor carrier extraction",
        "formation_inputs": r"g^{FQT}, g^{Fisher}, g^{Quantum}, g^{Topological}",
        "formation_note": "Minted from D:\\Tex\\topological_unification.tex line 284 / carrier-first review.",
        "dictionary": "FQT Metric Tensor-Sum Carrier — g_FQT is assembled from Fisher, quantum, and topological metric factors over summed indices.",
        "encyclopedia": "This entry records the source's tensor-sum form for the Fisher-Quantum-Topological metric carrier. It is useful as a typed bridge between information geometry, quantum structure, and topological geometry.",
    },
    {
        "id": "ID11376",
        "title": "FQT Metric Product Carrier",
        "canonical_statement": "The FQT metric carrier is the tensor product of Fisher, quantum, and topological metric carriers.",
        "canonical_equation": r"g^{\mathrm{FQT}}=g^{\mathrm{Fisher}}\otimes g^{\mathrm{Quantum}}\otimes g^{\mathrm{Topological}}",
        "formation_method": "Source-backed tensor product carrier extraction",
        "formation_inputs": r"g^{FQT}, g^{Fisher}, g^{Quantum}, g^{Topological}",
        "formation_note": "Minted from D:\\Tex\\topological_unification.tex line 295 / carrier-first review.",
        "dictionary": "FQT Metric Product Carrier — g_FQT is defined as the tensor product of Fisher, quantum, and topological metric carriers.",
        "encyclopedia": "This entry gives the compact product form of the FQT carrier. It is a source-backed categorical/metric bridge that can be consumed by later HOL carrier theories.",
    },
]


def row_uuid(row: dict[str, str]) -> str:
    payload = f"{row['id']}|{row['title']}|{row['canonical_equation']}"
    return str(uuid.uuid5(NAMESPACE, payload))


def piid(num: int) -> str:
    return f"PiID-{num}-carrier"


def rteid(num: int) -> str:
    return f"RTE:P{num * 3.14159:.4f}:T{(num % 6283) / 1000:.4f}"


def complete_row(row: dict[str, str], sid: int) -> dict[str, str]:
    out = deepcopy(row)
    out.update({
        "isabelle_kind": "Definition",
        "obligation_role": "Carrier_Definition",
        "proof_required_checks": "source_traceability;wolfram_symbolic_carrier;hol_carrier_typing",
        "gold_spine": "topological_unification;quantum_gr_unification",
        "lean_rocq": f"registry_{row['id']}",
        "wolfram_status": "pending_topological_unification_carrier_review",
        "isabelle_sid": str(sid),
        "uuid": row_uuid(row),
    })
    return out


def read_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        return list(reader.fieldnames or []), list(reader)


def write_rows(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def update_master(path: Path, minted: list[dict[str, str]]) -> str:
    fields, rows = read_rows(path)
    existing = {row["id"] for row in rows}
    added = [row for row in minted if row["id"] not in existing]
    if added:
        rows.extend(added)
        write_rows(path, fields, rows)
        return f"added {len(added)}"
    return "already present"


def write_markdown_master(csv_path: Path, md_path: Path) -> None:
    fields, rows = read_rows(csv_path)
    generated = datetime.now(timezone.utc).isoformat(timespec="seconds")
    lines = [
        "# TZPID Canonical Equation Master With Export",
        "",
        f"Generated UTC: {generated}",
        f"Rows: `{len(rows)}`",
        "",
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join(["---"] * len(fields)) + " |",
    ]
    for row in rows:
        vals = []
        for field in fields:
            val = (row.get(field, "") or "").replace("\n", " ").replace("|", "\\|")
            vals.append(val)
        lines.append("| " + " | ".join(vals) + " |")
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_id_files(row: dict[str, str]) -> None:
    num = int(row["id"][2:])
    folder = TZP_ID_DIR / row["id"]
    folder.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    metadata = {
        "tzpid": row["id"],
        "title": row["title"],
        "uuid": row["uuid"],
        "PiID": piid(num),
        "RTEID": rteid(num),
        "loc_class": "QA - Mathematics: category theory and geometry",
        "arxiv_class": "math.CT",
        "creator": CREATOR,
        "creator_orcid": ORCID,
        "embedded_at_utc": now,
    }
    source_truth = {
        "schema": {
            "name": "TZPID source truth prototype",
            "version": "0.2.1",
            "generated_at": now,
            "source": "topological_unification_carrier_mint",
            "non_destructive": True,
        },
        "identity": {
            "tzpid": row["id"],
            "uuid": row["uuid"],
            "registry_id": f"registry_id_{num}",
            "piid": metadata["PiID"],
            "canonical_title": row["title"],
            "source_files": {
                "source_tex": SOURCE_PATH,
                "source_truth": str(folder / f"{row['id']}.source_truth.json"),
            },
        },
        "creator": {
            "name": CREATOR,
            "orcid": ORCID,
        },
        "classification": {
            "category": "topological-unification-carrier",
            "discipline": "mathematics",
            "loc_class": metadata["loc_class"],
            "arxiv_class": metadata["arxiv_class"],
        },
        "theory": {
            "canonical_statement": row["canonical_statement"],
            "technical_interpretation": row["encyclopedia"],
            "source_lineage": row["formation_note"],
        },
        "canonical_equation": {
            "latex_blocks": [row["canonical_equation"]],
            "source_section_latex": row["canonical_equation"],
        },
        "proof_lane": {
            "isabelle_kind": row["isabelle_kind"],
            "obligation_role": row["obligation_role"],
            "required_checks": row["proof_required_checks"].split(";"),
            "wolfram_status": row["wolfram_status"],
            "isabelle_sid": row["isabelle_sid"],
        },
    }
    tex = "\n".join([
        f"% Auto-generated source-truth intake stub for {row['id']}.",
        f"\\tzpentry{{{row['id']}}}{{{row['title']}}}",
        "\\paragraph{Canonical Statement.}",
        row["canonical_statement"],
        "\\paragraph{Canonical Equation.}",
        row["canonical_equation"],
        "\\paragraph{Registry Metadata.}",
        f"UUID: \\texttt{{{row['uuid']}}}. PiID: \\texttt{{{metadata['PiID']}}}. LOC: \\texttt{{{metadata['loc_class']}}}. arXiv: \\texttt{{{metadata['arxiv_class']}}}.",
        "",
    ])
    (folder / f"{row['id']}.metadata.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    (folder / f"{row['id']}.source_truth.json").write_text(json.dumps(source_truth, indent=2), encoding="utf-8")
    (folder / f"{row['id']}.tex").write_text(tex, encoding="utf-8")


def main() -> None:
    minted = [complete_row(row, 11372 + idx) for idx, row in enumerate(ROWS)]
    statuses = {}
    for master in MASTERS:
        if master.exists():
            statuses[str(master)] = update_master(master, minted)
    for row in minted:
        write_id_files(row)
    for csv_path, md_path in zip(MASTERS, MD_MASTERS):
        if csv_path.exists():
            write_markdown_master(csv_path, md_path)
    MINT_JSON.write_text(json.dumps(minted, indent=2), encoding="utf-8")
    lines = [
        "# Topological Unification Carrier Mint Report",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat(timespec='seconds')}",
        "",
        "## Result",
        "",
        "Minted five carrier-first categorical equations from `D:\\Tex\\topological_unification.tex`.",
        "",
        "## Master Updates",
        "",
    ]
    for path, status in statuses.items():
        lines.append(f"- `{path}`: {status}")
    lines.extend([
        "",
        "## Minted IDs",
        "",
        "| ID | Title | Role |",
        "| --- | --- | --- |",
    ])
    for row in minted:
        lines.append(f"| {row['id']} | {row['title']} | {row['obligation_role']} |")
    lines.extend([
        "",
        "## Source Truth",
        "",
        "Each minted ID has a folder under `D:\\TZPIDProof\\tzp_id\\` containing metadata JSON, source-truth JSON, and TeX stub.",
        "",
        f"Machine-readable minted rows: `{MINT_JSON}`",
    ])
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"statuses": statuses, "minted_ids": [r["id"] for r in minted]}, indent=2))


if __name__ == "__main__":
    main()
