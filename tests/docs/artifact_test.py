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

WHAT THIS DELIBERATELY DOES NOT DO, so "checked" is not overclaimed:

  - It is not an HTML validator. `Balance` checks that tags nest and close.
    HTML5 permits `<li>`, `<p>` and `<td>` to omit their closing tags; this
    would report those as unclosed. Both current documents close everything
    explicitly. A future document that does not is a reason to teach this
    check the optional-end-tag rules, not a reason to loosen it into silence.
  - CSS is read with a brace counter that understands strings and comments and
    nothing else. It is not a CSS parser. Where it cannot locate a block it
    says so as its own failure rather than reporting the empty result as a
    hundred colour mismatches.
  - It compares values, and separately checks that every colour in the base
    :root has a variant in each override. It does not check that any of those
    values are *good* - a theme where every colour is correct-by-this-file and
    unreadable on its ground passes here. Look at the page.

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


class ArtifactDocument(HTMLParser):
    """Tag balance and scaffolding, both read from the parse rather than the text.

    The scaffolding was checked by substring match in the first version, which
    would have failed a document using `<!doctype html>` or
    `<meta charset='utf-8'>` — both perfectly valid. A check that rejects
    correct input is not as bad as one that accepts wrong input, but it is
    still a check that is wrong, and this file has no standing to ship one.
    """

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.stack: list[tuple[str, int]] = []
        self.errors: list[str] = []
        self.doctype = False
        self.charset = False
        self.body = False
        self.html = False

    def handle_decl(self, decl: str) -> None:
        if decl.strip().lower().startswith("doctype html"):
            self.doctype = True

    def handle_starttag(self, tag: str, attrs) -> None:
        a = {k.lower(): (v or "") for k, v in attrs}
        if tag == "meta" and a.get("charset", "").strip().lower() == "utf-8":
            self.charset = True
        if tag == "body":
            self.body = True
        if tag == "html":
            self.html = True
        if tag not in VOID:
            self.stack.append((tag, self.getpos()[0]))

    def handle_startendtag(self, tag: str, attrs) -> None:
        self.handle_starttag(tag, attrs)
        if self.stack and self.stack[-1][0] == tag:
            self.stack.pop()

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

    def scaffolding(self) -> list[str]:
        missing = []
        if not self.doctype:
            missing.append("a <!DOCTYPE html> declaration")
        if not self.charset:
            missing.append('a <meta charset="utf-8">')
        if not self.html:
            missing.append("an <html> element")
        if not self.body:
            missing.append("a <body> element")
        return missing


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
        doc = ArtifactDocument()
        doc.feed(read(path))
        for missing in doc.scaffolding():
            out.append(f"{rel(path)}: missing {missing} — a fragment, not a "
                       "document. It will parse in quirks mode.")
        for err in doc.errors:
            out.append(f"{rel(path)}: {err}")
        for tag, line in doc.stack:
            out.append(f"{rel(path)}: <{tag}> opened on line {line}, never closed")
    return out


# Any script tag, however it is spelled. The first version of this matched a
# bare `<script>` only, and the failure mode was the worst available: a second
# document written as `<script type="module">` was silently excluded from the
# comparison, so the check reported "one shared widget" across two documents
# whose widgets differed. Verified as a real false pass before this was
# changed, not reasoned about. A check that goes quiet exactly when someone
# deviates is the defect this file exists to catch, and it was in this file.
#
# Non-greedy to the first `</script>`, which was raised in review as the same
# fragility the CSS scanner has - a `</script>` inside a JS string would end
# the match early. Checked rather than assumed, and the premise does not hold:
# an unescaped `</script>` inside a string ends the *element* too. HTML has no
# escaping inside raw text, which is why the idiom is to write `<\/script>`.
#
#     >>> feed('<script>var s = "</script>"; alert(1)</script>')
#     script body: 'var s = "'
#
# So this agrees with the parser rather than approximating it. The genuine edge
# is the double-escaped state a `<!--` opens, which nothing here uses.
SCRIPT_RE = re.compile(r"<script\b([^>]*)>(.*?)</script>", re.S | re.I)


