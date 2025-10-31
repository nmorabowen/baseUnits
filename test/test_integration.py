import pytest
from baseUnits import (
    m, mm, kg, s,
    N, kN, kgf, lbf,
    MPa,
    minutes
)

def test_gravity_and_force_conversion():
    """
    Tests the F = m*a calculation from the 'super example'.
    This confirms the Force dimension is Mass*Length/Time^2.
    """
    g = 9.81 * m / s**2
    mass = 100 * kg
    
    # F = m * a
    weight = mass * g
    
    # Test that the dimension of weight (Mass*Length/Time^2)
    # is correctly seen as convertible to the dimension of N (Force)
    assert weight.to(N).value == pytest.approx(981.0)
    assert weight.to(kN).value == pytest.approx(0.981)
    assert weight.to(lbf).value == pytest.approx(220.554856) # 981 / 4.448

def test_stress_and_pressure_conversion():
    """
    Tests the Stress = F/A calculation from the 'super example'.
    This confirms the Pressure dimension is Mass/(Length*Time^2).
    """
    force = 20 * kgf
    area = 2 * mm**2
    
    stress = force / area
    
    # Test that the dimension of stress (Force/Area)
    # is correctly seen as convertible to the dimension of MPa (Pressure)
    assert stress.to(MPa).value == pytest.approx(98.07)
    
    # Test conversion to a dynamically-created unit
    assert stress.to(N/mm**2).value == pytest.approx(98.07)