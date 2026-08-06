CREATE OR REPLACE VIEW `churn_dataset.vw_data_quality` AS
SELECT
  customerID,
  
  CASE WHEN tenure < 0 OR tenure > 72 THEN 'Tenure fora do range' END AS erro_tenure,
  CASE WHEN MonthlyCharges <= 0 OR MonthlyCharges > 200 THEN 'Mensalidade inválida' END AS erro_monthly,
  CASE WHEN TotalCharges < 0 THEN 'Total negativo' END AS erro_total,
  CASE WHEN InternetService NOT IN ('DSL', 'Fiber_optic', 'No') THEN 'Internet inválida' END AS erro_internet,
  CASE WHEN Contract NOT IN ('Month-to-month', 'One_year', 'Two_year') THEN 'Contrato inválido' END AS erro_contrato,
  CASE WHEN PaymentMethod NOT IN ('Electronic_check', 'Mailed_check', 'Bank_transfer_automatic', 'Credit_card_automatic') THEN 'Pagamento inválido' END AS erro_pagamento,
  CASE WHEN customerID IS NULL THEN 'CustomerID nulo' END AS erro_id,
  CASE WHEN MonthlyCharges IS NULL THEN 'Mensalidade nula' END AS erro_monthly_null

FROM `churn_dataset.customers_cleaned`
WHERE
  tenure < 0 OR tenure > 72
  OR MonthlyCharges <= 0 OR MonthlyCharges > 200
  OR TotalCharges < 0
  OR InternetService NOT IN ('DSL', 'Fiber_optic', 'No')
  OR Contract NOT IN ('Month-to-month', 'One_year', 'Two_year')
  OR PaymentMethod NOT IN ('Electronic_check', 'Mailed_check', 'Bank_transfer_automatic', 'Credit_card_automatic')
  OR customerID IS NULL
  OR MonthlyCharges IS NULL