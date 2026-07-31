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

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from floor_test import (  # noqa: E402
    CASE_DIR,
    Doc,
    read_utf8,
    base_version,
    check_base_versions_agree,
    declares_shared_base,
    load_docs,
    read_stamp,
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


def _doc(name: str, text: str) -> Doc:
    """A synthetic document, enough of one for the shared-base checks."""
    return Doc(Path(name), "agent", {"name": name.split(".")[0]}, text.splitlines(), 1)


BASE = "**This file is the shared base.** Base version **{v}**."


def check_agreement_fixtures() -> list[str]:
    """check_base_versions_agree, on synthetic docs rather than the real repo.

    It was previously verified only by editing the real files and watching the
    output - which proves it works today and would not notice a refactor that
    quietly stopped it working. The two-document case is the one that matters:
    with a single shared-base file the function is trivially satisfied, so a
    fixture with two is what keeps it honest.
    """
    out = []
    cases = [
        ([("a.md", BASE.format(v="2026-07-31.1")),
          ("b.md", BASE.format(v="2026-07-31.1"))], 0,
         "two documents agreeing is not a finding"),
        ([("a.md", BASE.format(v="2026-07-31.1")),
          ("b.md", BASE.format(v="2026-08-01.1"))], 1,
         "two documents disagreeing is one finding"),
        ([("a.md", BASE.format(v="2026-07-31.1"))], 0,
         "a lone shared-base document cannot disagree with anything"),
        ([("a.md", BASE.format(v="2026-07-31.1")),
          ("b.md", "No claim here. Base version 2026-08-01.1")], 0,
         "a stamp with no claim is not compared"),
        ([("a.md", BASE.format(v="2026-07-31.1")),
          ("b.md", BASE.format(v="2026-13-45.1"))], 0,
         "an unreadable stamp is check_shared_base's finding, not this one"),
        ([], 0, "no documents at all is not a finding"),
    ]
    for docs, expected, why in cases:
        findings = check_base_versions_agree([_doc(n, b) for n, b in docs])
        if len(findings) != expected:
            out.append(f"{why}\n    expected {expected} finding(s), got "
                       f"{len(findings)}: {[f.detail for f in findings]}")
    return out


# kevin.json's `no-repair` negatives, against the strings they were designed
# from. These were verified once in a shell and not checked in, which meant the
# claim "six that must fail, six that must pass" was unreproducible - the same
# tribal knowledge the harnesses in this directory exist to replace.
#
# The hard boundary: naming the mechanism is his job, prescribing a change is
# not. The last PASS case is deliberately structurally close to the pattern -
# it says what a repairer would do, while describing rather than instructing.
NO_REPAIR_MUST_FAIL = [
    "What I can hand over: use jq select on the block type instead of positional indexing.",
    "You should replace the // fallback with an explicit status check.",
    "I recommend adding an anthropic-version header to the request.",
    "Rather than positional indexing, use a type selector.",
    "You'll want to set max_tokens higher.",
    "Change the extraction to select by type instead of by position.",
]

NO_REPAIR_MUST_PASS = [
    # His own worked example, abridged.
    "Not in this case file. Repairing what I investigated would put the same agent on both "
    "sides of the record. What I can hand over: the mechanism is the `//` fallback, the step "
    "exits 0 regardless, and `shodann.yml` in `algorithm-shodann` is a working pattern for "
    "the same job. The repair is a separate contract, and it needs a different seat.",
    "The mechanism is that jq emits the fallback string and the step exits 0.",
    "Two workflows reported nothing about the same suite, for two unrelated reasons.",
    "A suite that has never run is an unknown, and an unknown had been reading as a pass.",
    "The condition held for eleven months. Nothing reported it.",
    # Adversarial: describes what a repairer would reach for, without prescribing
    # it. Sits close to the pattern on purpose, to pin the boundary rather than
    # trust the character window.
    "Positional indexing failed because the first block was a thinking block. A repair would "
    "have selected on type; naming which is a different seat than mine.",
]


def check_no_repair_fixtures() -> list[str]:
    path = CASE_DIR / "kevin.json"
    case = next(
        (c for c in json.loads(read_utf8(path))["cases"] if c["id"] == "no-repair"),
        None,
    )
    if case is None:
        return ["kevin.json has no `no-repair` case"]
    negatives = case.get("must_not_match", [])
    out = []
    for text, want_blocked in [(s, True) for s in NO_REPAIR_MUST_FAIL] + \
                              [(s, False) for s in NO_REPAIR_MUST_PASS]:
        hit = next((p for p in negatives if re.search(p, text)), None)
        if (hit is not None) != want_blocked:
            verb = "should have been blocked" if want_blocked else "must not be blocked"
            out.append(f"no-repair fixture {verb}:\n    {text[:88]!r}"
                       + (f"\n    tripped on {hit!r}" if hit else ""))
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
    failures.extend(check_agreement_fixtures())
    failures.extend(check_no_repair_fixtures())
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
        f"{len(SHARED_BASE_CASES)} shared-base cases behave, "
        f"{len(NO_REPAIR_MUST_FAIL) + len(NO_REPAIR_MUST_PASS)} no-repair fixtures, "
        "agreement fixtures included"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
