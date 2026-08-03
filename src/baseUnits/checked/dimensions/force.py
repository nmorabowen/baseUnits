"""
Defines all Force units.
Dimension: Mass * Length / Time^2
Base Unit: N (which is 1.0 tonne*mm/s^2)

Factors come from ``baseUnits._factors`` so this layer cannot drift away from
the float layer; see :mod:`baseUnits.checked._derived`.
"""

# Import the base Unit class
# Import the Dimension helper class
from .._derived import factors
from ..dimension import Dimension
from ..units import Unit, register_base_unit

# 1. Define the compound dimension for Force
FORCE_DIMENSION = Dimension("Mass") * Dimension("Length") / (Dimension("Time") ** 2)

_F = factors("FORCE", "N")

# 2. Define the base unit for this dimension
#    N = 1 kg*m/s^2 = (1e-3 tonne)*(1e3 mm)/s^2 = 1.0 tonne*mm/s^2
N = register_base_unit(Unit(name="Newton", symbol="N", dimension=FORCE_DIMENSION, factor=_F["N"]))

# 3. Define other Force units relative to the base (N)
kN = Unit(name="kiloNewton", symbol="kN", dimension=FORCE_DIMENSION, factor=_F["kN"])
MN = Unit(name="MegaNewton", symbol="MN", dimension=FORCE_DIMENSION, factor=_F["MN"])
dyne = Unit(name="dyne", symbol="dyne", dimension=FORCE_DIMENSION, factor=_F["dyne"])
kgf = Unit(name="kilogram-force", symbol="kgf", dimension=FORCE_DIMENSION, factor=_F["kgf"])
tf = Unit(name="tonne-force", symbol="tf", dimension=FORCE_DIMENSION, factor=_F["tf"])

# 4. Imperial units
lbf = Unit(name="pound-force", symbol="lbf", dimension=FORCE_DIMENSION, factor=_F["lbf"])
kip = Unit(name="kip", symbol="kip", dimension=FORCE_DIMENSION, factor=_F["kip"])
