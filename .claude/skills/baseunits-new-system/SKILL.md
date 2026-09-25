---
name: baseunits-new-system
description: >
  Checklist for adding, renaming or removing a pre-built unit system in the
  baseUnits repo (src/baseUnits/systems/<force>_<length>_<time>.py, e.g. N_mm_s,
  kN_m_s, kip_in_s, kgf_m_s, tf_m_s, dyne_cm_s), or for changing which system is
  the top-level default. Use it before creating or editing a system module or
  calling make_system for a new system. It lists every place a system must be
  registered; each item points to the AGENTS.md lesson that explains it. It is
  for changing baseUnits, not for using it in another project.
---

# New, renamed or removed system: checklist

Read this before adding, renaming or removing a module under
`src/baseUnits/systems/`. Each item names the `AGENTS.md` heading to grep for;
read that entry when the item applies. Items marked **[lint]** are enforced by
`python scripts/check_quirk_patterns.py` (rule Q1). For why these lists
drift, see AGENTS.md "Adding a system: the registration sites drift".

## The module

- [ ] Name it `<force>_<length>_<time>` (`d1a655f` set this convention; its
      commit message explains why `mks` and `kg_cm_s` were dropped). Copy
      `systems/N_mm_s.py`: one `make_system` call, then
      `globals().update(...)`, `__all__`, and `del`.
- [ ] Pass every primitive you can name (`length`, `time`, `force`, and `mass`
      if the mass has a name in `_factors.MASS`). The factory then checks
      `F = M*L/T**2` for you. If the derived mass has no name, say so in a
      comment, as `tf_m_s.py` does.
- [ ] Do not make a new consistent system out of a `g = 1` shortcut. `g`
      stays physical (see the `tf_m_s.py` docstring).
- [ ] Is a new primitive needed? Then add the unit first, following
      `.claude/skills/baseunits-change-factors/SKILL.md`.

## Register it everywhere the systems are listed

- [ ] **[lint]** `test/test_consistency.py`: add a `SYSTEMS` row with exactly
      one of force or mass, matching your `make_system` call. Leave it out and
      the system escapes "the one rule".
- [ ] `test/test_consistency.py`: add a `NATURAL_BASES` entry, with `None`
      where the natural pressure, energy or power base has no name. Not
      linted: pytest already fails with a `KeyError` without it.
- [ ] **[lint]** `docs/scripts/gen_unit_tables.py`: add the module to
      `SYSTEMS` (module, label, prose). The published Systems page is
      generated from it at build time.
- [ ] **[lint]** `src/baseUnits/__init__.py`: the docstring paragraph that
      names the pre-built systems.
- [ ] **[lint]** `README.md`: the bullet list under "## Available systems".
- [ ] Stubs: add the name to `SYSTEMS` in `scripts/gen_stubs.py`, then run
      `PYTHONPATH=src python scripts/gen_stubs.py` from the repo root to write
      `systems/<name>.pyi` (AGENTS.md rule 4). Not linted: this has never been
      missed, and the script calls itself temporary tooling.
- [ ] `test/test_systems_parity.py`: one hand-written identity test for what
      makes the system distinctive (for example `test_tf_m_s_force_base`).
      Not linted, because it is not a list.
- [ ] Do not add the system to any other hand-written list. Point readers to
      the generated Systems page instead; `docs/architecture.md` does this
      since PR #6.

## Renaming or removing

- [ ] A system module name is public API. Consumers use these names:
      - `kN_m_s`: apeETABS, apeGmsh and apeRevit
      - `N_mm_s`, `kgf_m_s` and `tf_m_s`: apeRevit
      - `N_m_s`: OpenSees model scripts

      Read AGENTS.md
      "Cross-repo contract: what downstream relies on" before renaming or
      removing one, and grep the consumers.
- [ ] Update every site above. Delete the stale `.pyi`; `gen_stubs.py` does
      not remove files.
- [ ] Changing the top-level default (`N_mm_s`) breaks apeSteel and
      apeConcrete at import time (they assert `BASE` and `mm == 1.0`). Do not
      do it without a coordinated change downstream.

## Before the PR

- [ ] `CHANGELOG.md`: add an entry under `## [Unreleased]`, never in a
      released section. AGENTS.md "CHANGELOG entries get skipped": no system
      addition so far has recorded one.
- [ ] Run `python -m pytest -q`, `ruff check .`, and
      `python scripts/check_quirk_patterns.py`. Check first that pytest is
      testing this checkout (AGENTS.md "pytest may be testing another
      checkout").
- [ ] Run `PYTHONPATH=src mkdocs build --strict -d <tmp-dir>`. CI builds the
      docs only after the merge.

Found a new trap? Add a lesson to `AGENTS.md`, then add one line here that
points to it. If the trap has a pattern you can grep for, add a rule to
`scripts/check_quirk_patterns.py` instead.
