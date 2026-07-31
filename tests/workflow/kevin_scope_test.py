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

`.claude/hooks/kevin-forensics-only.py` is the enforcement. This exercises the
real script, including the paths where it must refuse rather than guess.

    python3 tests/workflow/kevin_scope_test.py

Standard library only.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
HOOK = REPO / ".claude/hooks/kevin-forensics-only.py"
SETTINGS = REPO / ".claude/settings.json"
KEVIN = REPO / ".claude/agents/kevin.md"

# Tools that can put bytes on disk through a path argument. If Kevin ever
# gains one of these, the hook's matcher must already cover it.
WRITE_TOOLS = ("Write", "Edit", "MultiEdit", "NotebookEdit")

# (payload, expect_denied, what it pins down)
CASES: list[tuple[dict, bool, str]] = [
    ({"agent_type": "kevin", "cwd": "{repo}",
      "tool_input": {"file_path": "artifacts/forensics/2026-07-31-a-case.md"}},
     False, "his own directory is where he works"),

    ({"agent_type": "kevin", "cwd": "{repo}",
      "tool_input": {"file_path": "{repo}/artifacts/forensics/absolute.md"}},
     False, "an absolute path into that directory is the same place"),

    ({"agent_type": "kevin", "cwd": "{repo}",
      "tool_input": {"file_path": "artifacts/forensics/nested/deeper.md"}},
     False, "a subdirectory of it is still it"),

    ({"agent_type": "kevin", "cwd": "{repo}",
      "tool_input": {"file_path": "docs/csi/ROSTER.md"}},
     True, "the roster is not his to edit"),

    ({"agent_type": "kevin", "cwd": "{repo}",
      "tool_input": {"file_path": "artifacts/casefiles/kai.md"}},
     True, "Kai's case files are hers; same unit, different job, separate paths"),

    ({"agent_type": "kevin", "cwd": "{repo}",
      "tool_input": {"file_path": "/etc/passwd"}},
     True, "nor anything outside the repository"),

    ({"agent_type": "kevin", "cwd": "{repo}",
      "tool_input": {"file_path": "artifacts/forensics/../../docs/sneak.md"}},
     True, "traversal out of the directory is not a way back in"),

    ({"agent_type": "kevin", "cwd": "{repo}",
      "tool_input": {"file_path": "artifacts/forensics-notes/x.md"}},
     True, "a directory that merely starts with the allowed name is not it"),

    ({"agent_type": "kevin", "cwd": "{repo}",
      "tool_input": {"notebook_path": "notebooks/scratch.ipynb"}},
     True, "NotebookEdit names its path differently and is still covered"),

    # --- fails closed, not open ---
    ({"agent_type": "kevin", "cwd": "{repo}", "tool_input": {}},
     True, "a call naming no path is refused, not waved through"),

    ({"agent_type": "kevin", "tool_input": {"file_path": "artifacts/forensics/x.md"}},
     True, "no cwd means the allowed directory cannot be located - refuse"),

    ({"agent_type": "kevin", "cwd": "relative/nonsense",
      "tool_input": {"file_path": "artifacts/forensics/x.md"}},
     True, "a non-absolute cwd is not something to guess from"),

    # --- and open for everyone else ---
    ({"agent_type": "general-purpose", "cwd": "{repo}",
      "tool_input": {"file_path": "docs/csi/ROSTER.md"}},
     False, "another agent's writes are not this hook's business"),

    ({"cwd": "{repo}", "tool_input": {"file_path": "docs/csi/ROSTER.md"}},
     False, "the main thread carries no agent_type and is never held"),
]


