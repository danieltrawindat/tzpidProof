import csv
import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\TZPIDProof")
INTAKE = ROOT / "phone2_intake"
OUTDIR = INTAKE / "wolfram_batch1"
MASTER = ROOT / "TZPID_ALL_IDS_CANONICAL_EQUATION_MASTER_with_export.csv"
MINTED = INTAKE / "PHONE2_BATCH1_MINTED_IDS.csv"

CANDIDATES_JSON = OUTDIR / "phone2_batch1_wolfram_candidates.json"
WLS = OUTDIR / "phone2_batch1_wolfram_certificate.wls"
RESULTS_JSON = OUTDIR / "phone2_batch1_wolfram_certificate_results.json"
RESULTS_CSV = OUTDIR / "phone2_batch1_wolfram_certificate_results.csv"
REPORT = OUTDIR / "PHONE2_BATCH1_WOLFRAM_CERTIFICATE.md"


SUBSCRIPT_MAP = str.maketrans("₀₁₂₃₄₅₆₇₈₉", "0123456789")
SUPERSCRIPT_MAP = {
    "²": "^2",
    "³": "^3",
    "⁴": "^4",
    "⁵": "^5",
    "⁶": "^6",
    "⁷": "^7",
    "⁸": "^8",
    "⁹": "^9",
}


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def clean_wolfram(text: str) -> str:
    s = text or ""
    s = re.sub(r"\(\*.*?\*\)", "", s)
    s = s.translate(SUBSCRIPT_MAP)
    for old, new in SUPERSCRIPT_MAP.items():
        s = s.replace(old, new)
    replacements = [
        ("→", "->"),
        ("↦", "->"),
        ("⇒", "->"),
        ("⟹", "->"),
        ("×", "*"),
        ("·", "*"),
        ("≤", "<="),
        ("≥", ">="),
        ("≈", "=="),
        ("≅", "=="),
        ("∝", "=="),
        ("∂", "d"),
        ("∫", "Integrate"),
        ("Σ", "Sum"),
        ("Π", "Product"),
        ("√", "Sqrt"),
        ("∞", "Infinity"),
        ("⊔", "+"),
        ("⊗", "CircleTimes"),
        ("⊕", "CirclePlus"),
        ("∘", "@*"),
        ("ℒ", "Lagrangian"),
        ("𝒮", "Action"),
        ("𝒟", "MeasureD"),
        ("ħ", "hbar"),
        ("Φ", "Phi"),
        ("φ", "phi"),
        ("ψ", "psi"),
        ("Ψ", "Psi"),
        ("τ", "tau"),
        ("ρ", "rho"),
        ("λ", "lambda"),
        ("π", "Pi"),
        ("θ", "theta"),
        ("μ", "mu"),
        ("ν", "nu"),
        ("α", "alpha"),
        ("β", "beta"),
        ("γ", "gamma"),
        ("δ", "delta"),
        ("Ω", "Omega"),
        ("ω", "omega"),
        ("₊", "Plus"),
        ("₋", "Minus"),
        ("¯", "bar"),
    ]
    for old, new in replacements:
        s = s.replace(old, new)
    latex_replacements = [
        (r"\\frac\{([^{}]+)\}\{([^{}]+)\}", r"(\1)/(\2)"),
        (r"\\sqrt\{([^{}]+)\}", r"Sqrt[\1]"),
        (r"\\lim_\{([^{}]+)\}", r"Limit"),
        (r"\\left|\\right|\\,", ""),
        (r"\\left|\\right|", ""),
        (r"\\left", ""),
        (r"\\right", ""),
        (r"\\langle", ""),
        (r"\\rangle", ""),
        (r"\\hat\{([^{}]+)\}", r"\1Hat"),
        (r"\\text\{([^{}]+)\}", r"\1"),
        (r"\\mathrm\{([^{}]+)\}", r"\1"),
        (r"\\bar\{([^{}]+)\}", r"\1Bar"),
        (r"\\hbar", "hbar"),
        (r"\\pi", "Pi"),
        (r"\\theta", "theta"),
        (r"\\phi", "phi"),
        (r"\\tau", "tau"),
        (r"\\rho", "rho"),
        (r"\\lambda", "lambda"),
        (r"\\alpha", "alpha"),
        (r"\\beta", "beta"),
        (r"\\gamma", "gamma"),
        (r"\\delta", "delta"),
        (r"\\omega", "omega"),
        (r"\\Omega", "Omega"),
        (r"\\sum", "Sum"),
        (r"\\int", "Integrate"),
        (r"\\partial", "d"),
        (r"\\to", "->"),
        (r"\\mapsto", "->"),
        (r"\\in", " in "),
    ]
    for pattern, repl in latex_replacements:
        s = re.sub(pattern, repl, s)
    s = re.sub(r"∀\s*([A-Za-z][A-Za-z0-9$]*)\s*,?", r"", s)
    s = re.sub(r"∃\s*([A-Za-z][A-Za-z0-9$]*)\s*,?", r"", s)
    s = s.replace("\\", "")
    s = re.sub(r"\b([A-Za-z][A-Za-z0-9]*)_([A-Za-z0-9]+)\b", r"\1$\2", s)
    s = re.sub(r"\]\s*\[", "][", s)
    s = re.sub(r"!\s*\(", "!*(", s)
    s = re.sub(r"\s+", " ", s.strip())
    s = s.strip(" ,.;")
    # Convert a single unambiguous assignment to equality for parse-only certification.
    if ":=" not in s and "==" not in s and re.search(r"(?<![<>=!])=(?![=>])", s):
        s = re.sub(r"(?<![<>=!])=(?![=>])", "==", s, count=1)
    return s


