"""
Defines all Angle units.

The base unit for Angle is 'radian', so all conversion
factors are relative to 'radian'.
"""

from math import pi
# Import the base Unit class from the 'units.py' file (one level up)
from ..units import Unit, register_base_unit

# 1. Define the base unit for this dimension
radian = register_base_unit(
    Unit(name="radian", symbol="rad", dimension="Angle", factor=1.0)
)

# 2. Define other Angle units relative to the base (radian)
degree = Unit(name="degree", symbol="°", dimension="Angle", factor=(pi / 180.0))