def check_shared_widget() -> list[str]:
    """Every inline script under docs/ is the same script.

    Today that is the tab widget, in two files. The rule is stated as "all of
    them agree" rather than "these two agree" so that a third document cannot
    quietly introduce a third variant — which is the precise way the previous
    two copies diverged.

    If a document ever legitimately needs a *different* script, this check is
    the thing that must be reopened and argued with, on purpose.
    """
    out: list[str] = []
    scripts: dict[str, list[str]] = {}

    for path in html_files():
        for attrs, body in SCRIPT_RE.findall(read(path)):
            if "src=" in attrs.lower():
                # An external script has no body to compare. It also cannot be
                # checked by this harness at all, so it is named rather than
                # skipped: silence here is the thing being guarded against.
                out.append(f"{rel(path)}: loads an external script "
                           f"(<script{attrs}>). This harness cannot compare it, "
                           "and a standalone document should not need one.")
                continue
            if body.strip():
                where = rel(path) + (f" (<script{attrs}>)" if attrs.strip() else "")
                scripts.setdefault(body, []).append(where)

    if len(scripts) > 1:
        out.append("inline scripts under docs/ have diverged; they are meant "
                   "to be one widget, pasted rather than shared:")
        for body, wheres in scripts.items():
            first = next((ln.strip() for ln in body.splitlines() if ln.strip()), "")
            out.append(f"    {len(body)} chars in {', '.join(wheres)}"
                       f"  — starts {first[:60]!r}")
        out.append("    Extract it, or make them identical again. A comment "
                   "asking for this is what failed last time.")
    return out


DECL_NAME_RE = re.compile(r"^\s*(--[\w-]+)\s*:\s*(.*)$", re.S)


def declarations(css: str) -> list[str]:
    """Split a declaration block on the semicolons that actually separate it.

    `([^;]+);` was the first version and it truncates `content: ";"` at the
    quote's semicolon. `body_at` already had to learn strings and comments to
    count braces safely; splitting declarations needs the same knowledge and
    was written without it, which is how one function in a file ends up
    stricter than another about the same input.
    """
    parts, buf, quote, i, n = [], [], None, 0, len(css)
    while i < n:
        c = css[i]
        if quote:
            buf.append(c)
            if c == "\\" and i + 1 < n:
                buf.append(css[i + 1])
                i += 2
                continue
            if c == quote:
                quote = None
        elif c in "\"'":
            quote = c
            buf.append(c)
        elif c == "/" and css.startswith("/*", i):
            end = css.find("*/", i + 2)
            i = n if end < 0 else end + 2
            continue
        elif c in ";{}":
            # Braces separate as well as semicolons. The media blocks here wrap
            # a nested `:root { ... }`, so splitting on `;` alone glued the
            # selector onto the first declaration and lost it - which the
            # harness caught the moment it ran, reporting the first token of
            # every media block as missing. Left as a comment because the
            # regex this replaced did not have the bug, and a fix that
            # introduces one is worth marking.
            parts.append("".join(buf))
            buf = []
        else:
            buf.append(c)
        i += 1
    parts.append("".join(buf))
    return parts
MEDIA_RE = re.compile(r"@media\s*\(\s*prefers-color-scheme\s*:\s*(\w+)\s*\)", re.I)
BASE_ROOT_RE = re.compile(r":root\s*\{")
THEME_RE = r':root\s*\[\s*data-theme\s*=\s*["\']{name}["\']\s*\]\s*\{{'


class BlockNotFound(Exception):
    """Distinct from an empty block, so the error names the real problem."""


def body_at(text: str, brace_index: int) -> str:
    """Brace-balanced body starting at an opening brace.

    Aware of strings and `/* */` comments, because a declaration like
    `content: "{"` would otherwise desync the counter and silently truncate
    the block — producing a short token map and a page of invented mismatches.
    Not a CSS parser; this is the smallest thing that is not wrong here.
    """
    depth, i, n = 0, brace_index, len(text)
    quote = None
    while i < n:
        c = text[i]
        if quote:
            if c == "\\":
                i += 2
                continue
            if c == quote:
                quote = None
        elif c in "\"'":
            quote = c
        elif c == "/" and text.startswith("/*", i):
            end = text.find("*/", i + 2)
            i = n if end < 0 else end + 2
            continue
        elif c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return text[brace_index + 1:i]
        i += 1
    raise BlockNotFound("unbalanced braces from this selector to end of file")


