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

# The parents[2] above is a depth assumption, and a wrong one would not raise -
# it would point DOCS somewhere with no HTML in it, and main()'s empty-set
# branch would report "no HTML under docs/" as though the documents had been
# deleted. Anchored so a moved file says what actually happened.
#
# The first version of this guard was `if not .git and not tests/docs`, which
# only fires when BOTH signals are wrong - so a nested repository, a submodule,
# or a moved file with a .git at some other ancestor sails straight through. A
# guard added to fix a fragility, carrying the same fragility. Review caught it.
#
# This asserts the one thing that is load-bearing: that parents[2] lands where
# this file says it does. It cannot be satisfied by coincidence.
def check_layout() -> list[str]:
    """parents[2] must land where this file says this file is.

    Derived from __file__ rather than from REPO, which harness_test.py
    reassigns to a scratch directory - so this asks about the source tree
    either way.

    Called from main() rather than run at import. A bare `raise SystemExit` at
    module level executes as a side effect of `import`, which works today only
    because the one importer does so from the real path; coverage, a linter or
    a doc tool would trip it.
    """
    # The literal "tests/docs" below is coupled to where this file lives. If
    # the directory is renamed, this fails with a message about parents[2]
    # rather than about the rename - correct verdict, imprecise reason. Stated
    # rather than solved: the alternative is a marker file, which an earlier
    # round rejected because a nested repository satisfies it by accident.
    here = Path(__file__).resolve()
    if here != here.parents[2] / "tests" / "docs" / "artifact_test.py":
        return [f"parents[2] resolves to {here.parents[2]}, which would put "
                f"this file at {here.parents[2] / 'tests/docs/artifact_test.py'} "
                f"- it is actually at {here}. The file moved; fix the depth "
                "rather than letting the checks run against the wrong tree."]
    return []


# Elements with no closing tag. A hand-written list rather than a dependency;
# if one is missing the parser reports a false unclosed tag, which fails loudly
# rather than passing quietly.
VOID = {
    "area", "base", "br", "col", "embed", "hr", "img", "input",
    "link", "meta", "param", "source", "track", "wbr",
}

# Subtrees parsed as foreign content, where XML rules apply and `<circle/>`
# genuinely self-closes. Outside these, a trailing slash is ignored by the
# parser and the element stays open.
FOREIGN = {"svg", "math"}


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
        self.scripts: list[tuple[dict, str]] = []
        self._script: list | None = None
        self.doctype = False
        self.charset = False
        self.body = False
        self.html = False

    def handle_decl(self, decl: str) -> None:
        if decl.strip().lower().startswith("doctype html"):
            self.doctype = True

    def handle_starttag(self, tag: str, attrs) -> None:
        a = {k.lower(): (v or "") for k, v in attrs}
        # Both spellings. <meta charset> is the HTML5 form and what both
        # current documents use; the http-equiv form is still valid and a
        # document using it is correct, so rejecting it would be this file
        # failing a correct input - which it has already done once, over
        # <!doctype html>.
        if tag == "meta":
            if a.get("charset", "").strip().lower() == "utf-8":
                self.charset = True
            elif (a.get("http-equiv", "").strip().lower() == "content-type"
                  and "utf-8" in a.get("content", "").lower()):
                self.charset = True
        if tag == "script":
            self._script = [a, ""]
        if tag == "body":
            self.body = True
        if tag == "html":
            self.html = True
        if tag not in VOID:
            self.stack.append((tag, self.getpos()[0]))

    def handle_startendtag(self, tag: str, attrs) -> None:
        """`<x/>` self-closes only where the parser is in foreign content.

        In HTML proper the slash is ignored and a closing tag is still
        required, so the previous version - which popped the stack for any
        self-closed tag - let a genuinely unclosed `<div/>` parse clean here
        and wrong in a browser.

        Inside an <svg> or <math> subtree the rules are XML's and `<circle/>`
        really does close. The first fix for the <div/> case did not make that
        distinction and reported thirty unclosed tags in the calibration
        brief's inline SVG - correct about HTML, wrong about the document.
        Caught by the real documents, again.
        """
        self.handle_starttag(tag, attrs)
        # `self.stack`, not `self.stack[:-1]`. The tag just pushed counts:
        # a bare `<svg/>` with no children is itself foreign content and does
        # self-close, and excluding it reported that as an unbalanced <svg>.
        foreign = any(t in FOREIGN for t, _ in self.stack)
        if foreign and self.stack and self.stack[-1][0] == tag:
            self.stack.pop()

    def handle_data(self, data: str) -> None:
        if self._script is not None:
            self._script[1] += data

    def handle_endtag(self, tag: str) -> None:
        if tag == "script" and self._script is not None:
            self.scripts.append((self._script[0], self._script[1]))
            self._script = None
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


