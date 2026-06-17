import csv
import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


SOURCE = Path(r"D:\Phone2")
ROOT = Path(r"D:\TZPIDProof")
OUT = ROOT / "phone2_intake"
EQUATIONS_CSV = OUT / "PHONE2_EQUATION_CANDIDATES.csv"
SEMANTICS_CSV = OUT / "PHONE2_SEMANTIC_CANDIDATES.csv"
WOLFRAM_CSV = OUT / "PHONE2_WOLFRAM_MODULE_CANDIDATES.csv"
INVENTORY_CSV = OUT / "PHONE2_FILE_INVENTORY.csv"
REPORT_MD = OUT / "PHONE2_INTAKE_REPORT.md"
SUMMARY_JSON = OUT / "phone2_intake_summary.json"


MOJIBAKE = {
    "â†’": "→", "â‡’": "⇒", "â‰ ": "≠", "â‰": "≈", "âˆˆ": "∈", "âˆ€": "∀",
    "âˆƒ": "∃", "âˆž": "∞", "âˆ«": "∫", "âˆ‘": "∑", "âˆ‚": "∂", "âˆ‡": "∇",
    "âŠ—": "⊗", "âŠƒ": "⊃", "âˆ§": "∧", "âˆ¨": "∨", "Ã—": "×",
    "Â²": "²", "Â³": "³", "Â±": "±", "Ï€": "π", "Îπ": "π",
    "Î¼": "μ", "Î½": "ν", "Î›": "Λ", "Î©": "Ω", "Î¦": "Φ", "Î¨": "Ψ",
    "Î¸": "θ", "Ï†": "φ", "Ïƒ": "σ", "Ï": "ρ", "Î·": "η",
    "Î³": "γ", "Î´": "δ", "Î±": "α", "Îβ": "β", "Î²": "β",
    "Îµ": "ε", "Î¾": "ξ", "Î¶": "ζ", "Îº": "κ", "Î»": "λ",
    "â„": "ℏ", "â„¤": "ℤ", "â„‚": "ℂ", "â„": "ℝ", "â„³": "ℳ",
    "â„‹": "ℋ", "â„’": "ℒ", "âŸ¨": "⟨", "âŸ©": "⟩",
    "ð•": "𝕋", "ð”": "𝔔", "ð’": "𝒟",
}

EQUATION_SIGNALS = [
    r"\\begin\{equation\}", r"\\\[", r"\$\$", r"\\\(", r":=", r"==", r"(?<![A-Za-z])=(?![=>])",
    r"≈", r"≅", r"≠", r"≤", r"≥", r"∈", r"∀", r"∃", r"→", r"⇒", r"↦",
    r"\\sum", r"\\int", r"\\nabla", r"\\partial", r"\bSum\[", r"\bIntegrate\[",
    r"\bLimit\[", r"\bSolve\[", r"\bBesselJ\[", r"\bSphericalHarmonicY\[",
]

SEMANTIC_SIGNALS = [
    r"\bAxiom\b", r"\bDefinition\b", r"\bTheorem\b", r"\bLemma\b", r"\bCorollary\b",
    r"\bInvariant\b", r"\bProtocol\b", r"\bFunctor\b", r"\bMonad\b", r"\bTopos\b",
    r"\bProof\b", r"\bConstraint\b", r"\bMechanism\b", r"\bValidation\b",
    r"\bPrediction\b", r"\bFalsifiable\b", r"\bAssumption\b",
]

TOP_LEVEL_WL = re.compile(
    r"^\s*([A-Za-z_][A-Za-z0-9_]*|[\w𝓐-𝓩𝔄-𝔝𝕀-𝕫]+)\s*(?:\[[^\]]*\])?\s*:=\s*(Module|Association|ResourceFunction|Function|CompiledFunction|With|Dataset)\[",
    re.UNICODE,
)


def clean_text(text):
    for bad, good in MOJIBAKE.items():
        text = text.replace(bad, good)
    text = text.replace("\ufeff", "")
    return text


def md_escape(text):
    return (text or "").replace("|", "\\|").replace("\n", " ").strip()


def write_csv(path, rows, fields):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def compact(s):
    return re.sub(r"\s+", " ", s or "").strip()


def equation_score(text):
    score = 0
    score += len(re.findall(r"[=≈≅≠≤≥∈∀∃→⇒↦]", text))
    score += 4 if re.search(r"\\int|∫|Integrate\[", text) else 0
    score += 4 if re.search(r"\\sum|∑|Sum\[", text) else 0
    score += 4 if re.search(r"BesselJ|SphericalHarmonicY|Y_\\ell|j_\\ell", text) else 0
    score += 3 if re.search(r"\\nabla|∇|\\partial|∂", text) else 0
    score += 3 if re.search(r"\\lim|lim|Limit\[", text, flags=re.I) else 0
    score += 2 if re.search(r"\d+(/\d+)?|\d+\.\d+|153600|153,600|10\^", text) else 0
    score -= 5 if len(text) > 800 else 0
    return score


