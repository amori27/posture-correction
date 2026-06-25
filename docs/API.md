# API Reference

## `GET /health`

```json
{"status": "ok", "fps": 31}
```

## `POST /analyze`

Upload a frame image for posture analysis.

**Request:** multipart/form-data with `image` field.

**Response:**
```json
{
  "posture": "bad",
  "angles": {
    "neck_tilt": 18.5,
    "shoulder_slope": 5.2,
    "head_forward": 22.1
  },
  "landmarks": [[0.5, 0.3], [0.51, 0.35], ...]
}
```

## WebSocket `/stream`

Real-time posture analysis stream. Sends JSON frames at ~30 FPS.
