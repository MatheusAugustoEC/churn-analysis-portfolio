CREATE OR REPLACE VIEW `churn_dataset.vw_bi_predictions` AS
SELECT
  p.customerID,
  p.probabilidade_churn,
  p.risco,
  p.churn_real,
  CASE p.churn_real WHEN 1 THEN 'Churn' ELSE 'Ativo' END AS status_churn,
  p.MonthlyCharges,
  p.tenure,

  -- Contrato traduzido
  CASE c.Contract
    WHEN 'Month-to-month' THEN 'Mensal'
    WHEN 'One_year'       THEN 'Anual'
    WHEN 'Two_year'       THEN 'Bianual'
  END AS contrato,

  -- Internet traduzido
  CASE c.InternetService
    WHEN 'Fiber_optic' THEN 'Fibra Ótica'
    WHEN 'DSL'         THEN 'DSL'
    WHEN 'No'          THEN 'Sem Internet'
  END AS internet,

  -- Pagamento traduzido
  CASE c.PaymentMethod
    WHEN 'Electronic_check'         THEN 'Cheque Eletrônico'
    WHEN 'Mailed_check'             THEN 'Cheque Postal'
    WHEN 'Bank_transfer_automatic'  THEN 'Transferência Bancária'
    WHEN 'Credit_card_automatic'    THEN 'Cartão de Crédito'
  END AS metodo_pagamento,

  -- Faixa etária
  CASE WHEN c.SeniorCitizen = TRUE THEN 'Idoso' ELSE 'Não Idoso' END AS faixa_etaria,

  -- Perfil familiar
  CASE WHEN c.Partner = TRUE THEN 'Com Parceiro' ELSE 'Sem Parceiro' END AS parceiro,
  CASE WHEN c.Dependents = TRUE THEN 'Com Dependentes' ELSE 'Sem Dependentes' END AS dependentes,

  -- Grupo de tenure
  CASE
    WHEN c.tenure BETWEEN 0  AND 12 THEN '0-12 meses'
    WHEN c.tenure BETWEEN 13 AND 24 THEN '13-24 meses'
    WHEN c.tenure BETWEEN 25 AND 48 THEN '25-48 meses'
    WHEN c.tenure BETWEEN 49 AND 60 THEN '49-60 meses'
    ELSE '60+ meses'
  END AS grupo_tenure

FROM `churn_dataset.churn_predictions` p
LEFT JOIN `churn_dataset.customers_cleaned` c
  ON p.customerID = c.customerID