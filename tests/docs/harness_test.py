#!/usr/bin/env python3
"""The harness for the harness.

`tests/docs/artifact_test.py` was verified by hand: break a thing, run it,
watch it fail, put the change back. Six cases, done at a terminal, and the
evidence written into a pull request description.

That is exactly what that file exists to stop. It checks two documents whose
"parses clean" and "byte-identical" claims were narrated rather than enforced,
and it was itself narrated rather than enforced. Against the real documents it
can only exercise the branches those two documents happen to trigger — so an
edit to `body_at`, `THEME_RE` or `SCRIPT_RE` that reintroduces a false pass
would be caught by nothing.

It has already shipped three defects of that kind:

    a false positive   `<script>` matched bare only, so a divergent
                       `<script type="module">` was not compared at all
    a false negative   a colour declared once in the base and omitted from
                       every override was never looked at
    a mutual deferral  two checks each relying on the other to report an
                       unreadable base :root, under a case neither covered

Each was found by a reviewer, not by a test. These are those cases, committed.

    python3 tests/docs/harness_test.py

Standard library only.
"""

from __future__ import annotations

import contextlib
import io
import shutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import artifact_test as A  # noqa: E402


def doc(style: str = "", body: str = "<p>x</p>", script: str | None = None,
        head: str = '<!DOCTYPE html>\n<html lang="en"><head>'
                    '<meta charset="utf-8"><title>t</title>') -> str:
    parts = [head]
    if style:
        parts.append(f"<style>\n{style}\n</style>")
    parts.append(f"</head><body>{body}")
    if script is not None:
        parts.append(script)
    parts.append("</body></html>")
    return "\n".join(parts)


# A palette that satisfies every check: a dark base, a light media query, and
# both data-theme blocks agreeing with their counterparts.
GOOD_CSS = """
  :root {
    --ground: #0E1116;
    --ink: #E7E9ED;
    --sans: system-ui, sans-serif;
  }
  @media (prefers-color-scheme: light) {
    :root { --ground: #EFEEE9; --ink: #15181D; }
  }
  :root[data-theme="light"] { --ground: #EFEEE9; --ink: #15181D; }
  :root[data-theme="dark"] { --ground: #0E1116; --ink: #E7E9ED; }
"""

WIDGET = "<script>\n  var a = 1;\n</script>"

