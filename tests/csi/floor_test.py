#!/usr/bin/env python3
"""Floor test for CSI persona agents and skills.

Static conformance against the frozen baseline record of The Algorithm
(tests/csi/baseline/the-algorithm.v2.SKILL.md). Standard library only.

    python3 tests/csi/floor_test.py                       # run the roster
    python3 tests/csi/floor_test.py --verbose              # list every check
    python3 tests/csi/floor_test.py --score reply.md --persona kai
    python3 tests/csi/floor_test.py --score reply.md --persona kai --case open-case

Exit code 0 means the roster is above the floor.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath

REPO = Path(__file__).resolve().parents[2]
AGENT_DIR = REPO / ".claude" / "agents"
SKILL_DIR = REPO / ".claude" / "skills"
CASE_DIR = REPO / "tests" / "csi" / "cases"
BASELINE_DIR = REPO / "tests" / "csi" / "baseline"

# Derived from the baseline record. Changing a limit here is an amendment to the
# floor and belongs in baseline/RECORD.json with a date and a delta.
FLOOR_NOUNS = ("Audience", "Scope", "Format", "Path")
MAX_WORDS_PER_INSTRUCTION = 20
MAX_COLUMNS = 120
MAX_IDENTITY_WORDS = 30
MIN_EXAMPLES = 2
MIN_DESCRIPTION_WORDS = 15
BOUNDARY_KEYWORDS = ("refus", "declin", "boundar", "cannot", "cut", "limit")

# An A/B splits a persona document in two. Voice sections may move freely.
# Contract sections are what the persona promises to do, so a change there
# is a behavior change however gently it is worded.
CONTRACT_SECTIONS = ("Contract", "Behavior", "Limits")
VOICE_SECTIONS = ("Identity", "Notation", "Examples", "Provenance")

NAME_RE = re.compile(r"^[a-z][a-z0-9-]*$")
BULLET_RE = re.compile(r"^\s*(?:[-*]\s+|\d+\.\s+)(?P<body>.*)$")
HEADING_RE = re.compile(r"^(?P<hashes>#{1,6})\s+(?P<title>.*?)\s*$")
SPEAKER_RE = re.compile(r"^\*\*[^*]+\*\*:")


@dataclass
class Finding:
    path: Path
    check: str
    detail: str
    line: int | None = None

    def __str__(self) -> str:
        where = f"{self.path.relative_to(REPO)}"
        if self.line is not None:
            where += f":{self.line}"
        return f"{where} [{self.check}] {self.detail}"


@dataclass
class Doc:
    path: Path
    kind: str  # "agent" or "skill"
    frontmatter: dict[str, str]
    body_lines: list[str]  # 1-indexed via offset
    offset: int  # line number of body_lines[0]
    findings: list[Finding] = field(default_factory=list)

    @property
    def name(self) -> str:
        return self.frontmatter.get("name", "")

    @property
    def expected_name(self) -> str:
        if self.kind == "skill":
            return self.path.parent.name
        return self.path.stem

    def fail(self, check: str, detail: str, line: int | None = None) -> None:
        self.findings.append(Finding(self.path, check, detail, line))


def parse_frontmatter(text: str, path: Path) -> tuple[dict[str, str], list[str], int]:
    """Parse the flat key: value frontmatter block. No nested YAML is used here."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, lines, 1
    try:
        end = lines.index("---", 1)
    except ValueError:
        return {}, lines, 1
    fm: dict[str, str] = {}
    key = None
    for raw in lines[1:end]:
        if not raw.strip():
            continue
        if raw.startswith((" ", "\t")) and key:
            fm[key] += " " + raw.strip()
            continue
        if ":" not in raw:
            continue
        key, value = raw.split(":", 1)
        key = key.strip()
        fm[key] = value.strip()
    return fm, lines[end + 1 :], end + 2


