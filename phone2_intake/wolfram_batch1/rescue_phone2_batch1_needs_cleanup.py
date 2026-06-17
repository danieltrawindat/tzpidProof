import csv
import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\TZPIDProof")
WB = ROOT / "phone2_intake" / "wolfram_batch1"
MASTER = ROOT / "TZPID_ALL_IDS_CANONICAL_EQUATION_MASTER_with_export.csv"

RESCUE_JSON = WB / "phone2_batch1_needs_cleanup_rescue_candidates.json"
WLS = WB / "phone2_batch1_needs_cleanup_rescue.wls"
RESULTS_JSON = WB / "phone2_batch1_needs_cleanup_rescue_results.json"
RESULTS_CSV = WB / "phone2_batch1_needs_cleanup_rescue_results.csv"


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def wl_string(text: str) -> str:
    return json.dumps(text or "", ensure_ascii=False)


def normalize(s: str) -> str:
    s = s or ""
    s = re.sub(r"\(\*.*?(?:\*/|\*\))", "", s)
    s = s.translate(str.maketrans("₀₁₂₃₄₅₆₇₈₉", "0123456789"))
    for old, new in {"²": "^2", "³": "^3", "⁴": "^4"}.items():
        s = s.replace(old, new)
    replacements = [
        ("→", "->"),
        ("↦", "->"),
        ("≤", "<="),
        ("≥", ">="),
        ("≈", "=="),
        ("≅", "=="),
        ("×", "*"),
        ("·", "*"),
        ("∂", "d"),
        ("∫", "Integrate"),
        ("𝒟", "MeasureD"),
        ("𝒮", "Action"),
        ("𝓣", "ToposT"),
        ("ℒ", "Lagrangian"),
        ("ħ", "hbar"),
        ("ρ", "rho"),
        ("τ", "tau"),
        ("θ", "theta"),
        ("α", "alpha"),
        ("δ", "delta"),
        ("Π", "PiTensor"),
        ("π", "Pi"),
        ("Φ", "Phi"),
        ("ψ", "psi"),
    ]
    for old, new in replacements:
        s = s.replace(old, new)
    s = re.sub(r"\\frac\{([^{}]+)\}\{([^{}]+)\}", r"(\1)/(\2)", s)
    s = re.sub(r"\\sqrt\{([^{}]+)\}", r"Sqrt[\1]", s)
    s = s.replace("\\", "")
    s = re.sub(r"\b([A-Za-z][A-Za-z0-9]*)_([A-Za-z0-9]+)\b", r"\1\2", s)
    s = re.sub(r"~\s*(\d+)\s*ns\b", r'Quantity[\1, "Nanoseconds"]', s)
    s = re.sub(r"~\s*(\d+)\s*ms\b", r'Quantity[\1, "Milliseconds"]', s)
    s = re.sub(r"\s+", " ", s.strip(" ,.;"))
    if ":=" not in s and "==" not in s and re.search(r"(?<![<>=!])=(?![=>])", s):
        s = re.sub(r"(?<![<>=!])=(?![=>])", "==", s, count=1)
    return s


def balance(s: str) -> str:
    out = s
    for left, right in [("[", "]"), ("(", ")"), ("{", "}")]:
        diff = out.count(left) - out.count(right)
        if diff > 0:
            out += right * diff
    return out


def is_hard_fragment(original: str, cleaned: str) -> bool:
    o = (original or "").strip()
    c = (cleaned or "").strip()
    if not c:
        return True
    if o.endswith(("[", "+", "*", "/", ",", "=", "==", ":=", "->", "<|")):
        return True
    if re.search(r"\b(Module|Category|HigherTopos|Case|If|Sum|Integrate|Sequence)\[$", o):
        return True
    if c.endswith(("+", "*", "/", ",", "==", ":=", "->", "<|")):
        return True
    return False


def rescue_expression(original: str) -> tuple[str, str]:
    cleaned = normalize(original)
    if is_hard_fragment(original, cleaned):
        return "fragment_carrier", carrier_expr("", original, "hard_fragment")
    # Try bracket closure for near-complete function calls/equalities.
    balanced = balance(cleaned)
    if "==" in balanced or ":=" in balanced or "->" in balanced:
        return "balanced_equation_candidate", balanced
    if balanced:
        return "balanced_expression_candidate", balanced
    return "fragment_carrier", carrier_expr("", original, "empty_after_cleaning")


