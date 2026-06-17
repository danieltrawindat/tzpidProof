ClearAll["Global`*"];
script = Part[$ScriptCommandLine, -2];
out = Part[$ScriptCommandLine, -1];
Get[script];
out = Part[$ScriptCommandLine, -1];
script = Part[$ScriptCommandLine, -2];

payload = Which[
  ValueQ[results], results,
  ValueQ[spineChecks], spineChecks,
  True, {<|"name" -> FileNameTake[script], "status" -> "no_payload", "engine" -> "WolframScript", "note" -> "Script loaded but did not define results or spineChecks."|>}
];

Export[out, payload, "RawJSON"];
Print["Wrote " <> out];
