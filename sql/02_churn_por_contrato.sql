-- Objetivo: comparar o churn entre os tipos de contrato

SELECT
  contract AS contrato,                                          -- tipo de contrato do cliente
  COUNT(*) AS clientes,                                          -- clientes em cada tipo de contrato
  COUNT(*) FILTER (WHERE churn = 'Yes') AS clientes_churn,       -- quantos saíram
  -- percentual de saída dentro de cada contrato
  ROUND(100.0 * COUNT(*) FILTER (WHERE churn = 'Yes') / COUNT(*), 2) AS taxa_churn_pct,
  ROUND(AVG(monthly_charges)::numeric, 2) AS mensalidade_media   -- mensalidade média do grupo
FROM telco_churn                                                 -- tabela de clientes
GROUP BY contract                                                -- uma linha por tipo de contrato
ORDER BY taxa_churn_pct DESC;                                    -- do maior churn para o menor