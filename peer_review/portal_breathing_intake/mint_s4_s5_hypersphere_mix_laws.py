import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from uuid import NAMESPACE_URL, uuid5


ROOT = Path(r"D:\TZPIDProof")
MASTER = ROOT / "TZPID_ALL_IDS_CANONICAL_EQUATION_MASTER_with_export.csv"
MASTER_MD = ROOT / "TZPID_ALL_IDS_CANONICAL_EQUATION_MASTER_with_export.md"
DICTIONARY = ROOT / "TZPID_DICTIONARY.csv"
ENCYCLOPEDIA = ROOT / "TZPID_ENCYCLOPEDIA.md"
TZP_ID = ROOT / "tzp_id"
OUT = ROOT / "peer_review" / "portal_breathing_intake"
ISABELLE_DIR = ROOT / "tzpid_proof" / "isabelle_tzpid"
ROOT_FILE = ISABELLE_DIR / "ROOT"

CREATOR = "Daniel Alexander Trawin"
ORCID = "https://orcid.org/0009-0001-4630-3715"
SOURCE = r"D:\TZPIDProof\ll restart from the original hypersphere.txt"


ENTRIES = [
    ("General Sn Hypersphere Hypervolume",
     "The n-sphere hypervolume carrier is the standard surface measure of S^n with radius R.",
     r"V_{S^{n}}(R)=\frac{2\pi^{(n+1)/2}}{\Gamma((n+1)/2)}R^{n}",
     "S4/S5 hypersphere rewrite extraction", "V, n, R, Gamma", "Definition", "HigherDimensional_Volume",
     "General Sn Hypersphere Hypervolume — VSn is 2 pi^((n+1)/2) over Gamma((n+1)/2) times R^n.",
     "This is the dimension-generic carrier for extending the breathing enclosure from S3 into S4 and S5.",
     "Vn == Cn*R^n"),
    ("General Sn Fractional Breathing Rate",
     "For an n-sphere whose radius breathes with H=Rdot/R, the fractional hypervolume rate is nH.",
     r"\frac{\dot V_{S^{n}}}{V_{S^{n}}}=n\frac{\dot R}{R}=nH",
     "Differentiated n-sphere hypervolume", "V, Vdot, n, R, Rdot, H", "Theorem", "HigherDimensional_Volume",
     "General Sn Fractional Breathing Rate — Vdot over V equals n times H.",
     "This is the central dimension-upgrade law: S4 breathes at 4H in hypervolume and S5 at 5H.",
     "VdotOverV == n*Rdot/R"),
    ("S4 Hypervolume Carrier",
     "For a 4-sphere of radius R, the hypervolume is eight pi squared over three times R to the fourth.",
     r"V_{S^{4}}=\frac{8\pi^{2}}{3}R^{4}",
     "S4 explicit volume extraction", "V_S4, R", "Definition", "HigherDimensional_Volume",
     "S4 Hypervolume Carrier — VS4 equals eight pi squared R^4 over three.",
     "This gives the explicit S4 volume carrier used by the higher-dimensional breathing interpretation.",
     "VS4 == (8*Pi^2/3)*R^4"),
    ("S4 Fractional Breathing Rate",
     "The S4 hypervolume fractional breathing rate is four times the Hubble breathing rate.",
     r"\frac{\dot V_{S^{4}}}{V_{S^{4}}}=4H",
     "S4 differentiated volume extraction", "V_S4, H", "Theorem", "HigherDimensional_Volume",
     "S4 Fractional Breathing Rate — Vdot over V equals 4H.",
     "This is the S4-specific amplification of the radius-breathing law.",
     "VdotOverV4 == 4*H"),
    ("S5 Hypervolume Carrier",
     "For a 5-sphere of radius R, the hypervolume is pi cubed times R to the fifth.",
     r"V_{S^{5}}=\pi^{3}R^{5}",
     "S5 explicit volume extraction", "V_S5, R", "Definition", "HigherDimensional_Volume",
     "S5 Hypervolume Carrier — VS5 equals pi cubed R^5.",
     "This gives the explicit S5 volume carrier used by the higher-dimensional breathing interpretation.",
     "VS5 == Pi^3*R^5"),
    ("S5 Fractional Breathing Rate",
     "The S5 hypervolume fractional breathing rate is five times the Hubble breathing rate.",
     r"\frac{\dot V_{S^{5}}}{V_{S^{5}}}=5H",
     "S5 differentiated volume extraction", "V_S5, H", "Theorem", "HigherDimensional_Volume",
     "S5 Fractional Breathing Rate — Vdot over V equals 5H.",
     "This is the S5-specific amplification of the radius-breathing law.",
     "VdotOverV5 == 5*H"),
    ("Redshift Radius Ratio",
     "Cosmological redshift is the ratio of present radius to emission radius in the breathing model.",
     r"1+z=\frac{R_{0}}{R_{e}}",
     "Redshift breathing extraction", "z, R0, Re", "Definition", "Redshift_Breathing",
     "Redshift Radius Ratio — one plus z equals present radius over emission radius.",
     "This makes redshift a color/wavelength stretching effect of the breathing metric rather than local photon speed change.",
     "1 + z == R0/Re"),
    ("Photon Wavelength Redshift Stretch",
     "Photon wavelength stretches linearly with the breathing radius ratio.",
     r"\lambda_{0}=(1+z)\lambda_{e}",
     "Redshift observable extraction", "lambda0, lambdae, z", "Definition", "Redshift_Breathing",
     "Photon Wavelength Redshift Stretch — observed wavelength equals one plus z times emitted wavelength.",
     "This is the color-stretch carrier in the breathing interpretation.",
     "lambda0 == (1 + z)*lambdae"),
    ("Photon Frequency Redshift Drop",
     "Photon frequency drops inversely with one plus redshift.",
     r"\nu_{0}=\frac{\nu_{e}}{1+z}",
     "Redshift observable extraction", "nu0, nue, z", "Definition", "Redshift_Breathing",
     "Photon Frequency Redshift Drop — observed frequency equals emitted frequency divided by one plus z.",
     "This records the frequency side of the color-stretch interpretation.",
     "nu0 == nue/(1 + z)"),
    ("Photon Energy Redshift Drop",
     "Photon energy drops inversely with one plus redshift.",
     r"E_{0}=\frac{E_{e}}{1+z}",
     "Redshift observable extraction", "E0, Ee, z", "Definition", "Redshift_Breathing",
     "Photon Energy Redshift Drop — observed photon energy equals emitted energy divided by one plus z.",
     "This is the energy-loss side of metric redshift.",
     "E0 == Ee/(1 + z)"),
    ("Sn Redshift Hypervolume Ratio",
     "The present-to-emission hypervolume ratio scales as one plus redshift to the dimension n.",
     r"\frac{V_{S^{n},0}}{V_{S^{n},e}}=(1+z)^{n}",
     "Corrected redshift hypervolume extraction", "V0, Ve, z, n", "Theorem", "Redshift_Breathing",
     "Sn Redshift Hypervolume Ratio — V0 over Ve equals (1+z)^n.",
     "The source examples use present/emission volume ratio. This entry preserves the examples by storing the corrected orientation.",
     "V0/Ve == (1 + z)^n"),
    ("Sn Matter Density Scaling",
     "Matter density distributed through an n-sphere scales inversely with R to the n.",
     r"\rho_{m}\sim R^{-n}",
     "Density scaling extraction", "rho_m, R, n", "Scaling_Law", "HigherDimensional_Density",
     "Sn Matter Density Scaling — matter density scales as R^-n.",
     "This generalizes the familiar S3 matter scaling to S4 and S5.",
     "rhom == R^-n"),
    ("Sn Radiation Density Scaling",
     "Radiation density in an n-sphere scales as inverse R to the n plus one due to volume dilution and photon redshift.",
     r"\rho_{\gamma}\sim R^{-(n+1)}",
     "Density scaling extraction", "rho_gamma, R, n", "Scaling_Law", "HigherDimensional_Density",
     "Sn Radiation Density Scaling — radiation density scales as R^-(n+1).",
     "This is the dimension-generic radiation scaling law for S3, S4, and S5.",
     "rhogamma == R^(-n - 1)"),
    ("Sn Mode Density Scaling",
     "Nested mode density scales as inverse R to the n plus one when mode energy follows hbar omega and omega follows inverse radius.",
     r"\omega\sim R^{-1},\quad V_{S^n}\sim R^{n}\Rightarrow \rho_{\mathrm{mode}}\sim R^{-(n+1)}",
     "Nested mode-density extraction", "omega, V, rho_mode, R, n", "Theorem", "HigherDimensional_Density",
     "Sn Mode Density Scaling — mode density scales as R^-(n+1).",
     "This is the higher-dimensional upgrade of the nested-frequency pressure argument.",
     "rhomode == R^(-n - 1)"),
    ("S4 Mode Density Scaling",
     "For S4, mode density scales as R to the minus fifth.",
     r"\rho_{S^{4}}\sim R^{-5}",
     "S4 density extraction", "rho_S4, R", "Scaling_Law", "HigherDimensional_Density",
     "S4 Mode Density Scaling — S4 mode density scales as R^-5.",
     "This is the S4-specific nested density law.",
     "rho4 == R^-5"),
    ("S5 Mode Density Scaling",
     "For S5, mode density scales as R to the minus sixth.",
     r"\rho_{S^{5}}\sim R^{-6}",
     "S5 density extraction", "rho_S5, R", "Scaling_Law", "HigherDimensional_Density",
     "S5 Mode Density Scaling — S5 mode density scales as R^-6.",
     "This is the S5-specific nested density law.",
     "rho5 == R^-6"),
    ("Occupancy Equivalent Radius Ratio",
     "For an n-dimensional hypervolume fraction phi_i, the equivalent radius ratio is phi_i to the one over n.",
     r"\frac{R_i}{R}=\phi_i^{1/n}",
     "Occupancy radius extraction", "R_i, R, phi_i, n", "Definition", "Occupancy_Interface",
     "Occupancy Equivalent Radius Ratio — Ri over R equals phi_i^(1/n).",
     "This generalizes the occupancy-radius conversion from S3 to S4 and S5.",
     "RiOverR == phi_i^(1/n)"),
    ("Occupancy Equivalent Frequency Ratio",
     "For an n-dimensional hypervolume fraction phi_i, inverse-radius frequency gives equivalent frequency ratio phi_i to the minus one over n.",
     r"\frac{\omega_i}{\omega}=\phi_i^{-1/n}",
     "Occupancy frequency extraction", "omega_i, omega, phi_i, n", "Scaling_Law", "Occupancy_Interface",
     "Occupancy Equivalent Frequency Ratio — omega_i over omega equals phi_i^(-1/n).",
     "This stores the frequency side of the equivalent occupancy-radius conversion.",
     "omegaRatio == phi_i^(-1/n)"),
    ("Folded Phase-Mix Source Term",
     "The folded source term multiplies phase occupancies, resonance gates, Bessel support, capture probability, ratio gates, and energy inversion, then subtracts baryonic damping.",
     r"S_b(n)=\eta_b\phi_T\phi_EK_{TE}G_{\mathrm{res}}D_{\mathrm{DAT}}A_BC_{\mathrm{cap}}R_{\mathrm{mode}}R_{\mathrm{FFT}}I_E-\Gamma_b\phi_b",
     "Folded source-term extraction", "S_b, eta_b, phi_T, phi_E, K_TE, G_res, D_DAT, A_B, C_cap, R_mode, R_FFT, I_E, Gamma_b, phi_b", "Definition", "Folded_Source_Term",
     "Folded Phase-Mix Source Term — source activation multiplies gates and subtracts damping.",
     "This folds the phase mix, mode-ratio gate, FFT-ratio gate, signed energy inversion, Bessel support, and capture probability into one reusable source carrier.",
     "Sb == etab*phiT*phiE*KTE*Gres*DDAT*AB*Ccap*Rmode*RFFT*IE - Gammab*phib"),
    ("Mode Ratio Golden Gate",
     "The mode-ratio gate is a Gaussian weight centered on the golden ratio.",
     r"R_{\mathrm{mode}}=\exp\left[-\frac{(r_{\mathrm{mode}}-\varphi)^2}{2\sigma_r^2}\right]",
     "Mode-ratio gate extraction", "R_mode, r_mode, varphi, sigma_r", "Definition", "Folded_Source_Term",
     "Mode Ratio Golden Gate — Gaussian penalty around the golden ratio.",
     "This stores the mode-ratio gate named in the folded source term.",
     "Rmode == Exp[-(rmode - phi)^2/(2*sigmar^2)]"),
    ("FFT Ratio Golden Gate",
     "The FFT-ratio gate is a Gaussian weight centered on the golden ratio.",
     r"R_{\mathrm{FFT}}=\exp\left[-\frac{(r_{\mathrm{FFT}}-\varphi)^2}{2\sigma_f^2}\right]",
     "FFT-ratio gate extraction", "R_FFT, r_FFT, varphi, sigma_f", "Definition", "Folded_Source_Term",
     "FFT Ratio Golden Gate — Gaussian penalty around the golden ratio.",
     "This stores the FFT-ratio gate named in the folded source term.",
     "RFFT == Exp[-(rfft - phi)^2/(2*sigmaf^2)]"),
    ("Signed Energy Inversion",
     "The TZP energy channel is modeled as equal magnitude and opposite polarity relative to ordinary projection energy.",
     r"E=mc^2,\qquad E_{\mathrm{TZP}}=-E,\qquad I_E=\operatorname{sign}(E_{\mathrm{TZP}}/E)=-1",
     "Energy inversion extraction", "E, m, c, E_TZP, I_E", "Definition", "Folded_Source_Term",
     "Signed Energy Inversion — ETZP equals negative E and IE is negative one.",
     "This records the polarity symmetry rule from the folded source discussion without treating it as proof of physical negative energy.",
     "E == m*c^2 && ETZP == -E && IE == Sign[ETZP/E]"),
    ("Bessel Signal Z Score Calibration",
     "The Bessel support statistic is normalized by the recorded mean and standard deviation.",
     r"z_B=\frac{s(t)-2.5055}{0.2167}",
     "Bessel statistics extraction", "z_B, s(t)", "Diagnostic_Definition", "Folded_Source_Term",
     "Bessel Signal Z Score Calibration — zB equals signal minus 2.5055 over 0.2167.",
     "This records the Bessel signal calibration cited by the folded-source note.",
     "zB == (s - 2.5055)/0.2167"),
    ("Capture Probability Maximum",
     "The cited capture layer has maximum probability 0.175 at e equals 0.045 and sigma equals 0.0005.",
     r"P_{\max}=0.175\quad\text{at}\quad e=0.045,\ \sigma=0.0005",
     "Capture-statistics extraction", "Pmax, e, sigma", "Diagnostic_Definition", "Folded_Source_Term",
     "Capture Probability Maximum — Pmax is 0.175 at e 0.045 and sigma 0.0005.",
     "This stores the max-capture statistic as a diagnostic carrier for later certificate tables.",
     "Pmax == 0.175 && e == 0.045 && sigma == 0.0005"),
]


