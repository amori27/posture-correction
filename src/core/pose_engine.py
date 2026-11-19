"""MediaPipe Pose wrapper with configurable confidence."""

from typing import Any

import cv2
import mediapipe as mp
import numpy as np
from src.core.config import settings

# MediaPipe has moved this result type between releases (``mp.python.solutions``
# on old versions, no such namespace on current ones). Resolve it when present
# and fall back to a generic annotation so the module imports on both APIs.
_pose_solutions = getattr(getattr(getattr(mp, "python", None), "solutions", None), "pose", None)
PoseSolutionOutputs = getattr(_pose_solutions, "PoseSolutionOutputs", Any)


class PoseEngine:
    """Thin wrapper around MediaPipe Pose for real-time landmark detection.

    Configures detection/tracking confidence from the global *settings*.
    """

    def __init__(self) -> None:
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            static_image_mode=False,
            model_complexity=1,
            min_detection_confidence=settings.min_detection_confidence,
            min_tracking_confidence=settings.min_tracking_confidence,
        )

    def process(self, frame: np.ndarray) -> PoseSolutionOutputs:
        """Run pose detection on a BGR *frame* and return results."""
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return self.pose.process(rgb)

    def close(self) -> None:
        """Release MediaPipe resources."""
        self.pose.close()
