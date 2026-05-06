"""kgf-m-s consistent unit system (gravitational / engineering metric).

Force base is the kilogram-force. Mass is *derived* and equals the **hyl**
(also called *technical mass unit* or *metric slug*), 1 hyl = 9.80665 kg.
The hyl has no popular short name, so ``BASE`` reads ``"kgf-m-s"``.

Consequences worth knowing:

- ``kg = 1 / 9.80665 ≈ 0.10197`` in this system, because the natural mass
  base is the hyl, not the kilogram. ``100 * kg * g`` evaluates to ``100``
  (i.e. 100 kgf) — which is exactly the weight of a 100 kg mass.
- ``g = 9.80665`` (m/s²), unchanged: this is a *consistent* system, not a
  gravitational shortcut where ``g = 1``.
- The natural pressure base is ``kgf/m²`` (~9.80665 Pa). The library does
  not expose that as a named unit, so ``Pa = 0.10197`` and
  ``kgf_cm2 = 1e4`` in this system.
"""

from .._make_system import make_system as _make

# Mass primitive is the hyl (~9.80665 kg); no popular short name in the
# factor table, so we cannot pass mass="...".
_ns = _make(length="m", force="kgf", time="s")
globals().update(_ns.__dict__)
__all__ = [k for k in _ns.__dict__]
del _make, _ns
