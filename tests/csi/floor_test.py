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
    if data.get("persona") != doc.expected_name:
        doc.fail("cases", f"{path.name} declares persona {data.get('persona')!r}")
    cases = data.get("cases") or []
    if len(cases) < MIN_EXAMPLES:
        doc.fail("cases", f"{path.name} holds {len(cases)} cases, need {MIN_EXAMPLES}")
    seen: set[str] = set()
    for case in cases:
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
            for pattern in case.get(key, []):
                try:
                    re.compile(pattern)
                except re.error as exc:
                    doc.fail("cases", f"case {cid!r} {key} pattern is not valid regex: {exc}")
    if not any(case.get("must_not_match") for case in cases):
        doc.fail("cases", f"{path.name} has no refusal case; drift shows up there first")


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
    target = BASELINE_DIR / record["file"]
    if not target.exists():
        return [Finding(record_path, "baseline", f"recorded file {record['file']} is missing")]
    digest = hashlib.sha256(target.read_bytes()).hexdigest()
    if digest != record["sha256"]:
        return [
            Finding(
                target,
                "baseline-drift",
                "the frozen record changed and RECORD.json did not. "
                "Restore the file, or record the amendment in full. "
                f"expected {record['sha256'][:12]}, found {digest[:12]}",
            )
        ]
    return []


def run_roster(verbose: bool) -> int:
    docs = load_docs()
    if not docs:
        print("no persona documents found under .claude/", file=sys.stderr)
        return 1

    findings = check_baseline()

    by_name: dict[str, list[Path]] = {}
    for doc in docs:
        secs = sections(doc)
        check_identity(doc)
        check_contract(doc, secs)
        check_declared_paths(doc, secs)
        check_speak_test(doc)
        check_token_economy(doc, secs)
        check_notation(doc, secs)
        check_examples(doc, secs)
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
    case_path = CASE_DIR / f"{persona}.json"
    if not case_path.exists():
        print(f"no cases for persona {persona!r}", file=sys.stderr)
        return 1
    if not transcript.exists():
        print(f"no transcript at {transcript}", file=sys.stderr)
        return 1

    text = read_utf8(transcript)
    cases = json.loads(read_utf8(case_path)).get("cases", [])
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


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--verbose", "-v", action="store_true", help="list documents that pass")
    parser.add_argument("--score", metavar="FILE", type=Path, help="score a captured reply against a case file")
    parser.add_argument("--persona", help="persona name, required with --score")
    parser.add_argument("--case", dest="case_id", help="a single case id to score")
    args = parser.parse_args()

    if args.score:
        if not args.persona:
            parser.error("--score needs --persona")
        return score(args.score, args.persona, args.case_id)
    return run_roster(args.verbose)


if __name__ == "__main__":
    sys.exit(main())
