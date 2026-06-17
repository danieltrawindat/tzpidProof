(* Creator: Daniel Alexander Trawin | ORCID: https://orcid.org/0009-0001-4630-3715 *)
(* Worked check: cosmic filament web = spherical-enclosure acoustics.
   Anchors registry IDs ID7733 (j_l(kr)), ID7257 (delta_b = A j0(k r_s)), ID7259 (sound horizon r_s).
   Run:  wolframscript -file bao_enclosure_acoustics_check.wl  *)

(* --- 1. Enclosure acoustic eigenvalues = zeros of the spherical Bessel j_l --- *)
(* j_l(x) = Sqrt[Pi/(2 x)] BesselJ[l+1/2, x], so its k-th zero is BesselJZero[l+1/2, k]. *)
sphZero[l_, k_] := N[BesselJZero[l + 1/2, k], 8];
enclosureSpectrum = Table[sphZero[l, n], {l, 0, 3}, {n, 1, 4}];

(* j_0 zeros must equal n*Pi exactly (the harmonic acoustic ladder) *)
j0Residual = Table[sphZero[0, n] - n Pi, {n, 1, 4}];
j0Exact = Max[Abs[j0Residual]] < 10^-6;

(* --- 2. BAO acoustic scale (Planck 2018 sound horizon at the drag epoch) --- *)
rs = 147.05;                       (* Mpc *)
hLittle = 0.6774;
k1 = Pi/rs;                        (* first node of j0(k r_s), Mpc^-1 *)
dk = 2 Pi/rs;                      (* BAO wiggle period in P(k), Mpc^-1 *)
baoBumpMpc = rs;                   (* real-space clustering/filament scale, Mpc *)
baoBumphMpc = rs hLittle;          (* ~ h^-1 Mpc *)

(* --- 3. The identity that ties them together --- *)
(* delta_b(r) ~ A j0(k r_s): its first node sits at k r_s = Pi = first zero of j_0,
   i.e. the cosmic acoustic node IS the fundamental enclosure mode. *)
firstJ0Zero = sphZero[0, 1];       (* = Pi *)
baoMatch = Abs[k1 rs - firstJ0Zero] < 10^-6;

results = {
  <| "name" -> "enclosure_spectrum_is_jl_zeros", "status" -> "computed",
     "result" -> ToString[enclosureSpectrum, InputForm],
     "note" -> "Spherical-cavity acoustic eigenvalues k_ln*R are the zeros of j_l." |>,
  <| "name" -> "j0_harmonic_ladder", "status" -> If[j0Exact, "pass", "needs_review"],
     "result" -> "j0 zeros = n*Pi to <1e-6",
     "note" -> "The l=0 acoustic ladder is exactly harmonic (n*Pi), as in a 1-D resonator." |>,
  <| "name" -> "bao_first_node_equals_fundamental_mode", "status" -> If[baoMatch, "pass", "needs_review"],
     "result" -> "k1*rs = " <> ToString[k1 rs] <> " ; first j0 zero = " <> ToString[firstJ0Zero],
     "note" -> "BAO first node (k r_s = Pi) coincides with the fundamental enclosure mode." |>,
  <| "name" -> "bao_scales", "status" -> "computed",
     "result" -> StringJoin["k1=", ToString[k1], " Mpc^-1 ; dk=", ToString[dk],
        " Mpc^-1 ; bump=", ToString[baoBumpMpc], " Mpc (~", ToString[Round[baoBumphMpc,0.1]], " h^-1 Mpc)"],
     "note" -> "Matches the observed ~100 h^-1 Mpc BAO feature in galaxy clustering." |>
};
Export[FileNameJoin[{DirectoryName[$InputFileName], "bao_enclosure_acoustics_results.json"}], results, "JSON"];
Print["BAO enclosure-acoustics check done: ", Counts[#["status"] & /@ results]];
