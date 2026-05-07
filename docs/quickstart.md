# Quickstart

## Importing

```python
import baseUnits as u
print(u.BASE)   # 'N-mm-tonne-s'
```

`u.m`, `u.kN`, `u.MPa`, `u.tonne`, etc. are plain floats expressed in the
default base (N-mm-tonne-s).

## FEM-style calculations

```python
import baseUnits as u

# Cantilever tip deflection: delta = P L^3 / (3 E I)
P = 10 * u.kN
L = 2.5 * u.m
E = 200 * u.GPa
I = 8.33e7 * u.mm**4

delta = P * L**3 / (3 * E * I)
print(delta / u.mm)   # tip deflection in mm
```

```python
# Stress on a bar
F = 50 * u.kN
A = 25 * u.mm * 10 * u.mm
sigma = F / A
print(sigma / u.MPa)   # 200.0
```

## Converting between units

Multiply by the source unit, divide by the target unit.

```python
length_in_inches = 2 * u.m / u.inches
print(length_in_inches)   # 78.7401...

stress_in_psi = (50 * u.MPa) / u.psi
print(stress_in_psi)      # 7251.89...
```

## Numpy and pandas

```python
import numpy as np
import baseUnits as u

displacements = np.array([0.0, 1.2, 3.4, 5.1]) * u.mm
stiffness = 4.5 * u.kN / u.mm
forces = stiffness * displacements      # numpy array of floats in N
```

There is no `Quantity` wrapper to fight numpy. Broadcasting, ufuncs, and
pandas columns all see ordinary floats.

## The `g` constant

`u.g` is gravity in the active system. Multiply masses by it to get weights:

```python
mass = 250 * u.kg
weight = mass * u.g
print(weight / u.kN)   # 2.4516625
```

## The `BASE` sanity check

In project code, assert what system you are running in:

```python
import baseUnits as u
assert u.BASE == "N-mm-tonne-s", f"unexpected base: {u.BASE}"
```

That single assert catches accidental system swaps (someone pasting
`from baseUnits.systems.kip_in_s import *` two scopes up).
