import argparse
import concurrent.futures
import html
import os
import re
import sys
import warnings
from pathlib import Path

os.environ.setdefault("PYTHONWARNINGS", "ignore")
warnings.filterwarnings("ignore")

import pandas as pd
from sympy import Eq, Symbol, diff, limit, oo, parse_expr
from sympy.parsing.latex import parse_latex
from sympy.parsing.sympy_parser import (
    convert_xor,
    implicit_multiplication_application,
    standard_transformations,
)

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)



DEFAULT_CSV = "TZPID_ALL_IDS_CANONICAL_EQUATION_MASTER_with_export.csv"
DEFAULT_OUTPUT = "toe_pipeline_results.csv"
DEFAULT_SHORTLIST_OUTPUT = "toe_shortlist.csv"
DEFAULT_APPROX_OUTPUT = "toe_approximated_parse.csv"
DEFAULT_CLEANUP_OUTPUT = "toe_cleanup_queue.csv"

ID_COLUMN = "id"
EQUATION_COLUMN = "canonical_equation"
SCALE_COLUMN = "Intended_Scale"

x, y, z, t, r = Symbol("x"), Symbol("y"), Symbol("z"), Symbol("t"), Symbol("r", positive=True)
G, c, hbar, m = Symbol("G", positive=True), Symbol("c", positive=True), Symbol("hbar", positive=True), Symbol("m", positive=True)
Lambda_ToE, Psi_field = Symbol("Lambda_ToE"), Symbol("Psi_field")

custom_context = {
    "x": x,
    "y": y,
    "z": z,
    "t": t,
    "r": r,
    "G": G,
    "c": c,
    "hbar": hbar,
    "m": m,
    "I": Symbol("I"),
    "N": Symbol("N"),
    "Lambda": Symbol("Lambda"),
    "GoldenRatio": Symbol("GoldenRatio"),
    "Lambda_ToE": Lambda_ToE,
    "Psi_field": Psi_field,
}

PARSE_TRANSFORMATIONS = standard_transformations + (implicit_multiplication_application, convert_xor)

CODE_OR_PROSE_PATTERNS = re.compile(
    r"Join-Path|env:|ErrorActionPreference|Category\[|Module\[|Association\[|"
    r"def\s+\w+\(|Preserves symplectic|energy conservation|canonical structure|"
    r"\bvelocity\b|\bstructure spans\b|\bFundamental Dimensions\b",
    re.IGNORECASE,
)

UNICODE_MATH_MAP = {
    "Φ": r"\Phi",
    "φ": r"\phi",
    "Ψ": r"\Psi",
    "ψ": r"\psi",
    "Λ": r"\Lambda",
    "λ": r"\lambda",
    "Ω": r"\Omega",
    "ω": r"\omega",
    "Σ": r"\Sigma",
    "σ": r"\sigma",
    "μ": r"\mu",
    "ν": r"\nu",
    "π": r"\pi",
    "θ": r"\theta",
    "τ": r"\tau",
    "γ": r"\gamma",
    "ρ": r"\rho",
    "η": r"\eta",
    "∑": r"\sum",
    "∫": r"\int",
    "∮": r"\oint",
    "∂": r"\partial",
    "∇": r"\nabla",
    "√": r"\sqrt",
    "≤": r"\leq",
    "≥": r"\geq",
    "≠": r"\neq",
    "≈": r"\approx",
    "∈": r"\in",
    "⊂": r"\subset",
    "→": r"\to",
    "↦": r"\mapsto",
    "⇒": r"\implies",
    "⇔": r"\Longleftrightarrow",
    "×": r"\times",
    "⋅": r"\cdot",
    "−": "-",
    "ℓ": r"\ell",
    "𝒪": "O",
    "𝟙": "1",
    "Ĥ": r"\hat{H}",
    "Ĵ": r"\hat{J}",
}

SUBSCRIPT_DIGITS = str.maketrans("₀₁₂₃₄₅₆₇₈₉", "0123456789")
SUPERSCRIPT_DIGITS = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹", "0123456789")


