# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added

-

### Changed

-

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
- Pre-built systems under `baseUnits.systems`: `N_mm`, `N_m`, `kN_m`, `kip_in`.
- Missing temperature unit `K` now exported alongside the other base units.

### Changed

- The dimensional-checking `Quantity`, `Unit`, and `Dimension` types moved
  under `baseUnits.checked`. The default path is now zero-overhead.

### Removed

- Implicit `Quantity` wrapping at module top level. Use `baseUnits.checked`
  for dimensional verification.
