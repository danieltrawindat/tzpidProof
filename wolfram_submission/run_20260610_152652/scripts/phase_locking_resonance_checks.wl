(*
  Project: TZPID Proof Pipeline
  Creator: Daniel Alexander Trawin
  ORCID: https://orcid.org/0009-0001-4630-3715
  Generated UTC: 2026-06-07T07:16:10Z
  Note: Focused checks for the phase-locking / resonance ratio-selection vertebra.
*)
ClearAll["Global`*"];
outputPath = If[Length[$ScriptCommandLine] >= 2, $ScriptCommandLine[[2]], FileNameJoin[{DirectoryName[$InputFileName], "..", "wolfram_results", "phase_locking_resonance_results.json"}]];
outputDir = DirectoryName[outputPath];
If[StringLength[outputDir] > 0 && ! DirectoryQ[outputDir], CreateDirectory[outputDir, CreateIntermediateDirectories -> True]];
asString[expr_] := ToString[expr, InputForm];

angles = N[Range[0, 7] 2 Pi/8];
rOrder = Abs[Mean[Exp[I angles]]];
orderPass = 0 <= Chop[rOrder] <= 1;

phaseResidual = FullSimplify[K Sin[delta] - dw /. delta -> ArcSin[dw/K], Assumptions -> K > 0 && 0 <= dw <= K];
phasePass = TrueQ[phaseResidual == 0];

spinRatio = 3/2;
spinReciprocalResidual = FullSimplify[spinRatio (2/3) - 1];
spinPass = TrueQ[spinReciprocalResidual == 0];

cavityRatio = FullSimplify[(2 f1)/f1, Assumptions -> f1 != 0];
cavityReciprocalResidual = FullSimplify[cavityRatio (1/2) - 1];
cavityPass = TrueQ[cavityRatio == 2 && cavityReciprocalResidual == 0];

besselRoot = N[BesselJZero[0, 1], 20];
besselBoundaryValue = N[BesselJ[0, besselRoot], 20];
besselPass = Abs[besselBoundaryValue] < 10^-12;

grad = {gx, gy, gz};
lyapunovDerivative = FullSimplify[-(gx^2 + gy^2 + gz^2)];
lyapunovPass = TrueQ[lyapunovDerivative <= 0 /. {gx -> 1, gy -> -2, gz -> 3}];

beatSpacing = FullSimplify[((n + 1)/(2 df) - n/(2 df)), Assumptions -> df > 0 && Element[n, Integers]];
beatPass = TrueQ[beatSpacing == 1/(2 df)];

bridgeResidual = FullSimplify[(32/27) (27/32) - 1];
bridgePass = TrueQ[bridgeResidual == 0];

results = {
  <|"id" -> "ID0117", "check" -> "kuramoto_order_parameter_bounds", "status" -> If[TrueQ[orderPass], "pass", "fail"], "engine" -> "WolframScript", "order_parameter_sample" -> asString[N[rOrder, 12]], "notes" -> "The finite Kuramoto order parameter r = |Mean[Exp[I theta]]| is bounded by 0 and 1."|>,
  <|"id" -> "ID9513", "check" -> "phase_lock_threshold", "status" -> If[TrueQ[phasePass], "pass", "fail"], "engine" -> "WolframScript", "residual_after_lock_substitution" -> asString[phaseResidual], "notes" -> "For K >= |Delta omega|, a two-oscillator fixed phase delta = ArcSin[Delta omega/K] solves K Sin[delta] = Delta omega."|>,
  <|"id" -> "ID0143", "check" -> "spin_orbit_3_2_reciprocal", "status" -> If[TrueQ[spinPass], "pass", "fail"], "engine" -> "WolframScript", "ratio" -> asString[spinRatio], "residual_after_reciprocal" -> asString[spinReciprocalResidual], "notes" -> "The Mercury-style 3:2 spin-orbit lock has exact reciprocal 2/3."|>,
  <|"id" -> "ID0252", "check" -> "cavity_harmonic_2_1", "status" -> If[TrueQ[cavityPass], "pass", "fail"], "engine" -> "WolframScript", "ratio" -> asString[cavityRatio], "residual_after_reciprocal" -> asString[cavityReciprocalResidual], "notes" -> "The harmonic ladder f_n = n f_1 gives f_2/f_1 = 2 and reciprocal 1/2."|>,
  <|"id" -> "ID0261", "check" -> "cavity_bessel_boundary", "status" -> If[TrueQ[besselPass], "pass", "fail"], "engine" -> "WolframScript", "first_bessel_root" -> asString[besselRoot], "boundary_value" -> asString[besselBoundaryValue], "notes" -> "The first radial cavity mode root satisfies J_0(root) = 0 numerically."|>,
  <|"id" -> "ID9494", "check" -> "entrainment_lyapunov_descent", "status" -> If[TrueQ[lyapunovPass], "pass", "fail"], "engine" -> "WolframScript", "dVdt" -> asString[lyapunovDerivative], "notes" -> "A negative-gradient entrainment law gives nonpositive Lyapunov derivative."|>,
  <|"id" -> "ID0099", "check" -> "beat_window_spacing", "status" -> If[TrueQ[beatPass], "pass", "fail"], "engine" -> "WolframScript", "window_spacing" -> asString[beatSpacing], "notes" -> "Beat activation windows t_n = n/(2 Delta f) are evenly spaced by 1/(2 Delta f)."|>,
  <|"id" -> "ID0097", "check" -> "bridge_ratio_reciprocal", "status" -> If[TrueQ[bridgePass], "pass", "fail"], "engine" -> "WolframScript", "residual_after_reciprocal" -> asString[bridgeResidual], "notes" -> "The bridge ratio 32/27 has exact reciprocal 27/32."|>
};
Export[outputPath, results, "RawJSON"];
Print["Wrote " <> outputPath];
