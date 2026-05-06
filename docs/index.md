# baseUnits

A float-based unit-factor library for consistent unit systems used in
engineering and physics. Pick a base system once; every named unit becomes a
plain `float` you multiply scalars by. No wrapper objects, no per-operation
overhead, no surprises when you hand values to numpy, pandas, or matplotlib.

## 30-second quickstart

```python
import baseUnits as u

# Default system: N-mm-tonne-s
print(u.BASE)            # 'N-mm-tonne-s'

length = 5 * u.m         # 5 metres -> 5000.0 (mm)
force  = 100 * u.kN      # 100 kN  -> 100000.0 (N)
stress = force / (50 * u.mm**2)
print(stress / u.MPa)    # 40.0
```

## Philosophy

- **Floats by default.** Every unit is a `float`. Math is regular arithmetic;
  numpy and pandas don't know anything special is happening.
- **Consistent systems by construction.** A system is fixed by a
  *length / force / time* triple. Mass is derived so `F = m * a` falls out of
  ordinary multiplication.
- **Opt-in safety.** When you want runtime dimensional checks, import from
  `baseUnits.checked` instead. Same factor library, wrapped objects.

## Where to next

- [Architecture](architecture.md) — how the package is laid out.
- [The one rule](the-one-rule.md) — the invariant every system obeys.
- [Systems](systems.md) — every available system and its unit table.
