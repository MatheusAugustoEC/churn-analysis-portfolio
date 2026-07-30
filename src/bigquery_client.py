from google.cloud import bigquery
from dotenv import load_dotenv
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, '.env'))

def get_client():
    credentials_path = os.path.join(BASE_DIR, os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))
    project_id = os.getenv("PROJECT_ID")
    
    client = bigquery.Client.from_service_account_json(
        credentials_path,
        project=project_id
    )
    return client

def run_query(sql: str):
    client = get_client()
    return client.query(sql).to_dataframe()