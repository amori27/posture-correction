"""Real-time posture correction application."""

import cv2
import numpy as np
import mediapipe as mp
from src.core.config import settings
from src.core.pose_engine import PoseEngine
from src.core.angle_calculator import neck_tilt, shoulder_slope, classify_posture
from src.core.alert import AlertSystem


def draw_overlay(frame, posture: str, neck: float, slope: float):
    color = (0, 255, 0) if posture == "good" else (0, 0, 255)
    cv2.putText(frame, f"Posture: {posture}", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
    cv2.putText(frame, f"Neck: {neck:.1f}deg", (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
    cv2.putText(frame, f"Shoulder: {slope:.1f}", (20, 110),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)


def main():
    cap = cv2.VideoCapture(settings.camera_id)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, settings.frame_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, settings.frame_height)

    engine = PoseEngine()
    alert = AlertSystem()
    mp_draw = mp.solutions.drawing_utils

    bad_start = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        results = engine.process(frame)

        if results.pose_landmarks:
            lm = results.pose_landmarks.landmark
            neck = neck_tilt(lm, mp.solutions.pose)
            slope = shoulder_slope(lm, mp.solutions.pose)
            posture = classify_posture(neck, slope)

            draw_overlay(frame, posture, neck, slope)
            mp_draw.draw_landmarks(frame, results.pose_landmarks,
                                   mp.solutions.pose.POSE_CONNECTIONS)

            if posture == "bad":
                if bad_start is None:
                    bad_start = cv2.getTickCount()
                elapsed = (cv2.getTickCount() - bad_start) / cv2.getTickFrequency()
                if elapsed > settings.bad_posture_threshold_sec:
                    alert.trigger()
            else:
                bad_start = None

        cv2.imshow("Posture Correction", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    engine.close()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
