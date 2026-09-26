---
name: baseunits-change-factors
description: >
  Checklist for adding a unit to the baseUnits repo, changing a conversion
  factor value (src/baseUnits/_factors.py: LENGTH, FORCE, MASS, PRESSURE, ksi,
  psi, lbf, kip, kgf, ...), or editing the opt-in checked layer
  (src/baseUnits/checked/: Unit, Quantity, Dimension, _derived.factors). Use it
  before touching any numeric factor, adding a unit name, or changing what
  baseUnits.checked exposes. Downstream design libraries (apeSteel, apeConcrete,
  apeETABS) depend on these exact numbers. Each item points to the AGENTS.md
  lesson that explains it. It is for changing baseUnits, not for using it.
---

# New unit, changed factor, or checked-layer change: checklist

Read this before adding a unit, changing a factor, or editing
`src/baseUnits/checked/`. Each item names the `AGENTS.md` heading to grep for;
read that entry when the item applies. None of these items is linted: the
tests named below are what enforce them.

## The value (`src/baseUnits/_factors.py`)

- [ ] `_factors.py` is the ONLY place the number is written: AGENTS.md rule 1,
      and the lesson "Factor drift between the float and checked layers".
      Never type a factor into `checked/` or a system module.
- [ ] The value must be the correctly rounded double of the exact
      definition. Derive it with `decimal.Decimal` from the four constants in
      the `_factors.py` docstring (inch, pound, g0, lbf). Do not use a
      handbook rounding. See AGENTS.md rule 2.
- [ ] If the unit descends from in/lb/g0, add it to `EXACT_FACTORS` in
      `test/test_exact_factors.py`. If it is a kilo-pair or a force-over-area
      identity, extend the identity tests there too. Encode the definition,
      not a copy of your literal.
- [ ] The name must be a valid identifier that collides with nothing already
      in the namespace (`g`, `BASE`, other dimensions' keys). Every system
      exposes it at top level.
- [ ] Cite the source (NIST SP 811, ISO 80000, ...) in the PR. The template
      section "Source for any new conversion factors" asks for it.

## Everything that must follow a new or renamed unit

- [ ] Checked layer: in `checked/dimensions/<dim>.py`, add
      `x = Unit(..., factor=_F["x"])`, and add `"x"` to `checked/__init__.py`
      `__all__`. `test_checked_layer_matches_float_layer` fails until you do.
      The checked layer had silently fallen behind before: PR #4 found it
      missing `psi`, `bar`, `atm`, `lb_per_ft3` and `rad`. CONTRIBUTING's
      "Adding a new unit" does not mention this step.
- [ ] Stubs: run `PYTHONPATH=src python scripts/gen_stubs.py` (AGENTS.md
      rule 4). Nothing fails if you skip it; editors and type checkers just
      stop seeing the name.
- [ ] A new *dimension* dict also needs its handling in `make_system`, a
      checked dimension module, `CHECKED_BASES` in `test_exact_factors.py`,
      and `_bases` in `test_consistency.py`.

## Changing an existing value

- [ ] It changes numbers in every consumer on their next install, with no
      version gate. Read AGENTS.md "Cross-repo contract: what downstream relies
      on":
      - apeSteel pins `ksi` at `rel_tol=1e-9`.
      - apeConcrete asserts the base values at import time.
      - apeRevit hard-codes three `kN_m_s` ratios.
- [ ] Run the consumers' suites (apeSteel, apeETABS, apeConcrete), as PR #4
      did, and put the results in the PR body. Grep the consumers for the old
      literal.
- [ ] Compare with `rel_tol` around 1e-15, never `==`, except in the
      Decimal-derived exact pins. See AGENTS.md "Compare factors with a
      tolerance, not ==".
- [ ] Removing or renaming a unit breaks consumers' imports. The used names
      are listed in the contract section.

## The checked layer (`src/baseUnits/checked/`)

- [ ] Its base system is N-mm-tonne-s, one base unit per dimension
      (`CHECKED_BASES` in `test_exact_factors.py`). Consumers (apeETABS,
      apeConcrete) read `Unit.factor` and rely on `Unit` having no
      `__float__`. Keep both.
- [ ] Do not register a second base unit for a dimension: `register_base_unit`
      raises on it.

## Before the PR

- [ ] `CHANGELOG.md`: add an entry under `## [Unreleased]`, stating the old
      value, the new value and the relative change, as PR #4 did. AGENTS.md
      "CHANGELOG entries get skipped".
- [ ] Run `python -m pytest -q`, `ruff check .`, and
      `python scripts/check_quirk_patterns.py`. Check first that pytest is
      testing this checkout (AGENTS.md "pytest may be testing another
      checkout").
- [ ] Format only the files you changed (AGENTS.md "ruff versions disagree").

Found a new trap? Add a lesson to `AGENTS.md`, then add one line here that
points to it. If the trap has a pattern you can grep for, add a rule to
`scripts/check_quirk_patterns.py` instead.
