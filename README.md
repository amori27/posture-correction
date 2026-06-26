# Posture Correction System

[![CI/CD](https://github.com/amori27/posture-correction/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/amori27/posture-correction/actions)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> Real-time posture analysis using webcam. MediaPipe pose estimation with geometric angle calculations — not black-box ML — to detect poor ergonomics and trigger alerts.

## Architecture

```
Webcam ──> MediaPipe Pose ──> 33 Landmarks ──> Angle Calculator ──> Classifier ──> Overlay + Beep
```

## Key Features

- **Geometric angle math** — neck-shoulder-hip, shoulder-elbow-wrist angles calculated via vector dot product
- **30+ FPS** on mid-tier hardware using MediaPipe Lite model
- **Configurable thresholds** — detection confidence, bad posture duration
- **Audio alerts** — beep triggers after sustained bad posture (configurable delay)

## Requirements

- Python 3.8+
- Webcam

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Install MediaPipe (heavy ~200MB with model weights)
pip install mediapipe

# 3. Run
python -m src.main
```

Press `q` to quit.

## Angle Thresholds

| Metric | Good | Bad |
|---|---|---|
| Neck Tilt | < 20° | ≥ 20° |
| Shoulder Slope | < 15 | ≥ 15 |

## License

MIT
