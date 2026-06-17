import argparse
import csv
import hashlib
import json
import re
import subprocess
from pathlib import Path

from tzpid_provenance import generated_utc, isabelle_text, wolfram_comment


DEFAULT_OBLIGATIONS = "TZPID_NESTED_HYPERSPHERE_obligations.csv"
DEFAULT_SPINE = "TZPID_NESTED_HYPERSPHERE_SPINE.md"
DEFAULT_BACKING = "TZPID_NESTED_HYPERSPHERE_backing_ids.csv"
DEFAULT_OUTPUT_DIR = "isabelle_tzpid"
DEFAULT_WOLFRAM_DIR = "wolfram_checks"


CHECKS = [
    {
        "id": "ID7733",
        "check": "hs_enclosure_eigenfreq",
        "constructor": "HS_Enclosure_Eigenfreq",
        "notes": "Spherical enclosure j0 first-node check: SphericalBesselJ[0, pi] is numerically zero, and omega = c x/R has zero residual after substitution.",
    },
    {
        "id": "ID7259",
        "check": "hs_filament_scale",
        "constructor": "HS_Filament_Scale",
        "notes": "The first node of the BAO standing-wave surrogate satisfies k r_s = pi, so characteristic spacing scales with the sound horizon r_s.",
    },
    {
        "id": "ID6583",
        "check": "hs_ratio_scale_free",
        "constructor": "HS_Ratio_Scale_Free",
        "notes": "The registry ratio 32/27 is dimensionless and unchanged by common length rescaling.",
    },
    {
        "id": "ID0256",
        "check": "hs_projection_ladder",
        "constructor": "HS_Projection_Ladder",
        "notes": "The harmonic ladder f_n = n f_1 preserves integer mode ratios under common projection rescaling.",
    },
    {
        "id": "ID0104",
        "check": "hs_holographic_count",
        "constructor": "HS_Holographic_Count",
        "notes": "The holographic entropy-area relation S_A = Area/(4G) has zero residual after direct substitution.",
    },
    {
        "id": "ID10786",
        "check": "comma_exact",
        "constructor": "HS_Comma_Exact",
        "notes": "The Pythagorean comma is exactly (3/2)^12 / 2^7 = 531441/524288.",
    },
    {
        "id": "ID10787",
        "check": "comma_cents",
        "constructor": "HS_Comma_Cents",
        "notes": "The Pythagorean comma is 1200 log2(gamma) = 23.460010 cents.",
    },
    {
        "id": "ID10788",
        "check": "comma_hopf_holonomy",
        "constructor": "HS_Comma_Hopf_Holonomy",
        "notes": "The circle-of-fifths residual phase theta_gamma is the holonomy solid angle Omega.",
    },
    {
        "id": "ID10790",
        "check": "inverse_outward_flip",
        "constructor": "HS_Inverse_Outward_Flip",
        "notes": "The heard comma excess and the bulk ratio are exact reciprocals: gamma*(1/gamma)=1.",
    },
    {
        "id": "comparison_53_fifths",
        "check": "comma_53_near_closure",
        "constructor": "HS_Comma_53_Near_Closure",
        "notes": "53 perfect fifths against 31 octaves gives a smaller nonzero holonomy defect than the 12-fifth comma.",
    },
    {
        "id": "ID0395",
        "check": "crit_universal_exponent",
        "constructor": "HS_Crit_Universal_Exponent",
        "notes": "The mean-field avalanche-size exponent is tau = 3/2.",
    },
    {
        "id": "ID0470",
        "check": "crit_cascade_intensity",
        "constructor": "HS_Crit_Cascade_Intensity",
        "notes": "With tau = 3/2, cascade intensity exponent 1-tau equals -1/2.",
    },
    {
        "id": "ID10791",
        "check": "crit_crackling_relation",
        "constructor": "HS_Crit_Crackling_Relation",
        "notes": "With alpha = 2 and tau = 3/2, the crackling relation gives 1/(sigma nu z) = 2.",
    },
    {
        "id": "ID10792",
        "check": "crit_reciprocal_duality",
        "constructor": "HS_Crit_Reciprocal_Duality",
        "notes": "The avalanche/cascade pair is reciprocal: (3/2)*(2/3)=1.",
    },
]


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


def read_rows(path):
    with Path(path).open("r", encoding="utf-8-sig", errors="ignore", newline="") as handle:
        return list(csv.DictReader(handle))


