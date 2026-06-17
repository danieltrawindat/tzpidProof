$HistoryLength = 0;
candidates = Import["D:\\TZPIDProof\\phone2_intake\\theorem_toe\\theorem_toe_wolfram_parse_candidates.json", "RawJSON"];
checkOne[row_] := Module[{held,status,message},
  held = Quiet[Check[ToExpression[row["code"], InputForm, HoldComplete], $Failed], {ToExpression::sntx, ToExpression::sntxi, Syntax::sntxf, Syntax::tsntxi, General::stop}];
  If[held === $Failed, status="parse_error"; message="ToExpression failed", status="parse_ok"; message="parsed under HoldComplete"];
  <|"index"->row["index"],"name"->row["name"],"path"->row["path"],"length"->row["length"],"status"->status,"message"->message|>
];
results = checkOne /@ candidates;
summary = <|"total"->Length[results],"status_counts"->Counts[results[[All,"status"]]],"results"->results|>;
Export["D:\\TZPIDProof\\phone2_intake\\theorem_toe\\THEOREM_TOE_WOLFRAM_PARSE_RESULTS.json", summary, "RawJSON"];
Print[ExportString[KeyDrop[summary,"results"], "RawJSON"]];