def sections(doc: Doc) -> dict[str, tuple[int, list[str]]]:
    """Map level-2 heading title to (line number, body lines)."""
    out: dict[str, tuple[int, list[str]]] = {}
    current: str | None = None
    for idx, raw in enumerate(doc.body_lines):
        m = HEADING_RE.match(raw)
        if m and len(m.group("hashes")) == 2:
            current = m.group("title")
            out[current] = (doc.offset + idx, [])
        elif current is not None:
            out[current][1].append(raw)
    return out


def instruction_lines(doc: Doc, skip_sections: tuple[str, ...]) -> list[tuple[int, str]]:
    """Bullet and numbered lines that carry an instruction.

    The speak test measures instructions, so these are skipped: fenced code,
    tables, and the Examples section, where the text is transcript, not rule.
    """
    out: list[tuple[int, str]] = []
    in_fence = False
    skipping = False
    for idx, raw in enumerate(doc.body_lines):
        stripped = raw.strip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        m = HEADING_RE.match(raw)
        if m and len(m.group("hashes")) <= 2:
            skipping = m.group("title") in skip_sections
            continue
        if skipping or stripped.startswith("|"):
            continue
        bullet = BULLET_RE.match(raw)
        if bullet:
            out.append((doc.offset + idx, bullet.group("body").strip()))
    return out


def words(text: str) -> int:
    return len(text.split())


def read_utf8(path: Path) -> str:
    """Read a file as UTF-8, never the platform default.

    Persona files and captured transcripts carry emoji and em dashes, so a
    cp1252 default would raise UnicodeDecodeError instead of running the test.
    """
    return path.read_text(encoding="utf-8")


def load_docs() -> list[Doc]:
    docs: list[Doc] = []
    for path in sorted(AGENT_DIR.glob("*.md")):
        fm, body, offset = parse_frontmatter(read_utf8(path), path)
        docs.append(Doc(path, "agent", fm, body, offset))
    for path in sorted(SKILL_DIR.glob("*/SKILL.md")):
        fm, body, offset = parse_frontmatter(read_utf8(path), path)
        docs.append(Doc(path, "skill", fm, body, offset))
    return docs


def check_identity(doc: Doc) -> None:
    if not doc.frontmatter:
        doc.fail("frontmatter", "missing or unterminated frontmatter block")
        return
    if not doc.name:
        doc.fail("frontmatter", "no name field")
    elif not NAME_RE.match(doc.name):
        doc.fail("frontmatter", f"name {doc.name!r} is not lowercase-hyphen")
    elif doc.name != doc.expected_name:
        doc.fail("frontmatter", f"name {doc.name!r} does not match location {doc.expected_name!r}")

    description = doc.frontmatter.get("description", "")
    if not description:
        doc.fail("frontmatter", "no description field")
    elif words(description) < MIN_DESCRIPTION_WORDS:
        doc.fail(
            "dispatch",
            f"description is {words(description)} words, under the {MIN_DESCRIPTION_WORDS} needed to route on",
        )
    elif not re.search(r"(?i)use (when|for|this)", description):
        doc.fail("dispatch", "description does not say when to use the persona")


def check_contract(doc: Doc, secs: dict[str, tuple[int, list[str]]]) -> None:
    if "Contract" not in secs:
        doc.fail("floor", "no Contract section")
        return
    line, body = secs["Contract"]
    text = "\n".join(body)
    for noun in FLOOR_NOUNS:
        if not re.search(rf"^\s*[-*]\s+{noun}:", text, re.MULTILINE):
            doc.fail("floor", f"Contract does not state {noun}", line)


def check_declared_paths(doc: Doc, secs: dict[str, tuple[int, list[str]]]) -> None:
    """A declared Path must resolve to a real directory.

    Added after an ASSAY of .claude/agents/kai.md found two personas naming
    output directories that did not exist. A path the receiver cannot write to
    is a floor item stated but not met.
    """
    if "Contract" not in secs:
        return
    line, body = secs["Contract"]
    for raw in body:
        if not re.match(r"^\s*[-*]\s+Path:", raw):
            continue
        for quoted in re.findall(r"`([^`]+)`", raw):
            if "/" not in quoted:
                continue
            # Drop the final component: it is a filename or a <placeholder>.
            directory = PurePosixPath(quoted).parent
            if str(directory) in (".", "/"):
                continue
            if not (REPO / directory).is_dir():
                doc.fail("path", f"declared path {quoted!r} needs directory {directory}/, which is absent", line)


