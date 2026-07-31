#!/usr/bin/env python3
"""The documents under docs/ are checked, not vouched for.

Three claims were being made about `docs/big-board.html` and
`docs/csi/shodann/calibration-brief.html` in a pull request description, each
one true at the time and none of them enforced:

    "both parse with no unclosed or mismatched tags"
    "the widget is byte-identical in both files"
    the palette is restated three times per file and must agree

A review named the double standard exactly. `.claude/agents/shodann.md` and
`.claude/skills/shodann-voice/SKILL.md` are also two copies expected to move
together, and they got a version stamp and a lint check *because comparing
bytes by hand was judged insufficient*. These two got a comment. The comment
even explains that two earlier copies of the same widget had already diverged
into an accessible one and a not-quite one — a note about drift, holding the
line against drift, by itself.

So this is that check. It is deliberately persona-unaware: `floor_test.py` is
scoped to `.claude/` on purpose, because `docs/csi/ROSTER.md` describes the
shared-base arrangement without being one and would false-positive if swept in.
Nothing here reads prose. It checks structure only.

    python3 tests/docs/artifact_test.py

Standard library only.
"""

from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
DOCS = REPO / "docs"

# Elements with no closing tag. A hand-written list rather than a dependency;
# if one is missing the parser reports a false unclosed tag, which fails loudly
# rather than passing quietly.
VOID = {
    "area", "base", "br", "col", "embed", "hr", "img", "input",
    "link", "meta", "param", "source", "track", "wbr",
}

REQUIRED_SCAFFOLD = (
    "<!DOCTYPE html>",
    '<meta charset="utf-8">',
    "<body>",
    "</html>",
)


