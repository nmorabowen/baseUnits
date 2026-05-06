"""Generate the entire ``systems.md`` page at build time from ``_factors.py``.

Both the prose intros and the unit tables live here so the page cannot
drift from the implementation. Hand-edits to ``docs/systems.md`` are
overwritten on every build.
"""
from __future__ import annotations

import importlib

import mkdocs_gen_files

from baseUnits import _factors as _f


SYSTEMS = [
    (
        "N_mm",
        "N-mm-tonne-s",
        "Default system. Used for FEM models in millimetres with newton "
        "forces and tonne masses. `MPa` is the natural pressure unit and "
        "equals `1.0`.",
    ),
    (
        "N_m",
        "N-m-kg-s",
        "Strict SI. Length in metres, force in newtons, mass in kilograms. "
        "`Pa` is the natural pressure unit.",
    ),
    (
        "kN_m",
        "kN-m-tonne-s",
        "Common in geotechnical and large-scale civil engineering. `kPa` is "
        "the natural pressure unit.",
    ),
    (
        "kip_in",
        "kip-inches-s",
        "US customary. `ksi` is the natural pressure unit. Mass has no named "
        "consistent unit (it is `kip*s^2/in`).",
    ),
    (
        "mks",
        "N-m-kg-s (MKS)",
        "Built via the L-M-T path (`make_system(length=\"m\", mass=\"kg\", time=\"s\")`). "
        "Numerically identical to `N_m` — the same system, expressed in the "
        "physics/SI mental model where mass is a primitive and force is derived.",
    ),
    (
        "cgs",
        "dyne-cm-gram-s (CGS)",
        "Centimetre-gram-second. Force base is the dyne. Common in physics and "
        "chemistry; the natural pressure (barye), energy (erg), and power "
        "(erg/s) units are not currently in the factor table, so `Pa = 10` "
        "and `MPa = 1e7` here.",
    ),
]

DIMENSIONS = [
    ("Length", "LENGTH"),
    ("Force", "FORCE"),
    ("Mass", "MASS"),
    ("Time", "TIME"),
    ("Pressure", "PRESSURE"),
    ("Energy", "ENERGY"),
    ("Power", "POWER"),
    ("Density", "DENSITY"),
    ("Unit Weight", "UNIT_WEIGHT"),
    ("Angle", "ANGLE"),
    ("Temperature", "TEMPERATURE"),
]


def _fmt(v: float) -> str:
    return f"{v:.6g}"


def _table_for(sys_mod, sysname: str, dim_label: str, dim_attr: str) -> str:
    factors = getattr(_f, dim_attr)
    lines = [
        f"#### {dim_label}",
        "",
        f"| Unit | Value (in `{sysname}`) | Absolute SI |",
        "| --- | --- | --- |",
    ]
    for name, abs_si in factors.items():
        sys_val = getattr(sys_mod, name)
        lines.append(f"| `{name}` | {_fmt(sys_val)} | {_fmt(abs_si)} |")
    lines.append("")
    return "\n".join(lines)


def _render_section(sysname: str, label: str, intro: str) -> str:
    sys_mod = importlib.import_module(f"baseUnits.systems.{sysname}")
    base = getattr(sys_mod, "BASE")
    out = [
        f"## {label}",
        "",
        intro,
        "",
        f"**`baseUnits.BASE`:** `{base}`",
        "",
        f'**Import:** `from baseUnits.systems.{sysname} import *`',
        "",
    ]
    for dim_label, dim_attr in DIMENSIONS:
        out.append(_table_for(sys_mod, sysname, dim_label, dim_attr))
    return "\n".join(out)


HEADER = """# Systems

Each pre-built system fixes a *length / force / time* triple and derives
mass, pressure, energy, power, density, and unit-weight bases from it.
The tables on this page are generated at build time directly from
`_factors.py` and the system definitions, so they cannot drift from the
implementation.

The `Value (in <sys>)` column is what you get when you multiply a scalar
by `sys.<unit>`. For example, in the N-mm system, `5 * u.m` evaluates to
`5000.0` because `u.m == 1000.0`.

!!! note "Auto-generated"
    This page is rebuilt from `_factors.py` on every docs build. Do not
    edit `docs/systems.md` directly; edit `docs/scripts/gen_unit_tables.py`.

"""


parts = [HEADER]
for sysname, label, intro in SYSTEMS:
    parts.append(_render_section(sysname, label, intro))
    parts.append("")

with mkdocs_gen_files.open("systems.md", "w") as fh:
    fh.write("\n".join(parts))
