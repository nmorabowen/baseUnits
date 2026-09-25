"""Quirk-pattern lint for baseUnits (agent surface, see docs/agent-surface.md).

Turns a lesson that names a greppable pattern into a CI failure, so a known
trap fails the build instead of relying on someone re-reading AGENTS.md.
Dependency-free (standard library only); runs in well under a second.

  Q1 registry   Every pre-built system module src/baseUnits/systems/<name>.py
                must be listed in every place the repo enumerates the systems:

                  stub           src/baseUnits/systems/<name>.pyi exists
                                 (only once stubs exist: _unit_consts.pyi)
                  gen_stubs      scripts/gen_stubs.py            SYSTEMS
                  consistency    test/test_consistency.py        SYSTEMS
                  natural_bases  test/test_consistency.py        NATURAL_BASES
                  docs_tables    docs/scripts/gen_unit_tables.py SYSTEMS
                  package_doc    src/baseUnits/__init__.py       module docstring
                  readme         README.md
                  architecture   docs/architecture.md

                Python sites are read with `ast` (a name in a comment does not
                count); text sites need the name as a whole word (`N_m_s` is
                not satisfied by `kN_m_s`). A site whose file or variable is
                absent cannot be read and is skipped, never guessed.
                Incident: 862b7e0 had eight system modules while README.md
                listed four and the package docstring three (fixed in
                d1a655f); docs/architecture.md has listed four systems since,
                missed by three system additions (AGENTS.md, Lessons,
                "Adding a system: the registration sites drift").
                Waive one site for one system with a comment in that system's
                module:
                    # baseunits-lint: registry-ok <site> <reason>

A waiver needs a reason of at least 12 characters and a known site name, and a
waiver that no longer suppresses anything is itself a finding (stale).

Usage:
    python scripts/check_quirk_patterns.py               # exit 1 on any finding
    python scripts/check_quirk_patterns.py --root <dir>  # lint another tree
"""

from __future__ import annotations

import argparse
import ast
import re
import sys
from pathlib import Path
from typing import Callable, NamedTuple, Optional

SYSTEMS_DIR = "src/baseUnits/systems"
WAIVER_RE = re.compile(r"#\s*baseunits-lint:\s*registry-ok\b[ \t]*(\S*)[ \t]*(.*)")
MIN_REASON = 12


class Finding(NamedTuple):
    path: str
    line: int
    rule: str
    message: str

    def __str__(self) -> str:
        return f"{self.path}:{self.line}: {self.rule}: {self.message}"


