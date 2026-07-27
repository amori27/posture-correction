"""Video capture helper utilities."""

import cv2


def list_cameras(max_tested: int = 5) -> list[int]:
    """Probe system video devices and return indices that open successfully.

    Checks camera IDs 0 .. *max_tested* - 1 and returns the list of
    indices whose ``VideoCapture`` can be opened.
    """
    available: list[int] = []
    for i in range(max_tested):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            available.append(i)
            cap.release()
    return available
