"""
baseUnits: A Python package for unit-aware physical calculations.
"""

# 1. Expose the core classes and helpers
from .dimension import Dimension
from .units import Unit, register_base_unit, get_base_unit
from .quantity import Quantity

# 2. Expose all unit instances from the dimensions sub-package
from .dimensions.length import *
from .dimensions.mass import *
from .dimensions.force import *
from .dimensions.time import *
from .dimensions.angle import *
from .dimensions.temperature import *
# --- Derived Units ---
from .dimensions.pressure import *
from .dimensions.energy import *
from .dimensions.power import *
from .dimensions.density import * # <-- NEW
from .dimensions.unit_weight import * # <-- NEW

# 3. Define '__all__' for a clean 'from baseUnits import *'
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

    # Density (NEW)
    'tonne_per_mm3', 'kg_per_m3', 'gr_per_cm3', 'tonne_per_m3',

    # Unit Weight (NEW)
    'N_per_mm3', 'N_per_m3', 'kN_per_m3', 'kgf_per_m3',
]