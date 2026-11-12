## Churn geral e por contrato
- Fato: taxa de churn de 26,54% (1.869 de 7.043 clientes).
- Fato: 30,5% da receita mensal (R$ 139.130,85 de R$ 456.116,60) saiu com o churn.
- Fato: churn por contrato: mensal 42,71%, 1 ano 11,27%, 2 anos 2,83%.
- Cálculo: contrato mensal tem 55,0% dos clientes e 88,6% do churn.
- Cálculo: mensalidade média de quem saiu R$ 74,44 vs R$ 61,27 de quem ficou.
- Hipótese: contrato longo pode refletir clientes já mais satisfeitos (associação, não causa).
- Limite: dataset é uma foto da base, sem datas de calendário.

## Churn por tempo de casa e retenção (Kaplan-Meier)
- Fato: o único campo com vazios é total_charges (11 clientes, todos com 0 meses de casa).
- Fato: retenção geral: 88,5% em 6 meses; 84,3% em 12; 78,9% em 24; 70,9% em 48; 59,3% em 72.
- Fato: retenção por contrato aos 24 meses: mensal 58,6%; 1 ano 97,8%; 2 anos 100,0%.
- Fato: no contrato mensal a retenção chega a 50% no mês 35 e a 12,9% aos 72 meses.
- Interpretação: o risco por mês é maior no começo; no contrato mensal a perda é contínua.
- Hipótese: nos contratos longos, o churn se concentra no fim do contrato (sem datas de contrato, não dá para verificar).
- Limite: a tabela por faixa de tempo de casa mostra a parcela de saídas entre clientes cujo tempo observado cai na faixa, e não a chance de um cliente novo sair. A curva Kaplan-Meier mede isso corretamente.
- Limite: contrato é o atual; pontas da curva (60 e 72 meses) têm poucos clientes.

## Churn por tipo de internet e forma de pagamento
- Fato: churn por internet: fibra 41,89%, DSL 18,96%, sem internet 7,40%.
- Fato: churn por pagamento: cheque eletrônico 45,29%, cheque postal 19,11%, débito automático 16,71%, cartão automático 15,24%.
- Cálculo: fibra = 44,0% da base e 69,4% do churn; cheque eletrônico = 33,6% da base e 57,3% do churn.
- Interpretação: fibra (maior mensalidade) e pagamento manual concentram o risco.
- Limite: não há dados de qualidade do serviço nem de concorrência; fatores podem estar misturados com contrato e tempo de casa.

## Segmentos de risco (contrato x internet x pagamento)
- Fato: maior risco: contrato mensal + fibra + cheque eletrônico, 60,37% de churn (789 de 1.307).
- Fato: menor risco: contrato de 2 anos sem internet, 0,81% (5 de 620).
- Cálculo: o segmento de maior risco = 18,6% da base e 42,2% do churn.
- Cálculo: contrato mensal + fibra = 30,2% da base e 62,2% do churn (taxa de 54,61%).
- Cálculo: cheque eletrônico soma cerca de 14,9 pontos percentuais ao churn no contrato mensal com fibra.
- Limite: tempo de casa não controlado; associação, não causa; grupos com menos de 100 clientes foram omitidos (272 clientes, 28 saídas).

## Clientes ativos em risco (score por regras)
- Fato: 5.174 clientes ativos; score 4 e 5 somam 779 clientes (15,1%) e R$ 60.501,95 de mensalidade (19,1% da receita ativa).
- Cálculo: score 3 ou mais: 1.834 clientes (35,4%) e R$ 118.913,15 (37,5%).
- Limite: o score é uma regra simples, com pesos escolhidos por mim com base nos próprios dados; não é um modelo preditivo validado fora da amostra.
- Limite: "receita em risco" é a mensalidade total do grupo, e não a perda esperada.

## Validação do score de risco
- Fato: churn real por score: 5 = 71,16%; 4 = 53,50%; 3 = 30,36%; 2 = 16,27%; 1 = 9,15%; 0 = 2,99%.
- Cálculo: scores 4 e 5 = 27,2% da base e 60,8% do churn; score 3 ou mais = 85,4% do churn.
- Interpretação: o score é coerente e concentra o risco; serve para priorizar a atenção do time de CS.
- Limite: validação em amostra (mesmos dados usados para desenhar a regra); não prova capacidade de prever clientes novos.
- Estimativa grosseira: ~R$ 68,9 mil de receita mensal esperada em risco (21,7% da receita ativa), metade nos scores 4 e 5.