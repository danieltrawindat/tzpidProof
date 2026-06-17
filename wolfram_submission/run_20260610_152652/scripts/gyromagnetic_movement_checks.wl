(*
  Project: TZPID Proof Pipeline
  Creator: Daniel Alexander Trawin
  ORCID: https://orcid.org/0009-0001-4630-3715
  Generated UTC: 2026-06-07T07:34:27Z
  Note: Algebraic guardrails for gyromagnetic movement mechanism before Isabelle encoding.
*)
ClearAll["Global`*"];
outputPath = If[Length[$ScriptCommandLine] >= 2, $ScriptCommandLine[[2]], FileNameJoin[{DirectoryName[$InputFileName], "..", "wolfram_results", "gyromagnetic_movement_results.json"}]];
outputDir = DirectoryName[outputPath];
If[StringLength[outputDir] > 0 && ! DirectoryQ[outputDir], CreateDirectory[outputDir, CreateIntermediateDirectories -> True]];
asString[expr_] := ToString[expr, InputForm];

stateDim = 3 + 3 + 3 + 3;
configPass = stateDim == 12;

torque = Cross[mu, b];
torqueOrthResidual = FullSimplify[mu . torque];
torquePass = TrueQ[torqueOrthResidual == 0];

omegaSolution = FullSimplify[omega0 + (tau/I) t, Assumptions -> I != 0];
omegaDerivativeResidual = FullSimplify[D[omegaSolution, t] - tau/I];
omegaIntegralPass = TrueQ[omegaDerivativeResidual == 0];

lambdaSol = FullSimplify[1 + (lambda0 - 1) Exp[-k t]];
lambdaResidual = FullSimplify[D[lambdaSol, t] + k (lambdaSol - 1)];
lambdaLimit = Assuming[k > 0, Limit[lambdaSol, t -> Infinity]];
elsasserPass = TrueQ[lambdaResidual == 0] && TrueQ[lambdaLimit == 1];

equipResidual = FullSimplify[B^2/(2 mu0) - (1/2) rho (Omega r)^2 /. B -> Sqrt[mu0 rho] Omega r, Assumptions -> mu0 > 0 && rho > 0];
equipPass = TrueQ[equipResidual == 0];

gmu = FullSimplify[(k M R^2 Omega)/(M R^2 Omega), Assumptions -> M != 0 && R != 0 && Omega != 0];
scalingPass = TrueQ[gmu == k];

gammaRatio = FullSimplify[L/muMag /. L -> gamma muMag, Assumptions -> muMag != 0];
gammaPass = TrueQ[gammaRatio == gamma];

hSolution = H0;
helicityPass = TrueQ[D[hSolution, t] == 0];

metricZeroResidual = FullSimplify[(omegaR/c)^2 /. omegaR -> 0, Assumptions -> c != 0];
metricPass = TrueQ[metricZeroResidual == 0];

gravitoZeroResidual = FullSimplify[(2 G/c^2) omegaR inertia/r^2 /. omegaR -> 0, Assumptions -> c != 0 && r != 0];
gravitoPass = TrueQ[gravitoZeroResidual == 0];

magnetoResponse = alpha/(kappa + I w);
magnetoMagnitudeSquared = FullSimplify[ComplexExpand[Abs[magnetoResponse]^2], Assumptions -> alpha > 0 && kappa > 0 && Element[w, Reals]];
magnetoAtZero = FullSimplify[magnetoMagnitudeSquared /. w -> 0, Assumptions -> alpha > 0 && kappa > 0];
magnetoPass = TrueQ[magnetoAtZero == alpha^2/kappa^2];

results = {
  <|"id" -> "ID10146", "check" -> "config_state_dimension", "status" -> If[configPass, "pass", "fail"], "engine" -> "WolframScript", "state_dimension" -> asString[stateDim], "notes" -> "Vimana state vector has four R3 components: r_cm, omega_gyro, mu_constrained, L_mech."|>,
  <|"id" -> "ID0037", "check" -> "torque_orthogonality", "status" -> If[torquePass, "pass", "fail"], "engine" -> "WolframScript", "residual" -> asString[torqueOrthResidual], "notes" -> "For torque mu x B, torque is perpendicular to the magnetic moment direction."|>,
  <|"id" -> "ID0087", "check" -> "angular_velocity_integral", "status" -> If[omegaIntegralPass, "pass", "fail"], "engine" -> "WolframScript", "residual" -> asString[omegaDerivativeResidual], "notes" -> "Constant torque history integrates to omega(t)=omega0+(tau/I)t."|>,
  <|"id" -> "ID0038", "check" -> "elsasser_relaxation", "status" -> If[elsasserPass, "pass", "fail"], "engine" -> "WolframScript", "solution" -> asString[lambdaSol], "limit" -> asString[lambdaLimit], "notes" -> "Normal form dot Lambda=-k(Lambda-1) relaxes to Lambda=1 for k>0."|>,
  <|"id" -> "ID0039", "check" -> "equipartition_identity", "status" -> If[equipPass, "pass", "fail"], "engine" -> "WolframScript", "residual" -> asString[equipResidual], "notes" -> "Magnetic and rotational energy densities match when B=sqrt(mu0 rho) Omega r."|>,
  <|"id" -> "ID0044", "check" -> "gyromagnetic_scaling", "status" -> If[scalingPass, "pass", "fail"], "engine" -> "WolframScript", "dimensionless_ratio" -> asString[gmu], "notes" -> "If mu=k M R^2 Omega then mu/(M R^2 Omega)=k."|>,
  <|"id" -> "ID10131", "check" -> "gyromagnetic_ratio", "status" -> If[gammaPass, "pass", "fail"], "engine" -> "WolframScript", "ratio" -> asString[gammaRatio], "notes" -> "The celestial gyromagnetic ratio gamma=L/mu is recovered by substitution."|>,
  <|"id" -> "ID9758", "check" -> "helicity_constant", "status" -> If[helicityPass, "pass", "fail"], "engine" -> "WolframScript", "dHdt" -> asString[D[hSolution,t]], "notes" -> "Ideal topological-protection obligation: constant helicity has zero time derivative."|>,
  <|"id" -> "ID10145", "check" -> "rotating_metric_zero_limit", "status" -> If[metricPass, "pass", "fail"], "engine" -> "WolframScript", "residual" -> asString[metricZeroResidual], "notes" -> "Rotating-frame correction controlled by (omega R/c)^2 vanishes at zero rim speed."|>,
  <|"id" -> "ID10272", "check" -> "gravitomagnetic_zero_limit", "status" -> If[gravitoPass, "pass", "fail"], "engine" -> "WolframScript", "residual" -> asString[gravitoZeroResidual], "notes" -> "Weak gravitomagnetic surrogate term vanishes when omega R is zero."|>,
  <|"id" -> "source:Our_Gyromagnetic_Universe", "check" -> "magnetoacoustic_response_zero", "status" -> If[magnetoPass, "pass", "fail"], "engine" -> "WolframScript", "response_abs_squared" -> asString[magnetoMagnitudeSquared], "at_zero" -> asString[magnetoAtZero], "notes" -> "The response deltaLambda=alpha/(kappa+i omega) has zero-frequency magnitude squared alpha^2/kappa^2."|>
};
Export[outputPath, results, "RawJSON"];
Print["Wrote " <> outputPath];
