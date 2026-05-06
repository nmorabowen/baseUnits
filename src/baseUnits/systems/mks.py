"""MKS (length-mass-time) consistent unit system: m-kg-s.

Numerically identical to ``N_m`` (force is derived as ``M*L/T^2 = N``); the
two modules are different mental models of the same system. Use ``mks`` if
you think in the SI / physics-textbook L-M-T convention.
"""

from .._make_system import make_system as _make

_ns = _make(length="m", force="N", mass="kg", time="s")
globals().update(_ns.__dict__)
__all__ = [k for k in _ns.__dict__]
del _make, _ns