def html_files(docs: Path) -> list[Path]:
    return sorted(docs.rglob("*.html"))


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def rel(path: Path, repo: Path) -> str:
    return str(path.relative_to(repo))


def check_parses(docs: Path, repo: Path) -> list[str]:
    """Every document is a whole document, and its tags balance.

    The scaffolding half exists because both of these shipped as *fragments*
    first: authored as embedded artifacts, where the host supplies the doctype
    and head. Opened from disk that is quirks mode with the encoding
    unspecified. Correct where they were rendered, wrong in a repository.
    """
    out = []
    for path in html_files(docs):
        doc = ArtifactDocument()
        doc.feed(read(path))
        for missing in doc.scaffolding():
            out.append(f"{rel(path, repo)}: missing {missing} — a fragment, not a "
                       "document. It will parse in quirks mode.")
        for err in doc.errors:
            out.append(f"{rel(path, repo)}: {err}")
        for tag, line in doc.stack:
            out.append(f"{rel(path, repo)}: <{tag}> opened on line {line}, never closed")
    return out


# SCRIPT_RE and TYPE_RE used to live here: a hand-rolled `<script>` matcher
# and an attribute reader beside it. Nearly every false pass this file has
# shipped came from that one decision to re-parse text the ArtifactDocument
# walk was already reading -
#
#     a bare `<script>` pattern skipped `<script type="module">` entirely
#     `[^>]*` ended the tag at a `>` inside an attribute value
#     `\btype` matched inside `data-type` and won over the real attribute
#
# - three separate patches to three symptoms of the same cause. html.parser
# puts <script> in CDATA_CONTENT_ELEMENTS, so it handles the raw-text body, any
# attribute spelling, and quoted `>` for free, and it agrees with a browser on
# where the element ends. Verified against all five shapes before switching,
# including the double-escaped state a `<!--` opens.
#
# Scripts now come off the same parse as the tag balance. There is one reader.


def scripts_in(path: Path) -> list[tuple[dict, str]]:
    """Every <script> in a document, off the same parse as the tag balance."""
    doc = ArtifactDocument()
    doc.feed(read(path))
    return doc.scripts


def script_problem(attrs: dict, body: str) -> str | None:
    """Why this script cannot be compared, or None if it can.

    Returns the complaint rather than a bool because check_shared_widget must
    say why it is skipping - silence there is the thing being guarded against -
    while main()'s count only needs the verdict. One definition, two readings.

    The first version of this was a bool that only main() called, while
    check_shared_widget kept its three conditions inline: a helper written to
    stop two filters drifting, used by one of them. The drift it warns about,
    in its own introduction.
    """
    if "src" in attrs:
        # Stated as a limit of this harness, NOT as a verdict on the
        # architecture. An earlier wording said "a standalone document should
        # not need one", which quietly encodes "keep it pasted, but check the
        # paste" - and extracting the widget to one real file is the actual fix
        # for the drift this check exists to detect. Refusing what this cannot
        # read is right; declaring it wrong is not this file's call. See #43,
        # which holds the toolchain decision for these documents.
        return ("loads an external script, which this harness has no way to "
                "compare. If the widget is being extracted to a shared file, "
                "teach this check to follow it - see #43 - rather than working "
                "around this message.")
    # The `<!--` refusal that used to sit here was justified by the regex not
    # being able to follow the double-escaped state. The parser can, and a rule
    # outliving its reason is a rule nobody can argue with. Removed rather than
    # kept for safety: refusing input this harness now reads correctly is the
    # false-fail side of the same coin.
    return None


