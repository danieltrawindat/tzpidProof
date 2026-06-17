If[Length[$ScriptCommandLine] < 3,
  Print["usage: wolframscript -file validate_wolfram_representations.wls <input.json> <output-dir>"];
  Exit[2];
];

inputPath = $ScriptCommandLine[[2]];
outDir = $ScriptCommandLine[[3]];
Quiet[CreateDirectory[outDir, CreateIntermediateDirectories -> True]];

data = Import[inputPath, "RawJSON"];

ClearAll[parseHeld, numericTruthStatus, validateBlock];

parseHeld[source_String] := Module[{parsed},
  parsed = Quiet[Check[ToExpression[source, InputForm, HoldComplete], $Failed]];
  If[parsed === $Failed,
    <|"status" -> "parse_error", "held_inputform" -> ""|>,
    <|"status" -> "parse_pass", "held_inputform" -> ToString[InputForm[parsed]]|>
  ]
];

numericTruthStatus[held_] := Module[{expr, eval},
  expr = Quiet[Check[ReleaseHold[held], $Failed]];
  If[expr === $Failed, Return["not_evaluable"]];
  eval = Quiet[Check[FullSimplify[expr], $Failed]];
  Which[
    eval === True, "numeric_or_symbolic_true",
    eval === False, "numeric_or_symbolic_false",
    NumberQ[eval], "numeric_computed",
    True, "symbolic_held"
  ]
];

validateBlock[row_, block_] := Module[
  {id, title, idx, repSource, candSource, repParse, candParse, candHeld, candEval = "not_attempted"},
  id = Lookup[row, "id", ""];
  title = Lookup[row, "title", ""];
  idx = Lookup[block, "block_index", Missing["block_index"]];
  repSource = Lookup[block, "wolfram_input", ""];
  candSource = Lookup[block, "candidate_wolfram_input", ""];
  repParse = parseHeld[repSource];
  If[StringQ[candSource] && StringLength[StringTrim[candSource]] > 0,
    candParse = parseHeld[candSource];
    If[candParse["status"] === "parse_pass",
      candHeld = ToExpression[candSource, InputForm, HoldComplete];
      candEval = numericTruthStatus[candHeld],
      candEval = "not_evaluable_parse_error"
    ],
    candParse = <|"status" -> "not_attempted", "held_inputform" -> ""|>
  ];
  <|
    "id" -> id,
    "title" -> title,
    "block_index" -> idx,
    "representation_status" -> "wolfram_representation_" <> repParse["status"],
    "representation_held_inputform" -> repParse["held_inputform"],
    "candidate_status" -> "candidate_" <> candParse["status"],
    "candidate_eval_status" -> candEval,
    "candidate_wolfram_input" -> candSource,
    "numeric_atoms" -> Lookup[block, "numeric_atoms", {}],
    "symbolic_tokens" -> Lookup[block, "symbolic_tokens", {}],
    "candidate_method" -> Lookup[block, "candidate_method", ""]
  |>
];

results = Flatten[
  Table[
    validateBlock[row, block],
    {row, data},
    {block, Lookup[row, "blocks", {}]}
  ],
  1
];

repCounts = Counts[Lookup[results, "representation_status"]];
candCounts = Counts[Lookup[results, "candidate_status"]];
evalCounts = Counts[Lookup[results, "candidate_eval_status"]];
ids = DeleteDuplicates[Lookup[results, "id"]];

summary = <|
  "input_path" -> inputPath,
  "ids_checked" -> Length[ids],
  "blocks_checked" -> Length[results],
  "representation_status_counts" -> repCounts,
  "candidate_status_counts" -> candCounts,
  "candidate_eval_status_counts" -> evalCounts
|>;

Export[FileNameJoin[{outDir, "wolfram_representation_validation_results.json"}], results, "RawJSON"];
Export[FileNameJoin[{outDir, "wolfram_representation_validation_summary.json"}], summary, "RawJSON"];

summaryMarkdown = StringRiffle[
  Join[
    {
      "# TZPID Wolfram Numeric/Symbolic Representation Validation",
      "",
      "This check validates the per-ID `wolfram_representation` layer generated from source-truth equations.",
      "Each representation block contains numeric atoms, symbolic tokens, and an optional best-effort Wolfram candidate expression.",
      "",
      "## Summary",
      "",
      "- IDs checked: `" <> ToString[summary["ids_checked"]] <> "`",
      "- Blocks checked: `" <> ToString[summary["blocks_checked"]] <> "`",
      "",
      "## Representation Parse Status",
      ""
    },
    KeyValueMap["- `" <> #1 <> "`: `" <> ToString[#2] <> "`" &, repCounts],
    {
      "",
      "## Candidate Parse Status",
      ""
    },
    KeyValueMap["- `" <> #1 <> "`: `" <> ToString[#2] <> "`" &, candCounts],
    {
      "",
      "## Candidate Evaluation Status",
      ""
    },
    KeyValueMap["- `" <> #1 <> "`: `" <> ToString[#2] <> "`" &, evalCounts]
  ],
  "\n"
];

Export[FileNameJoin[{outDir, "WOLFRAM_REPRESENTATION_VALIDATION_SUMMARY.md"}], summaryMarkdown, "Text"];
Print[summaryMarkdown];
