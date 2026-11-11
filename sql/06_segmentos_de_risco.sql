-- Objetivo: encontrar combinações de contrato, internet e pagamento com maior churn

SELECT
  contract AS contrato,                                          -- tipo de contrato
  internet_service AS internet,                                  -- tipo de internet
  -- junta as formas de pagamento automáticas e manuais em dois grupos
  CASE WHEN payment_method = 'Electronic check'
       THEN 'Cheque eletrônico' ELSE 'Outras formas' END AS pagamento,
  COUNT(*) AS clientes,                                          -- clientes em cada combinação
  COUNT(*) FILTER (WHERE churn = 'Yes') AS clientes_churn,       -- quantos saíram
  -- percentual de saída dentro de cada combinação
  ROUND(100.0 * COUNT(*) FILTER (WHERE churn = 'Yes') / COUNT(*), 2) AS taxa_churn_pct
FROM telco_churn                                                 -- tabela de clientes
GROUP BY contract, internet_service, 3                           -- agrupa pelas três colunas (a terceira é o pagamento)
HAVING COUNT(*) >= 100                                           -- ignora combinações com poucos clientes
ORDER BY taxa_churn_pct DESC;                                    -- do maior churn para o menor