def status_hint(expr: str) -> str:
    if not expr:
        return "empty_after_cleaning"
    if expr.count("[") != expr.count("]") or expr.count("(") != expr.count(")"):
        return "likely_incomplete_brackets"
    if expr.endswith(("+", "*", "-", "/", "[", ",")):
        return "likely_fragment"
    return "candidate"


def main() -> None:
    OUTDIR.mkdir(parents=True, exist_ok=True)
    minted_ids = [row["minted_id"] for row in csv.DictReader(MINTED.open(encoding="utf-8-sig", newline=""))]
    minted = set(minted_ids)
    rows = []
    with MASTER.open(encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            if row.get("id") in minted:
                expr = clean_wolfram(row.get("canonical_equation", ""))
                rows.append(
                    {
                        "id": row["id"],
                        "title": row.get("title", ""),
                        "canonical_equation": row.get("canonical_equation", ""),
                        "wolfram_candidate": expr,
                        "precheck_status": status_hint(expr),
                    }
                )
    rows.sort(key=lambda r: minted_ids.index(r["id"]))
    CANDIDATES_JSON.write_text(json.dumps(rows, indent=2, ensure_ascii=False), encoding="utf-8")

    candidate_path = str(CANDIDATES_JSON).replace("\\", "\\\\")
    results_json_path = str(RESULTS_JSON).replace("\\", "\\\\")
    wls = f'''$HistoryLength = 0;
candidates = Import["{candidate_path}", "RawJSON"];

ClearAll[parseCandidate];
parseCandidate[row_] := Module[{{held, status, message, freeSymbols}},
  If[row["precheck_status"] =!= "candidate",
    Return[<|
      "id" -> row["id"],
      "title" -> row["title"],
      "canonical_equation" -> row["canonical_equation"],
      "wolfram_candidate" -> row["wolfram_candidate"],
      "status" -> "wolfram_needs_cleanup",
      "message" -> row["precheck_status"],
      "held_head" -> "",
      "free_symbol_count" -> "not_parsed"
    |>]
  ];
  held = Quiet[
    Check[ToExpression[row["wolfram_candidate"], InputForm, HoldComplete], $Failed],
    {{ToExpression::sntx, Syntax::sntxf, Syntax::tsntxi, General::stop}}
  ];
  If[held === $Failed,
    status = "wolfram_parse_error"; message = "ToExpression failed"; freeSymbols = "not_parsed",
    status = "wolfram_equation_parse_verified"; message = "ToExpression parsed under HoldComplete";
    freeSymbols = Length@DeleteDuplicates@Cases[held, s_Symbol /; Context[s] =!= "System`", Infinity]
  ];
  <|
    "id" -> row["id"],
    "title" -> row["title"],
    "canonical_equation" -> row["canonical_equation"],
    "wolfram_candidate" -> row["wolfram_candidate"],
    "status" -> status,
    "message" -> message,
    "held_head" -> If[held === $Failed, "", ToString[Head[held], InputForm]],
    "free_symbol_count" -> freeSymbols
  |>
];

results = parseCandidate /@ candidates;
summary = <|
  "generated_utc" -> "{now_utc()}",
  "total" -> Length[results],
  "status_counts" -> Counts[results[[All, "status"]]],
  "results" -> results
|>;
Export["{results_json_path}", summary, "RawJSON"];
Print[ExportString[KeyDrop[summary, "results"], "RawJSON"]];
'''
    WLS.write_text(wls, encoding="utf-8")
    print(json.dumps({"candidates": len(rows), "json": str(CANDIDATES_JSON), "wls": str(WLS)}, indent=2))


if __name__ == "__main__":
    main()