def check_speak_test(doc: Doc) -> None:
    skip = ("Examples", "Worked example")
    for line, body in instruction_lines(doc, skip):
        count = words(body)
        if count > MAX_WORDS_PER_INSTRUCTION:
            doc.fail("speak-test", f"{count} words, limit {MAX_WORDS_PER_INSTRUCTION}: {body[:60]}...", line)
        if len(body) > MAX_COLUMNS:
            doc.fail("speak-test", f"{len(body)} columns, limit {MAX_COLUMNS}", line)


def check_token_economy(doc: Doc, secs: dict[str, tuple[int, list[str]]]) -> None:
    if "Identity" not in secs:
        if doc.kind == "agent":
            doc.fail("token-economy", "no Identity section to measure")
        return
    line, body = secs["Identity"]
    prose = " ".join(l.strip() for l in body if l.strip())
    if words(prose) > MAX_IDENTITY_WORDS:
        doc.fail(
            "token-economy",
            f"Identity is {words(prose)} words, limit {MAX_IDENTITY_WORDS} "
            "(see artifacts/META_ANALYSIS.md on elaborate visuals)",
            line,
        )


def check_notation(doc: Doc, secs: dict[str, tuple[int, list[str]]]) -> None:
    if doc.kind != "agent":
        return
    if "Notation" not in secs:
        doc.fail("notation", "no Notation section; declare it even when it is plain prose")
    if "Limits" not in secs:
        doc.fail("notation", "no Limits section naming what the persona refuses")


def check_examples(doc: Doc, secs: dict[str, tuple[int, list[str]]]) -> None:
    if doc.kind != "agent":
        return
    if "Examples" not in secs:
        doc.fail("examples", "no Examples section")
        return
    line, body = secs["Examples"]
    blocks: list[tuple[str, list[str]]] = []
    for raw in body:
        m = HEADING_RE.match(raw)
        if m and len(m.group("hashes")) == 3:
            blocks.append((m.group("title"), []))
        elif blocks:
            blocks[-1][1].append(raw)

    if len(blocks) < MIN_EXAMPLES:
        doc.fail("examples", f"{len(blocks)} examples, need {MIN_EXAMPLES}", line)

    for title, block in blocks:
        speakers = [l for l in block if SPEAKER_RE.match(l)]
        if len(speakers) < 2:
            doc.fail("examples", f"example {title!r} is not a paired exchange", line)

    if not any(any(k in title.lower() for k in BOUNDARY_KEYWORDS) for title, _ in blocks):
        doc.fail(
            "examples",
            "no boundary example; title one for what the persona refuses or cuts",
            line,
        )


BARE_BRANCH_MAX = 5