def media_spans(text: str) -> list[tuple[int, int]]:
    """Where the prefers-color-scheme blocks are, so the base :root search can
    step over the one nested inside them.

    A malformed block raises rather than being skipped. The first version
    swallowed it — and the consequence was specific: an unreadable @media block
    is not excluded from the search, so the `:root` inside it can be picked up
    as the base and every comparison after that is against the wrong palette.
    A file that says elsewhere "this is a failure of this check, not a colour
    mismatch" does not get to have a silent `except: pass` in it.
    """
    spans = []
    for m in MEDIA_RE.finditer(text):
        open_i = text.index("{", m.end())
        spans.append((open_i, open_i + len(body_at(text, open_i))))
    return spans


# A value that names a colour. Used to tell a token that *should* have a theme
# variant from one that legitimately does not.
COLOUR_RE = re.compile(r"^(#[0-9a-fA-F]{3,8}|rgba?\(|hsla?\(|color-mix\()")

# Colour tokens that are deliberately the same in every theme. Empty today.
# Pinned as an explicit list rather than inferred, on the same reasoning as
# KEVIN_TOOLS in tests/workflow/kevin_scope_test.py: an exemption should be a
# visible, deliberate edit that a reader can question, not a gap that a
# heuristic quietly opens. Adding to this is a claim that the colour reads
# correctly on both grounds, which is a thing to check by looking.
THEME_INVARIANT: set[str] = set()


def check_every_colour_themes() -> list[str]:
    """A colour declared in the base :root must appear in every override block.

    This is the check that was missing, and its absence was not an oversight in
    the ordinary sense - it was a false negative *by construction*.
    check_theme_parity compares the tokens the override blocks happen to name,
    so a variable declared once in the base and omitted from all three
    overrides was invisible to it. The harness would report "themes agree by
    both routes" for a document where an entire colour never themed at all.

    It shipped that way, and `--ultraviolet` in the calibration brief was
    exactly it: eight of nine spectrum bands lifted for dark, one stayed put,
    and the check written to catch theme drift said everything agreed.

    Fonts, measures and radii are not colours and are not expected to theme,
    which is what makes the rule statable without a hand-maintained list of
    everything in the file.
    """
    out = []
    for path in html_files():
        text = read(path)
        if not has_theming(text):
            continue

        # Reported here rather than deferred. The previous version said
        # `except BlockNotFound: continue  # check_theme_parity reports this`,
        # which was true only when a data-theme block also existed -
        # check_theme_parity short-circuits before reading the base when there
        # is none. So a document with a prefers-color-scheme query, no
        # data-theme block, and an unreadable base :root passed BOTH checks and
        # printed "every colour themes, both routes agree". Reproduced as a
        # real file before this was changed, not reasoned about.
        #
        # Two functions each deferring to the other, through a comment
        # promising the other would catch it. That is the third time in this
        # file that a comment has been asked to do a check's job, and it is
        # what the file is about.
        try:
            base = tokens(block(text, BASE_ROOT_RE, outside_media=True))
        except BlockNotFound as exc:
            out.append(f"{rel(path)}: this document themes, but its base :root "
                       f"could not be read ({exc}). This is a failure of this "
                       "check, not a colour mismatch.")
            continue

        overrides: dict[str, dict[str, str]] = {}
        media = MEDIA_RE.search(text)
        if media:
            try:
                overrides[f"prefers-color-scheme:{media.group(1).lower()}"] = (
                    tokens(block(text, MEDIA_RE_BRACE)))
            except BlockNotFound as exc:
                out.append(f"{rel(path)}: could not read the "
                           f"prefers-color-scheme block ({exc}).")
        for name in ("light", "dark"):
            try:
                overrides[f'data-theme="{name}"'] = tokens(
                    block(text, re.compile(THEME_RE.format(name=name))))
            except BlockNotFound:
                pass

        if not overrides:
            continue

        for key, value in sorted(base.items()):
            if not COLOUR_RE.match(value) or key in THEME_INVARIANT:
                continue
            absent = [where for where, toks in overrides.items() if key not in toks]
            if len(absent) == len(overrides):
                out.append(
                    f"{rel(path)}: {key} is a colour ({value}) declared only in "
                    "the base :root — it never themes, while its neighbours do. "
                    "Give it a variant in each override, or add it to "
                    "THEME_INVARIANT here and say why.")
            elif absent:
                out.append(
                    f"{rel(path)}: {key} themes in some blocks but is missing "
                    f"from {', '.join(absent)} — it will fall back to the base "
                    f"value ({value}) there while its neighbours change.")
    return out


