"""
Defines all Power units.

The base unit for Power in a (N, mm, s) system is (N*mm / s),
which is equivalent to 'mJ/s' (milliJoule-per-second).

This file defines the Power dimension as Force * Length / Time.
"""

# Import the base Unit class
from ..units import Unit, register_base_unit
# Import the Dimension helper class
from ..dimension import Dimension

# 1. Define the compound dimension for Power
POWER_DIMENSION = (Dimension("Force") * Dimension("Length")) / Dimension("Time")

# 2. Define the base unit for this dimension
#    Base unit is (N * mm / s) = mJ/s
mJ_s = register_base_unit(
    Unit(name="milliJJoule-per-second", symbol="mJ/s", dimension=POWER_DIMENSION, factor=1.0)
)

# 3. Define other Power units relative to the base (mJ/s)
W = Unit(name="Watt", symbol="W", dimension=POWER_DIMENSION, factor=1000.0)
kW = Unit(name="kiloWatt", symbol="kW", dimension=POWER_DIMENSION, factor=1e6)
MW = Unit(name="MegaWatt", symbol="MW", dimension=POWER_DIMENSION, factor=1e9)
HP = Unit(name="Horsepower", symbol="HP", dimension=POWER_DIMENSION, factor=745700.0)