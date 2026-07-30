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

## The fourth operation — A/B

Layers 1 to 3 all ask the same question: is this persona above the floor. A voice rewrite
asks a different one, so it gets a different instrument.

The risk in a voice edit is that it is invisible. Changing a Limit from "Do not claim a
performance win without a before number" to "Try to have a before number" is two words. In
a diff review it reads as tone. It is a behavior change, and the floor test passes either
way — both versions are above the floor, because the floor measures shape, not strictness.

So the A/B splits the document. Contract, Behavior, Limits, plus the `tools` and
`description` frontmatter, are contract. Identity, Notation, Examples, Provenance are
voice. An edit touching only voice gets a clean verdict; an edit touching both exits 2 and
says to split the commit.

Verified against exactly the case above: the softened LIZA limit passed the floor test on
both sides and the A/B flagged it as MIXED.

At the reply level, `--ab-score` runs the same case prompt's captured replies from both
versions and reports which markers flipped. A marker A held and B dropped is the voice
change taking behavior with it.

What neither does is rank the voices. That is a reading, and it should be done without
knowing which version is new — otherwise novelty scores as quality.

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

### The harness watches its own limits

For one commit, the paragraph above was the whole enforcement mechanism — a sentence in a
document and a comment in a source file. Pointed at itself, that is the failure it exists
to catch. Widening the harness's own limits and running it produced:

```
MAX_WORDS_PER_INSTRUCTION = 40      # was 20
MAX_IDENTITY_WORDS = 200            # was 30
MIN_EXAMPLES = 0                    # was 2

floor test: 7 documents above the floor, baseline intact
```

Nothing found anything, because the drift meter watched the frozen document and not the
limits derived from it. A harness can be defanged and still report green.

`RECORD.json` now carries a `limits` object and `check_limits` compares it against what the
code enforces. The finding names the direction, because the two directions are not the same
event: a MAX rising, a MIN falling, or a list shortening means the floor lost teeth.

```
FAIL RECORD.json [limits] MAX_WORDS_PER_INSTRUCTION 20 → 40 · loosened
FAIL RECORD.json [limits] MAX_WORDS_PER_INSTRUCTION 20 → 12 · tightened
FAIL RECORD.json [limits] FLOOR_NOUNS [...4 items] → [...3 items] · loosened
FAIL RECORD.json [limits] RECORD.json states no limits, so the harness grades its own homework
```

Both directions report, because both are amendments and the record is the drift meter. Only
one is self-erasure, and now it says which.
