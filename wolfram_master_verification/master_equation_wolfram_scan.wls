inputPath = Part[$ScriptCommandLine, -2];
outputPath = Part[$ScriptCommandLine, -1];

segments = Import[inputPath, "RawJSON"];

ClearAll[tryTeXParse, classifyParsed, statusOf];

tryTeXParse[s_String] := Module[{held},
  Quiet @ Check[
    TimeConstrained[
      held = ToExpression[s, TeXForm, HoldComplete];
      <|"ok" -> True, "held" -> ToString[held, InputForm]|>,
      0.25,
      <|"ok" -> False, "error" -> "timeout"|>
    ],
    <|"ok" -> False, "error" -> "parse_error"|>
  ]
];

statusOf[assoc_] := If[TrueQ[assoc["ok"]], "wolfram_tex_parse_pass", assoc["error"]];

results = Table[
  Module[{seg = segments[[i]], parsed, status},
    parsed = tryTeXParse[seg["segment"]];
    status = statusOf[parsed];
    <|
      "row" -> seg["row"],
      "id" -> seg["id"],
      "title" -> seg["title"],
      "segment_index" -> seg["segment_index"],
      "class" -> seg["class"],
      "length" -> seg["length"],
      "segment" -> seg["segment"],
      "status" -> status,
      "parsed_inputform" -> If[TrueQ[parsed["ok"]], parsed["held"], ""],
      "claim_boundary" -> "Full-master Wolfram scan: status records TeXForm parseability/evaluability, not a proof of physical truth."
    |>
  ],
  {i, Length[segments]}
];

Export[outputPath, results, "RawJSON"];
Print["Scanned segments: " <> ToString[Length[results]]];
Print[Counts[results[[All, "status"]]]];
