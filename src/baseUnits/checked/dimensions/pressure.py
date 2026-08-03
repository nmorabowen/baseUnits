"""
Defines all Pressure units.
Dimension: Mass / (Length * Time^2)
Base Unit: MPa (which is N/mm^2)

Factors come from ``baseUnits._factors`` so this layer cannot drift away from
the float layer; see :mod:`baseUnits.checked._derived`.
"""

# Import the base Unit class
# Import the Dimension helper class
from .._derived import factors
from ..dimension import Dimension
from ..units import Unit, register_base_unit

# 1. Define the compound dimension for Pressure
#    Pressure = Force / Length^2 = (Mass * Length / Time^2) / Length^2
PRESSURE_DIMENSION = Dimension("Mass") / (Dimension("Length") * (Dimension("Time") ** 2))

_F = factors("PRESSURE", "MPa")

# 2. Define the base unit for this dimension
#    Base unit is N/mm^2 = MPa
MPa = register_base_unit(
    Unit(name="MegaPascal", symbol="MPa", dimension=PRESSURE_DIMENSION, factor=_F["MPa"])
)

# 3. Define other Pressure units relative to the base (MPa)
Pa = Unit(name="Pascal", symbol="Pa", dimension=PRESSURE_DIMENSION, factor=_F["Pa"])
kPa = Unit(name="kiloPascal", symbol="kPa", dimension=PRESSURE_DIMENSION, factor=_F["kPa"])
GPa = Unit(name="GigaPascal", symbol="GPa", dimension=PRESSURE_DIMENSION, factor=_F["GPa"])
kgf_cm2 = Unit(
    name="kg-force-per-sq-cm", symbol="kgf/cm²", dimension=PRESSURE_DIMENSION, factor=_F["kgf_cm2"]
)
bar = Unit(name="bar", symbol="bar", dimension=PRESSURE_DIMENSION, factor=_F["bar"])
atm = Unit(name="atmosphere", symbol="atm", dimension=PRESSURE_DIMENSION, factor=_F["atm"])

# 4. Imperial units
ksi = Unit(name="kip-per-sq-inch", symbol="ksi", dimension=PRESSURE_DIMENSION, factor=_F["ksi"])
psi = Unit(name="pound-per-sq-inch", symbol="psi", dimension=PRESSURE_DIMENSION, factor=_F["psi"])
