# CSI persona tests

Conformance tests for the persona agents in `.claude/agents/` and the skills in
`.claude/skills/`, measured against the frozen baseline record of The Algorithm.

No dependencies. Python 3.9 or later, standard library only.

## Run it

```bash
python3 tests/csi/floor_test.py            # the roster
python3 tests/csi/floor_test.py --verbose  # list what passed too
```

Exit 0 means every document is above the floor and the baseline is intact.

## Score a reply

Dispatch a persona with a case prompt from `cases/<persona>.json`, save the reply, then:

```bash
python3 tests/csi/floor_test.py --score reply.md --persona kai
python3 tests/csi/floor_test.py --score reply.md --persona kai --case no-ghostwriting
```

Markers are evidence that the persona held its shape. They are not a quality score — read
the reply yourself. The refusal cases are the ones that matter; drift shows up there first.

## A/B a voice change

When a persona's tongue is rewritten, the question is not "does it pass" but "what did the
rewrite change". Two commands:

```bash
python3 tests/csi/floor_test.py --ab kai                    # working tree vs HEAD
python3 tests/csi/floor_test.py --ab kai --base <git-ref>   # vs any earlier version
python3 tests/csi/floor_test.py --ab-score kai --case no-ghostwriting --a old.md --b new.md
```

The first classifies every changed section as voice or contract. Exit 2 means the edit
changed both, so it needs splitting before either can be judged.

The second compares two captured replies to the same case prompt. A marker that A held and
B dropped is a regression — the voice change took behavior with it.

Neither says which voice is better. That reading is yours.

## Layout

```
baseline/
  the-algorithm.v2.SKILL.md   frozen record, checksummed
  RECORD.json                 checksum, derived checks, amendment record
cases/
  <persona>.json              prompts with must_match / must_not_match markers
floor_test.py                 the harness
```

## Reading a failure

Every finding names the file, the line, and the check.

```
FAIL .claude/agents/liza.md:9 [path] declared path 'artifacts/diagrams/<slug>.mmd' needs directory artifacts/diagrams/, which is absent
FAIL .claude/agents/kai.md:22 [speak-test] 26 words, limit 20: Ask for the traceback, the input...
```

Fix the line. Do not widen the limit — the limits come from the baseline record, and
changing one is an amendment that belongs in `RECORD.json` with a date and a delta.

`baseline-drift` is a different kind of failure. It means the frozen record changed without
a recorded amendment. Restore the file, or record the amendment in full.

`limits` is the same idea pointed one layer up: the harness's own limits no longer match
what `baseline/RECORD.json` says it enforces. The finding names the direction — `loosened`
means the floor lost teeth and will find less than the record claims. Restore the limit, or
amend the record with the date and the delta.

Background: `docs/csi/BASELINE.md` for what each check is derived from, and
`docs/csi/ROSTER.md` for the personas themselves.
