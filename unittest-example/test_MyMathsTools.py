from MyMathsTools import deg2rad, sin_deg, cos_deg
import math
import pytest


def test_deg2rad():
    assert deg2rad(0) == 0
    assert deg2rad(90) == math.pi / 2


def test_sin_deg():
    assert sin_deg(0) == 0
    assert sin_deg(90) == 1
    assert sin_deg(-30) == pytest.approx(-0.5)
    assert sin_deg(-30, inverse=True) == pytest.approx(-2)


def test_cos_deg():
    assert cos_deg(0) == 1
