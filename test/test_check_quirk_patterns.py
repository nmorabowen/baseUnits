"""Self-test for scripts/check_quirk_patterns.py (see docs/agent-surface.md).

Each case builds a small synthetic repository tree and asserts that rule Q1
flags the bug shape it exists for, passes the fixed shape, reports a site it
cannot read, and handles waivers. Every hole found by the adversarial review
(docs/agent-surface.md, Revision 2) has a case here. Lives in test/ on purpose
so the normal ``pytest -q`` (and CI) runs it; the lint itself runs on the real
tree as its own, last CI step.
"""

from __future__ import annotations

import importlib.util
from collections.abc import Mapping
from pathlib import Path

import pytest

_SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "check_quirk_patterns.py"
_spec = importlib.util.spec_from_file_location("check_quirk_patterns", _SCRIPT)
assert _spec is not None and _spec.loader is not None
cq = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cq)

SYSTEMS = ["N_mm_s", "N_m_s", "kN_m_s"]
CONSISTENCY = "test/test_consistency.py"
TABLES = "docs/scripts/gen_unit_tables.py"
INIT = "src/baseUnits/__init__.py"
README = "README.md"


def _consistency(rows: list[str]) -> str:
    body = "".join(f"    {r},\n" for r in rows)
    return f'"""The one rule."""\n\nimport pytest\n\nSYSTEMS = [\n{body}]\n'


def _row(n: str) -> str:
    return f'("{n}", "mm", "N", None, "s")'


def _init(listed: list[str], extra: str = "") -> str:
    names = ", ".join(f"``{n}``" for n in listed)
    return (
        f'"""baseUnits.\n\nThe default system is re-exported.\n\n'
        f"Other pre-built systems live under ``baseUnits.systems``: {names}.\n"
        f'{extra}"""\n\nfrom .systems.N_mm_s import *\n'
    )


def _readme(listed: list[str], after: str = "") -> str:
    items = "".join(f"- `baseUnits.systems.{n}` - label\n" for n in listed)
    return f"# baseUnits\n\n## Available systems\n\n{items}\n## Quickstart\n\n{after}"


def _files(names: list[str]) -> dict[str, str]:
    """A tree in which every system is registered in every site."""
    files: dict[str, str] = {f"src/baseUnits/systems/{n}.py": f'"""{n}."""\n' for n in names}
    files["src/baseUnits/systems/__init__.py"] = ""
    files[CONSISTENCY] = _consistency([_row(n) for n in names])
    rows = "".join(f'    ("{n}", "label", "prose"),\n' for n in names)
    files[TABLES] = f"SYSTEMS = [\n{rows}]\n"
    files[INIT] = _init(names)
    files[README] = _readme(names)
    return files


def _write(root: Path, files: Mapping[str, str | bytes]) -> Path:
    for rel, content in files.items():
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(content, bytes):
            p.write_bytes(content)
        else:
            p.write_text(content, encoding="utf-8")
    return root


def _lint(tmp_path: Path, files: dict) -> list[str]:
    return [str(f) for f in cq.check_registry(_write(tmp_path, files))]


def _only(found: list[str], site: str, system: str, where: str) -> None:
    assert len(found) == 1, found
    assert found[0].startswith(where + ": Q1:"), found
    assert f"system '{system}'" in found[0] and f"not listed in {site};" in found[0], found


def _unreadable(found: list[str], site: str, where: str) -> None:
    assert len(found) == 1, found
    assert found[0].startswith(where + ": Q1:"), found
    assert f"cannot read site {site}:" in found[0], found


# --------------------------------------------------------------- must pass
def test_complete_tree_passes(tmp_path):
    assert _lint(tmp_path, _files(SYSTEMS)) == []


def test_private_modules_and_init_are_not_systems(tmp_path):
    files = _files(SYSTEMS)
    files["src/baseUnits/systems/_helper.py"] = "X = 1\n"
    assert _lint(tmp_path, files) == []


