#!/usr/bin/env python3
"""Regression test for the ai-review response extraction.

The guard this covers was almost removed an hour after it was added. The
workflow originally read `.content[0].text`, which broke the moment the model
put a thinking block first. The repair selected by type instead. A later
cleanup swapped `add` for `join` to stop adjacent text blocks running
together - correct in itself, and it would have silently disarmed the guard,
because `join` on an empty list returns "" and `jq -e` treats "" as success.

That was caught by hand. This is so it does not need to be caught by hand
again.

The jq program is read out of the workflow rather than copied here. A test
holding its own copy of the expression passes while the workflow drifts, which
is the failure mode it exists to prevent.

    python3 tests/workflow/extraction_test.py

Exit 0 means the extraction behaves. Standard library plus jq, matching
tests/csi/floor_test.py.
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
WORKFLOW = REPO_ROOT / ".github/workflows/ai-code-review.yml"

# (name, response body, expect_exit_zero, expected stdout when it succeeds)
CASES = [
    (
        "thinking then text",
        {"content": [{"type": "thinking", "thinking": "..."},
                     {"type": "text", "text": "REVIEW BODY"}]},
        True,
        "REVIEW BODY",
    ),
    (
        "thinking only - the guard case",
        {"content": [{"type": "thinking", "thinking": "..."}]},
        False,
        None,
    ),
    (
        "two text blocks are separated",
        {"content": [{"type": "text", "text": "one"},
                     {"type": "text", "text": "two"}]},
        True,
        "one\n\ntwo",
    ),
    (
        "text first, no thinking",
        {"content": [{"type": "text", "text": "REVIEW BODY"}]},
        True,
        "REVIEW BODY",
    ),
    (
        "empty content list",
        {"content": []},
        False,
        None,
    ),
    (
        "tool_use block only",
        {"content": [{"type": "tool_use", "id": "x", "name": "y", "input": {}}]},
        False,
        None,
    ),
]


def read_utf8(path: Path) -> str:
    """Explicit encoding. The platform default is not a property of the file."""
    return path.read_text(encoding="utf-8")


def extraction_program() -> str:
    """Pull the jq program the workflow actually runs out of the workflow.

    Read from between explicit markers rather than scraped by matching shell
    syntax embedded in YAML. The first version of this used a regex against
    the `jq -e -r '...'` call and would have broken on any reflow of that
    block - a comment added mid-expression, a line rewrapped - failing the
    test for a reason that has nothing to do with the behaviour under test.
    """
    text = read_utf8(WORKFLOW)
    match = re.search(
        r"# EXTRACTION_PROGRAM_START\b(.*?)# EXTRACTION_PROGRAM_END",
        text,
        re.S,
    )
    if not match:
        raise SystemExit(
            "no EXTRACTION_PROGRAM_START/END markers in "
            f"{WORKFLOW.relative_to(REPO_ROOT)}.\n"
            "They delimit the jq program this test runs. If the extraction "
            "moved, move the markers with it - do not delete this test."
        )

    assignment = re.search(r"EXTRACTION='(.*?)'", match.group(1), re.S)
    if not assignment:
        raise SystemExit(
            "found the markers but no EXTRACTION='...' assignment between "
            "them. This test runs whatever that variable holds."
        )
    return assignment.group(1)


def run_case(program: str, body: dict, tmp: Path) -> tuple[int, str]:
    response = tmp / "response.json"
    response.write_text(json.dumps(body), encoding="utf-8")
    proc = subprocess.run(
        ["jq", "-e", "-r", program, str(response)],
        capture_output=True,
        text=True,
    )
    return proc.returncode, proc.stdout.rstrip("\n")


def main() -> int:
    if shutil.which("jq") is None:
        # Not a skip. A skip that exits 0 reports success while testing
        # nothing, which is the `//` fallback this whole test exists because
        # of, rewritten in Python. The workflow under test runs jq; if jq is
        # missing, this test has no opinion and must not pretend otherwise.
        print("extraction test: FAILED")
        print("  jq is not installed, so the extraction was not exercised.")
        print("  This is a failure, not a skip - the test cannot pass without")
        print("  running the program it exists to check.")
        return 1

    program = extraction_program()
    failures = []

    with tempfile.TemporaryDirectory() as raw:
        tmp = Path(raw)
        for name, body, expect_ok, expect_out in CASES:
            code, out = run_case(program, body, tmp)
            ok = (code == 0)
            if ok != expect_ok:
                failures.append(
                    f"{name}: expected {'exit 0' if expect_ok else 'non-zero exit'}, "
                    f"got exit {code}"
                )
                continue
            if expect_ok and out != expect_out:
                failures.append(f"{name}: expected {expect_out!r}, got {out!r}")

    if failures:
        print("extraction test: FAILED")
        for line in failures:
            print(f"  {line}")
        print(
            "\nIf `join` replaced a null-producing form, note that `join` on an "
            "empty list\nreturns \"\", which `jq -e` treats as success. That "
            "disarms the guard."
        )
        return 1

    print(f"extraction test: {len(CASES)} response shapes behave")
    return 0


if __name__ == "__main__":
    sys.exit(main())
