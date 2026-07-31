# Walking the beat — what this repository's CI has done since it acquired any

Case opened 2026-07-30. Reconstructing what `the_intern`'s own automation executed,
and what it reported while executing it, from the first workflow file to HEAD.

Scope is the machinery: the three workflow files, their placement history, what
they point at, and the dependency that stood in front of all of it. Not the
persona roster's content. Not whether any of this code is good.

Evidence available: `git log`, the working tree, the workflow YAML, and local
reproduction of the CI steps. Evidence not available: the GitHub Actions API.
Run counts, run conclusions and job logs are held only there. Where this case
needs them it says so and stops.

Repository state at the time of writing:

```
9bb1abe6d99a28dca2b105f031d1a77a44727fce  (HEAD -> claude/csi-agents-personas-ma5aj1, origin/claude/csi-agents-personas-ma5aj1) 2026-07-30T22:55:30+00:00
```

`git status --porcelain` was empty before this file was written and after every
verification run below.

---

## Timeline

Timestamps as `git` recorded them. Committer offsets vary between `-04:00` and
`+00:00` within this history; both forms are reproduced unaltered, and durations
below are computed in UTC.

| When (as recorded) | Commit | Event |
|---|---|---|
| 2025-07-29T20:44:56-04:00 | `44e4213` | `deploy.yml` created at `projects/algocratic-futures/.github/workflows/deploy.yml`. `backend/requirements.txt` created, 17 lines, no `adventurelib`. |
| 2025-07-30T11:53:36-04:00 | `708ab53` | `adventurelib==2.0.0` added to `backend/requirements.txt`. |
| 2025-08-18T22:09:12-04:00 | `d189f70` | `agent_tier_tests.yml` created at `projects/algocratic-futures/backend/.github/workflows/`. A second nested copy of `ai-code-review.yml` created. Branch `feature/algocratic-base-platform`. |
| 2025-08-18T22:26:54-04:00 | `4ad5fff` | "Test: Trigger AI code review workflow" — one line appended to `backend/test_trigger.py`. Feature branch. |
| 2025-08-18T22:30:11-04:00 | `9cd1d73` | `projects/algocratic-futures/.github/workflows/ai-code-review.yml` added **on `main`**. |
| 2025-08-18T22:30:43-04:00 | `e51c5d2` | "Test: Trigger AI review now that workflow is on main" — one line appended. Feature branch. |
| 2025-08-18T22:31:44-04:00 | `5f6baa3` | `.github/workflows/ai-code-review.yml` added on `main`. First workflow file at a path GitHub Actions reads, on the default branch. |
| 2025-08-18T22:32:28-04:00 | `c67d1e2` | "Test: Workflow should now trigger from root .github/workflows" — one line appended. Feature branch. |
| 2025-08-20T20:13:58-04:00 | `166102f` | All three workflows relocated to `.github/workflows/` — on `feature/algocratic-base-platform`, not on `main`. |
| 2026-07-30T16:25:22-04:00 | `0c3a9ab` | Merge PR #6. |
| 2026-07-30T20:28:00+00:00 | `e3b2b1b` | "Resolving merge conflicts with main branch". |
| 2026-07-30T16:28:39-04:00 | `161a3e5` | Merge PR #13. `deploy.yml` and `agent_tier_tests.yml` reach `main` at a readable path for the first time. |
| 2026-07-30T16:29:26-04:00 | `9da5c73` | Merge PR #23. |
| 2026-07-30T20:45:54+00:00 | `2c32bdc` | CSI harness hardening. |
| 2026-07-30T20:57:51+00:00 | `2dedf02` | `adventurelib` re-pinned `2.0.0` → `1.2.1`. |
| 2026-07-30T17:25:14-04:00 | `7adf359` | Merge PR #24. |
| 2026-07-30T21:27:21+00:00 | `42d3da9` | `projects/algocratic-futures/TESTING.md` written. |
| 2026-07-30T22:55:30+00:00 | `9bb1abe` | This investigator added. |

The three "Test: Trigger" commits at 22:26, 22:30 and 22:32 on 2025-08-18 were
pushed to `feature/algocratic-base-platform`. `ai-code-review.yml` triggers on
`pull_request` only:

```yaml
on:
  pull_request:
    types: [opened, synchronize, reopened]
```

A push to a branch fires nothing under that trigger. Whether a pull request was
open from that branch at 22:26–22:32 on 2025-08-18 is held by the API and is not
established here.

---

## Finding 1 — the dependency that stood in front of every run

`708ab53` pinned a version that was never published.

```
+adventurelib==2.0.0
```

