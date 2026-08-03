"""
Defines all Time units.

The base unit for Time is 's' (second), so all conversion
factors are relative to 's'.

Factors come from ``baseUnits._factors`` so this layer cannot drift away from
the float layer; see :mod:`baseUnits.checked._derived`.
"""

# Import the base Unit class from the 'units.py' file (one level up)
from .._derived import factors
from ..units import Unit, register_base_unit

_F = factors("TIME", "s")

# 1. Define the base unit for this dimension
s = register_base_unit(Unit(name="second", symbol="s", dimension="Time", factor=_F["s"]))

# 2. Define other Time units relative to the base (s)
minutes = Unit(name="minute", symbol="min", dimension="Time", factor=_F["minutes"])
h = Unit(name="hour", symbol="h", dimension="Time", factor=_F["h"])
day = Unit(name="day", symbol="day", dimension="Time", factor=_F["day"])  # 24 * 3600
week = Unit(name="week", symbol="week", dimension="Time", factor=_F["week"])  # 7 * 86400

# 3. Approximate and average units
month = Unit(name="month (approx)", symbol="month", dimension="Time", factor=_F["month"])  # 30 days
year = Unit(name="year (avg)", symbol="year", dimension="Time", factor=_F["year"])  # 365.25 days
