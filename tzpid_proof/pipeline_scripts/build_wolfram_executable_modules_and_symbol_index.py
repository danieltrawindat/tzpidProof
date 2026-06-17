import csv
import base64
import hashlib
import json
import re
import shutil
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"d:\tzpidNEW")
WOLFRAM_DIR = Path(r"D:\WolfRam")
ALL_WLS = WOLFRAM_DIR / "all.wls"
SOURCE_CSV = WOLFRAM_DIR / "all_module_library_source.csv"
EXECUTABLE_WLS = WOLFRAM_DIR / "all_executable_modules.wls"
MASTER = Path(r"D:\00_Engine\AI_Workspaces\OpenAI2\TZPID_ALL_IDS_CANONICAL_EQUATION_MASTER_with_export.csv")
DICTIONARY = Path(r"D:\00_Engine\AI_Workspaces\OpenAI2\TZPID_DICTIONARY.csv")
ENCYCLOPEDIA = Path(r"D:\00_Engine\AI_Workspaces\OpenAI2\TZPID_ENCYCLOPEDIA.md")
TRAWIN_SYMBOLS = WOLFRAM_DIR / "TrawinisticSymbols.wls"
SYMBOL_TXT = WOLFRAM_DIR / "WolfRam" / "symbol.txt"


PROVENANCE = {
    "project": "TZPID Proof Pipeline",
    "creator": "Daniel Alexander Trawin",
    "creator_orcid": "0009-0001-4630-3715",
    "creator_orcid_url": "https://orcid.org/0009-0001-4630-3715",
}


KNOWN_SYMBOLS = {
    "π": ("pi; circle constant", "standard_math"),
    "Pi": ("pi; circle constant", "standard_math"),
    "φ": ("golden ratio or phase angle, context dependent", "standard_math"),
    "Phi": ("field, phase, or golden-ratio carrier, context dependent", "corpus_inferred"),
    "Φ": ("field, phase, flux, or golden-ratio carrier, context dependent", "corpus_inferred"),
    "ψ": ("wavefunction or state", "standard_quantum"),
    "Ψ": ("wavefunction, state, or DAANS/TZP map", "standard_quantum"),
    "ρ": ("density or density matrix, context dependent", "standard_physics"),
    "rho": ("density or density matrix, context dependent", "standard_physics"),
    "σ": ("cross-section, Pauli operator, or standard deviation, context dependent", "standard_physics"),
    "τ": ("time constant, winding time, or characteristic class, context dependent", "corpus_inferred"),
    "θ": ("angle coordinate", "standard_math"),
    "Theta": ("angle/phase structure or named operator, context dependent", "corpus_inferred"),
    "ω": ("angular frequency", "standard_physics"),
    "Omega": ("angular frequency, invariant, or topological charge, context dependent", "corpus_inferred"),
    "Ω": ("angular frequency, invariant, or topological charge, context dependent", "corpus_inferred"),
    "ℏ": ("reduced Planck constant", "standard_physics"),
    "hbar": ("reduced Planck constant", "standard_physics"),
    "c": ("speed of light or generic constant, context dependent", "standard_physics"),
    "G": ("Newton gravitational constant, tensor, or group, context dependent", "standard_physics"),
    "Λ": ("cosmological constant, cutoff, or named operator, context dependent", "standard_physics"),
    "lambda": ("wavelength, eigenvalue, coupling, or lambda abstraction, context dependent", "standard_math"),
    "λ": ("wavelength, eigenvalue, coupling, or lambda abstraction, context dependent", "standard_math"),
    "mu": ("mu parameter: mass, permeability, chemical potential, or measure, context dependent", "standard_math"),
    "nu": ("nu parameter: frequency, neutrino label, or index, context dependent", "standard_math"),
    "∇": ("gradient/nabla operator", "standard_math"),
    "∂": ("partial derivative operator", "standard_math"),
    "∫": ("integral operator", "standard_math"),
    "Σ": ("summation or named sigma component, context dependent", "standard_math"),
    "Δ": ("difference, gap, or Laplacian-like operator, context dependent", "standard_math"),
    "ℒ": ("Trawinistic manifold or Lagrangian, context dependent", "trawin_symbol_seed"),
    "TZP": ("Trawin Zero Point", "trawin_symbol_seed"),
    "J_TZP": ("source term localized at the Trawin Zero Point", "trawin_symbol_seed"),
    "ρ_vac": ("vacuum energy density", "trawin_symbol_seed"),
    "ν_T": ("Trawinistic winding number", "trawin_symbol_seed"),
    "SU_q(2)_TZP": ("TZP quantum group", "trawin_symbol_seed"),
    "T": ("temporal gradient or time variable, context dependent", "trawin_operator_seed"),
    "R": ("rotational/curl operator, radius, or Ricci scalar, context dependent", "trawin_operator_seed"),
    "A": ("amplitude, acceleration, connection, or area, context dependent", "trawin_operator_seed"),
    "W": ("wave operator or witness, context dependent", "trawin_operator_seed"),
    "I": ("information integral or identity/imaginary unit, context dependent", "trawin_operator_seed"),
    "N": ("normalization, count, or null constraint, context dependent", "trawin_operator_seed"),
}