Verified against PyPI on 2026-07-30:

```
releases: ['1.0', '1.0a1', '1.1', '1.2', '1.2.1']
```

Reproduced locally:

```
ERROR: Could not find a version that satisfies the requirement adventurelib==2.0.0 (from versions: 1.0a1, 1.0, 1.1, 1.2, 1.2.1)
ERROR: No matching distribution found for adventurelib==2.0.0
```

`deploy.yml`'s install step runs before its test step:

```yaml
    - name: Install dependencies
      run: |
        cd projects/algocratic-futures/backend
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-asyncio
```

The condition held from 2025-07-30T15:53:36Z to 2026-07-30T20:57:51Z — **365 days,
5 hours, 4 minutes**. Repaired by `2dedf02`, which recorded the same reading:

```
requirements.txt asked for adventurelib==2.0.0. PyPI's releases are 1.0a1,
1.0, 1.1, 1.2 and 1.2.1, so pip install failed and every CI run in this
repository died before any test executed. deploy.yml had never once passed,
on any branch, including main.
```

What reported it during those 365 days: nothing in the repository. There is no
lockfile check, no dependency audit, no scheduled install. The only thing that
would have observed it is `deploy.yml` itself, and see Finding 2 for where
`deploy.yml` was standing.

---

## Finding 2 — `deploy.yml` spent its first year at a path GitHub Actions does not read

Created 2025-07-29T20:44:56-04:00 by `44e4213` at:

```
projects/algocratic-futures/.github/workflows/deploy.yml
```

GitHub Actions reads `.github/workflows/` at the repository root only. `166102f`
relocated it on 2025-08-20T20:13:58-04:00, and named the relocation plainly:

```
RELOCATE WORKFLOWS TO REPOSITORY ROOT:
- Move AI code review workflow to proper .github/workflows location
- Move deployment workflow to proper .github/workflows location
- Move agent tier tests workflow to proper .github/workflows location
[...]
This remediation ensures GitHub Actions workflows execute properly
```

`166102f` is on `feature/algocratic-base-platform`. It is not on `main` until
merge `161a3e5`, 2026-07-30T16:28:39-04:00. A first-parent walk of `origin/main`
confirms the first commit whose tree carries anything under `.github/workflows/`:

```
FIRST: 5f6baa3|2025-08-18T22:31:44-04:00|Move AI code review workflow to repository root for proper GitHub Actions detection
```

— and that commit carries `ai-code-review.yml` alone.

`deploy.yml` triggers on `push: branches: [ main ]` and `pull_request: branches:
[ main ]`. Pushes to the feature branch did not match. Pull requests targeting
`main` from that branch did.

Duration at an unread path: 2025-07-30T00:44:56Z to 2026-07-30T20:28:39Z —
**365 days, 19 hours, 43 minutes**. Duration at a readable path on `main` as of
this writing: **2 hours, 26 minutes**.

A second copy of `ai-code-review.yml` remains nested, tracked, on `main`, today:

```
.github/workflows/agent_tier_tests.yml
.github/workflows/ai-code-review.yml
.github/workflows/deploy.yml
projects/algocratic-futures/.github/workflows/ai-code-review.yml
```

It is byte-identical to the root copy (`diff` reports no difference). It was
added on `main` by `9cd1d73` at 2025-08-18T22:30:11-04:00 and has never been
deleted from `main`'s history. `166102f` moved the copy on its own branch; the
`main`-side copy from `9cd1d73` survived the merge. That duplicate has stood for
**345 days, 20 hours, 25 minutes**. Nothing reads it.

---

## Finding 3 — `deploy.yml`'s test step points at a directory that does not exist

```yaml
    - name: Run tests
      run: |
        cd projects/algocratic-futures/backend
        pytest tests/ -v
```

There is no `projects/algocratic-futures/backend/tests/`. The backend's tests are
`test_*.py` in the backend's own root:

```
test_agent_tiers.py
test_liza_flash_compatibility.py
test_trigger.py
```

A separate suite sits one directory up, at `projects/algocratic-futures/tests/`:
`test_agent_conversation.py`, `test_database.py`, `test_integration.py`,
`__init__.py`.

Reproduced locally with `pytest 9.1.1` on Python 3.11.15:

```
collecting ... collected 0 items

============================ no tests ran in 0.00s =============================
ERROR: file or directory not found: tests/
```

```
EXIT CODE: 4
```

Exit 4 is a usage error. It is not a test result. The step fails, so the `deploy`
job — `needs: test` — does not run. That job would also have found nothing to
build: `docker build -t algocratic-futures:latest .` runs in
`projects/algocratic-futures`, and a filesystem search for `Dockerfile` returns
no match anywhere in this repository outside a vendored `gradio` virtualenv.