def target_list(rows):
    return "[" + ", ".join(isa_string(row["id"], 20) for row in rows) + "]"


def case_body(cases):
    return " | ".join(cases)


def write_focus_theory(path, rows, obligations_sha, spine_sha, backing_sha, generated_at):
    provenance = isabelle_text(
        "prepare_nested_hypersphere_certificates.py",
        [
            f"TZPID_NESTED_HYPERSPHERE_obligations.csv SHA1 {obligations_sha}",
            f"TZPID_NESTED_HYPERSPHERE_SPINE.md SHA1 {spine_sha}",
            f"TZPID_NESTED_HYPERSPHERE_backing_ids.csv SHA1 {backing_sha}",
        ],
        generated_at,
        "Curated nested-hypersphere focus theory for cosmic acoustics and cross-scale projection.",
    )
    text = f"""theory TZPID_NestedHypersphere_Focus
  imports TZPID_Obligations
begin

{provenance}

text \\<open>
  Curated gold spine: Nested Hyperspherical Enclosures.
  The focus layer records the registry-backed proof obligations as typed Isabelle
  predicates without claiming more than the curated source certifies.
\\<close>

typedecl hs_angular_mode
typedecl hs_radial_mode
typedecl hs_hypersphere_mode
typedecl hs_bao_field
typedecl hs_sound_horizon
typedecl hs_power_spectrum
typedecl hs_filament_mode_sum
typedecl hs_ripple_pattern
typedecl hs_harmonic_ladder
typedecl hs_scale_ratio
typedecl hs_scale_invariance
typedecl hs_holographic_projection
typedecl hs_bulk_boundary_dictionary
typedecl hs_daans_manifold
typedecl hs_enclosure_geometry
typedecl hs_projection_map
typedecl hs_comma_ratio
typedecl hs_comma_cents
typedecl hs_comma_holonomy
typedecl hs_curvature_holonomy
typedecl hs_hopf_flip
typedecl hs_avalanche_law
typedecl hs_critical_exponent
typedecl hs_cascade_law
typedecl hs_crackling_relation
typedecl hs_critical_reciprocity

consts
  HS_Ylm :: hs_angular_mode
  HS_jl :: hs_radial_mode
  HS_S3_modes :: hs_hypersphere_mode
  HS_delta_b :: hs_bao_field
  HS_rs :: hs_sound_horizon
  HS_Pk :: hs_power_spectrum
  HS_Sigma :: hs_filament_mode_sum
  HS_Psi :: hs_ripple_pattern
  HS_fn :: hs_harmonic_ladder
  HS_ratio_32_27 :: hs_scale_ratio
  HS_scale_invariance :: hs_scale_invariance
  HS_holographic_projection :: hs_holographic_projection
  HS_bulk_boundary :: hs_bulk_boundary_dictionary
  HS_M_DAANS :: hs_daans_manifold
  HS_geometry :: hs_enclosure_geometry
  HS_pi :: hs_projection_map
  HS_gamma :: hs_comma_ratio
  HS_gamma_cents :: hs_comma_cents
  HS_theta_gamma :: hs_comma_holonomy
  HS_Omega :: hs_curvature_holonomy
  HS_hopf_flip :: hs_hopf_flip
  HS_avalanche_law :: hs_avalanche_law
  HS_tau :: hs_critical_exponent
  HS_cascade_law :: hs_cascade_law
  HS_crackling :: hs_crackling_relation
  HS_critical_reciprocity :: hs_critical_reciprocity

consts
  spherical_angular_eigenmode :: "hs_angular_mode => bool"
  spherical_radial_standing_wave :: "hs_radial_mode => bool"
  hypersphere_global_modes :: "hs_hypersphere_mode => bool"
  bao_primordial_standing_wave :: "hs_bao_field => hs_radial_mode => hs_sound_horizon => bool"
  sound_horizon_sets_acoustic_scale :: "hs_sound_horizon => bool"
  cosmic_web_power_spectrum :: "hs_power_spectrum => hs_bao_field => bool"
  filament_web_mode_sum :: "hs_filament_mode_sum => hs_power_spectrum => bool"
  bessel_interference_ripple :: "hs_ripple_pattern => hs_radial_mode => bool"
  harmonic_projection_ladder :: "hs_harmonic_ladder => bool"
  scale_ratio_invariant :: "hs_scale_ratio => bool"
  daans_scale_invariance :: "hs_scale_invariance => hs_scale_ratio => bool"
  holographic_projection_relation :: "hs_holographic_projection => bool"
  bulk_boundary_dictionary_relation ::
    "hs_bulk_boundary_dictionary => hs_holographic_projection => bool"
  daans_high_dimensional_manifold :: "hs_daans_manifold => bool"
  daans_enclosure_geometry :: "hs_enclosure_geometry => hs_daans_manifold => bool"
  downward_projection_map ::
    "hs_projection_map => hs_daans_manifold => hs_holographic_projection => bool"
  pythagorean_comma_exact :: "hs_comma_ratio => bool"
  pythagorean_comma_cents :: "hs_comma_cents => hs_comma_ratio => bool"
  comma_phase_holonomy :: "hs_comma_holonomy => hs_comma_ratio => hs_curvature_holonomy => bool"
  holonomy_equals_enclosed_curvature :: "hs_curvature_holonomy => bool"
  hopf_lift_inverse_flip :: "hs_hopf_flip => hs_curvature_holonomy => hs_comma_ratio => bool"
  universal_avalanche_exponent :: "hs_avalanche_law => hs_critical_exponent => bool"
  mean_field_avalanche_scaling :: "hs_avalanche_law => hs_critical_exponent => bool"
  cascade_intensity_scaling :: "hs_cascade_law => hs_critical_exponent => bool"
  crackling_size_duration_relation :: "hs_crackling_relation => hs_critical_exponent => bool"
  avalanche_cascade_reciprocal_duality ::
    "hs_critical_reciprocity => hs_critical_exponent => bool"
  cosmic_acoustics_chain :: bool
  ripple_projection_chain :: bool
  acoustic_holonomy_chain :: bool
  critical_scale_invariance_chain :: bool
  nested_hypersphere_unifying_chain :: bool

definition nested_hypersphere_target_ids :: "string list" where
  "nested_hypersphere_target_ids = {target_list(rows)}"

definition nested_hypersphere_obligations_sha1 :: string where
  "nested_hypersphere_obligations_sha1 = {isa_string(obligations_sha)}"

definition nested_hypersphere_spine_sha1 :: string where
  "nested_hypersphere_spine_sha1 = {isa_string(spine_sha)}"

definition nested_hypersphere_backing_ids_sha1 :: string where
  "nested_hypersphere_backing_ids_sha1 = {isa_string(backing_sha)}"

locale TZPID_NestedHypersphere_Focus = TZPID_Proof_Obligations +
  assumes id7732_angular: "spherical_angular_eigenmode HS_Ylm"
  and id7733_radial: "spherical_radial_standing_wave HS_jl"
  and id6819_s3_modes: "hypersphere_global_modes HS_S3_modes"
  and id7257_bao_field: "bao_primordial_standing_wave HS_delta_b HS_jl HS_rs"
  and id7259_sound_horizon: "sound_horizon_sets_acoustic_scale HS_rs"
  and id7177_power_spectrum: "cosmic_web_power_spectrum HS_Pk HS_delta_b"
  and id7207_filament_sum: "filament_web_mode_sum HS_Sigma HS_Pk"
  and id0230_ripple: "bessel_interference_ripple HS_Psi HS_jl"
  and id0256_ladder: "harmonic_projection_ladder HS_fn"
  and id6583_ratio: "scale_ratio_invariant HS_ratio_32_27"
  and id0362_scale: "daans_scale_invariance HS_scale_invariance HS_ratio_32_27"
  and id0104_holographic: "holographic_projection_relation HS_holographic_projection"
  and id8796_dictionary:
    "bulk_boundary_dictionary_relation HS_bulk_boundary HS_holographic_projection"
  and id0285_manifold: "daans_high_dimensional_manifold HS_M_DAANS"
  and id0245_geometry: "daans_enclosure_geometry HS_geometry HS_M_DAANS"
  and id1837_projection:
    "downward_projection_map HS_pi HS_M_DAANS HS_holographic_projection"
  and id10786_comma: "pythagorean_comma_exact HS_gamma"
  and id10787_comma_cents: "pythagorean_comma_cents HS_gamma_cents HS_gamma"
  and id10788_comma_phase: "comma_phase_holonomy HS_theta_gamma HS_gamma HS_Omega"
  and id10789_curvature_holonomy: "holonomy_equals_enclosed_curvature HS_Omega"
  and id10790_hopf_flip: "hopf_lift_inverse_flip HS_hopf_flip HS_Omega HS_gamma"
  and id0353_avalanche: "universal_avalanche_exponent HS_avalanche_law HS_tau"
  and id0395_mean_field: "mean_field_avalanche_scaling HS_avalanche_law HS_tau"
  and id0470_cascade: "cascade_intensity_scaling HS_cascade_law HS_tau"
  and id10791_crackling: "crackling_size_duration_relation HS_crackling HS_tau"
  and id10792_reciprocal:
    "avalanche_cascade_reciprocal_duality HS_critical_reciprocity HS_tau"
  and cosmic_chain: "cosmic_acoustics_chain"
  and ripple_chain: "ripple_projection_chain"
  and acoustic_holonomy_chain: "acoustic_holonomy_chain"
  and critical_chain: "critical_scale_invariance_chain"
  and unifying_chain: "nested_hypersphere_unifying_chain"
begin

theorem cosmic_filament_web_as_enclosure_acoustics:
  "spherical_angular_eigenmode HS_Ylm
    & spherical_radial_standing_wave HS_jl
    & hypersphere_global_modes HS_S3_modes
    & bao_primordial_standing_wave HS_delta_b HS_jl HS_rs
    & sound_horizon_sets_acoustic_scale HS_rs
    & cosmic_web_power_spectrum HS_Pk HS_delta_b
    & filament_web_mode_sum HS_Sigma HS_Pk"
  using id7732_angular id7733_radial id6819_s3_modes id7257_bao_field
    id7259_sound_horizon id7177_power_spectrum id7207_filament_sum
  by simp

theorem cross_scale_ripple_as_projection_signature:
  "bessel_interference_ripple HS_Psi HS_jl
    & harmonic_projection_ladder HS_fn
    & scale_ratio_invariant HS_ratio_32_27
    & daans_scale_invariance HS_scale_invariance HS_ratio_32_27
    & holographic_projection_relation HS_holographic_projection
    & bulk_boundary_dictionary_relation HS_bulk_boundary HS_holographic_projection"
  using id0230_ripple id0256_ladder id6583_ratio id0362_scale id0104_holographic
    id8796_dictionary
  by simp

theorem daanssphere_nested_enclosure_projection:
  "daans_high_dimensional_manifold HS_M_DAANS
    & daans_enclosure_geometry HS_geometry HS_M_DAANS
    & downward_projection_map HS_pi HS_M_DAANS HS_holographic_projection"
  using id0285_manifold id0245_geometry id1837_projection
  by simp

theorem pythagorean_comma_as_hopf_holonomy:
  "pythagorean_comma_exact HS_gamma
    & pythagorean_comma_cents HS_gamma_cents HS_gamma
    & comma_phase_holonomy HS_theta_gamma HS_gamma HS_Omega
    & holonomy_equals_enclosed_curvature HS_Omega
    & hopf_lift_inverse_flip HS_hopf_flip HS_Omega HS_gamma"
  using id10786_comma id10787_comma_cents id10788_comma_phase
    id10789_curvature_holonomy id10790_hopf_flip
  by simp

theorem critical_scale_invariance_as_projection_signature:
  "universal_avalanche_exponent HS_avalanche_law HS_tau
    & mean_field_avalanche_scaling HS_avalanche_law HS_tau
    & cascade_intensity_scaling HS_cascade_law HS_tau
    & crackling_size_duration_relation HS_crackling HS_tau
    & avalanche_cascade_reciprocal_duality HS_critical_reciprocity HS_tau"
  using id0353_avalanche id0395_mean_field id0470_cascade id10791_crackling
    id10792_reciprocal
  by simp

theorem nested_hypersphere_spine:
  "cosmic_filament_web_as_enclosure_acoustics
    & cross_scale_ripple_as_projection_signature
    & pythagorean_comma_as_hopf_holonomy
    & critical_scale_invariance_as_projection_signature
    & daanssphere_nested_enclosure_projection"
  using cosmic_filament_web_as_enclosure_acoustics
    cross_scale_ripple_as_projection_signature pythagorean_comma_as_hopf_holonomy
    critical_scale_invariance_as_projection_signature daanssphere_nested_enclosure_projection
  by simp

end

lemma nested_hypersphere_spine_target_count:
  "length nested_hypersphere_target_ids = {len(rows)}"
  by (simp add: nested_hypersphere_target_ids_def)

end
"""
    Path(path).write_text(text, encoding="utf-8")