def carrier_expr(tzpid: str, original: str, rescue_class: str) -> str:
    return (
        "Phone2EquationCarrier["
        + wl_string(tzpid)
        + ", <|"
        + '"canonical" -> '
        + wl_string(original)
        + ', "rescueClass" -> '
        + wl_string(rescue_class)
        + "|>]"
    )


def main() -> None:
    rows = []
    with MASTER.open(encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            try:
                n = int(row["id"][2:])
            except Exception:
                continue
            status = (row.get("wolfram_status") or "").split(";")[0]
            if 10872 <= n <= 11121 and status == "wolfram_needs_cleanup":
                rescue_class, expr = rescue_expression(row.get("canonical_equation", ""))
                if rescue_class == "fragment_carrier":
                    expr = carrier_expr(row["id"], row.get("canonical_equation", ""), "hard_fragment")
                rows.append(
                    {
                        "id": row["id"],
                        "title": row.get("title", ""),
                "canonical_equation": row.get("canonical_equation", ""),
                "rescue_class": rescue_class,
                "rescue_wolfram_candidate": expr,
                "carrier_candidate": carrier_expr(row["id"], row.get("canonical_equation", ""), rescue_class),
            }
        )

    RESCUE_JSON.write_text(json.dumps(rows, indent=2, ensure_ascii=False), encoding="utf-8")
    json_path = str(RESCUE_JSON).replace("\\", "\\\\")
    results_path = str(RESULTS_JSON).replace("\\", "\\\\")
    wls = f'''$HistoryLength = 0;
candidates = Import["{json_path}", "RawJSON"];

ClearAll[attemptParse];
attemptParse[expr_String] := Quiet[
  Check[ToExpression[expr, InputForm, HoldComplete], $Failed],
  {{ToExpression::sntx, ToExpression::sntxi, Syntax::sntxf, Syntax::tsntxi, General::stop}}
];

ClearAll[checkOne];
checkOne[row_] := Module[{{held, carrierHeld, status, message, used}},
  held = attemptParse[row["rescue_wolfram_candidate"]];
  If[held === $Failed,
    carrierHeld = attemptParse[row["carrier_candidate"]];
    If[carrierHeld === $Failed,
      status = "wolfram_cleanup_rescue_failed";
      message = "cleanup candidate and carrier failed to parse";
      used = row["rescue_wolfram_candidate"],
      status = "wolfram_cleanup_fragment_carrier_verified";
      message = "fallback carrier parsed under HoldComplete";
      used = row["carrier_candidate"]
    ],
    status = Switch[row["rescue_class"],
      "balanced_equation_candidate", "wolfram_cleanup_equation_parse_verified",
      "balanced_expression_candidate", "wolfram_cleanup_expression_parse_verified",
      _, "wolfram_cleanup_fragment_carrier_verified"
    ];
    message = "cleanup candidate parsed under HoldComplete";
    used = row["rescue_wolfram_candidate"]
  ];
  <|
    "id" -> row["id"],
    "title" -> row["title"],
    "previous_status" -> "wolfram_needs_cleanup",
    "rescue_status" -> status,
    "message" -> message,
    "rescue_class" -> row["rescue_class"],
    "canonical_equation" -> row["canonical_equation"],
    "rescue_wolfram_candidate" -> used
  |>
];

results = checkOne /@ candidates;
summary = <|
  "generated_utc" -> "{now_utc()}",
  "total" -> Length[results],
  "status_counts" -> Counts[results[[All, "rescue_status"]]],
  "results" -> results
|>;
Export["{results_path}", summary, "RawJSON"];
Print[ExportString[KeyDrop[summary, "results"], "RawJSON"]];
'''
    WLS.write_text(wls, encoding="utf-8")
    print(json.dumps({"needs_cleanup": len(rows), "json": str(RESCUE_JSON), "wls": str(WLS)}, indent=2))


if __name__ == "__main__":
    main()
