"""Factory that builds a consistent unit system as a SimpleNamespace of floats."""

import math
from types import SimpleNamespace

from . import _factors as _f


def make_system(length: str, force: str, time: str) -> SimpleNamespace:
    """Build a consistent unit system from a length/force/time triple.

    Mass is *derived* from the chosen primitives via ``M = F * T**2 / L`` so
    that Newton's second law holds without spurious factors. Pressure, energy,
    power, density, and unit-weight bases follow the same construction.

    Each named unit in :mod:`baseUnits._factors` is then divided by its
    dimension's base SI value to produce a float you multiply scalars by.

    Args:
        length: Key in ``_factors.LENGTH`` (e.g. ``"mm"``, ``"m"``, ``"inches"``).
        force: Key in ``_factors.FORCE`` (e.g. ``"N"``, ``"kN"``, ``"kip"``).
        time: Key in ``_factors.TIME`` (typically ``"s"``).

    Returns:
        A :class:`types.SimpleNamespace` with one float attribute per named
        unit, plus ``g`` (gravity in the system) and ``BASE`` (human-readable
        label of the system).

    Raises:
        KeyError: If any of ``length``, ``force``, or ``time`` is not a known
            unit name in ``_factors``.

    Example:
        >>> sys = make_system("mm", "N", "s")
        >>> sys.m
        1000.0
        >>> sys.MPa
        1.0
        >>> sys.BASE
        'N-mm-tonne-s'
    """
    L = _f.LENGTH[length]
    F = _f.FORCE[force]
    T = _f.TIME[time]
    M = F * T**2 / L
    P = F / L**2
    E = F * L
    Pw = E / T
    D = M / L**3
    UW = F / L**3

    ns = SimpleNamespace()
    for name, v in _f.LENGTH.items():
        setattr(ns, name, v / L)
    for name, v in _f.FORCE.items():
        setattr(ns, name, v / F)
    for name, v in _f.MASS.items():
        setattr(ns, name, v / M)
    for name, v in _f.TIME.items():
        setattr(ns, name, v / T)
    for name, v in _f.PRESSURE.items():
        setattr(ns, name, v / P)
    for name, v in _f.ENERGY.items():
        setattr(ns, name, v / E)
    for name, v in _f.POWER.items():
        setattr(ns, name, v / Pw)
    for name, v in _f.DENSITY.items():
        setattr(ns, name, v / D)
    for name, v in _f.UNIT_WEIGHT.items():
        setattr(ns, name, v / UW)
    for name, v in _f.ANGLE.items():
        setattr(ns, name, v)
    for name, v in _f.TEMPERATURE.items():
        setattr(ns, name, v)

    ns.g = 9.80665 * T**2 / L

    mass_name = next((n for n, v in _f.MASS.items() if math.isclose(v, M)), None)
    ns.BASE = f"{force}-{length}-{mass_name}-{time}" if mass_name else f"{force}-{length}-{time}"
    return ns
