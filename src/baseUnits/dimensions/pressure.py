"""
Defines all Pressure units.

The base unit for Pressure in a (N, mm) system is (N / mm^2),
which is exactly equivalent to 'MPa' (MegaPascal).

This file defines the Pressure dimension as Force / Length^2.
"""

# Import the base Unit class
from ..units import Unit, register_base_unit
# Import the Dimension helper class
from ..dimension import Dimension

# 1. Define the compound dimension for Pressure
#    This is the key fix: Force / Length^2
PRESSURE_DIMENSION = Dimension("Force") / (Dimension("Length") ** 2)

# 2. Define the base unit for this dimension
#    Note: 'MPa' is (N / mm^2). Our base units are N and mm,
#    so the factor for MPa is 1.0.
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