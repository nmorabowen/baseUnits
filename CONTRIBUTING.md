# Contributing to baseUnits

Thanks for your interest in contributing. This guide covers the practical workflow.

## Quickstart

```bash
git clone https://github.com/nmorabowen/baseUnits.git
cd baseUnits
pip install -e .[dev]
pytest
```

## Adding a new unit

1. Open `src/baseUnits/_factors.py`.
2. Add an entry to the appropriate dimension dict, with the value expressed as the
   absolute SI factor (i.e., the multiplier that converts one unit of the new
   quantity to the SI base unit of that dimension).
3. Cite an authoritative source for the conversion factor (NIST SP 811, ISO 80000,
   or a recognized engineering reference) in the pull request description.
4. Run `pytest`. The new unit appears automatically in every pre-built system, and
   the consistency tests will catch any factor mistakes.

## Adding a new system

1. Create `src/baseUnits/systems/<name>.py` following the pattern of
   `src/baseUnits/systems/N_mm.py`. The file should make a single call to
   `make_system` with the desired base units.
2. Add the new system to the parametrized `SYSTEMS` list in
   `test/test_consistency.py` so it is exercised by the cross-system invariants.
3. Run `pytest`.

## The one rule

Every change must keep `test/test_consistency.py` green. That test enforces
F = m * a and the unit-table invariant across all systems. Do not skip or
suppress it; if it fails, fix the underlying factor.

## Style

- `ruff` is the formatter and linter.
- Run `ruff check .` and `ruff format .` before submitting.
- No emojis in code, comments, commits, or docs.

## Pull request workflow

1. Branch from `main`. One logical change per PR.
2. If your change addresses an issue, link it in the description.
3. Fill in the PR template.
4. Confirm `pytest` passes locally and `ruff check .` / `ruff format .` are clean.
5. Update `CHANGELOG.md` under the `Unreleased` section.
6. Update docs if the public API changed.

## Reporting bugs

Open an issue using the `Bug report` template. Please include a minimal
reproducer, expected vs. actual behavior, and your environment (Python
version, baseUnits version, OS).