The step below it has never executed either:

```yaml
    - name: Check clearance system integrity
      run: |
        cd projects/algocratic-futures/backend
        python -c "from clearance_system import ClearanceLevel; assert ClearanceLevel.UV == 9"
```

`backend/clearance_system.py:20` reads `UV = 9`. The assertion would hold. It has
not been asked.

---

## Finding 4 — `agent_tier_tests.yml` has never been eligible to trigger

```yaml
on:
  push:
    branches: [ main, feature/*, agent-* ]
    paths:
      - 'agent_prompts_tiered.py'
      - 'test_agent_tiers.py'
      - 'agent_system.py'
  pull_request:
    branches: [ main ]
    paths:
      - 'agent_prompts_tiered.py'
      - 'test_agent_tiers.py'
      - 'agent_system.py'
```

`paths` are matched from the repository root. A search of the whole tree finds
those three names at exactly one location each:

```
./projects/algocratic-futures/backend/agent_system.py
./projects/algocratic-futures/backend/agent_prompts_tiered.py
./projects/algocratic-futures/backend/test_agent_tiers.py
```

No file at `agent_prompts_tiered.py`, `test_agent_tiers.py` or `agent_system.py`
has ever existed at the root. The filter has not matched once since the file was
created on 2025-08-18T22:09:12-04:00 — **345 days, 20 hours, 46 minutes**.

Had it matched, its first two steps would not have completed either:

```yaml
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-cov

    - name: Run Agent Tier Tests
      run: |
        cd backend
        python -m pytest test_agent_tiers.py -v --cov=agent_prompts_tiered --cov-report=xml
```

There is no `requirements.txt` at the repository root, and no `backend/`
directory at the repository root. Every one of the seven subsequent steps opens
with `cd backend`.

A workflow that never triggers produces no run, and a repository with no runs for
a check produces no red. Nothing reported this because nothing was asked to.

---

## Finding 5 — the extraction step in `ai-code-review.yml`

This is the workflow the investigator writing this file was named after. It has
stood on `main` at a readable path since 2025-08-18T22:31:44-04:00 — **345 days,
20 hours, 23 minutes** as of HEAD.

```yaml
          # Call Claude API
          response=$(curl -s -X POST "https://api.anthropic.com/v1/messages" \
            -H "Content-Type: application/json" \
            -H "x-api-key: ${{ secrets.CLAUDE_API_KEY }}" \
[...]
          # Extract review content
          review_content=$(echo "$response" | jq -r '.content[0].text // "Error: Failed to get AI review"')
```

`curl -s` without `-f` returns 0 on an HTTP error and prints the error body.
`jq -r` with the `//` alternative operator returns the fallback string rather
than a non-zero status. Reproduced against a representative API error body:

```
$ echo '{"type":"error","error":{"type":"authentication_error","message":"invalid x-api-key"}}' | jq -r '.content[0].text // "Error: Failed to get AI review"'
Error: Failed to get AI review
jq exit: 0
```

And against an empty response body:

```
$ echo '' | jq -r '.content[0].text // "Error: Failed to get AI review"'
jq exit on empty: 0
```

Empty output, exit 0. The step's final command is `echo "EOF" >> $GITHUB_OUTPUT`,
which also exits 0, so the step's status is 0 regardless of what the API returned.
The next step then posts whatever it got:

```yaml
            const comment = `## AI Code Review

            ${review}

            ---
            *Review generated by Kevin, the GitHub Algorithm Enforcer*`;
```

The posted comment carries the literal string `Error: Failed to get AI review`,
or nothing, and the check reports success either way. That is the mechanism. What
it actually produced on any given run is a matter of run history.

---

## Finding 6 — the repository's newest test harness has no workflow

`tests/csi/floor_test.py` was created 2026-07-30T02:28:40+00:00 by `e1fb7f2` and
amended five times the same day. It has cases at `tests/csi/cases/*.json` and a
frozen baseline at `tests/csi/baseline/`.

No workflow references it:

```
$ grep -rn "floor_test\|tests/csi" .github/
NO MATCH in .github
```

It has been unqueued for **20 hours** at time of writing. Recorded here as
sequence, not as an omission of a year's standing.

---

## `TESTING.md` verified

`projects/algocratic-futures/TESTING.md` (`42d3da9`, 2026-07-30T21:27:21+00:00)
is a prior hand-written labelling of part of this ground. It was treated as a
claim. Every checkable assertion in it holds.

