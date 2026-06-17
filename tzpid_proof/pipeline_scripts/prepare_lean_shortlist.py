import argparse
import json
from pathlib import Path

import pandas as pd


DEFAULT_INPUT = "toe_shortlist_pipeline_passed.csv"
DEFAULT_OUTPUT = "TZPIDShortlistSeed.lean"


def lean_string(value):
    return json.dumps("" if pd.isna(value) else str(value), ensure_ascii=False)


def make_identifier(raw_id):
    text = str(raw_id)
    safe = "".join(ch if ch.isalnum() else "_" for ch in text)
    if not safe or safe[0].isdigit():
        safe = f"id_{safe}"
    return safe


def build_lean(input_path, output_path, limit):
    df = pd.read_csv(input_path)
    if limit:
        df = df.head(limit)

    rows = list(df.iterrows())

    lines = [
        "/-",
        "Generated from the TZPID strict shortlist.",
        "This is a Lean-readable manifest seed, not a proof of the physics yet.",
        "The next step is to replace `FrameworkDerivable` assumptions with real TZPID axioms.",
        "-/",
        "",
        "structure TZPIDCandidate where",
        "  id : String",
        "  title : String",
        "  canonicalEquation : String",
        "  parsedMath : String",
        "deriving Repr, BEq",
        "",
        "axiom FrameworkDerivable : TZPIDCandidate -> Prop",
        "",
    ]

    candidate_names = []
    for index, row in rows:
        raw_id = row.get("ID", f"row_{index}")
        name = f"candidate_{make_identifier(raw_id)}"
        candidate_names.append(name)
        lines.extend(
            [
                f"def {name} : TZPIDCandidate :=",
                "  {",
                f"    id := {lean_string(row.get('ID', ''))},",
                f"    title := {lean_string(row.get('title', ''))},",
                f"    canonicalEquation := {lean_string(row.get('canonical_equation', ''))},",
                f"    parsedMath := {lean_string(row.get('parsed_math', ''))}",
                "  }",
                "",
                f"axiom {name}_derivable : FrameworkDerivable {name}",
                "",
            ]
        )

    lines.append("def strictShortlist : Array TZPIDCandidate := #[")
    for name in candidate_names:
        lines.append(f"  {name},")
    lines.extend(
        [
        "]",
        "",
            "theorem strictShortlist_nonempty : strictShortlist.size > 0 := by",
            "  native_decide",
            "",
        ]
    )

    lines.append("")
    Path(output_path).write_text("\n".join(lines), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Prepare a Lean manifest seed from TZPID shortlist rows.")
    parser.add_argument("--input", default=DEFAULT_INPUT)
    parser.add_argument("--output", default=DEFAULT_OUTPUT)
    parser.add_argument("--limit", type=int, default=100)
    args = parser.parse_args()
    build_lean(args.input, args.output, args.limit)


if __name__ == "__main__":
    main()
