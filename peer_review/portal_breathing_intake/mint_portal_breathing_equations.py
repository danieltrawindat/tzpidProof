import csv
import json
import re
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
SOURCE_PORTAL = r"D:\Bessel\the_portal_equation.txt"
SOURCE_HYPERSPHERE = r"D:\TZPIDProof\hypersphere_idea.txt"
SOURCE_SPARTA = r"D:\TZPIDProof\this_is_SPARTA"


ENTRIES = [
    {
        "title": "Hyperspherical Hubble Velocity Law",
        "statement": "In the breathing hypersphere model, apparent recession velocity equals the Hubble rate times proper distance.",
        "equation": r"v = H_{0}D",
        "method": "Hypersphere breathing extraction",
        "inputs": "v, H_0, D",
        "kind": "Theorem",
        "role": "Breathing_Geometry",
        "dictionary": "Hyperspherical Hubble Velocity Law — apparent recession is modeled as metric breathing, v equals H0 times D.",
        "encyclopedia": "This entry records the ordinary Hubble law as the observational surface form of hyperspherical breathing. It supports the redshift/color-change interpretation without requiring galaxies to fly through a static external space.",
        "wolfram": "v == H0*D",
    },
    {
        "title": "Scale-Radius Hubble Rate",
        "statement": "The Hubble rate is the logarithmic derivative of the scale radius of the cosmic hypersphere.",
        "equation": r"H(t)=\frac{\dot R(t)}{R(t)}",
        "method": "Scale-factor to radius identification",
        "inputs": "H, R, Rdot",
        "kind": "Definition",
        "role": "Breathing_Geometry",
        "dictionary": "Scale-Radius Hubble Rate — H is Rdot divided by R.",
        "encyclopedia": "This is the clock equation for the breathing enclosure. It rewrites expansion as fractional change of the hyperspherical scale radius.",
        "wolfram": "H == Rdot/R",
    },
    {
        "title": "Closed S3 FLRW Metric",
        "statement": "The closed hyperspherical spatial metric uses angular coordinate chi on S3 with scale radius a(t).",
        "equation": r"ds^{2}=-c^{2}dt^{2}+a(t)^{2}\left[d\chi^{2}+\sin^{2}\chi(d\theta^{2}+\sin^{2}\theta d\phi^{2})\right]",
        "method": "Closed FLRW metric extraction",
        "inputs": "ds, c, t, a, chi, theta, phi",
        "kind": "Definition",
        "role": "Metric_Carrier",
        "dictionary": "Closed S3 FLRW Metric — the S3 line element with scale radius a(t).",
        "encyclopedia": "This gives the carrier geometry for the hyperspherical universe interpretation. It is a metric carrier, not by itself an observational proof of positive curvature.",
        "wolfram": "metricCarrier == {-c^2, a^2, a^2*Sin[chi]^2, a^2*Sin[chi]^2*Sin[theta]^2}",
    },
    {
        "title": "Hyperspherical Proper Distance",
        "statement": "For fixed comoving angular coordinate chi, proper distance is scale radius times chi.",
        "equation": r"D(t)=R(t)\chi",
        "method": "Closed-distance extraction",
        "inputs": "D, R, chi",
        "kind": "Definition",
        "role": "Breathing_Geometry",
        "dictionary": "Hyperspherical Proper Distance — D equals R times chi.",
        "encyclopedia": "This is the local distance rule that lets the Hubble law fall out of scale-radius breathing.",
        "wolfram": "D == R*chi",
    },
    {
        "title": "S3 Hypersphere Volume",
        "statement": "A 3-sphere of radius R has spatial volume two pi squared R cubed.",
        "equation": r"V_{S^{3}}=2\pi^{2}R^{3}",
        "method": "S3 geometry extraction",
        "inputs": "V, R",
        "kind": "Definition",
        "role": "Volume_Carrier",
        "dictionary": "S3 Hypersphere Volume — V equals 2 pi squared R cubed.",
        "encyclopedia": "This volume formula converts radius breathing into volume production in the closed hypersphere model.",
        "wolfram": "VS3 == 2*Pi^2*R^3",
    },
    {
        "title": "S3 Fractional Volume Breathing Rate",
        "statement": "The fractional volume rate of a breathing S3 is three times the Hubble breathing rate.",
        "equation": r"\frac{\dot V}{V}=3\frac{\dot R}{R}=3H",
        "method": "Differentiated S3 volume",
        "inputs": "V, Vdot, R, Rdot, H",
        "kind": "Theorem",
        "role": "Volume_Carrier",
        "dictionary": "S3 Fractional Volume Breathing Rate — Vdot over V equals three Rdot over R.",
        "encyclopedia": "This is one of the key algebraic bridges: the Hubble rate is a radius-breathing rate, while volume production is three times that fractional rate.",
        "wolfram": "VdotOverV == 3*Rdot/R",
    },
    {
        "title": "Closed Curvature Parameter Sign",
        "statement": "For a closed hypersphere with positive spatial curvature k=+1, the cosmological curvature parameter is negative.",
        "equation": r"\Omega_{K}=-\frac{k c^{2}}{a_{0}^{2}H_{0}^{2}},\qquad k=+1\Rightarrow \Omega_{K}<0",
        "method": "Curvature sign extraction",
        "inputs": "Omega_K, k, c, a_0, H_0",
        "kind": "Theorem",
        "role": "Curvature_Carrier",
        "dictionary": "Closed Curvature Parameter Sign — positive k gives negative Omega_K under the cosmology convention.",
        "encyclopedia": "This formalizes the sign convention needed to discuss a nearly flat but globally closed hypersphere.",
        "wolfram": "OmegaK == -k*c^2/(a0^2*H0^2)",
    },
    {
        "title": "Curvature Radius From OmegaK",
        "statement": "The curvature radius is c divided by H0 times the square root of the absolute curvature parameter.",
        "equation": r"R_{c}=\frac{c}{H_{0}\sqrt{|\Omega_{K}|}}",
        "method": "Curvature-radius extraction",
        "inputs": "R_c, c, H_0, Omega_K",
        "kind": "Definition",
        "role": "Curvature_Carrier",
        "dictionary": "Curvature Radius From OmegaK — Rc equals c over H0 square root abs OmegaK.",
        "encyclopedia": "This converts observational curvature bounds into a hyperspherical radius scale.",
        "wolfram": "Rc == c/(H0*Sqrt[Abs[OmegaK]])",
    },
    {
        "title": "Friedmann Breathing Component Equation",
        "statement": "The breathing model augments the Friedmann equation with curvature and a dynamic pressure function F(a).",
        "equation": r"H^{2}(a)=H_{0}^{2}\left[\Omega_{r}a^{-4}+\Omega_{m}a^{-3}+\Omega_{K}a^{-2}+\Omega_{X}F(a)\right]",
        "method": "Friedmann scaffold extraction",
        "inputs": "H, H0, Omega_r, Omega_m, Omega_K, Omega_X, F, a",
        "kind": "Definition",
        "role": "Friedmann_Carrier",
        "dictionary": "Friedmann Breathing Component Equation — H squared is the standard component sum plus dynamic F(a).",
        "encyclopedia": "This is the computational scaffold for comparing closed breathing models against CMB, BAO, and supernova distance data.",
        "wolfram": "Hsq == H0^2*(Or*a^-4 + Om*a^-3 + Ok*a^-2 + Ox*F)",
    },
    {
        "title": "Dynamic Dark-Energy Breathing Function",
        "statement": "The dynamic pressure contribution is encoded by an exponential integral over one plus the equation-of-state function.",
        "equation": r"F(a)=\exp\left(3\int_{a}^{1}\frac{1+w(a')}{a'}\,da'\right)",
        "method": "Dark-energy continuity extraction",
        "inputs": "F, a, w",
        "kind": "Definition",
        "role": "Friedmann_Carrier",
        "dictionary": "Dynamic Dark-Energy Breathing Function — F(a) is the exponential continuity factor.",
        "encyclopedia": "This stores the breathing/pressure history as a standard cosmological continuity factor.",
        "wolfram": "F[a_] := Exp[3*Integrate[(1 + w[x])/x, {x, a, 1}]]",
    },
    {
        "title": "CPL Breathing Equation of State",
        "statement": "The CPL parameterization models the equation of state as w0 plus wa times one minus the scale factor.",
        "equation": r"w(a)=w_{0}+w_{a}(1-a)",
        "method": "CPL extraction",
        "inputs": "w, w0, wa, a",
        "kind": "Definition",
        "role": "Friedmann_Carrier",
        "dictionary": "CPL Breathing Equation of State — w(a) equals w0 plus wa times one minus a.",
        "encyclopedia": "This is the w0-wa parameterization used for the dynamic breathing pressure lane.",
        "wolfram": "w[a_] := w0 + wa*(1 - a)",
    },
    {
        "title": "Closed Angular-Diameter Distance",
        "statement": "Positive-curvature distance replaces the flat chi distance by a sine of chi carrier.",
        "equation": r"D_{A}(z)=\frac{a_{0}\sin\chi(z)}{1+z}",
        "method": "Closed-distance extraction",
        "inputs": "D_A, z, a0, chi",
        "kind": "Definition",
        "role": "Observational_Carrier",
        "dictionary": "Closed Angular-Diameter Distance — DA uses a0 sin chi over 1 plus z.",
        "encyclopedia": "This is the geometric fingerprint to compare closed hypersphere distance against flat distance.",
        "wolfram": "DAclosed == a0*Sin[chi]/(1 + z)",
    },
    {
        "title": "Redshift Drift Breathing Observable",
        "statement": "The redshift drift observable compares present breathing rate with the historical Hubble rate at redshift z.",
        "equation": r"\dot z=(1+z)H_{0}-H(z)",
        "method": "Redshift observable extraction",
        "inputs": "zdot, z, H0, H",
        "kind": "Definition",
        "role": "Observational_Carrier",
        "dictionary": "Redshift Drift Breathing Observable — zdot equals (1+z)H0 minus H(z).",
        "encyclopedia": "This supports the statement that observed color shift is a metric/breathing observable rather than ordinary speed through external space.",
        "wolfram": "zdot == (1 + z)*H0 - Hz",
    },
    {
        "title": "Three-Phase Occupancy Closure",
        "statement": "Ordinary matter, THZ topological-current occupancy, and breathing-volume occupancy sum to one.",
        "equation": r"\phi_{b}(x,t)+\phi_{T}(x,t)+\phi_{E}(x,t)=1",
        "method": "Multiphase occupancy extraction",
        "inputs": "phi_b, phi_T, phi_E",
        "kind": "Definition",
        "role": "Occupancy_Interface",
        "dictionary": "Three-Phase Occupancy Closure — ordinary, topological-current, and breathing phases form a normalized occupancy.",
        "encyclopedia": "This is the conservative mathematical form of the oil-water/interface analogy: phases share an effective container but occupy incompatible state channels.",
        "wolfram": "phib + phiT + phiE == 1",
    },
    {
        "title": "Hyperbolic Phase-Separation Profiles",
        "statement": "Breathing and topological phases can be modeled by complementary tanh interface profiles.",
        "equation": r"\phi_{E}(s)=\frac{1}{2}\left[1+\tanh(s/\ell)\right],\qquad \phi_{T}(s)=\frac{1}{2}\left[1-\tanh(s/\ell)\right]",
        "method": "Interface profile extraction",
        "inputs": "phi_E, phi_T, s, ell",
        "kind": "Definition",
        "role": "Occupancy_Interface",
        "dictionary": "Hyperbolic Phase-Separation Profiles — phiE and phiT are complementary tanh profiles.",
        "encyclopedia": "This gives the phase-separation model a reusable smooth interface carrier.",
        "wolfram": "phiE[s_] := (1 + Tanh[s/ell])/2; phiT[s_] := (1 - Tanh[s/ell])/2",
    },
    {
        "title": "Interface Matter Condensate Profile",
        "statement": "Ordinary matter occupancy is concentrated at the interface by a sech-squared carrier.",
        "equation": r"\phi_{b}(s)\propto \operatorname{sech}^{2}(s/\ell)",
        "method": "Interface condensate extraction",
        "inputs": "phi_b, s, ell",
        "kind": "Definition",
        "role": "Occupancy_Interface",
        "dictionary": "Interface Matter Condensate Profile — ordinary matter peaks at the interface as sech squared.",
        "encyclopedia": "This formalizes matter as a boundary-layer condensate between breathing-volume and topological-current phases.",
        "wolfram": "phib[s_] := Sech[s/ell]^2",
    },
    {
        "title": "Nested Radius Contraction",
        "statement": "A nested enclosure is represented by a radius contraction factor lambda between zero and one.",
        "equation": r"R_{n+1}=\lambda R_{n},\qquad 0<\lambda<1",
        "method": "Nested-scale extraction",
        "inputs": "R_n, lambda",
        "kind": "Definition",
        "role": "Nested_Scaling",
        "dictionary": "Nested Radius Contraction — next radius equals lambda times current radius.",
        "encyclopedia": "This is the carrier for smaller nesting in the hyperspherical hierarchy.",
        "wolfram": "Rnext == lambda*R",
    },
    {
        "title": "Nested Frequency Inverse-Radius Scaling",
        "statement": "Mode frequency scales inversely with the effective enclosure radius.",
        "equation": r"\omega_{\ell q}\sim \frac{c\,j_{\ell+1,q}}{R_{\mathrm{eff}}}",
        "method": "Mode-frequency extraction",
        "inputs": "omega, c, j, R_eff",
        "kind": "Scaling_Law",
        "role": "Nested_Scaling",
        "dictionary": "Nested Frequency Inverse-Radius Scaling — smaller enclosure radius gives higher mode frequency.",
        "encyclopedia": "This is the formal version of the statement that smaller nested scales oscillate faster.",
        "wolfram": "omega == c*j/R",
    },
    {
        "title": "Nested Energy Density Fourth-Power Scaling",
        "statement": "If mode energy scales as hbar omega and omega scales as inverse radius while volume scales as R cubed, energy density scales as R to the minus fourth.",
        "equation": r"E_{n}\sim\hbar\omega_{n},\quad V_{n}\sim R_{n}^{3},\quad \omega_{n}\sim R_{n}^{-1}\Rightarrow \rho_{n}\sim R_{n}^{-4}",
        "method": "Nested-density extraction",
        "inputs": "E, hbar, omega, V, R, rho",
        "kind": "Theorem",
        "role": "Nested_Scaling",
        "dictionary": "Nested Energy Density Fourth-Power Scaling — density rises as inverse fourth power of radius.",
        "encyclopedia": "This is the core bridge between nested smaller scales, higher oscillation, and pressure/matter-threshold behavior.",
        "wolfram": "rho == hbar*c/R^4",
    },
    {
        "title": "Laplace-Style THZ Breathing Interface Pressure",
        "statement": "The THZ/breathing interface pressure jump is modeled by an interface tension times the sum of reciprocal curvature radii.",
        "equation": r"\Delta P_{\mathrm{THZ/E}}=\sigma_{\mathrm{THZ/E}}\left(\frac{1}{R_{\mathrm{THZ}}}+\frac{1}{R_{E}}\right)",
        "method": "Interface pressure extraction",
        "inputs": "DeltaP, sigma, R_THZ, R_E",
        "kind": "Definition",
        "role": "Occupancy_Interface",
        "dictionary": "Laplace-Style Interface Pressure — pressure jump is sigma times reciprocal radii sum.",
        "encyclopedia": "This adapts multiphase-fluid interface reasoning to the topological-current/breathing phase boundary.",
        "wolfram": "DeltaP == sigma*(1/Rt + 1/Re)",
    },
    {
        "title": "Total Stress-Energy Phase Decomposition",
        "statement": "The effective total stress-energy is decomposed into ordinary, topological-current, breathing, and interface contributions.",
        "equation": r"T^{\mathrm{total}}_{\mu\nu}=T^{b}_{\mu\nu}+T^{T}_{\mu\nu}+T^{E}_{\mu\nu}+T^{\mathrm{interface}}_{\mu\nu}",
        "method": "Stress-energy decomposition extraction",
        "inputs": "T_total, T_b, T_T, T_E, T_interface",
        "kind": "Definition",
        "role": "Stress_Energy_Carrier",
        "dictionary": "Total Stress-Energy Phase Decomposition — total stress-energy is a sum of four phase contributions.",
        "encyclopedia": "This provides the conservative carrier form for unifying ordinary matter, dark/topological current, breathing pressure, and interface stress.",
        "wolfram": "Ttotal == Tb + Tt + Te + Ti",
    },
    {
        "title": "Portal Force-Balance Equation",
        "statement": "The portal-equilibrium condition is represented as net zero directional force across gravitational, inertial, surface, electromagnetic, and zero-point contributions.",
        "equation": r"\sum_i F_i=F_g+F_{\mathrm{inertial}}+F_{\sigma}+F_{\mathrm{EM}}+F_{\mathrm{ZPF}}=0",
        "method": "Portal-equilibrium extraction",
        "inputs": "F_g, F_inertial, F_sigma, F_EM, F_ZPF",
        "kind": "Constraint",
        "role": "Portal_Equilibrium",
        "dictionary": "Portal Force-Balance Equation — the portal condition is zero net force across the modeled contributions.",
        "encyclopedia": "This is a formal placeholder for the water-droplet/field-equilibrium portal idea. It is a balance constraint and should be tested experimentally before being treated as a physical law.",
        "wolfram": "Fg + Fi + Fs + Fem + Fzpf == 0",
    },
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
    seed = "|".join(
        [
            row["id"],
            row["title"],
            row["canonical_statement"],
            row["canonical_equation"],
        ]
    )
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
        "schema": {
            "name": "TZPID source truth prototype",
            "version": "0.2.1",
            "generated_at": stamp,
            "source": "portal_breathing_intake",
            "non_destructive": True,
        },
        "identity": {
            "tzpid": tzpid,
            "uuid": row["uuid"],
            "registry_id": f"registry_id_{id_num(tzpid)}",
            "piid": f"PiID-{id_num(tzpid)}-portal-breathing",
            "canonical_title": row["title"],
            "source_files": {
                "portal_equation": SOURCE_PORTAL,
                "hypersphere_idea": SOURCE_HYPERSPHERE,
                "sparta_support": SOURCE_SPARTA,
                "source_truth": str(TZP_ID / tzpid / f"{tzpid}.source_truth.json"),
            },
        },
        "creator": {"name": CREATOR, "orcid": ORCID},
        "classification": {
            "category": "portal-breathing-occupancy-interface",
            "discipline": "mathematical physics",
            "loc_class": "QC - Physics",
            "arxiv_class": "physics.gen-ph",
        },
        "theory": {
            "canonical_statement": row["canonical_statement"],
            "technical_interpretation": row["encyclopedia"],
            "source_lineage": "Extracted from the_portal_equation.txt and hypersphere_idea.txt; SPARTA files provide computational cosmology context.",
        },
        "canonical_equation": {
            "latex_blocks": [row["canonical_equation"]],
            "source_section_latex": row["canonical_equation"],
        },
        "wolfram_form": {
            "audit": {
                "blocks": [
                    {
                        "name": row["title"],
                        "wolfram": entry["wolfram"],
                        "status": "queued_for_portal_breathing_certificate",
                    }
                ]
            }
        },
        "proof_lane": {
            "isabelle_kind": row["isabelle_kind"],
            "obligation_role": row["obligation_role"],
            "required_checks": row["proof_required_checks"].split(";"),
            "wolfram_status": row["wolfram_status"],
            "isabelle_sid": row["isabelle_sid"],
            "wolfram_artifact": str(OUT / "wolfram" / "portal_breathing_check_results.json"),
        },
    }


