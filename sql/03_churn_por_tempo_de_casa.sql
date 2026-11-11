-- Objetivo: ver em que faixa de tempo de casa os clientes mais saem

SELECT
  -- agrupa o tempo de casa (em meses) em faixas
  CASE
    WHEN tenure <= 6  THEN '1. 0 a 6 meses'                      -- clientes recém-chegados
    WHEN tenure <= 12 THEN '2. 7 a 12 meses'                     -- primeiro ano
    WHEN tenure <= 24 THEN '3. 13 a 24 meses'                    -- segundo ano
    WHEN tenure <= 48 THEN '4. 25 a 48 meses'                    -- de 2 a 4 anos
    ELSE '5. Mais de 48 meses'                                   -- clientes mais antigos
  END AS faixa_tempo_de_casa,
  COUNT(*) AS clientes,                                          -- clientes em cada faixa
  COUNT(*) FILTER (WHERE churn = 'Yes') AS clientes_churn,       -- quantos saíram
  -- percentual de saída dentro da faixa
  ROUND(100.0 * COUNT(*) FILTER (WHERE churn = 'Yes') / COUNT(*), 2) AS taxa_churn_pct,
  ROUND(AVG(monthly_charges)::numeric, 2) AS mensalidade_media   -- mensalidade média da faixa
FROM telco_churn                                                 -- tabela de clientes
GROUP BY 1                                                       -- agrupa pela faixa (primeira coluna)
ORDER BY 1;                                                      -- ordena pelas faixas