"""
Defines all Mass units.

The base unit for Mass is 'tonne' (1000 kg), so all conversion
factors are relative to 'tonne'.
"""

# Import the base Unit class from the 'units.py' file (one level up)
from ..units import Unit, register_base_unit

# 1. Define the base unit for this dimension
tonne = register_base_unit(
    Unit(name="tonne", symbol="tonne", dimension="Mass", factor=1.0)
)

# 2. Define other Mass units relative to the base (tonne)
kg = Unit(name="kilogram", symbol="kg", dimension="Mass", factor=1e-3)
gr = Unit(name="gram", symbol="gr", dimension="Mass", factor=1e-6)
mg = Unit(name="milligram", symbol="mg", dimension="Mass", factor=1e-9)

# 3. Create aliases for 'gram'
gram = gr

# 4. Imperial units
lb = Unit(name="pound", symbol="lb", dimension="Mass", factor=453.6e-6)
oz = Unit(name="ounce", symbol="oz", dimension="Mass", factor=28.3495e-6)