from bigquery_client import run_query

df = run_query("""
    SELECT *
    FROM `churn-analysis-portfolio.churn_dataset.raw_customers`
    LIMIT 5
""")

print(df.head())
print(f"\nShape: {df.shape}")
print(f"\nColunas: {df.columns.tolist()}")