import csv
import json
import re
from collections import Counter
from pathlib import Path


ROOT = Path(r"D:\TZPIDProof")
INTAKE = ROOT / "phone2_intake"
MASTER = Path(r"D:\00_Engine\AI_Workspaces\OpenAI2\TZPID_ALL_IDS_CANONICAL_EQUATION_MASTER_with_export.csv")

SOURCE = INTAKE / "PHONE2_ID_READY_EQUATION_QUEUE.csv"
OUT = INTAKE / "PHONE2_ATOMIC_EQUATION_QUEUE.csv"
BATCHES = INTAKE / "PHONE2_ATOMIC_REGISTRATION_BATCHES.csv"
REPORT = INTAKE / "PHONE2_ATOMIC_EQUATION_PLAN.md"
SUMMARY = INTAKE / "PHONE2_ATOMIC_EQUATION_SUMMARY.json"


DISPLAY_PATTERNS = [
    re.compile(r"\\\[(.*?)\\\]", re.DOTALL),
    re.compile(r"\\\((.*?)\\\)", re.DOTALL),
    re.compile(r"\$\$(.*?)\$\$", re.DOTALL),
    re.compile(r"\$([^$\n]{3,})\$", re.DOTALL),
]

LINE_EQUATION = re.compile(r"([^.!?\n]{0,180}(?:=|≈|∝|≤|≥|:=|\\to|→|\\mapsto|∈|⊂|⊆|⊗|⊕)[^.!?\n]{1,260})")
NOISE = re.compile(r"contentReference|oaicite|^\(\*|^\s*[-*#]+$|^={3,}$")


def clean(text: str) -> str:
    text = text or ""
    text = re.sub(r":contentReference\[[^\]]+\]\{[^}]+\}", "", text)
    text = text.replace("\u200b", "")
    text = re.sub(r"\s+", " ", text.strip())
    text = text.strip("` $")
    return text


def norm_key(text: str) -> str:
    text = clean(text).lower()
    text = re.sub(r"[\s`$\\{}\[\](),.;:|]+", "", text)
    return text


def split_atomic(text: str) -> list[str]:
    atoms = []
    for pat in DISPLAY_PATTERNS:
        atoms.extend(clean(m.group(1)) for m in pat.finditer(text))
    scrubbed = text
    for pat in DISPLAY_PATTERNS:
        scrubbed = pat.sub(" ", scrubbed)
    for line in re.split(r"(?:\n|---|;)", scrubbed):
        line = clean(line)
        if not line:
            continue
        for m in LINE_EQUATION.finditer(line):
            atoms.append(clean(m.group(1)))
    out = []
    seen = set()
    for atom in atoms:
        atom = clean(atom)
        if not atom or len(atom) < 4 or len(atom) > 700:
            continue
        if NOISE.search(atom):
            continue
        k = norm_key(atom)
        if not k or k in seen:
            continue
        seen.add(k)
        out.append(atom)
    return out


def wolfram_hint(text: str) -> str:
    t = clean(text)
    replacements = [
        (r"\\frac\{([^{}]+)\}\{([^{}]+)\}", r"(\1)/(\2)"),
        (r"\\sqrt\{([^{}]+)\}", r"Sqrt[\1]"),
        (r"\\left|\\right|\\,", ""),
        (r"\\sin", "Sin"),
        (r"\\cos", "Cos"),
        (r"\\tan", "Tan"),
        (r"\\exp", "Exp"),
        (r"\\log", "Log"),
        (r"\\int", "Integrate"),
        (r"\\sum", "Sum"),
        (r"\\pi|π", "Pi"),
        (r"\\infty|∞", "Infinity"),
        (r"\\theta|θ", "theta"),
        (r"\\phi|φ", "phi"),
        (r"\\omega|ω", "omega"),
        (r"\\alpha|α", "alpha"),
        (r"\\beta|β", "beta"),
        (r"\\gamma|γ", "gamma"),
        (r"\\delta|δ", "delta"),
        (r"\\lambda|λ", "lambda"),
        (r"\\mu|μ", "mu"),
        ("≈", "=="),
        ("≤", "<="),
        ("≥", ">="),
        ("→", "->"),
    ]
    for old, new in replacements:
        t = re.sub(old, new, t)
    t = t.replace("\\", "")
    return t[:500]


def domain_from_parent(parent: dict, atom: str) -> str:
    blob = f"{parent.get('domain_family', '')} {parent.get('source_file', '')} {atom}".lower()
    rules = [
        ("category_type_theory", r"monad|functor|topos|morphism|kleisli|category"),
        ("quantum_entanglement", r"quantum|entangle|bell|hilbert|qubit|density|tensor"),
        ("field_topology_mhd", r"magnetic|helicity|vector potential|alfv|vortex|curl|nabla|∇|torsion|dipole"),
        ("optimization_computation", r"fisher|optimizer|gradient|loss|complexity|neural|algorithm"),
        ("geometry_topology", r"topolog|manifold|homology|fiber|bundle|sphere|curvature"),
        ("signal_wave", r"wave|phase|omega|resonance|fourier|spectral|bessel"),
        ("protocol_systems", r"protocol|byob|ifp|schema|validation"),
        ("gravity_cosmology", r"gravity|metric|friedmann|hubble|spacetime"),
    ]
    for name, pattern in rules:
        if re.search(pattern, blob):
            return name
    return parent.get("domain_family") or "general_math"


