# What is a gate here, and what is a spike

Two sets of tests live under this project and they are not the same kind of thing.
Labelled here because the distinction was established in conversation and would
otherwise be lost.

## The gate — `backend/test_*.py`

- `backend/test_agent_tiers.py`
- `backend/test_liza_flash_compatibility.py`
- `backend/test_trigger.py`

These are the gate. **They run, and they pass.** As of 2026-07-31.

**Corrected 2026-07-31.** This section said "They have never run. Not 'run and
passed', not 'run and failed' — never executed, by anything, once." That was
true when written and is not true now, so it is replaced rather than left
standing with a note beside it.

**Corrected 2026-07-30** after Kevin's first case file,
`artifacts/forensics/2026-07-30-walking-the-beat.md`. This section previously
said "two independent reasons." That was incomplete and the order was wrong.

There were **four obstacles in series**, and each had to be cleared before the
next was visible. The pin was the second, not the first. The fourth was inside
the gate itself and could not be seen until the third cleared.

1. **`deploy.yml` was at a path GitHub Actions does not read** — for about a
   year. It lived at `projects/algocratic-futures/.github/workflows/`, a
   directory that no longer exists: its last occupant, a duplicate
   `ai-code-review.yml`, was removed 2026-07-31. Actions
   only reads `.github/workflows/` at the repository root. Commit `166102f`
   relocated it on 2025-08-20, but on a feature branch; a first-parent walk of
   `origin/main` shows it reached the default branch only at merge `161a3e5` on
   2026-07-30. Until that merge the workflow could not run at all.

2. **`requirements.txt` pinned a version that was never published.**
   `adventurelib==2.0.0` — PyPI's releases stop at `1.2.1`. `pip install` failed
   before any test step. Repaired by `2dedf02`, 2026-07-30.

3. **`deploy.yml` pointed at a directory that does not exist.** It ran
   `cd projects/algocratic-futures/backend` then `pytest tests/`. There is no
   `backend/tests/`. The step exited 4 — a usage error, not a test result.
   **Cleared 2026-07-31.**

   Pytest was never going to work here whatever the path. These files hold zero
   `def test_*` functions, and the one `class Test*` is `TestResult`, a
   dataclass pytest declines to collect. Correcting the path would have moved
   exit 4 to exit 5, *no tests collected*, and told nobody anything. They are
   scripts with a `main()` returning pass or fail, which is the convention
   `CLAUDE.md` documents. The workflow now runs them that way.

4. **A hardcoded path inside the gate itself.** With obstacle 3 cleared,
   `test_liza_flash_compatibility.py` ran its five checks, passed all five,
   printed `READY FOR DEPLOYMENT`, and then exited 1 writing its results to
   `/Users/norrisa/Documents/dev/github/the_intern/...` — one laptop, absent
   everywhere else. The next line already printed the *relative* filename, so
   the absolute path was a slip rather than a decision. **Cleared 2026-07-31**
   by writing beside the file instead of beside whoever runs it.

   This was the fourth obstacle in the series and it was invisible until the
   third cleared, exactly like the three before it.

Separately, and not in that series:

5. **`agent_tier_tests.yml` filters on paths that do not exist.** Its `paths:` are
   `agent_prompts_tiered.py`, `test_agent_tiers.py`, `agent_system.py` — matched
   from the repository root. These files are at
   `projects/algocratic-futures/backend/`. The filter never matches, so the
   workflow never triggers. It would also fail if it did: it runs
   `pip install -r requirements.txt` with no working directory, and there is no
   requirements file at the repository root.

**Now wired, and it runs.** As of 2026-07-31 `deploy.yml` runs
`test_agent_tiers.py` and `test_liza_flash_compatibility.py` as scripts on
every push and pull request, on Python 3.9 and 3.11. Both exit 0. The gate that
had never executed once now executes, and what it reports is a result rather
than a usage error.

`test_trigger.py` is deliberately not in that list. It is three comment lines
with no code, written to poke the review workflow into running. It is named
`test_*` and it is not a test, and running it would have contributed a
guaranteed exit 0 that measured nothing — which is the shape of the whole
problem this file records.

## The spike — the MUD, for AlgoCon in May

- `tests/test_integration.py`
- `tests/test_agent_conversation.py`
- `tests/test_database.py`
- and the MUD itself: `backend/mud_game.py`, `backend/terminal_mud.py`,
  `backend/room_system.py`

This is a proposed spike, aimed at AlgoCon in May. It is **not** a gate. Its
failures are spike findings and must not block unrelated work.

### Known spike finding, unfixed

`backend/mud_game.py` cannot import on any published version of `adventurelib`:

```python
Room.add_direction('arcade', 'boardwalk')
Room.add_direction('tunnel', 'boardwalk')   # KeyError: 'boardwalk' is already a direction!
```

`add_direction` registers both the forward and the reverse name, so the second
call always collides. Because the requirements file pinned a version that was
never published, this code has never executed anywhere and nothing had reported
it. Found 2026-07-30 while re-pinning to `1.2.1`.

## Why the labels matter

Fixing the pin surfaced the `pytest tests/` failure that the pin had been hiding,
which surfaced the question of which suite gates the repository. One broken thing
concealed the next. Recording which is which is what stops that stack rebuilding
itself.
