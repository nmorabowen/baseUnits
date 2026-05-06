"""kip-inches-s consistent unit system."""

from .._make_system import make_system as _make

_ns = _make(length="inches", force="kip", time="s")
globals().update(_ns.__dict__)
__all__ = [k for k in _ns.__dict__]
del _make, _ns