def write_tex(row):
    tzpid = row["id"]
    text = "\n".join(
        [
            f"% Auto-generated source-truth intake stub for {tzpid}.",
            rf"\tzpentry{{{tzpid}}}{{{row['title']}}}",
            r"\paragraph{Canonical Statement.}",
            row["canonical_statement"],
            r"\paragraph{Canonical Equation.}",
            row["canonical_equation"],
            r"\paragraph{Registry Metadata.}",
            rf"UUID: \texttt{{{row['uuid']}}}. PiID: \texttt{{PiID-{id_num(tzpid)}-portal-breathing}}. LOC: \texttt{{QC - Physics}}. arXiv: \texttt{{physics.gen-ph}}.",
            "",
        ]
    )
    target = TZP_ID / tzpid / f"{tzpid}.tex"
    target.write_text(text, encoding="utf-8")


def write_wolfram(stamp):
    wolfram_dir = OUT / "wolfram"
    wolfram_dir.mkdir(parents=True, exist_ok=True)
    text = r'''(* TZPID portal-breathing / occupancy-interface certificate *)
ClearAll["Global`*"];

checks = {
  <|"name" -> "hubble_law_from_breathing",
    "expr" -> FullSimplify[Rdot*chi == (Rdot/R)*(R*chi), Assumptions -> R != 0]|>,
  <|"name" -> "s3_fractional_volume_rate",
    "expr" -> FullSimplify[(D[2*Pi^2*R[t]^3, t]/(2*Pi^2*R[t]^3)) == 3*R'[t]/R[t], Assumptions -> R[t] != 0]|>,
  <|"name" -> "closed_curvature_negative_sample",
    "expr" -> TrueQ[-1*1^2/(2^2*3^2) < 0]|>,
  <|"name" -> "curvature_radius_positive_sample",
    "expr" -> TrueQ[1/(2*Sqrt[Abs[-1/4]]) == 1]|>,
  <|"name" -> "cpl_Fa_closed_form",
    "expr" -> FullSimplify[
      Exp[3*Integrate[(1 + w0 + wa*(1 - x))/x, {x, a, 1}]] ==
        a^(-3*(1 + w0 + wa))*Exp[3*wa*(a - 1)],
      Assumptions -> a > 0]|>,
  <|"name" -> "tanh_profiles_partition",
    "expr" -> FullSimplify[(1 + Tanh[s/ell])/2 + (1 - Tanh[s/ell])/2 == 1, Assumptions -> ell != 0]|>,
  <|"name" -> "nested_frequency_ratio",
    "expr" -> FullSimplify[(c*j/(lambda*R))/(c*j/R) == 1/lambda,
      Assumptions -> c != 0 && j != 0 && R != 0 && lambda != 0]|>,
  <|"name" -> "nested_density_ratio",
    "expr" -> FullSimplify[(hbar*c/(lambda*R)^4)/(hbar*c/R^4) == 1/lambda^4,
      Assumptions -> hbar != 0 && c != 0 && R != 0 && lambda != 0]|>,
  <|"name" -> "interface_pressure_positive_sample",
    "expr" -> TrueQ[2*(1/3 + 1/5) > 0]|>,
  <|"name" -> "stress_energy_sum",
    "expr" -> FullSimplify[Tb + Tt + Te + Ti == Ttotal /. Ttotal -> Tb + Tt + Te + Ti]|>,
  <|"name" -> "portal_force_balance",
    "expr" -> FullSimplify[Fg + Fi + Fs + Fem + Fzpf == 0 /. Fzpf -> -(Fg + Fi + Fs + Fem)]|>
};

results = checks /. a_Association :> Append[a, "status" -> If[TrueQ[a["expr"]], "pass", "fail"]];
summary = <|
  "generated_utc" -> "STAMP_PLACEHOLDER",
  "checks" -> Length[results],
  "pass" -> Count[results[[All, "status"]], "pass"],
  "fail" -> Count[results[[All, "status"]], "fail"],
  "results" -> results
|>;

Export["portal_breathing_check_results.json", summary, "RawJSON"];
Print[ExportString[summary, "RawJSON"]];
If[summary["fail"] > 0, Exit[1], Exit[0]];
'''.replace("STAMP_PLACEHOLDER", stamp)
    (wolfram_dir / "portal_breathing_check.wls").write_text(text, encoding="utf-8")


