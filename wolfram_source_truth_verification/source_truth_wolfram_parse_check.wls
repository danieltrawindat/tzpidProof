If[Length[$ScriptCommandLine] < 3,
  Print["usage: wolframscript -file source_truth_wolfram_parse_check.wls <input.json> <output-dir>"];
  Exit[2];
];

inputPath = $ScriptCommandLine[[2]];
outDir = $ScriptCommandLine[[3]];

Quiet[CreateDirectory[outDir, CreateIntermediateDirectories -> True]];

data = Import[inputPath, "RawJSON"];

ClearAll[classifyBlock];
classifyBlock[row_, block_] := Module[
  {id, title, index, source, parsed, status, inputForm, message = ""},
  id = Lookup[row, "id", ""];
  title = Lookup[row, "title", ""];
  index = Lookup[block, "block_index", Missing["block_index"]];
  source = Lookup[block, "wolfram_input", ""];
  parsed = Quiet[Check[ToExpression[source, InputForm, HoldComplete], $Failed]];
  If[parsed === $Failed,
    status = "wolfram_source_truth_parse_error";
    inputForm = "",
    status = "wolfram_source_truth_parse_pass";
    inputForm = ToString[InputForm[parsed]]
  ];
  <|
    "id" -> id,
    "title" -> title,
    "block_index" -> index,
    "wolfram_input" -> source,
    "status" -> status,
    "held_inputform" -> inputForm,
    "message" -> message
  |>
];

results = Flatten[
  Table[
    classifyBlock[row, block],
    {row, data},
    {block, Lookup[row, "blocks", {}]}
  ],
  1
];

statusCounts = Counts[Lookup[results, "status"]];
ids = DeleteDuplicates[Lookup[results, "id"]];
idsByStatus = Association[
  Table[
    status -> Length[DeleteDuplicates[Lookup[Select[results, #status == status &], "id"]]],
    {status, Keys[statusCounts]}
  ]
];

summary = <|
  "input_path" -> inputPath,
  "ids_checked" -> Length[ids],
  "blocks_checked" -> Length[results],
  "status_counts" -> statusCounts,
  "ids_by_status" -> idsByStatus
|>;

Export[FileNameJoin[{outDir, "source_truth_wolfram_parse_results.json"}], results, "RawJSON"];
Export[FileNameJoin[{outDir, "source_truth_wolfram_parse_summary.json"}], summary, "RawJSON"];

summaryMarkdown = StringRiffle[
  Join[
    {
      "# TZPID Source-Truth Wolfram Parse Check",
      "",
      "This check reads source-truth Wolfram blocks from `wolfram_form.audit.blocks[]`, accepting `wolfram_input` and reviewed `holdform_inputform` entries.",
      "Expressions are parsed under `HoldComplete`; this verifies Wolfram Language syntax without requiring domain-specific symbols to evaluate numerically.",
      "",
      "## Summary",
      "",
      "- IDs checked: `" <> ToString[summary["ids_checked"]] <> "`",
      "- Blocks checked: `" <> ToString[summary["blocks_checked"]] <> "`",
      "",
      "## Status Counts",
      ""
    },
    KeyValueMap["- `" <> #1 <> "`: `" <> ToString[#2] <> "`" &, statusCounts],
    {
      "",
      "## ID Counts By Status",
      ""
    },
    KeyValueMap["- `" <> #1 <> "`: `" <> ToString[#2] <> "`" &, idsByStatus]
  ],
  "\n"
];

Export[FileNameJoin[{outDir, "SOURCE_TRUTH_WOLFRAM_PARSE_SUMMARY.md"}], summaryMarkdown, "Text"];
Print[summaryMarkdown];
