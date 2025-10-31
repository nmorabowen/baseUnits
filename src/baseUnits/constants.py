"""
This file defines common physical and mathematical constants.

Physical constants are defined using the unit objects from the
'dimensions' sub-package. This makes them 'Quantity' objects,
fully compatible with all unit-aware calculations.
"""


# We import the specific units we need from the dimensions sub-package.
# These files (length.py, time.py) will define the 'm' and 's' Unit objects.
from .dimensions.length import m
from .dimensions.time import s

# --- Physical Constants ---

# Standard Gravity
# We define it in standard units (9.81 m/s^2).
# The multiplication (float * Unit / Unit**2) automatically
# creates a Quantity object with the correct compound unit.
# The library will handle all conversions to the base system (mm/s^2).
g = 9.81 * m / (s**2)