def semantic_kind(text):
    for kind in ["Axiom", "Definition", "Theorem", "Lemma", "Corollary", "Invariant", "Protocol", "Functor", "Monad", "Topos", "Constraint", "Mechanism", "Validation", "Prediction"]:
        if re.search(rf"\b{kind}\b", text, flags=re.I):
            return kind
    return "SemanticNote"


def extract_display_math(text, file_name):
    candidates = []
    patterns = [
        (r"\$\$(.*?)\$\$", "display_dollar"),
        (r"\\\[(.*?)\\\]", "display_bracket"),
        (r"\\begin\{equation\}(.*?)\\end\{equation\}", "latex_equation"),
        (r"\\begin\{align\}(.*?)\\end\{align\}", "latex_align"),
    ]
    for pattern, source_type in patterns:
        for m in re.finditer(pattern, text, flags=re.S):
            value = compact(m.group(1))
            if value:
                candidates.append({
                    "source_file": file_name,
                    "line_number": text[:m.start()].count("\n") + 1,
                    "source_type": source_type,
                    "candidate": value,
                    "score": equation_score(value),
                })
    return candidates


def extract_line_candidates(lines, file_name):
    eq_rows = []
    sem_rows = []
    eq_re = re.compile("|".join(EQUATION_SIGNALS))
    sem_re = re.compile("|".join(SEMANTIC_SIGNALS), re.I)
    for i, line in enumerate(lines, start=1):
        stripped = line.strip()
        if not stripped:
            continue
        if len(stripped) > 1200:
            stripped = stripped[:1200]
        if eq_re.search(stripped):
            score = equation_score(stripped)
            if score > 0:
                eq_rows.append({
                    "source_file": file_name,
                    "line_number": i,
                    "source_type": "line",
                    "candidate": stripped,
                    "score": score,
                })
        if sem_re.search(stripped):
            sem_rows.append({
                "source_file": file_name,
                "line_number": i,
                "semantic_kind": semantic_kind(stripped),
                "candidate": stripped,
            })
    return eq_rows, sem_rows


def extract_wolfram_blocks(text, lines, file_name):
    rows = []
    for m in re.finditer(r"```(?:wolfram|wl|mathematica)?\s*(.*?)```", text, flags=re.S | re.I):
        code = m.group(1).strip()
        if code:
            rows.append({
                "source_file": file_name,
                "line_number": text[:m.start()].count("\n") + 1,
                "module_name": infer_module_name(code),
                "source_type": "fenced_code",
                "raw_code": code,
                "cleaned_code": clean_wolfram_code(code),
            })

    starts = []
    for idx, line in enumerate(lines):
        m = TOP_LEVEL_WL.match(line)
        if m:
            starts.append((idx, m.group(1)))
    for pos, (idx, name) in enumerate(starts):
        end = starts[pos + 1][0] if pos + 1 < len(starts) else min(len(lines), idx + 220)
        block = "\n".join(lines[idx:end]).strip()
        rows.append({
            "source_file": file_name,
            "line_number": idx + 1,
            "module_name": name,
            "source_type": "top_level_assignment",
            "raw_code": block,
            "cleaned_code": clean_wolfram_code(block),
        })
    return rows


def infer_module_name(code):
    first = code.splitlines()[0].strip() if code.splitlines() else ""
    m = re.match(r"([A-Za-z_][A-Za-z0-9_]*)\s*(?:\[[^\]]*\])?\s*:=", first)
    return m.group(1) if m else ""


