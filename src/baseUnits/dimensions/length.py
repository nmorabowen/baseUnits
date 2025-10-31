"""
Defines all Length units.

The base unit for Length is 'mm' (millimeter), so all conversion
factors are relative to 'mm'.
"""

# Import the base Unit class from the 'units.py' file (one level up)
from ..units import Unit, register_base_unit

# 1. Define and register the base unit
mm = register_base_unit(
    Unit(name="millimeter", symbol="mm", dimension="Length", factor=1.0)
)

# 2. Define other Length units relative to the base (mm)
cm = Unit(name="centimeter", symbol="cm", dimension="Length", factor=10.0)
m = Unit(name="meter", symbol="m", dimension="Length", factor=1000.0)
km = Unit(name="kilometer", symbol="km", dimension="Length", factor=1.0e6)
inches = Unit(name="inch", symbol="inches", dimension="Length", factor=25.4)
ft = Unit(name="foot", symbol="ft", dimension="Length", factor=304.8)
yard = Unit(name="yard", symbol="yard", dimension="Length", factor=914.4)
mile = Unit(name="mile", symbol="mile", dimension="Length", factor=1609344.0)