results = <|
  "generated_utc" -> "2026-06-16T15:56:19+00:00",
  "registered_equations" -> 103,
  "checks" -> {
    <|"name" -> "sixty_efolds", "passed" -> (Abs[N[Exp[60]] - 1.1420073898156842*10^26] < 10^12)|>,
    <|"name" -> "early_sound_speed", "passed" -> (Abs[N[1/Sqrt[3]] - 0.5773502691896258] < 10^-12)|>,
    <|"name" -> "s4_s3_ratio", "passed" -> (Abs[N[Sqrt[4/3]] - 1.1547005383792515] < 10^-12)|>,
    <|"name" -> "s5_s3_ratio", "passed" -> (Abs[N[Sqrt[5/3]] - 1.2909944487358056] < 10^-12)|>,
    <|"name" -> "s5_s4_ratio", "passed" -> (Abs[N[Sqrt[5/4]] - 1.118033988749895] < 10^-12)|>
  }
|>;
results = Append[results, "pass" -> Count[results["checks"], _?(#passed === True &)]];
Export[FileNameJoin[{Directory[], "spartan_standing_wave_check_results.json"}], results, "JSON"];
Print[ExportString[results, "JSON"]];
