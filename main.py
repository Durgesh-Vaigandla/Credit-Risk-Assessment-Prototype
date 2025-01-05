# main.py
from fastapi import FastAPI, HTTPException, Depends, Security
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
from datetime import datetime
import numpy as np
import pandas as pd
import xgboost as xgb
from typing import List, Optional
import joblib

app = FastAPI(title="Credit Risk Assessment API")

# Security
API_KEY_HEADER = APIKeyHeader(name="X-API-Key")
API_KEYS = ["test_key_123"]  # In production, use secure key storage

# Data Models
class UtilityBill(BaseModel):
    provider: str
    amount: float
    due_date: datetime
    payment_date: Optional[datetime]
    status: str

class BankTransaction(BaseModel):
    date: datetime
    amount: float
    type: str
    category: str
    balance_after: float

class CreditRequest(BaseModel):
    user_id: str
    cibil_score: float
    utility_bills: List[UtilityBill]
    bank_transactions: List[BankTransaction]
    monthly_income: float
    rental_payment: float

class CreditScore(BaseModel):
    user_id: str
    risk_score: float
    confidence: float
    factors: dict
    timestamp: datetime

# Feature Engineering
def calculate_utility_score(bills: List[UtilityBill]) -> float:
    if not bills:
        return 0.0
    
    on_time_payments = sum(1 for bill in bills 
                          if bill.payment_date and bill.payment_date <= bill.due_date)
    return (on_time_payments / len(bills)) * 100

def analyze_bank_transactions(transactions: List[BankTransaction]) -> dict:
    df = pd.DataFrame([t.dict() for t in transactions])
    
    metrics = {
        'avg_balance': df['balance_after'].mean(),
        'income_stability': df[df['type'] == 'credit']['amount'].std(),
        'expense_ratio': (
            df[df['type'] == 'debit']['amount'].sum() / 
            df[df['type'] == 'credit']['amount'].sum()
        )
    }
    return metrics

# Risk Assessment Model
class CreditRiskModel:
    def __init__(self):
        # In production, load a trained model
        self.model = xgb.XGBRegressor(
            max_depth=6,
            learning_rate=0.01,
            n_estimators=100
        )
    
    def preprocess_features(self, request: CreditRequest) -> pd.DataFrame:
        utility_score = calculate_utility_score(request.utility_bills)
        bank_metrics = analyze_bank_transactions(request.bank_transactions)
        
        features = {
            'cibil_score': request.cibil_score,
            'utility_score': utility_score,
            'avg_balance': bank_metrics['avg_balance'],
            'income_stability': bank_metrics['income_stability'],
            'expense_ratio': bank_metrics['expense_ratio'],
            'income_to_rent_ratio': request.rental_payment / request.monthly_income
        }
        
        return pd.DataFrame([features])
    
    def predict(self, features: pd.DataFrame) -> tuple:
        # In MVP, using a simplified scoring method
        weighted_score = (
            features['cibil_score'] * 0.3 +
            features['utility_score'] * 0.25 +
            (1 - features['expense_ratio']) * 0.25 +
            (1 - features['income_to_rent_ratio']) * 0.2
        ).iloc[0]
        
        confidence = 0.8  # In production, use model confidence scores
        return weighted_score, confidence

# Initialize model
model = CreditRiskModel()

# Security dependency
async def verify_api_key(api_key: str = Security(API_KEY_HEADER)):
    if api_key not in API_KEYS:
        raise HTTPException(
            status_code=403,
            detail="Invalid API key"
        )
    return api_key

# Endpoints
@app.post("/credit-score", response_model=CreditScore)
async def get_credit_score(
    request: CreditRequest,
    api_key: str = Depends(verify_api_key)
):
    try:
        # Process features
        features = model.preprocess_features(request)
        
        # Get prediction
        risk_score, confidence = model.predict(features)
        
        # Calculate factor importance
        factors = {
            'cibil_score': 0.3,
            'utility_payments': 0.25,
            'bank_transactions': 0.25,
            'income_and_rent': 0.2
        }
        
        return CreditScore(
            user_id=request.user_id,
            risk_score=float(risk_score),
            confidence=confidence,
            factors=factors,
            timestamp=datetime.now()
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing request: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
