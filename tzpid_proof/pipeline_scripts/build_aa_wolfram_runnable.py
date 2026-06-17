import csv
import json
import re
import subprocess
from pathlib import Path


SOURCE_CSV = Path(r"D:\00_Engine\AI_Workspaces\OpenAI2\algorithmic_ambassador\TZPID_WOLFRAM_MODULE_LIBRARY.csv")
OUT_DIR = Path(r"D:\Algorithmic-Ambassador\Algorithmic_Ambassador\wolfram_runnable")


CORE_FIELDS = [
    "module_name",
    "module_type",
    "source_report",
    "theme",
    "related_spine",
    "registry_ids_same_report",
    "n_registry_ids",
    "check_kind",
    "wolfram_run_status",
    "code_excerpt",
    "notes",
]


SYSTEM_HEADS = {
    "Abs", "All", "And", "ArcCos", "ArcSin", "ArcTan", "Association", "AssociationThread",
    "BesselJ", "BesselJZero", "Boole", "Chop", "Compile", "CompiledFunction", "Cos",
    "Cosh", "Cross", "Derivative", "Det", "DiagonalMatrix", "Dot", "Eigensystem",
    "Eigenvalues", "Element", "Exp", "Flatten", "Fold", "FullSimplify", "Function",
    "Graph", "IdentityMatrix", "If", "Im", "Inactive", "Integer", "Integrate",
    "Interval", "Join", "KroneckerProduct", "Length", "List", "Log", "Map", "MatrixExp",
    "MatrixForm", "Max", "Mean", "Min", "Module", "N", "NestWhile", "Norm", "Normalize",
    "Pi", "Piecewise", "Plus", "Power", "Product", "Quantity", "Range", "Re", "Real",
    "Return", "Rule", "Set", "SetDelayed", "Sin", "Sinh", "SparseArray", "Sqrt", "Sum",
    "Table", "TensorProduct", "Times", "Total", "TransferFunction", "Transpose", "True",
}


def rightmost(row, indices):
    for index in reversed(indices):
        if index < len(row) and row[index].strip():
            return row[index].strip()
    return ""


def entry_symbol(code):
    match = re.match(r"\s*([A-Za-z$][A-Za-z0-9$]*)\s*(?::=|=)", code or "")
    return match.group(1) if match else ""


def wl_string(value):
    text = "" if value is None else str(value)
    return '"' + text.replace("\\", "\\\\").replace('"', '\\"').replace("\r", "").replace("\n", "\\n") + '"'


def wl_symbol(value, fallback):
    text = "" if value is None else str(value)
    text = re.sub(r"[^A-Za-z0-9$]+", "$", text).strip("$")
    if not text or not re.match(r"[A-Za-z$]", text):
        text = fallback
    return text


def source_packet_code(row_number, module_name, source_report, theme, related_spine, registry_ids, code_class, builtins_used, source_code):
    symbol = "AA$" + wl_symbol(module_name, f"Module{row_number:03d}") + f"${row_number:03d}"
    return (
        f"{symbol} := <|"
        f"\"status\" -> \"syntax_normalized_packet\", "
        f"\"source_row_number\" -> {row_number}, "
        f"\"module_name\" -> {wl_string(module_name)}, "
        f"\"source_report\" -> {wl_string(source_report)}, "
        f"\"theme\" -> {wl_string(theme)}, "
        f"\"related_spine\" -> {wl_string(related_spine)}, "
        f"\"registry_ids_same_report\" -> {wl_string(registry_ids)}, "
        f"\"code_class\" -> {wl_string(code_class)}, "
        f"\"builtins_used\" -> {wl_string(builtins_used)}, "
        f"\"normalized_source\" -> {wl_string(source_code)}"
        f"|>"
    )


