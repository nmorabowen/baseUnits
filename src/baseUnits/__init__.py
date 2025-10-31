"""
baseUnits: A Python package for unit-aware physical calculations.

This __init__.py file assembles the library's public API, making
core classes, constants, and all unit definitions available
from the top-level 'baseUnits' import.
"""

# 1. Expose the core classes and helpers
#    The order here is critical to avoid circular imports.
#    Dimension has no dependencies.
#    Unit depends on Dimension.
#    Quantity depends on Unit and Dimension.
from .dimension import Dimension
from .units import Unit
from .quantity import Quantity

# 2. Expose all unit instances from the dimensions sub-package
#    These modules all depend on 'Unit'
from .dimensions.length import *
from .dimensions.mass import *
from .dimensions.force import *
from .dimensions.pressure import *
from .dimensions.time import *
from .dimensions.energy import *
from .dimensions.power import *
from .dimensions.angle import *
from .dimensions.temperature import *

# 3. Expose constants
#    This MUST be imported LAST, because constants.py
#    depends on the 'dimensions' modules (for m, s) and
#    implicitly on 'quantity' (to create the 'g' object).
# from .constants import *

# 4. Define '__all__' for a clean 'from baseUnits import *'
#    This lists all public-facing names.
__all__ = [
    # Core Classes
    'Unit', 'Quantity', 'Dimension',

    # Length
    'mm', 'cm', 'm', 'km', 'inches', 'ft', 'yard', 'mile',

    # Force
    'N', 'kN', 'MN', 'dyne', 'kgf', 'tf', 'lbf', 'kip',

    # Mass
    'tonne', 'kg', 'gr', 'gram', 'mg', 'lb', 'oz', 

    # Pressure
    'MPa', 'kPa', 'GPa', 'kgf_cm2', 'Pa', 'ksi',

    # Energy
    'J', 'kJ', 'mJ', 'cal', 'kcal', 'eV', 'Wh', 'kWh',

    # Power
    'W', 'kW', 'MW', 'HP', 'mJ_s',

    # Time
    's', 'minutes', 'h', 'day', 'week', 'month', 'year',

    # Angle
    'radian', 'degree',

    # Temperature
    'K', 'C', 'F',
]