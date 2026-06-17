entries = Import["D:\\TZPIDProof\\phone2_intake\\phone2_wolfram_parse_candidates.json", "RawJSON"];

checkOne[entry_] := Module[{held, status, message},
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

Export["D:\\TZPIDProof\\phone2_intake\\PHONE2_WOLFRAM_PARSE_RESULTS.json", summary, "RawJSON"];
Export["D:\\TZPIDProof\\phone2_intake\\PHONE2_WOLFRAM_PARSE_RESULTS.csv", results, "CSV"];
Print[ExportString[KeyDrop[summary, "results"], "RawJSON"]];
