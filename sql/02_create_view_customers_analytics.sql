CREATE OR REPLACE VIEW `churn_dataset.customers_analytics` AS
SELECT
  Contract,
  tenure_group,
  InternetService,
  PaymentMethod,
  COUNT(*) AS total_customers,
  COUNTIF(Churn = TRUE) AS total_churn,
  ROUND(COUNTIF(Churn = TRUE) / COUNT(*) * 100, 2) AS churn_rate_pct,
  ROUND(AVG(MonthlyCharges), 2) AS avg_monthly_charges,
  ROUND(AVG(tenure), 2) AS avg_tenure,
  ROUND(AVG(AvgMonthlySpend), 2) AS avg_monthly_spend
FROM `churn_dataset.customers_cleaned`
GROUP BY Contract, tenure_group, InternetService, PaymentMethod