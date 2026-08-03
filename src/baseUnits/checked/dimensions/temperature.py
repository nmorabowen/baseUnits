"""Temperature units (deltas only — no offsets). Base unit is Kelvin.

Factors come from ``baseUnits._factors`` so this layer cannot drift away from
the float layer; see :mod:`baseUnits.checked._derived`.
"""

from .._derived import factors
from ..units import Unit, register_base_unit

_F = factors("TEMPERATURE", "K")

K = register_base_unit(Unit(name="Kelvin", symbol="K", dimension="Temperature", factor=_F["K"]))

C = Unit(name="Celsius", symbol="°C", dimension="Temperature", factor=_F["C"])

F = Unit(name="Fahrenheit", symbol="°F", dimension="Temperature", factor=_F["F"])
