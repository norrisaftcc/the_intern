#!/usr/bin/env python3
"""The stray-workflow guard, pinned against a real git repository.

`.github/workflows/checks.yml` fails CI when `git ls-files '*/.github/workflows/*'`
returns anything. That guard exists because a workflow file outside the
repository root is inert — Actions does not read it — until someone moves it,
at which point it is live with whatever it contains. This repository has been
bitten twice: `deploy.yml` sat at `projects/algocratic-futures/.github/workflows/`
for about a year, and a duplicate `ai-code-review.yml` sat beside it holding an
injectable heredoc.

The guard hangs on one subtle thing: whether git's default pathspec matching
lets `*` cross a `/`. If it does not, `*/.github/workflows/*` would fail to
match a file nested two directories deep and the guard would pass while the
hole was open. That is not something to settle by reasoning about fnmatch —
it is settled here, against the git actually installed, in a scratch
repository built for the purpose.

    python3 tests/workflow/stray_workflow_test.py

Standard library plus git.
"""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
CHECKS = REPO / ".github/workflows/checks.yml"


def read_utf8(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def pathspec() -> str:
    """The pathspec the guard actually runs, read from the workflow.

    Not a copy. An earlier version of this file held its own constant, which
    meant an edit to checks.yml - a typo, a refactor to `**`, adding `:(glob)`
    magic - would leave this test passing against stale text while the live
    guard silently degraded. That is the exact failure this guard exists to
    prevent, committed one directory over from the guard itself.
    """
    text = read_utf8(CHECKS)
    block = re.search(
        r"# STRAY_PATHSPEC_START\b(.*?)# STRAY_PATHSPEC_END", text, re.S
    )
    if not block:
        raise SystemExit(
            "no STRAY_PATHSPEC_START/END markers in "
            f"{CHECKS.relative_to(REPO)}.\n"
            "They delimit the pathspec this test exercises. If the guard moved, "
            "move the markers with it - do not delete this test."
        )
    assignment = re.search(r"STRAY_PATHSPEC='(.*?)'", block.group(1), re.S)
    if not assignment:
        raise SystemExit(
            "found the markers but no STRAY_PATHSPEC='...' assignment between "
            "them. This test exercises whatever that variable holds."
        )
    return assignment.group(1)


PATHSPEC = pathspec()

# (files to create and track, expected matches for PATHSPEC, what it pins down)
CASES: list[tuple[list[str], list[str], str]] = [
    (
        [".github/workflows/ci.yml"],
        [],
        "a workflow at the repository root is not a match",
    ),
    (
        [".github/workflows/ci.yml", ".github/workflows/release.yml"],
        [],
        "several root workflows are still not matches",
    ),
    (
        ["projects/thing/.github/workflows/ci.yml"],
        ["projects/thing/.github/workflows/ci.yml"],
        "nested two deep is matched - the case that bit this repository twice",
    ),
    (
        ["sub/.github/workflows/ci.yml"],
        ["sub/.github/workflows/ci.yml"],
        "nested one deep is matched",
    ),
    (
        ["a/b/c/d/.github/workflows/ci.yml"],
        ["a/b/c/d/.github/workflows/ci.yml"],
        "`*` crosses several slashes - the semantics the guard depends on",
    ),
    (
        [".github/workflows/ci.yml", "projects/thing/.github/workflows/ci.yml"],
        ["projects/thing/.github/workflows/ci.yml"],
        "a root workflow does not mask a nested one",
    ),
    (
        [".github/ISSUE_TEMPLATE/bug.md", "docs/workflows/notes.md"],
        [],
        "neither a non-workflow .github file nor an unrelated workflows/ directory matches",
    ),
]

# Scope, stated so the cases above are not read as more than they are. This
# guard is about directory *depth*. A file at .github/workflows-old/ or
# .Github/workflows/ is out of its scope by design, and there is no case here
# asserting otherwise.

# The fixtures only `add` and `ls-files`, never `commit`, so no
# `git config user.*` is needed. Anything copied from here that does commit
# will need it, or it fails in a clean container with "please tell me who you
# are".


def git(*args: str, cwd: Path) -> str:
    proc = subprocess.run(
        ["git", *args], cwd=cwd, capture_output=True, text=True, check=True
    )
    return proc.stdout


def run_case(files: list[str], tmp: Path) -> list[str]:
    repo = tmp / "repo"
    if repo.exists():
        shutil.rmtree(repo)
    repo.mkdir()
    git("init", "-q", cwd=repo)
    for rel in files:
        target = repo / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("name: fixture\n", encoding="utf-8")
    git("add", "-A", cwd=repo)
    out = git("ls-files", PATHSPEC, cwd=repo)
    return sorted(line for line in out.splitlines() if line)


def main() -> int:
    if shutil.which("git") is None:
        # Not a skip. A skip that exits 0 reports success while testing
        # nothing, which is the failure mode this whole directory exists over.
        print("stray workflow test: FAILED")
        print("  git is not installed, so the pathspec was not exercised.")
        return 1

    failures = []
    with tempfile.TemporaryDirectory() as raw:
        tmp = Path(raw)
        for files, expected, why in CASES:
            got = run_case(files, tmp)
            if got != sorted(expected):
                failures.append(
                    f"{why}\n    tracked {files}\n"
                    f"    expected {sorted(expected)}, got {got}"
                )

    if failures:
        print("stray workflow test: FAILED")
        for line in failures:
            print(f"  {line}")
        print(
            "\nIf git's pathspec matching changed, the guard in checks.yml needs\n"
            "`:(glob)` magic or an explicit `--full-name` walk. Do not delete this\n"
            "test to make it pass."
        )
        return 1

    print(f"stray workflow test: {len(CASES)} pathspec cases behave")
    return 0


if __name__ == "__main__":
    sys.exit(main())
