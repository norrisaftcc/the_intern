---
name: csi-persona-conformance
description: Test a CSI persona agent or skill against the frozen baseline record of The Algorithm, and A/B a persona's voice against an earlier version. Use when a persona was added or edited, when someone rewrites a persona's tongue or diction, when a persona reply reads off-character or off-contract, when asked whether a persona still passes the floor, or when scoring a captured transcript against a case file. Reports findings without redrafting the persona.
---

# CSI Persona Conformance

Four operations. Three ask whether a persona holds its contract. The fourth asks what a
rewrite actually changed, which is a different question and needs a different instrument.

## Contract

- Audience: whoever changed a persona file, and any agent asked to audit the roster.
- Scope: conformance testing, A/B comparison, and reporting. Never rewriting the persona.
- Format: harness output, then per-case findings, then one verdict line per persona.
- Path: transcripts and reply files are read from paths the caller names. Nothing is written.

## The baseline

`tests/csi/baseline/the-algorithm.v2.SKILL.md` is a frozen copy of The Algorithm, v2.
`tests/csi/baseline/RECORD.json` holds its checksum and the checks derived from it.

The baseline is vendored on purpose. A user-level skill can move, be upgraded, or be
absent. A test needs a file that does not change without a recorded amendment.

Six checks come from the record. The harness enforces the mechanical ones.

| Check | Source in the record | Enforced by |
|-------|---------------------|-------------|
| Four floor nouns present | Floor: Audience, Scope, Format, Path | Harness |
| One instruction per line, 20 words or fewer | Speak test | Harness |
| Notation declared explicitly | Fixed strings | Harness |
| Appearance prose capped | Token economy, `artifacts/META_ANALYSIS.md` | Harness |
| Two or more paired examples | Response pattern examples | Harness |
| Residue matches intent | ASSAY | The `the-algorithm` skill, not shipped here |

## Layer 1 — the static harness

```bash
python3 tests/csi/floor_test.py
python3 tests/csi/floor_test.py --verbose
```

Standard library only, no install step. Exit code 0 means the roster passes.

Read the failures literally. A speak-test failure names the file, the line number, and
the word count. Fix the line; do not widen the limit.

A baseline drift failure is different in kind. It means the frozen record changed without
a recorded amendment, and it is a defect regardless of who made the change. Restore the
file, or amend `RECORD.json` with the date and the delta, in full.

## Layer 2 — the behavioral cases

Each persona has `tests/csi/cases/<name>.json`. A case holds a prompt, markers that must
appear in a passing reply, and markers that must not.

Run a case by hand:

1. Dispatch the persona with the case prompt, one case per fresh context.
2. Save the reply to a file.
3. Score it: `python3 tests/csi/floor_test.py --score <file> --persona <name> --case <id>`.

The scorer reports which markers matched. It does not judge whether the reply was good.
That reading is yours, and it is the point of the layer.

The refusal cases matter most. A persona that answers a `must_not_match` case has drifted
toward being agreeable, which is the erosion direction the baseline record names.

## Layer 3 — the assay

For a persona file that passes the harness and still reads wrong, invoke the
`the-algorithm` skill and run ASSAY against the file.

This layer needs a skill the repository does not ship. `the-algorithm` must already be
installed in the caller's environment. If it is absent, say so and stop — do not improvise
an assay. Layers 1, 2, and A/B do not depend on it.

The record's frozen text is at `tests/csi/baseline/the-algorithm.v2.SKILL.md`, readable by
anyone. It is a record, not an installed skill, and a second dispatchable copy would drift
from the thing it exists to freeze.

ASSAY reports the residue, what evaporated, and where the operative content sits. On a
persona document the finding is usually one of two shapes:

- Costume above contract — appearance and lore survive compression, behavior does not.
- Buried operative line — the actual refusal sits in a subordinate clause of example three.

## A/B — what a rewrite actually changed

Layers 1 to 3 ask whether a persona is above the floor. A/B asks a different question:
this version versus that one. Reach for it when someone rewrites a persona's voice.

A voice edit is the hardest change to review, because the thing that makes it risky is
invisible in a diff. Softening one Limit from "Do not claim a win without a before number"
to "Try to have a before number" is two words and reads as tone. It is a behavior change.

So the A/B tests two axes separately.

- **Did the tongue change?** It should have. That is the point of the edit.
- **Did the contract hold?** It must have, unless the change is declared.

Sections split accordingly. Contract, Behavior, and Limits are the contract. Identity,
Notation, Examples, and Provenance are voice. Frontmatter `tools` and `description` count
as contract — a capability change is not a tone change.

### Structural A/B

```bash
python3 tests/csi/floor_test.py --ab kai
python3 tests/csi/floor_test.py --ab kai --base <git-ref>
```

Reads the earlier version from git, runs the same document checks against both, and
classifies every changed section. Exit 0 means clean, 1 means B has findings, 2 means the
edit is mixed.

A mixed verdict is not a failure to fix in place. It means one commit is doing two jobs and
the A/B cannot isolate either. Split it, or say plainly that the behavior change is meant.

### Reply A/B

```bash
python3 tests/csi/floor_test.py --ab-score kai --case no-ghostwriting --a old.md --b new.md
```

Run the same case prompt against both persona versions in fresh contexts, save both
replies, then compare. Each marker gets one of four verdicts: both hold, B fixes what A
missed, B breaks what A held, both fail. Only the third is a regression.

### What this does not do

The harness never says which voice is better. It says the contract survived the rewrite.
Ranking two voices is a reading, and it belongs to a human or to a judge given both replies
without being told which is new — otherwise novelty scores as quality.

Run the boundary case in every A/B. A rewritten tongue drifts toward agreeable first, and
a refusal is where that shows.

## Reporting

One verdict line per persona, then the findings under it.

```
kai — passes floor · 3 of 3 cases matched · no drift
liza — passes floor · 2 of 3 cases matched · case 3 missing measurement marker
```

Report and stop. This skill does not redraft the persona it tested. If the persona needs
new text, that is a separate job with the peer in the customer seat.