def block(text: str, pattern: re.Pattern[str], *, outside_media: bool = False) -> str:
    """The body of the first block matching `pattern`. Raises if absent.

    Selector matching is by regex rather than by literal indented text. The
    first version searched for the string "\\n  :root {", so a reformat to four
    spaces would have made the base block un-findable, the token map empty, and
    every comparison a mismatch — sending the reader hunting a colour bug that
    did not exist. Failing loudly is right; failing loudly about the wrong
    thing is not.
    """
    spans = media_spans(text) if outside_media else []
    for m in pattern.finditer(text):
        i = m.end() - 1  # the opening brace
        if any(lo < i < hi for lo, hi in spans):
            continue
        return body_at(text, i)
    raise BlockNotFound(f"no block matching {pattern.pattern!r}")


def tokens(css: str) -> dict[str, str]:
    out = {}
    for decl in declarations(css):
        m = DECL_NAME_RE.match(decl)
        if m:
            out[m.group(1)] = m.group(2).strip()
    return out


def has_theming(text: str) -> bool:
    """Whether this document claims to theme at all.

    A page with no custom properties and no colour-scheme handling has no base
    :root to find, and demanding one would fail documents that are simply not
    themed. A page that has either apparatus must have a readable base.
    """
    return bool(MEDIA_RE.search(text)) or any(
        re.search(THEME_RE.format(name=n), text) for n in ("light", "dark"))


def check_theme_parity() -> list[str]:
    """The two ways of reaching a theme must agree.

    A viewer's OS preference arrives as `prefers-color-scheme`; their explicit
    toggle arrives as `data-theme` on the root and has to beat the media query.
    That means the palette is written twice per theme, by construction — and
    nothing stops the two from drifting apart, at which point flipping the
    toggle changes colours that flipping the OS setting does not.

    The two documents use opposite conventions — one has a dark base with a
    light media query, the other the reverse — so this checks the invariant
    that holds either way rather than a fixed layout. That they already differ
    in that way is why it is written like this.
    """
    out = []
    for path in html_files():
        text = read(path)
        themed = {}
        for name in ("light", "dark"):
            pattern = re.compile(THEME_RE.format(name=name))
            try:
                themed[name] = tokens(block(text, pattern))
            except BlockNotFound:
                themed[name] = None

        if not any(v for v in themed.values()):
            continue  # a document with no theme toggle has nothing to disagree

        media = MEDIA_RE.search(text)
        if media is None:
            out.append(f"{rel(path)}: has data-theme blocks but no "
                       "prefers-color-scheme query; the OS preference is ignored")
            continue
        media_name = media.group(1).lower()
        other = "dark" if media_name == "light" else "light"

        try:
            media_tokens = tokens(block(text, MEDIA_RE_BRACE))
        except BlockNotFound as exc:
            out.append(f"{rel(path)}: could not read the "
                       f"prefers-color-scheme:{media_name} block ({exc}). "
                       "This is a failure of this check, not a colour mismatch.")
            continue

        for name in (media_name, other):
            if themed.get(name) is None:
                out.append(f"{rel(path)}: could not read the "
                           f'data-theme="{name}" block. This is a failure of '
                           "this check, not a colour mismatch.")
        if themed.get(media_name) is None or themed.get(other) is None:
            continue

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
        try:
            base = tokens(block(text, BASE_ROOT_RE, outside_media=True))
        except BlockNotFound as exc:
            out.append(f"{rel(path)}: could not read the base :root block "
                       f"({exc}). This is a failure of this check, not a "
                       "colour mismatch.")
            continue
        for key, want in sorted(themed[other].items()):
            got = base.get(key)
            if got != want:
                out.append(
                    f"{rel(path)}: {key} is {got!r} in the base :root but "
                    f'{want!r} under data-theme="{other}" — these are the same '
                    "theme and must match")
    return out


# The media query and its opening brace, so `block` can find the body.
MEDIA_RE_BRACE = re.compile(
    r"@media\s*\(\s*prefers-color-scheme\s*:\s*\w+\s*\)\s*\{", re.I)


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

    failures = (check_parses() + check_shared_widget()
                + check_theme_parity() + check_every_colour_themes())

    if failures:
        print("docs artifact test: FAILED")
        for line in failures:
            print(f"  {line}")
        return 1

    print(f"docs artifact test: {len(files)} documents parse whole, "
          "one shared widget, every colour themes, both routes agree")
    return 0


if __name__ == "__main__":
    sys.exit(main())
