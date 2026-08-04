from google.cloud import bigquery
from google.oauth2 import service_account
import os
import streamlit as st

def get_client():
    project_id = os.getenv("PROJECT_ID", "churn-analysis-portfolio")
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"]
    )
    return bigquery.Client(credentials=credentials, project=project_id)

def run_query(sql: str):
    client = get_client()
    return client.query(sql).to_dataframe()