UNICODE_TO_WL = {
    "→": "->",
    "↦": "->",
    "⟹": "->",
    "⇒": "->",
    "π": "Pi",
    "Π": "PiCarrier",
    "ℏ": "hbar",
    "∂": "partialD",
    "∇": "nabla",
    "∫": "IntegralOp",
    "√": "Sqrt",
    "×": "*",
    "·": ".",
    "≈": "~",
    "≠": "!=",
    "≤": "<=",
    "≥": ">=",
    "∈": "Element",
    "∞": "Infinity",
    "∑": "Sum",
    "Σ": "Sigma",
    "Ω": "Omega",
    "ω": "omega",
    "ρ": "rho",
    "θ": "theta",
    "φ": "phi",
    "ϕ": "phi",
    "Φ": "Phi",
    "Ψ": "Psi",
    "ψ": "psi",
    "μ": "mu",
    "ν": "nu",
    "σ": "sigma",
    "τ": "tau",
    "λ": "lambda",
    "Λ": "Lambda",
    "Δ": "Delta",
    "η": "eta",
    "κ": "kappa",
    "α": "alpha",
    "β": "beta",
    "γ": "gamma",
    "ε": "epsilon",
    "ℒ": "ScriptL",
    "ℋ": "ScriptH",
    "ℐ": "ScriptI",
    "𝒦": "ScriptK",
    "𝒯": "ScriptT",
    "𝒟": "ScriptD",
    "𝔊": "ScriptG",
    "ℱ": "ScriptF",
    "ℂ": "ScriptC",
    "Ξ": "Xi",
    "Θ": "Theta",
    "𝕀": "IdentityCarrier",
    "†": "Dagger",
    "ᵀ": "T",
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
    "⁰": "0",
    "¹": "1",
    "²": "2",
    "³": "3",
    "⁴": "4",
    "⁵": "5",
    "⁶": "6",
    "⁷": "7",
    "⁸": "8",
    "⁹": "9",
}


TOKEN_RE = re.compile(
    r"[A-Za-z][A-Za-z0-9_]*(?:\^[A-Za-z0-9_]+)?|[Α-Ωα-ω][A-Za-z0-9_Α-Ωα-ω₀-₉⁰-⁹]*|[ℏℒℋℐ𝒦𝒯𝒟𝔊ℱℂ𝕀ΞΘΨΦΣΩΔΛ]"
)


STOP_TOKENS = {
    "begin", "end", "where", "with", "and", "or", "the", "of", "to", "in", "for", "from", "is",
    "as", "by", "if", "then", "else", "let", "return", "module", "association", "definition",
    "relation", "subject", "under", "report", "id", "true", "false", "none", "nan",
}


