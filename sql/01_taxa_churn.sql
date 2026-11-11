-- Objetivo: taxa de churn geral e quanto da receita mensal foi perdida

SELECT
  COUNT(*) AS total_clientes,                                    -- todos os clientes da base
  COUNT(*) FILTER (WHERE churn = 'Yes') AS clientes_churn,       -- clientes que saíram
  -- percentual de clientes que saíram
  ROUND(100.0 * COUNT(*) FILTER (WHERE churn = 'Yes') / COUNT(*), 2) AS taxa_churn_pct,
  -- soma das mensalidades de todos os clientes
  ROUND(SUM(monthly_charges)::numeric, 2) AS receita_mensal_total,
  -- soma das mensalidades de quem saiu
  ROUND((SUM(monthly_charges) FILTER (WHERE churn = 'Yes'))::numeric, 2) AS receita_mensal_perdida,
  -- percentual da receita mensal que foi embora com o churn
  -- (a conta toda é convertida para numeric antes de arredondar)
  ROUND((100.0 * SUM(monthly_charges) FILTER (WHERE churn = 'Yes') / SUM(monthly_charges))::numeric, 2) AS pct_receita_perdida
FROM telco_churn;                                                -- tabela carregada no Supabase