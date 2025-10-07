import tensorflow as tf
import numpy as np
from PIL import Image
import io
from typing import Tuple, Optional
from app.models import SingleDetectionResult, DetectionType

class DiabetesPredictor:
    """Class untuk melakukan prediksi diabetes dari gambar lidah dan kuku"""
    
    def __init__(self, lidah_model_path: str = "models/lidah_model.h5", 
                 kuku_model_path: str = "models/kuku_model.h5"):
        """
        Inisialisasi predictor dengan loading model
        
        Args:
            lidah_model_path: Path ke model lidah
            kuku_model_path: Path ke model kuku
        """
        print("Loading models...")
        self.lidah_model = tf.keras.models.load_model(lidah_model_path)
        self.kuku_model = tf.keras.models.load_model(kuku_model_path)
        print("✅ Models loaded successfully")
        
        self.img_size = (224, 224)
    
    def preprocess_image(self, image_bytes: bytes) -> np.ndarray:
        """
        Preprocessing gambar untuk prediksi
        
        Args:
            image_bytes: Bytes dari gambar yang diupload
        
        Returns:
            Numpy array yang sudah dipreprocess
        """
        # Load image dari bytes
        img = Image.open(io.BytesIO(image_bytes))
        
        # Convert ke RGB jika perlu
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Resize
        img = img.resize(self.img_size)
        
        # Convert ke array dan normalize
        img_array = np.array(img) / 255.0
        
        # Add batch dimension
        img_array = np.expand_dims(img_array, axis=0)
        
        return img_array
    
    def predict_lidah(self, image_bytes: bytes) -> SingleDetectionResult:
        """
        Prediksi diabetes dari gambar lidah
        
        Args:
            image_bytes: Bytes dari gambar lidah
        
        Returns:
            SingleDetectionResult dengan hasil prediksi
        """
        # Preprocess
        img_array = self.preprocess_image(image_bytes)
        
        # Predict
        prediction = self.lidah_model.predict(img_array, verbose=0)
        confidence_score = float(prediction[0][0])
        
        # Interpretasi hasil (sigmoid output)
        # prediction < 0.5 = diabet, >= 0.5 = non_diabet
        is_diabetic = confidence_score < 0.5
        label = "prediabet" if is_diabetic else "non_diabet"
        
        # Adjust confidence untuk interpretasi yang benar
        confidence = (1 - confidence_score) if is_diabetic else confidence_score
        
        return SingleDetectionResult(
            detection_type=DetectionType.LIDAH,
            is_diabetic=is_diabetic,
            confidence=confidence,
            label=label
        )
    
    def predict_kuku(self, image_bytes: bytes) -> SingleDetectionResult:
        """
        Prediksi diabetes dari gambar kuku
        
        Args:
            image_bytes: Bytes dari gambar kuku
        
        Returns:
            SingleDetectionResult dengan hasil prediksi
        """
        # Preprocess
        img_array = self.preprocess_image(image_bytes)
        
        # Predict
        prediction = self.kuku_model.predict(img_array, verbose=0)
        confidence_score = float(prediction[0][0])
        
        # Interpretasi hasil (sigmoid output)
        # prediction >= 0.5 = prediabet, < 0.5 = non_diabet
        is_diabetic = confidence_score >= 0.5
        label = "prediabet" if is_diabetic else "non_diabet"
        
        # Confidence
        confidence = confidence_score if is_diabetic else (1 - confidence_score)
        
        return SingleDetectionResult(
            detection_type=DetectionType.KUKU,
            is_diabetic=is_diabetic,
            confidence=confidence,
            label=label
        )
    
    def predict_both(self, lidah_bytes: Optional[bytes] = None, 
                    kuku_bytes: Optional[bytes] = None) -> Tuple[Optional[SingleDetectionResult], 
                                                                   Optional[SingleDetectionResult]]:
        """
        Prediksi dari kedua gambar (lidah dan kuku)
        
        Args:
            lidah_bytes: Bytes gambar lidah (optional)
            kuku_bytes: Bytes gambar kuku (optional)
        
        Returns:
            Tuple (lidah_result, kuku_result)
        """
        lidah_result = None
        kuku_result = None
        
        if lidah_bytes:
            lidah_result = self.predict_lidah(lidah_bytes)
        
        if kuku_bytes:
            kuku_result = self.predict_kuku(kuku_bytes)
        
        return lidah_result, kuku_result