def comparable_script(attrs: dict, body: str) -> bool:
    return script_problem(attrs, body) is None and bool(body.strip())


def check_shared_widget(docs: Path, repo: Path) -> list[str]:
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

    for path in html_files(docs):
        for attrs, body in scripts_in(path):
            problem = script_problem(attrs, body)
            if problem is not None:
                out.append(f"{rel(path, repo)}: an inline script {problem}")
                continue
            if body.strip():
                # Keyed on (type, body), not body alone. A module script runs
                # in strict mode, is deferred, and does not leak to global
                # scope - identical text under `<script>` and
                # `<script type="module">` is not the same widget. Grouping on
                # body alone would have traded the false pass this check just
                # fixed for its mirror image.
                kind = attrs.get("type", "classic").strip().lower() or "classic"
                shown = " ".join(f'{k}="{v}"' for k, v in sorted(attrs.items()))
                where = rel(path, repo) + (f" (<script {shown}>)" if shown else "")
                scripts.setdefault((kind, body), []).append(where)

    if len(scripts) > 1:
        out.append("inline scripts under docs/ have diverged; they are meant "
                   "to be one widget, pasted rather than shared:")
        for (kind, body), wheres in scripts.items():
            first = next((ln.strip() for ln in body.splitlines() if ln.strip()), "")
            out.append(f"    {len(body)} chars, type={kind}, in "
                       f"{', '.join(wheres)}  — starts {first[:60]!r}")
        out.append("    Extract it, or make them identical again. A comment "
                   "asking for this is what failed last time.")
    return out


DECL_NAME_RE = re.compile(r"^\s*(--[\w-]+)\s*:\s*(.*)$", re.S)


def scan_css(css: str):
    """Yield (index, char, quoted) for every character outside a comment.

    ONE definition of "inside a string" and "inside a comment", used by both
    callers. The previous shape had scan_css skipping comments while
    `declarations` sliced raw text and then ran COMMENT_RE over the pieces - a
    second, weaker comment path layered on the first, added to patch a bug the
    extraction had itself introduced. Two answers to one question is how this
    file's worst defects started; a scanner is not the place to keep a spare.
    """
    quote, i, n = None, 0, len(css)
    while i < n:
        c = css[i]
        if quote:
            yield i, c, True
            if c == "\\" and i + 1 < n:
                yield i + 1, css[i + 1], True
                i += 2
                continue
            if c == quote:
                quote = None
        elif c in "\"'":
            quote = c
            yield i, c, True
        elif c == "/" and css.startswith("/*", i):
            end = css.find("*/", i + 2)
            i = n if end < 0 else end + 2
            continue
        else:
            yield i, c, False
        i += 1


def declarations(css: str) -> list[str]:
    """Split a declaration block on the separators that actually separate it.

    `([^;]+);` was the first version and it truncates `content: ";"` at the
    quote's semicolon. Braces separate as well as semicolons: the media blocks
    here wrap a nested `:root { ... }`, and splitting on `;` alone glued the
    selector onto the first declaration and lost it.
    """
    parts, buf = [], []
    for _, c, quoted in scan_css(css):
        if c in ";{}" and not quoted:
            parts.append("".join(buf))
            buf = []
        else:
            buf.append(c)
    parts.append("".join(buf))
    return parts


