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
    """Build a consistent unit system from L, T, and force and/or mass.

    Always pass ``length`` and ``time``. You may additionally pass ``force``,
    ``mass``, or both:

    - **One of force/mass** — the other is derived so ``F = M * L / T**2``.
    - **Both** — the factory verifies they are mutually consistent and
      raises ``ValueError`` if not. Use this form to make every system
      module fully self-documenting at the call site.
    - **Neither** — raises ``ValueError``.

    Pressure, energy, power, density, and unit-weight bases are then
    constructed from the four primitives. Each named unit in
    :mod:`baseUnits._factors` is divided by its dimension's base SI value
    to produce a float you multiply scalars by.

    Args:
        length: Key in ``_factors.LENGTH`` (e.g. ``"mm"``, ``"m"``, ``"inches"``).
        time: Key in ``_factors.TIME`` (typically ``"s"``).
        force: Optional key in ``_factors.FORCE``.
        mass: Optional key in ``_factors.MASS``.

    Returns:
        A :class:`types.SimpleNamespace` with one float attribute per named
        unit, plus ``g`` (gravity in the system) and ``BASE`` (human-readable
        label of the system).

    Raises:
        ValueError: If neither force nor mass is given, or if both are given
            and their combination violates ``F = M * L / T**2``.
        KeyError: If any name is not a known unit in ``_factors``.

    Example:
        >>> # Three-arg form — derive mass from force.
        >>> sys = make_system(length="mm", force="N", time="s")
        >>> sys.MPa
        1.0
        >>> sys.BASE
        'N-mm-tonne-s'

        >>> # Four-arg form — fully explicit, factory verifies consistency.
        >>> mks = make_system(length="m", force="N", mass="kg", time="s")
        >>> mks.BASE
        'N-m-kg-s'
    """
    if force is None and mass is None:
        raise ValueError("Pass at least one of `force` or `mass`.")

    L = _f.LENGTH[length]
    T = _f.TIME[time]
    if force is not None and mass is not None:
        F = _f.FORCE[force]
        M = _f.MASS[mass]
        derived_M = F * T**2 / L
        if not math.isclose(derived_M, M, rel_tol=1e-9):
            raise ValueError(
                f"Inconsistent system: force='{force}' with length='{length}' "
                f"and time='{time}' implies mass={derived_M} kg, but "
                f"mass='{mass}' is {M} kg."
            )
    elif force is not None:
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