def test_annotated_assignment_is_read(tmp_path):
    files = _files(SYSTEMS)
    files[TABLES] = f"SYSTEMS: list[str] = {SYSTEMS!r}\n"
    assert _lint(tmp_path, files) == []


def test_pytest_param_row_is_read_by_its_first_argument(tmp_path):
    files = _files(SYSTEMS)
    rows = [_row("N_mm_s"), _row("N_m_s"), 'pytest.param("kN_m_s", "m", "kN", None, "s", id="x")']
    files[CONSISTENCY] = _consistency(rows)
    assert _lint(tmp_path, files) == []


def test_utf8_bom_is_read(tmp_path):
    files: dict = _files(SYSTEMS)
    files[CONSISTENCY] = b"\xef\xbb\xbf" + files[CONSISTENCY].encode("utf-8")
    assert _lint(tmp_path, files) == []


def test_readme_code_fence_with_hash_lines_does_not_end_the_section(tmp_path):
    files = _files(SYSTEMS)
    items = "".join(f"- `baseUnits.systems.{n}` - label\n" for n in SYSTEMS[1:])
    files[README] = (
        "## Available systems\n\n- `baseUnits.systems.N_mm_s` - default\n\n"
        f"```bash\n# a comment line\n```\n\n{items}\n## Quickstart\n"
    )
    assert _lint(tmp_path, files) == []


# ------------------------------------------------- must flag (bug shapes)
def test_readme_missing_a_system_is_flagged_at_its_heading(tmp_path):
    """The 862b7e0 shape: modules added, README list not updated."""
    files = _files(SYSTEMS)
    files[README] = _readme(["N_mm_s", "N_m_s"])
    _only(_lint(tmp_path, files), "readme", "kN_m_s", "README.md:3")


def test_readme_mention_outside_the_list_does_not_count(tmp_path):
    """Review finding 1: a code example naming the system is not the list."""
    files = _files(SYSTEMS)
    files[README] = _readme(
        ["N_mm_s", "N_m_s"], after="```python\nfrom baseUnits.systems.kN_m_s import m\n```\n"
    )
    _only(_lint(tmp_path, files), "readme", "kN_m_s", "README.md:3")


def test_readme_list_after_the_next_heading_does_not_count(tmp_path):
    files = _files(SYSTEMS)
    files[README] = _readme(["N_mm_s", "N_m_s"], after="- `baseUnits.systems.kN_m_s` - x\n")
    _only(_lint(tmp_path, files), "readme", "kN_m_s", "README.md:3")


def test_readme_whole_identifier_kN_m_s_does_not_satisfy_N_m_s(tmp_path):
    files = _files(SYSTEMS)
    files[README] = _readme(["N_mm_s", "kN_m_s"])
    _only(_lint(tmp_path, files), "readme", "N_m_s", "README.md:3")


def test_package_doc_needs_the_systems_paragraph(tmp_path):
    """The code imports N_mm_s and another paragraph names it: neither counts."""
    files = _files(SYSTEMS)
    files[INIT] = _init(["N_m_s", "kN_m_s"], extra="\nSee ``N_mm_s`` for the default.\n")
    _only(_lint(tmp_path, files), "package_doc", "N_mm_s", f"{INIT}:5")


def test_consistency_missing_is_flagged_at_the_list_line(tmp_path):
    files = _files(SYSTEMS)
    files[CONSISTENCY] = _consistency([_row("N_mm_s"), _row("N_m_s")])
    _only(_lint(tmp_path, files), "consistency", "kN_m_s", f"{CONSISTENCY}:5")


def test_docs_tables_reads_only_the_first_item_of_a_row(tmp_path):
    """A label that happens to equal a system name does not register it."""
    files = _files(SYSTEMS)
    files[TABLES] = 'SYSTEMS = [("N_mm_s", "kN_m_s", "x"), ("N_m_s", "a", "b")]\n'
    _only(_lint(tmp_path, files), "docs_tables", "kN_m_s", f"{TABLES}:1")


