import csv
import json
from pathlib import Path


ROOT = Path(r"D:\TZPIDProof")
INTAKE = ROOT / "phone2_intake"
WOLFRAM_CSV = INTAKE / "PHONE2_WOLFRAM_MODULE_CANDIDATES.csv"
WOLFRAM_JSON = INTAKE / "phone2_wolfram_parse_candidates.json"
WLS = INTAKE / "phone2_wolfram_parse_check.wls"
RESULTS = INTAKE / "PHONE2_WOLFRAM_PARSE_RESULTS.json"
RESULTS_CSV = INTAKE / "PHONE2_WOLFRAM_PARSE_RESULTS.csv"
SUMMARY_MD = INTAKE / "PHONE2_WOLFRAM_PARSE_REPORT.md"


def main():
    rows = []
    with WOLFRAM_CSV.open(encoding="utf-8-sig", newline="") as handle:
        for i, row in enumerate(csv.DictReader(handle), start=1):
            code = row.get("cleaned_code", "")
            if len(code) > 6000:
                code = code[:6000]
            rows.append({
                "index": i,
                "source_file": row.get("source_file", ""),
                "line_number": row.get("line_number", ""),
                "module_name": row.get("module_name", ""),
                "source_type": row.get("source_type", ""),
                "code": code,
            })

    WOLFRAM_JSON.write_text(json.dumps(rows, indent=2, ensure_ascii=False), encoding="utf-8")
    candidate_path = str(WOLFRAM_JSON).replace("\\", "\\\\")
    results_path = str(RESULTS).replace("\\", "\\\\")
    results_csv_path = str(RESULTS_CSV).replace("\\", "\\\\")

    script = f'''entries = Import["{candidate_path}", "RawJSON"];

checkOne[entry_] := Module[{{held, status, message}},
  held = Quiet[Check[ToExpression[entry["code"], InputForm, HoldComplete], $Failed]];
  If[held === $Failed,
    status = "parse_error"; message = "ToExpression failed",
    status = "parse_ok"; message = "held expression parsed"
  ];
  <|
    "index" -> entry["index"],
    "source_file" -> entry["source_file"],
    "line_number" -> entry["line_number"],
    "module_name" -> entry["module_name"],
    "source_type" -> entry["source_type"],
    "status" -> status,
    "message" -> message
  |>
];

results = checkOne /@ entries;
summary = <|
  "total" -> Length[results],
  "parse_ok" -> Count[results[[All, "status"]], "parse_ok"],
  "parse_error" -> Count[results[[All, "status"]], "parse_error"],
  "results" -> results
|>;

Export["{results_path}", summary, "RawJSON"];
Export["{results_csv_path}", results, "CSV"];
Print[ExportString[KeyDrop[summary, "results"], "RawJSON"]];
'''
    WLS.write_text(script, encoding="utf-8")
    print(json.dumps({"wls": str(WLS), "candidates": len(rows), "results": str(RESULTS)}, indent=2))


if __name__ == "__main__":
    main()
