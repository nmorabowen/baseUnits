"""
Defines all Pressure units.
Dimension: Mass / (Length * Time^2)
Base Unit: MPa (which is N/mm^2)
"""
# Import the base Unit class
from ..units import Unit, register_base_unit
# Import the Dimension helper class
from ..dimension import Dimension

# 1. Define the compound dimension for Pressure
#    Pressure = Force / Length^2 = (Mass * Length / Time^2) / Length^2
PRESSURE_DIMENSION = Dimension("Mass") / (Dimension("Length") * (Dimension("Time") ** 2))

# 2. Define the base unit for this dimension
#    Base unit is N/mm^2 = MPa
MPa = register_base_unit(
    Unit(name="MegaPascal", symbol="MPa", dimension=PRESSURE_DIMENSION, factor=1.0)
)

# 3. Define other Pressure units relative to the base (MPa)
Pa = Unit(name="Pascal", symbol="Pa", dimension=PRESSURE_DIMENSION, factor=1e-6)
kPa = Unit(name="kiloPascal", symbol="kPa", dimension=PRESSURE_DIMENSION, factor=1e-3)
GPa = Unit(name="GigaPascal", symbol="GPa", dimension=PRESSURE_DIMENSION, factor=1e3)
kgf_cm2 = Unit(name="kg-force-per-sq-cm", symbol="kgf/cm²", dimension=PRESSURE_DIMENSION, factor=0.09807)

# 4. Imperial units
ksi = Unit(name="kip-per-sq-inch", symbol="ksi", dimension=PRESSURE_DIMENSION, factor=6.895)