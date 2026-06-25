# Posture Correction System — Architecture

## Overview

Real-time posture analysis using webcam feed. MediaPipe Pose estimates 33 body landmarks; joint angles (neck-shoulder-hip, shoulder-elbow-wrist) are calculated geometrically to classify posture as correct/incorrect.

## Stack

| Layer | Technology |
|---|---|
| Pose Estimation | MediaPipe Pose (Lite model for speed) |
| Computer Vision | OpenCV |
| Angle Calculation | NumPy (vector dot-product geometry) |
| Alert System | PyGame audio + visual overlay |

## Data Flow

```
Webcam Feed ──> MediaPipe Pose ──> Landmarks ──> Angle Calc ──> Classifier
                                                                    │
                                                          ┌─────────▼────────┐
                                                          │ Good (green)     │
                                                          │ Bad  (red + beep)│
                                                          └──────────────────┘
```

## Angle Definitions

- **Neck angle**: shoulder-midhip vector vs vertical
- **Shoulder slope**: left shoulder - right shoulder delta Y
- **Head tilt**: nose-shoulder vector vs vertical
