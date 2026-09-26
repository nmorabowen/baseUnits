# baseUnits: working rules for agents

`baseUnits` is a small Python library of float unit-conversion factors for
consistent unit systems (default N-mm-tonne-s). It is small, but several of the
user's design libraries depend on its numbers. A wrong factor here makes their
capacity checks wrong without any error. `CLAUDE.md` is the single line
`@AGENTS.md`, so Claude, Codex and other agents all read this file.

## Task guides: read the matching one before starting

These are short checklists. Each item points to a lesson below, or to the file
that explains it; the guides do not replace those sources.

| Doing this | Read first |
|---|---|
| Adding, renaming or removing a pre-built system (`src/baseUnits/systems/`) | [`.claude/skills/baseunits-new-system/SKILL.md`](.claude/skills/baseunits-new-system/SKILL.md) |
| Adding a unit, changing a factor value, or touching `baseUnits.checked` | [`.claude/skills/baseunits-change-factors/SKILL.md`](.claude/skills/baseunits-change-factors/SKILL.md) |

`python scripts/check_quirk_patterns.py` enforces the mechanical items. It is
the last step of `.github/workflows/test.yml`, and its self-test is
`test/test_check_quirk_patterns.py`. When a new lesson names a pattern you can
grep for, add a rule to that script rather than another paragraph here.

These guides cover *changing* baseUnits. For *using* it, see `README.md` and
`docs/`.

## Where things live (a map; the explanations are in the files)

- `src/baseUnits/_factors.py`: the only place a numeric conversion factor is
  written. Its docstring explains the four exact defining constants.
- `src/baseUnits/_make_system.py`: `make_system(length=, time=, force=|mass=)`,
  the factory that builds every system.
- `src/baseUnits/systems/<force>_<length>_<time>.py`: one `make_system` call
  per module, with a matching `.pyi`. `src/baseUnits/__init__.py` re-exports
  `N_mm_s`.
- `src/baseUnits/checked/`: the opt-in `Quantity`/`Unit`/`Dimension` layer. Its
  factors are derived from `_factors` through `checked/_derived.py`.
- `src/baseUnits/_unit_consts.pyi`, `__init__.pyi`, `systems/*.pyi`: generated
  by `scripts/gen_stubs.py`. Never hand-edit them.
- `docs/`: the published MkDocs site, for end users. `docs/systems.md` is not
  committed; `docs/scripts/gen_unit_tables.py` generates it at build time.
  `docs/architecture.md` explains the layers.
- `test/` (singular): `test_consistency.py` is "the one rule" (see
  `CONTRIBUTING.md`); `test_exact_factors.py` pins the factors.
- `docs/agent-surface.md`: the plan doc for this file, the guides and the lint.
  It is excluded from the published site in `mkdocs.yml`.

## Build, test, lint: exact commands and traps

```bash
pip install -e .[dev]                        # docs extras: .[docs]
python -m pytest -q                          # CI: py 3.9 / 3.11 / 3.12
ruff check .                                 # CI
python scripts/check_quirk_patterns.py       # CI, last step
ruff format --check .                        # CONTRIBUTING requires it; CI does NOT run it
pyright                                      # configured in pyproject (src + test); CI does NOT run it
PYTHONPATH=src mkdocs build --strict -d <tmp-dir>   # docs; CI builds only on push to main
```

1. **pytest imports the installed `baseUnits`, which may not be this
   checkout.** This is a src-layout package. If another clone is installed in
   editable mode, `pytest` quietly tests that clone instead. Run
   `python -c "import baseUnits; print(baseUnits.__file__)"` first. In a
   worktree, use `PYTHONPATH=src python -m pytest -q`. See the lesson
   "pytest may be testing another checkout".
2. **ruff versions disagree** (see the lesson of that name). Do not reformat
   files your change does not touch.
3. **Python floor.** `requires-python` is `>=3.8`, ruff targets py39, and CI's
   oldest Python is 3.9. A downstream cluster install runs 3.10. Use
   `from __future__ import annotations` if you write `X | None`, and do not
   use `match`.
4. **Docs deploy only after merge.** `docs.yml` runs `mkdocs gh-deploy` on
   every push to `main`, so a broken docs build shows up after the merge. If
   you touched `docs/`, `mkdocs.yml`, `gen_unit_tables.py` or a system, build
   locally with `--strict`. Never edit the `gh-pages` branch by hand.

## Rules that cost real time when broken

1. **`_factors.py` is the only place a factor is written.** The checked layer
   derives its factors (`_F = factors("FORCE", "N")`, then `factor=_F["lbf"]`)
   and never holds its own literal. `test_checked_layer_matches_float_layer`
   enforces this. See the lesson "Factor drift between the float and checked
   layers".