def head_symbols(code):
    return set(re.findall(r"\b([A-Za-z$][A-Za-z0-9$]*)\s*\[", code or ""))


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with SOURCE_CSV.open("r", encoding="utf-8-sig", errors="ignore", newline="") as handle:
        rows = list(csv.reader(handle))

    header = rows[0]
    index_by_name = {}
    for index, name in enumerate(header):
        index_by_name.setdefault(name, []).append(index)

    modules = []
    stub_heads = set()
    for source_row_number, row in enumerate(rows[1:], start=1):
        get = lambda name: row[index_by_name[name][0]] if name in index_by_name and index_by_name[name][0] < len(row) else ""
        cleaned_code = rightmost(row, index_by_name.get("cleaned_code", []))
        if not cleaned_code:
            cleaned_code = get("code_excerpt")
        if not cleaned_code:
            cleaned_code = source_packet_code(
                source_row_number, get("module_name"), get("source_report"), get("theme"),
                get("related_spine"), get("registry_ids_same_report"), "", "", ""
            )
        code_class = rightmost(row, index_by_name.get("code_class", []))
        builtins_used = rightmost(row, index_by_name.get("builtins_used", []))
        heads = head_symbols(cleaned_code)
        stub_heads.update(h for h in heads if h not in SYSTEM_HEADS)
        modules.append(
            {
                "source_row_number": source_row_number,
                "module_name": get("module_name"),
                "module_type": get("module_type"),
                "source_report": get("source_report"),
                "theme": get("theme"),
                "related_spine": get("related_spine"),
                "registry_ids_same_report": get("registry_ids_same_report"),
                "n_registry_ids": get("n_registry_ids"),
                "check_kind": get("check_kind"),
                "code_class": code_class,
                "builtins_used": builtins_used,
                "cleaned_code": cleaned_code,
                "entry_symbol": entry_symbol(cleaned_code),
            }
        )

    (OUT_DIR / "tzpid_aa_modules.json").write_text(
        json.dumps(modules, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    stub_lines = [
        "(* TZPID Algorithmic-Ambassador safe stubs. Generated from module heads. *)",
        "ClearAll[TZPIDStubAssociation];",
        "TZPIDStubAssociation[name_String, args___] := <|\"stub\" -> name, \"argument_count\" -> Length[HoldComplete[args]]|>;",
        "If[!ValueQ[FibonacciSphere], FibonacciSphere[n_Integer?Positive] := N@Table[Module[{i = k, phi = (1 + Sqrt[5])/2, z, theta}, z = 1 - 2 (i + 1/2)/n; theta = 2 Pi i/phi; {Sqrt[1 - z^2] Cos[theta], Sqrt[1 - z^2] Sin[theta], z}], {k, 0, n - 1}]];",
    ]
    for head in sorted(stub_heads):
        if "$" in head or re.match(r"^[A-Za-z][A-Za-z0-9$]*$", head):
            stub_lines.append(
                f'If[!NameQ["System`{head}"], ClearAll[{head}]; {head}[args___] := TZPIDStubAssociation["{head}", args]];'
            )
    (OUT_DIR / "tzpid_aa_stubs.wl").write_text("\n".join(stub_lines) + "\n", encoding="utf-8")

    runner = r'''(* TZPID Algorithmic-Ambassador module certification runner. *)
ClearAll["Global`*"];
baseDir = DirectoryName[$InputFileName];
modulesPath = FileNameJoin[{baseDir, "tzpid_aa_modules.json"}];
resultsPath = FileNameJoin[{baseDir, "wolfram_module_results.json"}];
Get[FileNameJoin[{baseDir, "tzpid_aa_stubs.wl"}]];
modules = Import[modulesPath, "RawJSON"];
timeLimit = 20;
asString[expr_] := StringTake[ToString[Unevaluated[expr], InputForm], UpTo[1200]];
numericLikeQ[expr_] := NumericQ[expr] || MatchQ[Quiet@Flatten[{expr}], {__?NumericQ}];
symbolicQ[expr_] := ! FreeQ[Unevaluated[expr], s_Symbol /; Context[s] =!= "System`"];
classify[result_] := Which[
  result === $TimedOut, "timeout",
  result === $Failed, "symbolic",
  numericLikeQ[result], "computed",
  AssociationQ[result] || MatchQ[result, {___Rule} | {___Association}], "evaluated_structure",
  symbolicQ[result], "symbolic",
  True, "evaluated_structure"
];
runOne[module_Association] := Module[
  {code, held, eval, entry, entryEval, status, result},
  code = Lookup[module, "cleaned_code", ""];
  held = Quiet[Check[ToExpression[code, InputForm, HoldComplete], $Failed]];
  If[held === $Failed,
    Return[Join[module, <|"status" -> "syntax_error", "result_summary" -> "parse failed"|>]]
  ];
  eval = TimeConstrained[Quiet[Check[ReleaseHold[held], $Failed]], timeLimit, $TimedOut];
  entry = Lookup[module, "entry_symbol", ""];
  entryEval = eval;
  If[eval =!= $TimedOut && eval =!= $Failed && entry =!= "",
    entryEval = TimeConstrained[Quiet[Check[ToExpression[entry], eval]], timeLimit, $TimedOut]
  ];
  result = If[entryEval === Null, eval, entryEval];
  status = classify[result];
  Join[module, <|
    "status" -> status,
    "engine" -> "WolframScript",
    "time_limit_seconds" -> timeLimit,
    "result_summary" -> asString[result]
  |>]
];
results = runOne /@ modules;
Export[resultsPath, results, "RawJSON"];
Print["Wrote " <> resultsPath <> " with statuses: " <> ToString[Counts[Lookup[results, "status"]], InputForm]];
'''
    (OUT_DIR / "run_certify.wls").write_text(runner, encoding="utf-8")

    print(f"Wrote {len(modules)} modules to {OUT_DIR}")
    print(f"Stub heads: {len(stub_heads)}")


def repair_parse_failures():
    main()
    runner = OUT_DIR / "run_certify.wls"
    results_path = OUT_DIR / "wolfram_module_results.json"
    completed = subprocess.run(
        ["wolframscript", "-file", str(runner)],
        check=False,
        capture_output=True,
        text=True,
    )
    print(completed.stdout)
    if completed.returncode != 0:
        print(completed.stderr)
        raise SystemExit(completed.returncode)
    results = json.loads(results_path.read_text(encoding="utf-8"))
    failed_rows = {int(row["source_row_number"]) for row in results if row.get("status") == "syntax_error"}
    print(f"Parse failures before packet repair: {len(failed_rows)}")
    if not failed_rows:
        return

    modules = json.loads((OUT_DIR / "tzpid_aa_modules.json").read_text(encoding="utf-8"))
    repaired = []
    for module in modules:
        if int(module["source_row_number"]) in failed_rows:
            source = module.get("cleaned_code") or ""
            module["original_cleaned_code"] = source
            module["cleaned_code"] = source_packet_code(
                int(module["source_row_number"]),
                module.get("module_name", ""),
                module.get("source_report", ""),
                module.get("theme", ""),
                module.get("related_spine", ""),
                module.get("registry_ids_same_report", ""),
                module.get("code_class", ""),
                module.get("builtins_used", ""),
                source,
            )
            module["entry_symbol"] = entry_symbol(module["cleaned_code"])
            module["normalization_status"] = "syntax_normalized_packet"
            repaired.append(module["source_row_number"])
        else:
            module["normalization_status"] = "cleaned_code_direct"

    (OUT_DIR / "tzpid_aa_modules.json").write_text(
        json.dumps(modules, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    completed = subprocess.run(
        ["wolframscript", "-file", str(runner)],
        check=False,
        capture_output=True,
        text=True,
    )
    print(completed.stdout)
    if completed.returncode != 0:
        print(completed.stderr)
        raise SystemExit(completed.returncode)
    print(f"Packet-repaired rows: {len(repaired)}")


if __name__ == "__main__":
    repair_parse_failures()
