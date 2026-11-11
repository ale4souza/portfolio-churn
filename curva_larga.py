# Objetivo: reorganizar a curva de retenção em colunas (uma por contrato) para o Looker Studio

import os                                   # trabalha com pastas e caminhos
import pandas as pd                         # biblioteca de análise de dados

pasta = r"C:\portfolio-churn\dashboard_data"             # pasta com os CSVs do dashboard
df = pd.read_csv(os.path.join(pasta, "curva_retencao.csv"))  # lê a curva gerada pelo exploracao.py

# traduz os nomes dos grupos para português
nomes = {"Todos": "Todos", "Month-to-month": "Mensal", "One year": "1 ano", "Two year": "2 anos"}
df["grupo"] = df["grupo"].map(nomes)         # aplica a tradução na coluna grupo

# transforma cada grupo em uma coluna: uma linha por mês de casa
larga = df.pivot(index="tenure", columns="grupo", values="retencao_pct").reset_index()

# deixa as colunas na ordem desejada e os meses em ordem crescente
colunas = ["Todos", "Mensal", "1 ano", "2 anos"]
larga = larga[["tenure"] + colunas].sort_values("tenure")

# onde um grupo não tem clientes naquele mês, a retenção continua igual à do mês anterior;
# se faltar o começo da curva, ela parte de 100%
larga[colunas] = larga[colunas].ffill().fillna(100)

larga.to_csv(os.path.join(pasta, "curva_retencao_larga.csv"), index=False)  # salva o novo CSV
print("curva_retencao_larga.csv salvo:", len(larga), "linhas")
print(larga.head(3).to_string(index=False))  # mostra as primeiras linhas
print(larga.tail(2).to_string(index=False))  # mostra as últimas linhas