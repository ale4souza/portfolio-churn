-- Objetivo: conferir se o score de risco separa quem saiu de quem ficou

WITH pontuados AS (
  SELECT
    churn,                                                       -- se o cliente saiu (Yes) ou ficou (No)
    monthly_charges,                                             -- mensalidade
    -- mesma regra de pontuação da consulta anterior
    (CASE WHEN contract = 'Month-to-month' THEN 2 ELSE 0 END)           -- contrato mensal
    + (CASE WHEN internet_service = 'Fiber optic' THEN 1 ELSE 0 END)    -- fibra óptica
    + (CASE WHEN payment_method = 'Electronic check' THEN 1 ELSE 0 END) -- cheque eletrônico
    + (CASE WHEN tenure <= 12 THEN 1 ELSE 0 END)                        -- até 12 meses de casa
    AS score_risco
  FROM telco_churn                                               -- todos os clientes, sem filtro de churn
)
SELECT
  score_risco,                                                   -- pontuação de 0 a 5
  COUNT(*) AS clientes,                                          -- clientes em cada pontuação
  COUNT(*) FILTER (WHERE churn = 'Yes') AS clientes_churn,       -- quantos saíram
  -- percentual de saída dentro de cada pontuação
  ROUND(100.0 * COUNT(*) FILTER (WHERE churn = 'Yes') / COUNT(*), 2) AS taxa_churn_pct
FROM pontuados
GROUP BY score_risco                                             -- uma linha por pontuação
ORDER BY score_risco DESC;                                       -- do maior risco para o menor