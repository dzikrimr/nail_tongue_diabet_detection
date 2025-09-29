from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import os

from app.models import DiabetesAnalysisResponse, HealthCheckResponse
from app.predictor import DiabetesPredictor
from app.utils import get_risk_factors, calculate_risk_level, get_recommendation

# Initialize FastAPI app
app = FastAPI(
    title="Diabetes Detection API",
    description="API untuk deteksi diabetes melalui analisis gambar lidah dan kuku",
    version="1.0.0"
)

# CORS middleware untuk akses dari mobile app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Untuk production, ganti dengan domain spesifik
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize predictor
predictor = None

@app.on_event("startup")
async def startup_event():
    """Load models saat aplikasi startup"""
    global predictor
    try:
        predictor = DiabetesPredictor()
        print("✅ API ready to serve predictions")
    except Exception as e:
        print(f"❌ Error loading models: {e}")
        raise

@app.get("/", response_model=HealthCheckResponse)
async def root():
    """Health check endpoint"""
    return HealthCheckResponse(
        status="healthy",
        message="Diabetes Detection API is running"
    )

@app.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """Detailed health check"""
    if predictor is None:
        raise HTTPException(status_code=503, detail="Models not loaded")
    
    return HealthCheckResponse(
        status="healthy",
        message="All models loaded and ready"
    )

@app.post("/predict/lidah", response_model=DiabetesAnalysisResponse)
async def predict_lidah_only(
    lidah_image: UploadFile = File(..., description="Gambar lidah untuk dianalisis")
):
    """
    Endpoint untuk prediksi diabetes hanya dari gambar lidah
    
    Args:
        lidah_image: File upload gambar lidah
    
    Returns:
        DiabetesAnalysisResponse dengan hasil analisis
    """
    if predictor is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        # Read image bytes
        lidah_bytes = await lidah_image.read()
        
        # Predict
        lidah_result, _ = predictor.predict_both(lidah_bytes=lidah_bytes)
        
        # Calculate risk
        risk_level, risk_percentage = calculate_risk_level(
            lidah_diabetic=lidah_result.is_diabetic,
            kuku_diabetic=False
        )
        
        # Get risk factors
        risk_factors = get_risk_factors(
            lidah_diabetic=lidah_result.is_diabetic,
            kuku_diabetic=False
        )
        
        # Get recommendation
        recommendation = get_recommendation(risk_level)
        
        return DiabetesAnalysisResponse(
            risk_level=risk_level,
            risk_percentage=risk_percentage,
            lidah_result=lidah_result,
            kuku_result=None,
            risk_factors_identified=risk_factors,
            recommendation=recommendation
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

@app.post("/predict/kuku", response_model=DiabetesAnalysisResponse)
async def predict_kuku_only(
    kuku_image: UploadFile = File(..., description="Gambar kuku untuk dianalisis")
):
    """
    Endpoint untuk prediksi diabetes hanya dari gambar kuku
    
    Args:
        kuku_image: File upload gambar kuku
    
    Returns:
        DiabetesAnalysisResponse dengan hasil analisis
    """
    if predictor is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        # Read image bytes
        kuku_bytes = await kuku_image.read()
        
        # Predict
        _, kuku_result = predictor.predict_both(kuku_bytes=kuku_bytes)
        
        # Calculate risk
        risk_level, risk_percentage = calculate_risk_level(
            lidah_diabetic=False,
            kuku_diabetic=kuku_result.is_diabetic
        )
        
        # Get risk factors
        risk_factors = get_risk_factors(
            lidah_diabetic=False,
            kuku_diabetic=kuku_result.is_diabetic
        )
        
        # Get recommendation
        recommendation = get_recommendation(risk_level)
        
        return DiabetesAnalysisResponse(
            risk_level=risk_level,
            risk_percentage=risk_percentage,
            lidah_result=None,
            kuku_result=kuku_result,
            risk_factors_identified=risk_factors,
            recommendation=recommendation
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

@app.post("/predict/both", response_model=DiabetesAnalysisResponse)
async def predict_both(
    lidah_image: UploadFile = File(..., description="Gambar lidah untuk dianalisis"),
    kuku_image: UploadFile = File(..., description="Gambar kuku untuk dianalisis")
):
    """
    Endpoint untuk prediksi diabetes dari kedua gambar (lidah dan kuku)
    
    Args:
        lidah_image: File upload gambar lidah
        kuku_image: File upload gambar kuku
    
    Returns:
        DiabetesAnalysisResponse dengan hasil analisis lengkap
    """
    if predictor is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        # Read image bytes
        lidah_bytes = await lidah_image.read()
        kuku_bytes = await kuku_image.read()
        
        # Predict both
        lidah_result, kuku_result = predictor.predict_both(
            lidah_bytes=lidah_bytes,
            kuku_bytes=kuku_bytes
        )
        
        # Calculate risk
        risk_level, risk_percentage = calculate_risk_level(
            lidah_diabetic=lidah_result.is_diabetic,
            kuku_diabetic=kuku_result.is_diabetic
        )
        
        # Get risk factors
        risk_factors = get_risk_factors(
            lidah_diabetic=lidah_result.is_diabetic,
            kuku_diabetic=kuku_result.is_diabetic
        )
        
        # Get recommendation
        recommendation = get_recommendation(risk_level)
        
        return DiabetesAnalysisResponse(
            risk_level=risk_level,
            risk_percentage=risk_percentage,
            lidah_result=lidah_result,
            kuku_result=kuku_result,
            risk_factors_identified=risk_factors,
            recommendation=recommendation
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

@app.post("/predict", response_model=DiabetesAnalysisResponse)
async def predict_flexible(
    lidah_image: Optional[UploadFile] = File(None, description="Gambar lidah (optional)"),
    kuku_image: Optional[UploadFile] = File(None, description="Gambar kuku (optional)")
):
    """
    Endpoint fleksibel untuk prediksi diabetes
    Bisa menerima salah satu atau kedua gambar
    
    Args:
        lidah_image: File upload gambar lidah (optional)
        kuku_image: File upload gambar kuku (optional)
    
    Returns:
        DiabetesAnalysisResponse dengan hasil analisis
    """
    if predictor is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    if not lidah_image and not kuku_image:
        raise HTTPException(
            status_code=400, 
            detail="At least one image (lidah or kuku) must be provided"
        )
    
    try:
        # Read image bytes if provided
        lidah_bytes = await lidah_image.read() if lidah_image else None
        kuku_bytes = await kuku_image.read() if kuku_image else None
        
        # Predict
        lidah_result, kuku_result = predictor.predict_both(
            lidah_bytes=lidah_bytes,
            kuku_bytes=kuku_bytes
        )
        
        # Calculate risk
        risk_level, risk_percentage = calculate_risk_level(
            lidah_diabetic=lidah_result.is_diabetic if lidah_result else False,
            kuku_diabetic=kuku_result.is_diabetic if kuku_result else False
        )
        
        # Get risk factors
        risk_factors = get_risk_factors(
            lidah_diabetic=lidah_result.is_diabetic if lidah_result else False,
            kuku_diabetic=kuku_result.is_diabetic if kuku_result else False
        )
        
        # Get recommendation
        recommendation = get_recommendation(risk_level)
        
        return DiabetesAnalysisResponse(
            risk_level=risk_level,
            risk_percentage=risk_percentage,
            lidah_result=lidah_result,
            kuku_result=kuku_result,
            risk_factors_identified=risk_factors,
            recommendation=recommendation
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)