def read_utf8(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def fill(obj):
    if isinstance(obj, dict):
        return {k: fill(v) for k, v in obj.items()}
    if isinstance(obj, str):
        return obj.replace("{repo}", str(REPO))
    return obj


def decision(payload: dict) -> str:
    proc = subprocess.run(
        [sys.executable, str(HOOK)],
        input=json.dumps(fill(payload)),
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        return f"error(exit {proc.returncode}): {proc.stderr.strip()[:120]}"
    try:
        out = json.loads(proc.stdout or "{}")
    except json.JSONDecodeError:
        return f"unparseable: {proc.stdout.strip()[:120]}"
    return out.get("hookSpecificOutput", {}).get("permissionDecision", "allow")


def check_unparseable_payload() -> list[str]:
    """Garbage on stdin must deny, not allow.

    Unattributable input cannot be shown to be someone other than Kevin.
    """
    proc = subprocess.run(
        [sys.executable, str(HOOK)], input="{not json", capture_output=True, text=True
    )
    if proc.returncode != 0:
        return [f"unparseable payload made the hook exit {proc.returncode}; "
                "an erroring hook blocks every write in the repository"]
    try:
        out = json.loads(proc.stdout or "{}")
    except json.JSONDecodeError:
        return ["unparseable payload produced unparseable output"]
    if out.get("hookSpecificOutput", {}).get("permissionDecision") != "deny":
        return ["an unparseable payload was allowed; it must fail closed"]
    return []


def check_wiring() -> list[str]:
    """The hook only matters if settings.json invokes it, for every write tool.

    A correct script nothing calls is the defect this repository keeps finding.
    """
    out = []
    try:
        settings = json.loads(read_utf8(SETTINGS))
    except (OSError, json.JSONDecodeError) as exc:
        return [f".claude/settings.json is missing or unparseable: {exc}"]

    entries = settings.get("hooks", {}).get("PreToolUse", [])
    wired = [e for e in entries
             if any("kevin-forensics-only" in h.get("command", "")
                    for h in e.get("hooks", []))]
    if not wired:
        return ["no PreToolUse hook in .claude/settings.json invokes "
                "kevin-forensics-only - the script exists but nothing runs it"]

    matcher = wired[0].get("matcher", "")
    for tool in WRITE_TOOLS:
        if not re.search(rf"\b{tool}\b", matcher):
            out.append(f"the hook's matcher does not cover {tool!r} "
                       f"(matcher is {matcher!r}); a write through it is unchecked")
    return out


def check_kevin_has_no_uncovered_write_tool() -> list[str]:
    """His tool list must not gain a write tool the matcher does not cover.

    He holds Write and no other today. This is what notices if that changes
    without the matcher changing with it.
    """
    line = next((l for l in read_utf8(KEVIN).splitlines() if l.startswith("tools:")), None)
    if line is None:
        return ["no tools: line in .claude/agents/kevin.md"]
    tools = {t.strip() for t in line.split(":", 1)[1].split(",")}
    uncovered = sorted(t for t in tools if t in WRITE_TOOLS)
    # Every write-capable tool he holds must be in WRITE_TOOLS, which the
    # matcher check above proves the hook covers. A tool outside that set that
    # can still write is the gap worth failing on.
    unknown_writers = sorted(t for t in tools
                             if t not in WRITE_TOOLS
                             and t in {"Update", "Patch", "Create"})
    if unknown_writers:
        return [f"kevin holds write-capable tool(s) the hook does not know "
                f"about: {unknown_writers}"]
    if not uncovered:
        return []  # holds no write tool at all; hook is moot but harmless
    return []


def main() -> int:
    if not HOOK.exists():
        print("kevin scope test: FAILED")
        print(f"  {HOOK.relative_to(REPO)} is missing.")
        return 1

    failures = check_wiring()
    failures += check_unparseable_payload()
    failures += check_kevin_has_no_uncovered_write_tool()

    for payload, expect_denied, why in CASES:
        got = decision(payload)
        want = "deny" if expect_denied else "allow"
        if got != want:
            failures.append(f"{why}\n    {json.dumps(payload)}\n"
                            f"    expected {want}, got {got}")

    if failures:
        print("kevin scope test: FAILED")
        for line in failures:
            print(f"  {line}")
        return 1

    print(f"kevin scope test: {len(CASES)} write-scope cases behave, "
          "fails closed, wiring covers every write tool")
    return 0


if __name__ == "__main__":
    sys.exit(main())
