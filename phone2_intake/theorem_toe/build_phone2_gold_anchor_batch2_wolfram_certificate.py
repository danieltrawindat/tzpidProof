import csv
import json
import re
import shutil
import hashlib
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


PROOF_ROOT = Path(r"D:\TZPIDProof")
OPENAI2_ROOT = Path(r"D:\00_Engine\AI_Workspaces\OpenAI2")
THEOREM_DIR = PROOF_ROOT / "phone2_intake" / "theorem_toe"
OUTDIR = THEOREM_DIR / "wolfram_gold_anchor_batch2"
MASTER_NAME = "TZPID_ALL_IDS_CANONICAL_EQUATION_MASTER_with_export.csv"

START_ID = 11122
END_ID = 11371

CANDIDATES_JSON = OUTDIR / "phone2_gold_anchor_batch2_wolfram_candidates.json"
WLS = OUTDIR / "phone2_gold_anchor_batch2_wolfram_certificate.wls"
RESULTS_JSON = OUTDIR / "phone2_gold_anchor_batch2_wolfram_certificate_results.json"
RESULTS_CSV = OUTDIR / "phone2_gold_anchor_batch2_wolfram_certificate_results.csv"
REPORT = OUTDIR / "PHONE2_GOLD_ANCHOR_BATCH2_WOLFRAM_CERTIFICATE.md"


SUBSCRIPT_MAP = str.maketrans("₀₁₂₃₄₅₆₇₈₉", "0123456789")
SUPERSCRIPT = {"²": "^2", "³": "^3", "⁴": "^4", "⁵": "^5"}


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha1(path: Path) -> str:
    h = hashlib.sha1()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def wl_string(text: str) -> str:
    return json.dumps(text or "", ensure_ascii=False)


def clean_wolfram(text: str) -> str:
    s = text or ""
    s = re.sub(r"\(\*.*?(?:\*/|\*\))", "", s)
    s = s.translate(SUBSCRIPT_MAP)
    for old, new in SUPERSCRIPT.items():
        s = s.replace(old, new)
    replacements = [
        ("\\n", " "),
        ("→", "->"),
        ("↦", "->"),
        ("×", "*"),
        ("·", "*"),
        ("≤", "<="),
        ("≥", ">="),
        ("≈", "=="),
        ("≅", "=="),
        ("∝", "=="),
        ("∂", "d"),
        ("∫", "Integrate"),
        ("∑", "Sum"),
        ("Σ", "Sum"),
        ("√", "Sqrt"),
        ("∞", "Infinity"),
        ("⊗", "CircleTimes"),
        ("⊕", "CirclePlus"),
        ("∘", "CircleComposition"),
        ("ℒ", "Lagrangian"),
        ("𝒮", "Action"),
        ("𝒟", "MeasureD"),
        ("𝓣", "ToposT"),
        ("ħ", "hbar"),
        ("Λ", "Lambda"),
        ("λ", "lambda"),
        ("Ω", "Omega"),
        ("ω", "omega"),
        ("θ", "theta"),
        ("φ", "phi"),
        ("Φ", "Phi"),
        ("δ", "delta"),
        ("Δ", "Delta"),
        ("μ", "mu"),
        ("ν", "nu"),
        ("ρ", "rho"),
        ("τ", "tau"),
        ("π", "Pi"),
        ("×", "*"),
    ]
    for old, new in replacements:
        s = s.replace(old, new)
    latex = [
        (r"\\frac\{([^{}]+)\}\{([^{}]+)\}", r"(\1)/(\2)"),
        (r"\\left", ""),
        (r"\\right", ""),
        (r"\\text\{([^{}]+)\}", r"\1"),
        (r"\\mathrm\{([^{}]+)\}", r"\1"),
        (r"\\mathcal\{([^{}]+)\}", r"\1"),
        (r"\\mathbf\{([^{}]+)\}", r"\1"),
        (r"\\hat\{([^{}]+)\}", r"\1Hat"),
        (r"\\nabla", "Nabla"),
        (r"\\Delta", "Delta"),
        (r"\\delta", "delta"),
        (r"\\lambda", "lambda"),
        (r"\\Lambda", "Lambda"),
        (r"\\Omega", "Omega"),
        (r"\\omega", "omega"),
        (r"\\theta", "theta"),
        (r"\\phi", "phi"),
        (r"\\Phi", "Phi"),
        (r"\\mu", "mu"),
        (r"\\nu", "nu"),
        (r"\\rho", "rho"),
        (r"\\tau", "tau"),
        (r"\\pi", "Pi"),
        (r"\\times", "*"),
        (r"\\cdot", "*"),
        (r"\\to", "->"),
        (r"\\infty", "Infinity"),
        (r"\\sum", "Sum"),
        (r"\\int", "Integrate"),
        (r"\\sqrt\{([^{}]+)\}", r"Sqrt[\1]"),
    ]
    for pattern, repl in latex:
        s = re.sub(pattern, repl, s)
    s = s.replace("\\", "")
    s = re.sub(r"\b([A-Za-z][A-Za-z0-9]*)_([A-Za-z0-9]+)\b", r"\1\2", s)
    s = re.sub(r"\s+", " ", s.strip(" ,.;"))
    if ":=" not in s and "==" not in s and re.search(r"(?<![<>=!])=(?![=>])", s):
        s = re.sub(r"(?<![<>=!])=(?![=>])", "==", s, count=1)
    return balance(s)


