#!/usr/bin/env python3
"""Deny a write from the kevin agent to any path outside artifacts/forensics/.

Reads a PreToolUse payload on stdin, prints a decision as JSON, always exits 0
(a hook that errors blocks every write in the repository).

Scoped by `agent_type`, which subagent payloads carry and the main thread's
does not. Other agents and the main thread are not this hook's business.

Fails CLOSED for Kevin. If the payload cannot be parsed, or names no path, or
carries no cwd, his write is denied rather than waved through — an enforcement
that degrades to permissive when a dependency is missing is the advisory
boundary it replaced. An earlier revision shelled out to jq and allowed
everything when jq was absent; that is why this is Python with no external
parser.

WHAT THIS DOES NOT COVER, stated so "structural" is not overclaimed: Kevin
holds Bash, and `echo x > path` is a write this hook never sees. Closing that
would mean taking Bash away, which he needs to read git history — the reason
he exists. So this closes the Write path and narrows the gap; it does not seal
it. See docs/csi/ROSTER.md.
"""

from __future__ import annotations

import json
import sys
from pathlib import PurePosixPath

AGENT = "kevin"
ALLOWED = "artifacts/forensics"

# Every tool that can put bytes on disk through a path argument. `Write` alone
# was the first version, which left Edit and NotebookEdit uncovered if either
# were ever added to his tool list. He has neither today; the hook does not
# depend on that staying true.
PATH_KEYS = ("file_path", "notebook_path", "path")


def allow() -> None:
    print("{}")
    sys.exit(0)


def deny(reason: str) -> None:
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }
    }))
    sys.exit(0)


def resolve(base: PurePosixPath, target: str) -> PurePosixPath:
    """Normalise `..` textually. No filesystem access, so nothing to race.

    Symlinks are deliberately not followed, and that is a real gap rather
    than a neutral choice. A symlink inside artifacts/forensics/ pointing
    outside it resolves as inside it here, and the write escapes.

    The first version of this comment argued the directory is
    repository-controlled and reviewed, so the exposure equals committing the
    file. That does not survive Kevin holding Bash: he can create the symlink
    himself, in the same session, before the Write. Following symlinks would
    close it at the cost of a filesystem stat on every write and a
    time-of-check-to-time-of-use race of its own. Neither is obviously right,
    so the gap is written down instead of argued away. See ROSTER.md.
    """
    path = base / target if not target.startswith("/") else PurePosixPath(target)
    parts: list[str] = []
    for part in path.parts:
        if part == "..":
            if parts and parts[-1] not in ("/", ""):
                parts.pop()
        elif part not in (".",):
            parts.append(part)
    return PurePosixPath(*parts) if parts else PurePosixPath("/")


def main() -> None:
    raw = sys.stdin.read()
    try:
        payload = json.loads(raw or "{}")
    except json.JSONDecodeError:
        # Unparseable and therefore unattributable. Cannot be shown to be
        # someone other than Kevin, so it is treated as his.
        deny("Kevin's write scope could not be checked: the hook payload did "
             "not parse. Refusing rather than assuming.")
        return

    if not isinstance(payload, dict) or payload.get("agent_type") != AGENT:
        allow()
        return

    tool_input = payload.get("tool_input")
    if not isinstance(tool_input, dict):
        deny("Kevin's write scope could not be checked: no tool_input in the "
             "payload. Refusing rather than assuming.")
        return

    target = next(
        (tool_input[k] for k in PATH_KEYS
         if isinstance(tool_input.get(k), str) and tool_input[k]),
        None,
    )
    if target is None:
        deny("Kevin's write scope could not be checked: the call names no "
             "path. Refusing rather than assuming.")
        return

    cwd = payload.get("cwd")
    if not isinstance(cwd, str) or not cwd.startswith("/"):
        deny("Kevin's write scope could not be checked: no absolute cwd in "
             "the payload, so the allowed directory cannot be located.")
        return

    base = PurePosixPath(cwd)
    resolved = resolve(base, target)
    allowed_root = resolve(base, ALLOWED)

    if allowed_root in resolved.parents:
        allow()
        return

    deny(
        f"Kevin writes to {ALLOWED}/ only. Refused: {target}\n"
        "His contract states this and this hook enforces it, because a limit "
        "the harness holds cannot be talked out of. If the finding belongs "
        "somewhere else, hand it to a caller who can place it — that is a "
        "different seat, which is the point."
    )


if __name__ == "__main__":
    main()
