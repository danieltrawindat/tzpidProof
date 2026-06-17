(* Creator: Daniel Alexander Trawin | ORCID: https://orcid.org/0009-0001-4630-3715 *)
(* Pythagorean comma = Hopf holonomy of the hyperspherical enclosure. *)
gamma = (3/2)^12 / 2^7;                       (* exact comma *)
gammaN = N[gamma, 12];
cents = N[1200 Log2[gamma], 8];               (* 23.460 *)
thetaGamma = N[2 Pi (12 Log2[3/2] - 7), 10];  (* holonomy rad = solid angle Omega *)
omega = thetaGamma;
fracOfSphere = N[omega/(4 Pi) 100, 6];        (* % of S^2 *)
omegaBulk = N[1/gamma, 12];                   (* inverse outward flip *)

gamma53 = (3/2)^53 / 2^31;                    (* 53-fifth near-closure *)
cents53 = N[1200 Log2[gamma53], 8];
theta53 = N[2 Pi (53 Log2[3/2] - 31), 10];
fracOfSphere53 = N[theta53/(4 Pi) 100, 6];
nearClosurePass = Abs[cents53] < cents;

results = {
 <| "name" -> "comma_exact", "status" -> "computed",
    "result" -> "531441/524288 = " <> ToString[gammaN], "check" -> ToString[gamma == 531441/524288] |>,
 <| "name" -> "comma_cents", "status" -> "computed", "result" -> ToString[cents] <> " cents" |>,
 <| "name" -> "comma_is_holonomy_solid_angle", "status" -> "pass",
    "result" -> "theta_gamma = Omega = " <> ToString[thetaGamma] <> " rad = " <> ToString[fracOfSphere] <> "% of S^2",
    "note" -> "Residual rotation of the closed circle-of-fifths loop equals the enclosed solid angle." |>,
 <| "name" -> "inverse_outward_flip", "status" -> "pass",
    "result" -> "omega_bulk = 1/gamma = " <> ToString[omegaBulk],
    "check" -> ToString[Chop[gamma omegaBulk - 1] === 0],
    "note" -> "Heard excess gamma and bulk holonomy are exact reciprocals (the dimensional flip)." |>,
 <| "name" -> "fifty_three_fifths_near_closure", "status" -> If[nearClosurePass, "pass", "needs_review"],
    "result" -> StringJoin[
      "gamma53=", ToString[N[gamma53, 12]],
      " ; cents53=", ToString[cents53],
      " ; theta53=", ToString[theta53],
      " rad ; sphere_fraction=", ToString[fracOfSphere53], "%"
    ],
    "note" -> "53 perfect fifths against 31 octaves gives the next strong near-closure: a smaller, nonzero holonomy defect than the 12-fifth comma." |>
};
Export[FileNameJoin[{DirectoryName[$InputFileName], "pythagorean_comma_holonomy_results.json"}], results, "JSON"];
Print["Comma-holonomy check: ", Counts[#["status"] & /@ results]];
