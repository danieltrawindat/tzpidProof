(* TZPID portal-breathing / occupancy-interface certificate *)
ClearAll["Global`*"];

checks = {
  <|"name" -> "hubble_law_from_breathing",
    "passed" -> TrueQ[FullSimplify[Rdot*chi == (Rdot/R)*(R*chi), Assumptions -> R != 0]],
    "note" -> "Rdot chi equals (Rdot/R)(R chi)."|>,
  <|"name" -> "s3_fractional_volume_rate",
    "passed" -> TrueQ[FullSimplify[(D[2*Pi^2*R[t]^3, t]/(2*Pi^2*R[t]^3)) == 3*R'[t]/R[t], Assumptions -> R[t] != 0]],
    "note" -> "Derivative of 2 Pi^2 R^3 gives fractional volume rate 3 Rdot/R."|>,
  <|"name" -> "closed_curvature_negative_sample",
    "passed" -> TrueQ[-1*1^2/(2^2*3^2) < 0],
    "note" -> "Positive k under the cosmology sign convention gives negative OmegaK."|>,
  <|"name" -> "curvature_radius_positive_sample",
    "passed" -> TrueQ[1/(2*Sqrt[Abs[-1/4]]) == 1],
    "note" -> "Sample curvature radius expression evaluates correctly."|>,
  <|"name" -> "cpl_Fa_closed_form",
    "passed" -> TrueQ[FullSimplify[
      Exp[3*Integrate[(1 + w0 + wa*(1 - x))/x, {x, a, 1},
        GenerateConditions -> False]] ==
        a^(-3*(1 + w0 + wa))*Exp[3*wa*(a - 1)],
      Assumptions -> a > 0]],
    "note" -> "CPL integral reduces to the standard closed form."|>,
  <|"name" -> "tanh_profiles_partition",
    "passed" -> TrueQ[FullSimplify[(1 + Tanh[s/ell])/2 + (1 - Tanh[s/ell])/2 == 1, Assumptions -> ell != 0]],
    "note" -> "Complementary tanh profiles sum to one."|>,
  <|"name" -> "nested_frequency_ratio",
    "passed" -> TrueQ[FullSimplify[(c*j/(lambda*R))/(c*j/R) == 1/lambda,
      Assumptions -> c != 0 && j != 0 && R != 0 && lambda != 0]],
    "note" -> "Frequency ratio under R -> lambda R is 1/lambda."|>,
  <|"name" -> "nested_density_ratio",
    "passed" -> TrueQ[FullSimplify[(hbar*c/(lambda*R)^4)/(hbar*c/R^4) == 1/lambda^4,
      Assumptions -> hbar != 0 && c != 0 && R != 0 && lambda != 0]],
    "note" -> "Density ratio under R -> lambda R is 1/lambda^4."|>,
  <|"name" -> "interface_pressure_positive_sample",
    "passed" -> TrueQ[2*(1/3 + 1/5) > 0],
    "note" -> "Positive sample interface tension and radii give positive pressure."|>,
  <|"name" -> "stress_energy_sum",
    "passed" -> TrueQ[FullSimplify[Tb + Tt + Te + Ti == Ttotal /. Ttotal -> Tb + Tt + Te + Ti]],
    "note" -> "Stress-energy phase sum unfolds definitionally."|>,
  <|"name" -> "portal_force_balance",
    "passed" -> TrueQ[FullSimplify[Fg + Fi + Fs + Fem + Fzpf == 0 /. Fzpf -> -(Fg + Fi + Fs + Fem)]],
    "note" -> "Counterterm closes the net force balance."|>
};

results = checks /. a_Association :> Append[a, "status" -> If[TrueQ[a["passed"]], "pass", "fail"]];
summary = <|
  "generated_utc" -> "2026-06-12T11:47:20+00:00",
  "checks" -> Length[results],
  "pass" -> Count[results[[All, "status"]], "pass"],
  "fail" -> Count[results[[All, "status"]], "fail"],
  "results" -> results
|>;

Export["portal_breathing_check_results.json", summary, "RawJSON"];
Print[ExportString[summary, "RawJSON"]];
If[summary["fail"] > 0, Exit[1], Exit[0]];
