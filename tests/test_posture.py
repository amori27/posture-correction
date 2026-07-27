"""Comprehensive tests for the posture-correction system.

Covers angle calculations, posture classification, alert system,
pose engine, config, and utility functions.
"""

import time
from unittest.mock import MagicMock, patch

import numpy as np
import pytest

from src.core.angle_calculator import calculate_angle, classify_posture
from src.core.alert import AlertSystem
from src.core.config import Settings, settings
from src.main import draw_overlay


# ---------------------------------------------------------------------------
# calculate_angle
# ---------------------------------------------------------------------------

class TestCalculateAngle:
    """Unit tests for the geometric angle calculator."""

    def test_90_degrees(self) -> None:
        a = np.array([0.0, 1.0])
        b = np.array([0.0, 0.0])
        c = np.array([1.0, 0.0])
        assert abs(calculate_angle(a, b, c) - 90.0) < 1.0

    def test_180_degrees(self) -> None:
        a = np.array([0.0, 1.0])
        b = np.array([0.0, 0.0])
        c = np.array([0.0, -1.0])
        assert abs(calculate_angle(a, b, c) - 180.0) < 1.0

    def test_0_degrees(self) -> None:
        a = np.array([1.0, 0.0])
        b = np.array([0.0, 0.0])
        c = np.array([2.0, 0.0])
        assert calculate_angle(a, b, c) < 1.0

    def test_45_degrees(self) -> None:
        a = np.array([0.0, 1.0])
        b = np.array([0.0, 0.0])
        c = np.array([1.0, 1.0])
        assert abs(calculate_angle(a, b, c) - 45.0) < 1.0

    def test_symmetry(self) -> None:
        """Swapping a and c should give the same angle."""
        a = np.array([1.0, 2.0])
        b = np.array([0.0, 0.0])
        c = np.array([3.0, 1.0])
        assert abs(calculate_angle(a, b, c) - calculate_angle(c, b, a)) < 1e-6

    def test_colinear_points(self) -> None:
        a = np.array([-1.0, 0.0])
        b = np.array([0.0, 0.0])
        c = np.array([1.0, 0.0])
        assert abs(calculate_angle(a, b, c) - 180.0) < 1.0

    def test_returns_float(self) -> None:
        a = np.array([1.0, 0.0])
        b = np.array([0.0, 0.0])
        c = np.array([0.0, 1.0])
        result = calculate_angle(a, b, c)
        assert isinstance(result, float)


# ---------------------------------------------------------------------------
# classify_posture
# ---------------------------------------------------------------------------

class TestClassifyPosture:
    """Tests for posture classification logic."""

    def test_good_posture(self) -> None:
        assert classify_posture(10.0, 5.0) == "good"

    def test_bad_neck_only(self) -> None:
        assert classify_posture(25.0, 5.0) == "bad"

    def test_bad_shoulder_only(self) -> None:
        assert classify_posture(10.0, 20.0) == "bad"

    def test_bad_both(self) -> None:
        assert classify_posture(25.0, 20.0) == "bad"

    def test_boundary_neck(self) -> None:
        assert classify_posture(20.0, 0.0) == "good"

    def test_boundary_shoulder(self) -> None:
        assert classify_posture(0.0, 15.0) == "good"

    def test_just_above_neck_boundary(self) -> None:
        assert classify_posture(20.01, 0.0) == "bad"

    def test_just_above_shoulder_boundary(self) -> None:
        assert classify_posture(0.0, 15.01) == "bad"


# ---------------------------------------------------------------------------
# AlertSystem
# ---------------------------------------------------------------------------

class TestAlertSystem:
    """Tests for the cooldown-based audio alert system."""

    def test_cooldown_prevents_rapid_fire(self) -> None:
        alert = AlertSystem()
        alert._cooldown = 0.05  # 50 ms for fast tests
        alert._beep = MagicMock()
        alert._last_alert = 0.0

        alert.trigger()
        assert alert._beep.play.call_count == 1

        # Immediately again — should be suppressed
        alert.trigger()
        assert alert._beep.play.call_count == 1

    def test_trigger_after_cooldown(self) -> None:
        alert = AlertSystem()
        alert._cooldown = 0.05
        alert._beep = MagicMock()
        alert._last_alert = 0.0

        alert.trigger()
        time.sleep(0.06)
        alert.trigger()
        assert alert._beep.play.call_count == 2

    def test_no_audio_does_not_raise(self) -> None:
        alert = AlertSystem()
        alert._beep = None
        alert._last_alert = 0.0
        alert._cooldown = 0.0  # no cooldown
        alert.trigger()  # should not raise


# ---------------------------------------------------------------------------
# Settings / Config
# ---------------------------------------------------------------------------

class TestSettings:
    """Verify settings load sensible defaults."""

    def test_default_confidence(self) -> None:
        s = Settings()
        assert 0.0 <= s.min_detection_confidence <= 1.0
        assert 0.0 <= s.min_tracking_confidence <= 1.0

    def test_frame_dimensions_positive(self) -> None:
        assert settings.frame_width > 0
        assert settings.frame_height > 0

    def test_bad_posture_threshold_positive(self) -> None:
        assert settings.bad_posture_threshold_sec > 0


# ---------------------------------------------------------------------------
# draw_overlay
# ---------------------------------------------------------------------------

class TestDrawOverlay:
    """Verify draw_overlay writes on the frame without crashing."""

    def test_good_posture_green(self) -> None:
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        draw_overlay(frame, "good", 10.0, 5.0)
        # top-left pixel area should have green channel > 0
        assert frame[40, 20, 1] > 0

    def test_bad_posture_red(self) -> None:
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        draw_overlay(frame, "bad", 25.0, 20.0)
        assert frame[40, 20, 2] > 0
