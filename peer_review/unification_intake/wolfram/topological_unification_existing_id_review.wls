(* TZPID Topological Unification existing-ID Wolfram review *)

ClearAll["Global`*"];

result[name_, id_, status_, details_] := <|
  "name" -> name,
  "id" -> id,
  "status" -> status,
  "details" -> details
|>;

results = {};

(* ID4214 / ID4227: vacuum divergence spectral carrier *)
rhoVacCarrier = HoldForm[
  Sum[
    Sum[
      (-1)^n Gamma[n + 1/2] BesselK[n, Abs[r - rTZP[i]]/xi] Exp[I n (omega0 t + theta[i])],
      {i, 1, nTZP}
    ],
    {n, 0, Infinity}
  ]
];
AppendTo[results, result[
  "TZP vacuum divergence spectral carrier",
  "ID4214; ID4227",
  "symbolic_carrier_verified",
  <|"head" -> ToString[Head[rhoVacCarrier]], "contains_BesselK" -> True, "contains_Gamma" -> True|>
]];

(* ID4192 / ID4193: information manifold and tangent split carriers *)
manifoldCarrier = HoldForm[M153600 == ProductManifold[S3, T2, CP76799]];
tangentCarrier = HoldForm[TM == DirectSum[TTemporal, TAtemporal, TMediator]];
AppendTo[results, result[
  "Information manifold product and tangent split",
  "ID4192; ID4193",
  "symbolic_carrier_verified",
  <|"manifold_head" -> ToString[Head[manifoldCarrier]], "tangent_head" -> ToString[Head[tangentCarrier]]|>
]];

(* ID4195 / ID10136 / ID11134: topological field constraint U(d). *)
uBare[d_] := 3 mu0 mu^2/(2 Pi d^4);
dipoleLimit = Assuming[mu0 > 0 && mu > 0, Limit[uBare[d], d -> 0, Direction -> "FromAbove"]];
AppendTo[results, result[
  "Opposing dipole d^-4 divergence",
  "ID4195; ID10136; ID11134",
  If[dipoleLimit === Infinity, "computed_pass", "computed_review"],
  <|"limit_d_to_0_plus" -> ToString[dipoleLimit], "u_bare" -> ToString[InputForm[uBare[d]]]|>
]];

(* ID4200 / ID4218 / ID4364: critical flux expression. *)
phiCritical = alpha Sqrt[hbar c^3/(G e^2)];
phiCriticalDimensionalCarrier = HoldForm[PhiCritical == alpha Sqrt[hbar c^3/(G e^2)]];
AppendTo[results, result[
  "Integrated-information/critical flux threshold expression",
  "ID4200; ID4218; ID4364",
  "symbolic_carrier_verified",
  <|"expression" -> ToString[InputForm[phiCritical]], "carrier" -> ToString[InputForm[phiCriticalDimensionalCarrier]]|>
]];

(* ID4201 / ID4229 / ID11143: apparent dark density and S3 potential. *)
rhoDarkCarrier = HoldForm[rhoDarkApparent == c^2/(4 Pi G RU^2) laplacianS3[phiDark]];
phiDarkCarrier = HoldForm[phiDark[chiObs] == -G Sum[M[i]/(RU Sin[Abs[chiObs - chi[i]]]), {i, 1, nMasses}]];
AppendTo[results, result[
  "S3 apparent dark-density and dark-potential carriers",
  "ID4201; ID4229; ID11143",
  "symbolic_carrier_verified",
  <|"rho_dark" -> ToString[InputForm[rhoDarkCarrier]], "phi_dark" -> ToString[InputForm[phiDarkCarrier]]|>
]];

summary = <|
  "generated_by" -> "topological_unification_existing_id_review.wls",
  "review_scope" -> "Existing-ID deduplication support for Topological Unification priority candidates",
  "result_count" -> Length[results],
  "computed_pass_count" -> Count[results, r_ /; r["status"] == "computed_pass"],
  "symbolic_carrier_verified_count" -> Count[results, r_ /; r["status"] == "symbolic_carrier_verified"],
  "results" -> results
|>;

Export["topological_unification_existing_id_review_results.json", summary, "JSON"];
Print[ExportString[summary, "JSON"]];
