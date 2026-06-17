import json
import re
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\TZPIDProof")
TZP_ID = ROOT / "tzp_id"
OUT_BASE = ROOT / "wolfram_source_truth_verification"

GREEK = {
    "alpha": "alpha",
    "beta": "beta",
    "gamma": "gamma",
    "Gamma": "Gamma",
    "delta": "delta",
    "Delta": "Delta",
    "epsilon": "epsilon",
    "varepsilon": "epsilon",
    "zeta": "zeta",
    "eta": "eta",
    "theta": "theta",
    "Theta": "Theta",
    "lambda": "lambda",
    "Lambda": "Lambda",
    "mu": "mu",
    "nu": "nu",
    "pi": "Pi",
    "rho": "rho",
    "sigma": "sigma",
    "tau": "tau",
    "phi": "phi",
    "Phi": "Phi",
    "psi": "psi",
    "Psi": "Psi",
    "omega": "omega",
    "Omega": "Omega",
}

FUNCTIONS = {
    "sin": "Sin",
    "cos": "Cos",
    "tan": "Tan",
    "exp": "Exp",
    "ln": "Log",
    "log": "Log",
}


def wl_string(text):
    text = "" if text is None else str(text)
    return (
        '"'
        + text.replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("\r", "\\r")
        .replace("\n", "\\n")
        .replace("\t", "\\t")
        + '"'
    )


def wl_list(strings):
    return "{" + ", ".join(wl_string(s) for s in strings) + "}"


def wl_num_list(values):
    return "{" + ", ".join(values) + "}"


def title_of(obj, fallback):
    return (
        obj.get("title")
        or obj.get("canonical_title")
        or obj.get("identity", {}).get("canonical_title")
        or obj.get("tzpid_provenance", {}).get("canonical_title")
        or fallback
    )


def canonical_latex_blocks(obj):
    canonical = obj.get("canonical_equation")
    blocks = []
    if isinstance(canonical, dict):
        value = canonical.get("latex_blocks")
        if isinstance(value, list):
            blocks.extend(str(x).strip() for x in value if str(x).strip())
        elif isinstance(value, str) and value.strip():
            blocks.append(value.strip())
        source_section = canonical.get("source_section_latex")
        if not blocks and isinstance(source_section, str) and source_section.strip():
            blocks.append(source_section.strip())
    elif isinstance(canonical, str) and canonical.strip():
        blocks.append(canonical.strip())

    if not blocks:
        theory = obj.get("theory")
        if isinstance(theory, dict):
            statement = theory.get("canonical_statement")
            if isinstance(statement, str) and statement.strip():
                blocks.append(statement.strip())
    return blocks or ["NO_CANONICAL_LATEX_BLOCK_PRESENT"]


def strip_latex_wrappers(text):
    s = text.strip()
    s = re.sub(r"\\\[|\\\]", " ", s)
    s = re.sub(r"\\begin\{[^}]+\}|\\end\{[^}]+\}", " ", s)
    s = s.replace("&", " ")
    s = s.replace("\\\\", " ")
    s = re.sub(r"\s+", " ", s).strip()
    return s


def extract_numbers(latex):
    numbers = []
    for a, b in re.findall(r"\\frac\{([+-]?\d+(?:\.\d+)?)\}\{([+-]?\d+(?:\.\d+)?)\}", latex):
        numbers.append(f"{a}/{b}")
    for num in re.findall(r"(?<![A-Za-z])(?:[+-]?\d+\.\d+|[+-]?\d+)(?:[eE][+-]?\d+)?", latex):
        numbers.append(num)
    seen = set()
    clean = []
    for n in numbers:
        if n not in seen:
            seen.add(n)
            clean.append(n)
    return clean


def extract_symbols(latex):
    symbols = []
    for cmd in re.findall(r"\\([A-Za-z]+)", latex):
        if cmd in {
            "frac",
            "left",
            "right",
            "begin",
            "end",
            "text",
            "mathrm",
            "mathcal",
            "operatorname",
            "cdot",
            "times",
            "approx",
            "sim",
            "to",
            "leq",
            "geq",
            "infty",
            "quad",
            "qquad",
        }:
            continue
        symbols.append(GREEK.get(cmd, cmd))
    scrubbed = re.sub(r"\\[A-Za-z]+(?:\{[^{}]*\})?", " ", latex)
    for token in re.findall(r"[A-Za-z][A-Za-z0-9]*", scrubbed):
        if token.lower() in {"where", "with", "for", "and", "or", "the", "text", "kHz"}:
            continue
        symbols.append(token)
    seen = set()
    clean = []
    for sym in symbols:
        if sym not in seen:
            seen.add(sym)
            clean.append(sym)
    return clean[:80]