- "There is no `backend/tests/`. The step exits 4." — Confirmed by reproduction.
  Exit code 4, `ERROR: file or directory not found: tests/`.
- "`requirements.txt` pinned `adventurelib==2.0.0`, a version never published" —
  Confirmed against PyPI and by reproduction of the install failure.
- "Its `paths:` are [...] matched from the repository root. These files are at
  `projects/algocratic-futures/backend/`." — Confirmed by tree search.
- "there is no requirements file at the repository root" — Confirmed.
- "`backend/mud_game.py` cannot import on any published version of
  `adventurelib`" — Confirmed. Installed `adventurelib==1.2.1` and imported:

```
  File "/home/user/the_intern/projects/algocratic-futures/backend/mud_game.py", line 16, in <module>
    Room.add_direction('tunnel', 'boardwalk')
  File "/usr/local/lib/python3.11/dist-packages/adventurelib.py", line 149, in add_direction
    raise KeyError('%r is already a direction!' % dir)
KeyError: "'boardwalk' is already a direction!"
```

One thing `TESTING.md` does not carry, and this case adds: the reason the gate
never ran is older than the pin. `deploy.yml` spent its first 365 days at
`projects/algocratic-futures/.github/workflows/`, where GitHub Actions does not
look, and reached `main` only 2 hours before this case was opened.

---

## Repairs already made, and when

Stated as record, not as assessment.

- `5f6baa3`, 2025-08-18T22:31:44-04:00 — `ai-code-review.yml` copied to the root
  `.github/workflows/` on `main`. The nested copy on `main` was not removed and
  is still present.
- `166102f`, 2025-08-20T20:13:58-04:00 — all three workflows relocated to the
  root on `feature/algocratic-base-platform`. Reached `main` 2026-07-30.
- `2dedf02`, 2026-07-30T20:57:51+00:00 — `adventurelib` re-pinned to `1.2.1`.
  Its message states what it deliberately did not change, including the
  `pytest tests/` path.
- `2c32bdc`, 2026-07-30T20:45:54+00:00 — CSI harness case readers hardened
  against malformed input; the undeclared `the-algorithm` dependency declared.

---

## What reported any of this

Nothing in the machinery. For each condition, the thing that would have observed
it is the thing that was wrong:

- The unpublished pin would have been caught by `deploy.yml`, which was at a path
  Actions does not read for 365 days.
- The missing `backend/tests/` would have been caught by `deploy.yml`, which
  failed at `pip install` before reaching it, for the same 365 days.
- The unmatched `paths:` filter in `agent_tier_tests.yml` would have been caught
  by `agent_tier_tests.yml` running, which the filter prevents.
- The `//` fallback in `ai-code-review.yml` would have been caught by a review
  that flagged it, which is the function the fallback suppresses.

What did report it: human and agent reading, on 2026-07-30, in commits `2dedf02`,
`42d3da9` and this file. Four conditions, all found the same day, none found by a
check.

---

## Unestablished

- **All run history.** Run counts, conclusions, durations, and job logs for
  `ai-code-review.yml`, `deploy.yml` and `agent_tier_tests.yml` live in the
  GitHub Actions API, which this investigation cannot reach. This case does not
  assert how many times any workflow ran, or what any run concluded. Where
  `artifacts/forensics/README.md` states the review workflow "ran for eleven
  months, produced zero reviews, and reported `success` for all but the first
  two", that is a claim recorded in this repository, not a record verified in
  this case.
- **Whether `secrets.CLAUDE_API_KEY` is set.** Secret existence is not visible
  from the tree. The fallback path fires identically whether the key is absent,
  invalid, or the request body is malformed, so the file cannot distinguish them.
- **Whether a pull request was open from `feature/algocratic-base-platform`
  during 2025-08-18T22:26–22:32.** The three "Test: Trigger" commits assert
  intent; only the API holds whether anything fired.
- **Whether PR #13, #23 or #24 produced `ai-code-review` runs**, and what those
  runs posted. Same reason.
- **The Python 3.9 matrix leg of `deploy.yml`.** Local reproduction ran on
  3.11.15 only. `2dedf02` records the same gap: "Verified on Python 3.11. The 3.9
  matrix leg is unverified." `agent_tier_tests.yml` additionally declares
  `python-version: [3.9, 3.10, 3.11]`; none of the three has been exercised.
- **Whether either AlgoCratic suite passes.** Neither was run in this case.
  Running them is a different job.
- **Why the nested copy of `ai-code-review.yml` survived merge `161a3e5`.** The
  merge resolution is recorded as a result, not as a decision; `e3b2b1b`
  ("Resolving merge conflicts with main branch") carries no note on this path.
