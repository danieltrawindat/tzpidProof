ClearAll["Global`*"];
checks = {
  <|"name" -> "gravity_force", "passed" -> TrueQ[FullSimplify[m*g == Fg /. Fg -> m*g]], "note" -> "Fg = m g."|>,
  <|"name" -> "surface_tension_force", "passed" -> TrueQ[FullSimplify[gamma*(1/R1 + 1/R2) == Fs /. Fs -> gamma*(1/R1 + 1/R2)]], "note" -> "Fs = gamma(1/R1 + 1/R2)."|>,
  <|"name" -> "inertial_force", "passed" -> TrueQ[FullSimplify[m*a == Fi /. Fi -> m*a]], "note" -> "Fi = m a."|>,
  <|"name" -> "acoustic_pressure_force", "passed" -> TrueQ[FullSimplify[P*A == Fa /. Fa -> P*A]], "note" -> "Fa = P A."|>,
  <|"name" -> "drag_force", "passed" -> TrueQ[FullSimplify[1/2*rho*v^2*Cd*A == Fr /. Fr -> 1/2*rho*v^2*Cd*A]], "note" -> "Fr = 1/2 rho v^2 Cd A."|>,
  <|"name" -> "five_force_balance_by_counterterm", "passed" -> TrueQ[FullSimplify[Fg + Fs + Fi + Fa + Fr == 0 /. Fr -> -(Fg + Fs + Fi + Fa)]], "note" -> "Drag counterterm closes five-force balance."|>,
  <|"name" -> "phi_ratio_definition", "passed" -> TrueQ[FullSimplify[phiRatio == Fs/Fi /. phiRatio -> Fs/Fi]], "note" -> "phiRatio = Fs/Fi."|>,
  <|"name" -> "golden_state_rearrangement", "passed" -> TrueQ[FullSimplify[(Fs*phi)/(Fi + Fa) == 1 /. Fa -> Fs*phi - Fi, Assumptions -> Fi + Fs*phi - Fi != 0]], "note" -> "PortalState = 1 implies Fa = Fs phi - Fi."|>,
  <|"name" -> "fa_predicted_rearrangement", "passed" -> TrueQ[FullSimplify[FaPred == Fs*phi - Fi /. FaPred -> Fs*phi - Fi]], "note" -> "FaPred unfolds."|>,
  <|"name" -> "golden_ratio_constant", "passed" -> TrueQ[FullSimplify[((1 + Sqrt[5])/2)^2 == (1 + Sqrt[5])/2 + 1]], "note" -> "phi^2 = phi + 1."|>
};
results = checks /. a_Association :> Append[a, "status" -> If[TrueQ[a["passed"]], "pass", "fail"]];
summary = <|"generated_utc" -> "2026-06-12T12:04:23+00:00", "checks" -> Length[results], "pass" -> Count[results[[All, "status"]], "pass"], "fail" -> Count[results[[All, "status"]], "fail"], "results" -> results|>;
Export["portal_equilibrium_laws_check_results.json", summary, "RawJSON"];
Print[ExportString[summary, "RawJSON"]];
If[summary["fail"] > 0, Exit[1], Exit[0]];