def decode_export_escapes(text):
    text = text.replace("\\textbackslash", "\\")
    text = text.replace("textbackslash", "\\")
    text = text.replace("\\_", "_")
    text = text.replace("\\{", "{")
    text = text.replace("\\}", "}")
    text = text.replace("\\^{}", "^")
    text = text.replace("\\textbar", "|")
    return text


def unicode_math_to_latex(text):
    for source, target in UNICODE_MATH_MAP.items():
        text = text.replace(source, target)
    text = re.sub(r"([A-Za-z\\][A-Za-z{}\\]*)\s*([₀₁₂₃₄₅₆₇₈₉]+)", lambda m: f"{m.group(1)}_{m.group(2).translate(SUBSCRIPT_DIGITS)}", text)
    text = re.sub(r"([A-Za-z\\][A-Za-z{}\\]*)\s*([⁰¹²³⁴⁵⁶⁷⁸⁹]+)", lambda m: f"{m.group(1)}^{m.group(2).translate(SUPERSCRIPT_DIGITS)}", text)
    return text


def strip_latex_environments(text):
    text = re.sub(r"\\begin\s*\{(?:equation|align|aligned|definition|pmatrix|bmatrix|matrix)\*?\}", " ", text)
    text = re.sub(r"\\end\s*\{(?:equation|align|aligned|definition|pmatrix|bmatrix|matrix)\*?\}", " ", text)
    return text


def has_math_signal(text):
    return bool(re.search(r"[=<>_^\\∫∑√]|\\frac|\\int|\\sum|\\lim", text))


def extract_inline_math(text):
    fragments = []
    patterns = [
        r"\$\$([^$]+)\$\$",
        r"\$([^$]+)\$",
        r"\\\[([^\]]+)\\\]",
        r"\\\(([^)]+)\\\)",
    ]
    for pattern in patterns:
        fragments.extend(match.group(1) for match in re.finditer(pattern, text, flags=re.DOTALL))

    math_fragments = [fragment.strip() for fragment in fragments if has_math_signal(fragment)]
    if math_fragments:
        return " || ".join(math_fragments)
    return text


def normalize_equation_text(equation_text):
    text = html.unescape(str(equation_text))
    text = decode_export_escapes(text)
    text = unicode_math_to_latex(text)
    text = strip_latex_environments(text)
    text = extract_inline_math(text)
    return text


def normalize_text_command(match):
    content = match.group(1).strip()
    if re.fullmatch(r"[A-Za-z][A-Za-z0-9_-]*", content):
        return rf"\mathrm{{{content}}}"
    return ""