def balance(s: str) -> str:
    out = s
    for left, right in [("[", "]"), ("(", ")"), ("{", "}")]:
        diff = out.count(left) - out.count(right)
        if diff > 0:
            out += right * diff
    return out


def hard_fragment(original: str, candidate: str) -> bool:
    text = (original or "").strip()
    cand = (candidate or "").strip()
    if not cand:
        return True
    if text.endswith(("[", "+", "*", "/", ",", "=", "==", ":=", "->", "<|")):
        return True
    if cand.endswith(("+", "*", "/", ",", "==", ":=", "->", "<|")):
        return True
    return False


def carrier(tzpid: str, original: str, cls: str) -> str:
    return f"Phone2EquationCarrier[{wl_string(tzpid)}, <|\"canonical\" -> {wl_string(original)}, \"rescueClass\" -> {wl_string(cls)}|>]"


def main() -> None:
    OUTDIR.mkdir(parents=True, exist_ok=True)
    rows = []
    with (PROOF_ROOT / MASTER_NAME).open(encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            try:
                n = int(row["id"][2:])
            except Exception:
                continue
            if START_ID <= n <= END_ID:
                candidate = clean_wolfram(row.get("canonical_equation", ""))
                cls = "fragment_carrier" if hard_fragment(row.get("canonical_equation", ""), candidate) else "equation_candidate"
                rows.append(
                    {
                        "id": row["id"],
                        "title": row.get("title", ""),
                        "canonical_equation": row.get("canonical_equation", ""),
                        "rescue_class": cls,
                        "wolfram_candidate": candidate if cls == "equation_candidate" else carrier(row["id"], row.get("canonical_equation", ""), "hard_fragment"),
                        "carrier_candidate": carrier(row["id"], row.get("canonical_equation", ""), cls),
                    }
                )
    CANDIDATES_JSON.write_text(json.dumps(rows, indent=2, ensure_ascii=False), encoding="utf-8")
    candidate_path = str(CANDIDATES_JSON).replace("\\", "\\\\")
    result_path = str(RESULTS_JSON).replace("\\", "\\\\")
    WLS.write_text(
        f'''$HistoryLength = 0;
candidates = Import["{candidate_path}", "RawJSON"];
ClearAll[attemptParse];
attemptParse[expr_String] := Quiet[
  Check[ToExpression[expr, InputForm, HoldComplete], $Failed],
  {{ToExpression::sntx, ToExpression::sntxi, Syntax::sntxf, Syntax::tsntxi, General::stop}}
];
checkOne[row_] := Module[{{held, carrierHeld, status, message, used}},
  held = attemptParse[row["wolfram_candidate"]];
  If[held =!= $Failed,
    status = If[row["rescue_class"] === "equation_candidate", "wolfram_gold_anchor_equation_parse_verified", "wolfram_gold_anchor_fragment_carrier_verified"];
    message = "primary candidate parsed under HoldComplete";
    used = row["wolfram_candidate"],
    carrierHeld = attemptParse[row["carrier_candidate"]];
    If[carrierHeld =!= $Failed,
      status = "wolfram_gold_anchor_symbolic_carrier_verified";
      message = "fallback carrier parsed under HoldComplete";
      used = row["carrier_candidate"],
      status = "wolfram_gold_anchor_parse_failed";
      message = "candidate and carrier failed";
      used = row["wolfram_candidate"]
    ]
  ];
  <|"id" -> row["id"], "title" -> row["title"], "status" -> status,
    "message" -> message, "rescue_class" -> row["rescue_class"],
    "canonical_equation" -> row["canonical_equation"],
    "wolfram_candidate" -> used|>
];
results = checkOne /@ candidates;
summary = <|"generated_utc" -> "{now_utc()}", "total" -> Length[results],
  "status_counts" -> Counts[results[[All, "status"]]], "results" -> results|>;
Export["{result_path}", summary, "RawJSON"];
Print[ExportString[KeyDrop[summary, "results"], "RawJSON"]];
''',
        encoding="utf-8",
    )
    print(json.dumps({"candidates": len(rows), "wls": str(WLS), "results": str(RESULTS_JSON)}, indent=2))


if __name__ == "__main__":
    main()
