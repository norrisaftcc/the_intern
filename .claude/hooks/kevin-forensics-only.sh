#!/usr/bin/env bash
# Kevin writes to artifacts/forensics/ or he does not write.
#
# docs/csi/ROSTER.md states the principle: "Limits are structural where they
# can be. VITA must never write a student's code, so VITA has no Edit or Write
# tool. A rule the tool list enforces cannot be talked out of."
#
# Kevin is the roster's control and did not meet it. His contract said
# "Never write outside artifacts/forensics/" and nothing enforced it. He was
# reconstructed from a workflow that reported success for a year while
# producing nothing; a control whose boundary is advisory repeats that shape.
#
# This is the enforcement. It reads the PreToolUse payload on stdin and denies
# a Write from the kevin agent to any path outside artifacts/forensics/.
#
# Scoped by `agent_type`, which subagent payloads carry and the main thread's
# does not - confirmed by probing a real payload rather than assumed. So this
# bites Kevin and nobody else: another agent's writes and the main thread's
# writes are not this hook's business.
#
# Exit 0 always. A hook that errors is a hook that blocks everything, and the
# decision is carried in the JSON on stdout rather than in the exit code.

set -uo pipefail

payload=$(cat)

allow() { printf '{}\n'; exit 0; }

command -v jq >/dev/null 2>&1 || allow

agent=$(printf '%s' "$payload" | jq -r '.agent_type // ""' 2>/dev/null) || allow
[ "$agent" = "kevin" ] || allow

target=$(printf '%s' "$payload" | jq -r '.tool_input.file_path // ""' 2>/dev/null) || allow
[ -n "$target" ] || allow

cwd=$(printf '%s' "$payload" | jq -r '.cwd // ""' 2>/dev/null)

# Normalise to a repository-relative path. `realpath -m` resolves `..` without
# requiring the file to exist, which is what makes a traversal like
# artifacts/forensics/../../etc/passwd fail this check rather than pass it on
# a prefix match.
case "$target" in
  /*) abs="$target" ;;
  *)  abs="${cwd%/}/$target" ;;
esac
abs=$(realpath -m "$abs" 2>/dev/null || printf '%s' "$abs")
allowed=$(realpath -m "${cwd%/}/artifacts/forensics" 2>/dev/null || printf '%s' "${cwd%/}/artifacts/forensics")

case "$abs" in
  "$allowed"/*) allow ;;
esac

jq -n --arg p "$target" '{
  hookSpecificOutput: {
    hookEventName: "PreToolUse",
    permissionDecision: "deny",
    permissionDecisionReason: (
      "Kevin writes to artifacts/forensics/ only. Refused: " + $p +
      "\nHis contract states this and this hook enforces it, because a limit " +
      "the harness holds cannot be talked out of. If the finding belongs " +
      "somewhere else, hand it to a caller who can place it - that is a " +
      "different seat, which is the point."
    )
  }
}'
exit 0
