"""dyne-cm-gram-s consistent unit system (also known as CGS).

Force base is the dyne (``1 dyne = 1 g*cm/s^2``). Common in physics and
chemistry; rarely used in engineering. Pressure base is the barye
(``1 dyne/cm^2``); the library does not currently include it as a named
unit, so ``Pa = 10`` and ``MPa = 1e7`` in this system.
"""

from .._make_system import make_system as _make

_ns = _make(length="cm", force="dyne", mass="gram", time="s")
globals().update(_ns.__dict__)
__all__ = [k for k in _ns.__dict__]
del _make, _ns
