# The one rule

Every system built by `make_system(L, F, T)` satisfies a single invariant:

> For every named unit in `_factors`, the unit's value in the system,
> multiplied by the system's base SI value for that dimension, equals the
> unit's absolute SI value. As a corollary, `F = m * a` and `sigma = F / A`
> hold without spurious factors.

That invariant is what makes the library safe to use without wrapper
objects. If it holds, ordinary arithmetic on the named floats produces
correct results in the system's own base.

## Enforcement

The rule is parametrised over every pre-built system in
[`test/test_consistency.py`](https://github.com/nmorabowen/baseUnits/blob/main/test/test_consistency.py).
The test suite checks four things per system:

1. `100 kg * 9.81 m/s**2 == 981 N`.
2. `20 kgf / 2 mm**2 == 98.0665 MPa`.
3. Every unit's stored float equals `abs_si / base_si` to 1e-12.
4. The "natural" derived unit collapses to exactly 1.0 (e.g. `MPa == 1.0`
   in N-mm, `Pa == 1.0` in N-m, `kPa == 1.0` in kN-m).

## The same calculation in every system

```python
import baseUnits.systems.N_mm_s   as nmm
import baseUnits.systems.N_m_s    as nm
import baseUnits.systems.kN_m_s   as knm
import baseUnits.systems.kip_in_s as kin

def weight(sys):
    return 100 * sys.kg * 9.81 * sys.m / sys.s**2

# Each call returns the value of 981 N expressed in that system's base.
print(weight(nmm) / nmm.N)    # 981.0   (981 N in N-mm system)
print(weight(nm)  / nm.N)     # 981.0
print(weight(knm) / knm.N)    # 981.0
print(weight(kin) / kin.N)    # 981.0
```

Every call computes the same physical force; the underlying floats differ
but each ratio is `981.0` to numerical precision. That is the rule, made
visible.