# (name, {filename: content}, expect_failure, substring the report must contain)
CASES: list[tuple[str, dict[str, str], bool, str]] = [

    # ---------- check_parses ----------
    ("a whole document passes",
     {"a.html": doc(GOOD_CSS)}, False, ""),

    ("an unclosed tag is caught",
     {"a.html": doc(GOOD_CSS, body="<div><p>x</p>")}, True, "never closed"),

    ("a crossed tag is caught",
     {"a.html": doc(GOOD_CSS, body="<div><span>x</div></span>")},
     True, "closes <span>"),

    ("a fragment with no doctype is caught — both documents shipped as one",
     {"a.html": doc(GOOD_CSS, head='<html lang="en"><head>'
                                   '<meta charset="utf-8"><title>t</title>')},
     True, "<!DOCTYPE html>"),

    ("a document with no charset is caught",
     {"a.html": doc(GOOD_CSS, head='<!DOCTYPE html>\n<html lang="en">'
                                   "<head><title>t</title>")},
     True, "charset"),

    ("lowercase doctype and a single-quoted, reordered charset pass",
     {"a.html": doc(GOOD_CSS, head="<!doctype html>\n<html lang='en'><head>"
                                   "<meta name='x' content='y' charset='UTF-8'>"
                                   "<title>t</title>")},
     False, ""),

    ("the older http-equiv charset passes",
     {"a.html": doc(GOOD_CSS, head='<!DOCTYPE html>\n<html lang="en"><head>'
                                   '<meta http-equiv="Content-Type" '
                                   'content="text/html; charset=UTF-8">'
                                   "<title>t</title>")},
     False, ""),

    # ---------- check_shared_widget ----------
    ("two documents with the same widget pass",
     {"a.html": doc(GOOD_CSS, script=WIDGET),
      "b.html": doc(GOOD_CSS, script=WIDGET)}, False, ""),

    ("one space of drift between two widgets is caught",
     {"a.html": doc(GOOD_CSS, script=WIDGET),
      "b.html": doc(GOOD_CSS, script=WIDGET.replace("var a", "var  a"))},
     True, "diverged"),

    # The false pass that shipped. A bare-<script> pattern did not merely
    # mis-handle this - it did not collect it, so the check compared one script
    # against nothing and reported agreement.
    ("drift hidden behind <script type=\"module\"> is caught",
     {"a.html": doc(GOOD_CSS, script=WIDGET),
      "b.html": doc(GOOD_CSS, script='<script type="module">\n  var b = 2;\n</script>')},
     True, "diverged"),

    ("an external <script src> is reported, not skipped",
     {"a.html": doc(GOOD_CSS, script='<script src="tabs.js"></script>')},
     True, "external script"),

    # ---------- check_theme_parity ----------
    ("a token differing between the toggle and the OS preference is caught",
     {"a.html": doc(GOOD_CSS.replace(
         ':root[data-theme="light"] { --ground: #EFEEE9;',
         ':root[data-theme="light"] { --ground: #FF0000;'))},
     True, "would disagree"),

    ("a token differing between the base and its data-theme twin is caught",
     {"a.html": doc(GOOD_CSS.replace(
         ':root[data-theme="dark"] { --ground: #0E1116;',
         ':root[data-theme="dark"] { --ground: #FF0000;'))},
     True, "must match"),

    ("data-theme blocks with no media query are caught",
     {"a.html": doc("""
  :root { --ground: #0E1116; }
  :root[data-theme="light"] { --ground: #EFEEE9; }
  :root[data-theme="dark"] { --ground: #0E1116; }
""")},
     True, "OS preference is ignored"),

    # ---------- check_every_colour_themes ----------
    ("a colour declared only in the base is caught — this was --ultraviolet",
     {"a.html": doc(GOOD_CSS.replace("--ink: #E7E9ED;\n    --sans",
                                     "--ink: #E7E9ED;\n    --accent: #A855F7;\n    --sans"))},
     True, "never themes"),

    ("a colour missing from just one override is caught",
     {"a.html": doc(GOOD_CSS.replace(
         ':root[data-theme="dark"] { --ground: #0E1116; --ink: #E7E9ED; }',
         ':root[data-theme="dark"] { --ground: #0E1116; }'))},
     True, "missing from"),

    ("a non-colour token is not required to theme",
     {"a.html": doc(GOOD_CSS)}, False, ""),

    # ---------- the mutual-deferral gap ----------
    # A themed document whose base :root cannot be read, with no data-theme
    # block. check_theme_parity short-circuited before reading the base;
    # check_every_colour_themes deferred to it by comment. Both went quiet.
    ("an unreadable base :root is reported even with no data-theme block",
     {"a.html": doc("""
  :root {
    --ground: #0E1116;
  @media (prefers-color-scheme: light) {
    :root { --ground: #EFEEE9; }
  }
""")},
     True, "could not be read"),

    # ---------- the scanners ----------
    ("a brace inside a CSS string does not desync the block reader",
     {"a.html": doc(GOOD_CSS + '\n  .x::before { content: "{"; }\n')},
     False, ""),

    ("a semicolon inside a CSS string does not truncate a declaration",
     {"a.html": doc(GOOD_CSS.replace("--sans: system-ui, sans-serif;",
                                     '--sep: ";";\n    --sans: system-ui, sans-serif;'))},
     False, ""),

    # GOOD_CSS had no comments, so extracting the shared CSS scanner broke
    # comment handling and this file said nothing - the two real documents
    # caught it. A meta-test whose fixtures are simpler than the real input
    # tests the fixtures.
    ("a comment before the first declaration does not eat it",
     {"a.html": doc(GOOD_CSS.replace("  :root {",
                                     "  :root {\n    /* a note; with a semicolon and a { brace */"))},
     False, ""),

    ("a comment between declarations does not eat the next one",
     {"a.html": doc(GOOD_CSS.replace("--ink: #E7E9ED;",
                                     "--ink: #E7E9ED;\n    /* mid-block */"))},
     False, ""),

    ("a reformatted :root with no indent is still found",
     {"a.html": doc(GOOD_CSS.replace("\n  :root {", "\n:root{"))}, False, ""),

    # ---------- vacuous passes ----------
    ("an unthemed document is not required to have a :root",
     {"a.html": doc("", body="<p>plain</p>")}, False, ""),

    ("no documents at all is a failure, not a pass",
     {}, True, "no HTML under docs/"),

    ("a bare <svg/> with no children self-closes",
     {"a.html": doc(GOOD_CSS, body="<svg/><p>x</p>")}, False, ""),

    ("a data-type attribute does not classify the script",
     {"a.html": doc(GOOD_CSS, script=WIDGET),
      "b.html": doc(GOOD_CSS, script='<script data-type="module">\n  var a = 1;\n</script>')},
     False, ""),

    ("a colour named by a keyword still has to theme",
     {"a.html": doc(GOOD_CSS.replace("--ink: #E7E9ED;\n    --sans",
                                     "--ink: #E7E9ED;\n    --brand: red;\n    --sans"))},
     True, "never themes"),

    ("<div/> is not self-closing in HTML and must not balance the stack",
     {"a.html": doc(GOOD_CSS, body="<div/><p>x</p>")}, True, "never closed"),

    ("<circle/> inside <svg> is self-closing and must balance",
     {"a.html": doc(GOOD_CSS, body='<svg viewBox="0 0 2 2"><circle r="1"/>'
                                   '<line x1="0" y1="0" x2="1" y2="1"/></svg>')},
     False, ""),

    ("identical bodies under <script> and <script type=module> are not one widget",
     {"a.html": doc(GOOD_CSS, script=WIDGET),
      "b.html": doc(GOOD_CSS, script='<script type="module">\n  var a = 1;\n</script>')},
     True, "diverged"),

    ("a > inside an attribute value does not truncate the script body",
     {"a.html": doc(GOOD_CSS, script='<script data-x=">">\n  var a = 1;\n</script>'),
      "b.html": doc(GOOD_CSS, script=WIDGET)},
     False, ""),

    # A media query with no opening brace used to raise a bare ValueError out
    # of media_spans and kill main() with a traceback - in the file whose whole
    # promise is a path and a reason instead of a stack.
    ("a media query with no opening brace reports rather than crashing",
     {"a.html": doc("  :root { --a: #ffffff; }\n"
                    "  @media (prefers-color-scheme: dark)\n")},
     True, "could not be read"),
]


