import os
import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel

# Get absolute path to this script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Build path to model folder relative to this script
model_path = os.path.join(script_dir, "..", "models", "trained_model.pkl")

# Verify model exists
if not os.path.exists(model_path):
    raise FileNotFoundError(f"Trained model not found at: {os.path.abspath(model_path)}")

# Load the model
model = joblib.load(model_path)

# Initialize FastAPI
app = FastAPI(title="Fraud Detection API")

class Transaction(BaseModel):
    amount: float
    sender_balance: float
    receiver_balance: float
    transaction_hour: int
    day_of_week: int
    last_24h_tx_count: int
    device_change_flag: int
    country_change_flag: int

@app.post("/predict")
def predict_fraud(tx: Transaction):
    tx_df = pd.DataFrame([tx.dict()])
    prediction = model.predict(tx_df)[0]
    return {"is_fraud": int(prediction)}
