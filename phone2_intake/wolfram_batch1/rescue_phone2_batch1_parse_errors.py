import csv
import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\TZPIDProof\phone2_intake\wolfram_batch1")
SOURCE = ROOT / "phone2_batch1_wolfram_certificate_results.csv"
RESCUE_JSON = ROOT / "phone2_batch1_parse_error_rescue_candidates.json"
WLS = ROOT / "phone2_batch1_parse_error_rescue.wls"
RESULTS_JSON = ROOT / "phone2_batch1_parse_error_rescue_results.json"
RESULTS_CSV = ROOT / "phone2_batch1_parse_error_rescue_results.csv"
REPORT = ROOT / "PHONE2_BATCH1_PARSE_ERROR_RESCUE_REPORT.md"


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def wl_string(text: str) -> str:
    return json.dumps(text or "", ensure_ascii=False)


def normalize_identifiers(s: str) -> str:
    s = s or ""
    s = s.replace("M̄", "MBar")
    s = s.replace("ⱼ", "j").replace("ᵢ", "i")
    s = s.translate(str.maketrans("₀₁₂₃₄₅₆₇₈₉", "0123456789"))
    supers = {"²": "^2", "³": "^3", "⁴": "^4"}
    for old, new in supers.items():
        s = s.replace(old, new)
    replacements = [
        ("→", "->"),
        ("↦", "->"),
        ("⊔", "DisjointUnion"),
        ("⊆", "SubsetEqual"),
        ("∈", " in "),
        ("∀", " ForAll "),
        ("∃", " Exists "),
        ("≠", "!="),
        ("≤", "<="),
        ("≥", ">="),
        ("≅", "=="),
        ("∘", "CircleComposition"),
        ("⊗", "CircleTimes"),
        ("⊕", "CirclePlus"),
        ("⋃", "Union"),
        ("⟨⟩", "EmptyQueue[]"),
        ("∂", "Boundary"),
        ("λ", "lambda"),
        ("τ", "tau"),
        ("ρ", "rho"),
        ("Φ", "Phi"),
    ]
    for old, new in replacements:
        s = s.replace(old, new)
    s = re.sub(r"\bc'\b", "cPrime", s)
    s = re.sub(r"\b([A-Za-z][A-Za-z0-9]*)_([A-Za-z0-9]+)\b", r"\1\2", s)
    s = re.sub(r"~\s*(\d+)\s*ns\b", r'Quantity[\1, "Nanoseconds"]', s)
    s = re.sub(r"~\s*(\d+)\s*ms\b", r'Quantity[\1, "Milliseconds"]', s)
    s = re.sub(r"\s+", " ", s.strip(" ,.;"))
    return s


def likely_fragment(canonical: str, candidate: str) -> bool:
    text = (candidate or canonical or "").strip()
    if not text:
        return True
    if text.endswith(("->", "==", ":=", "=", "<|", "[", "+", "*", ":", "{")):
        return True
    if text.count("[") != text.count("]") or text.count("{") != text.count("}"):
        return True
    if re.search(r"\{\s*[A-Za-z].*==", text) and text.count("{") != text.count("}"):
        return True
    return False


def balance_brackets(s: str) -> str:
    pairs = [("[", "]"), ("(", ")"), ("{", "}")]
    out = s
    for left, right in pairs:
        diff = out.count(left) - out.count(right)
        if diff > 0:
            out += right * diff
    return out