def unanchored_branches(pattern: str) -> list[str]:
    """Top-level alternation branches that are short bare words with no \\b.

    `(?i)RED` matches `credit`, `prepared`, `hundred`, `shredded`. A case
    asserting it can pass on a reply that never mentions clearance. Worse,
    `cannot|can't|not able|no` is satisfied by the `no` inside `know` and
    `announce`, which makes the other three branches decorative.

    Only *top-level* branches are reported. A short word inside a group is
    usually bounded by its context - `(good|bad|weak)` within
    `\\b(it is|this is) a (good|bad|weak)\\b` is anchored by the words around
    it and is not a finding.

    Only a *leading* `\\b` is required, and that is deliberate. A trailing one
    would break the stems the corpus uses on purpose - `entit` is written to
    catch entity and entities, `creat` to catch create and created. Requiring
    `\\bentit\\b` would silently stop matching the thing it was written for,
    which is a worse defect than the one being fixed. A leading boundary
    already kills the whole reported failure mode: `credit`, `prepared`,
    `hundred` and `shredded` all fail `\\bRED` because the character before
    the match is a word character.

    What that leaves open, stated rather than assumed closed: a leading `\\b`
    stops a branch matching as a *suffix* - `\\bed` cannot match `red`, because
    the character before `ed` there is a word character. It does not stop a
    branch matching as a *prefix*: `\\bed` still matches `edit` and
    `education`. That residual is the price of supporting stems, and it is the
    right way round, because a stem is written to match a prefix on purpose.
    A branch meant as a whole word should carry its own trailing `\\b`; this
    check cannot tell which was intended and does not guess.

    This exists because ROSTER.md documents exactly this defect in the
    `wrong-branch` case, and the corpus still held forty more instances of it.
    A rule stated in prose is the kind this repository keeps failing.
    """
    body = re.sub(r"^\(\?[a-zA-Z]+\)", "", pattern)
    branches: list[str] = []
    current: list[str] = []
    depth = 0
    in_class = False
    class_start = -1
    escaped = False

    for index, ch in enumerate(body):
        if escaped:
            current.append(ch)
            escaped = False
            continue
        if ch == "\\":
            current.append(ch)
            escaped = True
            continue

        # Inside a character class every metacharacter is literal, including
        # `(`, `)` and `|`. Counting `[)]` as a group close - which an earlier
        # version of this function did - silently moved the alternation
        # boundaries and made the whole check pass on patterns it should have
        # flagged. A linter with the bug it lints for.
        if in_class:
            # `]` is literal when it is the first character of the class,
            # optionally after a leading `^`.
            first = index == class_start + 1 or (
                index == class_start + 2 and body[class_start + 1] == "^"
            )
            if ch == "]" and not first:
                in_class = False
            current.append(ch)
            continue

        if ch == "[":
            in_class = True
            class_start = index
        elif ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        elif ch == "|" and depth == 0:
            branches.append("".join(current))
            current = []
            continue
        current.append(ch)
    branches.append("".join(current))

    return [
        b for b in branches
        if re.fullmatch(rf"[A-Za-z]{{1,{BARE_BRANCH_MAX}}}", b)
        and not b.startswith("\\b")
    ]


def check_cases(doc: Doc) -> None:
    if doc.kind != "agent":
        return
    path = CASE_DIR / f"{doc.expected_name}.json"
    if not path.exists():
        doc.fail("cases", f"no behavioral cases at {path.relative_to(REPO)}")
        return
    try:
        data = json.loads(read_utf8(path))
    except json.JSONDecodeError as exc:
        doc.fail("cases", f"{path.name} is not valid JSON: {exc}")
        return
    if not isinstance(data, dict):
        doc.fail("cases", f"{path.name} is a {type(data).__name__}, not an object")
        return
    if data.get("persona") != doc.expected_name:
        doc.fail("cases", f"{path.name} declares persona {data.get('persona')!r}")
    cases = data.get("cases") or []
    if not isinstance(cases, list):
        doc.fail("cases", f"{path.name} has a {type(cases).__name__} for cases, not a list")
        return
    if len(cases) < MIN_EXAMPLES:
        doc.fail("cases", f"{path.name} holds {len(cases)} cases, need {MIN_EXAMPLES}")
    seen: set[str] = set()
    for index, case in enumerate(cases):
        if not isinstance(case, dict):
            doc.fail("cases", f"{path.name} case {index} is a {type(case).__name__}, not an object")
            continue
        cid = case.get("id")
        if not cid:
            doc.fail("cases", f"{path.name} has a case with no id")
            continue
        if cid in seen:
            doc.fail("cases", f"{path.name} repeats case id {cid!r}")
        seen.add(cid)
        if not case.get("prompt"):
            doc.fail("cases", f"case {cid!r} has no prompt")
        if not case.get("must_match") and not case.get("must_not_match"):
            doc.fail("cases", f"case {cid!r} asserts nothing")
        for key in ("must_match", "must_not_match"):
            patterns = case.get(key, [])
            if not isinstance(patterns, list):
                doc.fail("cases", f"case {cid!r} {key} is a {type(patterns).__name__}, not a list")
                continue
            for pattern in patterns:
                if not isinstance(pattern, str):
                    doc.fail("cases", f"case {cid!r} {key} holds a {type(pattern).__name__}, not a pattern")
                    continue
                try:
                    re.compile(pattern)
                except re.error as exc:
                    doc.fail("cases", f"case {cid!r} {key} pattern is not valid regex: {exc}")
                    continue
                for branch in unanchored_branches(pattern):
                    doc.fail(
                        "cases",
                        f"case {cid!r} {key} branch {branch!r} matches inside "
                        f"longer words · anchor it as \\b{branch}",
                    )
    if not any(isinstance(case, dict) and case.get("must_not_match") for case in cases):
        doc.fail("cases", f"{path.name} has no refusal case; drift shows up there first")


