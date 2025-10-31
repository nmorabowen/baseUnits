"""
Defines all Force units.

The base unit for Force is 'N' (Newton), so all conversion
factors are relative to 'N'.
"""

# Import the base Unit class from the 'units.py' file (one level up)
from ..units import Unit, register_base_unit

# 1. Define the base unit for this dimension
N = register_base_unit(
    Unit(name="Newton", symbol="N", dimension="Force", factor=1.0)
)

# 2. Define other Force units relative to the base (N)
kN = Unit(name="kiloNewton", symbol="kN", dimension="Force", factor=1e3)
MN = Unit(name="MegaNewton", symbol="MN", dimension="Force", factor=1e6)
dyne = Unit(name="dyne", symbol="dyne", dimension="Force", factor=1e-5)
kgf = Unit(name="kilogram-force", symbol="kgf", dimension="Force", factor=9.807)
tf = Unit(name="tonne-force", symbol="tf", dimension="Force", factor=9807.0)

# 3. Imperial units
lbf = Unit(name="pound-force", symbol="lbf", dimension="Force", factor=4.448)
kip = Unit(name="kip", symbol="kip", dimension="Force", factor=4448.0)