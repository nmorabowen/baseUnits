"""Factory that builds a consistent unit system as a SimpleNamespace of floats."""

from __future__ import annotations

import math
from types import SimpleNamespace

from . import _factors as _f


def make_system(
    *,
    length: str,
    time: str,
    force: str | None = None,
    mass: str | None = None,
) -> SimpleNamespace:
    """Build a consistent unit system from L-T plus exactly one of force or mass.

    Pick three primitives — length, time, and *either* force or mass — and the
    fourth is derived so that Newton's second law holds without spurious
    factors (``F = M * L / T**2``). Pressure, energy, power, density, and
    unit-weight bases follow the same construction.

    Each named unit in :mod:`baseUnits._factors` is then divided by its
    dimension's base SI value to produce a float you multiply scalars by.

    Args:
        length: Key in ``_factors.LENGTH`` (e.g. ``"mm"``, ``"m"``, ``"inches"``).
        time: Key in ``_factors.TIME`` (typically ``"s"``).
        force: Key in ``_factors.FORCE`` (e.g. ``"N"``, ``"kN"``, ``"kip"``).
            Provide this for the F-L-T mental model. Mutually exclusive with ``mass``.
        mass: Key in ``_factors.MASS`` (e.g. ``"kg"``, ``"gram"``, ``"tonne"``).
            Provide this for the L-M-T (physics/SI) mental model. Mutually
            exclusive with ``force``.

    Returns:
        A :class:`types.SimpleNamespace` with one float attribute per named
        unit, plus ``g`` (gravity in the system) and ``BASE`` (human-readable
        label of the system).

    Raises:
        ValueError: If neither or both of ``force`` and ``mass`` are given.
        KeyError: If any name is not a known unit in ``_factors``.

    Example:
        >>> sys = make_system(length="mm", force="N", time="s")
        >>> sys.MPa
        1.0
        >>> sys.BASE
        'N-mm-tonne-s'

        >>> mks = make_system(length="m", mass="kg", time="s")
        >>> mks.N
        1.0
        >>> mks.BASE
        'N-m-kg-s'
    """
    if (force is None) == (mass is None):
        raise ValueError("Pass exactly one of `force` or `mass`.")

    L = _f.LENGTH[length]
    T = _f.TIME[time]
    if force is not None:
        F = _f.FORCE[force]
        M = F * T**2 / L
    else:
        M = _f.MASS[mass]
        F = M * L / T**2

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

    force_name = force or next((n for n, v in _f.FORCE.items() if math.isclose(v, F)), None)
    mass_name = mass or next((n for n, v in _f.MASS.items() if math.isclose(v, M)), None)
    parts = [p for p in (force_name, length, mass_name, time) if p]
    ns.BASE = "-".join(parts)
    return ns
