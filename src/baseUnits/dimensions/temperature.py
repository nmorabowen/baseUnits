"""
Defines all Temperature units.

NOTE: Absolute temperature conversions (e.g., C -> F) involve
offsets, not just multiplicative factors. Our current Unit/Quantity
system is factor-based (e.g., 1 m = 1000 * 1 mm).

Therefore, these units are defined to represent
**temperature differences (deltas)**.

The base unit for Temperature is 'K' (Kelvin), as a 1 K
change is the standard SI unit for temperature difference.
"""

# Import the base Unit class from the 'units.py' file (one level up)
from ..units import Unit, register_base_unit

# A 1-degree Celsius *change* is equal to a 1-degree Kelvin *change*.
C = register_base_unit(
    Unit(name="Celsius", symbol="°C", dimension="Temperature", factor=1.0)
)

# A 1-degree Fahrenheit *change* is equal to a (5/9) Kelvin *change*.
F = Unit(name="Fahrenheit", symbol="°F", dimension="Temperature", factor=(5.0/9.0))