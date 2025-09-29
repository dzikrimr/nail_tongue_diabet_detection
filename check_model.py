import tensorflow as tf
from tensorflow.keras.models import load_model

for name in ["lidah_model.h5", "kuku_model.h5"]:
    print(f"\n=== Checking {name} ===")
    try:
        model = load_model(f"models/{name}")
        model.summary()
    except Exception as e:
        print(f"❌ Error loading {name}: {e}")
