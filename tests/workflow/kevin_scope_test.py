#!/usr/bin/env python3
"""Kevin's write scope, enforced by the harness rather than by his prompt.

`docs/csi/ROSTER.md` states the principle: limits are structural where they can
be. VITA has no Write tool, so "never write a student's code" is a fact about
the tool list rather than a promise in a prompt.

Kevin did not meet it. He is the roster's *control* — the agent that says when
the others are wrong — and his path limit was one sentence he could be talked
out of. He was reconstructed from a workflow that reported success for a year
while producing nothing, which makes an advisory boundary on him the same shape
as the defect he exists to find.

`.claude/hooks/kevin-forensics-only.sh` is the enforcement. This exercises it.

The hook is scoped by `agent_type`, a field subagent payloads carry and the
main thread's does not — established by probing a real payload, not assumed. So
the cases below check both halves: that Kevin is held, and that nobody else is.

    python3 tests/workflow/kevin_scope_test.py

Standard library plus bash and jq.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
HOOK = REPO / ".claude/hooks/kevin-forensics-only.sh"
SETTINGS = REPO / ".claude/settings.json"

# (agent_type, file_path, expect_denied, what it pins down)
CASES: list[tuple[str | None, str, bool, str]] = [
    ("kevin", "artifacts/forensics/2026-07-31-a-case.md", False,
     "his own directory is where he works"),
    ("kevin", str(REPO / "artifacts/forensics/absolute.md"), False,
     "an absolute path into that directory is the same place"),
    ("kevin", "docs/csi/ROSTER.md", True,
     "the roster is not his to edit"),
    ("kevin", "artifacts/casefiles/kai.md", True,
     "Kai's case files are hers; same unit, different job, separate paths"),
    ("kevin", "/etc/passwd", True,
     "nor anything outside the repository"),
    ("kevin", "artifacts/forensics/../../docs/sneak.md", True,
     "traversal out of the directory is not a way back in - the reason the "
     "check resolves the path instead of matching a prefix"),
    ("kevin", "artifacts/forensics-notes/x.md", True,
     "a directory that merely starts with the allowed name is not it"),
    ("general-purpose", "docs/csi/ROSTER.md", False,
     "another agent's writes are not this hook's business"),
    (None, "docs/csi/ROSTER.md", False,
     "the main thread carries no agent_type and is never held"),
]


def read_utf8(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def decision(agent: str | None, file_path: str) -> str:
    payload = {
        "cwd": str(REPO),
        "agent_type": agent,
        "hook_event_name": "PreToolUse",
        "tool_name": "Write",
        "tool_input": {"file_path": file_path, "content": "x"},
    }
    proc = subprocess.run(
        ["bash", str(HOOK)],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        # A hook that exits non-zero blocks the tool for reasons of its own,
        # which is worse than not having one.
        return f"error(exit {proc.returncode}): {proc.stderr.strip()[:120]}"
    try:
        out = json.loads(proc.stdout or "{}")
    except json.JSONDecodeError:
        return f"unparseable: {proc.stdout.strip()[:120]}"
    return out.get("hookSpecificOutput", {}).get("permissionDecision", "allow")


def check_settings_points_at_the_hook() -> list[str]:
    """The hook only matters if settings.json actually invokes it.

    A correct script nothing calls is the defect this repository keeps finding,
    so the wiring is checked rather than assumed.
    """
    try:
        settings = json.loads(read_utf8(SETTINGS))
    except (OSError, json.JSONDecodeError) as exc:
        return [f".claude/settings.json is missing or unparseable: {exc}"]

    commands = [
        h.get("command", "")
        for entry in settings.get("hooks", {}).get("PreToolUse", [])
        if "Write" in entry.get("matcher", "")
        for h in entry.get("hooks", [])
    ]
    if not any("kevin-forensics-only.sh" in c for c in commands):
        return [
            "no PreToolUse/Write hook in .claude/settings.json invokes "
            "kevin-forensics-only.sh - the script exists but nothing runs it"
        ]
    return []


def main() -> int:
    for tool in ("bash", "jq"):
        if shutil.which(tool) is None:
            print("kevin scope test: FAILED")
            print(f"  {tool} is not installed, so the hook was not exercised.")
            print("  This is a failure, not a skip - the hook shells out to it.")
            return 1
    if not HOOK.exists():
        print("kevin scope test: FAILED")
        print(f"  {HOOK.relative_to(REPO)} is missing.")
        return 1

    failures = check_settings_points_at_the_hook()
    for agent, path, expect_denied, why in CASES:
        got = decision(agent, path)
        want = "deny" if expect_denied else "allow"
        if got != want:
            failures.append(f"{why}\n    agent={agent!r} path={path!r}\n"
                            f"    expected {want}, got {got}")

    if failures:
        print("kevin scope test: FAILED")
        for line in failures:
            print(f"  {line}")
        return 1

    print(f"kevin scope test: {len(CASES)} write-scope cases behave")
    return 0


if __name__ == "__main__":
    sys.exit(main())