# Compound queries, either ordering. The first version required
# `@media (prefers-color-scheme: X)` in isolation, so
# `@media (prefers-color-scheme: dark) and (min-width: 600px)` was detected but
# unreadable - a false FAIL on valid CSS - and the same query with the terms
# reversed reported "no prefers-color-scheme query" while looking straight at
# one. Neither was the silent skip it was reported as, and both were wrong.
MEDIA_RE = re.compile(
    r"@media[^{]*?prefers-color-scheme\s*:\s*(\w+)[^{]*", re.I)
BASE_ROOT_RE = re.compile(r":root\s*\{")
THEME_RE = r':root\s*\[\s*data-theme\s*=\s*["\']{name}["\']\s*\]\s*\{{'


class BlockNotFound(Exception):
    """Distinct from an empty block, so the error names the real problem."""


def body_at(text: str, brace_index: int) -> str:
    """Brace-balanced body starting at an opening brace.

    Strings and comments come from the shared scanner, because a declaration
    like `content: "{"` would otherwise desync the counter and silently
    truncate the block - producing a short token map and a page of invented
    mismatches. Not a CSS parser; this is the smallest thing that is not wrong.
    """
    depth = 0
    for i, c, quoted in scan_css(text[brace_index:]):
        if quoted or c not in "{}":
            continue
        depth += 1 if c == "{" else -1
        if depth == 0:
            return text[brace_index + 1:brace_index + i]
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
        # `.index` raised a bare ValueError when a media query had no opening
        # brace after it. That escaped _read(), which only catches
        # BlockNotFound, and killed main() with a raw traceback - in the file
        # whose stated purpose is to fail with a path and a reason instead of
        # "failing loudly about the wrong thing". Same class as the bug it
        # describes, in the function that describes it.
        open_i = text.find("{", m.end())
        if open_i < 0:
            raise BlockNotFound(
                f"@media (prefers-color-scheme: {m.group(1)}) has no opening "
                "brace after it")
        spans.append((open_i, open_i + len(body_at(text, open_i))))
    return spans


