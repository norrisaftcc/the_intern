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

from floor_test import (  # noqa: E402
    base_version,
    declares_shared_base,
    load_docs,
    unanchored_branches,
)

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


# (text, declares?, version, what it pins down)
SHARED_BASE_CASES: list[tuple[str, bool, str | None, str]] = [
    ("**This file is the shared base.** Base version **2026-07-31.1**.",
     True, "2026-07-31.1", "the real declaration with a valid stamp"),
    ("**This file is the shared base**, and it is deliberately basic.",
     True, None, "declaration without a stamp is the failing case"),
    ("Base version 2026-07-31.1 appears here with no claim.",
     False, None, "a stamp with no claim is a no-op; the stamp belongs to a declaration"),
    ("**This file is the shared base.**\n\nUnrelated prose.\n\nBase version 2026-07-31.1",
     True, None, "a stamp in a later paragraph is not a stamp on the declaration"),
    ("**This file is the shared base.** Base version **2026-07-31.1**.\n"
     "Continuing the same paragraph.",
     True, "2026-07-31.1", "same paragraph, wrapped across a single newline, still counts"),
    ("This is not intended as a shared base.",
     False, None, "prose mentioning the phrase must not trip the check"),
    ("Unlike our shared base pattern, this file stands alone.",
     False, None, "the words in passing are not a declaration"),
    ("**This file is the shared base.** Base version **2026-13-45.1**.",
     True, None, "date-shaped but not a date - month 13, day 45"),
    ("**This file is the shared base.** Base version **2026-02-30.1**.",
     True, None, "date-shaped but not a date - February 30"),
    ("**this file is the shared base.** Base version 2026-07-31.2",
     True, "2026-07-31.2", "the declaration match is case-insensitive"),
]


def check_shared_base_cases() -> list[str]:
    out = []
    for text, declares, version, why in SHARED_BASE_CASES:
        got_declares = declares_shared_base(text)
        got_version = base_version(text)
        if got_declares != declares:
            out.append(f"{why}\n    declares_shared_base expected {declares}, got {got_declares}")
        if got_version != version:
            out.append(f"{why}\n    base_version expected {version!r}, got {got_version!r}")
    return out


def check_roster_is_not_loaded() -> list[str]:
    """docs/csi/ROSTER.md says "a shared base" while describing the arrangement.

    It passes today because load_docs() globs .claude/ only. That is a fact
    about the glob, not about the check, so it is pinned here rather than left
    to have happened to work.
    """
    loaded = {d.path.name for d in load_docs()}
    if "ROSTER.md" in loaded:
        return ["ROSTER.md is now loaded by the harness; it describes the shared-base "
                "arrangement without being one, so it will false-positive"]
    return []


def main() -> int:
    failures = []
    failures.extend(check_shared_base_cases())
    failures.extend(check_roster_is_not_loaded())
    for pattern, expected, why in CASES:
        got = unanchored_branches(pattern)
        if got != expected:
            failures.append(f"{why}\n    {pattern!r}\n    expected {expected}, got {got}")

    if failures:
        print("lint test: FAILED")
        for line in failures:
            print(f"  {line}")
        return 1

    print(
        f"lint test: {len(CASES)} regex-parser cases and "
        f"{len(SHARED_BASE_CASES)} shared-base cases behave"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