def read_csv(path):
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path, rows, fieldnames):
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def id_num(tzpid):
    return int(tzpid[2:])


def deterministic_uuid(row):
    seed = "|".join([row["id"], row["title"], row["canonical_statement"], row["canonical_equation"]])
    return str(uuid5(NAMESPACE_URL, "tzpid-source-truth:" + seed))


def md_escape(value):
    return str(value).replace("\n", " ").replace("|", "\\|")


def rebuild_master_md(rows, fieldnames, stamp):
    lines = [
        "# TZPID Canonical Equation Master With Export",
        "",
        f"Generated UTC: {stamp}",
        f"Rows: `{len(rows)}`",
        "",
        "| " + " | ".join(fieldnames) + " |",
        "| " + " | ".join(["---"] * len(fieldnames)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_escape(row.get(field, "")) for field in fieldnames) + " |")
    MASTER_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def source_truth_payload(row, entry, stamp):
    tzpid = row["id"]
    return {
        "schema": {"name": "TZPID source truth prototype", "version": "0.2.1", "generated_at": stamp, "source": "s4_s5_hypersphere_mix_intake", "non_destructive": True},
        "identity": {
            "tzpid": tzpid,
            "uuid": row["uuid"],
            "registry_id": f"registry_id_{id_num(tzpid)}",
            "piid": f"PiID-{id_num(tzpid)}-s4s5-mix",
            "canonical_title": row["title"],
            "source_files": {"s4_s5_hypersphere_mix": SOURCE, "source_truth": str(TZP_ID / tzpid / f"{tzpid}.source_truth.json")},
        },
        "creator": {"name": CREATOR, "orcid": ORCID},
        "classification": {"category": "s4-s5-hypersphere-mix-law", "discipline": "mathematical physics", "loc_class": "QC - Physics", "arxiv_class": "physics.gen-ph"},
        "theory": {"canonical_statement": row["canonical_statement"], "technical_interpretation": row["encyclopedia"], "source_lineage": "Extracted from the saved S4/S5 hypersphere rewrite and folded source-mix section."},
        "canonical_equation": {"latex_blocks": [row["canonical_equation"]], "source_section_latex": row["canonical_equation"]},
        "wolfram_form": {"audit": {"blocks": [{"name": row["title"], "wolfram": entry[-1], "status": "queued_for_s4_s5_mix_certificate"}]}},
        "proof_lane": {"isabelle_kind": row["isabelle_kind"], "obligation_role": row["obligation_role"], "required_checks": row["proof_required_checks"].split(";"), "wolfram_status": row["wolfram_status"], "isabelle_sid": row["isabelle_sid"], "wolfram_artifact": str(OUT / "wolfram" / "s4_s5_hypersphere_mix_check_results.json")},
    }