class ThemeBlocks:
    """Every theme block in one document, read once.

    check_theme_parity and check_every_colour_themes each
    re-derived the base :root, the media block and the two data-theme blocks,
    with their own try/except wording around each. The mutual-deferral bug came
    from exactly that shape - one function's error handling
    silently depending on the other's, under a combination neither covered.
    Fixing the one combination while leaving the duplication in place invites
    the next one, so the reading happens once and both checks consume it.
    """

    def __init__(self, path: Path, repo: Path) -> None:
        self.path = path
        self.repo = repo
        self.text = read(path)
        self.errors: list[str] = []
        self.themes = has_theming(self.text)

        self.base = self._read(BASE_ROOT_RE, "the base :root", outside_media=True)
        m = MEDIA_RE.search(self.text)
        self.media_name = m.group(1).lower() if m else None
        self.media = (self._read(MEDIA_RE_BRACE,
                                 f"the prefers-color-scheme:{self.media_name} block")
                      if m else None)
        self.themed = {
            name: self._read(re.compile(THEME_RE.format(name=name)),
                             f'the data-theme="{name}" block', quiet=True)
            for name in ("light", "dark")
        }
        self.errors += self.presence_errors()

    def _read(self, pattern, what: str, *, outside_media: bool = False,
              quiet: bool = False) -> dict[str, str] | None:
        try:
            return tokens(block(self.text, pattern, outside_media=outside_media))
        except BlockNotFound as exc:
            # `quiet` covers the blocks a document may legitimately not have.
            # Everything else is reported as a failure OF THIS CHECK, in those
            # words, because an unreadable block used to surface as a page of
            # invented colour mismatches.
            if not quiet and self.themes:
                self.errors.append(
                    f"{rel(self.path, self.repo)}: this document themes, but {what} could "
                    f"not be read ({exc}). This is a failure of this check, "
                    "not a colour mismatch.")
            return None

    def presence_errors(self) -> list[str]:
        """Structure that is present in the text but unreadable must be LOUD.

        The strict selector patterns are how blocks get read, and anything they
        do not match falls out of detection entirely - which is a silent skip,
        the failure this file exists to remove. Two shapes were found that way:
        `:root[data-theme="light"], .foo { }` and `html[data-theme="light"]`
        both parsed as "this document does not theme" and exited 0.

        Rather than widening the patterns until they cover every selector
        anyone might write - which is how the script regex accumulated three
        defects - this asks a cruder question: does the substring appear? If it
        does and nothing was read, say so. A checker that cannot read a
        construct should refuse it, not ignore it.
        """
        out = []
        if ("prefers-color-scheme" in self.text.lower()
                and self.media is None):
            out.append(
                f"{rel(self.path, self.repo)}: the text contains "
                "`prefers-color-scheme` but no block this check can read. It "
                "is themed in a shape this harness does not understand, which "
                "is refused rather than skipped.")
        for name in ("light", "dark"):
            if (re.search(rf'data-theme\s*=\s*["\']?{name}', self.text, re.I)
                    and self.themed.get(name) is None):
                out.append(
                    f"{rel(self.path, self.repo)}: the text contains "
                    f'`data-theme={name}` but no `:root[data-theme="{name}"]` '
                    "block this check can read - a combined selector or a "
                    "different element scope. Refused rather than skipped.")
        return out

    def overrides(self) -> dict[str, dict[str, str]]:
        """The readable override blocks, labelled as a reader would name them."""
        out = {}
        if self.media is not None:
            out[f"prefers-color-scheme:{self.media_name}"] = self.media
        for name, toks in self.themed.items():
            if toks is not None:
                out[f'data-theme="{name}"'] = toks
        return out


# A value that names a colour. Used to tell a token that *should* have a theme
# variant from one that legitimately does not.
#
# The named-colour set is complete - all 148 CSS keywords plus `transparent`
# and `currentColor`. A partial list was the first version and it was the worst
# of the three options: `red` and `transparent` were recognised while
# `rebeccapurple` was not, so the check LOOKED exhaustive and silently skipped
# the tokens nobody thought to add. That is the same shape as `--ultraviolet`,
# which is the defect this check was written for. Either enumerate them or
# narrow to hex and functions and say so; a partial set claims the first while
# delivering the second.
CSS_NAMED_COLOURS = frozenset("""
aliceblue antiquewhite aqua aquamarine azure beige bisque black blanchedalmond
blue blueviolet brown burlywood cadetblue chartreuse chocolate coral
cornflowerblue cornsilk crimson cyan darkblue darkcyan darkgoldenrod darkgray
darkgreen darkgrey darkkhaki darkmagenta darkolivegreen darkorange darkorchid
darkred darksalmon darkseagreen darkslateblue darkslategray darkslategrey
darkturquoise darkviolet deeppink deepskyblue dimgray dimgrey dodgerblue
firebrick floralwhite forestgreen fuchsia gainsboro ghostwhite gold goldenrod
gray green greenyellow grey honeydew hotpink indianred indigo ivory khaki
lavender lavenderblush lawngreen lemonchiffon lightblue lightcoral lightcyan
lightgoldenrodyellow lightgray lightgreen lightgrey lightpink lightsalmon
lightseagreen lightskyblue lightslategray lightslategrey lightsteelblue
lightyellow lime limegreen linen magenta maroon mediumaquamarine mediumblue
mediumorchid mediumpurple mediumseagreen mediumslateblue mediumspringgreen
mediumturquoise mediumvioletred midnightblue mintcream mistyrose moccasin
navajowhite navy oldlace olive olivedrab orange orangered orchid palegoldenrod
palegreen paleturquoise palevioletred papayawhip peachpuff peru pink plum
powderblue purple rebeccapurple red rosybrown royalblue saddlebrown salmon
sandybrown seagreen seashell sienna silver skyblue slateblue slategray
slategrey snow springgreen steelblue tan teal thistle tomato turquoise violet
wheat white whitesmoke yellow yellowgreen
""".split())

