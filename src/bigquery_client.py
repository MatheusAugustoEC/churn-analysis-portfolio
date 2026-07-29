from google.cloud import bigquery
from dotenv import load_dotenv
import os

load_dotenv()

def get_client():
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    project_id = os.getenv("PROJECT_ID")
    
    client = bigquery.Client.from_service_account_json(
        credentials_path,
        project=project_id
    )
    return client

def run_query(sql: str):
    client = get_client()
    return client.query(sql).to_dataframe()