def write_tex(row):
    tzpid = row["id"]
    text = "\n".join([
        f"% Auto-generated source-truth intake stub for {tzpid}.",
        rf"\tzpentry{{{tzpid}}}{{{row['title']}}}",
        r"\paragraph{Canonical Statement.}",
        row["canonical_statement"],
        r"\paragraph{Canonical Equation.}",
        row["canonical_equation"],
        r"\paragraph{Registry Metadata.}",
        rf"UUID: \texttt{{{row['uuid']}}}. PiID: \texttt{{PiID-{id_num(tzpid)}-s4s5-mix}}. LOC: \texttt{{QC - Physics}}. arXiv: \texttt{{physics.gen-ph}}.",
        "",
    ])
    (TZP_ID / tzpid / f"{tzpid}.tex").write_text(text, encoding="utf-8")


def write_wolfram(stamp):
    wolfram_dir = OUT / "wolfram"
    wolfram_dir.mkdir(parents=True, exist_ok=True)
    script = r'''ClearAll["Global`*"];
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
summary = <|"generated_utc" -> "STAMP", "checks" -> Length[results], "pass" -> Count[results[[All, "status"]], "pass"], "fail" -> Count[results[[All, "status"]], "fail"], "results" -> results|>;
Export["s4_s5_hypersphere_mix_check_results.json", summary, "RawJSON"];
Print[ExportString[summary, "RawJSON"]];
If[summary["fail"] > 0, Exit[1], Exit[0]];
'''.replace("STAMP", stamp)
    (wolfram_dir / "s4_s5_hypersphere_mix_check.wls").write_text(script, encoding="utf-8")


