"""Pydantic models for the posture-correction API."""

from pydantic import BaseModel


class AnalysisResult(BaseModel):
    """Result of a single posture analysis frame."""

    posture: str
    neck_tilt: float
    shoulder_slope: float


class HealthResponse(BaseModel):
    """Health-check response payload."""

    status: str
    fps: float
