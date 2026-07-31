from fastapi import FastAPI
from pydantic import create_model
import pickle
import pandas as pd
import numpy as np
from google.cloud import bigquery
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

app = FastAPI(title="Churn Prediction API", version="1.0.0")

with open('../models/modelo_churn.pkl', 'rb') as f:
    modelo = pickle.load(f)

with open('../models/scaler_churn.pkl', 'rb') as f:
    scaler = pickle.load(f)

feature_names = modelo.feature_names_in_
fields = {name: (float, ...) for name in feature_names}
ClienteData = create_model('ClienteData', **fields)

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