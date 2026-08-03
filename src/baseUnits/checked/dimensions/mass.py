"""
Defines all Mass units.

The base unit for Mass is 'tonne' (1000 kg), so all conversion
factors are relative to 'tonne'.

Factors come from ``baseUnits._factors`` so this layer cannot drift away from
the float layer; see :mod:`baseUnits.checked._derived`.
"""

# Import the base Unit class from the 'units.py' file (one level up)
from .._derived import factors
from ..units import Unit, register_base_unit

_F = factors("MASS", "tonne")

# 1. Define the base unit for this dimension
tonne = register_base_unit(Unit(name="tonne", symbol="tonne", dimension="Mass", factor=_F["tonne"]))

# 2. Define other Mass units relative to the base (tonne)
kg = Unit(name="kilogram", symbol="kg", dimension="Mass", factor=_F["kg"])
gr = Unit(name="gram", symbol="gr", dimension="Mass", factor=_F["gr"])
mg = Unit(name="milligram", symbol="mg", dimension="Mass", factor=_F["mg"])

# 3. Create aliases for 'gram'
gram = gr

# 4. Imperial units
lb = Unit(name="pound", symbol="lb", dimension="Mass", factor=_F["lb"])
oz = Unit(name="ounce", symbol="oz", dimension="Mass", factor=_F["oz"])