COMMON_WORDS = {
    "about", "above", "across", "after", "again", "against", "also", "because", "before",
    "being", "between", "built", "canonical", "captures", "case", "component", "components",
    "context", "corpus", "defined", "defines", "describes", "element", "equation", "expresses",
    "framework", "function", "general", "given", "inside", "interpreted", "introduces", "it",
    "key", "layer", "local", "math", "mathematical", "means", "model", "narrative", "object",
    "operator", "packet", "present", "preserve", "proof", "quantity", "relation", "relating",
    "represented", "section", "serves", "source", "statement", "structure", "symbol", "symbols",
    "technical", "terms", "through", "used", "variable", "variables", "where", "within",
    "text", "mathrm", "mathcal", "mathbb", "operatorname", "left", "right", "quad", "qquad",
    "frac", "begin", "end", "label", "equation", "align", "boxed", "displaystyle", "rm",
    "mathbf", "mathsf", "mathit", "mathscr", "overline", "underline", "hat", "tilde", "bar",
}


def utc_now():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha1(path):
    digest = hashlib.sha1()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_csv(path):
    with Path(path).open("r", encoding="utf-8-sig", errors="ignore", newline="") as handle:
        return list(csv.DictReader(handle))


def wl_string(text):
    text = "" if text is None else str(text)
    return '"' + text.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n").replace("\r", "") + '"'


def b64(text):
    return base64.b64encode(("" if text is None else str(text)).encode("utf-8")).decode("ascii")


def wl_symbol(name):
    safe = re.sub(r"[^A-Za-z0-9$]+", "$", name).strip("$")
    if not safe or not re.match(r"[A-Za-z$]", safe):
        safe = "Module$" + safe
    return "TZPID$" + safe


def normalize_for_wolfram(text):
    out = "" if text is None else str(text)
    for old, new in UNICODE_TO_WL.items():
        out = out.replace(old, new)
    out = re.sub(r"\(\*.*?\*\)", " ", out)
    out = re.sub(r"\s+", " ", out).strip()
    return out


def source_packet(row, parse_status):
    packet = {
        "module_name": row.get("module_name", ""),
        "module_type": row.get("module_type", ""),
        "source_report": row.get("source_report", ""),
        "theme": row.get("theme", ""),
        "related_spine": row.get("related_spine", ""),
        "registry_ids_same_report": row.get("registry_ids_same_report", ""),
        "n_registry_ids": row.get("n_registry_ids", ""),
        "check_kind": row.get("check_kind", ""),
        "execution_status": parse_status,
        "code_excerpt": row.get("code_excerpt", ""),
        "normalized_excerpt": normalize_for_wolfram(row.get("code_excerpt", "")),
    }
    return packet