def replace_frac_once(s):
    pattern = re.compile(r"\\frac\{([^{}]+)\}\{([^{}]+)\}")
    return pattern.sub(r"((\1)/(\2))", s)


def sanitize_symbol_name(name):
    name = re.sub(r"[^A-Za-z0-9$]", "$", name)
    if not name:
        return "sym"
    if name[0].isdigit():
        name = "n" + name
    return name


def heuristic_candidate(latex):
    raw = strip_latex_wrappers(latex)
    if not raw or raw == "NO_CANONICAL_LATEX_BLOCK_PRESENT":
        return "", "no_source"
    if re.search(r"\\text\{|[“”]|&#|<br|</|\\begin\{enumerate\}", raw):
        return "", "contains_text_or_markup"
    if re.search(r"\b(is|are|defined|velocity|drops|including|like|check|canonical|structure)\b", raw, re.I):
        return "", "contains_prose"
    if any(token in raw for token in ["[]", "y[:", "params_", "blob_", "threshold_", "(*"]):
        return "", "code_fragment_or_placeholder"

    s = raw
    s = s.replace(r"\ ", "*")
    for _ in range(8):
        new = replace_frac_once(s)
        if new == s:
            break
        s = new

    # A focused conversion for the common TZP limit pattern.
    lim_match = re.match(
        r"\\lim_\{\\?([A-Za-z]+)\\to\\infty\}\\?([A-Za-z]+)\((\\?[A-Za-z]+)\)\s*=\s*([A-Za-z]+),?",
        s,
    )
    if lim_match:
        var, fn, arg, rhs = lim_match.groups()
        var = GREEK.get(var.replace("\\", ""), var.replace("\\", ""))
        fn = GREEK.get(fn.replace("\\", ""), fn.replace("\\", ""))
        arg = GREEK.get(arg.replace("\\", ""), arg.replace("\\", ""))
        return f"HoldForm[Limit[{fn}[{arg}], {var} -> Infinity] == {rhs}]", "heuristic_limit"

    for cmd, repl in GREEK.items():
        s = re.sub(rf"\\{cmd}\b", repl, s)
    for cmd, repl in FUNCTIONS.items():
        s = re.sub(rf"\\{cmd}\b", repl, s)

    s = re.sub(r"\\operatorname\{([^{}]+)\}", lambda m: sanitize_symbol_name(m.group(1)), s)
    s = re.sub(r"\\mathrm\{([^{}]+)\}", lambda m: sanitize_symbol_name(m.group(1)), s)
    s = re.sub(r"\\mathcal\{([^{}]+)\}", lambda m: "cal" + sanitize_symbol_name(m.group(1)), s)
    s = re.sub(r"\\mathbb\{([^{}]+)\}", lambda m: "bb" + sanitize_symbol_name(m.group(1)), s)
    s = re.sub(r"\\hat\{([^{}]+)\}", lambda m: "hat" + sanitize_symbol_name(m.group(1)), s)

    replacements = {
        r"\cdot": "*",
        r"\times": "*",
        r"\,": "",
        r"\!": "",
        r"\;": "",
        r"\:": "",
        r"\left": "",
        r"\right": "",
        r"\leq": "<=",
        r"\geq": ">=",
        r"\neq": "!=",
        r"\approx": "==",
        r"\sim": "==",
        r"\|": "|",
    }
    for old, new in replacements.items():
        s = s.replace(old, new)

    s = re.sub(r"_\{([^{}]+)\}", lambda m: "$" + sanitize_symbol_name(m.group(1)), s)
    s = re.sub(r"_([A-Za-z0-9])", lambda m: "$" + m.group(1), s)
    s = re.sub(r"\^\{([^{}]+)\}", r"^(\1)", s)
    s = s.replace("{", "(").replace("}", ")")
    s = re.sub(r"([A-Za-z][A-Za-z0-9$]*)\(([^()]+)\)", r"\1[\2]", s)

    # Avoid Mathematica parse traps from non-WL tuple/vector and bracket conventions.
    if re.search(r"\([^()]*,[^()]*\)", s):
        return "", "tuple_notation_requires_semantic_translation"
    if re.search(r"(?<![A-Za-z0-9$])\[[^\]]+", s):
        return "", "commutator_or_list_notation_requires_semantic_translation"
    if "|" in s:
        return "", "absolute_value_or_norm_requires_semantic_translation"
    if ":" in s:
        return "", "definition_syntax_requires_semantic_translation"

    # Binary logic conversions for simple top-level forms.
    for op, head in [(r"\\Longleftrightarrow", "Equivalent"), (r"\\implies", "Implies")]:
        if op in s:
            left, right = s.split(op, 1)
            s = f"{head}[{left.strip()}, {right.strip()}]"
            break

    if re.search(r"\\[A-Za-z]+", s):
        return "", "untranslated_latex_command"

    # Convert standalone single equality to Wolfram equality.
    s = re.sub(r"(?<![<>=!])=(?!=)", "==", s)
    s = s.strip(" ,.;")
    if not s:
        return "", "empty_after_normalization"
    if any(ch in s for ch in ["#", "$$", "…", "'", '"']):
        return "", "unsupported_character"
    if not balanced(s):
        return "", "unbalanced_candidate"
    return f"HoldForm[{s}]", "heuristic_symbolic_candidate"