def main() -> None:
    master_keys = set()
    with MASTER.open(encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            for col in ("canonical_equation", "canonical_statement", "title"):
                if row.get(col):
                    master_keys.add(norm_key(row[col]))

    atomic = []
    seen = set()
    with SOURCE.open(encoding="utf-8-sig", newline="") as handle:
        for parent in csv.DictReader(handle):
            atoms = split_atomic(parent.get("candidate_equation", ""))
            if not atoms and parent.get("readiness") != "quarantine":
                atoms = [clean(parent.get("candidate_equation", ""))]
            for local_i, atom in enumerate(atoms, start=1):
                k = norm_key(atom)
                if not k or k in seen:
                    continue
                seen.add(k)
                duplicate_status = "possible_master_duplicate" if k in master_keys else "new_or_nonexact"
                readiness = "id_ready" if len(atom) <= 450 and duplicate_status == "new_or_nonexact" else "review"
                atomic.append(
                    {
                        "atomic_index": len(atomic) + 1,
                        "parent_queue_index": parent.get("queue_index", ""),
                        "local_atom_index": local_i,
                        "proposed_id": f"PHONE2_NEXT+{len(atomic) + 1:04d}",
                        "source_file": parent.get("source_file", ""),
                        "line_number": parent.get("line_number", ""),
                        "domain_family": domain_from_parent(parent, atom),
                        "semantic_kind": parent.get("semantic_kind", ""),
                        "semantic_context": parent.get("semantic_context", ""),
                        "duplicate_status": duplicate_status,
                        "readiness": readiness,
                        "wolfram_status": parent.get("wolfram_status", ""),
                        "atomic_equation": atom,
                        "wolfram_form_hint": wolfram_hint(atom),
                        "formation_method": "Phone2 atomic equation extraction",
                        "formation_inputs": parent.get("source_file", ""),
                        "formation_note": f"Atomized from Phone2 parent queue row {parent.get('queue_index', '')}; staged only.",
                        "source_tag": "PHONE2",
                    }
                )

    with OUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(atomic[0].keys()))
        writer.writeheader()
        writer.writerows(atomic)

    ordered = sorted(
        atomic,
        key=lambda r: (
            r["readiness"] != "id_ready",
            r["duplicate_status"] != "new_or_nonexact",
            r["wolfram_status"] != "file_has_parse_clean_wolfram",
            r["domain_family"],
            int(r["atomic_index"]),
        ),
    )
    batch_rows = []
    for i, row in enumerate(ordered, start=1):
        batch_rows.append(
            {
                "batch": (i - 1) // 250 + 1,
                "batch_position": (i - 1) % 250 + 1,
                "atomic_index": row["atomic_index"],
                "proposed_id": row["proposed_id"],
                "source_file": row["source_file"],
                "line_number": row["line_number"],
                "domain_family": row["domain_family"],
                "readiness": row["readiness"],
                "duplicate_status": row["duplicate_status"],
                "wolfram_status": row["wolfram_status"],
            }
        )
    with BATCHES.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(batch_rows[0].keys()))
        writer.writeheader()
        writer.writerows(batch_rows)

    summary = {
        "atomic_equations": len(atomic),
        "readiness_counts": Counter(r["readiness"] for r in atomic),
        "domain_counts": Counter(r["domain_family"] for r in atomic),
        "duplicate_status_counts": Counter(r["duplicate_status"] for r in atomic),
        "wolfram_status_counts": Counter(r["wolfram_status"] for r in atomic),
    }
    SUMMARY.write_text(json.dumps(json.loads(json.dumps(summary, default=dict)), indent=2), encoding="utf-8")

    lines = [
        "# Phone2 Atomic Equation Registration Plan",
        "",
        "This is the atomized queue derived from the Phone2 intake. Large mixed prose/equation blocks were split into smaller equation-level candidates where possible.",
        "",
        f"- Atomic equation candidates: `{len(atomic)}`",
        "",
        "## Readiness Counts",
        "",
        "| Status | Count |",
        "|---|---:|",
    ]
    for k, v in Counter(r["readiness"] for r in atomic).most_common():
        lines.append(f"| {k} | {v} |")
    lines.extend(["", "## Domain Counts", "", "| Domain | Count |", "|---|---:|"])
    for k, v in Counter(r["domain_family"] for r in atomic).most_common():
        lines.append(f"| {k} | {v} |")
    lines.extend(
        [
            "",
            "## Promotion Guidance",
            "",
            "Use `PHONE2_ATOMIC_REGISTRATION_BATCHES.csv` for batch promotion. Batch 1 prioritizes ID-ready, non-duplicate rows from files that already contain parse-clean Wolfram material.",
            "",
            "Do not mint rows marked `possible_master_duplicate` without checking the existing ID first.",
        ]
    )
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(json.loads(json.dumps(summary, default=dict)), indent=2))


if __name__ == "__main__":
    main()
