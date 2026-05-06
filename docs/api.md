# API reference

## Top-level package

::: baseUnits
    options:
      show_source: false
      members: false

## `make_system`

::: baseUnits._make_system.make_system

## Factor dictionaries

The single source of truth for absolute SI values.

::: baseUnits._factors
    options:
      show_source: false
      members: false

The module exposes one `dict` per dimension: `LENGTH`, `FORCE`, `MASS`,
`TIME`, `PRESSURE`, `ENERGY`, `POWER`, `DENSITY`, `UNIT_WEIGHT`, `ANGLE`,
`TEMPERATURE`. Each maps a Python identifier to the unit's absolute SI
value.

## Checked layer

::: baseUnits.checked
    options:
      show_source: false
      members: false

### `Quantity`

::: baseUnits.checked.quantity.Quantity
    options:
      show_source: false
      members_order: source

### `Unit`

::: baseUnits.checked.units.Unit
    options:
      show_source: false
      members_order: source

### `Dimension`

::: baseUnits.checked.dimension.Dimension
    options:
      show_source: false
      members_order: source

### Helpers

::: baseUnits.checked.units.register_base_unit

::: baseUnits.checked.units.get_base_unit