class Balance(HTMLParser):
    """Tag balance only. Not a validator, and does not pretend to be one."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.stack: list[tuple[str, int]] = []
        self.errors: list[str] = []

    def handle_starttag(self, tag: str, attrs) -> None:
        if tag not in VOID:
            self.stack.append((tag, self.getpos()[0]))

    def handle_startendtag(self, tag: str, attrs) -> None:
        pass  # self-closing, balanced by construction

    def handle_endtag(self, tag: str) -> None:
        if not self.stack:
            self.errors.append(f"line {self.getpos()[0]}: stray </{tag}>")
            return
        open_tag, line = self.stack[-1]
        if open_tag == tag:
            self.stack.pop()
        else:
            self.errors.append(
                f"line {self.getpos()[0]}: </{tag}> closes <{open_tag}> "
                f"opened on line {line}"
            )


def html_files() -> list[Path]:
    return sorted(DOCS.rglob("*.html"))


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def rel(path: Path) -> str:
    return str(path.relative_to(REPO))


def check_parses() -> list[str]:
    """Every document is a whole document, and its tags balance.

    The scaffolding half exists because both of these shipped as *fragments*
    first: authored as embedded artifacts, where the host supplies the doctype
    and head. Opened from disk that is quirks mode with the encoding
    unspecified. Correct where they were rendered, wrong in a repository.
    """
    out = []
    for path in html_files():
        text = read(path)
        for needed in REQUIRED_SCAFFOLD:
            if needed not in text:
                out.append(f"{rel(path)}: missing {needed!r} — a fragment, not "
                           "a document. It will parse in quirks mode.")
        parser = Balance()
        parser.feed(text)
        for err in parser.errors:
            out.append(f"{rel(path)}: {err}")
        for tag, line in parser.stack:
            out.append(f"{rel(path)}: <{tag}> opened on line {line}, never closed")
    return out


SCRIPT_RE = re.compile(r"<script>(.*?)</script>", re.S)


def check_shared_widget() -> list[str]:
    """Every inline script under docs/ is the same script.

    Today that is the tab widget, in two files. The rule is stated as "all of
    them agree" rather than "these two agree" so that a third document cannot
    quietly introduce a third variant — which is the precise way the previous
    two copies diverged.

    If a document ever legitimately needs a *different* script, this check is
    the thing that must be reopened and argued with, on purpose.
    """
    scripts: dict[str, list[Path]] = {}
    for path in html_files():
        for body in SCRIPT_RE.findall(read(path)):
            if body.strip():
                scripts.setdefault(body, []).append(path)

    if len(scripts) <= 1:
        return []

    out = ["inline scripts under docs/ have diverged; they are meant to be one "
           "widget, pasted rather than shared:"]
    for body, paths in scripts.items():
        first = next((ln.strip() for ln in body.splitlines() if ln.strip()), "")
        out.append(f"    {len(body)} chars in {', '.join(rel(p) for p in paths)}"
                   f"  — starts {first[:60]!r}")
    out.append("    Extract it, or make them identical again. A comment asking "
               "for this is what failed last time.")
    return out


DECL_RE = re.compile(r"(--[\w-]+)\s*:\s*([^;]+);")


def block_after(text: str, opener: str) -> str | None:
    """The brace-balanced body following `opener`. None if absent."""
    i = text.find(opener)
    if i < 0:
        return None
    i = text.index("{", i)
    depth, j = 0, i
    while j < len(text):
        if text[j] == "{":
            depth += 1
        elif text[j] == "}":
            depth -= 1
            if depth == 0:
                return text[i + 1:j]
        j += 1
    return None


def tokens(block: str | None) -> dict[str, str]:
    if block is None:
        return {}
    return {m.group(1): m.group(2).strip() for m in DECL_RE.finditer(block)}


def check_theme_parity() -> list[str]:
    """The two ways of reaching a theme must agree.

    A viewer's OS preference arrives as `prefers-color-scheme`; their explicit
    toggle arrives as `data-theme` on the root and has to beat the media query.
    That means the palette is written twice per theme, by construction — and
    nothing stops the two from drifting apart, at which case flipping the
    toggle changes colours that flipping the OS setting does not.

    The two documents use opposite conventions — one has a dark base with a
    light media query, the other the reverse — so this checks the invariant
    that holds either way rather than a fixed layout.
    """
    out = []
    for path in html_files():
        text = read(path)
        base = tokens(block_after(text, "\n  :root {"))
        themed = {
            name: tokens(block_after(text, f':root[data-theme="{name}"]'))
            for name in ("light", "dark")
        }
        if not any(themed.values()):
            continue

        media = None
        for name in ("light", "dark"):
            if f"@media (prefers-color-scheme: {name})" in text:
                media = (name, tokens(block_after(
                    text, f"@media (prefers-color-scheme: {name})")))
        if media is None:
            out.append(f"{rel(path)}: has data-theme blocks but no "
                       "prefers-color-scheme query; the OS preference is ignored")
            continue

        media_name, media_tokens = media
        # 1. media(T) and [data-theme=T] are the same theme, reached two ways.
        for key in sorted(set(media_tokens) | set(themed[media_name])):
            a, b = media_tokens.get(key), themed[media_name].get(key)
            if a != b:
                out.append(
                    f"{rel(path)}: {key} is {a!r} under "
                    f"prefers-color-scheme:{media_name} but {b!r} under "
                    f'data-theme="{media_name}" — the toggle and the OS '
                    "preference would disagree")

        # 2. The base :root carries the other theme; [data-theme=other] must
        #    restate it exactly. Only tokens the theme block names are compared,
        #    because :root also holds type and layout tokens that are not themed.
        other = "dark" if media_name == "light" else "light"
        for key, want in sorted(themed[other].items()):
            got = base.get(key)
            if got != want:
                out.append(
                    f"{rel(path)}: {key} is {got!r} in the base :root but "
                    f'{want!r} under data-theme="{other}" — these are the same '
                    "theme and must match")
    return out


def main() -> int:
    if not DOCS.is_dir():
        print("docs artifact test: FAILED")
        print("  docs/ is missing; this check cannot run, which is a failure "
              "rather than a pass.")
        return 1

    files = html_files()
    if not files:
        print("docs artifact test: FAILED")
        print("  no HTML under docs/. If the documents were removed on purpose, "
              "remove this harness in the same change rather than leaving a "
              "check that passes because it found nothing to check.")
        return 1

    failures = check_parses() + check_shared_widget() + check_theme_parity()

    if failures:
        print("docs artifact test: FAILED")
        for line in failures:
            print(f"  {line}")
        return 1

    print(f"docs artifact test: {len(files)} documents parse whole, "
          "one shared widget, themes agree by both routes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
