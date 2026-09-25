# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added

- `psi`, `bar`, `atm`, `lb_per_ft3`, and `rad` to `baseUnits.checked`, which had
  fallen behind the float layer's unit list. `psi` matters for ACI 318 work.
- `test/test_exact_factors.py`, pinning every inch-pound and gravitational
  factor to a `Decimal` recomputation from the four exact defining constants
  (1 in = 25.4 mm, 1 lb = 0.45359237 kg, g0 = 9.80665 m/s², 1 lbf = lb·g0), and
  asserting the checked layer matches the float layer for every unit.

### Changed

- `baseUnits.checked` now derives its conversion factors from `_factors.py`
  instead of hard-coding its own copies. The duplicated copies had drifted to
  four significant figures (`lbf = 4.448`, `kip = 4448.0`, `ksi = 6.895`,
  `kgf_cm2 = 0.09807`, `kgf = 9.807`, `lb = 453.6e-6`), a ~1e-4 relative error
  large enough to move a design-code capacity check. Anyone importing from
  `baseUnits.checked` sees corrected values; the float layer is unaffected.
- `ksi`, `psi`, and `lb_per_ft3` in `_factors.py` were truncated a few digits
  short of the nearest double and are now correctly rounded (relative
  corrections of 5e-14, 5e-14, and 2e-12).
- `docs/architecture.md` now points to the generated Systems page instead of
  keeping its own list, which named only four of the seven pre-built systems
  (`kgf_m_s`, `tf_m_s`, and `dyne_cm_s` were missing).

### Removed

-

## [2.0.0] - 2025-05-04

### Added

- Float-based unit system at the default import path. `baseUnits.<system>` now
  exposes plain floats whose values are conversion factors relative to the
  chosen base.
- `_factors.py` providing the single source of truth for absolute SI factors
  per dimension.
- `make_system` helper for assembling systems from any combination of base
  units.
- Pre-built systems under `baseUnits.systems`: `N_mm_s`, `N_m_s`, `kN_m_s`, `kip_in_s`.
- Missing temperature unit `K` now exported alongside the other base units.

### Changed

- The dimensional-checking `Quantity`, `Unit`, and `Dimension` types moved
  under `baseUnits.checked`. The default path is now zero-overhead.

### Removed

- Implicit `Quantity` wrapping at module top level. Use `baseUnits.checked`
  for dimensional verification.
