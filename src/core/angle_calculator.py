"""Geometric joint angle calculations from MediaPipe landmarks."""

import numpy as np
import mediapipe as mp


def calculate_angle(a: np.ndarray, b: np.ndarray, c: np.ndarray) -> float:
    """Calculate the angle (in degrees) between three 2-D points at vertex *b*.

    Uses the dot-product formula:
        cos(theta) = (ba . bc) / (|ba| * |bc|)

    Returns a value in [0, 180].
    """
    ba = a - b
    bc = c - b
    cosine = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc) + 1e-6)
    angle = np.degrees(np.arccos(np.clip(cosine, -1.0, 1.0)))
    return float(angle)


def neck_tilt(landmarks: list, mp_pose: mp.solutions.pose) -> float:
    """Compute the forward head-tilt angle (degrees).

    Measures the angle between the left ear, midpoint of the shoulders,
    and a vertical reference line.  Larger values indicate more forward tilt.
    """
    left_shoulder = np.array([
        landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].x,
        landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].y,
    ])
    right_shoulder = np.array([
        landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER].x,
        landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER].y,
    ])
    left_ear = np.array([
        landmarks[mp_pose.PoseLandmark.LEFT_EAR].x,
        landmarks[mp_pose.PoseLandmark.LEFT_EAR].y,
    ])
    mid_shoulder = (left_shoulder + right_shoulder) / 2
    vertical = np.array([mid_shoulder[0], mid_shoulder[1] - 1.0])
    return float(calculate_angle(left_ear, mid_shoulder, vertical))


def shoulder_slope(landmarks: list, mp_pose: mp.solutions.pose) -> float:
    """Return the shoulder slope as a percentage difference in Y-coordinates.

    A perfectly level pair of shoulders returns 0.0.
    """
    left = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].y
    right = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER].y
    return abs(left - right) * 100


def classify_posture(neck: float, slope: float) -> str:
    """Classify posture as ``"good"`` or ``"bad"`` based on thresholds.

    *neck* > 20 degrees **or** *slope* > 15% triggers a "bad" classification.
    """
    if neck > 20 or slope > 15:
        return "bad"
    return "good"
