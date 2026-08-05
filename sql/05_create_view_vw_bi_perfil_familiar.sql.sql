CREATE OR REPLACE VIEW `churn_dataset.vw_bi_perfil_familiar` AS
SELECT p.customerID, p.churn_real, p.risco, 'Com Parceiro' AS categoria
FROM `churn_dataset.churn_predictions` p
LEFT JOIN `churn_dataset.customers_cleaned` c ON p.customerID = c.customerID
WHERE c.Partner = TRUE

UNION ALL

SELECT p.customerID, p.churn_real, p.risco, 'Sem Parceiro' AS categoria
FROM `churn_dataset.churn_predictions` p
LEFT JOIN `churn_dataset.customers_cleaned` c ON p.customerID = c.customerID
WHERE c.Partner = FALSE

UNION ALL

SELECT p.customerID, p.churn_real, p.risco, 'Com Dependentes' AS categoria
FROM `churn_dataset.churn_predictions` p
LEFT JOIN `churn_dataset.customers_cleaned` c ON p.customerID = c.customerID
WHERE c.Dependents = TRUE

UNION ALL

SELECT p.customerID, p.churn_real, p.risco, 'Sem Dependentes' AS categoria
FROM `churn_dataset.churn_predictions` p
LEFT JOIN `churn_dataset.customers_cleaned` c ON p.customerID = c.customerID
WHERE c.Dependents = FALSE