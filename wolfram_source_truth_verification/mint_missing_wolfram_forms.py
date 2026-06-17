import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\TZPIDProof")
TZP_ID = ROOT / "tzp_id"
OUT_BASE = ROOT / "wolfram_source_truth_verification"


def wl_string(text):
    """Return a Wolfram Language string literal preserving source text."""
    if text is None:
        text = ""
    text = str(text)
    return (
        '"'
        + text.replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("\r", "\\r")
        .replace("\n", "\\n")
        .replace("\t", "\\t")
        + '"'
    )


def title_of(obj, fallback):
    return (
        obj.get("title")
        or obj.get("canonical_title")
        or obj.get("identity", {}).get("canonical_title")
        or obj.get("tzpid_provenance", {}).get("canonical_title")
        or fallback
    )


def has_usable_wolfram_blocks(obj):
    wf = obj.get("wolfram_form")
    if not isinstance(wf, dict):
        return False
    blocks = wf.get("audit", {}).get("blocks")
    if not isinstance(blocks, list):
        return False
    for block in blocks:
        if not isinstance(block, dict):
            continue
        for field in ("wolfram_input", "holdform_inputform"):
            value = block.get(field)
            if isinstance(value, str) and value.strip():
                return True
    return False


def canonical_latex_blocks(obj):
    canonical = obj.get("canonical_equation")
    blocks = []
    if isinstance(canonical, dict):
        value = canonical.get("latex_blocks")
        if isinstance(value, list):
            blocks.extend(str(x).strip() for x in value if str(x).strip())
        elif isinstance(value, str) and value.strip():
            blocks.append(value.strip())
        source_section = canonical.get("source_section_latex")
        if not blocks and isinstance(source_section, str) and source_section.strip():
            blocks.append(source_section.strip())
    elif isinstance(canonical, str) and canonical.strip():
        blocks.append(canonical.strip())

    if not blocks:
        for key in ("canonical_equation", "canonical_statement", "equation"):
            value = obj.get(key)
            if isinstance(value, str) and value.strip():
                blocks.append(value.strip())
                break
    return blocks or ["NO_CANONICAL_LATEX_BLOCK_PRESENT"]


def build_wolfram_form(tzpid, title, blocks, stamp):
    audit_blocks = []
    model_lines = [
        f"(* TZPID {tzpid} minted source-truth Wolfram carrier model *)",
        f"ClearAll[K{tzpid[2:]}, TZPIDCanonicalLatex, TZPIDCanonicalCarrier];",
    ]
    held_symbols = []
    for index, latex in enumerate(blocks, start=1):
        var_name = f"eq{tzpid[2:]}${index}"
        wolfram_input = (
            "HoldForm[TZPIDCanonicalLatex["
            f"{wl_string(tzpid)}, {index}, {wl_string(latex)}"
            "]]"
        )
        audit_blocks.append(
            {
                "latex": latex,
                "normalized_latex": latex,
                "wolfram_input": wolfram_input,
                "parse_method": "minted_source_truth_latex_carrier",
                "parse_status": "pending_wolfram_parse_check",
                "normalization_notes": [
                    "Minted from canonical_equation.latex_blocks",
                    "Carrier form preserves exact LaTeX as Wolfram string data",
                    "Semantic/numeric interpretation remains a later domain-specific upgrade",
                ],
                "messages": [],
            }
        )
        model_lines.append(f"{var_name} = {wolfram_input};")
        held_symbols.append(var_name)
    model_lines.append(f"K{tzpid[2:]} = HoldForm[{{{', '.join(held_symbols)}}}];")
    model_lines.append(
        f"TZPIDCanonicalCarrier[{wl_string(tzpid)}] = "
        f"<|\"id\" -> {wl_string(tzpid)}, \"title\" -> {wl_string(title)}, "
        f"\"blocks\" -> K{tzpid[2:]}|>;"
    )
    return {
        "existing_from_tex": "\n\n".join(blocks),
        "audit": {
            "engine": "Wolfram Engine",
            "version": "carrier_minted_without_engine_specific_translation",
            "status": "minted_source_truth_latex_carrier_pending_parse_verification",
            "minted_at_utc": stamp,
            "blocks": audit_blocks,
        },
        "generated_model": "\n".join(model_lines),
        "carrier_semantics": {
            "scope": "source_truth_preservation_and_wolfram_parse_coverage",
            "claim": "The block is a valid Wolfram carrier for the source equation text; it is not yet a domain-specific computational proof.",
        },
    }


def main():
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    report_stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    OUT_BASE.mkdir(parents=True, exist_ok=True)

    changed = []
    skipped = []
    for path in sorted(TZP_ID.glob("ID*/ID*.source_truth.json")):
        obj = json.loads(path.read_text(encoding="utf-8"))
        tzpid = path.parent.name
        if has_usable_wolfram_blocks(obj):
            skipped.append(tzpid)
            continue
        title = title_of(obj, tzpid)
        blocks = canonical_latex_blocks(obj)
        obj["wolfram_form"] = build_wolfram_form(tzpid, title, blocks, stamp)

        formal = obj.get("formal_derivations")
        if isinstance(formal, dict):
            existing = formal.get("wolfram")
            if not isinstance(existing, dict):
                existing = {}
            existing.update(
                {
                    "status": "wolfram_form_carrier_minted_pending_parse_verification",
                    "minted_at_utc": stamp,
                    "note": "Carrier form preserves source LaTeX as Wolfram-readable data; semantic proof remains domain-specific.",
                }
            )
            formal["wolfram"] = existing
            obj["formal_derivations"] = formal

        path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        changed.append({"id": tzpid, "path": str(path), "block_count": len(blocks), "title": title})

    report = {
        "minted_at_utc": stamp,
        "source_root": str(TZP_ID),
        "changed_count": len(changed),
        "skipped_existing_count": len(skipped),
        "changed": changed,
    }
    report_path = OUT_BASE / f"mint_missing_wolfram_forms_report_{report_stamp}.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    md_path = OUT_BASE / f"MINT_MISSING_WOLFRAM_FORMS_REPORT_{report_stamp}.md"
    md_lines = [
        "# TZPID Missing Wolfram Form Mint Report",
        "",
        f"- Minted at UTC: `{stamp}`",
        f"- Source root: `{TZP_ID}`",
        f"- IDs updated: `{len(changed)}`",
        f"- IDs skipped because they already had Wolfram blocks: `{len(skipped)}`",
        f"- JSON report: `{report_path}`",
        "",
        "Each minted block is a Wolfram Language carrier of the source LaTeX equation text:",
        "",
        "`HoldForm[TZPIDCanonicalLatex[id, block_index, latex_string]]`",
        "",
        "This provides syntax-checkable Wolfram coverage while preserving a clear distinction between carrier forms and later semantic/numeric proof models.",
    ]
    md_path.write_text("\n".join(md_lines) + "\n", encoding="utf-8")
    print(str(report_path))


if __name__ == "__main__":
    main()
