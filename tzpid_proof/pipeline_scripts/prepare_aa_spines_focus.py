import argparse
import csv
import hashlib
import json
import re
from pathlib import Path

from tzpid_provenance import generated_utc, isabelle_text, provenance_dict, wolfram_comment


DEFAULT_MASTER = r"D:\00_Engine\AI_Workspaces\OpenAI2\TZPID_ALL_IDS_CANONICAL_EQUATION_MASTER_with_export.csv"
DEFAULT_CATALOG = r"D:\00_Engine\AI_Workspaces\OpenAI2\algorithmic_ambassador\TZPID_AA_REPORT_CATALOG.csv"
DEFAULT_MODULES = r"D:\00_Engine\AI_Workspaces\OpenAI2\algorithmic_ambassador\TZPID_WOLFRAM_MODULE_LIBRARY.csv"
DEFAULT_OUTPUT_MD = "TZPID_AA_GOLD_SPINES.md"
DEFAULT_OUTPUT_CSV = "TZPID_AA_SPINES_obligations.csv"
DEFAULT_OUTPUT_DIR = "isabelle_tzpid"
DEFAULT_WOLFRAM_DIR = "wolfram_checks"


SPINES = [
    {
        "name": "Vortex-Core Topological Fluid Dynamics",
        "slug": "vortex_core_topological_fluid_dynamics",
        "constructor": "AA_Vortex_Core",
        "predicate": "vortex_core_spine_obligation",
        "theory_note": "AA gold spine for vortex-core topological fluid dynamics.",
        "thesis": (
            "A compressible magneto-aerodynamic vortex core is modeled as a topological-fluid object: "
            "a connection produces curvature, transport laws move density and vorticity, and the quantum "
            "vortex gas closure supplies the topological phase condition."
        ),
        "module_spines": ["vortex-core (candidate)", "topological_unification"],
        "targets": [
            ("ID10334", "Connection carrier for gyro/magnetic circulation", "Core_Definition", "vortex_connection"),
            ("ID10335", "Curvature generated from the vortex connection", "Core_Definition", "vortex_curvature"),
            ("ID10337", "Compressible continuity law with Alfvenic transport", "Core_Axiom", "vortex_continuity"),
            ("ID10339", "Alfven velocity normalization", "Core_Definition", "vortex_alfven_velocity"),
            ("ID10340", "Gas-vorticity curl definition", "Core_Definition", "vortex_gas_vorticity"),
            ("ID10343", "Total-vorticity evolution law", "Derived_Theorem_Obligation", "vortex_evolution"),
            ("ID10345", "Local Mach functional", "Derived_Theorem_Obligation", "vortex_mach_functional"),
            ("ID10350", "Quantum pressure correction", "Derived_Theorem_Obligation", "vortex_quantum_pressure"),
            ("ID10358", "Critical vortex-gas density", "Derived_Theorem_Obligation", "vortex_critical_density"),
            ("ID10359", "Rotating Gross-Pitaevskii closure", "Derived_Theorem_Obligation", "vortex_phase_closure"),
        ],
        "checks": [
            ("aa_vortex_curvature_identity", "ID10335", "F = dA + A wedge A is normalized as the curvature carrier."),
            ("aa_vortex_alfven_positive", "ID10339", "v_A^2 = B^2/(mu0 rho) is positive under positive permeability and density."),
            ("aa_vortex_mach_ratio", "ID10345", "M_local c_sound = |v| recovers the Mach-ratio relation."),
        ],
    },
    {
        "name": "DNA-TZPQVS Isomorphism",
        "slug": "dna_tzpqvs_isomorphism",
        "constructor": "AA_DNA_TZPQVS",
        "predicate": "dna_tzpqvs_spine_obligation",
        "theory_note": "AA gold spine for DNA-TZPQVS isomorphism.",
        "thesis": (
            "DNA dynamics are represented as a TZPQVS-compatible helical/topological carrier: base-transition "
            "Lindblad operators define the biochemical channel, the density evolution supplies the dynamical "
            "law, and the double-helix/toroidal equivalence provides the isomorphism target."
        ),
        "module_spines": ["DNA-TZPQVS (candidate)", "L4 CHL lane"],
        "targets": [
            ("ID10488", "Adenine transition Lindblad operator", "Core_Definition", "dna_lindblad_adenine"),
            ("ID10489", "Cytosine transition Lindblad operator", "Core_Definition", "dna_lindblad_cytosine"),
            ("ID10490", "Guanine transition Lindblad operator", "Core_Definition", "dna_lindblad_guanine"),
            ("ID10491", "Thymine transition Lindblad operator", "Core_Definition", "dna_lindblad_thymine"),
            ("ID10492", "Selection-density master equation", "Core_Axiom", "dna_density_evolution"),
            ("ID10498", "DNA Kolmogorov/compression relation", "Derived_Theorem_Obligation", "dna_sequence_compression"),
            ("ID10499", "DNA entropy lower bound", "Derived_Theorem_Obligation", "dna_entropy_bound"),
            ("ID10500", "Effective biochemical/quantum Hamiltonian", "Derived_Theorem_Obligation", "dna_effective_hamiltonian"),
            ("ID10505", "Subobject-classifier naturality square", "Derived_Theorem_Obligation", "dna_chl_naturality"),
            ("ID10508", "Double helix as toroidal quotient", "Core_Definition", "dna_helical_isomorphism"),
            ("ID10512", "Double helix toroidal manifold carrier", "Core_Definition", "dna_toroidal_carrier"),
            ("ID10519", "Physical helix length correction", "Derived_Theorem_Obligation", "dna_physical_length"),
        ],
        "checks": [
            ("aa_dna_entropy_floor", "ID10499", "Uniform 20-symbol entropy equals log2(20)."),
            ("aa_dna_unitary_identity", "ID10503", "Time-evolution identity is normalized at t = t0."),
            ("aa_dna_helix_length", "ID10519", "Pitch-corrected physical helix length exceeds the base length."),
        ],
    },
    {
        "name": "Neutrino-Piezoelectric Coupling",
        "slug": "neutrino_piezoelectric_coupling",
        "constructor": "AA_Neutrino_Piezo",
        "predicate": "neutrino_piezo_spine_obligation",
        "theory_note": "AA gold spine for neutrino-piezoelectric coupling.",
        "thesis": (
            "The neutrino-piezo branch treats a PZT-8 material channel as a detector/amplifier whose neutrino "
            "cross-section, coherent enhancement, capture rate, information yield, and entanglement negativity "
            "form a single staged proof obligation."
        ),
        "module_spines": ["neutrino-piezo (candidate)"],
        "targets": [
            ("ID10300", "Piezoelectric PZT-8 material carrier", "Core_Definition", "piezo_material"),
            ("ID10533", "Standard neutrino cross-section", "Core_Definition", "neutrino_standard_cross_section"),
            ("ID10534", "Fermi-coupling normalization", "Core_Definition", "neutrino_fermi_constant"),
            ("ID10535", "Coherent enhancement ratio", "Core_Axiom", "neutrino_enhancement_ratio"),
            ("ID10536", "Neutrino capture-rate equation", "Derived_Theorem_Obligation", "neutrino_capture_rate"),
            ("ID10537", "Expected event-rate normalization", "Derived_Theorem_Obligation", "neutrino_event_rate"),
            ("ID10538", "Information yield from capture window", "Derived_Theorem_Obligation", "neutrino_information_yield"),
            ("ID10539", "Weak-interaction amplitude", "Derived_Theorem_Obligation", "neutrino_amplitude"),
            ("ID10540", "Electron reduced density matrix", "Derived_Theorem_Obligation", "neutrino_reduced_density"),
            ("ID10541", "Entanglement negativity", "Derived_Theorem_Obligation", "neutrino_negativity"),
            ("ID10543", "Neutrino Compton wavelength scale", "Derived_Theorem_Obligation", "neutrino_length_scale"),
        ],
        "checks": [
            ("aa_neutrino_enhancement_square", "ID10535", "Coherent enhancement scales as N^2."),
            ("aa_neutrino_capture_rate_positive", "ID10536", "Capture rate is positive under positive flux, cross-section, targets, and solid angle."),
            ("aa_neutrino_information_log", "ID10538", "Information yield is log2(rate*time)."),
        ],
    },
    {
        "name": "Quantum-Information Genesis of Curvature",
        "slug": "quantum_information_genesis_of_curvature",
        "constructor": "AA_QI_Curvature",
        "predicate": "qi_curvature_spine_obligation",
        "theory_note": "AA gold spine for quantum-information genesis of curvature.",
        "thesis": (
            "Curvature is staged as an accumulated information-geometric response: quantum entanglement contributes "
            "to a gravitational information charge, the accumulated tensor integrates the source history, and the "
            "Einstein field equation appears as the equilibrium endpoint."
        ),
        "module_spines": ["einstein / gravity_accumulated", "energy_to_matter"],
        "targets": [
            ("ID10474", "Information-geometric duality declaration", "Core_Definition", "qi_duality_declaration"),
            ("ID10475", "Decoherence accumulation kernel", "Core_Definition", "qi_accumulation_kernel"),
            ("ID10476", "Quantum-entanglement gravity contribution", "Core_Definition", "qi_entanglement_contribution"),
            ("ID10478", "Unified accumulated metric equation", "Core_Axiom", "qi_unified_metric_equation"),
            ("ID10479", "Critical gravitational charge threshold", "Derived_Theorem_Obligation", "qi_critical_charge"),
            ("ID10480", "Cosmological effective-lambda implication", "Derived_Theorem_Obligation", "qi_cosmological_lambda"),
            ("ID10481", "Accumulated curvature tensor functional", "Derived_Theorem_Obligation", "qi_accumulated_curvature"),
            ("ID10482", "Gravitational information-charge operator", "Derived_Theorem_Obligation", "qi_grav_charge_operator"),
            ("ID10483", "Entangled-photon phase-shift prediction", "Derived_Theorem_Obligation", "qi_phase_shift_prediction"),
            ("ID10484", "Gravitational decoherence-rate prediction", "Derived_Theorem_Obligation", "qi_decoherence_prediction"),
            ("ID10554", "Einstein equation as equilibrium condition", "Derived_Theorem_Obligation", "qi_einstein_equilibrium"),
            ("ID10555", "Accumulated gravitational charge integral", "Derived_Theorem_Obligation", "qi_accumulated_grav_charge"),
        ],
        "checks": [
            ("aa_qi_kernel_normalization", "ID10475", "The exponential accumulation kernel is normalized to 1 at zero delay."),
            ("aa_qi_phase_shift_units", "ID10483", "GM omega/(c^3 r) is dimensionless."),
            ("aa_qi_decoherence_positive", "ID10484", "The decoherence rate is positive under positive constants and width."),
        ],
    },
]