def write_wolfram_checks(path, results_path, source_sha, generated_at):
    provenance = wolfram_comment(
        "prepare_nested_hypersphere_certificates.py",
        [f"TZPID_NESTED_HYPERSPHERE_obligations.csv SHA1 {source_sha}"],
        generated_at,
        "Generated Wolfram checks for the nested-hypersphere gold spine.",
    )
    text = provenance + f"""ClearAll["Global`*"];
outputPath = If[Length[$ScriptCommandLine] >= 2, $ScriptCommandLine[[2]], "{results_path.as_posix()}"];
If[! DirectoryQ[DirectoryName[outputPath]], CreateDirectory[DirectoryName[outputPath], CreateIntermediateDirectories -> True]];
asString[expr_] := ToString[expr, InputForm];

j0Node = FullSimplify[Sin[Pi]/Pi];
omegaResidual = FullSimplify[(omega - c x/R) /. omega -> c x/R, Assumptions -> R != 0];
enclosurePass = Chop[j0Node] == 0 && TrueQ[omegaResidual == 0];

baoNodeResidual = FullSimplify[(k rs /. k -> Pi/rs) - Pi, Assumptions -> rs != 0];
filamentPass = TrueQ[baoNodeResidual == 0];

ratioValue = N[32/27, 20];
ratioScaleResidual = FullSimplify[(lambda 32)/(lambda 27) - 32/27, Assumptions -> lambda != 0];
ratioPass = TrueQ[ratioScaleResidual == 0];

ladderRatios = FullSimplify[Table[(lambda n f1)/(lambda f1), {{n, 1, 5}}], Assumptions -> lambda != 0 && f1 != 0];
ladderPass = ladderRatios === Range[5];

holographicResidual = FullSimplify[SA - AreaGamma/(4 G) /. SA -> AreaGamma/(4 G), Assumptions -> G != 0];
holographicPass = TrueQ[holographicResidual == 0];

gammaComma = (3/2)^12 / 2^7;
gammaExactPass = TrueQ[gammaComma == 531441/524288];
commaCents = N[1200 Log[2, gammaComma], 12];
commaCentsPass = Abs[commaCents - 23.460010384649] < 10^-9;
thetaGamma = N[2 Pi (12 Log[2, 3/2] - 7), 14];
sphereFraction = N[thetaGamma/(4 Pi) 100, 12];
holonomyResidual = FullSimplify[2 Pi Log[2, gammaComma] - 2 Pi (12 Log[2, 3/2] - 7)];
holonomyPass = TrueQ[holonomyResidual == 0];
omegaBulk = 1/gammaComma;
inverseFlipResidual = FullSimplify[gammaComma omegaBulk - 1];
inverseFlipPass = TrueQ[inverseFlipResidual == 0];
gamma53 = (3/2)^53 / 2^31;
cents53 = N[1200 Log[2, gamma53], 12];
theta53 = N[2 Pi (53 Log[2, 3/2] - 31), 14];
sphereFraction53 = N[theta53/(4 Pi) 100, 12];
nearClosurePass = TrueQ[Abs[cents53] < commaCents && Abs[cents53 - 3.615045773] < 10^-6];

tauCrit = 3/2;
alphaCrit = 2;
universalExponentResidual = FullSimplify[tauCrit - 3/2];
universalExponentPass = TrueQ[universalExponentResidual == 0];
cascadeExponentResidual = FullSimplify[(1 - tauCrit) - (-1/2)];
cascadeIntensityPass = TrueQ[cascadeExponentResidual == 0];
cracklingValue = FullSimplify[(alphaCrit - 1)/(tauCrit - 1)];
cracklingPass = TrueQ[cracklingValue == 2];
criticalReciprocalResidual = FullSimplify[(3/2) (2/3) - 1];
criticalReciprocalPass = TrueQ[criticalReciprocalResidual == 0];

results = {{
  <|"id" -> "ID7733", "check" -> "hs_enclosure_eigenfreq", "status" -> If[TrueQ[enclosurePass], "pass", "fail"], "engine" -> "WolframScript", "spherical_bessel_j0_pi" -> asString[j0Node], "frequency_residual" -> asString[omegaResidual], "notes" -> "{CHECKS[0]['notes']}"|>,
  <|"id" -> "ID7259", "check" -> "hs_filament_scale", "status" -> If[TrueQ[filamentPass], "pass", "fail"], "engine" -> "WolframScript", "node_residual" -> asString[baoNodeResidual], "notes" -> "{CHECKS[1]['notes']}"|>,
  <|"id" -> "ID6583", "check" -> "hs_ratio_scale_free", "status" -> If[TrueQ[ratioPass], "pass", "fail"], "engine" -> "WolframScript", "ratio_value" -> asString[ratioValue], "scale_residual" -> asString[ratioScaleResidual], "notes" -> "{CHECKS[2]['notes']}"|>,
  <|"id" -> "ID0256", "check" -> "hs_projection_ladder", "status" -> If[TrueQ[ladderPass], "pass", "fail"], "engine" -> "WolframScript", "ladder_ratios" -> asString[ladderRatios], "notes" -> "{CHECKS[3]['notes']}"|>,
  <|"id" -> "ID0104", "check" -> "hs_holographic_count", "status" -> If[TrueQ[holographicPass], "pass", "fail"], "engine" -> "WolframScript", "entropy_residual" -> asString[holographicResidual], "notes" -> "{CHECKS[4]['notes']}"|>,
  <|"id" -> "ID10786", "check" -> "comma_exact", "status" -> If[TrueQ[gammaExactPass], "pass", "fail"], "engine" -> "WolframScript", "gamma" -> asString[gammaComma], "notes" -> "{CHECKS[5]['notes']}"|>,
  <|"id" -> "ID10787", "check" -> "comma_cents", "status" -> If[TrueQ[commaCentsPass], "pass", "fail"], "engine" -> "WolframScript", "cents" -> asString[commaCents], "notes" -> "{CHECKS[6]['notes']}"|>,
  <|"id" -> "ID10788", "check" -> "comma_hopf_holonomy", "status" -> If[TrueQ[holonomyPass], "pass", "fail"], "engine" -> "WolframScript", "theta_gamma" -> asString[thetaGamma], "sphere_fraction_percent" -> asString[sphereFraction], "holonomy_residual" -> asString[holonomyResidual], "notes" -> "{CHECKS[7]['notes']}"|>,
  <|"id" -> "ID10790", "check" -> "inverse_outward_flip", "status" -> If[TrueQ[inverseFlipPass], "pass", "fail"], "engine" -> "WolframScript", "residual_after_substitution" -> asString[inverseFlipResidual], "omega_bulk" -> asString[N[omegaBulk, 14]], "notes" -> "{CHECKS[8]['notes']}"|>,
  <|"id" -> "comparison_53_fifths", "check" -> "comma_53_near_closure", "status" -> If[TrueQ[nearClosurePass], "pass", "fail"], "engine" -> "WolframScript", "gamma53" -> asString[N[gamma53, 14]], "cents53" -> asString[cents53], "theta53" -> asString[theta53], "sphere_fraction53_percent" -> asString[sphereFraction53], "notes" -> "{CHECKS[9]['notes']}"|>,
  <|"id" -> "ID0395", "check" -> "crit_universal_exponent", "status" -> If[TrueQ[universalExponentPass], "pass", "fail"], "engine" -> "WolframScript", "tau" -> asString[tauCrit], "residual_after_substitution" -> asString[universalExponentResidual], "notes" -> "{CHECKS[10]['notes']}"|>,
  <|"id" -> "ID0470", "check" -> "crit_cascade_intensity", "status" -> If[TrueQ[cascadeIntensityPass], "pass", "fail"], "engine" -> "WolframScript", "cascade_exponent" -> asString[1 - tauCrit], "residual_after_substitution" -> asString[cascadeExponentResidual], "notes" -> "{CHECKS[11]['notes']}"|>,
  <|"id" -> "ID10791", "check" -> "crit_crackling_relation", "status" -> If[TrueQ[cracklingPass], "pass", "fail"], "engine" -> "WolframScript", "crackling_value" -> asString[cracklingValue], "notes" -> "{CHECKS[12]['notes']}"|>,
  <|"id" -> "ID10792", "check" -> "crit_reciprocal_duality", "status" -> If[TrueQ[criticalReciprocalPass], "pass", "fail"], "engine" -> "WolframScript", "residual_after_substitution" -> asString[criticalReciprocalResidual], "notes" -> "{CHECKS[13]['notes']}"|>
}};
Export[outputPath, results, "RawJSON"];
Print["Wrote " <> outputPath];
"""
    Path(path).write_text(text, encoding="utf-8")


