# Switching systems

The default top-level package is N-mm-tonne-s. Three patterns let you work
in a different system.

## 1. Whole-script switch

```python
from baseUnits.systems.kip_in import *

assert BASE == "kip-inches-s"
F = 50 * kip
A = 0.5 * inches * 0.5 * inches
sigma = F / A
print(sigma / ksi)
```

The `import *` puts every named float (and `BASE`, `g`) in your module
namespace. Use this in standalone scripts or notebooks where the target
system is unambiguous.

## 2. Aliased import

```python
import baseUnits.systems.kN_m as u

assert u.BASE == "kN-m-tonne-s"
F = 100 * u.kN
L = 5 * u.m
moment = F * L
print(moment / u.kN / u.m)   # 500.0
```

Slightly more verbose, but every unit is qualified — easier to read in
larger codebases and trivial to swap by changing the module name.

## 3. Project-level convention

For a multi-file project, define the system in one place and import that
everywhere:

```python
# myproject/units.py
from baseUnits.systems.kN_m import *  # noqa: F401, F403
```

```python
# myproject/analysis.py
from .units import kN, m, MPa, kg, BASE
assert BASE == "kN-m-tonne-s"
```

The single `units.py` is now the only file that decides which system the
project runs in. Switching is a one-line change.

## Sanity-check the active base

Whichever pattern you pick, assert it:

```python
import baseUnits
assert baseUnits.BASE == "N-mm-tonne-s"
```

or with an aliased system:

```python
import baseUnits.systems.kip_in as u
assert u.BASE == "kip-inches-s"
```

This protects against accidental imports in the wrong order — a frequent
source of silent unit bugs.
