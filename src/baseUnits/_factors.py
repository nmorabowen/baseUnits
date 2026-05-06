"""Absolute SI values for every named unit.

Each dimension is a plain ``dict`` mapping the Python identifier of a unit to
its value in the corresponding SI base unit (metre, newton, kilogram, second,
pascal, joule, watt, kg/m^3, N/m^3, radian, kelvin). This module is the single
source of truth: every consistent system is built by dividing these absolute
SI values by the chosen system's base SI values (see
:func:`baseUnits._make_system.make_system`).

Edit this file to add a new unit; every pre-built system picks it up
automatically on the next build.
"""

import math

LENGTH = {  # in meters
    "mm": 1e-3,
    "cm": 1e-2,
    "m": 1.0,
    "km": 1e3,
    "inches": 0.0254,
    "ft": 0.3048,
    "yard": 0.9144,
    "mile": 1609.344,
}
FORCE = {  # in newtons
    "N": 1.0,
    "kN": 1e3,
    "MN": 1e6,
    "dyne": 1e-5,
    "kgf": 9.80665,
    "tf": 9806.65,
    "lbf": 4.4482216152605,
    "kip": 4448.2216152605,
}
MASS = {  # in kg
    "kg": 1.0,
    "tonne": 1e3,
    "gram": 1e-3,
    "gr": 1e-3,
    "mg": 1e-6,
    "lb": 0.45359237,
    "oz": 0.028349523125,
}
TIME = {  # in seconds
    "s": 1.0,
    "minutes": 60.0,
    "h": 3600.0,
    "day": 86400.0,
    "week": 604800.0,
    "month": 2592000.0,
    "year": 31557600.0,
}
PRESSURE = {  # in Pa
    "Pa": 1.0,
    "kPa": 1e3,
    "MPa": 1e6,
    "GPa": 1e9,
    "kgf_cm2": 98066.5,
    "ksi": 6894757.293168,
    "psi": 6894.757293168,
    "bar": 1e5,
    "atm": 101325.0,
}
ENERGY = {  # in J
    "J": 1.0,
    "kJ": 1e3,
    "mJ": 1e-3,
    "cal": 4.184,
    "kcal": 4184.0,
    "eV": 1.602176634e-19,
    "Wh": 3600.0,
    "kWh": 3.6e6,
}
POWER = {  # in W
    "W": 1.0,
    "kW": 1e3,
    "MW": 1e6,
    "HP": 745.6998715822702,
    "mJ_s": 1e-3,
}
DENSITY = {  # in kg/m^3
    "kg_per_m3": 1.0,
    "gr_per_cm3": 1000.0,
    "tonne_per_m3": 1000.0,
    "tonne_per_mm3": 1e12,
    "lb_per_ft3": 16.018463374,
}
UNIT_WEIGHT = {  # in N/m^3
    "N_per_m3": 1.0,
    "kN_per_m3": 1e3,
    "kgf_per_m3": 9.80665,
    "N_per_mm3": 1e9,
}
ANGLE = {  # in rad (dimensionless)
    "radian": 1.0,
    "rad": 1.0,
    "degree": math.pi / 180.0,
}
TEMPERATURE = {  # in K (deltas only — no offsets)
    "K": 1.0,
    "C": 1.0,
    "F": 5.0 / 9.0,
}