# The board-count check needs a workflow to count, so these carry one.
# (name, board html, workflow yaml, expect_failure, needle)
BOARD_CASES: list[tuple[str, str, str, bool, str]] = [
    ("a matching count passes",
     doc(GOOD_CSS, body='<div data-harness-count="2">x</div>'),
     "steps:\n  - run: python3 tests/a_test.py\n  - run: python3 tests/b_test.py\n",
     False, ""),

    ("a wrong count is caught",
     doc(GOOD_CSS, body='<div data-harness-count="1">x</div>'),
     "steps:\n  - run: python3 tests/a_test.py\n  - run: python3 tests/b_test.py\n",
     True, "claims 1 harnesses; checks.yml runs 2"),

    ("no count attribute at all is caught",
     doc(GOOD_CSS, body="<div>x</div>"),
     "steps:\n  - run: python3 tests/a_test.py\n",
     True, "no data-harness-count"),

    # The counter was anchored on `run:` and found 1 of 3 in this shape.
    ("a run: | block scalar is counted",
     doc(GOOD_CSS, body='<div data-harness-count="3">x</div>'),
     ("steps:\n  - run: |\n      python3 tests/a_test.py\n"
      "      python3 tests/b_test.py\n  - run: python3 tests/c_test.py\n"),
     False, ""),

    ("a chained command is counted",
     doc(GOOD_CSS, body='<div data-harness-count="2">x</div>'),
     "steps:\n  - run: python3 tests/a_test.py && python3 tests/b_test.py\n",
     False, ""),

    # Greedy \S+ with no trailing anchor captured `tests/foo.py` out of
    # `tests/foo.pyx`, inflating the count against a file that does not run.
    ("a .pyx path is not counted as a .py harness",
     doc(GOOD_CSS, body='<div data-harness-count="1">x</div>'),
     "steps:\n  - run: python3 tests/a_test.py\n  - run: python3 tests/b.pyx\n",
     False, ""),

    # A pytest/tox/wrapper step would have dropped out of the count in silence.
    ("a test invoked by a wrapper is reported, not silently dropped",
     doc(GOOD_CSS, body='<div data-harness-count="1">x</div>'),
     "steps:\n  - run: python3 tests/a_test.py\n  - run: pytest tests/b_test.py\n",
     True, "cannot read"),

    ("a path named only in a comment is not counted",
     doc(GOOD_CSS, body='<div data-harness-count="1">x</div>'),
     "steps:\n  # python3 tests/ghost_test.py used to run here\n"
     "  - run: python3 tests/a_test.py\n",
     False, ""),
]