def write_executable_wls(rows, results_by_key, generated_at):
    source_csv_wl = str(SOURCE_CSV).replace("\\", "\\\\")
    lines = [
        "(* ::Package:: *)",
        "(* TZPID Algorithmic-Ambassador executable module library *)",
        f"(* Generated UTC: {generated_at} *)",
        f"(* Creator: {PROVENANCE['creator']} / {PROVENANCE['creator_orcid_url']} *)",
        "",
        "ClearAll[TZPIDModuleSourceCSV, TZPIDModuleRows, TZPIDModuleLibrary, TZPIDModuleIndex, TZPIDRunModule, TZPIDRunAllModules, TZPIDModuleStatusCounts];",
        "",
        f"TZPIDModuleSourceCSV = \"{source_csv_wl}\";",
        "TZPID$rawRows = Import[TZPIDModuleSourceCSV, \"CSV\"];",
        "TZPID$headers = ToString /@ First[TZPID$rawRows];",
        "TZPIDModuleRows = AssociationThread[TZPID$headers, #]& /@ Rest[TZPID$rawRows];",
        "TZPID$clean[value_] := If[Head[value] === Missing, \"\", ToString[value]];",
        "TZPID$statusFor[row_Association] := Module[{code = Lookup[row, \"code_excerpt\", \"\"], parsed},",
        "  parsed = Quiet[Check[ToExpression[code, InputForm, HoldComplete], $Failed]];",
        "  If[parsed === $Failed, \"source_packet_normalized\", \"parse_ok\"]",
        "];",
        "TZPID$keyFor[row_Association, i_Integer] := TZPID$clean[Lookup[row, \"module_name\", \"Module\"]] <> \"::\" <> IntegerString[i, 10, 3];",
        "TZPID$packet[row_Association, i_Integer] := Module[{key = TZPID$keyFor[row, i], status = TZPID$statusFor[row]},",
        "  <|",
        "    \"LibraryKey\" -> key,",
        "    \"Ordinal\" -> i,",
        "    \"ModuleName\" -> TZPID$clean[Lookup[row, \"module_name\", \"\"]],",
        "    \"ModuleType\" -> TZPID$clean[Lookup[row, \"module_type\", \"\"]],",
        "    \"SourceReport\" -> TZPID$clean[Lookup[row, \"source_report\", \"\"]],",
        "    \"Theme\" -> TZPID$clean[Lookup[row, \"theme\", \"\"]],",
        "    \"RelatedSpine\" -> TZPID$clean[Lookup[row, \"related_spine\", \"\"]],",
        "    \"RegistryIDs\" -> TZPID$clean[Lookup[row, \"registry_ids_same_report\", \"\"]],",
        "    \"CheckKind\" -> TZPID$clean[Lookup[row, \"check_kind\", \"\"]],",
        "    \"ExecutionStatus\" -> status,",
        "    \"CodeExcerpt\" -> TZPID$clean[Lookup[row, \"code_excerpt\", \"\"]],",
        "    \"Callable\" -> Function[{}, <|",
        "      \"LibraryKey\" -> key,",
        "      \"ModuleName\" -> TZPID$clean[Lookup[row, \"module_name\", \"\"]],",
        "      \"ExecutionStatus\" -> status,",
        "      \"ResultKind\" -> \"ExecutableSourcePacket\",",
        "      \"SourceReport\" -> TZPID$clean[Lookup[row, \"source_report\", \"\"]],",
        "      \"RelatedSpine\" -> TZPID$clean[Lookup[row, \"related_spine\", \"\"]],",
        "      \"RegistryIDs\" -> TZPID$clean[Lookup[row, \"registry_ids_same_report\", \"\"]],",
        "      \"CodeExcerpt\" -> TZPID$clean[Lookup[row, \"code_excerpt\", \"\"]]",
        "    |>]",
        "  |>",
        "];",
        "TZPIDModuleLibrary = Association@Table[TZPID$keyFor[TZPIDModuleRows[[i]], i] -> TZPID$packet[TZPIDModuleRows[[i]], i], {i, Length[TZPIDModuleRows]}];",
        "TZPIDModuleIndex = Association@Table[TZPID$clean[Lookup[TZPIDModuleRows[[i]], \"module_name\", \"Module\"]] -> TZPID$keyFor[TZPIDModuleRows[[i]], i], {i, Length[TZPIDModuleRows]}];",
        "",
    ]
    index_entries = []
    function_defs = []
    for idx, row in enumerate(rows, start=1):
        key = f"{row.get('module_name','')}::{idx:03d}"
        function_name = wl_symbol(key)
        index_entries.append(f'  {wl_string(row.get("module_name", ""))} -> {wl_string(key)}')
        function_defs.append(f"{function_name}[] := TZPIDModuleLibrary[{wl_string(key)}][\"Callable\"][];")
    lines.extend(function_defs)
    lines.append("")
    lines.extend(
        [
            "TZPIDModuleIndex = <|",
            ",\n".join(index_entries),
            "|>;",
            "",
            "TZPIDRunModule[key_String] := If[KeyExistsQ[TZPIDModuleLibrary, key], TZPIDModuleLibrary[key][\"Callable\"][], Missing[\"UnknownModule\", key]];",
            "TZPIDRunAllModules[] := AssociationMap[TZPIDRunModule, Keys[TZPIDModuleLibrary]];",
            "TZPIDModuleStatusCounts[] := Counts[TZPIDModuleLibrary[[All, \"ExecutionStatus\"]]];",
            "",
            "If[$FrontEnd === Null && Length[$ScriptCommandLine] > 1 && Last[$ScriptCommandLine] === \"--run-summary\",",
            "  Print[ExportString[<|\"ModuleCount\" -> Length[TZPIDModuleLibrary], \"StatusCounts\" -> TZPIDModuleStatusCounts[]|>, \"JSON\"]]",
            "];",
            "",
        ]
    )
    EXECUTABLE_WLS.write_text("\n".join(lines), encoding="utf-8")
    shutil.copy2(EXECUTABLE_WLS, ALL_WLS)