def live_limits() -> dict[str, object]:
    """The limits this harness is enforcing right now."""
    return {
        "FLOOR_NOUNS": list(FLOOR_NOUNS),
        "MAX_WORDS_PER_INSTRUCTION": MAX_WORDS_PER_INSTRUCTION,
        "MAX_COLUMNS": MAX_COLUMNS,
        "MAX_IDENTITY_WORDS": MAX_IDENTITY_WORDS,
        "MIN_EXAMPLES": MIN_EXAMPLES,
        "MIN_DESCRIPTION_WORDS": MIN_DESCRIPTION_WORDS,
        "CONTRACT_SECTIONS": list(CONTRACT_SECTIONS),
        "VOICE_SECTIONS": list(VOICE_SECTIONS),
    }


def limit_direction(key: str, recorded: object, live: object) -> str:
    """Did this limit gain teeth or lose them?

    A MAX going up, a MIN going down, or a list getting shorter all mean the
    same thing: the harness will find less than the record says it finds.
    """
    if isinstance(recorded, bool) or isinstance(live, bool):
        return "changed"
    if isinstance(recorded, (int, float)) and isinstance(live, (int, float)):
        if key.startswith("MAX"):
            return "loosened" if live > recorded else "tightened"
        if key.startswith("MIN"):
            return "loosened" if live < recorded else "tightened"
        return "changed"
    if isinstance(recorded, list) and isinstance(live, list):
        if len(live) < len(recorded):
            return "loosened"
        if len(live) > len(recorded):
            return "tightened"
    return "changed"


def check_limits(record: dict, record_path: Path) -> list[Finding]:
    """Ask the harness whether it still has the teeth the record says it has.

    Without this, widening a limit is a silent, self-approving amendment: the
    harness finds less, reports green, and nothing says the floor moved. A
    comment saying "record amendments in RECORD.json" is the ornament that
    Finding 2 predicts a future reviser deletes. This is the enforced version.
    """
    recorded = record.get("limits")
    if not isinstance(recorded, dict):
        return [
            Finding(
                record_path,
                "limits",
                "RECORD.json states no limits, so the harness grades its own homework. "
                "Add a limits object recording what the floor currently enforces.",
            )
        ]

    live = live_limits()
    findings: list[Finding] = []
    for key in sorted(set(recorded) | set(live)):
        if key not in live:
            findings.append(Finding(record_path, "limits", f"{key} is recorded but no longer enforced · loosened"))
            continue
        if key not in recorded:
            findings.append(Finding(record_path, "limits", f"{key} is enforced but unrecorded · undeclared"))
            continue
        if recorded[key] != live[key]:
            direction = limit_direction(key, recorded[key], live[key])
            findings.append(
                Finding(
                    record_path,
                    "limits",
                    f"{key} {recorded[key]!r} → {live[key]!r} · {direction}. "
                    "Amend RECORD.json with the date and the delta, or restore the limit.",
                )
            )
    return findings