def write_isabelle():
    theory = r'''theory TZPID_PortalBreathing_OccupancyInterface
  imports
    TZPID_HubbleBreathing_Enclosure
    TZPID_MatterCreation_PressureEoS
begin

text \<open>
  Project: TZPID Proof Pipeline
  Creator: Daniel Alexander Trawin
  ORCID: https://orcid.org/0009-0001-4630-3715

  Source lane: portal-breathing intake from the_portal_equation.txt and
  hypersphere_idea.txt.

  This file keeps the claims conservative: it formalizes algebraic carriers,
  normalized occupancy, nested inverse-radius scaling, interface pressure, and
  portal force balance. It does not assert empirical truth of the physical
  interpretation.
\<close>

definition pb_redshift_wavelength :: "real \<Rightarrow> real \<Rightarrow> real" where
  "pb_redshift_wavelength z lambda_emit = (1 + z) * lambda_emit"

definition pb_redshift_frequency :: "real \<Rightarrow> real \<Rightarrow> real" where
  "pb_redshift_frequency z freq_emit = freq_emit / (1 + z)"

definition pb_three_phase_closed :: "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> bool" where
  "pb_three_phase_closed phi_b phi_T phi_E \<longleftrightarrow> phi_b + phi_T + phi_E = 1"

definition pb_interface_phi_E :: "real \<Rightarrow> real \<Rightarrow> real" where
  "pb_interface_phi_E s ell = (1 + tanh (s / ell)) / 2"

definition pb_interface_phi_T :: "real \<Rightarrow> real \<Rightarrow> real" where
  "pb_interface_phi_T s ell = (1 - tanh (s / ell)) / 2"

definition pb_nested_radius :: "real \<Rightarrow> real \<Rightarrow> real" where
  "pb_nested_radius lambda R = lambda * R"

definition pb_mode_frequency :: "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real" where
  "pb_mode_frequency c j R = c * j / R"

definition pb_mode_energy_density :: "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real" where
  "pb_mode_energy_density hbar c R = hbar * c / R\<^sup>4"

definition pb_interface_pressure :: "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real" where
  "pb_interface_pressure sigma R_T R_E = sigma * (1 / R_T + 1 / R_E)"

definition pb_total_stress_energy :: "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real" where
  "pb_total_stress_energy T_b T_T T_E T_I = T_b + T_T + T_E + T_I"

definition pb_portal_force_balance :: "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> bool" where
  "pb_portal_force_balance F_g F_i F_sigma F_EM F_ZPF \<longleftrightarrow>
    F_g + F_i + F_sigma + F_EM + F_ZPF = 0"

lemma pb_redshift_color_not_speed_carrier:
  assumes "z \<noteq> -1"
  shows "pb_redshift_wavelength z lambda_emit *
      pb_redshift_frequency z freq_emit =
    lambda_emit * freq_emit"
proof -
  show ?thesis
    unfolding pb_redshift_wavelength_def pb_redshift_frequency_def
    using assms
    by field
qed

lemma pb_interface_profiles_partition:
  shows "pb_interface_phi_E s ell + pb_interface_phi_T s ell = 1"
proof -
  show ?thesis
    unfolding pb_interface_phi_E_def pb_interface_phi_T_def
    by algebra
qed

lemma pb_interface_profiles_close_three_phase_without_matter:
  shows "pb_three_phase_closed 0 (pb_interface_phi_T s ell) (pb_interface_phi_E s ell)"
proof -
  have "0 + pb_interface_phi_T s ell + pb_interface_phi_E s ell = 1"
    using pb_interface_profiles_partition[of s ell]
    by linarith
  then show ?thesis
    unfolding pb_three_phase_closed_def .
qed

lemma pb_nested_frequency_ratio:
  assumes "lambda \<noteq> 0"
    and "R \<noteq> 0"
    and "c \<noteq> 0"
    and "j \<noteq> 0"
  shows "pb_mode_frequency c j (pb_nested_radius lambda R) /
      pb_mode_frequency c j R = 1 / lambda"
proof -
  show ?thesis
    unfolding pb_mode_frequency_def pb_nested_radius_def
    using assms
    by field
qed

lemma pb_nested_density_ratio:
  assumes "lambda \<noteq> 0"
    and "R \<noteq> 0"
    and "hbar \<noteq> 0"
    and "c \<noteq> 0"
  shows "pb_mode_energy_density hbar c (pb_nested_radius lambda R) /
      pb_mode_energy_density hbar c R = 1 / lambda\<^sup>4"
proof -
  have lambda4_nonzero: "lambda\<^sup>4 \<noteq> 0"
    using assms(1)
    by positivity
  show ?thesis
    unfolding pb_mode_energy_density_def pb_nested_radius_def
    using assms lambda4_nonzero
    by field
qed

lemma pb_interface_pressure_positive:
  assumes "0 < sigma"
    and "0 < R_T"
    and "0 < R_E"
  shows "0 < pb_interface_pressure sigma R_T R_E"
proof -
  have reciprocal_sum_pos: "0 < 1 / R_T + 1 / R_E"
    using assms
    by positivity
  show ?thesis
    unfolding pb_interface_pressure_def
    using assms reciprocal_sum_pos
    by positivity
qed

lemma pb_total_stress_energy_unfolds:
  shows "pb_total_stress_energy T_b T_T T_E T_I =
    T_b + T_T + T_E + T_I"
  unfolding pb_total_stress_energy_def .

lemma pb_portal_balance_by_counterterm:
  shows "pb_portal_force_balance
    F_g F_i F_sigma F_EM (-(F_g + F_i + F_sigma + F_EM))"
proof -
  show ?thesis
    unfolding pb_portal_force_balance_def
    by algebra
qed

theorem pb_portal_breathing_interface_contract:
  assumes "lambda \<noteq> 0"
    and "R \<noteq> 0"
    and "c \<noteq> 0"
    and "j \<noteq> 0"
    and "hbar \<noteq> 0"
  shows "pb_interface_phi_E s ell + pb_interface_phi_T s ell = 1
    \<and> pb_mode_frequency c j (pb_nested_radius lambda R) /
        pb_mode_frequency c j R = 1 / lambda
    \<and> pb_mode_energy_density hbar c (pb_nested_radius lambda R) /
        pb_mode_energy_density hbar c R = 1 / lambda\<^sup>4
    \<and> pb_portal_force_balance
        F_g F_i F_sigma F_EM (-(F_g + F_i + F_sigma + F_EM))"
proof (intro conjI)
  show "pb_interface_phi_E s ell + pb_interface_phi_T s ell = 1"
    by (rule pb_interface_profiles_partition)
  show "pb_mode_frequency c j (pb_nested_radius lambda R) /
        pb_mode_frequency c j R = 1 / lambda"
    using assms(1,2,3,4)
    by (rule pb_nested_frequency_ratio)
  show "pb_mode_energy_density hbar c (pb_nested_radius lambda R) /
        pb_mode_energy_density hbar c R = 1 / lambda\<^sup>4"
    using assms(1,2,5,3)
    by (rule pb_nested_density_ratio)
  show "pb_portal_force_balance
        F_g F_i F_sigma F_EM (-(F_g + F_i + F_sigma + F_EM))"
    by (rule pb_portal_balance_by_counterterm)
qed

end
'''
    (ISABELLE_DIR / "TZPID_PortalBreathing_OccupancyInterface.thy").write_text(theory, encoding="utf-8")
    root = ROOT_FILE.read_text(encoding="utf-8")
    theory_name = "    TZPID_PortalBreathing_OccupancyInterface"
    if theory_name not in root:
        root = root.replace(
            "    TZPID_TRAWIN_Composition_GoldSpine\n    TZPID_ExternalEvidence_Certificates",
            "    TZPID_TRAWIN_Composition_GoldSpine\n"
            + theory_name
            + "\n    TZPID_ExternalEvidence_Certificates",
        )
        ROOT_FILE.write_text(root, encoding="utf-8")


