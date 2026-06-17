$HistoryLength = 0;
candidates = Import["D:\\TZPIDProof\\phone2_intake\\wolfram_batch1\\phone2_batch1_needs_cleanup_rescue_candidates.json", "RawJSON"];

ClearAll[attemptParse];
attemptParse[expr_String] := Quiet[
  Check[ToExpression[expr, InputForm, HoldComplete], $Failed],
  {ToExpression::sntx, ToExpression::sntxi, Syntax::sntxf, Syntax::tsntxi, General::stop}
];

ClearAll[checkOne];
checkOne[row_] := Module[{held, carrierHeld, status, message, used},
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
  "generated_utc" -> "2026-06-11T06:38:22Z",
  "total" -> Length[results],
  "status_counts" -> Counts[results[[All, "rescue_status"]]],
  "results" -> results
|>;
Export["D:\\TZPIDProof\\phone2_intake\\wolfram_batch1\\phone2_batch1_needs_cleanup_rescue_results.json", summary, "RawJSON"];
Print[ExportString[KeyDrop[summary, "results"], "RawJSON"]];
