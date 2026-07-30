# What is a gate here, and what is a spike

Two sets of tests live under this project and they are not the same kind of thing.
Labelled here because the distinction was established in conversation and would
otherwise be lost.

## The gate — `backend/test_*.py`

- `backend/test_agent_tiers.py`
- `backend/test_liza_flash_compatibility.py`
- `backend/test_trigger.py`

These are the gate. **They have never run.** Not "run and passed", not "run and
failed" — never executed, by anything, once.

Two independent reasons, both still true:

1. **`deploy.yml` points at a directory that does not exist.** It runs
   `cd projects/algocratic-futures/backend` then `pytest tests/`. There is no
   `backend/tests/`. The step exits 4. Until 2026-07-30 nothing had ever reached
   it, because `requirements.txt` pinned `adventurelib==2.0.0`, a version never
   published, so `pip install` failed first.

2. **`agent_tier_tests.yml` filters on paths that do not exist.** Its `paths:` are
   `agent_prompts_tiered.py`, `test_agent_tiers.py`, `agent_system.py` — matched
   from the repository root. These files are at
   `projects/algocratic-futures/backend/`. The filter never matches, so the
   workflow never triggers. It would also fail if it did: it runs
   `pip install -r requirements.txt` with no working directory, and there is no
   requirements file at the repository root.

**Not wired here on purpose.** Where to queue these safely is undecided. A gate
that has never run is an unknown, not a pass, and switching it on without
choosing where it runs would convert an unknown into a red wall.

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
