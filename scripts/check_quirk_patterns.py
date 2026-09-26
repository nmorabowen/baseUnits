"""Quirk-pattern lint for baseUnits (agent surface, see docs/agent-surface.md).

Turns a lesson that names a greppable pattern into a CI failure, so a known
trap fails the build instead of relying on someone re-reading AGENTS.md.
Dependency-free (standard library only).

  Q1 registry   Every pre-built system module src/baseUnits/systems/<name>.py
                must appear in each hand-maintained list of the systems:

                  consistency   test/test_consistency.py         SYSTEMS
                                (a miss: the system escapes "the one rule")
                  docs_tables   docs/scripts/gen_unit_tables.py  SYSTEMS
                                (a miss: the published Systems page omits it)
                  package_doc   src/baseUnits/__init__.py, the docstring
                                paragraph that names the pre-built systems
                  readme        README.md, the "## Available systems" list

                Only the list itself counts. Python lists are read with `ast`:
                an entry is a str, a tuple/list whose FIRST item is a str, or
                pytest.param(<str>, ...). README entries are the bullets
                "- `baseUnits.systems.<name>`" inside the "Available systems"
                section; docstring entries are the ``<name>`` tokens of the
                paragraph that says "pre-built systems". A name mentioned
                anywhere else (a code example, a comment, another paragraph)
                does not count.

                These are fixed, known sites in this repo's own files, so a
                site that is missing or cannot be read is itself a finding.
                This departs from "stay silent when you can't read a case",
                which is for scans over arbitrary code: a silently skipped
                site here would switch the rule off without anyone noticing.

                Incident: at 862b7e0 there were eight system modules while
                README.md listed four and the package docstring three (fixed
                in d1a655f). See AGENTS.md, Lessons, "Adding a system: the
                registration sites drift".

                Waive one site for one system with a real comment (not text
                inside a string) in that system's module:
                    # baseunits-lint: registry-ok <site> <reason>

A waiver needs a known site name and a reason of at least 12 characters. A
duplicate waiver, or a waiver that no longer suppresses anything (stale), is
itself a finding.

Usage:
    python scripts/check_quirk_patterns.py               # exit 1 on any finding
    python scripts/check_quirk_patterns.py --root <dir>  # lint another tree
"""

from __future__ import annotations

import argparse
import ast
import io
import re
import sys
import tokenize
from pathlib import Path
from typing import Callable, NamedTuple, Union

SYSTEMS_DIR = "src/baseUnits/systems"
WAIVER_RE = re.compile(r"#\s*baseunits-lint:\s*registry-ok\b[ \t]*(\S*)[ \t]*(.*)")
MIN_REASON = 12
IDENT = r"[A-Za-z_][A-Za-z0-9_]*"
GUIDE = ".claude/skills/baseunits-new-system/SKILL.md"


class Finding(NamedTuple):
    path: str
    line: int
    rule: str
    message: str

    def __str__(self) -> str:
        return f"{self.path}:{self.line}: {self.rule}: {self.message}"


class Reading(NamedTuple):
    """A site that was read: the systems it lists, and the line of the list."""

    path: str
    line: int
    names: set[str]


class Unreadable(NamedTuple):
    """A site that could not be read; reported as a finding."""

    path: str
    line: int
    why: str


SiteResult = Union[Reading, Unreadable]


def _read(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8-sig")
    except (OSError, UnicodeDecodeError):
        return None


def _parse(path: Path) -> ast.Module | None:
    text = _read(path)
    if text is None:
        return None
    try:
        return ast.parse(text)
    except SyntaxError:
        return None


def _str_const(node: ast.expr) -> str | None:
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    return None


def _entry_name(elt: ast.expr) -> str | None:
    """System name of one list entry, or None if the entry has another shape."""
    if isinstance(elt, (ast.Tuple, ast.List)):
        return _str_const(elt.elts[0]) if elt.elts else None
    if isinstance(elt, ast.Call):
        func = elt.func
        is_param = (isinstance(func, ast.Attribute) and func.attr == "param") or (
            isinstance(func, ast.Name) and func.id == "param"
        )
        if not is_param or not elt.args:
            return None
        return _entry_name(elt.args[0])
    return _str_const(elt)


def _names_in(value: ast.expr) -> set[str] | None:
    """Names in a literal list/tuple of entries; None if any entry is unreadable."""
    if not isinstance(value, (ast.List, ast.Tuple)):
        return None
    names: set[str] = set()
    for elt in value.elts:
        name = _entry_name(elt)
        if name is None:
            return None
        names.add(name)
    return names


def _touches(stmt: ast.stmt, var: str) -> bool:
    """True if a module-level statement assigns to `var` or calls a method on it."""
    targets: list[ast.expr] = []
    if isinstance(stmt, ast.Assign):
        targets = list(stmt.targets)
    elif isinstance(stmt, (ast.AnnAssign, ast.AugAssign)):
        targets = [stmt.target]
    elif isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Call):
        func = stmt.value.func
        if isinstance(func, ast.Attribute):
            targets = [func.value]
    return any(isinstance(t, ast.Name) and t.id == var for t in targets)


def _py_site(rel: str, var: str) -> Callable[[Path], SiteResult]:
    def read(root: Path) -> SiteResult:
        tree = _parse(root / rel)
        if tree is None:
            return Unreadable(rel, 1, "file is missing, not UTF-8, or not valid Python")
        stmts = [s for s in tree.body if _touches(s, var)]
        if not stmts:
            return Unreadable(rel, 1, f"no module-level {var} assignment")
        first = stmts[0]
        if len(stmts) > 1:
            return Unreadable(rel, stmts[1].lineno, f"{var} is modified after it is assigned")
        value = first.value if isinstance(first, (ast.Assign, ast.AnnAssign)) else None
        names = _names_in(value) if value is not None else None
        if value is None or names is None:
            return Unreadable(
                rel, first.lineno, f"{var} is not a literal list of entries the lint can read"
            )
        return Reading(rel, value.lineno, names)

    return read


