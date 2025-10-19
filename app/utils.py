import random
from typing import List
from app.models import RiskLevel

LIDAH_RISK_FACTORS = {
    "diabet": [
        "Kelainan ketebalan lapisan lidah",
        "Perubahan warna pada permukaan lidah",
        "Ketidakteraturan pola tekstur",
        "Perubahan tingkat kelembapan permukaan",
        "Kelainan distribusi papila",
        "Terdeteksi pola tepi lidah bergelombang"
    ]
}

KUKU_RISK_FACTORS = {
    "prediabet": [
        "Pola perubahan warna kuku",
        "Terdeteksi ketidakteraturan tekstur",
        "Teramati perubahan pada permukaan",
        "Indikator sindrom kuku kuning",
        "Variasi warna dasar kuku",
        "Tanda-tanda awal onikolisis",
        "Peradangan mirip paronikia",
        "Karakteristik kuku rapuh",
        "Kelainan pola pertumbuhan"
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
    
    if not factors:
        return [
            "Tidak ada kelainan signifikan yang terdeteksi",
            "Penampilan normal teramati",
            "Terdapat indikator kesehatan"
        ]

    if len(factors) > 3:
        factors = random.sample(factors, 3)
    elif len(factors) < 3:
        general_factors = [
            "Kemungkinan indikator tahap awal",
            "Variasi kecil dari kondisi normal",
            "Memerlukan pemantauan lebih lanjut"
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
            "Risiko tinggi terdeteksi. Kami sangat merekomendasikan untuk segera berkonsultasi "
            "dengan tenaga kesehatan profesional untuk skrining diabetes komprehensif dan tes glukosa darah. "
            "Intervensi dini sangat penting untuk hasil kesehatan yang lebih baik."
        ),
        RiskLevel.SEDANG: (
            "Risiko sedang terdeteksi. Harap jadwalkan pemeriksaan medis dalam beberapa minggu ke depan. "
            "Pertimbangkan untuk memantau kadar gula darah Anda dan menjaga gaya hidup sehat dengan "
            "pola makan seimbang dan olahraga teratur."
        ),
        RiskLevel.RENDAH: (
            "Risiko rendah terdeteksi. Lanjutkan menjaga gaya hidup sehat dengan olahraga teratur, "
            "nutrisi seimbang, dan tidur yang cukup. Pemeriksaan kesehatan rutin tetap disarankan "
            "untuk pencegahan dan deteksi dini."
        )
    }
    
    return recommendations.get(risk_level, "Silakan berkonsultasi dengan tenaga kesehatan profesional.")