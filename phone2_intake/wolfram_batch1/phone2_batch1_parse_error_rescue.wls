$HistoryLength = 0;
candidates = Import["D:\\TZPIDProof\\phone2_intake\\wolfram_batch1\\phone2_batch1_parse_error_rescue_candidates.json", "RawJSON"];

ClearAll[attemptParse];
attemptParse[expr_String] := Quiet[
  Check[ToExpression[expr, InputForm, HoldComplete], $Failed],
  {ToExpression::sntx, ToExpression::sntxi, Syntax::sntxf, Syntax::tsntxi, General::stop}
];

ClearAll[checkOne];
checkOne[row_] := Module[{eqHeld, carrierHeld, status, message, used},
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
  "generated_utc" -> "2026-06-11T06:33:40Z",
  "total" -> Length[results],
  "status_counts" -> Counts[results[[All, "rescue_status"]]],
  "results" -> results
|>;
Export["D:\\TZPIDProof\\phone2_intake\\wolfram_batch1\\phone2_batch1_parse_error_rescue_results.json", summary, "RawJSON"];
Print[ExportString[KeyDrop[summary, "results"], "RawJSON"]];
