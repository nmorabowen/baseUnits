"""
Defines all Energy units.

The base unit for Energy in a (N, mm) system is (N * mm),
which is equivalent to 'mJ' (milliJoule).

This file defines the Energy dimension as Force * Length.
"""

# Import the base Unit class
from ..units import Unit, register_base_unit
# Import the Dimension helper class
from ..dimension import Dimension

# 1. Define the compound dimension for Energy
ENERGY_DIMENSION = register_base_unit(
    Dimension("Force") * Dimension("Length")
)

# 2. Define the base unit for this dimension
#    Base unit is (N * mm) = mJ
mJ = Unit(name="milliJoule", symbol="mJ", dimension=ENERGY_DIMENSION, factor=1.0)

# 3. Define other Energy units relative to the base (mJ)
J = Unit(name="Joule", symbol="J", dimension=ENERGY_DIMENSION, factor=1000.0)
kJ = Unit(name="kiloJoule", symbol="kJ", dimension=ENERGY_DIMENSION, factor=1e6)
cal = Unit(name="calorie", symbol="cal", dimension=ENERGY_DIMENSION, factor=4184.0)
kcal = Unit(name="kiloCalorie", symbol="kcal", dimension=ENERGY_DIMENSION, factor=4.184e6)
eV = Unit(name="electronVolt", symbol="eV", dimension=ENERGY_DIMENSION, factor=1.60218e-16)
Wh = Unit(name="Watt-hour", symbol="Wh", dimension=ENERGY_DIMENSION, factor=3.6e6)
kWh = Unit(name="kilowatt-hour", symbol="kWh", dimension=ENERGY_DIMENSION, factor=3.6e9)