import random
from typing import List
from app.models import RiskLevel

# Risk factors untuk setiap kondisi
LIDAH_RISK_FACTORS = {
    "diabet": [
        "Tongue coating thickness abnormality",
        "Color changes in tongue surface",
        "Texture pattern irregularities",
        "Surface moisture level changes",
        "Papillae distribution abnormality",
        "Edge scalloping patterns detected"
    ]
}

KUKU_RISK_FACTORS = {
    "prediabet": [
        "Nail discoloration patterns",
        "Texture irregularities detected",
        "Surface changes observed",
        "Yellow nail syndrome indicators",
        "Nail bed color variations",
        "Onycholysis early signs",
        "Paronychia-like inflammation",
        "Brittle nail characteristics",
        "Growth pattern abnormalities"
    ]
}

def get_risk_factors(lidah_diabetic: bool, kuku_diabetic: bool) -> List[str]:
    """
    Menghasilkan 3 risk factors berdasarkan hasil deteksi
    
    Args:
        lidah_diabetic: True jika lidah terdeteksi diabetes
        kuku_diabetic: True jika kuku terdeteksi diabetes
    
    Returns:
        List berisi 3 risk factors
    """
    factors = []
    
    if lidah_diabetic:
        factors.extend(LIDAH_RISK_FACTORS["diabet"])
    
    if kuku_diabetic:
        factors.extend(KUKU_RISK_FACTORS["prediabet"])
    
    # Jika tidak ada yang terdeteksi, return list kosong atau faktor umum
    if not factors:
        return [
            "No significant abnormalities detected",
            "Normal appearance observed",
            "Healthy indicators present"
        ]
    
    # Ambil 3 faktor secara random jika lebih dari 3
    if len(factors) > 3:
        factors = random.sample(factors, 3)
    elif len(factors) < 3:
        # Jika kurang dari 3, tambahkan faktor umum
        general_factors = [
            "Possible early stage indicators",
            "Minor variations from baseline",
            "Requires further monitoring"
        ]
        factors.extend(general_factors[:3 - len(factors)])
    
    return factors[:3]

def calculate_risk_level(lidah_diabetic: bool, kuku_diabetic: bool) -> tuple[RiskLevel, float]:
    """
    Menghitung risk level berdasarkan hasil deteksi
    
    Args:
        lidah_diabetic: True jika lidah terdeteksi diabetes
        kuku_diabetic: True jika kuku terdeteksi diabetes
    
    Returns:
        Tuple (RiskLevel, risk_percentage)
    """
    if lidah_diabetic and kuku_diabetic:
        # Keduanya terdeteksi = Risiko Tinggi
        return RiskLevel.TINGGI, random.uniform(75, 95)
    elif lidah_diabetic or kuku_diabetic:
        # Salah satu terdeteksi = Risiko Sedang
        return RiskLevel.SEDANG, random.uniform(45, 70)
    else:
        # Tidak ada yang terdeteksi = Risiko Rendah
        return RiskLevel.RENDAH, random.uniform(5, 25)

def get_recommendation(risk_level: RiskLevel) -> str:
    """
    Memberikan rekomendasi berdasarkan risk level
    
    Args:
        risk_level: Level risiko yang terdeteksi
    
    Returns:
        String rekomendasi untuk user
    """
    recommendations = {
        RiskLevel.TINGGI: (
            "High risk detected. We strongly recommend immediate consultation with a healthcare "
            "professional for comprehensive diabetes screening and blood glucose testing. "
            "Early intervention is crucial for better health outcomes."
        ),
        RiskLevel.SEDANG: (
            "Moderate risk detected. Please schedule a medical check-up within the next few weeks. "
            "Consider monitoring your blood sugar levels and maintaining a healthy lifestyle with "
            "balanced diet and regular exercise."
        ),
        RiskLevel.RENDAH: (
            "Low risk detected. Continue maintaining a healthy lifestyle with regular exercise, "
            "balanced nutrition, and adequate sleep. Regular health check-ups are still recommended "
            "for prevention and early detection."
        )
    }
    
    return recommendations.get(risk_level, "Please consult with a healthcare professional.")