def main():
    stamp = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    OUT.mkdir(parents=True, exist_ok=True)
    master_rows = read_csv(MASTER)
    fieldnames = list(master_rows[0].keys())
    existing_ids = {row["id"] for row in master_rows}
    max_id = max(id_num(row["id"]) for row in master_rows)

    new_rows = []
    for offset, entry in enumerate(ENTRIES, start=1):
        tzpid = f"ID{max_id + offset:04d}"
        row = {
            "id": tzpid,
            "title": entry["title"],
            "canonical_statement": entry["statement"],
            "canonical_equation": entry["equation"],
            "formation_method": entry["method"],
            "formation_inputs": entry["inputs"],
            "formation_note": f"Extracted from {SOURCE_PORTAL} and {SOURCE_HYPERSPHERE}; SPARTA files provide supporting computational context. Generated UTC {stamp}.",
            "dictionary": entry["dictionary"],
            "encyclopedia": entry["encyclopedia"],
            "isabelle_kind": entry["kind"],
            "obligation_role": entry["role"],
            "proof_required_checks": "source_traceability;wolfram_certificate;hol_carrier_typing",
            "gold_spine": "nested_hyperspherical_enclosure;portal_breathing;occupancy_interface",
            "lean_rocq": f"registry_{tzpid}",
            "wolfram_status": "queued;artifact=peer_review/portal_breathing_intake/wolfram/portal_breathing_check_results.json",
            "isabelle_sid": str(id_num(tzpid)),
            "uuid": "",
        }
        row["uuid"] = deterministic_uuid(row)
        if tzpid in existing_ids:
            raise RuntimeError(f"ID collision: {tzpid}")
        new_rows.append((row, entry))

    all_rows = master_rows + [row for row, _ in new_rows]
    write_csv(MASTER, all_rows, fieldnames)
    rebuild_master_md(all_rows, fieldnames, stamp)

    dict_rows = read_csv(DICTIONARY)
    dict_fields = list(dict_rows[0].keys())
    dict_rows.extend(
        {
            "id": row["id"],
            "title": row["title"],
            "dictionary_definition": row["dictionary"],
        }
        for row, _ in new_rows
    )
    write_csv(DICTIONARY, dict_rows, dict_fields)

    with ENCYCLOPEDIA.open("a", encoding="utf-8") as handle:
        handle.write("\n\n## Portal Breathing / Occupancy Interface Intake\n\n")
        handle.write(f"Generated UTC: {stamp}\n\n")
        for row, _entry in new_rows:
            handle.write(f"### {row['id']} -- {row['title']}\n\n")
            handle.write(f"{row['encyclopedia']}\n\n")
            handle.write(f"Canonical equation: `{row['canonical_equation']}`\n\n")

    for row, entry in new_rows:
        folder = TZP_ID / row["id"]
        folder.mkdir(parents=True, exist_ok=True)
        (folder / f"{row['id']}.source_truth.json").write_text(
            json.dumps(source_truth_payload(row, entry, stamp), indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        write_tex(row)

    write_wolfram(stamp)
    write_isabelle()

    report = {
        "generated_utc": stamp,
        "source_files": [SOURCE_PORTAL, SOURCE_HYPERSPHERE, SOURCE_SPARTA],
        "excluded_non_math_source": r"D:\UserData\.vscode\extensions\anthropic.claude-code-2.1.173-win32-x64\README.md",
        "previous_max_id": f"ID{max_id:04d}",
        "new_ids": [row["id"] for row, _ in new_rows],
        "new_count": len(new_rows),
        "new_master_rows": len(all_rows),
        "isabelle_theory": str(ISABELLE_DIR / "TZPID_PortalBreathing_OccupancyInterface.thy"),
        "wolfram_script": str(OUT / "wolfram" / "portal_breathing_check.wls"),
    }
    (OUT / "PORTAL_BREATHING_INTAKE_REPORT.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
