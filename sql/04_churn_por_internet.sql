-- Objetivo: comparar o churn entre os tipos de serviço de internet

SELECT
  internet_service AS internet,                                  -- tipo de internet contratada
  COUNT(*) AS clientes,                                          -- clientes em cada tipo
  COUNT(*) FILTER (WHERE churn = 'Yes') AS clientes_churn,       -- quantos saíram
  -- percentual de saída dentro de cada tipo
  ROUND(100.0 * COUNT(*) FILTER (WHERE churn = 'Yes') / COUNT(*), 2) AS taxa_churn_pct,
  ROUND(AVG(monthly_charges)::numeric, 2) AS mensalidade_media   -- mensalidade média do grupo
FROM telco_churn                                                 -- tabela de clientes
GROUP BY internet_service                                        -- uma linha por tipo de internet
ORDER BY taxa_churn_pct DESC;                                    -- do maior churn para o menor