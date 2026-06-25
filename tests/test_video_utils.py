from src.utils.video_utils import list_cameras


def test_list_cameras_returns_list():
    cams = list_cameras(3)
    assert isinstance(cams, list)
