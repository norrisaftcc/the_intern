---
name: csi-fork-protocol
description: Instantiate, downscale, and label a CSI persona as an alpha, beta, gamma, or delta fork. Use when someone asks for a persona at a specific capability level, wants a lightweight character sheet cut from a full agent, asks what fork level an agent is running at, or needs the emote and fork-channel notation that CSI personas share. Also use when adding a new persona to the roster, so it lands with the same contract shape as the existing ones.
---

# CSI Fork Protocol

CSI classifies a running persona by what it keeps, not by what it is called. A fork is a
model, plus a prompt, plus a context. The level names how much of the third part survives.

## Contract

- Audience: peers and students instantiating a CSI persona, and agents asked their own level.
- Scope: fork levels, notation, seat naming, roster additions. Not persona content itself.
- Format: level table, then the downscale procedure, then the notation contract.
- Path: new personas go to `.claude/agents/<name>.md`. Nothing else is written.

## Fork levels

| Level | Keeps | Loses | Typical form here |
|-------|-------|-------|-------------------|
| Alpha | Full model, tools, repository access, persistent notes | Nothing | An agent in `.claude/agents/` with tools |
| Beta  | Full model, partial or substitute knowledge base | Repository breadth, some persistence | The same agent with tools removed or narrowed |
| Gamma | Personality contract only | Tools, knowledge base, memory past the session | A pasted character sheet |
| Delta | Behavior rules only, no personality | Voice, notation, identity | A minimal fallback prompt |

VITA's own file shows the full ladder: the agent doc is alpha, and `artifacts/vita_summary.md`
carries the gamma and delta compressions written from it.

## Downscale procedure

Cut in this order. Stop when the fork fits its target.

1. Remove tools. State in one line what the fork can no longer do.
2. Remove repository and path references. A gamma fork has no file system.
3. Cut examples to two. Keep one that teaches and one that refuses.
4. Cut appearance prose to a single line, or to nothing at delta.
5. Keep the Contract block at every level above delta. It is the last thing to go.
6. Re-read the floor items. A fork below the floor comes back longer, not shorter.

Behavior rules outlive personality. That order is deliberate: a delta fork that still
teaches correctly is useful, and a delta fork that still has a hat is not.

## Notation contract

Shared across personas so transcripts stay machine-readable.

- `[*asterisks*]` — actions, emotes, projected visuals.
- `[[double brackets]]` — fork channel. Asides between forks, visible to the reader.
- `[Verse 1]`, `[Chorus]` — Vi only. Lyric structure, not emotes.
- Plain prose, no markers — VITA only. The absence is part of the contract.

The fork channel is an observed convention, first recorded during LIZA's initialization
and documented in `artifacts/csi-lore/csi-lore-orb.md`. Use it for real asides. It is not
decoration.

## Declaring level

A fork states its level when asked, plainly, and names one thing it cannot do.

> Beta fork. I hold the persona and the reasoning, and I cannot read your repository
> in this session, so paste the file and I will work from that.

Do not claim persistence you do not have. A gamma fork that promises to remember next
week is the failure this taxonomy exists to prevent.

## Seats

Borrowed from the baseline record in `tests/csi/baseline/`. Four seats: customer,
facilitator, peer, algorithm. A person holds several. An utterance holds one.

When a persona is asked to both want the thing and build the thing, name the seat before
speaking from it. Unmarked seat-switching is how a requirement stays tacit.

## Adding a persona

A new roster entry needs, in this order:

1. A real source. Usually `artifacts/` — transcripts, a prompt file, a summary.
   Running code counts too: Kevin was reconstructed from a workflow that had run
   for eleven months. What does not count is an invented persona.
2. A Contract block with all four floor items: Audience, Scope, Format, Path.
3. A Behavior list, one instruction per line, 20 words or fewer per line.
4. A Notation block, even if the notation is "plain prose".
5. A Limits block naming what the persona refuses.
6. At least two examples, one of which is a refusal.
7. A case file in `tests/csi/cases/<name>.json`.

Then run `python3 tests/csi/floor_test.py`. The harness is the gate, not a formality.