2. **Every value in `_factors.py` is the correctly rounded double of its exact
   definition.** Compute it with `decimal.Decimal`, as `test/test_exact_factors.py`
   does, and cite the source in the PR (the PR template asks for it). Do not
   "simplify" these literals.
3. **Keep the one rule green:** `test/test_consistency.py` must pass. Never
   skip or loosen it (`CONTRIBUTING.md`, "The one rule").
4. **Regenerate the stubs; do not edit them.** Whenever a unit name or a system
   is added or removed, run `PYTHONPATH=src python scripts/gen_stubs.py` from
   the repo root. It writes the `.pyi` files and reads the system list from its
   own `SYSTEMS`.
5. **Record every user-visible change in `CHANGELOG.md` under
   `## [Unreleased]`,** and never edit a released section. See the lesson
   "CHANGELOG entries get skipped".

## Cross-repo contract: what downstream relies on

Verified 2026-09-25 by reading each consumer read-only. Runtime dependents are
apeSteel, apeConcrete and apeETABS; apeRobot declares the dependency but never
imports it. apeRevit (C#) hard-codes numbers that baseUnits printed. apeGmsh
scripts, ConstitutiveRelationships and several notebooks import it without
declaring it. None of them imports `_factors` or `_make_system`, so those stay
private.

- **Plain floats in N-mm-tonne-s at the top level.** `mm == N == tonne == s ==
  MPa == 1.0` and `m == kN == 1000.0`. apeSteel and apeConcrete both assert
  this at import time (`src/<pkg>/core/units.py`).
- **`BASE == "N-mm-tonne-s"`.** apeSteel raises `AssertionError` otherwise.
  Importing a `baseUnits.systems.*` module must never change the top-level
  default.
- **`g == 9806.65` (mm/s²).** apeSteel computes self-weight with it and pins
  it in `tests/unit/test_aisc_v16_catalog.py`.
- **Full-precision factors.**
  - apeSteel's `tests/test_smoke.py` pins `ksi` to 6.894757293168 at
    `rel_tol=1e-9`.
  - apeConcrete checks `inches`, `lbf`, `kip`, `ksi` and `kgf_cm2` against
    NIST to 0.1%.
  - apeRevit's `LoadUnitsTests.cs` holds three `kN_m_s` ratios that baseUnits
    printed.
- **Unit names and system module names are public API.** Consumers import
  names such as `mm, cm, m, inches, ft, N, kN, MN, kgf, tf, lbf, kip, kg,
  tonne, gram, s, Pa, kPa, MPa, GPa, ksi, psi, kgf_cm2, radian, rad, degree,
  g, BASE`. Their code and docs name `systems.kN_m_s`, `N_m_s`, `N_mm_s`,
  `kgf_m_s` and `tf_m_s`. Renaming any of these breaks them; `d1a655f` renamed
  every system module once.
- **`baseUnits.checked` units are `Unit` objects** with a numeric `.factor`
  and no `__float__`. apeETABS and apeConcrete read `.factor`.
- **A merge reaches consumers on their next install.** apeSteel and
  apeConcrete declare `baseUnits @ git+https://github.com/nmorabowen/baseUnits.git`
  with no ref; apeETABS and apeRobot declare bare `baseUnits`. The ape-setup
  venv lock pins one commit (`7bd4c8f` as of 2026-09-25, which predates the
  #4 factor fix), so the office environments get a fix only when that lock is
  bumped. Nothing has been released: there are no tags and nothing on PyPI.
  `pyproject.toml` says `1.1.0`, and the CHANGELOG keeps every change under
  `Unreleased`. PR #8 folded the never-released `2.0.0` section into it.
- **Before merging a change to a value or a name,** run the consumers' test
  suites, as PR #4 did (apeSteel, apeETABS, apeConcrete), and report the
  results in the PR.

## Lessons (the archive: guides point here; add new entries at the end)

### Factor drift between the float and checked layers

- **What happened.** Until PR #4 (`a74e3ac`, 2026-08-03), `baseUnits.checked`
  kept its own hand-typed factors. They were four significant figures
  (`lbf = 4.448`, `ksi = 6.895`, `kgf = 9.807`) while `_factors.py` held exact
  values: a ~1e-4 error, enough to move an ACI/AISC capacity check. It was
  also missing `psi`.
- **The fix.** `checked/_derived.py` now derives every checked factor, and
  `test_checked_layer_matches_float_layer` compares every unit in every
  dimension. Run on the pre-fix tree (`9b869e7`), that test fails six of its
  eleven dimensions.
- **More detail:** `CHANGELOG.md` "Unreleased" and the `_factors.py`
  docstring.

### Adding a system: the registration sites drift

Several files name each system. The guide `baseunits-new-system` has the full
checklist.

- **The history.** At `862b7e0`, 8 system modules existed, but `README.md`
  listed 4 and the package docstring listed 3. `d1a655f` fixed both lists.
  `docs/architecture.md` kept its own list of 4 systems. Every commit that
  added a system missed it: `49d93d7`, `6a4e4a6`, `47b6682`, and PR #3
  (`ab8189a`), whose own description said "Registered in every place existing
  systems are listed". PR #6 replaces that list with a pointer to the
  generated Systems page.
- **The rule.** Do not add another hand-maintained list of systems to a
  document. Point to the Systems page instead, which
  `docs/scripts/gen_unit_tables.py` generates.
- **Enforcement.** Rule Q1 of `scripts/check_quirk_patterns.py` checks the four
  lists that must stay hand-maintained:
  - `SYSTEMS` in `test/test_consistency.py`
  - `SYSTEMS` in `docs/scripts/gen_unit_tables.py`
  - the package docstring
  - the README "Available systems" list

  A missing `NATURAL_BASES` entry already fails pytest with a `KeyError`.

### CHANGELOG entries get skipped

`CONTRIBUTING.md` and the PR template have required an `Unreleased` entry since
`d9b230a` (2026-05-06). Of the 9 commits that changed `src/` after that, only
`a74e3ac` added one. `d1a655f` rewrote the `[2.0.0]` section instead. That
section was never released, and PR #8 folded it into `Unreleased`. As a result, the CHANGELOG never mentions `kgf_m_s`, `dyne_cm_s`,
`tf_m_s` or the type stubs. This is not linted, because it depends on the diff
and has no fix commit to test against.

### ruff versions disagree

- **Three different versions.** `.pre-commit-config.yaml` pins ruff `v0.7.4`,
  the `[dev]` extra allows `ruff>=0.6`, and CI installs the latest.
- **They format differently.** Measured 2026-09-25 on `main`:
  - ruff 0.15.10 would reformat `scripts/gen_stubs.py`.
  - ruff 0.16.8 would also reformat `README.md`, because it formats the
    Python code blocks inside Markdown.
- **It has already cost a commit.** PR #4 needed the fix-up commit `b87f29d`
  after a format miss.
- **What to do.** Format only the files you change, and say in the PR which
  ruff version you used. Whether to pin one version is the owner's decision
  (see `docs/agent-surface.md`).

### pytest may be testing another checkout

On 2026-09-25, the machine's global Python had `baseUnits` installed in
editable mode from an older clone (at `9b869e7`, before the #4 factor fix). So
`pytest` run from a worktree imported that clone. apeGmsh has a doctor check,
D6, for the same kind of problem: separate interpreters holding different
baseUnits installs. Always print `baseUnits.__file__` before trusting a test
run.

### Compare factors with a tolerance, not ==

Depending on the order of operations, `psi` in N-mm-tonne-s comes out either
`0.006894757293168362` (from the `_factors` division) or `...361` (from
`lbf/inches**2`). Both are correct. Compare derived factors with
`rel_tol` around 1e-15. Only `test_exact_factors.py` uses `==`, and it does so
deliberately, against Decimal-derived, correctly rounded doubles. (PR #4.)

### Density in kN-m-s is tonne-based

In `kN_m_s` the mass base is the tonne, so a density of 2300 kg/m³ must be
written `2300*kg/m**3` (or `2.3*tonne/m**3`). A downstream notebook's
reference wrote `2.3*kg/m**3` and came out 1000× too light. (Recorded in
apeGmsh work, 2026-06.)

## Docs by audience

- `README.md` and `docs/` are for end users. They are published, so never
  document internals there.
- `CONTRIBUTING.md` is for human contributors. Its "Adding a new unit" and
  "Adding a new system" step lists are incomplete; the guides above have the
  full lists.
- `AGENTS.md` and `.claude/skills/` are for agents changing the code.
  `.claude/` is otherwise session scratch (ignored), which includes
  `.claude/worktrees/`.

## PRs and branches

- **Follow `CONTRIBUTING.md`.**
  - Branch from `main` and open PRs against `main`. See the global note on the
    stacked-PR `--base` pitfall.
  - Make one logical change per PR, fill in `.github/PULL_REQUEST_TEMPLATE.md`,
    keep pytest and ruff clean, add a CHANGELOG entry, and update the docs if
    the public API changed.
  - No emojis in code, comments, commits or docs.
- **Work in a worktree, not the shared checkout:**
  `git worktree add .claude/worktrees/<name> -b <branch> origin/main`.
- **Never push to `main` or `gh-pages` directly,** and never auto-merge. The
  owner merges.
