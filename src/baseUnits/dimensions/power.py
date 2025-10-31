"""
Defines all Power units.
Dimension: Mass * Length^2 / Time^3
Base Unit: mJ/s (which is N*mm/s)
"""
# Import the base Unit class
from ..units import Unit, register_base_unit
# Import the Dimension helper class
from ..dimension import Dimension

# 1. Define the compound dimension for Power
#    Power = Energy / Time = (Mass * Length^2 / Time^2) / Time
POWER_DIMENSION = Dimension("Mass") * (Dimension("Length") ** 2) / (Dimension("Time") ** 3)

# 2. Define the base unit for this dimension
#    Base unit is mJ/s
mJ_s = register_base_unit(
    Unit(name="milliJoule-per-second", symbol="mJ/s", dimension=POWER_DIMENSION, factor=1.0)
)

# 3. Define other Power units relative to the base (mJ/s)
W = Unit(name="Watt", symbol="W", dimension=POWER_DIMENSION, factor=1000.0)
kW = Unit(name="kiloWatt", symbol="kW", dimension=POWER_DIMENSION, factor=1e6)
MW = Unit(name="MegaWatt", symbol="MW", dimension=POWER_DIMENSION, factor=1e9)
HP = Unit(name="Horsepower", symbol="HP", dimension=POWER_DIMENSION, factor=745700.0)