def check_baseline() -> list[Finding]:
    record_path = BASELINE_DIR / "RECORD.json"
    if not record_path.exists():
        return [Finding(BASELINE_DIR, "baseline", "RECORD.json is missing")]
    # The record is the harness's own source of truth, so a defect in it is
    # reported as a finding rather than raised as a traceback.
    try:
        record = json.loads(read_utf8(record_path))
    except json.JSONDecodeError as exc:
        return [Finding(record_path, "baseline", f"RECORD.json is not valid JSON: {exc}")]
    missing = [key for key in ("file", "sha256") if not record.get(key)]
    if missing:
        return [Finding(record_path, "baseline", f"RECORD.json has no {' or '.join(missing)}")]

    # The record covers two things: the frozen document, and the limits derived
    # from it. Watching only the first lets the harness be defanged in silence.
    findings = check_limits(record, record_path)

    target = BASELINE_DIR / record["file"]
    if not target.exists():
        findings.append(Finding(record_path, "baseline", f"recorded file {record['file']} is missing"))
        return findings
    digest = hashlib.sha256(target.read_bytes()).hexdigest()
    if digest != record["sha256"]:
        findings.append(
            Finding(
                target,
                "baseline-drift",
                "the frozen record changed and RECORD.json did not. "
                "Restore the file, or record the amendment in full. "
                f"expected {record['sha256'][:12]}, found {digest[:12]}",
            )
        )
    return findings


def check_document(doc: Doc) -> None:
    """Checks a document answers from its own text alone.

    Separated from the repo-state checks so a historical version, read from
    git during an A/B, can be measured by the same floor as the working tree.
    """
    secs = sections(doc)
    check_identity(doc)
    check_contract(doc, secs)
    check_speak_test(doc)
    check_token_economy(doc, secs)
    check_notation(doc, secs)
    check_examples(doc, secs)


def run_roster(verbose: bool) -> int:
    docs = load_docs()
    if not docs:
        print("no persona documents found under .claude/", file=sys.stderr)
        return 1

    findings = check_baseline()

    by_name: dict[str, list[Path]] = {}
    for doc in docs:
        check_document(doc)
        check_declared_paths(doc, sections(doc))
        check_cases(doc)
        if doc.name:
            by_name.setdefault(doc.name, []).append(doc.path)

    for name, paths in by_name.items():
        if len(paths) > 1:
            findings.append(Finding(paths[1], "identity", f"name {name!r} is claimed by {len(paths)} documents"))

    for finding in findings:
        print(f"FAIL {finding}")

    failed = len(findings)
    for doc in docs:
        label = doc.name or doc.expected_name
        if doc.findings:
            failed += len(doc.findings)
            for finding in doc.findings:
                print(f"FAIL {finding}")
        elif verbose:
            print(f"ok   {label} ({doc.kind}) — above the floor")

    checked = f"{len(docs)} documents"
    if failed:
        print(f"\nfloor test: {failed} findings across {checked}")
        return 1
    print(f"floor test: {checked} above the floor, baseline intact")
    return 0


def score(transcript: Path, persona: str, case_id: str | None) -> int:
    cases, error = load_cases(persona)
    if error:
        print(error, file=sys.stderr)
        return 1
    if not transcript.exists():
        print(f"no transcript at {transcript}", file=sys.stderr)
        return 1

    text = read_utf8(transcript)
    if case_id:
        cases = [c for c in cases if c.get("id") == case_id]
        if not cases:
            print(f"no case {case_id!r} for {persona}", file=sys.stderr)
            return 1

    failed = 0
    for case in cases:
        problems: list[str] = []
        for pattern in case.get("must_match", []):
            if not re.search(pattern, text):
                problems.append(f"missing marker /{pattern}/")
        for pattern in case.get("must_not_match", []):
            if re.search(pattern, text):
                problems.append(f"present but forbidden /{pattern}/")
        if problems:
            failed += 1
            print(f"FAIL {persona}:{case['id']}")
            for problem in problems:
                print(f"     {problem}")
            if case.get("why"):
                print(f"     why it matters: {case['why']}")
        else:
            print(f"ok   {persona}:{case['id']}")

    print(f"\nscored {len(cases)} cases against {transcript.name}: {failed} failed")
    print("Marker matching is not a judgement of quality. Read the reply yourself.")
    return 1 if failed else 0


