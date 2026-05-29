"""N-mm-tonne-s consistent unit system."""

from .._make_system import make_system as _make

_ns = _make(length="mm", force="N", mass="tonne", time="s")
globals().update(_ns.__dict__)
__all__ = list(_ns.__dict__)  # pyright: ignore[reportUnsupportedDunderAll]
del _make, _ns
