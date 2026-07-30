# Testing the personas against The Algorithm

The Algorithm is the most disciplined document in this lineage. It states its own floor,
locks its own invariants, records its own amendments, and submits to its own test. That
makes it the right baseline for the persona roster: not a style guide, a measuring stick.

A frozen copy lives at `tests/csi/baseline/the-algorithm.v2.SKILL.md`, with its checksum in
`tests/csi/baseline/RECORD.json`. It is vendored on purpose. A user-level skill can be
upgraded, moved, or absent, and a baseline that moves is not a baseline.

## What the baseline contributes

| From the record | Becomes | Enforced by |
|-----------------|---------|-------------|
| Floor: Audience, Scope, Format, Path | A Contract block in every persona | Harness |
| Speak test — one line, one instruction, one breath | 20 words and 120 columns per instruction | Harness |
| Path names the exact file produced | Declared directories must exist | Harness |
| Token economy, via `artifacts/META_ANALYSIS.md` | Identity capped at 30 words | Harness |
| Fixed strings | Notation declared explicitly, never implied | Harness |
| Amendment record as drift meter | Baseline checksum comparison | Harness |
| ASSAY | Read a persona file for what survives compression | The `the-algorithm` skill |
| Erosion toward the smooth | Refusal cases, where drift shows first | Case files |

## Three layers

**Layer 1, static.** `python3 tests/csi/floor_test.py`. Standard library, no install.
Mechanical checks only. Exit 0 means the roster is above the floor.

**Layer 2, behavioral.** Dispatch a persona with a case prompt, save the reply, then
`--score` it against `tests/csi/cases/<persona>.json`. Markers are evidence, not a grade.

**Layer 3, the assay.** Invoke the `the-algorithm` skill and run ASSAY against a persona
file. Use it when the file passes layer 1 and still reads wrong.

## Recorded findings

The harness and the assay both found real defects on the first run. Recorded here because a
test suite that has never failed has not been tested.

**Layer 1, first run.** Three findings. Vi had no Identity section to measure. Vi and VITA
had no boundary example — neither file demonstrated its own refusal, which is the behavior
most worth demonstrating.

**Layer 2, first run.** Two findings, pointing in opposite directions.

- Kai's `open-case` marker required a question mark. Her Behavior line permits a question
  *or* a next step. The case was wrong, not the persona — an over-assertion, corrected.
- VITA's loop example closed with "if you cannot find one". Her own Notation section
  requires success-assuming tense. The persona was wrong, not the case — corrected to
  "when you find that no line does".

Both directions matter. A suite that can only convict the thing under test is a suite that
will eventually convict it wrongly.

**Layer 3, ASSAY of `.claude/agents/kai.md`.** Above the floor. Operative sentence at 30 of
35, main clause, imperative — "Do not write a graded deliverable for a student." Erosion
direction ornamental rather than smooth, so no manufacturing signature. Two defects the
compression exposed:

1. Contract and Behavior disagreed on the closing move. Format mandated a question;
   Behavior permitted a question or a next step. The layer-2 failure above was the same
   defect seen from the other side, which is what a consistent floor is supposed to do.
2. `artifacts/casefiles/` and `artifacts/diagrams/` were declared as output paths and did
   not exist. Both created, and a `path` check added to the harness so the next one fails
   loudly instead of at write time.

That third finding is the argument for the baseline in one line: the assay found a class of
defect the harness could not see, and the harness now covers it permanently.

## Amending the floor

The limits in `floor_test.py` are derived from the record, so changing one is an amendment.
Record it in `RECORD.json` with the date and the delta, as the record requires of itself.

A speak-test failure is not an argument for a wider limit. It is a line that needs cutting.
