"""tf-m-s consistent unit system (gravitational / engineering metric, tonne-force).

Force base is the tonne-force (1 tf = 9806.65 N = 1000 kgf). Mass is *derived*
and equals 9806.65 kg (1000 hyl); this primitive has no popular short name, so
``BASE`` reads ``"tf-m-s"``.

This is the ``kgf-m-s`` system scaled up by 1000 in force, common in large-scale
civil/geotechnical work where loads are quoted in tonnes-force.

Consequences worth knowing:

- ``tf = 1`` (the force base) and ``kgf = 1e-3`` (since 1 tf = 1000 kgf).
- ``g = 9.80665`` (m/s²), unchanged: this is a *consistent* system, not a
  gravitational shortcut where ``g = 1``.
- The natural pressure base is ``tf/m²`` (~9.80665 Pa). The library does not
  expose that as a named unit, so ``Pa = 1.0197e-4`` and ``kgf_cm2 = 10`` in
  this system (1 kgf/cm² = 10 tf/m²).
"""

from .._make_system import make_system as _make

# Mass primitive is 9806.65 kg (1000 hyl); no popular short name in the
# factor table, so we cannot pass mass="...".
_ns = _make(length="m", force="tf", time="s")
globals().update(_ns.__dict__)
__all__ = list(_ns.__dict__)  # pyright: ignore[reportUnsupportedDunderAll]
del _make, _ns
