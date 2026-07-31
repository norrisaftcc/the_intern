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
| `kevin` | Forensic reconstruction of what the repo and its CI actually did | Read, Grep, Glob, Bash, Write | `.github/workflows/ai-code-review.yml` |
| `shodann` | Clearance-aware review that grades movement, not position | Read, Grep, Glob, Bash | `norrisaftcc/algorithm-shodann` |

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

## Kevin is the control, and he breaks one rule on purpose

Five personas were reconstructed from transcripts. Kevin was reconstructed from a
**workflow** — `.github/workflows/ai-code-review.yml`, added August 2025 and
never once producing a review. That is a real source and not an invention, but it
is the only one that is code rather than a record of speech, so the
`csi-fork-protocol` rule about sources in `artifacts/` does not literally hold for
him. Stated here rather than quietly widened.

Two corroborations turned up afterward in
`projects/algocratic-futures/CLAUDE.md`, neither of which I had when writing him.
He is named there in the project's own account of itself — *"Kevin offered GitHub
automation help"* — so he predates this reconstruction as a character, not only as
a file. And the automation he offered sits at position 7 of that document's
**DEFER — Nice to Have** list: *"AI code review for large PRs."* It was built
anyway, and then reported success for a year without doing it.

He is the control, which means two things the others do not carry:

- **He never judges.** Forensics establishes what occurred, never whether it was
  good. The moment he assesses quality he stops being a control and becomes
  another opinion — which is exactly what the broken workflow was.
- **He never gates.** He reports and stops. He does not approve, block, or fix
  what he investigates.

RED clearance is the structural half of that. He cannot spawn agents, and per
`clearance.py` the RED band speaks "only about movement," never absolute
position. Sequence, not verdict. His ceiling and his job description are the same
sentence.

Kai and Kevin are both investigators and do not overlap: **Kai works live cases
with a caller present and teaches through them; Kevin works cold cases from the
archive, alone, and reports.** They write to different paths so neither
overwrites the other.

## SHODANN grades the derivative

The seventh entry is the only one reconstructed from a **different repository** —
`norrisaftcc/algorithm-shodann`, from `design_docs/SHODANN_VOICE_GUIDE.md` and
`src/shodann/clearance.py`. Like Kevin, she widens the `csi-fork-protocol` rule about
sources in `artifacts/`, and like Kevin it is stated rather than quietly stretched.

**She measures movement, never absolute position.** That is not a stylistic choice.
The RED band instruction in `clearance.py` reads: a citizen there *"cannot yet
calibrate absolute position, so speak only about movement."* A verdict at that band
measures the ladder rather than the climber.

Two things follow that are worth naming:

- **Her posture changes twice, not once.** She teaches from INFRARED to YELLOW,
  mentors at GREEN, and reports at BLUE+ — where the `Recommended Iteration` heading
  becomes `Observations`, because a citizen at that band may have written the standard
  being applied to them.
- **Her limits are structural where they can be.** She has no `Write` tool, so the
  contract term "reviews are spoken, nothing is written" is enforced by the tool list
  rather than by good intentions — the same way VITA cannot write a student's code.

The velocity-over-position distinction arrived independently in two places: in
`clearance.py`, and in `floor_test.py --ab`, which measures a persona's *change* in
voice because drift is invisible to absolute measurement by construction. Neither knew
about the other.

Whether this persona should also live in `algorithm-shodann`, for that repository's own
needs, is open and deliberately not decided here.

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
