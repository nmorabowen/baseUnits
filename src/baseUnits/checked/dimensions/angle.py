"""
Defines all Angle units.

The base unit for Angle is 'radian', so all conversion
factors are relative to 'radian'.

Factors come from ``baseUnits._factors`` so this layer cannot drift away from
the float layer; see :mod:`baseUnits.checked._derived`.
"""

# Import the base Unit class from the 'units.py' file (one level up)
from .._derived import factors
from ..units import Unit, register_base_unit

_F = factors("ANGLE", "radian")

# 1. Define the base unit for this dimension
radian = register_base_unit(
    Unit(name="radian", symbol="rad", dimension="Angle", factor=_F["radian"])
)

# 2. Define other Angle units relative to the base (radian)
degree = Unit(name="degree", symbol="°", dimension="Angle", factor=_F["degree"])

# 3. Short alias, matching the float layer
rad = radian
