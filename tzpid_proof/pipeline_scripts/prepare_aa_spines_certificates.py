import argparse
import hashlib
import json
import re
from pathlib import Path

from tzpid_provenance import generated_utc, isabelle_text


DEFAULT_RESULTS = "wolfram_checks/aa_spines_results.json"
DEFAULT_MODULE_SUMMARY = "wolfram_checks/aa_module_library_certification_summary.json"
DEFAULT_OUTPUT_DIR = "isabelle_tzpid"


CONSTRUCTORS = {
    "aa_vortex_curvature_identity": "AA_Vortex_Curvature_Identity",
    "aa_vortex_alfven_positive": "AA_Vortex_Alfven_Positive",
    "aa_vortex_mach_ratio": "AA_Vortex_Mach_Ratio",
    "aa_dna_entropy_floor": "AA_DNA_Entropy_Floor",
    "aa_dna_unitary_identity": "AA_DNA_Unitary_Identity",
    "aa_dna_helix_length": "AA_DNA_Helix_Length",
    "aa_neutrino_enhancement_square": "AA_Neutrino_Enhancement_Square",
    "aa_neutrino_capture_rate_positive": "AA_Neutrino_Capture_Rate_Positive",
    "aa_neutrino_information_log": "AA_Neutrino_Information_Log",
    "aa_qi_kernel_normalization": "AA_QI_Kernel_Normalization",
    "aa_qi_phase_shift_units": "AA_QI_Phase_Shift_Units",
    "aa_qi_decoherence_positive": "AA_QI_Decoherence_Positive",
}


def file_sha1(path):
    digest = hashlib.sha1()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def ascii_clean(value, max_len=500):
    text = "" if value is None else str(value)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = text.replace("\\", "/").replace("''", "'")
    text = re.sub(r"\s+", " ", text).strip()
    return text[:max_len]


def isa_string(value, max_len=500):
    return "''" + ascii_clean(value, max_len=max_len) + "''"


def constructor_for(row):
    check = row.get("check", "")
    if check in CONSTRUCTORS:
        return CONSTRUCTORS[check]
    safe = re.sub(r"[^A-Za-z0-9]+", "_", check).strip("_")
    return "AA_Check_" + safe


def case_body(cases):
    return " | ".join(cases)