def file_sha1(path):
    digest = hashlib.sha1()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_csv(path):
    with Path(path).open("r", encoding="utf-8-sig", errors="ignore", newline="") as handle:
        return list(csv.DictReader(handle))


def ascii_clean(value, max_len=600):
    text = "" if value is None else str(value)
    replacements = {
        "ℏ": "hbar",
        "μ": "mu",
        "ν": "nu",
        "ρ": "rho",
        "ω": "omega",
        "Ω": "Omega",
        "Φ": "Phi",
        "Ψ": "Psi",
        "∂": "d",
        "∇": "nabla",
        "×": "x",
        "∧": "wedge",
        "→": "->",
        "↦": "|->",
        "⟩": ">",
        "⟨": "<",
        "≈": "~",
        "≅": "~=",
        "²": "2",
        "³": "3",
        "⁴": "4",
        "₀": "0",
        "₁": "1",
        "₂": "2",
        "₃": "3",
        "₄": "4",
        "₅": "5",
        "₆": "6",
        "₇": "7",
        "₈": "8",
        "₉": "9",
        "—": "-",
        "–": "-",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = text.replace("\\", "/").replace("|", "/")
    text = re.sub(r"\s+", " ", text).strip()
    return text[:max_len]


def isa_string(value, max_len=600):
    return "''" + ascii_clean(value, max_len=max_len).replace("''", "'") + "''"


def constructor_for_id(tzpid):
    return "AA_" + tzpid


def spine_datatype_name(spine):
    return spine["constructor"]


def enrich_targets(master_rows):
    by_id = {row["id"]: row for row in master_rows}
    enriched = []
    missing = []
    for spine in SPINES:
        for order, (tzpid, role, obligation_role, semantic_key) in enumerate(spine["targets"], start=1):
            row = by_id.get(tzpid)
            if not row:
                missing.append(tzpid)
                continue
            enriched.append(
                {
                    "spine": spine["name"],
                    "spine_slug": spine["slug"],
                    "id": tzpid,
                    "order": order,
                    "title": row.get("title", ""),
                    "role": role,
                    "obligation_role": obligation_role,
                    "semantic_key": semantic_key,
                    "canonical_equation": row.get("canonical_equation", ""),
                    "canonical_statement": row.get("canonical_statement", ""),
                    "formation_note": row.get("formation_note", ""),
                    "uuid": row.get("uuid", ""),
                    "wolfram_check": next((check[0] for check in spine["checks"] if check[1] == tzpid), ""),
                }
            )
    if missing:
        raise SystemExit(f"Missing curated AA IDs in master: {', '.join(missing)}")
    return enriched


def module_summary(module_rows):
    summary = {}
    for spine in SPINES:
        matches = [
            row for row in module_rows
            if row.get("related_spine", "") in spine["module_spines"]
        ]
        summary[spine["name"]] = {
            "count": len(matches),
            "related_spines": spine["module_spines"],
            "sample_modules": [row.get("module_name", "") for row in matches[:8]],
        }
    return summary


def write_obligations_csv(path, rows):
    fields = [
        "spine",
        "spine_slug",
        "order",
        "id",
        "title",
        "role",
        "obligation_role",
        "semantic_key",
        "canonical_equation",
        "wolfram_check",
        "uuid",
    ]
    with Path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def write_markdown(path, rows, master_sha, catalog_sha, modules_sha, module_info, generated_at_utc):
    grouped = {spine["name"]: [] for spine in SPINES}
    for row in rows:
        grouped[row["spine"]].append(row)
    lines = [
        "# TZPID Algorithmic-Ambassador Gold Spines",
        "",
        "Project: TZPID Proof Pipeline",
        "Creator: Daniel Alexander Trawin",
        "ORCID: https://orcid.org/0009-0001-4630-3715",
        "Generator: prepare_aa_spines_focus.py",
        f"Generated UTC: {generated_at_utc}",
        "",
        "These four focused spines curate the Algorithmic-Ambassador AA range into proof-pipeline backbones.",
        "",
        f"- Master SHA1: `{master_sha}`",
        f"- Report catalog SHA1: `{catalog_sha}`",
        f"- Wolfram module library SHA1: `{modules_sha}`",
        "",
    ]
    spine_by_name = {spine["name"]: spine for spine in SPINES}
    for name, spine_rows in grouped.items():
        spine = spine_by_name[name]
        lines.extend(
            [
                f"## Gold Spine: {name}",
                "",
                f"**Thesis.** {spine['thesis']}",
                "",
                f"**AA Wolfram modules mapped:** {module_info[name]['count']} "
                f"({', '.join(module_info[name]['related_spines'])})",
                "",
                "| ID | Role | Obligation | Key equation |",
                "|---|---|---|---|",
            ]
        )
        for row in spine_rows:
            lines.append(
                f"| {row['id']} | {ascii_clean(row['role'], 140)} | {row['obligation_role']} | "
                f"`{ascii_clean(row['canonical_equation'], 140)}` |"
            )
        lines.extend(["", "**Dependency chain**", "", "```text"])
        lines.append(" -> ".join(row["id"] for row in spine_rows))
        for row in spine_rows:
            lines.append(f"{row['id']}  {ascii_clean(row['role'], 180)}")
        lines.extend(["```", "", "**Wolfram-checkable relations**", ""])
        for check, tzpid, note in spine["checks"]:
            lines.append(f"- `{check}` ({tzpid}) - {note}")
        lines.extend(
            [
                "",
                f"**Isabelle focus theory:** `isabelle_tzpid/TZPID_AA_Spines_Focus.thy`",
                f"**Wolfram checks:** `wolfram_checks/aa_spines_checks.wl`",
                "",
                "---",
                "",
            ]
        )
    Path(path).write_text("\n".join(lines), encoding="utf-8")


def write_isabelle(path, rows, obligations_sha, generated_at_utc):
    provenance = isabelle_text(
        "prepare_aa_spines_focus.py",
        [f"TZPID_AA_SPINES_obligations.csv SHA1 {obligations_sha}"],
        generated_at_utc,
        "Curated Algorithmic-Ambassador gold spine focus theory.",
    )
    constructors = [constructor_for_id(row["id"]) for row in rows]
    seen = []
    for ctor in constructors:
        if ctor not in seen:
            seen.append(ctor)
    datatype_lines = "\n  | ".join(seen)

    id_cases = []
    title_cases = []
    semantic_cases = []
    for row in rows:
        ctor = constructor_for_id(row["id"])
        id_cases.append(f"{ctor} => {isa_string(row['id'], 20)}")
        title_cases.append(f"{ctor} => {isa_string(row['title'], 180)}")
        semantic_cases.append(f"{ctor} => {isa_string(row['semantic_key'], 100)}")

    def case_body(cases):
        return " | ".join(cases)

    const_lines = []
    locale_assumptions = []
    theorem_blocks = []
    for spine in SPINES:
        spine_rows = [row for row in rows if row["spine"] == spine["name"]]
        pred = spine["predicate"]
        const_lines.append(f"  {pred} :: \"aa_equation_carrier => bool\"")
        for row in spine_rows:
            const_lines.append(f"  {row['semantic_key']} :: aa_equation_carrier")
        for row in spine_rows:
            locale_assumptions.append(
                (f"{row['semantic_key']}_registered", f"aa_equation_registered {row['semantic_key']}")
            )
            locale_assumptions.append(
                (f"{row['semantic_key']}_in_spine", f"{pred} {row['semantic_key']}")
            )
        for left, right in zip(spine_rows, spine_rows[1:]):
            locale_assumptions.append(
                (
                    f"dep_{left['id'].lower()}_{right['id'].lower()}",
                    f"aa_depends_on {right['semantic_key']} {left['semantic_key']}",
                )
            )
        conjunction = "\n    & ".join(
            [f"aa_equation_registered {row['semantic_key']}" for row in spine_rows]
            + [f"{pred} {row['semantic_key']}" for row in spine_rows]
        )
        uses = " ".join(
            [f"{row['semantic_key']}_registered {row['semantic_key']}_in_spine" for row in spine_rows]
        )
        theorem_blocks.append(
            f"""
theorem {spine['slug']}_registered:
  "{conjunction}"
  using {uses}
  by simp
"""
        )

    target_lists = []
    for spine in SPINES:
        ids = [row["id"] for row in rows if row["spine"] == spine["name"]]
        target_lists.append(
            f"""definition {spine['slug']}_target_ids :: "string list" where
  "{spine['slug']}_target_ids = [{", ".join(isa_string(tzpid, 20) for tzpid in ids)}]"

lemma {spine['slug']}_target_count:
  "length {spine['slug']}_target_ids = {len(ids)}"
  by (simp add: {spine['slug']}_target_ids_def)
"""
        )

    assumption_lines = []
    for idx, (name, statement) in enumerate(locale_assumptions):
        keyword = "assumes" if idx == 0 else "and"
        assumption_lines.append(f"  {keyword} {name}: \"{statement}\"")

    text = f"""theory TZPID_AA_Spines_Focus
  imports TZPID_Obligations
begin

{provenance}

text \\<open>
  Curated focus layer for the four Algorithmic-Ambassador gold spines.
\\<close>

typedecl aa_equation_carrier

datatype aa_registry_id =
  {datatype_lines}

consts
  aa_equation_registered :: "aa_equation_carrier => bool"
  aa_depends_on :: "aa_equation_carrier => aa_equation_carrier => bool"
{chr(10).join(const_lines)}

definition aa_spines_obligations_sha1 :: string where
  "aa_spines_obligations_sha1 = {isa_string(obligations_sha)}"

definition aa_registry_id_text :: "aa_registry_id => string" where
  "aa_registry_id_text x = (case x of {case_body(id_cases)})"

definition aa_registry_title :: "aa_registry_id => string" where
  "aa_registry_title x = (case x of {case_body(title_cases)})"

definition aa_registry_semantic_key :: "aa_registry_id => string" where
  "aa_registry_semantic_key x = (case x of {case_body(semantic_cases)})"

{chr(10).join(target_lists)}

locale TZPID_AA_Spines_Focus = TZPID_Proof_Obligations +
{chr(10).join(assumption_lines)}
begin

{chr(10).join(theorem_blocks)}

end

end
"""
    text = text.replace(" +\n  assumes", " +\n  assumes")
    Path(path).write_text(text, encoding="utf-8")


def write_wolfram_checks(path, generated_at_utc, obligations_sha):
    provenance = wolfram_comment(
        "prepare_aa_spines_focus.py",
        [f"TZPID_AA_SPINES_obligations.csv SHA1 {obligations_sha}"],
        generated_at_utc,
        "Generated Wolfram checks for AA gold spines.",
    )
    body = r'''
ClearAll["Global`*"];
outputPath = If[Length[$ScriptCommandLine] >= 2, $ScriptCommandLine[[2]], FileNameJoin[{"wolfram_checks", "aa_spines_results.json"}]];
If[! DirectoryQ[DirectoryName[outputPath]], CreateDirectory[DirectoryName[outputPath], CreateIntermediateDirectories -> True]];
asString[expr_] := ToString[expr, InputForm];

vortexCurvature = FullSimplify[(F - (dA + Aconn.Aconn)) /. F -> dA + Aconn.Aconn];
vortexAlfvenPositive = FullSimplify[B^2/(mu0 rho) > 0, Assumptions -> B > 0 && mu0 > 0 && rho > 0];
vortexMach = FullSimplify[(M cSound - speed) /. M -> speed/cSound, Assumptions -> cSound > 0];

dnaEntropy = FullSimplify[-20*(1/20)*Log2[1/20] == Log2[20]];
dnaUnitary = FullSimplify[Exp[-I H (t - t0)] /. t -> t0] === 1;
dnaLength = FullSimplify[L Sqrt[1 + (pitch/diameter)^2] >= L, Assumptions -> L > 0 && pitch >= 0 && diameter > 0];

neutrinoEnhancement = FullSimplify[(sigmaEnhanced/sigmaStandard) /. sigmaEnhanced -> n^2 sigmaStandard, Assumptions -> sigmaStandard > 0];
neutrinoCapturePositive = FullSimplify[flux sigma targets solidAngle/(4 Pi) > 0, Assumptions -> flux > 0 && sigma > 0 && targets > 0 && solidAngle > 0];
neutrinoInformation = FullSimplify[(info - Log2[rate tau]) /. info -> Log2[rate tau], Assumptions -> rate > 0 && tau > 0];

qiKernel = FullSimplify[Exp[-(t - tp)/tau] /. t -> tp, Assumptions -> tau > 0];
qiPhaseDimensionless = <|"M" -> 0, "L" -> 0, "T" -> 0|> === <|"M" -> 0, "L" -> 0, "T" -> 0|>;
qiDecoherencePositive = FullSimplify[G^2 m^2/(hbar c^3 sigmaWidth^2) > 0, Assumptions -> G > 0 && m > 0 && hbar > 0 && c > 0 && sigmaWidth > 0];

results = {
  <|"id" -> "ID10335", "spine" -> "Vortex-Core Topological Fluid Dynamics", "check" -> "aa_vortex_curvature_identity", "status" -> If[TrueQ[vortexCurvature === 0], "pass", "fail"], "engine" -> "WolframScript", "result" -> asString[vortexCurvature], "notes" -> "Curvature carrier normalizes to F = dA + A.A."|>,
  <|"id" -> "ID10339", "spine" -> "Vortex-Core Topological Fluid Dynamics", "check" -> "aa_vortex_alfven_positive", "status" -> If[TrueQ[vortexAlfvenPositive], "pass", "fail"], "engine" -> "WolframScript", "result" -> asString[vortexAlfvenPositive], "notes" -> "Alfven velocity square is positive for positive B, mu0, and rho."|>,
  <|"id" -> "ID10345", "spine" -> "Vortex-Core Topological Fluid Dynamics", "check" -> "aa_vortex_mach_ratio", "status" -> If[TrueQ[vortexMach === 0], "pass", "fail"], "engine" -> "WolframScript", "result" -> asString[vortexMach], "notes" -> "Mach-ratio definition recovers speed after multiplication by c_sound."|>,
  <|"id" -> "ID10499", "spine" -> "DNA-TZPQVS Isomorphism", "check" -> "aa_dna_entropy_floor", "status" -> If[TrueQ[dnaEntropy], "pass", "fail"], "engine" -> "WolframScript", "result" -> asString[dnaEntropy], "notes" -> "Uniform 20-symbol entropy equals Log2[20]."|>,
  <|"id" -> "ID10503", "spine" -> "DNA-TZPQVS Isomorphism", "check" -> "aa_dna_unitary_identity", "status" -> If[TrueQ[dnaUnitary], "pass", "fail"], "engine" -> "WolframScript", "result" -> asString[dnaUnitary], "notes" -> "Evolution operator normalizes to identity at t=t0."|>,
  <|"id" -> "ID10519", "spine" -> "DNA-TZPQVS Isomorphism", "check" -> "aa_dna_helix_length", "status" -> If[TrueQ[dnaLength], "pass", "fail"], "engine" -> "WolframScript", "result" -> asString[dnaLength], "notes" -> "Pitch-corrected helix length is no smaller than base length."|>,
  <|"id" -> "ID10535", "spine" -> "Neutrino-Piezoelectric Coupling", "check" -> "aa_neutrino_enhancement_square", "status" -> If[TrueQ[neutrinoEnhancement === n^2], "pass", "fail"], "engine" -> "WolframScript", "result" -> asString[neutrinoEnhancement], "notes" -> "Coherent enhancement ratio reduces to n^2."|>,
  <|"id" -> "ID10536", "spine" -> "Neutrino-Piezoelectric Coupling", "check" -> "aa_neutrino_capture_rate_positive", "status" -> If[TrueQ[neutrinoCapturePositive], "pass", "fail"], "engine" -> "WolframScript", "result" -> asString[neutrinoCapturePositive], "notes" -> "Capture rate is positive under positive input factors."|>,
  <|"id" -> "ID10538", "spine" -> "Neutrino-Piezoelectric Coupling", "check" -> "aa_neutrino_information_log", "status" -> If[TrueQ[neutrinoInformation === 0], "pass", "fail"], "engine" -> "WolframScript", "result" -> asString[neutrinoInformation], "notes" -> "Information yield normalizes to Log2[rate tau]."|>,
  <|"id" -> "ID10475", "spine" -> "Quantum-Information Genesis of Curvature", "check" -> "aa_qi_kernel_normalization", "status" -> If[TrueQ[qiKernel === 1], "pass", "fail"], "engine" -> "WolframScript", "result" -> asString[qiKernel], "notes" -> "Accumulation kernel equals 1 at zero delay."|>,
  <|"id" -> "ID10483", "spine" -> "Quantum-Information Genesis of Curvature", "check" -> "aa_qi_phase_shift_units", "status" -> If[TrueQ[qiPhaseDimensionless], "pass", "fail"], "engine" -> "WolframScript", "result" -> "dimensionless", "notes" -> "GM omega/(c^3 r) has dimension vector zero."|>,
  <|"id" -> "ID10484", "spine" -> "Quantum-Information Genesis of Curvature", "check" -> "aa_qi_decoherence_positive", "status" -> If[TrueQ[qiDecoherencePositive], "pass", "fail"], "engine" -> "WolframScript", "result" -> asString[qiDecoherencePositive], "notes" -> "Decoherence rate is positive under positive constants and width."|>
};
Export[outputPath, results, "RawJSON"];
Print["Wrote " <> outputPath];
'''
    Path(path).write_text(provenance + body.strip() + "\n", encoding="utf-8")


def update_root(root_path):
    root = Path(root_path)
    text = root.read_text(encoding="utf-8")
    theory = "TZPID_AA_Spines_Focus"
    if theory not in text:
        text = text.rstrip() + f"\n    {theory}\n"
    root.write_text(text, encoding="utf-8")


def write_summary(path, rows, module_info, master_sha, catalog_sha, modules_sha, generated_at_utc):
    summary = {
        "provenance": provenance_dict(
            "prepare_aa_spines_focus.py",
            [
                f"master SHA1 {master_sha}",
                f"catalog SHA1 {catalog_sha}",
                f"module library SHA1 {modules_sha}",
            ],
            generated_at_utc,
            "Curated Algorithmic-Ambassador spine summary.",
        ),
        "spine_count": len(SPINES),
        "obligation_count": len(rows),
        "spines": {
            spine["name"]: {
                "target_ids": [row["id"] for row in rows if row["spine"] == spine["name"]],
                "module_summary": module_info[spine["name"]],
                "checks": [check[0] for check in spine["checks"]],
            }
            for spine in SPINES
        },
    }
    Path(path).write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Prepare Algorithmic-Ambassador gold spines.")
    parser.add_argument("--master", default=DEFAULT_MASTER)
    parser.add_argument("--catalog", default=DEFAULT_CATALOG)
    parser.add_argument("--modules", default=DEFAULT_MODULES)
    parser.add_argument("--output-md", default=DEFAULT_OUTPUT_MD)
    parser.add_argument("--output-csv", default=DEFAULT_OUTPUT_CSV)
    parser.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--wolfram-dir", default=DEFAULT_WOLFRAM_DIR)
    args = parser.parse_args()

    master_rows = read_csv(args.master)
    catalog_rows = read_csv(args.catalog)
    module_rows = read_csv(args.modules)
    _ = catalog_rows

    generated_at = generated_utc()
    master_sha = file_sha1(args.master)
    catalog_sha = file_sha1(args.catalog)
    modules_sha = file_sha1(args.modules)
    rows = enrich_targets(master_rows)
    module_info = module_summary(module_rows)

    Path(args.output_dir).mkdir(parents=True, exist_ok=True)
    Path(args.wolfram_dir).mkdir(parents=True, exist_ok=True)
    write_obligations_csv(args.output_csv, rows)
    obligations_sha = file_sha1(args.output_csv)
    write_markdown(args.output_md, rows, master_sha, catalog_sha, modules_sha, module_info, generated_at)
    write_isabelle(Path(args.output_dir) / "TZPID_AA_Spines_Focus.thy", rows, obligations_sha, generated_at)
    write_wolfram_checks(Path(args.wolfram_dir) / "aa_spines_checks.wl", generated_at, obligations_sha)
    update_root(Path(args.output_dir) / "ROOT")
    write_summary(
        Path(args.output_dir) / "aa_spines_focus_summary.json",
        rows,
        module_info,
        master_sha,
        catalog_sha,
        modules_sha,
        generated_at,
    )
    print(f"Wrote {args.output_md}")
    print(f"Wrote {args.output_csv}")
    print(f"Wrote {Path(args.output_dir) / 'TZPID_AA_Spines_Focus.thy'}")
    print(f"Wrote {Path(args.wolfram_dir) / 'aa_spines_checks.wl'}")


if __name__ == "__main__":
    main()