def _read(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
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


def _module_value(tree: ast.Module, var: str) -> ast.expr | None:
    """Value assigned to module-level `var` (plain or annotated), else None."""
    for node in tree.body:
        if isinstance(node, ast.Assign):
            if any(isinstance(t, ast.Name) and t.id == var for t in node.targets):
                return node.value
        elif (
            isinstance(node, ast.AnnAssign)
            and isinstance(node.target, ast.Name)
            and node.target.id == var
            and node.value is not None
        ):
            return node.value
    return None


def _str_const(node: ast.expr) -> str | None:
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    return None


def _names_in(value: ast.expr) -> set[str] | None:
    """System names in a list/tuple of str, a list/tuple of tuples whose first
    item is a str, or the str keys of a dict. None if ANY entry has another
    shape (e.g. a dict keyed by (force, length) tuples, as test_consistency's
    NATURAL_BASES was before 47b6682): an unreadable site is skipped."""
    if isinstance(value, ast.Dict):
        names: set[str] = set()
        for key in value.keys:
            name = _str_const(key) if key is not None else None
            if name is None:
                return None
            names.add(name)
        return names
    if not isinstance(value, (ast.List, ast.Tuple)):
        return None
    names = set()
    for elt in value.elts:
        if isinstance(elt, (ast.Tuple, ast.List)) and elt.elts:
            elt = elt.elts[0]
        name = _str_const(elt)
        if name is None:
            return None
        names.add(name)
    return names


def _word_in(name: str, text: str) -> bool:
    return re.search(rf"(?<![A-Za-z0-9_]){re.escape(name)}(?![A-Za-z0-9_])", text) is not None


# A site reader returns (path shown in findings, line, names-or-None). For text
# sites the "names" are every system name found as a whole word.
SiteReader = Callable[[Path, list[str]], Optional[tuple[str, int, set[str]]]]


def _py_site(rel: str, var: str) -> SiteReader:
    def read(root: Path, systems: list[str]) -> tuple[str, int, set[str]] | None:
        tree = _parse(root / rel)
        if tree is None:
            return None
        value = _module_value(tree, var)
        if value is None:
            return None
        names = _names_in(value)
        if names is None:
            return None
        return rel, value.lineno, names

    return read


def _text_site(rel: str, docstring_only: bool = False) -> SiteReader:
    def read(root: Path, systems: list[str]) -> tuple[str, int, set[str]] | None:
        if docstring_only:
            tree = _parse(root / rel)
            text = ast.get_docstring(tree) if tree is not None else None
        else:
            text = _read(root / rel)
        if text is None:
            return None
        return rel, 1, {s for s in systems if _word_in(s, text)}

    return read


def _stub_site(root: Path, systems: list[str]) -> tuple[str, int, set[str]] | None:
    if not (root / "src/baseUnits/_unit_consts.pyi").is_file():
        return None  # the tree has no type stubs yet; nothing to check
    have = {s for s in systems if (root / SYSTEMS_DIR / f"{s}.pyi").is_file()}
    return f"{SYSTEMS_DIR}/<name>.pyi", 1, have


SITES: dict[str, SiteReader] = {
    "stub": _stub_site,
    "gen_stubs": _py_site("scripts/gen_stubs.py", "SYSTEMS"),
    "consistency": _py_site("test/test_consistency.py", "SYSTEMS"),
    "natural_bases": _py_site("test/test_consistency.py", "NATURAL_BASES"),
    "docs_tables": _py_site("docs/scripts/gen_unit_tables.py", "SYSTEMS"),
    "package_doc": _text_site("src/baseUnits/__init__.py", docstring_only=True),
    "readme": _text_site("README.md"),
    "architecture": _text_site("docs/architecture.md"),
}


def system_modules(root: Path) -> list[str]:
    """Names of the pre-built system modules (no __init__, no private files)."""
    sysdir = root / SYSTEMS_DIR
    if not sysdir.is_dir():
        return []
    return sorted(p.stem for p in sysdir.glob("*.py") if not p.stem.startswith("_"))


def _waivers(root: Path, name: str) -> list[tuple[int, str, str]]:
    """(line, site, reason) for every registry waiver in a system module."""
    text = _read(root / SYSTEMS_DIR / f"{name}.py") or ""
    out = []
    for lineno, line in enumerate(text.splitlines(), start=1):
        m = WAIVER_RE.search(line)
        if m:
            out.append((lineno, m.group(1), m.group(2).strip()))
    return out


def check_registry(root: Path) -> list[Finding]:
    systems = system_modules(root)
    findings: list[Finding] = []
    readings = {site: reader(root, systems) for site, reader in SITES.items()}
    for name in systems:
        module = f"{SYSTEMS_DIR}/{name}.py"
        waived: dict[str, int] = {}
        for lineno, site, reason in _waivers(root, name):
            if site not in SITES:
                findings.append(
                    Finding(module, lineno, "Q1", f"registry waiver names unknown site {site!r}")
                )
            elif len(reason) < MIN_REASON:
                findings.append(
                    Finding(
                        module,
                        lineno,
                        "Q1",
                        f"registry waiver for {site!r} needs a reason of at least "
                        f"{MIN_REASON} characters",
                    )
                )
            else:
                waived[site] = lineno
        for site, reading in readings.items():
            if reading is None:
                continue
            where, line, names = reading
            listed = name in names
            if site in waived:
                if listed:
                    findings.append(
                        Finding(
                            module,
                            waived[site],
                            "Q1",
                            f"stale registry waiver: {name!r} is listed in {site} ({where})",
                        )
                    )
                continue
            if not listed:
                findings.append(
                    Finding(
                        where,
                        line,
                        "Q1",
                        f"system {name!r} ({module}) is not listed in {site}; register "
                        f"it in every site (.claude/skills/baseunits-new-system/SKILL.md)",
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