def test_commented_out_entry_does_not_count(tmp_path):
    files = _files(SYSTEMS)
    files[TABLES] = 'SYSTEMS = [\n    "N_mm_s",\n    "N_m_s",\n    # "kN_m_s",\n]\n'
    _only(_lint(tmp_path, files), "docs_tables", "kN_m_s", f"{TABLES}:1")


# ------------------------------------ unreadable site -> a finding, not silence
@pytest.mark.parametrize(
    "site,rel", [("consistency", CONSISTENCY), ("docs_tables", TABLES), ("package_doc", INIT)]
)
def test_missing_python_site_file_is_a_finding(tmp_path, site, rel):
    files = _files(SYSTEMS)
    del files[rel]
    _unreadable(_lint(tmp_path, files), site, f"{rel}:1")


def test_missing_readme_is_a_finding(tmp_path):
    files = _files(SYSTEMS)
    del files[README]
    _unreadable(_lint(tmp_path, files), "readme", "README.md:1")


def test_missing_variable_is_a_finding(tmp_path):
    files = _files(SYSTEMS)
    files[TABLES] = "NAMES = []\n"
    _unreadable(_lint(tmp_path, files), "docs_tables", f"{TABLES}:1")


def test_concatenated_list_is_a_finding(tmp_path):
    """Review finding 2: `SYSTEMS = _EXTRA + [...]` used to pass silently."""
    files = _files(SYSTEMS)
    files[TABLES] = f"_EXTRA = []\nSYSTEMS = _EXTRA + {SYSTEMS!r}\n"
    _unreadable(_lint(tmp_path, files), "docs_tables", f"{TABLES}:2")


def test_one_non_literal_entry_makes_the_site_unreadable(tmp_path):
    files = _files(SYSTEMS)
    files[TABLES] = 'NAME = "kN_m_s"\nSYSTEMS = ["N_mm_s", "N_m_s", NAME]\n'
    _unreadable(_lint(tmp_path, files), "docs_tables", f"{TABLES}:2")


@pytest.mark.parametrize(
    "later",
    ['SYSTEMS.append("x")', "SYSTEMS += []", "SYSTEMS = []"],
)
def test_list_modified_after_assignment_is_a_finding(tmp_path, later):
    files = _files(SYSTEMS)
    files[TABLES] = f"SYSTEMS = {SYSTEMS!r}\n{later}\n"
    _unreadable(_lint(tmp_path, files), "docs_tables", f"{TABLES}:2")


def test_syntax_error_is_a_finding(tmp_path):
    files = _files(SYSTEMS)
    files[CONSISTENCY] = "SYSTEMS = [\n"
    _unreadable(_lint(tmp_path, files), "consistency", f"{CONSISTENCY}:1")


def test_invalid_utf8_is_a_finding(tmp_path):
    files: dict = _files(SYSTEMS)
    files[README] = b"## Available systems\n\n- `baseUnits.systems.N_mm_s` \xff\n"
    _unreadable(_lint(tmp_path, files), "readme", "README.md:1")


def test_readme_without_section_or_entries_is_a_finding(tmp_path):
    files = _files(SYSTEMS)
    files[README] = "# baseUnits\n\n## Systems\n\n- `baseUnits.systems.N_mm_s`\n"
    _unreadable(_lint(tmp_path, files), "readme", "README.md:1")
    files[README] = "# baseUnits\n\n## Available systems\n\nSee the docs.\n"
    _unreadable(_lint(tmp_path / "b", files), "readme", "README.md:3")


def test_docstring_without_the_systems_paragraph_is_a_finding(tmp_path):
    files = _files(SYSTEMS)
    files[INIT] = '"""baseUnits.\n\nNothing about systems here.\n"""\n'
    _unreadable(_lint(tmp_path, files), "package_doc", f"{INIT}:1")
    files[INIT] = "X = 1\n"
    _unreadable(_lint(tmp_path / "b", files), "package_doc", f"{INIT}:1")


