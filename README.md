# baseUnits

Float-based unit conversion factors for consistent unit systems.

## Architecture

Every unit is a plain `float` equal to its conversion factor into a chosen consistent base system. Absolute SI values live in a single source of truth (`_factors.py`); a system factory derives a consistent set of float constants for any (length, force, time) triple. An opt-in `baseUnits.checked` submodule keeps a `Quantity`/`Unit`/`Dimension` runtime layer for safety-critical code.

## Default system: N-mm-tonne-s

| Quantity | Unit | Value |
|---|---|---|
| Length | mm | 1.0 |
| Force | N | 1.0 |
| Mass | tonne | 1.0 |
| Time | s | 1.0 |
| Pressure | MPa | 1.0 |
| g | gravity | 9806.65 |

## Available systems

- `baseUnits.systems.N_mm` — N-mm-tonne-s (default)
- `baseUnits.systems.N_m` — N-m-kg-s
- `baseUnits.systems.kN_m` — kN-m-tonne-s
- `baseUnits.systems.kip_in` — kip-inches-s

## Quickstart

```python
from baseUnits import m, kN, MPa, g

length = 5 * m          # 5000.0 (mm)
load   = 100 * kN       # 100000.0 (N)
stress = 30 * MPa       # 30.0 (MPa)
weight = 80 * g         # 80 * 9806.65 (mm/s^2 acceleration scale)
```

## Switching systems

```python
from baseUnits.systems.kip_in import m, kN, ksi, BASE

print(BASE)             # "kip-inches-s"
print(5 * m)            # 196.85 (inches)
```

## Opt-in dimensional safety

For runtime checks that catch dimension mismatches, use `baseUnits.checked`:

```python
from baseUnits.checked import Quantity, m, mm, K, C

q = 5 * m
print(q.to(mm).value)   # 5000.0
print((1 * K).to(C).value)  # 1.0
```

Arithmetic on `Quantity` objects raises if you mix incompatible dimensions.

## Installation

```bash
git clone https://github.com/nmorabowen/baseUnits.git
cd baseUnits
pip install -e .
```
