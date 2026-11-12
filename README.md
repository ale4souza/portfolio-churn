# Churn e retenção de clientes (Telco)

Análise de churn e retenção com **SQL, Python e um dashboard**, usando um dataset público de uma operadora de telecomunicações. O objetivo é responder onde os clientes saem, em que momento e **quem o time de Customer Success deveria priorizar**.

**Dashboard interativo:** https://datastudio.google.com/reporting/2368c04d-f191-4393-84e9-e3c60f280ea5

![Dashboard, página 1](docs/dashboard_pagina1.png)
![Dashboard, página 2](docs/dashboard_pagina2.png)

## Perguntas de negócio

1. Qual é a taxa de churn e quanto da receita mensal ela representa?
2. O churn muda conforme o contrato, o tipo de internet e a forma de pagamento?
3. Como a retenção evolui com o tempo de casa?
4. Quais clientes ativos têm mais risco de sair e merecem atenção primeiro?

## Principais achados

- **Churn geral:** 26,54% dos clientes saíram (1.869 de 7.043), levando **30,5% da receita mensal** (R$ 139.130,85 de R$ 456.116,60). Quem saiu pagava mais: mensalidade média de R$ 74,44, contra R$ 61,27 de quem ficou.
- **O contrato mensal concentra o problema:** churn de 42,71%, contra 11,27% no contrato de 1 ano e 2,83% no de 2 anos. O contrato mensal tem 55,0% dos clientes e **88,6% de todas as saídas**.
- **Retenção (Kaplan-Meier):** no contrato mensal, a retenção chega a 50% no **mês 35** e a 12,9% aos 72 meses. No contrato de 2 anos, ainda é de 93,6% aos 72 meses. Na base toda, é de 88,5% aos 6 meses e 84,3% aos 12 meses.
- **Fibra óptica e cheque eletrônico concentram o risco:** churn de 41,89% na fibra (contra 18,96% no DSL e 7,40% sem internet) e de 45,29% no cheque eletrônico (contra 15,24% no cartão automático). A fibra é 44,0% da base e responde por 69,4% do churn.
- **Segmento de maior risco:** contrato mensal + fibra + cheque eletrônico, com **60,37% de churn** (789 de 1.307 clientes). É 18,6% da base e **42,2% de todas as saídas**. Dentro do mesmo contrato e tipo de internet, o cheque eletrônico soma cerca de 15 pontos percentuais de churn (60,37% contra 45,43% no contrato mensal com fibra).
- **Score de risco por regras simples** (ver abaixo): o churn real cresce de forma regular, de **2,99% (score 0) a 71,16% (score 5)**. Os scores 4 e 5 reúnem 27,2% da base e 60,8% das saídas. Entre os **clientes ativos**, 779 estão nos scores 4 e 5, com R$ 60.501,95 de mensalidade (19,1% da receita ativa).

## Como o score de risco funciona

Cada cliente soma pontos: **contrato mensal = 2** e **fibra óptica, cheque eletrônico e até 12 meses de casa = 1 ponto cada** (de 0 a 5). A regra vem dos padrões vistos na análise e serve para **priorizar a atenção do time**. Ela **não é um modelo estatístico**.

## Limitações

- **Associação não é causa.** O dataset não traz qualidade do serviço, preço dos concorrentes nem datas de contrato. Contrato, internet, pagamento e tempo de casa estão misturados entre si.
- **Os dados são uma foto única, sem datas de calendário.** Não dá para fazer coortes por mês de entrada, e o tempo de casa foi usado no lugar. O tipo de contrato é o atual, e não sabemos se o cliente trocou de contrato.
- **O score foi desenhado e validado nos mesmos dados.** O resultado mostra que ele é coerente, mas não prova que preveria o churn de clientes novos. O teste mais honesto seria usar dados de outro período.
- **Pontas da curva de retenção:** acima de 60 meses há poucos clientes observados, e os valores são menos confiáveis (o de 56,8% aos 72 meses no contrato de 1 ano, por exemplo).
- **Churn por faixa de tempo de casa:** a consulta `03` mostra a parcela de saídas entre clientes cujo tempo de casa observado cai na faixa. Ela **não** é a chance de um cliente novo sair nos primeiros meses, que é medida pela curva de Kaplan-Meier.
- **Combinações com menos de 100 clientes** foram omitidas da tabela de segmentos (272 clientes e 28 saídas).
- **Qualidade dos dados:** a coluna `TotalCharges` tem 11 valores vazios, todos de clientes com 0 meses de casa (e que não saíram).

