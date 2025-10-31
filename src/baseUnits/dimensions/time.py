"""
Defines all Time units.

The base unit for Time is 's' (second), so all conversion
factors are relative to 's'.
"""

# Import the base Unit class from the 'units.py' file (one level up)
from ..units import Unit, register_base_unit

# 1. Define the base unit for this dimension
s = register_base_unit(
    Unit(name="second", symbol="s", dimension="Time", factor=1.0)
)

# 2. Define other Time units relative to the base (s)
minutes = Unit(name="minute", symbol="min", dimension="Time", factor=60.0)
h = Unit(name="hour", symbol="h", dimension="Time", factor=3600.0)
day = Unit(name="day", symbol="day", dimension="Time", factor=86400.0) # 24 * 3600
week = Unit(name="week", symbol="week", dimension="Time", factor=604800.0) # 7 * 86400

# 3. Approximate and average units
month = Unit(name="month (approx)", symbol="month", dimension="Time", factor=2.592e6) # 30 * 86400
year = Unit(name="year (avg)", symbol="year", dimension="Time", factor=3.15576e7) # 365.25 * 86400