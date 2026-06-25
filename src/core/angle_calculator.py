"""Geometric joint angle calculations from MediaPipe landmarks."""

import numpy as np


def calculate_angle(a: np.ndarray, b: np.ndarray, c: np.ndarray) -> float:
    ba = a - b
    bc = c - b
    cosine = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc) + 1e-6)
    angle = np.degrees(np.arccos(np.clip(cosine, -1.0, 1.0)))
    return angle


def neck_tilt(landmarks, mp_pose) -> float:
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
    return calculate_angle(left_ear, mid_shoulder, vertical)


def shoulder_slope(landmarks, mp_pose) -> float:
    left = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].y
    right = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER].y
    return abs(left - right) * 100


def classify_posture(neck: float, slope: float) -> str:
    if neck > 20 or slope > 15:
        return "bad"
    return "good"
