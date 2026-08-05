CREATE OR REPLACE VIEW `churn_dataset.vw_bi_servicos_unpivot` AS
SELECT p.customerID, p.churn_real, p.risco, 'Streaming TV' AS servico
FROM `churn_dataset.churn_predictions` p
LEFT JOIN `churn_dataset.customers_cleaned` c ON p.customerID = c.customerID
WHERE c.StreamingTV = 'Yes'

UNION ALL

SELECT p.customerID, p.churn_real, p.risco, 'Streaming Filmes' AS servico
FROM `churn_dataset.churn_predictions` p
LEFT JOIN `churn_dataset.customers_cleaned` c ON p.customerID = c.customerID
WHERE c.StreamingMovies = 'Yes'

UNION ALL

SELECT p.customerID, p.churn_real, p.risco, 'Backup Online' AS servico
FROM `churn_dataset.churn_predictions` p
LEFT JOIN `churn_dataset.customers_cleaned` c ON p.customerID = c.customerID
WHERE c.OnlineBackup = 'Yes'

UNION ALL

SELECT p.customerID, p.churn_real, p.risco, 'Segurança Online' AS servico
FROM `churn_dataset.churn_predictions` p
LEFT JOIN `churn_dataset.customers_cleaned` c ON p.customerID = c.customerID
WHERE c.OnlineSecurity = 'Yes'

UNION ALL

SELECT p.customerID, p.churn_real, p.risco, 'Suporte Técnico' AS servico
FROM `churn_dataset.churn_predictions` p
LEFT JOIN `churn_dataset.customers_cleaned` c ON p.customerID = c.customerID
WHERE c.TechSupport = 'Yes'

UNION ALL

SELECT p.customerID, p.churn_real, p.risco, 'Proteção de Dispositivo' AS servico
FROM `churn_dataset.churn_predictions` p
LEFT JOIN `churn_dataset.customers_cleaned` c ON p.customerID = c.customerID
WHERE c.DeviceProtection = 'Yes'