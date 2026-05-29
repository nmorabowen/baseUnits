"""kip-inches-s consistent unit system."""

from .._make_system import make_system as _make

# Mass primitive is the derived "kip*s^2/in" (~175126.835 kg); it has no
# popular short name, so we cannot pass mass="...".
_ns = _make(length="inches", force="kip", time="s")
globals().update(_ns.__dict__)
__all__ = list(_ns.__dict__)  # pyright: ignore[reportUnsupportedDunderAll]
del _make, _ns