def write_theory(path, rows, results_sha, module_summary, module_summary_sha, generated_at):
    constructors = [constructor_for(row) for row in rows]
    datatype_lines = "\n  | ".join(constructors)
    status_cases = []
    id_cases = []
    spine_cases = []
    note_cases = []
    for row in rows:
        ctor = constructor_for(row)
        status_cases.append(f"{ctor} => {isa_string(row.get('status', ''), 80)}")
        id_cases.append(f"{ctor} => {isa_string(row.get('id', ''), 20)}")
        spine_cases.append(f"{ctor} => {isa_string(row.get('spine', ''), 120)}")
        note_cases.append(f"{ctor} => {isa_string(row.get('notes', ''), 700)}")

    pass_lemmas = []
    for row in rows:
        ctor = constructor_for(row)
        lemma_name = re.sub(r"[^a-z0-9]+", "_", row.get("check", "").lower()).strip("_") + "_passed"
        if row.get("status") == "pass":
            pass_lemmas.append(
                f"""lemma {lemma_name}:
  "aa_wolfram_verified_check {ctor}"
  by (simp add: aa_wolfram_verified_check_def aa_wolfram_check_status_def)
"""
            )

    status_counts = module_summary.get("status_counts", {})
    parse_counts = module_summary.get("parse_status_counts", {})
    module_pass = int(status_counts.get("pass", 0))
    module_needs = int(status_counts.get("needs_normalization", 0))
    module_packets = int(status_counts.get("source_packet_normalized", 0))
    parse_ok = int(parse_counts.get("parse_ok", 0))
    parse_failed = int(parse_counts.get("parse_failed", 0))
    source_packet_normalized = int(parse_counts.get("source_packet_normalized", 0))
    module_rows = int(module_summary.get("library_rows", 0))

    provenance = isabelle_text(
        "prepare_aa_spines_certificates.py",
        [
            f"aa spine Wolfram result SHA1 {results_sha}",
            f"AA module summary SHA1 {module_summary_sha}",
        ],
        generated_at,
        "Wolfram-backed certificate layer for Algorithmic-Ambassador spines and module parse lane.",
    )

    text = f"""theory TZPID_AA_Spines_Computational_Checks
  imports TZPID_AA_Spines_Focus
begin

{provenance}

text \\<open>
  Wolfram-backed certificate layer for the Algorithmic-Ambassador gold spines.
\\<close>

datatype aa_wolfram_check =
  {datatype_lines}

definition aa_spines_wolfram_results_sha1 :: string where
  "aa_spines_wolfram_results_sha1 = {isa_string(results_sha)}"

definition aa_module_library_summary_sha1 :: string where
  "aa_module_library_summary_sha1 = {isa_string(module_summary_sha)}"

definition aa_wolfram_check_status :: "aa_wolfram_check => string" where
  "aa_wolfram_check_status check = (case check of {case_body(status_cases)})"

definition aa_wolfram_check_registry_id :: "aa_wolfram_check => string" where
  "aa_wolfram_check_registry_id check = (case check of {case_body(id_cases)})"

definition aa_wolfram_check_spine :: "aa_wolfram_check => string" where
  "aa_wolfram_check_spine check = (case check of {case_body(spine_cases)})"

definition aa_wolfram_check_notes :: "aa_wolfram_check => string" where
  "aa_wolfram_check_notes check = (case check of {case_body(note_cases)})"

definition aa_wolfram_verified_check :: "aa_wolfram_check => bool" where
  "aa_wolfram_verified_check check = (aa_wolfram_check_status check = ''pass'')"

definition aa_module_library_rows :: nat where
  "aa_module_library_rows = {module_rows}"

definition aa_module_library_parse_passes :: nat where
  "aa_module_library_parse_passes = {parse_ok}"

definition aa_module_library_parse_normalization_queue :: nat where
  "aa_module_library_parse_normalization_queue = {parse_failed}"

definition aa_module_library_source_packets :: nat where
  "aa_module_library_source_packets = {source_packet_normalized}"

definition aa_module_library_wolfram_passes :: nat where
  "aa_module_library_wolfram_passes = {module_pass}"

definition aa_module_library_needs_normalization :: nat where
  "aa_module_library_needs_normalization = {module_needs}"

definition aa_module_library_source_packet_statuses :: nat where
  "aa_module_library_source_packet_statuses = {module_packets}"

{chr(10).join(pass_lemmas)}

lemma aa_module_library_partition:
  "aa_module_library_parse_passes + aa_module_library_parse_normalization_queue + aa_module_library_source_packets = aa_module_library_rows"
  by (simp add: aa_module_library_parse_passes_def aa_module_library_parse_normalization_queue_def aa_module_library_source_packets_def aa_module_library_rows_def)

context TZPID_AA_Spines_Focus
begin

theorem aa_vortex_core_spine_has_wolfram_certificate:
  "aa_wolfram_verified_check AA_Vortex_Curvature_Identity
    & aa_wolfram_verified_check AA_Vortex_Alfven_Positive
    & aa_wolfram_verified_check AA_Vortex_Mach_Ratio
    & vortex_core_spine_obligation vortex_curvature
    & vortex_core_spine_obligation vortex_alfven_velocity
    & vortex_core_spine_obligation vortex_mach_functional"
  using aa_vortex_curvature_identity_passed aa_vortex_alfven_positive_passed
    aa_vortex_mach_ratio_passed vortex_core_topological_fluid_dynamics_registered
  by simp

theorem aa_dna_tzpqvs_spine_has_wolfram_certificate:
  "aa_wolfram_verified_check AA_DNA_Entropy_Floor
    & aa_wolfram_verified_check AA_DNA_Unitary_Identity
    & aa_wolfram_verified_check AA_DNA_Helix_Length
    & dna_tzpqvs_spine_obligation dna_entropy_bound
    & dna_tzpqvs_spine_obligation dna_physical_length"
  using aa_dna_entropy_floor_passed aa_dna_unitary_identity_passed aa_dna_helix_length_passed
    dna_tzpqvs_isomorphism_registered
  by simp

theorem aa_neutrino_piezo_spine_has_wolfram_certificate:
  "aa_wolfram_verified_check AA_Neutrino_Enhancement_Square
    & aa_wolfram_verified_check AA_Neutrino_Capture_Rate_Positive
    & aa_wolfram_verified_check AA_Neutrino_Information_Log
    & neutrino_piezo_spine_obligation neutrino_enhancement_ratio
    & neutrino_piezo_spine_obligation neutrino_capture_rate
    & neutrino_piezo_spine_obligation neutrino_information_yield"
  using aa_neutrino_enhancement_square_passed aa_neutrino_capture_rate_positive_passed
    aa_neutrino_information_log_passed neutrino_piezoelectric_coupling_registered
  by simp

theorem aa_quantum_information_curvature_spine_has_wolfram_certificate:
  "aa_wolfram_verified_check AA_QI_Kernel_Normalization
    & aa_wolfram_verified_check AA_QI_Phase_Shift_Units
    & aa_wolfram_verified_check AA_QI_Decoherence_Positive
    & qi_curvature_spine_obligation qi_accumulation_kernel
    & qi_curvature_spine_obligation qi_phase_shift_prediction
    & qi_curvature_spine_obligation qi_decoherence_prediction"
  using aa_qi_kernel_normalization_passed aa_qi_phase_shift_units_passed
    aa_qi_decoherence_positive_passed quantum_information_genesis_of_curvature_registered
  by simp

end

end
"""
    Path(path).write_text(text, encoding="utf-8")


