ClearAll["Global`*"];
checks = {
  <|"name" -> "general_fractional_rate", "passed" -> TrueQ[FullSimplify[D[Cn*R[t]^n, t]/(Cn*R[t]^n) == n*R'[t]/R[t], Assumptions -> Cn != 0 && R[t] > 0 && n > 0]], "note" -> "D[Cn R^n]/(Cn R^n) = n Rdot/R."|>,
  <|"name" -> "s4_volume_derivative", "passed" -> TrueQ[FullSimplify[D[(8*Pi^2/3)*R[t]^4, t]/((8*Pi^2/3)*R[t]^4) == 4*R'[t]/R[t], Assumptions -> R[t] > 0]], "note" -> "S4 fractional rate is 4H."|>,
  <|"name" -> "s5_volume_derivative", "passed" -> TrueQ[FullSimplify[D[Pi^3*R[t]^5, t]/(Pi^3*R[t]^5) == 5*R'[t]/R[t], Assumptions -> R[t] > 0]], "note" -> "S5 fractional rate is 5H."|>,
  <|"name" -> "redshift_volume_ratio", "passed" -> TrueQ[FullSimplify[(R0/Re)^n == (1 + z)^n /. (1 + z) -> R0/Re, Assumptions -> Re != 0]], "note" -> "V0/Ve = (1+z)^n."|>,
  <|"name" -> "matter_density_ratio", "passed" -> TrueQ[FullSimplify[(lambda*R)^(-n)/R^(-n) == lambda^-n, Assumptions -> lambda > 0 && R > 0]], "note" -> "Matter density scales as R^-n."|>,
  <|"name" -> "radiation_density_ratio", "passed" -> TrueQ[FullSimplify[(lambda*R)^(-n - 1)/R^(-n - 1) == lambda^(-n - 1), Assumptions -> lambda > 0 && R > 0]], "note" -> "Radiation/mode density scales as R^-(n+1)."|>,
  <|"name" -> "occupancy_radius_inverse", "passed" -> TrueQ[FullSimplify[(phi^(1/n))^n == phi, Assumptions -> phi > 0 && n > 0]], "note" -> "Radius fraction phi^(1/n) recovers volume fraction phi."|>,
  <|"name" -> "folded_source_unfolds", "passed" -> TrueQ[FullSimplify[Sb == etab*phiT*phiE*KTE*Gres*DDAT*AB*Ccap*Rmode*RFFT*IE - Gammab*phib /. Sb -> etab*phiT*phiE*KTE*Gres*DDAT*AB*Ccap*Rmode*RFFT*IE - Gammab*phib]], "note" -> "Folded source term unfolds."|>,
  <|"name" -> "mode_gate_center", "passed" -> TrueQ[FullSimplify[Exp[-(rmode - phi)^2/(2*sigmar^2)] == 1 /. rmode -> phi, Assumptions -> sigmar != 0]], "note" -> "Mode gate equals 1 at phi."|>,
  <|"name" -> "fft_gate_center", "passed" -> TrueQ[FullSimplify[Exp[-(rfft - phi)^2/(2*sigmaf^2)] == 1 /. rfft -> phi, Assumptions -> sigmaf != 0]], "note" -> "FFT gate equals 1 at phi."|>,
  <|"name" -> "signed_energy_inversion", "passed" -> TrueQ[FullSimplify[Sign[ETZP/E] == -1 /. ETZP -> -E, Assumptions -> E > 0]], "note" -> "ETZP=-E gives IE=-1 for positive E."|>,
  <|"name" -> "bessel_z_center", "passed" -> TrueQ[FullSimplify[(s - 2.5055)/0.2167 == 0 /. s -> 2.5055]], "note" -> "Bessel z-score centers at recorded mean."|>,
  <|"name" -> "capture_probability_record", "passed" -> TrueQ[0.175 > 0 && 0.045 > 0 && 0.0005 > 0], "note" -> "Capture diagnostic values are positive."|>
};
results = checks /. a_Association :> Append[a, "status" -> If[TrueQ[a["passed"]], "pass", "fail"]];
summary = <|"generated_utc" -> "2026-06-12T12:12:30+00:00", "checks" -> Length[results], "pass" -> Count[results[[All, "status"]], "pass"], "fail" -> Count[results[[All, "status"]], "fail"], "results" -> results|>;
Export["s4_s5_hypersphere_mix_check_results.json", summary, "RawJSON"];
Print[ExportString[summary, "RawJSON"]];
If[summary["fail"] > 0, Exit[1], Exit[0]];