def write_isabelle():
    theory = r'''theory TZPID_S4S5_Hypersphere_Mix_Laws
  imports TZPID_PortalEquilibrium_Laws
begin

text \<open>
  S4/S5 hypersphere-breathing extension and folded source-mix carriers.
  These are algebraic carriers extracted from the saved "restart from the
  original hypersphere" note.
\<close>

definition s45_volume_power :: "real \<Rightarrow> nat \<Rightarrow> real" where
  "s45_volume_power R n = R ^ n"

definition s45_fractional_rate :: "real \<Rightarrow> real \<Rightarrow> nat \<Rightarrow> real" where
  "s45_fractional_rate R Rdot n = real n * Rdot / R"

definition s45_redshift_ratio :: "real \<Rightarrow> real" where
  "s45_redshift_ratio z = 1 + z"

definition s45_present_emission_volume_ratio :: "real \<Rightarrow> nat \<Rightarrow> real" where
  "s45_present_emission_volume_ratio z n = (1 + z) ^ n"

definition s45_density_scaling :: "real \<Rightarrow> nat \<Rightarrow> real" where
  "s45_density_scaling R n = R powr (-(real n))"

definition s45_radiation_density_scaling :: "real \<Rightarrow> nat \<Rightarrow> real" where
  "s45_radiation_density_scaling R n = R powr (-(real n + 1))"

definition s45_occupancy_radius_ratio :: "real \<Rightarrow> nat \<Rightarrow> real" where
  "s45_occupancy_radius_ratio phi n = phi powr (1 / real n)"

definition s45_folded_source ::
  "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real" where
  "s45_folded_source eta_b phi_T phi_E K_TE G_res D_DAT A_B C_cap R_mode R_FFT I_E Gamma_b phi_b =
    eta_b * phi_T * phi_E * K_TE * G_res * D_DAT * A_B * C_cap * R_mode * R_FFT * I_E -
    Gamma_b * phi_b"

definition s45_gaussian_gate :: "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real" where
  "s45_gaussian_gate r center sigma = exp (- ((r - center)\<^sup>2) / (2 * sigma\<^sup>2))"

definition s45_energy_inversion_sign :: "real \<Rightarrow> real \<Rightarrow> real" where
  "s45_energy_inversion_sign E_TZP E = sgn (E_TZP / E)"

definition s45_bessel_z :: "real \<Rightarrow> real" where
  "s45_bessel_z s = (s - 2.5055) / 0.2167"

lemma s45_s3_fractional_rate:
  assumes "R \<noteq> 0"
  shows "s45_fractional_rate R Rdot 3 = 3 * Rdot / R"
  unfolding s45_fractional_rate_def
  by simp

lemma s45_s4_fractional_rate:
  assumes "R \<noteq> 0"
  shows "s45_fractional_rate R Rdot 4 = 4 * Rdot / R"
  unfolding s45_fractional_rate_def
  by simp

lemma s45_s5_fractional_rate:
  assumes "R \<noteq> 0"
  shows "s45_fractional_rate R Rdot 5 = 5 * Rdot / R"
  unfolding s45_fractional_rate_def
  by simp

lemma s45_redshift_volume_examples:
  shows "s45_present_emission_volume_ratio 1 3 = 8
    \<and> s45_present_emission_volume_ratio 1 4 = 16
    \<and> s45_present_emission_volume_ratio 1 5 = 32"
  unfolding s45_present_emission_volume_ratio_def
  by simp

lemma s45_gaussian_gate_at_center:
  assumes "sigma \<noteq> 0"
  shows "s45_gaussian_gate center center sigma = 1"
  unfolding s45_gaussian_gate_def
  using assms
  by simp

lemma s45_energy_inversion_sign_negative:
  assumes "0 < E"
  shows "s45_energy_inversion_sign (-E) E = -1"
  unfolding s45_energy_inversion_sign_def
  using assms
  by simp

lemma s45_bessel_z_center:
  shows "s45_bessel_z 2.5055 = 0"
  unfolding s45_bessel_z_def
  by simp

theorem s45_mix_contract:
  assumes "sigma_r \<noteq> 0"
    and "sigma_f \<noteq> 0"
    and "0 < E"
  shows "s45_fractional_rate R Rdot 4 = 4 * Rdot / R
    \<and> s45_fractional_rate R Rdot 5 = 5 * Rdot / R
    \<and> s45_present_emission_volume_ratio 1 5 = 32
    \<and> s45_gaussian_gate phi phi sigma_r = 1
    \<and> s45_gaussian_gate phi phi sigma_f = 1
    \<and> s45_energy_inversion_sign (-E) E = -1"
proof (intro conjI)
  show "s45_fractional_rate R Rdot 4 = 4 * Rdot / R"
    by (rule s45_s4_fractional_rate)
  show "s45_fractional_rate R Rdot 5 = 5 * Rdot / R"
    by (rule s45_s5_fractional_rate)
  show "s45_present_emission_volume_ratio 1 5 = 32"
    unfolding s45_present_emission_volume_ratio_def
    by simp
  show "s45_gaussian_gate phi phi sigma_r = 1"
    using assms(1)
    by (rule s45_gaussian_gate_at_center)
  show "s45_gaussian_gate phi phi sigma_f = 1"
    using assms(2)
    by (rule s45_gaussian_gate_at_center)
  show "s45_energy_inversion_sign (-E) E = -1"
    using assms(3)
    by (rule s45_energy_inversion_sign_negative)
qed

end
'''
    (ISABELLE_DIR / "TZPID_S4S5_Hypersphere_Mix_Laws.thy").write_text(theory, encoding="utf-8")
    root = ROOT_FILE.read_text(encoding="utf-8")
    name = "    TZPID_S4S5_Hypersphere_Mix_Laws"
    if name not in root:
        root = root.replace(
            "    TZPID_PortalEquilibrium_Laws\n    TZPID_ExternalEvidence_Certificates",
            "    TZPID_PortalEquilibrium_Laws\n" + name + "\n    TZPID_ExternalEvidence_Certificates",
        )
        ROOT_FILE.write_text(root, encoding="utf-8")


