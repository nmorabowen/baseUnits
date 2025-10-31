import pytest
import math
from baseUnits import (
    m, mm, ft, inches,
    kg, tonne, lb, gr,
    s, h,
    N, kgf, lbf,
    MPa, ksi, Pa,
    J, cal, mJ,
    W, HP,
    radian, degree,
    minutes
)

def test_length_conversions():
    assert (1 * m).to(mm).value == 1000.0
    assert (1 * ft).to(mm).value == pytest.approx(304.8)
    assert (1 * inches).to(mm).value == pytest.approx(25.4)

def test_mass_conversions():
    assert (1 * kg).to(tonne).value == 0.001
    assert (1 * lb).to(gr).value == pytest.approx(453600000.0 * 1e-6) # 453.6 gr
    assert (1000 * kg).to(tonne).value == 1.0

def test_force_conversions():
    assert (1 * kgf).to(N).value == pytest.approx(9.807)
    assert (1 * lbf).to(N).value == pytest.approx(4.448)

def test_pressure_conversions():
    assert (1 * MPa).to(Pa).value == 1_000_000.0
    assert (1 * ksi).to(MPa).value == pytest.approx(6.895)
    assert (1 * (N/m**2)).to(Pa).value == pytest.approx(1.0)
    assert (1 * (N/mm**2)).to(MPa).value == pytest.approx(1.0)

def test_energy_conversions():
    assert (1 * J).to(mJ).value == 1000.0
    assert (1 * cal).to(J).value == pytest.approx(4.184)

def test_power_conversions():
    assert (1 * W).to(mJ/s).value == 1000.0
    assert (1 * HP).to(W).value == pytest.approx(745.7)

def test_time_conversions():
    assert (1 * h).to(s).value == 3600.0
    assert (1 * h).to(minutes).value == 60.0

def test_angle_conversions():
    assert (180 * degree).to(radian).value == pytest.approx(math.pi)