# ------------------------------------------------------------------- waivers
def _waive(files: dict, system: str, comment: str) -> None:
    files[f"src/baseUnits/systems/{system}.py"] += comment + "\n"


REASON = "experimental, not advertised"


def test_waiver_with_reason_suppresses_one_site(tmp_path):
    files = _files(SYSTEMS)
    files[README] = _readme(["N_mm_s", "N_m_s"])
    _waive(files, "kN_m_s", f"# baseunits-lint: registry-ok readme {REASON}")
    assert _lint(tmp_path, files) == []


@pytest.mark.parametrize(
    "comment,expected",
    [
        ("# baseunits-lint: registry-ok readme short", "needs a reason"),
        (f"# baseunits-lint: registry-ok readmee {REASON}", "unknown site"),
    ],
)
def test_bad_waiver_is_a_finding_and_does_not_suppress(tmp_path, comment, expected):
    files = _files(SYSTEMS)
    files[README] = _readme(["N_mm_s", "N_m_s"])
    _waive(files, "kN_m_s", comment)
    found = _lint(tmp_path, files)
    assert len(found) == 2, found
    assert any(expected in f for f in found), found
    assert any("not listed in readme;" in f for f in found), found


def test_stale_waiver_is_a_finding(tmp_path):
    files = _files(SYSTEMS)
    _waive(files, "kN_m_s", f"# baseunits-lint: registry-ok readme {REASON}")
    found = _lint(tmp_path, files)
    assert len(found) == 1 and "stale registry waiver" in found[0], found


def test_duplicate_waiver_is_a_finding(tmp_path):
    files = _files(SYSTEMS)
    files[README] = _readme(["N_mm_s", "N_m_s"])
    _waive(files, "kN_m_s", f"# baseunits-lint: registry-ok readme {REASON}")
    _waive(files, "kN_m_s", f"# baseunits-lint: registry-ok readme {REASON} again")
    found = _lint(tmp_path, files)
    assert len(found) == 1 and "duplicate registry waiver" in found[0], found


def test_waiver_text_inside_a_docstring_is_not_a_waiver(tmp_path):
    files = _files(SYSTEMS)
    files[README] = _readme(["N_mm_s", "N_m_s"])
    files["src/baseUnits/systems/kN_m_s.py"] = (
        f'"""kN_m_s.\n\n# baseunits-lint: registry-ok readme {REASON}\n"""\n'
    )
    _only(_lint(tmp_path, files), "readme", "kN_m_s", "README.md:3")


def test_waiver_for_an_unreadable_site_cannot_hide_it(tmp_path):
    """Review finding 3: the site finding is still reported."""
    files = _files(SYSTEMS)
    del files[README]
    _waive(files, "kN_m_s", f"# baseunits-lint: registry-ok readme {REASON}")
    _unreadable(_lint(tmp_path, files), "readme", "README.md:1")


def test_module_that_cannot_be_tokenized_is_a_finding(tmp_path):
    files = _files(SYSTEMS)
    files["src/baseUnits/systems/kN_m_s.py"] = '"""unterminated\n'
    found = _lint(tmp_path, files)
    assert len(found) == 1 and "cannot tokenize" in found[0], found


# ---------------------------------------------------------------------- CLI
def test_main_exit_codes(tmp_path, capsys):
    good = _write(tmp_path / "good", _files(SYSTEMS))
    assert cq.main(["--root", str(good)]) == 0

    files = _files(SYSTEMS)
    files[README] = _readme(["N_mm_s"])
    bad = _write(tmp_path / "bad", files)
    assert cq.main(["--root", str(bad)]) == 1

    only_modules = {k: v for k, v in _files(SYSTEMS).items() if "/systems/" in k}
    dark = _write(tmp_path / "dark", only_modules)
    assert cq.main(["--root", str(dark)]) == 1  # all four sites missing

    assert cq.main(["--root", str(tmp_path / "empty")]) == 2
    capsys.readouterr()
