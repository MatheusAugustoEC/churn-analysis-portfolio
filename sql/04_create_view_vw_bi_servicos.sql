CREATE OR REPLACE VIEW `churn_dataset.vw_bi_servicos` AS
SELECT
  p.customerID,
  p.churn_real,
  p.risco,
  CASE WHEN c.StreamingTV      = 'Yes' THEN 1 ELSE 0 END AS streaming_tv,
  CASE WHEN c.StreamingMovies  = 'Yes' THEN 1 ELSE 0 END AS streaming_filmes,
  CASE WHEN c.OnlineBackup     = 'Yes' THEN 1 ELSE 0 END AS backup_online,
  CASE WHEN c.OnlineSecurity   = 'Yes' THEN 1 ELSE 0 END AS seguranca_online,
  CASE WHEN c.TechSupport      = 'Yes' THEN 1 ELSE 0 END AS suporte_tecnico,
  CASE WHEN c.DeviceProtection = 'Yes' THEN 1 ELSE 0 END AS protecao_dispositivo,
  CASE WHEN c.MultipleLines    = 'Yes' THEN 1 ELSE 0 END AS multiplas_linhas
FROM `churn_dataset.churn_predictions` p
LEFT JOIN `churn_dataset.customers_cleaned` c
  ON p.customerID = c.customerID