def main():
    stamp = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    master_rows = read_csv(MASTER)
    fields = list(master_rows[0].keys())
    max_id = max(id_num(r["id"]) for r in master_rows)
    new_rows = []
    for offset, e in enumerate(ENTRIES, start=1):
        title, statement, equation, method, inputs, kind, role, dictionary, encyclopedia, wolfram = e
        tzpid = f"ID{max_id + offset:04d}"
        row = {
            "id": tzpid,
            "title": title,
            "canonical_statement": statement,
            "canonical_equation": equation,
            "formation_method": method,
            "formation_inputs": inputs,
            "formation_note": f"Extracted from {SOURCE}. Generated UTC {stamp}.",
            "dictionary": dictionary,
            "encyclopedia": encyclopedia,
            "isabelle_kind": kind,
            "obligation_role": role,
            "proof_required_checks": "source_traceability;wolfram_certificate;hol_carrier_typing;empirical_validation_pending",
            "gold_spine": "nested_hyperspherical_enclosure;s4_s5_breathing;folded_source_mix",
            "lean_rocq": f"registry_{tzpid}",
            "wolfram_status": "queued;artifact=peer_review/portal_breathing_intake/wolfram/s4_s5_hypersphere_mix_check_results.json",
            "isabelle_sid": str(id_num(tzpid)),
            "uuid": "",
        }
        row["uuid"] = deterministic_uuid(row)
        new_rows.append((row, e))
    all_rows = master_rows + [r for r, _ in new_rows]
    write_csv(MASTER, all_rows, fields)
    rebuild_master_md(all_rows, fields, stamp)
    dict_rows = read_csv(DICTIONARY)
    dict_fields = list(dict_rows[0].keys())
    dict_rows.extend({"id": r["id"], "title": r["title"], "dictionary_definition": r["dictionary"]} for r, _ in new_rows)
    write_csv(DICTIONARY, dict_rows, dict_fields)
    with ENCYCLOPEDIA.open("a", encoding="utf-8") as h:
        h.write("\n\n## S4/S5 Hypersphere And Folded Source Mix Intake\n\n")
        h.write(f"Generated UTC: {stamp}\n\n")
        for r, _ in new_rows:
            h.write(f"### {r['id']} -- {r['title']}\n\n{r['encyclopedia']}\n\nCanonical equation: `{r['canonical_equation']}`\n\n")
    for r, e in new_rows:
        folder = TZP_ID / r["id"]
        folder.mkdir(parents=True, exist_ok=True)
        (folder / f"{r['id']}.source_truth.json").write_text(json.dumps(source_truth_payload(r, e, stamp), indent=2, ensure_ascii=False), encoding="utf-8")
        write_tex(r)
    OUT.mkdir(parents=True, exist_ok=True)
    write_wolfram(stamp)
    write_isabelle()
    report = {"generated_utc": stamp, "source_file": SOURCE, "previous_max_id": f"ID{max_id:04d}", "new_ids": [r["id"] for r, _ in new_rows], "new_count": len(new_rows), "new_master_rows": len(all_rows)}
    (OUT / "S4_S5_HYPERSPHERE_MIX_INTAKE_REPORT.json").write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
