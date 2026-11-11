-- Objetivo: comparar o churn entre as formas de pagamento

SELECT
  payment_method AS pagamento,                                   -- forma de pagamento do cliente
  COUNT(*) AS clientes,                                          -- clientes em cada forma
  COUNT(*) FILTER (WHERE churn = 'Yes') AS clientes_churn,       -- quantos saíram
  -- percentual de saída dentro de cada forma de pagamento
  ROUND(100.0 * COUNT(*) FILTER (WHERE churn = 'Yes') / COUNT(*), 2) AS taxa_churn_pct
FROM telco_churn                                                 -- tabela de clientes
GROUP BY payment_method                                          -- uma linha por forma de pagamento
ORDER BY taxa_churn_pct DESC;                                    -- do maior churn para o menor