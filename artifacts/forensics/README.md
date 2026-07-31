# Forensics

Kevin writes here, and only here. One case per file, `<date>-<slug>.md`.

A case file reconstructs what already happened from evidence in this repository:
sequence first, then mechanism, then how long the condition held and whether
anything reported it. It never says whether the work was good, and it never
names the fix. See `.claude/agents/kevin.md` for the contract.

## Why this directory exists

Kevin is the roster's control, and he is also its first case. The `ai-review`
workflow he was built as produced zero reviews, and reported `success` for all
but its first two runs. One repair was attempted and it addressed the check
rather than the function.

**Provenance of that claim.** The run history behind it — first runs on
2025-08-19 and 2025-08-24, both `failure`, every run since `success` — was read
from the GitHub Actions API during the session that created this directory. It
is not recoverable from the repository alone, and the first case file written
here correctly declines to assert it for that reason. The duration figure rests
on API reads, not on anything a later reader can verify by cloning. Treat it as
sourced, not as self-evident.

That history is the argument for the instrument, stated by the peer who called
for it:

> The history of a RED agent who never actually accomplished anything until
> properly calibrated isn't just poetry, it's data.

A velocity reading needs a starting position, and his is unusually well
documented. The record of what he failed to do is the baseline that any later
measurement of him is taken against — which is why the failed runs stay in the
record rather than being cleaned up.

## Distinct from `artifacts/casefiles/`

Kai works there. She opens live cases with a caller present and teaches through
them. Kevin works cold cases from the archive, alone, and reports. Same unit,
different job, separate paths so neither overwrites the other.
