import pickle
import pandas as pd
from google.cloud import bigquery
from dotenv import load_dotenv
import os

load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_client():
    credentials_path = os.path.join(BASE_DIR, os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))
    project_id = os.getenv("PROJECT_ID")
    return bigquery.Client.from_service_account_json(credentials_path, project=project_id)

def load_model():
    with open(os.path.join(BASE_DIR, 'models/modelo_churn.pkl'), 'rb') as f:
        return pickle.load(f)

def check_data_quality(client):
    result = client.query("""
        SELECT COUNT(*) as erros
        FROM `churn_dataset.vw_data_quality`
    """).to_dataframe()
    
    erros = result['erros'][0]
    
    if erros > 0:
        raise ValueError(f"Pipeline abortado: {erros} registros inválidos encontrados em churn_dataset.vw_data_quality")
    
    print("✅ Validação de qualidade ok — nenhum registro inválido encontrado.")

def run_pipeline():
    client = get_client()
    check_data_quality(client)
    check_data_quality(client)
    modelo = load_model()

    df = client.query("""
        SELECT *
        FROM `churn_dataset.customers_cleaned`
    """).to_dataframe()

    X = df.drop(columns=['customerID', 'Churn', 'tenure_group', 'TotalCharges', 'AvgMonthlySpend'])
    
    bool_cols = X.select_dtypes(include='boolean').columns
    X[bool_cols] = X[bool_cols].astype(int)
    
    colunas_categoricas = X.select_dtypes(include='str').columns.tolist()
    X = pd.get_dummies(X, columns=colunas_categoricas, drop_first=True)
    X = X.astype(float)

    probabilidades = modelo.predict_proba(X)[:, 1]
    
    resultado = pd.DataFrame({
        'customerID': df['customerID'],
        'probabilidade_churn': (probabilidades * 100).round(2),
        'risco': ['Alto' if p >= 0.7 else 'Médio' if p >= 0.4 else 'Baixo' for p in probabilidades],
        'MonthlyCharges': df['MonthlyCharges'],
        'Contract': df['Contract'],
        'tenure': df['tenure'],
        'InternetService': df['InternetService'],
        'churn_real': df['Churn'].astype(int),
        'PaymentMethod': df['PaymentMethod']
    })

    job_config = bigquery.LoadJobConfig(write_disposition='WRITE_TRUNCATE')
    client.load_table_from_dataframe(
        resultado,
        'churn_dataset.churn_predictions',
        job_config=job_config
    ).result()

    print(f'Pipeline executado com sucesso! {len(resultado)} clientes processados.')

if __name__ == '__main__':
    print("Iniciando pipeline...")
    run_pipeline()