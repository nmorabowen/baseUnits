"""Pin every inch-pound and gravitational factor to its exact definition.

The library once shipped four-significant-figure imperial factors
(``lbf = 4.448``, ``ksi = 6.895``, ``kgf_cm2 = 0.09807``). That is a ~1e-4
relative error, which is large enough to move a design-code capacity check in
the last printed digit — ACI 318 and AISC 360 are written against the exact
conversions, so a rounded factor makes a hand check and a library check
disagree for no physical reason.

Every expected value below is recomputed with :class:`decimal.Decimal` from the
four exactly-defined constants, so these tests encode the *definitions* rather
than copies of the literals they are guarding.
"""

from decimal import Decimal as D
from decimal import getcontext

import pytest

from baseUnits import _factors as _f

getcontext().prec = 60

# The four exact definitions everything else descends from.
INCH = D("0.0254")  # international inch, exact
LB = D("0.45359237")  # international avoirdupois pound, exact
G0 = D("9.80665")  # standard gravity, exact
LBF = LB * G0  # = 4.4482216152605 N, exact

FT = INCH * 12


def _exact(value: D) -> float:
    """Correctly-rounded double of an exact decimal value."""
    return float(value)


# (dimension dict, unit name, exact SI value)
EXACT_FACTORS = [
    # Length — in metres
    ("LENGTH", "inches", INCH),
    ("LENGTH", "ft", FT),
    ("LENGTH", "yard", FT * 3),
    ("LENGTH", "mile", FT * 5280),
    # Force — in newtons
    ("FORCE", "lbf", LBF),
    ("FORCE", "kip", LBF * 1000),
    ("FORCE", "kgf", G0),
    ("FORCE", "tf", G0 * 1000),
    # Mass — in kilograms
    ("MASS", "lb", LB),
    ("MASS", "oz", LB / 16),
    # Pressure — in pascals
    ("PRESSURE", "psi", LBF / INCH**2),
    ("PRESSURE", "ksi", LBF * 1000 / INCH**2),
    ("PRESSURE", "kgf_cm2", G0 / D("0.01") ** 2),
    # Power — in watts (1 HP = 550 ft-lbf/s)
    ("POWER", "HP", D(550) * FT * LBF),
    # Density — in kg/m^3
    ("DENSITY", "lb_per_ft3", LB / FT**3),
    # Unit weight — in N/m^3
    ("UNIT_WEIGHT", "kgf_per_m3", G0),
]


@pytest.mark.parametrize("dimension,name,exact", EXACT_FACTORS)
def test_factor_is_exact(dimension, name, exact):
    """Each stored factor is the correctly-rounded double of its definition."""
    stored = getattr(_f, dimension)[name]
    assert stored == _exact(exact), (
        f"_factors.{dimension}['{name}'] is {stored!r}, expected the exact value {_exact(exact)!r}"
    )


def test_lbf_is_lb_times_standard_gravity():
    """The pound-force is defined as one pound mass under standard gravity."""
    assert _f.FORCE["lbf"] == _exact(LBF)
    assert _exact(LB * G0) == _exact(D("4.4482216152605"))


@pytest.mark.parametrize(
    "dimension,big,small,ratio",
    [
        ("FORCE", "kip", "lbf", 1000),
        ("FORCE", "tf", "kgf", 1000),
        ("PRESSURE", "ksi", "psi", 1000),
    ],
)
def test_kilo_prefixed_pairs(dimension, big, small, ratio):
    """A kip is exactly 1000 lbf, a ksi exactly 1000 psi, a tf exactly 1000 kgf."""
    table = getattr(_f, dimension)
    assert table[big] == pytest.approx(table[small] * ratio, rel=1e-15)


def test_pressure_units_follow_from_force_and_area():
    """psi and ksi are force-over-area identities, not independent numbers."""
    lbf_si = _f.FORCE["lbf"]
    inch_si = _f.LENGTH["inches"]
    assert _f.PRESSURE["psi"] == pytest.approx(lbf_si / inch_si**2, rel=1e-15)
    assert _f.PRESSURE["ksi"] == pytest.approx(_f.FORCE["kip"] / inch_si**2, rel=1e-15)


def test_kgf_cm2_follows_from_kgf_and_area():
    kgf_si = _f.FORCE["kgf"]
    cm_si = _f.LENGTH["cm"]
    assert _f.PRESSURE["kgf_cm2"] == pytest.approx(kgf_si / cm_si**2, rel=1e-15)


def test_no_factor_is_a_four_figure_rounding():
    """Guard against the specific rounded values this library used to ship."""
    known_bad = {
        ("FORCE", "lbf"): 4.448,
        ("FORCE", "kip"): 4448.0,
        ("FORCE", "kgf"): 9.807,
        ("FORCE", "tf"): 9807.0,
        ("MASS", "lb"): 0.4536,
        ("PRESSURE", "ksi"): 6.895e6,
        ("PRESSURE", "kgf_cm2"): 0.09807e6,
        ("UNIT_WEIGHT", "kgf_per_m3"): 9.807,
    }
    for (dimension, name), bad in known_bad.items():
        assert getattr(_f, dimension)[name] != bad, (
            f"_factors.{dimension}['{name}'] regressed to the rounded value {bad!r}"
        )


# --- The two layers must agree ------------------------------------------------

# Checked-layer base unit for each dimension (see baseUnits.checked._derived).
CHECKED_BASES = [
    ("LENGTH", "mm"),
    ("FORCE", "N"),
    ("MASS", "tonne"),
    ("TIME", "s"),
    ("PRESSURE", "MPa"),
    ("ENERGY", "mJ"),
    ("POWER", "mJ_s"),
    ("DENSITY", "tonne_per_mm3"),
    ("UNIT_WEIGHT", "N_per_mm3"),
    ("ANGLE", "radian"),
    ("TEMPERATURE", "K"),
]


@pytest.mark.parametrize("dimension,base", CHECKED_BASES)
def test_checked_layer_matches_float_layer(dimension, base):
    """Every unit in _factors exists in the checked layer with the derived factor.

    This is the anti-drift guard: the checked layer previously hard-coded its
    own copies of these numbers and fell four significant figures behind.
    """
    import baseUnits.checked as checked

    table = getattr(_f, dimension)
    base_si = table[base]
    for name, si in table.items():
        unit = getattr(checked, name, None)
        assert unit is not None, f"baseUnits.checked is missing '{name}' ({dimension})"
        assert unit.factor == pytest.approx(si / base_si, rel=1e-15), (
            f"checked.{name}.factor is {unit.factor!r}, expected {si / base_si!r}"
        )


def test_checked_imperial_stress_roundtrip():
    """60 ksi through the checked layer lands on the exact MPa value."""
    from baseUnits.checked import MPa, ksi

    expected = _exact(D(60) * LBF * 1000 / INCH**2 / D(10) ** 6)
    assert (60 * ksi).to(MPa).value == pytest.approx(expected, rel=1e-15)


def test_checked_psi_is_exposed():
    """psi was absent from the checked layer entirely; ACI 318 is written in it."""
    from baseUnits.checked import MPa, psi

    assert (1000 * psi).to(MPa).value == pytest.approx(
        _exact(D(1000) * LBF / INCH**2 / D(10) ** 6), rel=1e-15
    )
