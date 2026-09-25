"""Self-test for scripts/check_quirk_patterns.py (see docs/agent-surface.md).

Each case builds a small synthetic repository tree and asserts that rule Q1
flags the bug shape it exists for, passes the fixed shape, and stays silent on
shapes it cannot read. Lives in test/ on purpose so the normal ``pytest -q``
(and CI) runs it; the lint itself runs on the real tree as its own CI step.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

_SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "check_quirk_patterns.py"
_spec = importlib.util.spec_from_file_location("check_quirk_patterns", _SCRIPT)
assert _spec is not None and _spec.loader is not None
cq = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cq)

SYSTEMS = ["N_mm_s", "N_m_s", "kN_m_s"]


def _files(names: list[str]) -> dict[str, str]:
    """A tree in which every system is registered in every site."""
    files: dict[str, str] = {"src/baseUnits/_unit_consts.pyi": "BASE: str\n"}
    for n in names:
        files[f"src/baseUnits/systems/{n}.py"] = f'"""{n} system."""\n'
        files[f"src/baseUnits/systems/{n}.pyi"] = "from .._unit_consts import *\n"
    files["src/baseUnits/systems/__init__.py"] = ""
    files["scripts/gen_stubs.py"] = f"SYSTEMS = {names!r}\n"
    rows = "".join(f'    ("{n}", "mm", "N", None, "s"),\n' for n in names)
    bases = "".join(f'    "{n}": (None, None, None),\n' for n in names)
    files["test/test_consistency.py"] = f"SYSTEMS = [\n{rows}]\n\nNATURAL_BASES = {{\n{bases}}}\n"
    tables = "".join(f'    ("{n}", "label", "prose"),\n' for n in names)
    files["docs/scripts/gen_unit_tables.py"] = f"SYSTEMS = [\n{tables}]\n"
    listed = ", ".join(f"``{n}``" for n in names)
    files["src/baseUnits/__init__.py"] = (
        f'"""baseUnits.\n\nSystems: {listed}.\n"""\n\nfrom .systems.N_mm_s import *\n'
    )
    files["README.md"] = "".join(f"- `baseUnits.systems.{n}`\n" for n in names)
    files["docs/architecture.md"] = f"Available out of the box: {listed}.\n"
    return files


def _lint(tmp_path: Path, files: dict[str, str]) -> list[str]:
    for rel, text in files.items():
        p = tmp_path / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
    return [str(f) for f in cq.check_registry(tmp_path)]


def _only(findings: list[str], site: str, system: str) -> None:
    assert len(findings) == 1, findings
    assert f"system '{system}'" in findings[0], findings
    assert f"not listed in {site};" in findings[0], findings


# --------------------------------------------------------------- must pass
def test_complete_tree_passes(tmp_path):
    assert _lint(tmp_path, _files(SYSTEMS)) == []


def test_private_modules_and_init_are_not_systems(tmp_path):
    files = _files(SYSTEMS)
    files["src/baseUnits/systems/_helper.py"] = "X = 1\n"
    assert _lint(tmp_path, files) == []


def test_annotated_assignment_is_read(tmp_path):
    files = _files(SYSTEMS)
    files["scripts/gen_stubs.py"] = f"SYSTEMS: list[str] = {SYSTEMS!r}\n"
    assert _lint(tmp_path, files) == []


# ------------------------------------------------- must flag (one per site)
def test_flags_readme_missing_a_system(tmp_path):
    """The 862b7e0 shape: modules added, README list not updated."""
    files = _files(SYSTEMS)
    files["README.md"] = "- `baseUnits.systems.N_mm_s`\n- `baseUnits.systems.N_m_s`\n"
    _only(_lint(tmp_path, files), "readme", "kN_m_s")


def test_flags_architecture_missing_a_system(tmp_path):
    """The live shape: docs/architecture.md stuck on an older list."""
    files = _files(SYSTEMS)
    files["docs/architecture.md"] = "Available out of the box: `N_mm_s`, `N_m_s`.\n"
    _only(_lint(tmp_path, files), "architecture", "kN_m_s")


def test_package_doc_needs_the_docstring_not_the_code(tmp_path):
    """Importing N_mm_s in code does not count; the docstring must name it."""
    files = _files(SYSTEMS)
    files["src/baseUnits/__init__.py"] = (
        '"""baseUnits.\n\nOther systems: ``N_m_s``, ``kN_m_s``.\n"""\n\n'
        "from .systems.N_mm_s import *\n"
    )
    _only(_lint(tmp_path, files), "package_doc", "N_mm_s")


def test_flags_gen_stubs_missing_a_system(tmp_path):
    files = _files(SYSTEMS)
    files["scripts/gen_stubs.py"] = 'SYSTEMS = ["N_mm_s", "N_m_s"]\n'
    _only(_lint(tmp_path, files), "gen_stubs", "kN_m_s")


def test_flags_consistency_and_natural_bases(tmp_path):
    files = _files(SYSTEMS)
    files["test/test_consistency.py"] = (
        'SYSTEMS = [("N_mm_s", "mm", "N", None, "s"), ("N_m_s", "m", "N", None, "s")]\n'
        'NATURAL_BASES = {"N_mm_s": (1,), "N_m_s": (1,)}\n'
    )
    found = _lint(tmp_path, files)
    assert len(found) == 2, found
    assert any("not listed in consistency;" in f for f in found)
    assert any("not listed in natural_bases;" in f for f in found)


def test_flags_docs_tables_missing_a_system(tmp_path):
    files = _files(SYSTEMS)
    files["docs/scripts/gen_unit_tables.py"] = 'SYSTEMS = [("N_mm_s", "a", "b")]\n'
    found = _lint(tmp_path, files)
    assert len(found) == 2 and all("docs_tables" in f for f in found), found


def test_flags_missing_stub_once_stubs_exist(tmp_path):
    files = _files(SYSTEMS)
    del files["src/baseUnits/systems/kN_m_s.pyi"]
    _only(_lint(tmp_path, files), "stub", "kN_m_s")


def test_no_stub_check_before_the_tree_has_stubs(tmp_path):
    files = {k: v for k, v in _files(SYSTEMS).items() if not k.endswith(".pyi")}
    assert _lint(tmp_path, files) == []


# ------------------------------------------------------ holes that must hold
def test_word_boundary_kN_m_s_does_not_satisfy_N_m_s(tmp_path):
    files = _files(SYSTEMS)
    files["docs/architecture.md"] = "Available: `N_mm_s`, `kN_m_s`.\n"
    _only(_lint(tmp_path, files), "architecture", "N_m_s")


def test_commented_out_entry_does_not_count(tmp_path):
    files = _files(SYSTEMS)
    files["scripts/gen_stubs.py"] = 'SYSTEMS = [\n    "N_mm_s",\n    "N_m_s",\n    # "kN_m_s",\n]\n'
    _only(_lint(tmp_path, files), "gen_stubs", "kN_m_s")


# ------------------------------------------------ unreadable -> stay silent
def test_unreadable_shape_is_skipped(tmp_path):
    """NATURAL_BASES keyed by (force, length) tuples, as before 47b6682."""
    files = _files(SYSTEMS)
    files["test/test_consistency.py"] = (
        "SYSTEMS = [" + ", ".join(f'("{n}", "mm", "N", "s")' for n in SYSTEMS) + "]\n"
        'NATURAL_BASES = {("N", "mm"): ("MPa", "mJ", "mJ_s")}\n'
    )
    assert _lint(tmp_path, files) == []


def test_missing_site_file_or_variable_is_skipped(tmp_path):
    files = _files(SYSTEMS)
    del files["docs/scripts/gen_unit_tables.py"]
    files["scripts/gen_stubs.py"] = "NAMES = []\n"
    assert _lint(tmp_path, files) == []


# ------------------------------------------------------------------- waivers
def _waive(files: dict[str, str], system: str, comment: str) -> None:
    files[f"src/baseUnits/systems/{system}.py"] += comment + "\n"


def test_waiver_with_reason_suppresses_one_site(tmp_path):
    files = _files(SYSTEMS)
    files["README.md"] = "- `baseUnits.systems.N_mm_s`\n- `baseUnits.systems.N_m_s`\n"
    _waive(files, "kN_m_s", "# baseunits-lint: registry-ok readme experimental, not advertised")
    assert _lint(tmp_path, files) == []


@pytest.mark.parametrize(
    "comment,expected",
    [
        ("# baseunits-lint: registry-ok readme short", "needs a reason"),
        ("# baseunits-lint: registry-ok readmee experimental, not advertised", "unknown site"),
    ],
)
def test_bad_waiver_is_a_finding_and_does_not_suppress(tmp_path, comment, expected):
    files = _files(SYSTEMS)
    files["README.md"] = "- `baseUnits.systems.N_mm_s`\n- `baseUnits.systems.N_m_s`\n"
    _waive(files, "kN_m_s", comment)
    found = _lint(tmp_path, files)
    assert len(found) == 2, found
    assert any(expected in f for f in found), found
    assert any("not listed in readme;" in f for f in found), found


def test_stale_waiver_is_a_finding(tmp_path):
    files = _files(SYSTEMS)
    _waive(files, "kN_m_s", "# baseunits-lint: registry-ok readme experimental, not advertised")
    found = _lint(tmp_path, files)
    assert len(found) == 1 and "stale registry waiver" in found[0], found


# ---------------------------------------------------------------------- CLI
def test_main_exit_codes(tmp_path, capsys):
    good = tmp_path / "good"
    _lint(good, _files(SYSTEMS))
    assert cq.main(["--root", str(good)]) == 0

    bad = tmp_path / "bad"
    files = _files(SYSTEMS)
    files["README.md"] = ""
    _lint(bad, files)
    assert cq.main(["--root", str(bad)]) == 1

    assert cq.main(["--root", str(tmp_path / "empty")]) == 2
    capsys.readouterr()
