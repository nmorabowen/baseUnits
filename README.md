# baseUnits

A Python package for unit-aware physical calculations that ensures dimensional safety.

This library is built on a "consistent unit system" to prevent common errors in physical calculations (like adding mass to length). By wrapping values in a `Quantity` object, `baseUnits` can check the dimensions of all arithmetic operations at runtime.

The default consistent system is based on:
* **Length:** `mm` (millimeter)
* **Force:** `N` (Newton)
* **Mass:** `tonne` (1000 kg)
* **Time:** `s` (second)
* **Pressure:** `MPa` (MegaPascal, which is N/mm²)
* **Energy:** `mJ` (milliJoule, which is N*mm)

All other units are defined by their conversion factor to this base system.

## Installation

For development, clone the repository and install in editable mode:

```bash
git clone [https://github.com/nmorabowen/baseUnits.git](https://github.com/nmorabowen/baseUnits.git)
cd baseUnits
pip install -e .