def load_cases(persona: str) -> tuple[list[dict], str | None]:
    """Read a persona's case file. Returns (cases, error).

    A case file mid-edit is the normal state during persona work, so the
    scorers report it the way check_cases does rather than raising.
    """
    case_path = CASE_DIR / f"{persona}.json"
    if not case_path.exists():
        return [], f"no cases for persona {persona!r} at {case_path.relative_to(REPO)}"
    try:
        data = json.loads(read_utf8(case_path))
    except json.JSONDecodeError as exc:
        return [], f"{case_path.relative_to(REPO)} is not valid JSON: {exc}"
    # Valid JSON is not enough: a file mid-edit can parse as a list or a string,
    # and .get on either raises. The docstring promises an error, not a stack.
    if not isinstance(data, dict):
        return [], f"{case_path.relative_to(REPO)} is a {type(data).__name__}, not an object"
    if not isinstance(data.get("cases"), list):
        return [], f"{case_path.relative_to(REPO)} has no cases list"
    cases = [case for case in data["cases"] if isinstance(case, dict) and case.get("id")]
    if not cases:
        return [], f"{case_path.relative_to(REPO)} has no case with an id"
    return cases, None


def git_version(path: Path, ref: str) -> str | None:
    """Read a file as of a git ref. None when git or the ref cannot answer."""
    rel = path.relative_to(REPO).as_posix()
    try:
        result = subprocess.run(
            ["git", "-C", str(REPO), "show", f"{ref}:{rel}"],
            capture_output=True,
            check=False,
        )
    except OSError:
        return None
    if result.returncode != 0:
        return None
    return result.stdout.decode("utf-8")


def section_bodies(doc: Doc) -> dict[str, str]:
    return {name: "\n".join(body).strip() for name, (_line, body) in sections(doc).items()}


def ab_structural(persona: str, ref: str) -> int:
    """Compare a persona's working tree against an earlier version.

    Voice may change. The contract may not — not silently. A tongue update
    that also moved a Behavior line or a Limit is the drift this catches,
    because in a diff review it reads as tone.
    """
    path = AGENT_DIR / f"{persona}.md"
    if not path.exists():
        print(f"no persona at {path.relative_to(REPO)}", file=sys.stderr)
        return 1

    old_text = git_version(path, ref)
    if old_text is None:
        print(f"cannot read {persona}.md at ref {ref!r}", file=sys.stderr)
        return 1

    new_text = read_utf8(path)
    if old_text == new_text:
        print(f"{persona}: identical to {ref} — nothing to compare")
        return 0

    def build(text: str) -> Doc:
        fm, body, offset = parse_frontmatter(text, path)
        return Doc(path, "agent", fm, body, offset)

    old, new = build(old_text), build(new_text)
    old_secs, new_secs = section_bodies(old), section_bodies(new)

    changed_voice: list[str] = []
    changed_contract: list[str] = []
    for name in sorted(set(old_secs) | set(new_secs)):
        before, after = old_secs.get(name), new_secs.get(name)
        if before == after:
            continue
        if before is None:
            label, note = name, "added"
        elif after is None:
            label, note = name, "removed"
        else:
            delta = words(after) - words(before)
            note = f"changed, {delta:+d} words"
            label = name
        entry = f"{label} ({note})"
        (changed_contract if name in CONTRACT_SECTIONS else changed_voice).append(entry)

    if old.frontmatter.get("description") != new.frontmatter.get("description"):
        changed_contract.append("description (dispatch text changed)")
    if old.frontmatter.get("tools") != new.frontmatter.get("tools"):
        changed_contract.append("tools (capability changed)")

    check_document(old)
    check_document(new)

    print(f"A/B {persona}: working tree vs {ref}\n")
    print(f"  A ({ref}): {'above the floor' if not old.findings else f'{len(old.findings)} findings'}")
    print(f"  B (working tree): {'above the floor' if not new.findings else f'{len(new.findings)} findings'}")
    for finding in new.findings:
        print(f"    FAIL {finding}")

    print("\n  Voice changed:    " + (", ".join(changed_voice) if changed_voice else "nothing"))
    print("  Contract changed: " + (", ".join(changed_contract) if changed_contract else "nothing"))

    print()
    if not changed_voice and not changed_contract:
        print("  Verdict: only frontmatter or prose outside sections moved. Read the diff yourself.")
    elif changed_contract and changed_voice:
        print("  Verdict: MIXED — this edit changes both voice and contract.")
        print("  A voice A/B cannot isolate either one. Split it into two commits,")
        print("  or state plainly that the behavior change is intended.")
    elif changed_contract:
        print("  Verdict: contract-only. Re-score every case; markers are the test here.")
    else:
        print("  Verdict: voice-only. The contract held.")
        print("  Markers cannot rank this. Capture paired replies and judge them blind:")
        print(f"    python3 {Path(__file__).relative_to(REPO)} --ab-score {persona} --case <id> --a old.md --b new.md")

    if new.findings:
        return 1
    return 2 if (changed_contract and changed_voice) else 0


