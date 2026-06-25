import numpy as np
from src.core.angle_calculator import calculate_angle, classify_posture


def test_calculate_angle_90_degrees():
    a = np.array([0.0, 1.0])
    b = np.array([0.0, 0.0])
    c = np.array([1.0, 0.0])
    angle = calculate_angle(a, b, c)
    assert abs(angle - 90.0) < 1.0


def test_calculate_angle_180_degrees():
    a = np.array([0.0, 1.0])
    b = np.array([0.0, 0.0])
    c = np.array([0.0, -1.0])
    angle = calculate_angle(a, b, c)
    assert abs(angle - 180.0) < 1.0


def test_calculate_angle_0_degrees():
    a = np.array([1.0, 0.0])
    b = np.array([0.0, 0.0])
    c = np.array([2.0, 0.0])
    angle = calculate_angle(a, b, c)
    assert abs(angle) < 1.0


def test_classify_good():
    assert classify_posture(10.0, 5.0) == "good"


def test_classify_bad_neck():
    assert classify_posture(25.0, 5.0) == "bad"


def test_classify_bad_shoulder():
    assert classify_posture(10.0, 20.0) == "bad"


def test_classify_bad_both():
    assert classify_posture(25.0, 20.0) == "bad"
