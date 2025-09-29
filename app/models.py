from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

class RiskLevel(str, Enum):
    RENDAH = "rendah"
    SEDANG = "sedang"
    TINGGI = "tinggi"

class DetectionType(str, Enum):
    LIDAH = "lidah"
    KUKU = "kuku"

class SingleDetectionResult(BaseModel):
    """Hasil deteksi dari satu model"""
    detection_type: DetectionType
    is_diabetic: bool
    confidence: float
    label: str

class DiabetesAnalysisResponse(BaseModel):
    """Response lengkap analisis diabetes"""
    risk_level: RiskLevel
    risk_percentage: float
    lidah_result: Optional[SingleDetectionResult] = None
    kuku_result: Optional[SingleDetectionResult] = None
    risk_factors_identified: List[str]
    recommendation: str
    
class HealthCheckResponse(BaseModel):
    status: str
    message: str