def write_summary(path, rows, results_sha, module_summary, module_summary_sha, generated_at):
    lines = [
        "# Algorithmic-Ambassador Wolfram Certificates",
        "",
        "Project: TZPID Proof Pipeline",
        "Creator: Daniel Alexander Trawin",
        "ORCID: https://orcid.org/0009-0001-4630-3715",
        "Generator: prepare_aa_spines_certificates.py",
        f"Generated UTC: {generated_at}",
        "",
        f"AA spine result SHA1: `{results_sha}`",
        f"AA module summary SHA1: `{module_summary_sha}`",
        "",
        "| ID | Spine | Check | Status | Notes |",
        "|---|---|---|---|---|",
    ]
    for row in rows:
        lines.append(
            f"| {row.get('id', '')} | {ascii_clean(row.get('spine', ''), 120)} | "
            f"`{row.get('check', '')}` | `{row.get('status', '')}` | {ascii_clean(row.get('notes', ''), 240)} |"
        )
    lines.extend(
        [
            "",
            "## Module Library Parse Lane",
            "",
            f"- Rows: `{module_summary.get('library_rows', 0)}`",
            f"- Parse pass: `{module_summary.get('parse_status_counts', {}).get('parse_ok', 0)}`",
            f"- Source-packet normalized: `{module_summary.get('parse_status_counts', {}).get('source_packet_normalized', 0)}`",
            f"- Still parse failed: `{module_summary.get('parse_status_counts', {}).get('parse_failed', 0)}`",
        ]
    )
    Path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")


def update_root(root_path):
    root = Path(root_path)
    text = root.read_text(encoding="utf-8")
    theory = "TZPID_AA_Spines_Computational_Checks"
    if theory not in text:
        text = text.rstrip() + f"\n    {theory}\n"
    root.write_text(text, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Generate Isabelle certificates for AA Wolfram spine checks.")
    parser.add_argument("--results", default=DEFAULT_RESULTS)
    parser.add_argument("--module-summary", default=DEFAULT_MODULE_SUMMARY)
    parser.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()

    rows = json.loads(Path(args.results).read_text(encoding="utf-8"))
    module_summary = json.loads(Path(args.module_summary).read_text(encoding="utf-8"))
    results_sha = file_sha1(args.results)
    module_summary_sha = file_sha1(args.module_summary)
    generated_at = generated_utc()
    out = Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)
    write_theory(out / "TZPID_AA_Spines_Computational_Checks.thy", rows, results_sha, module_summary, module_summary_sha, generated_at)
    write_summary(out / "aa_spines_wolfram_certificate_summary.md", rows, results_sha, module_summary, module_summary_sha, generated_at)
    update_root(out / "ROOT")
    print("Wrote AA spine Isabelle certificate theory")


if __name__ == "__main__":
    main()
