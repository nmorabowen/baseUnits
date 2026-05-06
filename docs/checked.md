# Checked layer

`baseUnits.checked` is the opt-in dimensional-safety layer. It wraps each
unit in a `Quantity` object that tracks dimensions at runtime and raises
`TypeError` on incoherent operations.

## When to use it

- Development and debugging: catch unit bugs early.
- Validation suites and unit tests: assert that an expression has the right
  dimension before trusting its numerical value.
- Tutorials and onboarding code: the error messages teach.

## When not to use it

- Inside numpy/pandas/matplotlib code paths. `Quantity` is a Python object;
  you lose vectorisation and array interop.
- Hot loops in solvers. The overhead is per-operation.
- Anywhere the float layer is already covered by tests.

For those cases, use the float constants from `baseUnits` directly.

## Importing

```python
from baseUnits.checked import Quantity, m, kg, N, MPa
```

## Example

```python
from baseUnits.checked import m, kg

length = 10 * m
mass = 5 * kg

length + length      # OK
length + mass        # raises TypeError: incompatible dimensions
```

Because `Quantity` is a wrapper class, it is *not* a drop-in replacement
for the float layer when feeding numpy or pandas. That mismatch is by
design: the float layer and the checked layer are deliberately separate
tools.