## Ferramentas

- **Python** (pandas, SQLAlchemy, python-dotenv, openpyxl) para carga, exploração, curva de retenção e preparo dos dados do dashboard
- **SQL** (PostgreSQL no Supabase) com agregações, `FILTER`, `CASE` e CTEs
- **Google Planilhas** como fonte do dashboard
- **Looker Studio** para o dashboard
- **Git e GitHub** para versionamento

## Estrutura do repositório

```
portfolio-churn/
├── sql/                              consultas SQL comentadas
│   ├── 01_taxa_churn.sql             taxa de churn e receita perdida
│   ├── 02_churn_por_contrato.sql
│   ├── 03_churn_por_tempo_de_casa.sql
│   ├── 04_churn_por_internet.sql
│   ├── 05_churn_por_pagamento.sql
│   ├── 06_segmentos_de_risco.sql     contrato x internet x pagamento
│   ├── 07_clientes_ativos_em_risco.sql
│   └── 08_validacao_do_score.sql     score x churn real
├── dashboard_data/                   resultados agregados usados no dashboard
├── teste_leitura.py                  confere a leitura do dataset
├── carregar_dados.py                 carrega o CSV no Postgres
├── rodar_sql.py                      executa um arquivo .sql e mostra o resultado
├── exploracao.py                     exploração e curva de retenção (Kaplan-Meier)
├── exportar_csv.py                   exporta os resultados das consultas para CSV
├── curva_larga.py                    reorganiza a curva (uma coluna por contrato)
├── gerar_planilha.py                 junta tudo em uma planilha Excel para o dashboard
├── insights.md                       fatos, interpretações e hipóteses
└── README.md
```

## Como reproduzir

1. Baixe o dataset **Telco Customer Churn** no Kaggle e coloque o arquivo `WA_Fn-UseC_-Telco-Customer-Churn.csv` na pasta `data/` (ela não é versionada).
2. Crie um projeto gratuito no Supabase e guarde a connection string (Session pooler) num arquivo `.env` na raiz:
   ```
   DATABASE_URL=postgresql://usuario:senha@host:5432/postgres
   ```
   No plano gratuito, projetos inativos são pausados: restaure o projeto no painel antes de rodar os scripts.
3. Instale as dependências:
   ```
   pip install pandas sqlalchemy psycopg2-binary python-dotenv openpyxl
   ```
4. Carregue os dados e rode as análises:
   ```
   python carregar_dados.py
   python rodar_sql.py sql\01_taxa_churn.sql
   python exploracao.py
   ```
5. Gere os arquivos do dashboard:
   ```
   python exportar_csv.py
   python curva_larga.py
   python gerar_planilha.py
   ```
6. Suba o arquivo `churn_dashboard_data.xlsx` no Google Planilhas e use-o como fonte no Looker Studio.

Os caminhos nos scripts usam `C:\portfolio-churn`. Ajuste-os se o projeto estiver em outra pasta.

## Fonte dos dados

[Telco Customer Churn](https://www.kaggle.com/datasets/blastchar/telco-customer-churn) (Kaggle).

## Autora

**Alessandra Souza**
[LinkedIn](https://www.linkedin.com/in/alessandra-souza) · [GitHub](https://github.com/ale4souza)