def run_against(files: dict[str, str], workflow: str | None = None) -> tuple[int, str]:
    """Point the harness at a scratch docs/ and capture what it reports.

    `workflow` writes a .github/workflows/checks.yml, so the board-count check
    can be exercised against a real file rather than only against this
    repository's own - which is the only shape it would otherwise ever see.
    """
    tmp = Path(tempfile.mkdtemp())
    try:
        docs = tmp / "docs"
        docs.mkdir()
        for name, content in files.items():
            (docs / name).write_text(content, encoding="utf-8")
        if workflow is not None:
            wf = tmp / ".github" / "workflows"
            wf.mkdir(parents=True)
            (wf / "checks.yml").write_text(workflow, encoding="utf-8")

        real_docs, real_repo = A.DOCS, A.REPO
        A.DOCS, A.REPO = docs, tmp
        buf: list[str] = []
        # contextlib.redirect_stdout rather than monkeypatching builtins.print:
        # the stdlib primitive exists for this and does not interact oddly with
        # a runner that also patches print.
        sink = io.StringIO()
        try:
            with contextlib.redirect_stdout(sink):
                code = A.main()
        except Exception as exc:  # noqa: BLE001 - a Ctrl-C is not a finding
            # A harness that dies with a traceback where it should report is
            # the failure this whole stack is about. Reverting the media_spans
            # fix made THIS file crash rather than say which case broke.
            buf.append(f"the harness raised {type(exc).__name__}: {exc}")
            code = 1
        finally:
            A.DOCS, A.REPO = real_docs, real_repo
        return code, sink.getvalue() + "\n".join(buf)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def check_theme_invariant_exemption() -> list[str]:
    """The exemption path must actually exempt.

    THEME_INVARIANT ships empty with a paragraph of justification and no
    exercised branch. An exemption nobody has ever taken is a promise, and the
    first person to need it would find out at that moment whether it works.
    """
    files = {"a.html": doc(GOOD_CSS.replace(
        "--ink: #E7E9ED;\n    --sans",
        "--ink: #E7E9ED;\n    --brand: #A855F7;\n    --sans"))}

    code, _ = run_against(files)
    if code == 0:
        return ["an unthemed colour passed even before the exemption was "
                "applied; this case proves nothing as written"]

    original = A.THEME_INVARIANT
    A.THEME_INVARIANT = {"--brand"}
    try:
        code, output = run_against(files)
    finally:
        A.THEME_INVARIANT = original
    if code != 0:
        return [f"THEME_INVARIANT did not suppress the finding for an exempted "
                f"token; the exemption path does not work. output: "
                f"{output.strip()[:200]}"]
    return []


def check_board_cases() -> list[str]:
    """The board-count check, against workflows it would otherwise never see."""
    out = []
    for name, board, workflow, expect_failure, needle in BOARD_CASES:
        code, output = run_against({"big-board.html": board}, workflow=workflow)
        failed = code != 0
        if failed != expect_failure:
            out.append(f"board: {name}\n    expected "
                       f"{'a failure' if expect_failure else 'a pass'}, got "
                       f"{'a failure' if failed else 'a pass'}\n"
                       f"    output: {output.strip()[:300]}")
        elif expect_failure and needle and needle not in output:
            out.append(f"board: {name}\n    failed for the wrong reason: "
                       f"{needle!r} not in the report\n"
                       f"    output: {output.strip()[:300]}")
    return out


def main() -> int:
    failures = check_theme_invariant_exemption() + check_board_cases()
    for name, files, expect_failure, needle in CASES:
        code, output = run_against(files)
        failed = code != 0
        if failed != expect_failure:
            failures.append(
                f"{name}\n    expected {'a failure' if expect_failure else 'a pass'}, "
                f"got {'a failure' if failed else 'a pass'}\n"
                f"    output: {output.strip()[:300]}")
        elif expect_failure and needle and needle not in output:
            failures.append(
                f"{name}\n    failed as expected, but for the wrong reason: "
                f"{needle!r} not in the report\n    output: {output.strip()[:300]}")

    if failures:
        print("harness test: FAILED")
        for line in failures:
            print(f"  {line}")
        return 1

    fails = sum(1 for _, _, e, _ in CASES if e)
    print(f"harness test: {len(CASES)} document cases and {len(BOARD_CASES)} board-count cases behave — {fails} that must fail do")
    return 0


if __name__ == "__main__":
    sys.exit(main())
