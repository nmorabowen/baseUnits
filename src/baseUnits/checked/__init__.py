"""Opt-in dimensional safety layer with Quantity/Unit/Dimension objects.

Use this layer during development, validation, or unit tests where catching a
dimensional bug is worth the wrapper-object overhead. For high-performance
numerical work (numpy, pandas, matplotlib, FEM solvers) prefer the float
constants from ``baseUnits`` directly: ``Quantity`` does not interoperate with
those libraries.

Example:
    >>> from baseUnits.checked import m, kg
    >>> (10 * m) + (5 * kg)
    Traceback (most recent call last):
        ...
    TypeError: ...
"""

from .dimension import Dimension
from .dimensions.angle import *
from .dimensions.density import *
from .dimensions.energy import *
from .dimensions.force import *
from .dimensions.length import *
from .dimensions.mass import *
from .dimensions.power import *
from .dimensions.pressure import *
from .dimensions.temperature import *
from .dimensions.time import *
from .dimensions.unit_weight import *
from .quantity import Quantity
from .units import Unit, get_base_unit, register_base_unit

__all__ = [
    "Unit",
    "Quantity",
    "Dimension",
    "register_base_unit",
    "get_base_unit",
    # Length
    "mm",
    "cm",
    "m",
    "km",
    "inches",
    "ft",
    "yard",
    "mile",
    # Force
    "N",
    "kN",
    "MN",
    "dyne",
    "kgf",
    "tf",
    "lbf",
    "kip",
    # Mass
    "tonne",
    "kg",
    "gr",
    "gram",
    "mg",
    "lb",
    "oz",
    # Pressure
    "MPa",
    "kPa",
    "GPa",
    "kgf_cm2",
    "Pa",
    "ksi",
    # Energy
    "J",
    "kJ",
    "mJ",
    "cal",
    "kcal",
    "eV",
    "Wh",
    "kWh",
    # Power
    "W",
    "kW",
    "MW",
    "HP",
    "mJ_s",
    # Time
    "s",
    "minutes",
    "h",
    "day",
    "week",
    "month",
    "year",
    # Angle
    "radian",
    "degree",
    # Temperature
    "K",
    "C",
    "F",
    # Density
    "tonne_per_mm3",
    "kg_per_m3",
    "gr_per_cm3",
    "tonne_per_m3",
    # Unit Weight
    "N_per_mm3",
    "N_per_m3",
    "kN_per_m3",
    "kgf_per_m3",
]
