$HistoryLength = 0;
candidates = Import["D:\\TZPIDProof\\phone2_intake\\wolfram_batch1\\phone2_batch1_wolfram_candidates.json", "RawJSON"];

ClearAll[parseCandidate];
parseCandidate[row_] := Module[{held, status, message, freeSymbols},
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
    {ToExpression::sntx, Syntax::sntxf, Syntax::tsntxi, General::stop}
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
  "generated_utc" -> "2026-06-11T06:28:54Z",
  "total" -> Length[results],
  "status_counts" -> Counts[results[[All, "status"]]],
  "results" -> results
|>;
Export["D:\\TZPIDProof\\phone2_intake\\wolfram_batch1\\phone2_batch1_wolfram_certificate_results.json", summary, "RawJSON"];
Print[ExportString[KeyDrop[summary, "results"], "RawJSON"]];
