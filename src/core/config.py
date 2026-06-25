import os


class Settings:
    min_detection_confidence: float = float(
        os.getenv("MIN_DETECTION_CONFIDENCE", "0.7")
    )
    min_tracking_confidence: float = float(
        os.getenv("MIN_TRACKING_CONFIDENCE", "0.5")
    )
    bad_posture_threshold_sec: int = int(
        os.getenv("BAD_POSTURE_THRESHOLD_SEC", "5")
    )
    camera_id: int = int(os.getenv("CAMERA_ID", "0"))
    frame_width: int = int(os.getenv("FRAME_WIDTH", "640"))
    frame_height: int = int(os.getenv("FRAME_HEIGHT", "480"))


settings = Settings()
