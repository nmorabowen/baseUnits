"""
Defines all Unit Weight (or Specific Weight) units.
Dimension: Force / Length^3  (which is Mass / (Length^2 * Time^2))
Base Unit: N / mm^3
"""
from ..units import Unit, register_base_unit
from ..dimension import Dimension

# 1. Define the compound dimension for Unit Weight
#    Force / Length^3 = (Mass * Length / Time^2) / Length^3
UNIT_WEIGHT_DIMENSION = Dimension("Mass") / ((Dimension("Length") ** 2) * (Dimension("Time") ** 2))

# 2. Define and register the base unit for this dimension
#    Base Force = N
#    Base Length = mm
#    Base Unit = N / mm^3
N_per_mm3 = register_base_unit(
    Unit(name="Newton per cubic millimeter", symbol="N/mm³", dimension=UNIT_WEIGHT_DIMENSION, factor=1.0)
)

# 3. Define other common Unit Weight units
#    1 N/m^3 = (1 N) / ( (1e3 mm)^3 ) = 1 / 1e9 = 1e-9 N/mm³
N_per_m3 = Unit(name="Newton per cubic meter", symbol="N/m³", dimension=UNIT_WEIGHT_DIMENSION, factor=1e-9)

#    1 kN/m^3 = (1e3 N) / ( (1e3 mm)^3 ) = 1e3 / 1e9 = 1e-6 N/mm³
kN_per_m3 = Unit(name="kiloNewton per cubic meter", symbol="kN/m³", dimension=UNIT_WEIGHT_DIMENSION, factor=1e-6)

#    1 kgf/m^3 = (9.807 N) / ( (1e3 mm)^3 ) = 9.807 / 1e9 = 9.807e-9 N/mm³
kgf_per_m3 = Unit(name="kg-force per cubic meter", symbol="kgf/m³", dimension=UNIT_WEIGHT_DIMENSION, factor=9.807e-9)