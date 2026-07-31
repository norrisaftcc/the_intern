#!/usr/bin/env python3
"""The case-file lint must not have the bug it lints for.

`unanchored_branches` splits a regex on top-level `|`. Its first version
counted `(`/`[` and `)`/`]` interchangeably, so a literal `)` inside a
character class decremented the group depth and moved the alternation
boundaries. Patterns that should have been flagged came back clean - a linter
carrying exactly the class of subtle regex defect it exists to catch.

    python3 tests/csi/lint_test.py

Standard library only, matching the rest of tests/csi/.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from floor_test import unanchored_branches  # noqa: E402

# (pattern, expected flagged branches, what it pins down)
CASES: list[tuple[str, list[str], str]] = [
    (r"(?i)cannot|can't|no", ["no"],
     "the original defect: a bare short branch is flagged"),
    (r"(?i)\bno", [],
     "a leading \\b clears it"),
    (r"(?i)(foo[)]bar)|no", ["no"],
     "a literal ) inside a class is not a group close"),
    (r"(?i)[(]a|no", ["no"],
     "a literal ( inside a class is not a group open"),
    (r"(?i)[]]x|no", ["no"],
     "] is literal as the first character of a class"),
    (r"(?i)[^]]x|no", ["no"],
     "] is literal directly after a leading ^"),
    (r"(?i)a[|]b|no", ["no"],
     "a literal | inside a class does not split a branch"),
    (r"(?i)\|no", [],
     "an escaped pipe does not split a branch"),
    (r"(?i)(a|b)|no", ["no"],
     "alternation inside a group stays inside it"),
    (r"(?i)\b(it is|this is) a (good|bad)\b", [],
     "short words bounded by surrounding context are not findings"),
    (r"(?i)RED", ["RED"],
     "a whole pattern that is one bare word is flagged"),
    (r"(?i)entit|creat", ["entit", "creat"],
     "stems are flagged too; a leading \\b is what they need, not a trailing one"),
]


def main() -> int:
    failures = []
    for pattern, expected, why in CASES:
        got = unanchored_branches(pattern)
        if got != expected:
            failures.append(f"{why}\n    {pattern!r}\n    expected {expected}, got {got}")

    if failures:
        print("lint test: FAILED")
        for line in failures:
            print(f"  {line}")
        return 1

    print(f"lint test: {len(CASES)} regex-parser cases behave")
    return 0


if __name__ == "__main__":
    sys.exit(main())
