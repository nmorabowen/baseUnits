"""
Defines all Length units.

The base unit for Length is 'mm' (millimeter), so all conversion
factors are relative to 'mm'.

Factors come from ``baseUnits._factors`` so this layer cannot drift away from
the float layer; see :mod:`baseUnits.checked._derived`.
"""

# Import the base Unit class from the 'units.py' file (one level up)
from .._derived import factors
from ..units import Unit, register_base_unit

_F = factors("LENGTH", "mm")

# 1. Define and register the base unit
mm = register_base_unit(Unit(name="millimeter", symbol="mm", dimension="Length", factor=_F["mm"]))

# 2. Define other Length units relative to the base (mm)
cm = Unit(name="centimeter", symbol="cm", dimension="Length", factor=_F["cm"])
m = Unit(name="meter", symbol="m", dimension="Length", factor=_F["m"])
km = Unit(name="kilometer", symbol="km", dimension="Length", factor=_F["km"])
inches = Unit(name="inch", symbol="inches", dimension="Length", factor=_F["inches"])
ft = Unit(name="foot", symbol="ft", dimension="Length", factor=_F["ft"])
yard = Unit(name="yard", symbol="yard", dimension="Length", factor=_F["yard"])
mile = Unit(name="mile", symbol="mile", dimension="Length", factor=_F["mile"])