def result_key(row):
    return (
        row.get("module_name", ""),
        row.get("module_type", ""),
        row.get("source_report", ""),
        row.get("related_spine", ""),
        row.get("registry_ids_same_report", ""),
    )


def load_results():
    path = ROOT / "wolfram_checks" / "aa_module_library_results.json"
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return {result_key(row): row for row in data}


def parse_trawin_symbol_seeds():
    seeds = {}
    for path in [TRAWIN_SYMBOLS, SYMBOL_TXT]:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for match in re.finditer(r'TrawinSymbol\["([^"]+)"\]\s*:=\s*"([^"]+)"', text):
            seeds[match.group(1)] = (match.group(2), f"seed:{path.name}")
        for match in re.finditer(r'TrawinOperator\["([^"]+)"\]\s*:=\s*"([^"]+)"', text):
            seeds[match.group(1)] = (match.group(2), f"seed:{path.name}")
        for match in re.finditer(r'DAANSCoordinate\["([^"]+)"\]\s*:=\s*"([^"]+)"', text):
            seeds[match.group(1)] = (match.group(2), f"seed:{path.name}")
        for line in text.splitlines():
            cells = re.findall(r"`([^`]+)`|\|\s*([^|`]+?)\s*\|", line)
            flat = [a or b.strip() for a, b in cells if (a or b.strip())]
            if len(flat) >= 2 and flat[0] not in {"Symbol", "----------"}:
                symbol = flat[0].strip()
                meaning = flat[1].strip()
                if symbol and meaning and len(symbol) <= 40:
                    seeds.setdefault(symbol, (meaning, f"table:{path.name}"))
    return seeds


def infer_meaning(symbol, contexts, seed_meanings):
    if symbol in seed_meanings:
        return (*seed_meanings[symbol], "high")
    if symbol in KNOWN_SYMBOLS:
        meaning, source = KNOWN_SYMBOLS[symbol]
        return meaning, source, "medium"
    joined = " ".join(contexts[:20]).lower()
    rules = [
        ("vac" in symbol.lower() or "vacuum" in joined, "vacuum-sector quantity", "context_rule"),
        ("rho" in symbol.lower() or symbol.startswith("ρ"), "density or density-matrix quantity", "context_rule"),
        ("omega" in symbol.lower() or symbol.startswith("ω"), "frequency, winding, or angular quantity", "context_rule"),
        ("phi" in symbol.lower() or symbol in {"Φ", "φ"}, "field, phase, or golden-ratio quantity", "context_rule"),
        ("psi" in symbol.lower() or symbol in {"Ψ", "ψ"}, "state or wavefunction quantity", "context_rule"),
        ("hamilton" in joined or symbol.startswith("H"), "Hamiltonian, energy, or field strength depending on context", "context_rule"),
        ("curvature" in joined or symbol in {"F", "R"}, "curvature/geometric quantity depending on context", "context_rule"),
        ("neutrino" in joined or "_ν" in symbol or "nu" in symbol.lower(), "neutrino-sector quantity", "context_rule"),
        ("dna" in joined or "helix" in joined, "DNA/biological-sector quantity", "context_rule"),
    ]
    for ok, meaning, source in rules:
        if ok:
            return meaning, source, "low"
    return "needs definition: symbol occurs in corpus but no stable meaning was recovered", "needs_definition", "unknown"


def extract_symbols_from_master(rows):
    occurrences = defaultdict(lambda: {"count": 0, "ids": [], "titles": [], "contexts": Counter()})
    for row in rows:
        text = " ".join(
            [
                row.get("title", ""),
                row.get("canonical_statement", ""),
                row.get("canonical_equation", ""),
                row.get("formation_inputs", ""),
            ]
        )
        tokens = TOKEN_RE.findall(text)
        seen_in_row = set()
        for token in tokens:
            token = token.strip()
            if not token or token.lower() in STOP_TOKENS or token.lower() in COMMON_WORDS or token.isdigit() or len(token) > 50:
                continue
            occurrences[token]["count"] += 1
            if token not in seen_in_row:
                occurrences[token]["ids"].append(row.get("id", ""))
                occurrences[token]["titles"].append(row.get("title", ""))
                seen_in_row.add(token)
            context = " ".join([row.get("title", ""), row.get("canonical_equation", "")])[:240]
            occurrences[token]["contexts"][context] += 1
    return occurrences