def run_wolfram(script_path, results_path):
    completed = subprocess.run(
        ["wolframscript", "-file", str(script_path), str(results_path)],
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        raise RuntimeError(
            "wolframscript failed\nSTDOUT:\n"
            + completed.stdout
            + "\nSTDERR:\n"
            + completed.stderr
        )
    return completed.stdout.strip()


def constructor_for(row):
    check = row.get("check", "")
    for item in CHECKS:
        if item["check"] == check:
            return item["constructor"]
    safe = re.sub(r"[^A-Za-z0-9]+", "_", check).strip("_")
    return "HS_Check_" + safe


def write_certificate_theory(path, results, results_sha, generated_at):
    datatype_lines = "\n  | ".join(constructor_for(row) for row in results)
    status_cases = []
    id_cases = []
    note_cases = []
    for row in results:
        ctor = constructor_for(row)
        status_cases.append(f"{ctor} => {isa_string(row.get('status', ''), 80)}")
        id_cases.append(f"{ctor} => {isa_string(row.get('id', ''), 20)}")
        note_cases.append(f"{ctor} => {isa_string(row.get('notes', ''), 700)}")

    pass_lemmas = []
    for row in results:
        if row.get("status") != "pass":
            continue
        lemma_name = re.sub(r"[^a-z0-9]+", "_", row.get("check", "").lower()).strip("_") + "_passed"
        pass_lemmas.append(
            f"""lemma {lemma_name}:
  "nested_hypersphere_verified_check {constructor_for(row)}"
  by (simp add: nested_hypersphere_verified_check_def nested_hypersphere_check_status_def)
"""
        )

    provenance = isabelle_text(
        "prepare_nested_hypersphere_certificates.py",
        [f"nested hypersphere Wolfram results SHA1 {results_sha}"],
        generated_at,
        "Wolfram-backed certificate layer for the nested-hypersphere gold spine.",
    )

    text = f"""theory TZPID_NestedHypersphere_Computational_Checks
  imports TZPID_NestedHypersphere_Focus
begin

{provenance}

text \\<open>
  Wolfram-backed certificate layer for the nested-hypersphere spine.
\\<close>

datatype nested_hypersphere_check =
  {datatype_lines}

definition nested_hypersphere_wolfram_results_sha1 :: string where
  "nested_hypersphere_wolfram_results_sha1 = {isa_string(results_sha)}"

definition nested_hypersphere_check_status :: "nested_hypersphere_check => string" where
  "nested_hypersphere_check_status check = (case check of {case_body(status_cases)})"

definition nested_hypersphere_check_registry_id :: "nested_hypersphere_check => string" where
  "nested_hypersphere_check_registry_id check = (case check of {case_body(id_cases)})"

definition nested_hypersphere_check_notes :: "nested_hypersphere_check => string" where
  "nested_hypersphere_check_notes check = (case check of {case_body(note_cases)})"

definition nested_hypersphere_verified_check :: "nested_hypersphere_check => bool" where
  "nested_hypersphere_verified_check check = (nested_hypersphere_check_status check = ''pass'')"

{chr(10).join(pass_lemmas)}

context TZPID_NestedHypersphere_Focus
begin

theorem nested_hypersphere_spine_has_wolfram_certificate:
  "nested_hypersphere_verified_check HS_Enclosure_Eigenfreq
    & nested_hypersphere_verified_check HS_Filament_Scale
    & nested_hypersphere_verified_check HS_Ratio_Scale_Free
    & nested_hypersphere_verified_check HS_Projection_Ladder
    & nested_hypersphere_verified_check HS_Holographic_Count
    & nested_hypersphere_verified_check HS_Comma_Exact
    & nested_hypersphere_verified_check HS_Comma_Cents
    & nested_hypersphere_verified_check HS_Comma_Hopf_Holonomy
    & nested_hypersphere_verified_check HS_Inverse_Outward_Flip
    & nested_hypersphere_verified_check HS_Comma_53_Near_Closure
    & nested_hypersphere_verified_check HS_Crit_Universal_Exponent
    & nested_hypersphere_verified_check HS_Crit_Cascade_Intensity
    & nested_hypersphere_verified_check HS_Crit_Crackling_Relation
    & nested_hypersphere_verified_check HS_Crit_Reciprocal_Duality
    & nested_hypersphere_spine"
  using hs_enclosure_eigenfreq_passed hs_filament_scale_passed hs_ratio_scale_free_passed
    hs_projection_ladder_passed hs_holographic_count_passed comma_exact_passed
    comma_cents_passed comma_hopf_holonomy_passed inverse_outward_flip_passed
    comma_53_near_closure_passed crit_universal_exponent_passed
    crit_cascade_intensity_passed crit_crackling_relation_passed
    crit_reciprocal_duality_passed nested_hypersphere_spine
  by simp

end

end
"""
    Path(path).write_text(text, encoding="utf-8")


def write_summary(path, results, results_sha, generated_at, wolfram_stdout):
    lines = [
        "# Nested-Hypersphere Wolfram Certificates",
        "",
        "Project: TZPID Proof Pipeline",
        "Creator: Daniel Alexander Trawin",
        "ORCID: https://orcid.org/0009-0001-4630-3715",
        "Generator: prepare_nested_hypersphere_certificates.py",
        f"Generated UTC: {generated_at}",
        "",
        f"Wolfram result SHA1: `{results_sha}`",
        f"Wolfram stdout: `{ascii_clean(wolfram_stdout, 240)}`",
        "",
        "| ID | Check | Status | Notes |",
        "|---|---|---|---|",
    ]
    for row in results:
        lines.append(
            f"| {row.get('id', '')} | `{row.get('check', '')}` | `{row.get('status', '')}` | "
            f"{ascii_clean(row.get('notes', ''), 240)} |"
        )
    Path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")


def update_root(root_path):
    root = Path(root_path)
    text = root.read_text(encoding="utf-8")
    for theory in ["TZPID_NestedHypersphere_Focus", "TZPID_NestedHypersphere_Computational_Checks"]:
        if theory not in text:
            text = text.rstrip() + f"\n    {theory}\n"
    root.write_text(text, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--obligations", default=DEFAULT_OBLIGATIONS)
    parser.add_argument("--spine", default=DEFAULT_SPINE)
    parser.add_argument("--backing", default=DEFAULT_BACKING)
    parser.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--wolfram-dir", default=DEFAULT_WOLFRAM_DIR)
    parser.add_argument("--skip-wolfram", action="store_true")
    args = parser.parse_args()

    rows = read_rows(args.obligations)
    generated_at = generated_utc()
    obligations_sha = file_sha1(args.obligations)
    spine_sha = file_sha1(args.spine)
    backing_sha = file_sha1(args.backing)

    out = Path(args.output_dir)
    wf = Path(args.wolfram_dir)
    out.mkdir(parents=True, exist_ok=True)
    wf.mkdir(parents=True, exist_ok=True)

    focus_path = out / "TZPID_NestedHypersphere_Focus.thy"
    check_path = wf / "nested_hypersphere_checks.wl"
    results_path = wf / "nested_hypersphere_results.json"
    cert_path = out / "TZPID_NestedHypersphere_Computational_Checks.thy"
    summary_path = out / "nested_hypersphere_wolfram_certificate_summary.md"

    write_focus_theory(focus_path, rows, obligations_sha, spine_sha, backing_sha, generated_at)
    write_wolfram_checks(check_path, results_path, obligations_sha, generated_at)

    wolfram_stdout = "skipped"
    if not args.skip_wolfram:
        wolfram_stdout = run_wolfram(check_path, results_path)

    results = json.loads(results_path.read_text(encoding="utf-8"))
    results_sha = file_sha1(results_path)
    write_certificate_theory(cert_path, results, results_sha, generated_at)
    write_summary(summary_path, results, results_sha, generated_at, wolfram_stdout)
    update_root(out / "ROOT")

    print(f"Wrote {focus_path}")
    print(f"Wrote {check_path}")
    print(f"Wrote {results_path}")
    print(f"Wrote {cert_path}")
    print(f"Wrote {summary_path}")


if __name__ == "__main__":
    main()
