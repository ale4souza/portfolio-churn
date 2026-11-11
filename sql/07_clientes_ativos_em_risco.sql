-- Objetivo: listar clientes ativos com um score de risco de churn por regras simples

WITH pontuados AS (
  SELECT
    customer_id,                                                 -- identificador do cliente
    contract,                                                    -- tipo de contrato
    internet_service,                                            -- tipo de internet
    payment_method,                                              -- forma de pagamento
    tenure,                                                      -- meses de casa
    monthly_charges,                                             -- mensalidade
    -- soma pontos por cada característica de risco observada nos dados
    (CASE WHEN contract = 'Month-to-month' THEN 2 ELSE 0 END)           -- contrato mensal
    + (CASE WHEN internet_service = 'Fiber optic' THEN 1 ELSE 0 END)    -- fibra óptica
    + (CASE WHEN payment_method = 'Electronic check' THEN 1 ELSE 0 END) -- cheque eletrônico
    + (CASE WHEN tenure <= 12 THEN 1 ELSE 0 END)                        -- até 12 meses de casa
    AS score_risco
  FROM telco_churn                                               -- tabela de clientes
  WHERE churn = 'No'                                             -- só clientes ativos
)
SELECT
  score_risco,                                                   -- pontuação de 0 a 5
  COUNT(*) AS clientes_ativos,                                   -- clientes ativos em cada pontuação
  ROUND(SUM(monthly_charges)::numeric, 2) AS receita_mensal_em_risco  -- soma das mensalidades do grupo
FROM pontuados
GROUP BY score_risco                                             -- uma linha por pontuação
ORDER BY score_risco DESC;                                       -- do maior risco para o menor