def write_symbol_index(master_rows, generated_at):
    seed_meanings = parse_trawin_symbol_seeds()
    occurrences = extract_symbols_from_master(master_rows)
    rows = []
    for symbol, info in sorted(occurrences.items(), key=lambda item: (-item[1]["count"], item[0])):
        contexts = list(info["contexts"].keys())
        meaning, source, confidence = infer_meaning(symbol, contexts, seed_meanings)
        rows.append(
            {
                "symbol": symbol,
                "meaning": meaning,
                "meaning_source": source,
                "confidence": confidence,
                "occurrence_count": info["count"],
                "id_count": len(set(info["ids"])),
                "sample_ids": "; ".join(info["ids"][:20]),
                "sample_titles": " | ".join(info["titles"][:5]),
                "sample_context": contexts[0] if contexts else "",
                "wolfram_symbol": normalize_for_wolfram(symbol),
            }
        )
    curated_rows = [
        row for row in rows
        if is_curated_symbol_row(row, seed_meanings)
    ]
    csv_path = ROOT / "TZPID_CORPUS_SYMBOL_INDEX.csv"
    json_path = ROOT / "TZPID_CORPUS_SYMBOL_INDEX.json"
    md_path = ROOT / "TZPID_CORPUS_SYMBOL_INDEX.md"
    curated_csv_path = ROOT / "TZPID_CORPUS_SYMBOL_INDEX_CURATED.csv"
    curated_json_path = ROOT / "TZPID_CORPUS_SYMBOL_INDEX_CURATED.json"
    curated_md_path = ROOT / "TZPID_CORPUS_SYMBOL_INDEX_CURATED.md"
    fields = list(rows[0].keys()) if rows else []
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    with curated_csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(curated_rows)
    json_path.write_text(
        json.dumps(
            {
                "provenance": {
                    **PROVENANCE,
                    "generator": Path(__file__).name,
                    "generated_at_utc": generated_at,
                    "master": str(MASTER),
                    "master_sha1": sha1(MASTER),
                    "seed_sources": [str(TRAWIN_SYMBOLS), str(SYMBOL_TXT)],
                },
                "symbol_count": len(rows),
                "curated_symbol_count": len(curated_rows),
                "confidence_counts": dict(Counter(row["confidence"] for row in rows)),
                "curated_confidence_counts": dict(Counter(row["confidence"] for row in curated_rows)),
                "symbols": rows,
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    curated_json_path.write_text(
        json.dumps(
            {
                "provenance": {
                    **PROVENANCE,
                    "generator": Path(__file__).name,
                    "generated_at_utc": generated_at,
                    "master": str(MASTER),
                    "master_sha1": sha1(MASTER),
                    "seed_sources": [str(TRAWIN_SYMBOLS), str(SYMBOL_TXT)],
                    "note": "Curated high-signal subset of the full corpus symbol index.",
                },
                "symbol_count": len(curated_rows),
                "confidence_counts": dict(Counter(row["confidence"] for row in curated_rows)),
                "symbols": curated_rows,
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    lines = [
        "# TZPID Corpus Symbol Index",
        "",
        f"Generated UTC: {generated_at}",
        f"Creator: {PROVENANCE['creator']} ({PROVENANCE['creator_orcid_url']})",
        "",
        f"Symbols indexed: **{len(rows)}**",
        "",
        "| Symbol | Meaning | Confidence | Occurrences | Sample IDs |",
        "|---|---|---:|---:|---|",
    ]
    for row in rows[:300]:
        lines.append(
            f"| `{row['symbol']}` | {row['meaning']} | {row['confidence']} | {row['occurrence_count']} | {row['sample_ids']} |"
        )
    lines.extend(
        [
            "",
            "The CSV/JSON files contain the full symbol index. Rows marked `needs_definition` are known corpus symbols whose meaning still needs a human or source-backed definition.",
            "",
        ]
    )
    md_path.write_text("\n".join(lines), encoding="utf-8")
    curated_lines = [
        "# TZPID Curated Corpus Symbol Index",
        "",
        f"Generated UTC: {generated_at}",
        f"Creator: {PROVENANCE['creator']} ({PROVENANCE['creator_orcid_url']})",
        "",
        f"Curated symbols indexed: **{len(curated_rows)}**",
        "",
        "| Symbol | Meaning | Confidence | Occurrences | Sample IDs |",
        "|---|---|---:|---:|---|",
    ]
    for row in curated_rows[:600]:
        curated_lines.append(
            f"| `{row['symbol']}` | {row['meaning']} | {row['confidence']} | {row['occurrence_count']} | {row['sample_ids']} |"
        )
    curated_lines.extend(
        [
            "",
            "This curated file removes obvious prose tokens from the raw symbol index and keeps seeded symbols, math-like symbols, and recurring technical identifiers.",
            "",
        ]
    )
    curated_md_path.write_text("\n".join(curated_lines), encoding="utf-8")
    return rows, curated_rows


def is_curated_symbol_row(row, seed_meanings):
    symbol = row["symbol"]
    count = int(row["occurrence_count"])
    if symbol in seed_meanings or symbol in KNOWN_SYMBOLS:
        return True
    if symbol.lower() in COMMON_WORDS or symbol.lower() in STOP_TOKENS:
        return False
    if len(symbol) == 1 and symbol.islower():
        return False
    if any(ord(ch) > 127 for ch in symbol):
        return True
    if "_" in symbol or "^" in symbol:
        return True
    if any(ch.isdigit() for ch in symbol):
        return True
    if len(symbol) <= 2 and (
        any(ord(ch) > 127 for ch in symbol)
        or symbol.isupper()
        or symbol in {"T", "R", "A", "W", "I", "N", "G", "E", "M", "H", "F", "L", "P", "Q", "S", "V"}
    ):
        return True
    if count >= 5 and (
        any(part in symbol.lower() for part in ["tzp", "trawin", "phi", "rho", "omega", "sigma", "lambda", "theta", "psi", "field", "tensor"])
        or row["confidence"] != "unknown"
    ):
        return True
    return False


def write_summary(module_rows, symbol_rows, curated_symbol_rows, generated_at):
    summary = {
        "provenance": {
            **PROVENANCE,
            "generator": Path(__file__).name,
            "generated_at_utc": generated_at,
            "sources": {
                "source_module_csv": str(SOURCE_CSV),
                "executable_wls": str(EXECUTABLE_WLS),
                "active_all_wls": str(ALL_WLS),
                "master": str(MASTER),
            },
        },
        "modules": {
            "count": len(module_rows),
            "all_wls_sha1": sha1(ALL_WLS),
            "executable_wls_sha1": sha1(EXECUTABLE_WLS),
        },
        "symbols": {
            "count": len(symbol_rows),
            "curated_count": len(curated_symbol_rows),
            "confidence_counts": dict(Counter(row["confidence"] for row in symbol_rows)),
            "curated_confidence_counts": dict(Counter(row["confidence"] for row in curated_symbol_rows)),
            "needs_definition": sum(1 for row in symbol_rows if row["confidence"] == "unknown"),
            "curated_needs_definition": sum(1 for row in curated_symbol_rows if row["confidence"] == "unknown"),
        },
    }
    (ROOT / "wolfram_executable_and_symbol_index_summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2, ensure_ascii=False))


def main():
    generated_at = utc_now()
    if not ALL_WLS.exists():
        raise SystemExit(f"Missing {ALL_WLS}")
    raw = ALL_WLS.read_text(encoding="utf-8-sig", errors="ignore")
    if raw.lstrip().startswith('"module_name"') or raw.lstrip().startswith("module_name"):
        SOURCE_CSV.write_text(raw, encoding="utf-8")
    elif SOURCE_CSV.exists():
        pass
    else:
        raise SystemExit("all.wls is not CSV-shaped and no preserved all_module_library_source.csv exists.")

    module_rows = read_csv(SOURCE_CSV)
    results_by_key = load_results()
    write_executable_wls(module_rows, results_by_key, generated_at)
    master_rows = read_csv(MASTER)
    symbol_rows, curated_symbol_rows = write_symbol_index(master_rows, generated_at)
    write_summary(module_rows, symbol_rows, curated_symbol_rows, generated_at)


if __name__ == "__main__":
    main()
