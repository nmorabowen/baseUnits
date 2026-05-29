"""kN-m-tonne-s consistent unit system."""

from .._make_system import make_system as _make

_ns = _make(length="m", force="kN", mass="tonne", time="s")
globals().update(_ns.__dict__)
__all__ = list(_ns.__dict__)  # pyright: ignore[reportUnsupportedDunderAll]
del _make, _ns
