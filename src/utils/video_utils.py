import cv2


def list_cameras(max_tested: int = 5) -> list[int]:
    available = []
    for i in range(max_tested):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            available.append(i)
            cap.release()
    return available
