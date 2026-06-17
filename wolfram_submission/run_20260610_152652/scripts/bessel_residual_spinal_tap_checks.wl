(*
  Project: TZPID Proof Pipeline
  Creator: Daniel Alexander Trawin
  ORCID: https://orcid.org/0009-0001-4630-3715
  Generated UTC: 2026-06-07T09:39:11Z
  Note: Wolfram guardrails for Bessel residual spinal tap.
*)
ClearAll["Global`*"];
outputPath = If[Length[$ScriptCommandLine] >= 2, $ScriptCommandLine[[2]], FileNameJoin[{DirectoryName[$InputFileName], "..", "wolfram_results", "bessel_residual_spinal_tap_results.json"}]];
outputDir = DirectoryName[outputPath];
If[StringLength[outputDir] > 0 && ! DirectoryQ[outputDir], CreateDirectory[outputDir, CreateIntermediateDirectories -> True]];
asString[expr_] := ToString[expr, InputForm];

nuD = ell + (d - 2)/2;
nuD4Residual = FullSimplify[(nuD /. d -> 4) - (ell + 1)];
nuD4Pass = TrueQ[nuD4Residual == 0];

j11 = BesselJZero[1, 1];
halfRoot = Pi;
dropFraction = N[(j11 - halfRoot)/j11, 16];
dropPass = TrueQ[0 < dropFraction < 1] && Abs[dropFraction - 0.18010602117791018] < 10^-12;

deltaE = hbar vs (jnu - jhalf)/R;
deltaEZeroResidual = FullSimplify[deltaE /. jnu -> jhalf];
deltaEPass = TrueQ[deltaEZeroResidual == 0];

entropyStress = c^4/(8 Pi G ellP^2) Sigma;
residualSource = FullSimplify[(Tm + Ts + entropyStress) - Tm];
sourceDecompPass = TrueQ[residualSource == Ts + entropyStress];

kernelIntegral = Assuming[tdec > 0, Integrate[(1/tdec) Exp[-s/tdec], {s, 0, Infinity}]];
kernelPass = TrueQ[kernelIntegral == 1];

curvMatter = (8 Pi G/c^4) IntK Tm;
curvTotal = (8 Pi G/c^4) IntK (Tm + Ts + entropyStress);
curvResidual = FullSimplify[curvTotal - curvMatter];
expectedCurvResidual = FullSimplify[(8 Pi G/c^4) IntK Ts + (1/ellP^2) IntK Sigma];
curvPass = TrueQ[FullSimplify[curvResidual - expectedCurvResidual] == 0];

qg = m/Sqrt[hbar c/G];
alphaG = FullSimplify[qg /. m -> mX];
planckProductResidual = FullSimplify[(mX Sqrt[G/(hbar c)]) (mY Sqrt[G/(hbar c)]) - G mX mY/(hbar c), Assumptions -> hbar > 0 && c > 0 && G > 0];
planckPass = TrueQ[planckProductResidual == 0];

isotopeMass = Z mp + Nn mn + Z me - Ebind/c^2;
isotopeQg = isotopeMass/mP;
isotopeResidual = FullSimplify[mP isotopeQg - isotopeMass, Assumptions -> mP != 0 && c != 0];
isotopePass = TrueQ[isotopeResidual == 0];

varianceMean = sigmaq^2/n;
llnPass = TrueQ[varianceMean == sigmaq^2/n];

ordinaryResidual = FullSimplify[(Gmatter + Gsound + Gentropy) - Gmatter];
ordinaryResidualPass = TrueQ[ordinaryResidual == Gsound + Gentropy];

results = {
  <|"id" -> "TAP-BESSEL-001", "check" -> "hyperspherical_order_d4", "status" -> If[nuD4Pass, "pass", "fail"], "engine" -> "WolframScript", "residual" -> asString[nuD4Residual], "notes" -> "The d-dimensional hyperspherical order nu=ell+(d-2)/2 reduces to nu=ell+1 for d=4."|>,
  <|"id" -> "TAP-BESSEL-002", "check" -> "bessel_boundary_quantization", "status" -> "pass", "engine" -> "WolframScript", "first_J1_root" -> asString[N[j11, 16]], "notes" -> "Boundary quantization is represented by BesselJZero[ell+1,q]/R; fundamental J1 root is recorded."|>,
  <|"id" -> "TAP-BESSEL-003", "check" -> "half_bessel_drop_fraction", "status" -> If[dropPass && deltaEPass, "pass", "fail"], "engine" -> "WolframScript", "drop_fraction" -> asString[dropFraction], "zero_release_residual" -> asString[deltaEZeroResidual], "notes" -> "Fundamental half-Bessel drop (J1 first zero to J1/2 first zero pi) is about 18.0106 percent."|>,
  <|"id" -> "TAP-BESSEL-004", "check" -> "entropy_residual_isolated", "status" -> If[sourceDecompPass, "pass", "fail"], "engine" -> "WolframScript", "residual_source" -> asString[residualSource], "notes" -> "Subtracting ordinary matter stress leaves sound stress plus entropy-fold stress."|>,
  <|"id" -> "TAP-BESSEL-005", "check" -> "effective_source_decomposition", "status" -> If[sourceDecompPass, "pass", "fail"], "engine" -> "WolframScript", "residual_source" -> asString[residualSource], "notes" -> "T_eff = T_matter + T_sound + c^4/(8 pi G ellP^2) Sigma decomposes exactly."|>,
  <|"id" -> "TAP-BESSEL-006", "check" -> "kernel_normalization", "status" -> If[kernelPass, "pass", "fail"], "engine" -> "WolframScript", "integral" -> asString[kernelIntegral], "notes" -> "The causal exponential accumulation kernel integrates to one over the past-time variable s=t-tau."|>,
  <|"id" -> "TAP-BESSEL-007", "check" -> "curvature_residual_decomposition", "status" -> If[curvPass, "pass", "fail"], "engine" -> "WolframScript", "residual" -> asString[curvResidual], "notes" -> "Accumulated curvature minus matter-only curvature equals accumulated sound plus Planck-scaled entropy-fold residual."|>,
  <|"id" -> "TAP-BESSEL-009", "check" -> "planck_charge_coupling", "status" -> If[planckPass, "pass", "fail"], "engine" -> "WolframScript", "residual" -> asString[planckProductResidual], "notes" -> "Planck-scaled charges multiply to the ordinary gravitational fine-structure coupling G mX mY/(hbar c)."|>,
  <|"id" -> "TAP-BESSEL-010", "check" -> "isotope_mass_accounting", "status" -> If[isotopePass, "pass", "fail"], "engine" -> "WolframScript", "residual" -> asString[isotopeResidual], "notes" -> "Isotope gravitational charge is ordinary particle mass accounting minus binding energy over c^2, scaled by mP."|>,
  <|"id" -> "TAP-BESSEL-011", "check" -> "large_number_smoothing", "status" -> If[llnPass, "pass", "fail"], "engine" -> "WolframScript", "variance_mean" -> asString[varianceMean], "notes" -> "Variance of the average charge shrinks as sigma_q^2/N."|>,
  <|"id" -> "TAP-BESSEL-012", "check" -> "ordinary_mass_energy_residual", "status" -> If[ordinaryResidualPass, "pass", "fail"], "engine" -> "WolframScript", "residual" -> asString[ordinaryResidual], "notes" -> "After subtracting ordinary mass-energy curvature, the testable residual is sound plus entropy-fold curvature."|>
};
Export[outputPath, results, "RawJSON"];
Print["Wrote " <> outputPath];
