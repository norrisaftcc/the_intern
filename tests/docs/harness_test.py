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

It has already shipped three defects of that kind in six rounds:

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

    ("a reformatted :root with no indent is still found",
     {"a.html": doc(GOOD_CSS.replace("\n  :root {", "\n:root{"))}, False, ""),

    # ---------- vacuous passes ----------
    ("an unthemed document is not required to have a :root",
     {"a.html": doc("", body="<p>plain</p>")}, False, ""),

    ("no documents at all is a failure, not a pass",
     {}, True, "no HTML under docs/"),
]


def run_against(files: dict[str, str]) -> tuple[int, str]:
    """Point the harness at a scratch docs/ and capture what it reports."""
    tmp = Path(tempfile.mkdtemp())
    try:
        docs = tmp / "docs"
        docs.mkdir()
        for name, content in files.items():
            (docs / name).write_text(content, encoding="utf-8")

        real_docs, real_repo = A.DOCS, A.REPO
        A.DOCS, A.REPO = docs, tmp
        buf: list[str] = []
        import builtins
        original = builtins.print
        builtins.print = lambda *a, **k: buf.append(" ".join(str(x) for x in a))
        try:
            code = A.main()
        finally:
            builtins.print = original
            A.DOCS, A.REPO = real_docs, real_repo
        return code, "\n".join(buf)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main() -> int:
    failures = []
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
    print(f"harness test: {len(CASES)} cases behave — {fails} that must fail "
          f"do, {len(CASES) - fails} that must pass do")
    return 0


if __name__ == "__main__":
    sys.exit(main())
