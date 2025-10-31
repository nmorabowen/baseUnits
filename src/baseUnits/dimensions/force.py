"""
Defines all Force units.
Dimension: Mass * Length / Time^2
Base Unit: N (which is 1.0 tonne*mm/s^2)
"""
# Import the base Unit class
from ..units import Unit, register_base_unit
# Import the Dimension helper class
from ..dimension import Dimension

# 1. Define the compound dimension for Force
FORCE_DIMENSION = Dimension("Mass") * Dimension("Length") / (Dimension("Time") ** 2)

# 2. Define the base unit for this dimension
#    N = 1 kg*m/s^2 = (1e-3 tonne)*(1e3 mm)/s^2 = 1.0 tonne*mm/s^2
N = register_base_unit(
    Unit(name="Newton", symbol="N", dimension=FORCE_DIMENSION, factor=1.0)
)

# 3. Define other Force units relative to the base (N)
kN = Unit(name="kiloNewton", symbol="kN", dimension=FORCE_DIMENSION, factor=1e3)
MN = Unit(name="MegaNewton", symbol="MN", dimension=FORCE_DIMENSION, factor=1e6)
dyne = Unit(name="dyne", symbol="dyne", dimension=FORCE_DIMENSION, factor=1e-5)
kgf = Unit(name="kilogram-force", symbol="kgf", dimension=FORCE_DIMENSION, factor=9.807)
tf = Unit(name="tonne-force", symbol="tf", dimension=FORCE_DIMENSION, factor=9807.0)

# 4. Imperial units
lbf = Unit(name="pound-force", symbol="lbf", dimension=FORCE_DIMENSION, factor=4.448)
kip = Unit(name="kip", symbol="kip", dimension=FORCE_DIMENSION, factor=4448.0)