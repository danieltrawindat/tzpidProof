import csv
import json
import math
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


ENTRIES = [
    {
        "title": "Portal Gravity Force Component",
        "statement": "The gravity component in the portal force model is mass times gravitational acceleration.",
        "equation": r"F_{g}=mg",
        "method": "Portal force-vector extraction",
        "inputs": "F_g, m, g",
        "kind": "Definition",
        "role": "Portal_Force_Component",
        "dictionary": "Portal Gravity Force Component — gravity force is mass times gravitational acceleration.",
        "encyclopedia": "This is a standard component of the portal force-vector model. It is a modeling carrier, not a new gravitational law.",
        "wolfram": "Fg == m*g",
    },
    {
        "title": "Portal Surface-Tension Force Component",
        "statement": "The surface-tension component is modeled by a Young-Laplace-style curvature pressure term.",
        "equation": r"F_{s}=\gamma\left(\frac{1}{R_{1}}+\frac{1}{R_{2}}\right)",
        "method": "Portal force-vector extraction",
        "inputs": "F_s, gamma, R_1, R_2",
        "kind": "Definition",
        "role": "Portal_Force_Component",
        "dictionary": "Portal Surface-Tension Force Component — surface force is gamma times the sum of reciprocal curvature radii.",
        "encyclopedia": "This carries the Young-Laplace part of the droplet equilibrium model into the registry.",
        "wolfram": "Fs == gamma*(1/R1 + 1/R2)",
    },
    {
        "title": "Portal Inertial Force Component",
        "statement": "The inertial component in the portal force model is mass times acceleration.",
        "equation": r"F_{i}=ma",
        "method": "Portal force-vector extraction",
        "inputs": "F_i, m, a",
        "kind": "Definition",
        "role": "Portal_Force_Component",
        "dictionary": "Portal Inertial Force Component — inertial force is mass times acceleration.",
        "encyclopedia": "This is the inertial/momentum carrier for apex dynamics in the droplet equilibrium model.",
        "wolfram": "Fi == m*a",
    },
    {
        "title": "Portal Acoustic Pressure Force Component",
        "statement": "The acoustic or external field pressure component is pressure times effective area.",
        "equation": r"F_{a}=PA",
        "method": "Portal force-vector extraction",
        "inputs": "F_a, P, A",
        "kind": "Definition",
        "role": "Portal_Force_Component",
        "dictionary": "Portal Acoustic Pressure Force Component — acoustic/field force is pressure times area.",
        "encyclopedia": "This gives the acoustic or field-pressure term used to stabilize the candidate equilibrium state.",
        "wolfram": "Fa == P*A",
    },
    {
        "title": "Portal Drag Force Component",
        "statement": "The drag component is modeled by the standard quadratic drag law.",
        "equation": r"F_{r}=\frac{1}{2}\rho v^{2}C_{d}A",
        "method": "Portal force-vector extraction",
        "inputs": "F_r, rho, v, C_d, A",
        "kind": "Definition",
        "role": "Portal_Force_Component",
        "dictionary": "Portal Drag Force Component — drag force is one half rho v squared Cd A.",
        "encyclopedia": "This supplies the air-resistance term explicitly named in the portal force-vector section.",
        "wolfram": "Fr == 1/2*rho*v^2*Cd*A",
    },
    {
        "title": "Five-Force Portal Equilibrium Balance",
        "statement": "The droplet portal-equilibrium condition is the vanishing of the gravity, surface-tension, inertial, acoustic-pressure, and drag force sum.",
        "equation": r"F_{g}+F_{s}+F_{i}+F_{a}+F_{r}=0",
        "method": "Portal force-vector synthesis",
        "inputs": "F_g, F_s, F_i, F_a, F_r",
        "kind": "Constraint",
        "role": "Portal_Equilibrium",
        "dictionary": "Five-Force Portal Equilibrium Balance — the modeled equilibrium occurs when five force terms sum to zero.",
        "encyclopedia": "This is the saved transcript's sharper portal balance. It supplements the earlier generic force-balance carrier by naming the air-resistance term explicitly.",
        "wolfram": "Fg + Fs + Fi + Fa + Fr == 0",
    },
    {
        "title": "Portal Phi Force Ratio",
        "statement": "The portal analysis tracks the ratio of surface-tension force to inertial force as a candidate convergence toward the golden ratio.",
        "equation": r"\phi_{\mathrm{ratio}}=\frac{F_{s}}{F_{i}}",
        "method": "Phi ratio extraction",
        "inputs": "phi_ratio, F_s, F_i",
        "kind": "Diagnostic_Definition",
        "role": "Portal_Phi_Diagnostic",
        "dictionary": "Portal Phi Force Ratio — phi_ratio is Fs divided by Fi.",
        "encyclopedia": "This stores the diagnostic used to test whether the equilibrium data approaches the golden ratio. The convergence claim remains empirical until backed by measured data.",
        "wolfram": "phiRatio == Fs/Fi",
    },
    {
        "title": "Golden Portal State Equation",
        "statement": "The candidate golden equilibrium state is achieved when phi-scaled surface tension balances inertial plus acoustic/field pressure contributions.",
        "equation": r"\mathrm{PortalState}=\frac{F_{s}\varphi}{F_{i}+F_{a}}=1",
        "method": "Phi equilibrium synthesis",
        "inputs": "PortalState, F_s, F_i, F_a, varphi",
        "kind": "Candidate_Law",
        "role": "Portal_Phi_Equilibrium",
        "dictionary": "Golden Portal State Equation — portal state equals Fs phi over Fi plus Fa and is set to one.",
        "encyclopedia": "This captures the central candidate law in the saved portal-equation section. It is registered as a candidate law because the source transcript asserts validation, while the proof package still requires independent experimental data.",
        "wolfram": "portalState == Fs*phi/(Fi + Fa)",
    },
    {
        "title": "Predicted Acoustic Pressure Rearrangement",
        "statement": "Solving the golden portal state equation for the acoustic/field pressure force gives the predicted stabilizing field contribution.",
        "equation": r"F_{a,\mathrm{pred}}=F_{s}\varphi-F_{i}",
        "method": "Algebraic rearrangement of golden portal state",
        "inputs": "F_a_pred, F_s, F_i, varphi",
        "kind": "Theorem",
        "role": "Portal_Phi_Equilibrium",
        "dictionary": "Predicted Acoustic Pressure Rearrangement — Fa_pred equals Fs phi minus Fi under PortalState equals one.",
        "encyclopedia": "This is the algebraic rearrangement of the golden portal state. It is Wolfram-checkable and useful for future experimental prediction tables.",
        "wolfram": "FaPred == Fs*phi - Fi",
    },
    {
        "title": "Golden Ratio Constant Carrier",
        "statement": "The phi carrier is the positive golden ratio.",
        "equation": r"\varphi=\frac{1+\sqrt{5}}{2}",
        "method": "Constant carrier extraction",
        "inputs": "varphi",
        "kind": "Definition",
        "role": "Portal_Phi_Equilibrium",
        "dictionary": "Golden Ratio Constant Carrier — phi is one plus square root five over two.",
        "encyclopedia": "This gives the portal-equilibrium source lane a precise golden-ratio constant carrier.",
        "wolfram": "phi == (1 + Sqrt[5])/2",
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
        "schema": {
            "name": "TZPID source truth prototype",
            "version": "0.2.1",
            "generated_at": stamp,
            "source": "portal_equilibrium_laws_intake",
            "non_destructive": True,
        },
        "identity": {
            "tzpid": tzpid,
            "uuid": row["uuid"],
            "registry_id": f"registry_id_{id_num(tzpid)}",
            "piid": f"PiID-{id_num(tzpid)}-portal-equilibrium",
            "canonical_title": row["title"],
            "source_files": {
                "portal_equation": SOURCE_PORTAL,
                "source_truth": str(TZP_ID / tzpid / f"{tzpid}.source_truth.json"),
            },
        },
        "creator": {"name": CREATOR, "orcid": ORCID},
        "classification": {
            "category": "portal-equilibrium-force-law",
            "discipline": "mathematical physics",
            "loc_class": "QC - Physics",
            "arxiv_class": "physics.gen-ph",
        },
        "theory": {
            "canonical_statement": row["canonical_statement"],
            "technical_interpretation": row["encyclopedia"],
            "source_lineage": "Extracted from the saved portal-equation force-vector and phi-equilibrium sections.",
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
                        "status": "queued_for_portal_equilibrium_laws_certificate",
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
            "wolfram_artifact": str(OUT / "wolfram" / "portal_equilibrium_laws_check_results.json"),
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
            rf"UUID: \texttt{{{row['uuid']}}}. PiID: \texttt{{PiID-{id_num(tzpid)}-portal-equilibrium}}. LOC: \texttt{{QC - Physics}}. arXiv: \texttt{{physics.gen-ph}}.",
            "",
        ]
    )
    (TZP_ID / tzpid / f"{tzpid}.tex").write_text(text, encoding="utf-8")


def write_wolfram(stamp):
    wolfram_dir = OUT / "wolfram"
    wolfram_dir.mkdir(parents=True, exist_ok=True)
    script = r'''ClearAll["Global`*"];
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
summary = <|"generated_utc" -> "STAMP", "checks" -> Length[results], "pass" -> Count[results[[All, "status"]], "pass"], "fail" -> Count[results[[All, "status"]], "fail"], "results" -> results|>;
Export["portal_equilibrium_laws_check_results.json", summary, "RawJSON"];
Print[ExportString[summary, "RawJSON"]];
If[summary["fail"] > 0, Exit[1], Exit[0]];
'''.replace("STAMP", stamp)
    (wolfram_dir / "portal_equilibrium_laws_check.wls").write_text(script, encoding="utf-8")


def write_isabelle():
    theory = r'''theory TZPID_PortalEquilibrium_Laws
  imports TZPID_PortalBreathing_OccupancyInterface
begin

text \<open>
  Portal-equilibrium law extraction from the saved force-vector and phi-ratio
  sections of the_portal_equation.txt. These are conservative carriers and
  algebraic checks, not empirical validation of the stronger transcript claims.
\<close>

definition pe_gravity_force :: "real \<Rightarrow> real \<Rightarrow> real" where
  "pe_gravity_force m g = m * g"

definition pe_surface_force :: "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real" where
  "pe_surface_force gamma R1 R2 = gamma * (1 / R1 + 1 / R2)"

definition pe_inertial_force :: "real \<Rightarrow> real \<Rightarrow> real" where
  "pe_inertial_force m a = m * a"

definition pe_acoustic_force :: "real \<Rightarrow> real \<Rightarrow> real" where
  "pe_acoustic_force P A = P * A"

definition pe_drag_force :: "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real" where
  "pe_drag_force rho v C_d A = (1 / 2) * rho * v\<^sup>2 * C_d * A"

definition pe_five_force_balance :: "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> bool" where
  "pe_five_force_balance F_g F_s F_i F_a F_r \<longleftrightarrow>
    F_g + F_s + F_i + F_a + F_r = 0"

definition pe_phi_ratio :: "real \<Rightarrow> real \<Rightarrow> real" where
  "pe_phi_ratio F_s F_i = F_s / F_i"

definition pe_portal_state :: "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real" where
  "pe_portal_state F_s F_i F_a phi = F_s * phi / (F_i + F_a)"

definition pe_predicted_acoustic_force :: "real \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real" where
  "pe_predicted_acoustic_force F_s F_i phi = F_s * phi - F_i"

definition pe_golden_ratio :: real where
  "pe_golden_ratio = (1 + sqrt 5) / 2"

lemma pe_five_force_balance_by_counterterm:
  shows "pe_five_force_balance F_g F_s F_i F_a (-(F_g + F_s + F_i + F_a))"
  unfolding pe_five_force_balance_def
  by algebra

lemma pe_portal_state_one_from_predicted_acoustic_force:
  assumes "F_s * phi \<noteq> 0"
  shows "pe_portal_state F_s F_i
    (pe_predicted_acoustic_force F_s F_i phi) phi = 1"
proof -
  show ?thesis
    unfolding pe_portal_state_def pe_predicted_acoustic_force_def
    using assms
    by field
qed

lemma pe_phi_ratio_positive:
  assumes "0 < F_s"
    and "0 < F_i"
  shows "0 < pe_phi_ratio F_s F_i"
  unfolding pe_phi_ratio_def
  using assms
  by positivity

lemma pe_golden_ratio_positive:
  shows "0 < pe_golden_ratio"
proof -
  have "0 < sqrt 5"
    by simp
  then show ?thesis
    unfolding pe_golden_ratio_def
    by linarith
qed

theorem pe_portal_equilibrium_law_contract:
  assumes "F_s * phi \<noteq> 0"
  shows "pe_five_force_balance F_g F_s F_i F_a (-(F_g + F_s + F_i + F_a))
    \<and> pe_portal_state F_s F_i
      (pe_predicted_acoustic_force F_s F_i phi) phi = 1"
proof (intro conjI)
  show "pe_five_force_balance F_g F_s F_i F_a (-(F_g + F_s + F_i + F_a))"
    by (rule pe_five_force_balance_by_counterterm)
  show "pe_portal_state F_s F_i
      (pe_predicted_acoustic_force F_s F_i phi) phi = 1"
    using assms
    by (rule pe_portal_state_one_from_predicted_acoustic_force)
qed

end
'''
    (ISABELLE_DIR / "TZPID_PortalEquilibrium_Laws.thy").write_text(theory, encoding="utf-8")
    root = ROOT_FILE.read_text(encoding="utf-8")
    name = "    TZPID_PortalEquilibrium_Laws"
    if name not in root:
        root = root.replace(
            "    TZPID_PortalBreathing_OccupancyInterface\n    TZPID_ExternalEvidence_Certificates",
            "    TZPID_PortalBreathing_OccupancyInterface\n"
            + name
            + "\n    TZPID_ExternalEvidence_Certificates",
        )
        ROOT_FILE.write_text(root, encoding="utf-8")


def main():
    stamp = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    OUT.mkdir(parents=True, exist_ok=True)
    master_rows = read_csv(MASTER)
    fieldnames = list(master_rows[0].keys())
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
            "formation_note": f"Extracted from {SOURCE_PORTAL} force-vector / phi-equilibrium section. Generated UTC {stamp}.",
            "dictionary": entry["dictionary"],
            "encyclopedia": entry["encyclopedia"],
            "isabelle_kind": entry["kind"],
            "obligation_role": entry["role"],
            "proof_required_checks": "source_traceability;wolfram_certificate;hol_carrier_typing;empirical_validation_pending",
            "gold_spine": "portal_breathing;portal_equilibrium;occupancy_interface",
            "lean_rocq": f"registry_{tzpid}",
            "wolfram_status": "queued;artifact=peer_review/portal_breathing_intake/wolfram/portal_equilibrium_laws_check_results.json",
            "isabelle_sid": str(id_num(tzpid)),
            "uuid": "",
        }
        row["uuid"] = deterministic_uuid(row)
        new_rows.append((row, entry))

    all_rows = master_rows + [row for row, _ in new_rows]
    write_csv(MASTER, all_rows, fieldnames)
    rebuild_master_md(all_rows, fieldnames, stamp)

    dict_rows = read_csv(DICTIONARY)
    dict_fields = list(dict_rows[0].keys())
    dict_rows.extend({"id": row["id"], "title": row["title"], "dictionary_definition": row["dictionary"]} for row, _ in new_rows)
    write_csv(DICTIONARY, dict_rows, dict_fields)

    with ENCYCLOPEDIA.open("a", encoding="utf-8") as handle:
        handle.write("\n\n## Portal Equilibrium Force Laws Intake\n\n")
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
        "source_file": SOURCE_PORTAL,
        "previous_max_id": f"ID{max_id:04d}",
        "new_ids": [row["id"] for row, _ in new_rows],
        "new_count": len(new_rows),
        "new_master_rows": len(all_rows),
        "note": "Literal S4/S5 strings were not found in the saved source files; this pass extracts the saved portal-equilibrium laws.",
    }
    (OUT / "PORTAL_EQUILIBRIUM_LAWS_INTAKE_REPORT.json").write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
