"""
Defines all Density units.
Dimension: Mass / Length^3
Base Unit: tonne / mm^3

Factors come from ``baseUnits._factors`` so this layer cannot drift away from
the float layer; see :mod:`baseUnits.checked._derived`.
"""

from .._derived import factors
from ..dimension import Dimension
from ..units import Unit, register_base_unit

# 1. Define the compound dimension for Density
DENSITY_DIMENSION = Dimension("Mass") / (Dimension("Length") ** 3)

_F = factors("DENSITY", "tonne_per_mm3")

# 2. Define and register the base unit for this dimension
tonne_per_mm3 = register_base_unit(
    Unit(
        name="tonne per cubic millimeter",
        symbol="tonne/mm³",
        dimension=DENSITY_DIMENSION,
        factor=_F["tonne_per_mm3"],
    )
)

# 3. Define other common Density units
#    1 kg/m^3 = (1e-3 tonne) / ( (1e3 mm)^3 ) = (1e-3) / (1e9) = 1e-12 tonne/mm³
kg_per_m3 = Unit(
    name="kilogram per cubic meter",
    symbol="kg/m³",
    dimension=DENSITY_DIMENSION,
    factor=_F["kg_per_m3"],
)

#    1 gr/cm^3 = (1e-6 tonne) / ( (10 mm)^3 ) = (1e-6) / (1e3) = 1e-9 tonne/mm³
gr_per_cm3 = Unit(
    name="gram per cubic centimeter",
    symbol="gr/cm³",
    dimension=DENSITY_DIMENSION,
    factor=_F["gr_per_cm3"],
)

#    1 tonne/m^3 = (1 tonne) / ( (1e3 mm)^3 ) = 1 / 1e9 = 1e-9 tonne/mm³
tonne_per_m3 = Unit(
    name="tonne per cubic meter",
    symbol="tonne/m³",
    dimension=DENSITY_DIMENSION,
    factor=_F["tonne_per_m3"],
)

lb_per_ft3 = Unit(
    name="pound per cubic foot",
    symbol="lb/ft³",
    dimension=DENSITY_DIMENSION,
    factor=_F["lb_per_ft3"],
)
