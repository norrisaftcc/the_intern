# CSI Roster

Five personas, reconstructed from the artifacts collection into agents this repository can
actually dispatch. Each one is an alpha fork: a contract, a behavior list, and tools.

## The roster

| Persona | Use for | Tools | Reconstructed from |
|---------|---------|-------|--------------------|
| `kai` | Python and web debugging, guided investigation | Read, Grep, Glob, Edit, Write, Bash | `artifacts/kai/`, `artifacts/kai_summary.md` |
| `liza` | UI, render behavior, diagrams, schema design | Read, Grep, Glob, Edit, Write, Bash | `artifacts/liza/`, `artifacts/liza_summary.md` |
| `wyatt` | git and GitHub, branch and merge recovery | Read, Grep, Glob, Edit, Bash | `artifacts/liza/wyatt_readme.md`, `artifacts/wyatt_summary.md` |
| `vita` | Introductory Python tutoring, guided discovery | Read, Grep, Glob | `artifacts/vita_summary.md` |
| `vi` | Songwriting, lyrics, genre and scene research | Read, Write, WebSearch | `artifacts/Vi/`, `artifacts/vi_summary.md` |

Dispatch by name with the Agent tool, or invoke the shared skills directly:

- `csi-fork-protocol` — instantiate a persona at a chosen capability level.
- `csi-persona-conformance` — test a persona against the baseline record.

## What changed in reconstruction

The summaries in `artifacts/` are character studies. An agent is a contract. Three
differences follow from that, and all three come from `artifacts/META_ANALYSIS.md`, which
audited the original collection and named what was wasteful.

**Appearance is one line, not fifteen.** The meta-analysis measured elaborate visual
description at 100 to 200 tokens with no effect on behavior. The harness now caps the
Identity section at 30 words. Kai still has the fedora. She does not have a paragraph
about it.

**Every persona states its floor.** Audience, Scope, Format, Path — the four nouns from
the baseline record. The original prompts stated none of them, which is why the same
character behaved differently across sessions.

**Limits are structural where they can be.** VITA must never write a student's code, so
VITA has no Edit or Write tool. A rule the tool list enforces cannot be talked out of.

## Fidelity notes

- Kai defers to TeacherBot (🤖). That is in the source and it is load-bearing: she declines
  graded work because someone else grades it.
- LIZA's `[[double bracket]]` fork channel is an observed convention, first recorded in
  `artifacts/csi-lore/csi-lore-orb.md`. It was not designed.
- VITA's banned-word list — simply, just, obviously, clearly — comes straight from the
  source and is checked by a case file, not left to good intentions.
- Vi runs on Pi.ai. Her agent file says so in a Provenance section, because the original
  notes open with that disclaimer and the reconstruction should not quietly drop it.
- Civvie and the Notion bot are in `artifacts/` but stayed out of the roster. The sources
  are a joke and an observation, not a persona. No invented personas.

## Adding one

See the `csi-fork-protocol` skill, section "Adding a persona". The short version: it needs
a real source in `artifacts/`, a Contract with four floor items, a boundary example, a case
file, and a passing run of `python3 tests/csi/floor_test.py`.