def _readme_site(root: Path) -> SiteResult:
    rel = "README.md"
    text = _read(root / rel)
    if text is None:
        return Unreadable(rel, 1, "file is missing or not UTF-8")
    lines = text.splitlines()
    heading = next(
        (i for i, line in enumerate(lines) if re.match(r"^##\s+Available systems\s*$", line)),
        None,
    )
    if heading is None:
        return Unreadable(rel, 1, 'no "## Available systems" section')
    names: set[str] = set()
    in_fence = False
    for line in lines[heading + 1 :]:
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if re.match(r"^#{1,6}\s", line):
            break
        m = re.match(rf"^[-*]\s+`baseUnits\.systems\.({IDENT})`", line)
        if m:
            names.add(m.group(1))
    if not names:
        return Unreadable(rel, heading + 1, '"Available systems" lists no systems')
    return Reading(rel, heading + 1, names)


def _package_doc_site(root: Path) -> SiteResult:
    rel = "src/baseUnits/__init__.py"
    tree = _parse(root / rel)
    if tree is None:
        return Unreadable(rel, 1, "file is missing, not UTF-8, or not valid Python")
    first = tree.body[0] if tree.body else None
    doc = _str_const(first.value) if isinstance(first, ast.Expr) else None
    if first is None or doc is None:
        return Unreadable(rel, 1, "no module docstring")
    for para in re.split(r"\n[ \t]*\n", doc):
        if "pre-built systems" in para.lower():
            names = set(re.findall(rf"``({IDENT})``", para))
            line = first.lineno + doc.count("\n", 0, doc.find(para))
            if not names:
                return Unreadable(rel, line, "the pre-built systems paragraph names no systems")
            return Reading(rel, line, names)
    return Unreadable(rel, first.lineno, 'no docstring paragraph mentions "pre-built systems"')


SITES: dict[str, Callable[[Path], SiteResult]] = {
    "consistency": _py_site("test/test_consistency.py", "SYSTEMS"),
    "docs_tables": _py_site("docs/scripts/gen_unit_tables.py", "SYSTEMS"),
    "package_doc": _package_doc_site,
    "readme": _readme_site,
}


def system_modules(root: Path) -> list[str]:
    """Names of the pre-built system modules (no __init__, no private files)."""
    sysdir = root / SYSTEMS_DIR
    if not sysdir.is_dir():
        return []
    return sorted(p.stem for p in sysdir.glob("*.py") if not p.stem.startswith("_"))


def _waivers(root: Path, name: str) -> list[tuple[int, str, str]] | None:
    """(line, site, reason) for every registry waiver COMMENT in a system module.

    Only real comments count (tokenize), so text inside a docstring is not a
    waiver. None if the module cannot be tokenized.
    """
    text = _read(root / SYSTEMS_DIR / f"{name}.py")
    if text is None:
        return None
    out = []
    try:
        for tok in tokenize.generate_tokens(io.StringIO(text).readline):
            if tok.type == tokenize.COMMENT:
                m = WAIVER_RE.search(tok.string)
                if m:
                    out.append((tok.start[0], m.group(1), m.group(2).strip()))
    except (tokenize.TokenError, SyntaxError):
        return None
    return out


def check_registry(root: Path) -> list[Finding]:
    systems = system_modules(root)
    findings: list[Finding] = []
    readings: dict[str, Reading] = {}
    for site, reader in SITES.items():
        result = reader(root)
        if isinstance(result, Unreadable):
            findings.append(
                Finding(result.path, result.line, "Q1", f"cannot read site {site}: {result.why}")
            )
        else:
            readings[site] = result
    for name in systems:
        module = f"{SYSTEMS_DIR}/{name}.py"
        waived: dict[str, int] = {}
        waivers = _waivers(root, name)
        if waivers is None:
            findings.append(Finding(module, 1, "Q1", "cannot tokenize module to read waivers"))
            waivers = []
        for lineno, site, reason in waivers:
            if site not in SITES:
                message = f"registry waiver names unknown site {site!r}"
            elif len(reason) < MIN_REASON:
                message = (
                    f"registry waiver for {site!r} needs a reason of at least "
                    f"{MIN_REASON} characters"
                )
            elif site in waived:
                message = f"duplicate registry waiver for {site!r} (first at line {waived[site]})"
            else:
                waived[site] = lineno
                continue
            findings.append(Finding(module, lineno, "Q1", message))
        for site in SITES:
            reading = readings.get(site)
            if reading is None:
                continue  # already reported as "cannot read site"
            listed = name in reading.names
            if site in waived:
                if listed:
                    findings.append(
                        Finding(
                            module,
                            waived[site],
                            "Q1",
                            f"stale registry waiver: {name!r} is listed in {site} "
                            f"({reading.path}:{reading.line})",
                        )
                    )
            elif not listed:
                findings.append(
                    Finding(
                        reading.path,
                        reading.line,
                        "Q1",
                        f"system {name!r} ({module}) is not listed in {site}; "
                        f"register it in every site ({GUIDE})",
                    )
                )
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="baseUnits quirk-pattern lint")
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
        help="repository root to lint (default: this checkout)",
    )
    args = parser.parse_args(argv)
    root: Path = args.root
    if not system_modules(root):
        print(f"quirk lint: no system modules under {root / SYSTEMS_DIR}", file=sys.stderr)
        return 2
    findings = check_registry(root)
    for f in findings:
        print(f)
    n_sys = len(system_modules(root))
    print(f"quirk lint: {len(findings)} finding(s) over {n_sys} system module(s)")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