def normalize_segment(segment):
    text = normalize_equation_text(segment).strip()
    text = re.sub(r"<[^>]+>", " ", text)
    text = text.replace("$$", "")
    text = re.sub(r"\\\[(.*?)\\\]", r"\1", text)
    text = re.sub(r"\\\((.*?)\\\)", r"\1", text)
    text = text.strip("$")
    text = re.sub(r"^\s*[-*]\s+", "", text)
    text = re.sub(r"^\s*\d+\.\s*", "", text)
    text = text.strip(" ,.;")
    text = text.replace("\\\\", "\\")
    text = text.replace("\\!", "")
    text = re.sub(r"([A-Za-z])'", r"\1^{\\prime}", text)
    text = text.replace("\\;", " ")
    text = text.replace("\\,", " ")
    text = re.sub(r"\\quad|\\qquad", " ", text)
    text = text.replace("\\displaystyle", "")
    text = re.sub(r"\\(?:bigl|bigr|Bigl|Bigr|biggl|biggr|Biggl|Biggr|big|Big|bigg|Bigg)", "", text)
    text = re.sub(r"\\text\s*\{([^{}]*)\}", normalize_text_command, text)
    text = re.sub(r"\\textsuperscript\s*\{([^{}]+)\}", r"^{\1}", text)
    text = text.replace("\\left", "").replace("\\right", "")
    text = text.replace(":=", "=")
    text = re.sub(r"(?<!\\)frac\{", r"\\frac{", text)
    text = re.sub(r"(?<!\\)mathcal\{", r"\\mathcal{", text)
    text = re.sub(r"(?<!\\)mathrm\{", r"\\mathrm{", text)
    text = re.sub(r"\\(sum|prod|int|oint)_([A-Za-z0-9]+)", r"\\\1_{\2}", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def equation_segments(equation_text):
    equation_text = normalize_equation_text(equation_text)
    raw_segments = re.split(
        r"\|\||\\implies|\\Longleftrightarrow|\\leftrightarrow|\\Rightarrow|⇒|⇔",
        str(equation_text),
    )
    return [segment for segment in (normalize_segment(part) for part in raw_segments) if segment]


def classify_unparsed(equation_text, errors):
    text = str(equation_text)
    if CODE_OR_PROSE_PATTERNS.search(text):
        return "Needs cleanup", "Code/prose fragment, not a direct symbolic equation"

    math_signal = re.search(r"[=<>_^\\∫∑√]|\\frac|\\int|\\sum|\\lim", text)
    if not math_signal:
        return "Needs cleanup", "No strong symbolic-math signal"

    return "Syntax Error", " | ".join(errors[:3])


def parse_plain(segment):
    text = segment.replace("^", "**")
    if "=" in text and "==" not in text:
        left, right = text.split("=", 1)
        return Eq(
            parse_expr(left, local_dict=custom_context, transformations=PARSE_TRANSFORMATIONS, evaluate=False),
            parse_expr(right, local_dict=custom_context, transformations=PARSE_TRANSFORMATIONS, evaluate=False),
            evaluate=False,
        )
    return parse_expr(text, local_dict=custom_context, transformations=PARSE_TRANSFORMATIONS, evaluate=False)


def simplify_latex_for_approximate_parse(segment):
    text = segment
    text = text.replace(r"\displaystyle", "")
    text = re.sub(r"\\(?:int|oint)_\{[^{}]*\}", lambda m: m.group(0).split("_", 1)[0], text)
    text = re.sub(r"\\sum_\{([^{}]+)\}", lambda m: f"S_{{{m.group(1)}}}", text)
    text = re.sub(r"\\sum_([A-Za-z0-9]+)", lambda m: f"S_{{{m.group(1)}}}", text)
    text = text.replace(r"\sum", "S")
    text = re.sub(r"\\prod_\{([^{}]+)\}", lambda m: f"P_{{{m.group(1)}}}", text)
    text = re.sub(r"\\mathbf\s*\{([^{}]+)\}", r"\1", text)
    text = re.sub(r"\\hat\s*\{([^{}]+)\}", r"\1_{hat}", text)
    text = re.sub(r"\\mathcal\s*\{([^{}]+)\}", r"\1", text)
    text = re.sub(r"\\operatorname\s*\{([^{}]+)\}", r"\1", text)
    text = re.sub(r"\\mathbb\s*\{([^{}]+)\}", r"\1", text)
    text = text.replace(r"\dagger", "^{dagger}")
    text = text.replace(r"\mid", ",")
    text = text.replace(r"\otimes", "*")
    text = text.replace(r"\times", "*")
    text = text.replace(r"\cdot", "*")
    text = text.replace(r"\circ", "*")
    text = text.replace(r"\wedge", "*")
    text = text.replace(r"\leq", "=")
    text = text.replace(r"\geq", "=")
    text = text.replace(r"\approx", "=")
    text = text.replace(r"\neq", "=")
    text = text.replace(r"\sim", "=")
    for command in (
        "Delta",
        "Gamma",
        "Lambda",
        "Phi",
        "Psi",
        "Omega",
        "Sigma",
        "alpha",
        "beta",
        "gamma",
        "delta",
        "epsilon",
        "eta",
        "theta",
        "kappa",
        "lambda",
        "mu",
        "nu",
        "pi",
        "rho",
        "sigma",
        "tau",
        "varphi",
        "omega",
        "ell",
        "hbar",
    ):
        text = text.replace(rf"\{command}", command)
    text = text.replace(r"\lvert", "|").replace(r"\rvert", "|")
    text = text.replace(r"\|", "|")
    text = text.replace(r"\dots", "dots")
    text = text.replace(r"\ldots", "dots")
    text = re.sub(r"\\\{([^{}]*)\\\}", r"(\1)", text)
    text = re.sub(r"\{([^{}]*)\}", r"{\1}", text)
    return text


def segment_variants(segment):
    variants = [
        (segment, ""),
        (segment.replace("\\|", "|"), ""),
        (re.sub(r"\s*\([^()]*\)\s*$", "", segment).strip(), ""),
        (re.sub(r"\\mathrm\s*\{([^{}]+)\}", r"\1", segment), ""),
        (segment.replace("\\vert", "|"), ""),
        (simplify_latex_for_approximate_parse(segment), "unsupported LaTeX simplified"),
    ]

    unique = []
    seen = set()
    for variant, note in variants:
        variant = variant.strip(" ,.;")
        if variant and variant not in seen:
            seen.add(variant)
            unique.append((variant, note))
    return unique


def is_likely_latex(segment):
    return "\\" in segment or bool(re.search(r"[_^{}]", segment))


def parse_segment(segment):
    errors = []
    for variant, note in segment_variants(segment):
        try:
            if is_likely_latex(variant):
                try:
                    return parse_latex(variant), note
                except Exception:
                    return parse_latex(variant, backend="lark"), note
            return parse_plain(variant), note
        except Exception as exc:
            errors.append(exc)

    last_error = errors[-1]
    raise last_error


def safe_limit(expr, symbol, target):
    try:
        return limit(expr, symbol, target)
    except Exception:
        return None


def safe_text(value, max_length=500):
    try:
        text = str(value)
    except Exception as exc:
        return f"<unprintable {type(value).__name__}: {type(exc).__name__}: {exc}>"
    if len(text) > max_length:
        return f"{text[:max_length]}... <truncated {len(text)} chars>"
    return text


def verify_toe_candidate(row):
    equation_text = row.get(EQUATION_COLUMN, "")
    scale = row.get(SCALE_COLUMN, "Universal")
    segments = equation_segments(equation_text)

    if not segments:
        return {
            "status": "Needs cleanup",
            "reason": "Empty equation",
            "segment_count": 0,
            "normalized_candidate": "",
        }

    parsed = []
    errors = []
    parse_notes = []

    for segment in segments:
        try:
            expr, note = parse_segment(segment)
            parsed.append((segment, expr))
            if note:
                parse_notes.append(note)
        except Exception as exc:
            errors.append(f"{segment[:80]} -> {type(exc).__name__}: {exc}")

    if not parsed:
        status, reason = classify_unparsed(equation_text, errors)
        return {
            "status": status,
            "reason": reason,
            "segment_count": len(segments),
            "parse_errors": len(errors),
            "normalized_candidate": " || ".join(segments),
            "first_error": errors[0] if errors else "",
        }

    flags = []
    macro_boundaries = []

    for _, expr in parsed:
        for symbol in (t, r):
            planck_limit = safe_limit(expr, symbol, 0)
            if planck_limit in (oo, -oo):
                flags.append(f"Infinity as {symbol} -> 0")

        if scale == "Quantum":
            try:
                gradient_check = diff(expr, x) + diff(expr, y)
                if gradient_check == 0:
                    flags.append("Trivial static field anomaly")
            except Exception:
                pass

        macro_limit = safe_limit(expr, t, oo)
        if macro_limit is not None:
            macro_boundaries.append(safe_text(macro_limit))

    if flags:
        status = "Flagged"
        reason = "; ".join(dict.fromkeys(flags))
    elif errors:
        status = "Partial Parse"
        reason = "Some segments need cleanup"
    elif parse_notes:
        status = "Approximated Parse"
        reason = "; ".join(dict.fromkeys(parse_notes))
    else:
        status = "Passed"
        reason = ""

    return {
        "status": status,
        "reason": reason,
        "segment_count": len(segments),
        "parsed_segments": len(parsed),
        "parse_errors": len(errors),
        "parse_notes": "; ".join(dict.fromkeys(parse_notes)),
        "normalized_candidate": " || ".join(segments),
        "parsed_math": " || ".join(safe_text(expr) for _, expr in parsed),
        "macro_boundary": " || ".join(macro_boundaries),
        "first_error": errors[0] if errors else "",
    }


def build_result(index_and_row):
    idx, row = index_and_row
    res = verify_toe_candidate(row)
    res["ID"] = row.get(ID_COLUMN, idx)
    res["title"] = row.get("title", "")
    res[EQUATION_COLUMN] = row.get(EQUATION_COLUMN, "")
    return res


def run_pipeline(
    csv_path=DEFAULT_CSV,
    output_path=DEFAULT_OUTPUT,
    limit_rows=None,
    workers=1,
    shortlist_output_path=DEFAULT_SHORTLIST_OUTPUT,
    approx_output_path=DEFAULT_APPROX_OUTPUT,
    cleanup_output_path=DEFAULT_CLEANUP_OUTPUT,
):
    csv_path = Path(csv_path)
    output_path = Path(output_path)
    shortlist_output_path = Path(shortlist_output_path)
    approx_output_path = Path(approx_output_path)
    cleanup_output_path = Path(cleanup_output_path)

    df = pd.read_csv(csv_path)
    if EQUATION_COLUMN not in df.columns:
        raise KeyError(f"CSV must contain '{EQUATION_COLUMN}'. Found: {', '.join(df.columns)}")

    if limit_rows:
        df = df.head(limit_rows)

    print(f"Loaded registry with {len(df)} candidate items.")

    records = list(enumerate(df.to_dict("records")))

    if workers and workers > 1:
        print(f"Using {workers} worker processes.")
        with concurrent.futures.ProcessPoolExecutor(max_workers=workers) as executor:
            results = list(executor.map(build_result, records, chunksize=25))
    else:
        results = [build_result(record) for record in records]

    results_df = pd.DataFrame(results)
    summary = results_df["status"].value_counts(dropna=False)

    print("\n--- Pipeline Execution Summary ---")
    print(summary)

    results_df.to_csv(output_path, index=False, encoding="utf-8-sig")
    print(f"\nDetailed results exported to '{output_path}'")

    passed_candidates = results_df[results_df["status"] == "Passed"]
    passed_candidates.to_csv(shortlist_output_path, index=False, encoding="utf-8-sig")
    print(f"Shortlisted candidates exported to '{shortlist_output_path}'")

    approximated_candidates = results_df[results_df["status"] == "Approximated Parse"]
    approximated_candidates.to_csv(approx_output_path, index=False, encoding="utf-8-sig")
    print(f"Approximated parses exported to '{approx_output_path}'")

    cleanup_candidates = results_df[results_df["status"].isin(["Syntax Error", "Needs cleanup"])]
    cleanup_candidates.to_csv(cleanup_output_path, index=False, encoding="utf-8-sig")
    print(f"Cleanup queue exported to '{cleanup_output_path}'")

    return results_df


def main():
    parser = argparse.ArgumentParser(description="Run TZPID equation parser and validation checks.")
    parser.add_argument("csv_path", nargs="?", default=DEFAULT_CSV)
    parser.add_argument("--output", default=DEFAULT_OUTPUT)
    parser.add_argument("--shortlist-output", default=DEFAULT_SHORTLIST_OUTPUT)
    parser.add_argument("--approx-output", default=DEFAULT_APPROX_OUTPUT)
    parser.add_argument("--cleanup-output", default=DEFAULT_CLEANUP_OUTPUT)
    parser.add_argument("--limit", type=int, default=None, help="Process only the first N rows.")
    parser.add_argument(
        "--workers",
        type=int,
        default=1,
        help=f"CPU worker processes to use. Try {max(1, (os.cpu_count() or 2) - 1)} on this machine.",
    )
    args = parser.parse_args()

    run_pipeline(
        args.csv_path,
        args.output,
        args.limit,
        args.workers,
        args.shortlist_output,
        args.approx_output,
        args.cleanup_output,
    )


if __name__ == "__main__":
    main()
