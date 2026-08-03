"""Conversion factors for the checked layer, derived from the SI source of truth.

:mod:`baseUnits._factors` holds every unit's absolute SI value. The checked
layer works in N-mm-tonne-s, so a checked unit's factor is simply its SI value
divided by the SI value of that dimension's checked base unit.

Deriving the numbers instead of re-typing them is what keeps the checked layer
and the float layer from drifting apart — they did drift once, leaving the
checked layer on four-significant-figure imperial factors (``lbf = 4.448``)
long after the float layer had moved to exact ones. ``test_exact_factors.py``
enforces the invariant.
"""

from __future__ import annotations

from .. import _factors as _f


def factors(dimension: str, base: str) -> dict[str, float]:
    """Return every unit of ``dimension`` expressed in the ``base`` unit.

    Args:
        dimension: Name of a dict in :mod:`baseUnits._factors`, e.g. ``"FORCE"``.
        base: Key within that dict naming the checked layer's base unit for
            the dimension, e.g. ``"N"``.

    Returns:
        Mapping of unit name to its factor relative to ``base``.

    Example:
        >>> factors("LENGTH", "mm")["inches"]
        25.4
    """
    table: dict[str, float] = getattr(_f, dimension)
    base_si = table[base]
    return {name: si / base_si for name, si in table.items()}
