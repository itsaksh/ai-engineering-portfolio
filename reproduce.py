"""Reproduce issue #296 against the real quality check at a revision or checkout."""
import argparse
import json
from pathlib import Path
import re
import subprocess
import tempfile
import types

RELATIVE = ".github/quality/tests/test_repository_quality.py"
CASES = [
    ("misdecoded_em_dash", "The result \u00e2\u20ac\u201d is ready", True),
    ("misdecoded_apostrophe", "It\u00e2\u20ac\u2122s ready", True),
    ("existing_accent_marker", "caf\u00c3\u00a9", True),
    ("existing_box_marker", "\u00e2\u201d", True),
    ("replacement_character", "invalid \ufffd", True),
    ("valid_punctuation", "The result \u2014 it\u2019s ready.", False),
    ("valid_multilingual", "caf\u00e9, S\u00e3o Paulo, \u65e5\u672c\u8a9e, \u0928\u092e\u0938\u094d\u0924\u0947", False),
    ("valid_a_circumflex", "A valid character: \u00e2", False),
]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkout", required=True, type=Path)
    parser.add_argument("--revision", help="Optional full 40-character Git commit SHA")
    parser.add_argument("--git", default="git")
    parser.add_argument("--expect", choices=["before", "after"], required=True)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    checkout = args.checkout.resolve()
    if args.revision:
        if not re.fullmatch("[0-9a-fA-F]{40}", args.revision):
            parser.error("revision must be a full commit SHA")
        source = subprocess.check_output([args.git, "-C", str(checkout), "show", f"{args.revision}:{RELATIVE}"])
    else:
        source = (checkout / RELATIVE).read_bytes()
    module = types.ModuleType("issue296_quality_check")
    module.__file__ = str(checkout / RELATIVE)
    exec(compile(source, module.__file__, "exec"), module.__dict__)
    results = []
    with tempfile.TemporaryDirectory() as directory:
        for name, text, expected in CASES:
            sample = Path(directory) / f"{name}.md"
            sample.write_text(text, encoding="utf-8")
            try:
                module.test_markdown_has_no_common_encoding_corruption(sample)
                rejected = False
            except AssertionError:
                rejected = True
            results.append({"case": name, "expected_rejected": expected, "actual_rejected": rejected,
                            "correct": expected == rejected})
    record = {"phase": args.expect, "revision": args.revision or "working checkout",
              "issue": "https://github.com/FinanceFlash/unvibecode/issues/296", "results": results}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(record, indent=2)+"\n", encoding="utf-8", newline="\n")
    misses = [r["case"] for r in results if not r["correct"]]
    expected = ["misdecoded_em_dash", "misdecoded_apostrophe"] if args.expect == "before" else []
    if misses != expected:
        raise SystemExit(f"Unexpected outcomes: {misses}")
    print(json.dumps({"phase": args.expect, "cases": len(results), "known_misses": misses}, indent=2))


if __name__ == "__main__":
    main()