def balanced(s):
    pairs = {")": "(", "]": "["}
    stack = []
    for ch in s:
        if ch in "([":
            stack.append(ch)
        elif ch in pairs:
            if not stack or stack[-1] != pairs[ch]:
                return False
            stack.pop()
    return not stack


def representation_input(tzpid, title, index, latex, numbers, symbols, candidate, candidate_method):
    kind = "numeric_symbolic" if numbers else "symbolic"
    if not candidate:
        kind = "symbolic_token_index"
    assoc = (
        "<|"
        f"\"kind\" -> {wl_string(kind)}, "
        f"\"title\" -> {wl_string(title)}, "
        f"\"latex\" -> {wl_string(latex)}, "
        f"\"numericAtoms\" -> {wl_num_list(numbers)}, "
        f"\"symbolicTokens\" -> {wl_list(symbols)}, "
        f"\"candidateWolframInput\" -> {wl_string(candidate)}, "
        f"\"candidateMethod\" -> {wl_string(candidate_method)}"
        "|>"
    )
    return f"HoldForm[TZPIDWolframRepresentation[{wl_string(tzpid)}, {index}, {assoc}]]"


def main():
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    run_stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    OUT_BASE.mkdir(parents=True, exist_ok=True)
    changed = []

    for path in sorted(TZP_ID.glob("ID*/ID*.source_truth.json")):
        obj = json.loads(path.read_text(encoding="utf-8"))
        tzpid = path.parent.name
        title = title_of(obj, tzpid)
        blocks = canonical_latex_blocks(obj)
        rep_blocks = []
        for index, latex in enumerate(blocks, start=1):
            numbers = extract_numbers(latex)
            symbols = extract_symbols(latex)
            candidate, candidate_method = heuristic_candidate(latex)
            rep_blocks.append(
                {
                    "block_index": index,
                    "latex": latex,
                    "numeric_atoms": numbers,
                    "symbolic_tokens": symbols,
                    "candidate_wolfram_input": candidate,
                    "candidate_method": candidate_method,
                    "wolfram_input": representation_input(
                        tzpid, title, index, latex, numbers, symbols, candidate, candidate_method
                    ),
                    "representation_parse_status": "pending_wolfram_parse_check",
                    "candidate_parse_status": "pending_wolfram_parse_check" if candidate else "not_attempted",
                }
            )

        obj["wolfram_representation"] = {
            "schema": "tzpid_wolfram_representation_v1",
            "created_at_utc": stamp,
            "scope": "per-ID numeric atom and symbolic token representation with best-effort Wolfram candidates",
            "status": "pending_wolfram_parse_verification",
            "blocks": rep_blocks,
        }
        path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        changed.append({"id": tzpid, "path": str(path), "blocks": len(rep_blocks)})

    report = {
        "created_at_utc": stamp,
        "changed_count": len(changed),
        "changed": changed,
    }
    report_path = OUT_BASE / f"build_wolfram_representations_report_{run_stamp}.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(report_path)


if __name__ == "__main__":
    main()
