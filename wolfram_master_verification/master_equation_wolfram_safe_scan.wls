inputPath = Part[$ScriptCommandLine, -2];
outputPath = Part[$ScriptCommandLine, -1];

segments = Import[inputPath, "RawJSON"];

ClearAll[safeNumericQ, normalizeNumericRelation, evalNumericRelation, statusFor];

safeNumericQ[s_String] := StringMatchQ[
  StringDelete[s, WhitespaceCharacter],
  RegularExpression["[0-9\\.\\+\\-\\*/\\^\\(\\)=<>]+"] ..
];

normalizeNumericRelation[s_String] := Module[{t = StringDelete[s, WhitespaceCharacter]},
  t = StringReplace[t, "==" -> "="];
  If[StringContainsQ[t, "="],
    StringReplace[t, "=" -> "==", 1],
    t
  ]
];

evalNumericRelation[s_String] := Module[{expr, norm = normalizeNumericRelation[s]},
  Quiet @ Check[
    TimeConstrained[
      expr = ToExpression[norm, InputForm, HoldComplete];
      Which[
        MatchQ[expr, HoldComplete[_Equal | _Less | _Greater | _LessEqual | _GreaterEqual]],
          If[TrueQ[ReleaseHold[expr]], "wolfram_direct_numeric_pass", "wolfram_direct_numeric_fail"],
        True,
          "wolfram_numeric_expression_computed"
      ],
      0.05,
      "wolfram_numeric_timeout"
    ],
    "wolfram_numeric_parse_error"
  ]
];

statusFor[seg_Association] := Module[{s = seg["segment"], cls = seg["class"]},
  Which[
    StringLength[StringTrim[s]] == 0,
      "empty",
    safeNumericQ[s],
      evalNumericRelation[s],
    cls == "operator_latex",
      "classified_operator_latex_needs_semantic_translation",
    cls == "logical_latex",
      "classified_logical_latex_needs_hol_translation",
    cls == "elementary_latex",
      "classified_elementary_latex_candidate",
    cls == "relation_latex",
      "classified_relation_latex_candidate",
    True,
      "classified_symbolic_latex_candidate"
  ]
];

results = Table[
  Module[{seg = segments[[i]], status},
    status = statusFor[seg];
    <|
      "row" -> seg["row"],
      "id" -> seg["id"],
      "title" -> seg["title"],
      "segment_index" -> seg["segment_index"],
      "class" -> seg["class"],
      "length" -> seg["length"],
      "segment" -> seg["segment"],
      "status" -> status,
      "engine" -> "WolframScript",
      "claim_boundary" -> "Full-master Wolfram safe scan: every equation segment is processed; direct pass/fail is only asserted for Wolfram-safe numeric relations. Other LaTeX segments are classified for semantic/HOL/Wolfram follow-up."
    |>
  ],
  {i, Length[segments]}
];

Export[outputPath, results, "RawJSON"];
Print["Scanned segments: " <> ToString[Length[results]]];
Print[Counts[results[[All, "status"]]]];
