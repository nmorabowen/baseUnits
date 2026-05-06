"""Temperature units (deltas only — no offsets). Base unit is Kelvin."""

from ..units import Unit, register_base_unit

K = register_base_unit(Unit(name="Kelvin", symbol="K", dimension="Temperature", factor=1.0))

C = Unit(name="Celsius", symbol="°C", dimension="Temperature", factor=1.0)

F = Unit(name="Fahrenheit", symbol="°F", dimension="Temperature", factor=(5.0 / 9.0))
