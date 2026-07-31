#!/usr/bin/env python3
"""Every documented example reply must satisfy one of its persona's cases.

An agent file's Examples section and its case file are two statements of the
same contract. Nothing checked that they agreed. "20 of 20 example replies
score clean" has appeared in pull request descriptions as verification, run by
hand each time - the same tribal knowledge that `floor_test.py` and
`extraction_test.py` were, until they were wired in.

The check is one-directional on purpose. Every example must pass at least one
case; not every case needs an example, because refusal cases outnumber the
examples a persona file has room for. A case with no example is listed rather
than failed, so the gap is visible without being fatal.

    python3 tests/csi/examples_test.py
    python3 tests/csi/examples_test.py --matrix

Standard library only, matching floor_test.py.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
AGENT_DIR = REPO / ".claude/agents"
CASE_DIR = REPO / "tests/csi/cases"

EXAMPLE_SPLIT = re.compile(r"^### Example\b.*$", re.M)
# The reply runs from the persona's bolded name to the next heading.
REPLY = re.compile(r"^\*\*(?!User\b|Student\b)([A-Za-z]+)\*\*:(.*?)(?=\n#{2,3} |\Z)", re.S | re.M)


def read_utf8(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def examples(agent: Path) -> list[str]:
    """Each example's persona reply, in document order."""
    chunks = EXAMPLE_SPLIT.split(read_utf8(agent))[1:]
    out = []
    for chunk in chunks:
        match = REPLY.search(chunk)
        if match:
            out.append(match.group(2).strip())
    return out


def cases_for(persona: str) -> list[dict]:
    path = CASE_DIR / f"{persona}.json"
    if not path.exists():
        return []
    return json.loads(read_utf8(path)).get("cases", [])


def satisfies(reply: str, case: dict) -> bool:
    for pattern in case.get("must_match", []):
        if not re.search(pattern, reply):
            return False
    for pattern in case.get("must_not_match", []):
        if re.search(pattern, reply):
            return False
    return bool(case.get("must_match") or case.get("must_not_match"))


def main() -> int:
    show_matrix = "--matrix" in sys.argv
    failures: list[str] = []
    uncovered: list[str] = []
    total = 0

    for agent in sorted(AGENT_DIR.glob("*.md")):
        persona = agent.stem
        cases = cases_for(persona)
        if not cases:
            continue
        replies = examples(agent)
        if not replies:
            failures.append(f"{persona}: no example replies found in {agent.name}")
            continue

        hit_by_case: dict[str, list[int]] = {c["id"]: [] for c in cases}
        for index, reply in enumerate(replies, start=1):
            total += 1
            passed = [c["id"] for c in cases if satisfies(reply, c)]
            for cid in passed:
                hit_by_case[cid].append(index)
            if not passed:
                failures.append(
                    f"{persona} example {index}: satisfies no case in {persona}.json"
                )
            elif show_matrix:
                print(f"  {persona} example {index} -> {', '.join(passed)}")

        for cid, hits in hit_by_case.items():
            if not hits:
                uncovered.append(f"{persona}:{cid}")

    if failures:
        print("examples test: FAILED")
        for line in failures:
            print(f"  {line}")
        return 1

    print(f"examples test: {total} example replies satisfy their cases")
    if uncovered:
        print(f"  {len(uncovered)} cases with no worked example: {', '.join(uncovered)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
