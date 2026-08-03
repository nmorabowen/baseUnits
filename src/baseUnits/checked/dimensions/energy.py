"""
Defines all Energy units.
Dimension: Mass * Length^2 / Time^2
Base Unit: mJ (which is N*mm)

Factors come from ``baseUnits._factors`` so this layer cannot drift away from
the float layer; see :mod:`baseUnits.checked._derived`.
"""

# Import the base Unit class
# Import the Dimension helper class
from .._derived import factors
from ..dimension import Dimension
from ..units import Unit, register_base_unit

# 1. Define the compound dimension for Energy
#    Energy = Force * Length = (Mass * Length / Time^2) * Length
ENERGY_DIMENSION = Dimension("Mass") * (Dimension("Length") ** 2) / (Dimension("Time") ** 2)

_F = factors("ENERGY", "mJ")

# 2. Define the base unit for this dimension
#    Base unit is N*mm = mJ
mJ = register_base_unit(
    Unit(name="milliJoule", symbol="mJ", dimension=ENERGY_DIMENSION, factor=_F["mJ"])
)

# 3. Define other Energy units relative to the base (mJ)
J = Unit(name="Joule", symbol="J", dimension=ENERGY_DIMENSION, factor=_F["J"])
kJ = Unit(name="kiloJoule", symbol="kJ", dimension=ENERGY_DIMENSION, factor=_F["kJ"])
cal = Unit(name="calorie", symbol="cal", dimension=ENERGY_DIMENSION, factor=_F["cal"])
kcal = Unit(name="kiloCalorie", symbol="kcal", dimension=ENERGY_DIMENSION, factor=_F["kcal"])
eV = Unit(name="electronVolt", symbol="eV", dimension=ENERGY_DIMENSION, factor=_F["eV"])
Wh = Unit(name="Watt-hour", symbol="Wh", dimension=ENERGY_DIMENSION, factor=_F["Wh"])
kWh = Unit(name="kilowatt-hour", symbol="kWh", dimension=ENERGY_DIMENSION, factor=_F["kWh"])
