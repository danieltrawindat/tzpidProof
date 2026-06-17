queue = Import["D:\\TZPIDProof\\peer_review\\coverage\\zenodo_targeted_wolfram\\zenodo_targeted_wolfram_queue.json", "RawJSON"];
verify[item_] := Module[{expr, status, message = ""},
  expr = Quiet @ Check[
     TimeConstrained[
       ToExpression[item["wolfram_input"], InputForm, HoldComplete],
       20,
       $TimedOut
     ],
     $Failed
   ];
  status = Which[
    expr === $TimedOut, "timeout",
    expr === $Failed, "parse_error",
    True, "pass"
  ];
  <|
    "id" -> item["id"],
    "block_index" -> item["block_index"],
    "status" -> status,
    "wolfram_input" -> item["wolfram_input"],
    "paper_keys" -> item["paper_keys"],
    "source_method" -> item["source_method"]
  |>
];
results = verify /@ queue;
Export["D:\\TZPIDProof\\peer_review\\coverage\\zenodo_targeted_wolfram\\zenodo_targeted_wolfram_results.json", results, "RawJSON"];
Print["verified ", Length[results], " Wolfram carrier blocks"];