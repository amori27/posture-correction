from src.core.config import settings


def test_settings_defaults():
    assert settings.min_detection_confidence == 0.7
    assert settings.min_tracking_confidence == 0.5
    assert settings.bad_posture_threshold_sec == 5
    assert settings.camera_id == 0
