"""N-m-kg-s consistent unit system."""

from .._make_system import make_system as _make

_ns = _make(length="m", force="N", mass="kg", time="s")
globals().update(_ns.__dict__)
__all__ = list(_ns.__dict__)  # pyright: ignore[reportUnsupportedDunderAll]
del _make, _ns
