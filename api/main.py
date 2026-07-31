from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import pandas as pd
import numpy as np
from google.cloud import bigquery
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

app = FastAPI(title="Churn Prediction API", version="1.0.0")

# Carrega modelo e scaler
with open('../models/modelo_churn.pkl', 'rb') as f:
    modelo = pickle.load(f)

with open('../models/scaler_churn.pkl', 'rb') as f:
    scaler = pickle.load(f)

class ClienteData(BaseModel):
    SeniorCitizen: int
    Partner: int
    Dependents: int
    tenure: float
    PhoneService: int
    PaperlessBilling: int
    MonthlyCharges: float
    gender_Male: int
    MultipleLines_Yes: int
    InternetService_Fiber_optic: int
    InternetService_No: int
    OnlineSecurity_Yes: int
    OnlineBackup_Yes: int
    DeviceProtection_Yes: int
    TechSupport_Yes: int
    StreamingTV_Yes: int
    StreamingMovies_Yes: int
    Contract_One_year: int
    Contract_Two_year: int
    PaymentMethod_Credit_card_automatic: int
    PaymentMethod_Electronic_check: int
    PaymentMethod_Mailed_check: int

@app.get("/")
def root():
    return {"status": "Churn Prediction API online"}

@app.post("/predict")
def predict(cliente: ClienteData):
    dados = pd.DataFrame([cliente.dict()])
    dados[['tenure', 'MonthlyCharges']] = scaler.transform(dados[['tenure', 'MonthlyCharges']])
    probabilidade = modelo.predict_proba(dados)[:, 1][0]
    churn = int(probabilidade >= 0.5)
    return {
        "churn": churn,
        "probabilidade_churn": round(float(probabilidade), 4),
        "risco": "Alto" if probabilidade >= 0.7 else "Médio" if probabilidade >= 0.4 else "Baixo"
    }
