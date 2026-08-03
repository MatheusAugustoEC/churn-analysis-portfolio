CREATE OR REPLACE VIEW `churn_dataset.customers_cleaned` AS
SELECT
  customerID,
  gender,
  CAST(SeniorCitizen AS BOOL) AS SeniorCitizen,
  Partner,
  Dependents,
  tenure,
  PhoneService,
  CASE
    WHEN MultipleLines = 'No phone service' THEN 'No'
    ELSE MultipleLines
  END AS MultipleLines,
  -- Substituindo espaços por underscore para consistência com o modelo
  REPLACE(InternetService, ' ', '_') AS InternetService,
  CASE WHEN OnlineSecurity = 'No internet service' THEN 'No' ELSE OnlineSecurity END AS OnlineSecurity,
  CASE WHEN OnlineBackup = 'No internet service' THEN 'No' ELSE OnlineBackup END AS OnlineBackup,
  CASE WHEN DeviceProtection = 'No internet service' THEN 'No' ELSE DeviceProtection END AS DeviceProtection,
  CASE WHEN TechSupport = 'No internet service' THEN 'No' ELSE TechSupport END AS TechSupport,
  CASE WHEN StreamingTV = 'No internet service' THEN 'No' ELSE StreamingTV END AS StreamingTV,
  CASE WHEN StreamingMovies = 'No internet service' THEN 'No' ELSE StreamingMovies END AS StreamingMovies,
  -- Substituindo espaços por underscore para consistência com o modelo
  REPLACE(Contract, ' ', '_') AS Contract,
  PaperlessBilling,
  -- Substituindo espaços, parênteses por underscore para consistência com o modelo
  REPLACE(REPLACE(REPLACE(PaymentMethod, ' ', '_'), '(', ''), ')', '') AS PaymentMethod,
  MonthlyCharges,
  COALESCE(SAFE_CAST(TotalCharges AS FLOAT64), 0) AS TotalCharges,
  CASE
    WHEN tenure BETWEEN 0 AND 12 THEN '0-12 months'
    WHEN tenure BETWEEN 13 AND 24 THEN '13-24 months'
    WHEN tenure BETWEEN 25 AND 48 THEN '25-48 months'
    WHEN tenure BETWEEN 49 AND 60 THEN '49-60 months'
    ELSE '60+ months'
  END AS tenure_group,
  COALESCE(ROUND(SAFE_DIVIDE(SAFE_CAST(TotalCharges AS FLOAT64), tenure), 2), MonthlyCharges) AS AvgMonthlySpend,
  Churn
FROM `churn_dataset.raw_customers`