def equation_rescue(canonical: str, candidate: str) -> str:
    s = normalize_identifiers(candidate or canonical)
    # Convert visual absolute-value bars used in a few probability expressions.
    s = re.sub(r"\|([^|\[\]]{1,80})\|", r"Abs[\1]", s)
    # Make common typed/rule clauses into inert symbolic relations.
    if ":" in s and "->" in s:
        left, right = s.split("->", 1)
        return f"Phone2Relation[{left.strip()}, {wl_string(right.strip())}]"
    if ":=" in s:
        left, right = s.split(":=", 1)
        if right.strip():
            return f"SetDelayed[{left.strip()}, Phone2Predicate[{wl_string(right.strip())}]]"
    if "==" in s:
        return s
    if "->" in s:
        left, right = s.split("->", 1)
        if left.strip() and right.strip():
            return f"Rule[{left.strip()}, Phone2Expression[{wl_string(right.strip())}]]"
    if "=" in s:
        left, right = s.split("=", 1)
        if left.strip() and right.strip():
            return balance_brackets(f"Equal[{left.strip()}, Phone2Expression[{wl_string(right.strip())}]]")
    return balance_brackets(s)


def carrier_expr(row: dict, rescue_class: str) -> str:
    return (
        "Phone2EquationCarrier["
        + wl_string(row["id"])
        + ", <|"
        + '"canonical" -> '
        + wl_string(row["canonical_equation"])
        + ', "previousCandidate" -> '
        + wl_string(row["wolfram_candidate"])
        + ', "rescueClass" -> '
        + wl_string(rescue_class)
        + "|>]"
    )


def main() -> None:
    rows = [r for r in csv.DictReader(SOURCE.open(encoding="utf-8-sig", newline="")) if r["status"] == "wolfram_parse_error"]
    out = []
    for row in rows:
        rescue_class = "fragment_carrier" if likely_fragment(row["canonical_equation"], row["wolfram_candidate"]) else "equation_candidate"
        eq = equation_rescue(row["canonical_equation"], row["wolfram_candidate"])
        out.append(
            {
                "id": row["id"],
                "title": row["title"],
                "canonical_equation": row["canonical_equation"],
                "previous_wolfram_candidate": row["wolfram_candidate"],
                "rescue_class": rescue_class,
                "equation_rescue_candidate": eq,
                "carrier_candidate": carrier_expr(row, rescue_class),
            }
        )
    RESCUE_JSON.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")

    rescue_path = str(RESCUE_JSON).replace("\\", "\\\\")
    results_path = str(RESULTS_JSON).replace("\\", "\\\\")
    wls = f'''$HistoryLength = 0;
candidates = Import["{rescue_path}", "RawJSON"];

ClearAll[attemptParse];
attemptParse[expr_String] := Quiet[
  Check[ToExpression[expr, InputForm, HoldComplete], $Failed],
  {{ToExpression::sntx, ToExpression::sntxi, Syntax::sntxf, Syntax::tsntxi, General::stop}}
];

ClearAll[checkOne];
checkOne[row_] := Module[{{eqHeld, carrierHeld, status, message, used}},
  eqHeld = attemptParse[row["equation_rescue_candidate"]];
  If[eqHeld =!= $Failed,
    status = "wolfram_rescue_equation_parse_verified";
    message = "rescued equation candidate parsed under HoldComplete";
    used = row["equation_rescue_candidate"],
    carrierHeld = attemptParse[row["carrier_candidate"]];
    If[carrierHeld =!= $Failed,
      status = If[row["rescue_class"] === "fragment_carrier", "wolfram_fragment_carrier_verified", "wolfram_symbolic_carrier_verified"];
      message = "carrier parsed under HoldComplete; not a complete semantic equation proof";
      used = row["carrier_candidate"],
      status = "wolfram_rescue_failed";
      message = "equation and carrier parse failed";
      used = row["equation_rescue_candidate"]
    ]
  ];
  <|
    "id" -> row["id"],
    "title" -> row["title"],
    "previous_status" -> "wolfram_parse_error",
    "rescue_status" -> status,
    "message" -> message,
    "rescue_class" -> row["rescue_class"],
    "canonical_equation" -> row["canonical_equation"],
    "previous_wolfram_candidate" -> row["previous_wolfram_candidate"],
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
    print(json.dumps({"parse_errors": len(out), "json": str(RESCUE_JSON), "wls": str(WLS)}, indent=2))


if __name__ == "__main__":
    main()
