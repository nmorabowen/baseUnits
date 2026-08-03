"""
Defines all Power units.
Dimension: Mass * Length^2 / Time^3
Base Unit: mJ/s (which is N*mm/s)

Factors come from ``baseUnits._factors`` so this layer cannot drift away from
the float layer; see :mod:`baseUnits.checked._derived`.
"""

# Import the base Unit class
# Import the Dimension helper class
from .._derived import factors
from ..dimension import Dimension
from ..units import Unit, register_base_unit

# 1. Define the compound dimension for Power
#    Power = Energy / Time = (Mass * Length^2 / Time^2) / Time
POWER_DIMENSION = Dimension("Mass") * (Dimension("Length") ** 2) / (Dimension("Time") ** 3)

_F = factors("POWER", "mJ_s")

# 2. Define the base unit for this dimension
#    Base unit is mJ/s
mJ_s = register_base_unit(
    Unit(name="milliJoule-per-second", symbol="mJ/s", dimension=POWER_DIMENSION, factor=_F["mJ_s"])
)

# 3. Define other Power units relative to the base (mJ/s)
W = Unit(name="Watt", symbol="W", dimension=POWER_DIMENSION, factor=_F["W"])
kW = Unit(name="kiloWatt", symbol="kW", dimension=POWER_DIMENSION, factor=_F["kW"])
MW = Unit(name="MegaWatt", symbol="MW", dimension=POWER_DIMENSION, factor=_F["MW"])
HP = Unit(name="Horsepower", symbol="HP", dimension=POWER_DIMENSION, factor=_F["HP"])