COLOUR_FUNC_RE = re.compile(
    r"^(#[0-9a-fA-F]{3,8}|(?:rgba?|hsla?|hwb|lab|lch|oklab|oklch|color|"
    r"color-mix|light-dark)\s*\()")


def is_colour(value: str) -> bool:
    v = value.strip().lower()
    if COLOUR_FUNC_RE.match(v):
        return True
    if v.startswith("var("):
        # Indirection through another custom property. The target is themed or
        # it is not, and this check will reach it under its own name.
        return True
    return v in CSS_NAMED_COLOURS or v in {"transparent", "currentcolor"}


# Colour tokens that are deliberately the same in every theme. Empty today.
# Pinned as an explicit list rather than inferred, on the same reasoning as
# KEVIN_TOOLS in tests/workflow/kevin_scope_test.py: an exemption should be a
# visible, deliberate edit that a reader can question, not a gap that a
# heuristic quietly opens. Adding to this is a claim that the colour reads
# correctly on both grounds, which is a thing to check by looking.
THEME_INVARIANT: set[str] = set()


def check_every_colour_themes(all_blocks: list[ThemeBlocks], repo: Path,
                              theme_invariant: set[str]) -> list[str]:
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
    for blocks in all_blocks:
        path = blocks.path
        if not blocks.themes or blocks.base is None:
            continue
        overrides = blocks.overrides()
        if not overrides:
            continue

        for key, value in sorted(blocks.base.items()):
            if not is_colour(value) or key in theme_invariant:
                continue
            absent = [where for where, toks in overrides.items() if key not in toks]
            if len(absent) == len(overrides):
                out.append(
                    f"{rel(path, repo)}: {key} is a colour ({value}) declared only in "
                    "the base :root — it never themes, while its neighbours do. "
                    "Give it a variant in each override, or add it to "
                    "THEME_INVARIANT here and say why.")
            elif absent:
                out.append(
                    f"{rel(path, repo)}: {key} themes in some blocks but is missing "
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


def check_theme_parity(all_blocks: list[ThemeBlocks], repo: Path) -> list[str]:
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
    for blocks in all_blocks:
        path = blocks.path
        if not any(v for v in blocks.themed.values()):
            continue  # no theme toggle; nothing can disagree

        if blocks.media_name is None:
            out.append(f"{rel(path, repo)}: has data-theme blocks but no "
                       "prefers-color-scheme query; the OS preference is ignored")
            continue
        media_name = blocks.media_name
        other = "dark" if media_name == "light" else "light"

        if blocks.media is None or blocks.themed.get(media_name) is None \
                or blocks.themed.get(other) is None or blocks.base is None:
            continue  # unreadable; already reported as this check's own failure

        # 1. media(T) and [data-theme=T] are the same theme, reached two ways.
        for key in sorted(set(blocks.media) | set(blocks.themed[media_name])):
            a, b = blocks.media.get(key), blocks.themed[media_name].get(key)
            if a != b:
                out.append(
                    f"{rel(path, repo)}: {key} is {a!r} under "
                    f"prefers-color-scheme:{media_name} but {b!r} under "
                    f'data-theme="{media_name}" — the toggle and the OS '
                    "preference would disagree")

        # 2. The base :root carries the other theme; [data-theme=other] must
        #    restate it exactly. Only tokens the theme block names are compared,
        #    because :root also holds type and layout tokens that are not themed.
        for key, want in sorted(blocks.themed[other].items()):
            got = blocks.base.get(key)
            if got != want:
                out.append(
                    f"{rel(path, repo)}: {key} is {got!r} in the base :root but "
                    f'{want!r} under data-theme="{other}" — these are the same '
                    "theme and must match")
    return out


# The media query and its opening brace, so `block` can find the body.
MEDIA_RE_BRACE = re.compile(
    r"@media[^{]*?prefers-color-scheme\s*:\s*\w+[^{]*\{", re.I)


# Deliberately NOT anchored on `run:`. That version matched a single-line
# `run: python3 <path>` only, so a `run: |` block scalar, a chained
# `a && b`, or an added flag silently dropped out of the count - and the
# failure surfaced as this check blaming big-board.html for a number that was
# actually wrong because of the regex. Checked against a realistic sample:
# anchored found 1 of 3, unanchored found 3 of 3.
#
# yaml.safe_load would be the better tool and is not available: every harness
# here is standard library only, on purpose, so there is nothing to pin and
# nothing to go stale. Comment lines are stripped first so prose mentioning a
# path cannot inflate the count.
# `(?!\S)` is load-bearing. Without it, greedy \S+ backtracks to find any
# `.py` substring, so `tests/foo.pyx` and `tests/foo.py_disabled` both captured
# as `tests/foo.py` - a regex disagreeing with reality, in the counter that
# exists to stop a document disagreeing with reality.
HARNESS_STEP_RE = re.compile(r"python3\s+(tests/\S+\.py)(?!\S)")
YAML_COMMENT_RE = re.compile(r"^\s*#.*$", re.M)
BOARD = "docs/big-board.html"


def run_blocks(yaml_text: str) -> str:
    """Just the shell of every `run:` step, joined.

    The counter used to scan the whole file with only whole-line comments
    stripped, so a step named `run tests/ghost_test.py nightly` was read as an
    uncountable invocation and failed the build over prose. Restricting the
    scan to what actually executes is the difference between "this workflow
    runs a test I cannot count" and "this workflow mentions a filename".

    Not a YAML parser - it understands `run:` inline and `run: |` block
    scalars, which is what checks.yml uses. Anything else contributes nothing,
    and the uncountable-step guard below is what makes that loud.
    """
    out, lines = [], yaml_text.splitlines()
    i = 0
    while i < len(lines):
        m = re.match(r"^(\s*)(?:-\s*)?run:\s*(.*)$", lines[i])
        if not m:
            i += 1
            continue
        indent, inline = len(m.group(1)), m.group(2).strip()
        if inline in ("|", ">", "|-", ">-", "|+", ">+"):
            i += 1
            while i < len(lines):
                if lines[i].strip() and (len(lines[i]) - len(lines[i].lstrip())) <= indent:
                    break
                out.append(lines[i])
                i += 1
        else:
            out.append(inline)
            i += 1
    return "\n".join(out)


def check_board_harness_count(repo: Path) -> list[str]:
    """The board's headline harness count must match what CI actually runs.

    The board is a static snapshot and says so, but "how many harnesses run in
    CI" is not a fact about the day it was written - it is a fact about the
    repository, checkable at any moment, and it was WRONG IN THE PULL REQUEST
    THAT ADDED IT: checks.yml ran eight, the board said six. A page whose
    subject is checks that report without checking, misreporting the number of
    checks.

    This does not make the board live. It pins the one number that can be
    derived, so the document cannot claim more coverage than exists.
    """
    board = repo / BOARD
    workflow = repo / ".github/workflows/checks.yml"
    if not board.exists() or not workflow.exists():
        return []

    body = run_blocks(YAML_COMMENT_RE.sub("", read(workflow)))
    actual = sorted(set(HARNESS_STEP_RE.findall(body)))

    # Anything under tests/ that this counter cannot attribute to a
    # `python3 <path>` invocation is named rather than dropped. A step using
    # pytest, tox, or a wrapper script would otherwise fall out of the count
    # silently and the board would be "correct" about a number that had
    # stopped describing CI - skip-and-pass, in the check that exists to stop
    # a document overclaiming its own coverage.
    mentioned = set(re.findall(r"(tests/\S+\.py)(?!\S)", body))
    uncounted = sorted(mentioned - set(actual))
    if uncounted:
        return [f"{BOARD}: checks.yml references {', '.join(uncounted)} in a "
                "form this counter cannot read - it counts `python3 <path>` "
                "invocations only. Either the step changed shape or a test is "
                "run by a wrapper; teach HARNESS_STEP_RE rather than letting "
                "the count quietly stop describing CI."]
    text = read(board)
    m = re.search(r'data-harness-count="(\d+)"', text)
    if not m:
        return [f"{BOARD}: no data-harness-count attribute. It states a number "
                "of harnesses in prose; that number needs to be machine-"
                f"checkable against checks.yml, which runs {len(actual)}."]
    claimed = int(m.group(1))
    if claimed != len(actual):
        return [f"{BOARD}: claims {claimed} harnesses; checks.yml runs "
                f"{len(actual)} ({', '.join(actual)}). The board was already "
                "wrong about this once, in the pull request that added it."]
    return []


def main(docs_root: Path | None = None, repo_root: Path | None = None,
         theme_invariant: set[str] | None = None) -> int:
    """Run every check against the given roots.

    NO GLOBAL MUTATION. An earlier version assigned DOCS, REPO and
    THEME_INVARIANT onto the module and restored them in a finally, with a
    comment claiming that removed the shared mutable state - it did not. It
    moved the race from the caller into this function, where the window
    between saving and restoring is just as open to a second concurrent call.
    Review caught the overclaim, which was mine and in a comment about
    robustness.

    The module-level DOCS and REPO are defaults for a direct run and nothing
    reads them after this line.
    """
    docs = docs_root if docs_root is not None else DOCS
    repo = repo_root if repo_root is not None else REPO
    invariant = theme_invariant if theme_invariant is not None else THEME_INVARIANT

    if not docs.is_dir():
        print("docs artifact test: FAILED")
        print("  docs/ is missing; this check cannot run, which is a failure "
              "rather than a pass.")
        return 1

    files = html_files(docs)
    if not files:
        print("docs artifact test: FAILED")
        print("  no HTML under docs/. If the documents were removed on purpose, "
              "remove this harness in the same change rather than leaving a "
              "check that passes because it found nothing to check.")
        return 1

    # Read once, here. Both theme checks used to build their own ThemeBlocks,
    # and the errors were emitted by whichever of them happened to run - a
    # coupling held by a comment. main() owns the read and the reporting, so
    # removing or reordering either check cannot make an unreadable block go
    # quiet.
    all_blocks = [ThemeBlocks(path, repo) for path in files]
    block_errors = [err for blocks in all_blocks for err in blocks.errors]

    failures = (check_layout()
                + check_parses(docs, repo)
                + check_shared_widget(docs, repo)
                + block_errors
                + check_theme_parity(all_blocks, repo)
                + check_every_colour_themes(all_blocks, repo, invariant)
                + check_board_harness_count(repo))

    if failures:
        print("docs artifact test: FAILED")
        for line in failures:
            print(f"  {line}")
        return 1

    # Derived, not asserted. The previous version printed "one shared widget"
    # unconditionally on success, while check_shared_widget only requires that
    # there be no MORE than one - so three documents with no scripts at all
    # would have reported a widget that does not exist. A success line is a
    # claim like any other.
    n_widgets = len({body for path in files
                     for attrs, body in scripts_in(path)
                     if comparable_script(attrs, body)})
    widget = ("no inline widget" if n_widgets == 0
              else f"{n_widgets} shared widget")
    print(f"docs artifact test: {len(files)} documents parse whole, "
          f"{widget}, every colour themes, both routes agree")
    return 0


if __name__ == "__main__":
    sys.exit(main())
