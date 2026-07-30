---
name: csi-persona-conformance
description: Test a CSI persona agent or skill against the frozen baseline record of The Algorithm. Use when a persona was added or edited, when a persona reply reads off-character or off-contract, when asked whether a persona still passes the floor, or when scoring a captured transcript against a persona's case file. Runs the static harness first, then the behavioral cases, and reports findings without redrafting the persona.
---

# CSI Persona Conformance

Two layers of test. The static layer is mechanical and runs in a shell. The behavioral
layer needs a transcript. Both measure the same thing: does the persona still hold its
contract under the discipline of the baseline record.

## Contract

- Audience: whoever changed a persona file, and any agent asked to audit the roster.
- Scope: conformance testing and reporting. Never rewriting the persona under test.
- Format: harness output, then per-case findings, then one verdict line per persona.
- Path: transcripts are read from a path the caller names. Nothing is written.

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
| Residue matches intent | ASSAY | The `the-algorithm` skill |

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

ASSAY reports the residue, what evaporated, and where the operative content sits. On a
persona document the finding is usually one of two shapes:

- Costume above contract — appearance and lore survive compression, behavior does not.
- Buried operative line — the actual refusal sits in a subordinate clause of example three.

## Reporting

One verdict line per persona, then the findings under it.

```
kai — passes floor · 3 of 3 cases matched · no drift
liza — passes floor · 2 of 3 cases matched · case 3 missing measurement marker
```

Report and stop. This skill does not redraft the persona it tested. If the persona needs
new text, that is a separate job with the peer in the customer seat.
