from pydantic import BaseModel


class AnalysisResult(BaseModel):
    posture: str
    neck_tilt: float
    shoulder_slope: float


class HealthResponse(BaseModel):
    status: str
    fps: float
