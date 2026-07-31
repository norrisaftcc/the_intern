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
import posixpath
import unicodedata

# The literal the harness puts in `agent_type` for this agent. Captured from a
# real invocation on 2026-07-31, not inferred: a live dispatch logged
# `agent_type: 'kevin'` on every call. Compared case-insensitively anyway,
# because a mismatch here does not fail loudly - it takes the "not Kevin"
# branch and allows everything, which is the one silent fail-open this file
# could still have had. tests/workflow/kevin_scope_test.py pins the casing.
AGENT = "kevin"
ALLOWED = "artifacts/forensics"

# Every tool that can put bytes on disk through a path argument. `Write` alone
# was the first version, which left Edit and NotebookEdit uncovered if either
# were ever added to his tool list. He has neither today; the hook does not
# depend on that staying true.
PATH_KEYS = ("file_path", "notebook_path", "path")

# The tools this hook knows how to read a path out of.
#
# Three places encode overlapping facts about writing: this list, the matcher
# in .claude/settings.json, and KEVIN_TOOLS in the test. They are separate on
# purpose - the matcher decides what reaches the hook, this decides what it
# will act on, and the test pins what Kevin holds - but they can drift.
# tests/workflow/kevin_scope_test.py fails if any pair disagrees. A fourth
# list would want a single source of truth instead.
WRITE_TOOLS = ("Write", "Edit", "MultiEdit", "NotebookEdit")


def normalise(value: object) -> str:
    """Fold an agent identifier to something comparable.

    This is the single point of trust: if the comparison fails, the hook takes
    the "not Kevin" branch and allows everything. So a zero-width space or a
    compatibility-form character in `agent_type` would be a silent fail-open,
    which is the one shape of failure this file exists to prevent. NFKC folds
    compatibility forms; the filter drops anything unprintable.
    """
    if not isinstance(value, str):
        return ""
    folded = unicodedata.normalize("NFKC", value)
    return "".join(c for c in folded if c.isprintable()).strip().lower()


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


def resolve(cwd: str, target: str) -> str:
    """Absolute, `..` collapsed, no filesystem access.

    `posixpath.normpath` rather than a hand-rolled loop: an earlier version
    popped `..` by hand, which is security-critical logic reimplemented beside
    a stdlib function that already does it and has been read by more people.
    `posixpath` specifically, not `os.path`, so the result does not change
    shape on a Windows checkout.

    Symlinks are deliberately not followed, and that is a real gap rather than
    a neutral choice. A symlink inside artifacts/forensics/ pointing outside it
    resolves as inside it here, and the write escapes.

    The first version of this comment argued the directory is
    repository-controlled and reviewed, so the exposure equals committing the
    file. That does not survive Kevin holding Bash: he can create the symlink
    himself, in the same session, before the Write. Following symlinks would
    close it at the cost of a stat on every write and a
    time-of-check-to-time-of-use race of its own. Neither is obviously right,
    so the gap is written down instead of argued away. See ROSTER.md and #36.
    """
    joined = target if target.startswith("/") else posixpath.join(cwd, target)
    return posixpath.normpath(joined)


def main() -> None:
    # Bounded. Not exploitable from a trusted harness, but an unbounded read
    # in a file this careful about everything else reads as an oversight.
    MAX_PAYLOAD = 8 * 1024 * 1024
    raw = sys.stdin.read(MAX_PAYLOAD + 1)
    if len(raw) > MAX_PAYLOAD:
        deny(f"Kevin's write scope could not be checked: payload exceeded "
             f"{MAX_PAYLOAD} bytes. Refusing rather than truncating.")
        return
    try:
        payload = json.loads(raw or "{}")
    except json.JSONDecodeError:
        # Unparseable and therefore unattributable. Cannot be shown to be
        # someone other than Kevin, so it is treated as his.
        deny("Kevin's write scope could not be checked: the hook payload did "
             "not parse. Refusing rather than assuming.")
        return

    if not isinstance(payload, dict):
        # A JSON array or scalar has no .get. The previous version called
        # .get before this check, so a non-dict raised AttributeError and was
        # caught by the guard in __main__ - it failed closed by accident,
        # and this check was unreachable.
        deny("Kevin's write scope could not be checked: the payload was not "
             "an object. Refusing rather than assuming.")
        return

    if normalise(payload.get("agent_type")) != AGENT:
        allow()
        return

    # Defence in depth. The matcher in settings.json decides what reaches this
    # hook; this decides what it will act on. The two are separate statements
    # of the same list and can drift, so an unrecognised tool arriving here is
    # a refusal rather than a shrug - it means the matcher was widened without
    # this being updated, and the safe reading of an unknown write path is no.
    # Absent is refused too. Every other missing field here denies, and
    # exempting this one would leave the matcher in settings.json as the sole
    # gate - which is what the check exists to stop depending on.
    tool_name = payload.get("tool_name")
    if tool_name not in WRITE_TOOLS:
        deny(f"Kevin's write scope could not be checked: {tool_name!r} reached "
             "this hook, which only knows how to read a path out of "
             f"{', '.join(WRITE_TOOLS)}. Widening the matcher needs this "
             "updated too.")
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

    # LOAD-BEARING ASSUMPTION: cwd is the repository root, so ALLOWED resolves
    # against it. If Kevin were ever invoked from a subdirectory the allowed
    # root would move with it and the boundary would silently follow. The
    # harness sets cwd to the project root today - the same live dispatch that
    # confirmed agent_type showed cwd as the repository root on both calls -
    # and this refuses rather than guesses if it is absent or relative.
    cwd = payload.get("cwd")
    if not isinstance(cwd, str) or not cwd.startswith("/"):
        deny("Kevin's write scope could not be checked: no absolute cwd in "
             "the payload, so the allowed directory cannot be located.")
        return

    resolved = resolve(cwd, target)
    allowed_root = resolve(cwd, ALLOWED)

    if resolved.startswith(allowed_root + "/"):
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
    try:
        main()
    except SystemExit:
        raise
    except BaseException as exc:  # noqa: BLE001 - the promise is the point
        # The docstring promises this exits 0 on every path, because a hook
        # that errors blocks every write in the repository. That promise has
        # to hold against edits that introduce a branch nobody thought about,
        # so the catch-all is here and it fails closed.
        deny("Kevin's write scope could not be checked: the hook raised "
             f"{type(exc).__name__}. Refusing rather than assuming.")
