$HistoryLength = 0;
candidates = Import["D:\\TZPIDProof\\phone2_intake\\theorem_toe\\wolfram_gold_anchor_batch2\\phone2_gold_anchor_batch2_wolfram_candidates.json", "RawJSON"];
ClearAll[attemptParse];
attemptParse[expr_String] := Quiet[
  Check[ToExpression[expr, InputForm, HoldComplete], $Failed],
  {ToExpression::sntx, ToExpression::sntxi, Syntax::sntxf, Syntax::tsntxi, General::stop}
];
checkOne[row_] := Module[{held, carrierHeld, status, message, used},
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
summary = <|"generated_utc" -> "2026-06-11T06:56:35Z", "total" -> Length[results],
  "status_counts" -> Counts[results[[All, "status"]]], "results" -> results|>;
Export["D:\\TZPIDProof\\phone2_intake\\theorem_toe\\wolfram_gold_anchor_batch2\\phone2_gold_anchor_batch2_wolfram_certificate_results.json", summary, "RawJSON"];
Print[ExportString[KeyDrop[summary, "results"], "RawJSON"]];
