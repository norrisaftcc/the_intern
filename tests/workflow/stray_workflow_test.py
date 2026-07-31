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

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

PATHSPEC = "*/.github/workflows/*"

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