def clean_wolfram_code(code):
    code = clean_text(code)
    replacements = {
        "→": "->", "⇒": "->", "×": "*", "≤": "<=", "≥": ">=", "≠": "!=", "π": "Pi",
        "∞": "Infinity", "∑": "Sum", "∫": "Integrate", "√": "Sqrt", "ℏ": "hbar",
        "⊗": "**", "∧": "&&", "∨": "||", "∂": "D", "∇": "Grad",
        "⟨": "<", "⟩": ">", "𝟙": "Identity",
    }
    for old, new in replacements.items():
        code = code.replace(old, new)
    # Replace a few common decorative Unicode identifiers with ASCII.
    greek = {
        "θ": "theta", "φ": "phi", "Φ": "Phi", "Ψ": "Psi", "Ω": "Omega", "ω": "omega",
        "Λ": "Lambda", "λ": "lambda", "ρ": "rho", "σ": "sigma", "η": "eta",
        "α": "alpha", "β": "beta", "γ": "gamma", "δ": "delta", "κ": "kappa",
        "μ": "mu", "ν": "nu", "ξ": "xi", "τ": "tau", "ε": "epsilon",
    }
    for old, new in greek.items():
        code = code.replace(old, new)
    code = re.sub(r"[𝓐-𝓩𝓪-𝔃𝔄-𝔝𝕀-𝕫]", "sym", code)
    code = code.replace("(*", "(*").replace("*/", "*)")
    return code


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    inventory = []
    equations = []
    semantics = []
    wolfram = []
    if not SOURCE.exists():
        raise SystemExit(f"Missing source directory: {SOURCE}")

    for path in sorted(SOURCE.rglob("*.txt")):
        raw = path.read_text(encoding="utf-8", errors="replace")
        text = clean_text(raw)
        rel = str(path.relative_to(SOURCE))
        lines = text.splitlines()
        inventory.append({
            "source_file": rel,
            "bytes": path.stat().st_size,
            "lines": len(lines),
            "last_write_time": path.stat().st_mtime,
        })
        equations.extend(extract_display_math(text, rel))
        eq_line, sem_line = extract_line_candidates(lines, rel)
        equations.extend(eq_line)
        semantics.extend(sem_line)
        wolfram.extend(extract_wolfram_blocks(text, lines, rel))

    # Deduplicate equation rows by source and candidate text.
    seen = set()
    deduped_eq = []
    for row in sorted(equations, key=lambda r: (-int(r["score"]), r["source_file"], int(r["line_number"]))):
        key = (row["source_file"], row["candidate"])
        if key not in seen:
            deduped_eq.append(row)
            seen.add(key)

    seen = set()
    deduped_sem = []
    for row in semantics:
        key = (row["source_file"], row["candidate"])
        if key not in seen:
            deduped_sem.append(row)
            seen.add(key)

    write_csv(INVENTORY_CSV, inventory, ["source_file", "bytes", "lines", "last_write_time"])
    write_csv(EQUATIONS_CSV, deduped_eq, ["source_file", "line_number", "source_type", "score", "candidate"])
    write_csv(SEMANTICS_CSV, deduped_sem, ["source_file", "line_number", "semantic_kind", "candidate"])
    write_csv(WOLFRAM_CSV, wolfram, ["source_file", "line_number", "module_name", "source_type", "raw_code", "cleaned_code"])

    semantic_counts = Counter(row["semantic_kind"] for row in deduped_sem)
    summary = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "source": str(SOURCE),
        "files": len(inventory),
        "total_bytes": sum(int(row["bytes"]) for row in inventory),
        "equation_candidates": len(deduped_eq),
        "semantic_candidates": len(deduped_sem),
        "wolfram_candidates": len(wolfram),
        "semantic_counts": dict(semantic_counts),
        "outputs": {
            "inventory": str(INVENTORY_CSV),
            "equations": str(EQUATIONS_CSV),
            "semantics": str(SEMANTICS_CSV),
            "wolfram": str(WOLFRAM_CSV),
            "report": str(REPORT_MD),
        },
    }
    SUMMARY_JSON.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")

    top_eq = deduped_eq[:40]
    lines = [
        "# Phone2 Intake Report",
        "",
        f"Generated UTC: {summary['generated_utc']}",
        "",
        "This is an intake/extraction pass only. Nothing has been minted into the master registry.",
        "",
        "## Counts",
        "",
        f"- Source files: `{summary['files']}`",
        f"- Total bytes: `{summary['total_bytes']}`",
        f"- Equation candidates: `{summary['equation_candidates']}`",
        f"- Semantic candidates: `{summary['semantic_candidates']}`",
        f"- Wolfram/module candidates: `{summary['wolfram_candidates']}`",
        "",
        "## Semantic Counts",
        "",
    ]
    for kind, count in semantic_counts.most_common():
        lines.append(f"- `{kind}`: `{count}`")
    lines += [
        "",
        "## Top Equation Candidates",
        "",
        "| Rank | Score | Source | Line | Candidate |",
        "|---:|---:|---|---:|---|",
    ]
    for idx, row in enumerate(top_eq, start=1):
        lines.append(
            f"| {idx} | {row['score']} | `{row['source_file']}` | {row['line_number']} | {md_escape(row['candidate'])[:420]} |"
        )
    lines += [
        "",
        "## Outputs",
        "",
        f"- Inventory CSV: `{INVENTORY_CSV}`",
        f"- Equation candidates CSV: `{EQUATIONS_CSV}`",
        f"- Semantic candidates CSV: `{SEMANTICS_CSV}`",
        f"- Wolfram candidates CSV: `{WOLFRAM_CSV}`",
    ]
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
