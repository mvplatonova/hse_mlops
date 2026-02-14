from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
from typing import List

app = FastAPI(title="ML Service", version="1.0")

# Простая "ML-модель" - линейная регрессия
class PredictionInput(BaseModel):
    features: List[float]

class PredictionOutput(BaseModel):
    prediction: float

# Имитация обученной модели (коэффициенты)
MODEL_WEIGHTS = np.array([0.5, 1.2, -0.3, 0.8])
MODEL_BIAS = 2.5

@app.get("/")
def read_root():
    return {
        "message": "ML Service is running",
        "version": "1.0",
        "endpoints": ["/predict", "/health"]
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/predict", response_model=PredictionOutput)
def predict(data: PredictionInput):
    """
    Простое предсказание: y = w1*x1 + w2*x2 + ... + bias
    """
    features = np.array(data.features)
    
    # Убедимся, что количество признаков совпадает
    if len(features) != len(MODEL_WEIGHTS):
        return {
            "prediction": 0.0,
            "error": f"Expected {len(MODEL_WEIGHTS)} features, got {len(features)}"
        }
    
    prediction = np.dot(features, MODEL_WEIGHTS) + MODEL_BIAS
    
    return {"prediction": float(prediction)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