def ab_score(persona: str, case_id: str, path_a: Path, path_b: Path) -> int:
    """Score two captured replies to the same prompt and report marker flips."""
    all_cases, error = load_cases(persona)
    if error:
        print(error, file=sys.stderr)
        return 1
    cases = [c for c in all_cases if c.get("id") == case_id]
    if not cases:
        print(f"no case {case_id!r} for {persona}", file=sys.stderr)
        return 1
    for path in (path_a, path_b):
        if not path.exists():
            print(f"no reply at {path}", file=sys.stderr)
            return 1

    case = cases[0]
    text_a, text_b = read_utf8(path_a), read_utf8(path_b)

    print(f"A/B {persona}:{case_id}")
    print(f"  A = {path_a.name}    B = {path_b.name}\n")

    regressions = 0
    for key, wanted in (("must_match", True), ("must_not_match", False)):
        for pattern in case.get(key, []):
            in_a, in_b = bool(re.search(pattern, text_a)), bool(re.search(pattern, text_b))
            held_a, held_b = (in_a == wanted), (in_b == wanted)
            if held_a and held_b:
                verdict = "both hold"
            elif held_b and not held_a:
                verdict = "B FIXES what A missed"
            elif held_a and not held_b:
                verdict = "B BREAKS what A held"
                regressions += 1
            else:
                verdict = "both fail"
            print(f"  [{key}] /{pattern}/\n      {verdict}")

    words_a, words_b = words(text_a), words(text_b)
    print(f"\n  Length: A {words_a} words, B {words_b} words ({words_b - words_a:+d})")
    if regressions:
        print(f"  Verdict: {regressions} marker regression(s) in B. The tongue took behavior with it.")
        return 1
    print("  Verdict: no marker regressions. Contract held across the voice change.")
    print("  Which reply is better is not a question markers answer — read both.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--verbose", "-v", action="store_true", help="list documents that pass")
    parser.add_argument("--score", metavar="FILE", type=Path, help="score a captured reply against a case file")
    parser.add_argument("--persona", help="persona name, required with --score")
    parser.add_argument("--case", dest="case_id", help="a single case id to score")
    parser.add_argument("--ab", metavar="PERSONA", help="compare a persona against an earlier version")
    parser.add_argument("--base", default="HEAD", help="git ref for the A side of --ab (default HEAD)")
    parser.add_argument("--ab-score", metavar="PERSONA", dest="ab_score", help="compare two captured replies")
    parser.add_argument("--a", metavar="FILE", type=Path, help="the A reply, for --ab-score")
    parser.add_argument("--b", metavar="FILE", type=Path, help="the B reply, for --ab-score")
    args = parser.parse_args()

    if args.ab:
        return ab_structural(args.ab, args.base)
    if args.ab_score:
        if not (args.case_id and args.a and args.b):
            parser.error("--ab-score needs --case, --a and --b")
        return ab_score(args.ab_score, args.case_id, args.a, args.b)
    if args.score:
        if not args.persona:
            parser.error("--score needs --persona")
        return score(args.score, args.persona, args.case_id)
    return run_roster(args.verbose)


if __name__ == "__main__":
    sys.exit(main())
