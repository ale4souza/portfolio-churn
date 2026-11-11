# Objetivo: confirmar que o Python consegue ler o dataset de churn

import pandas as pd  # biblioteca de análise de dados

# lê o arquivo CSV com os dados dos clientes
df = pd.read_csv(r"C:\portfolio-churn\data\WA_Fn-UseC_-Telco-Customer-Churn.csv")

print(df.shape)                # mostra quantas linhas e colunas existem
print(df.head())               # mostra as primeiras linhas da tabela
print(df["Churn"].value_counts())  # conta quantos clientes saíram (Yes) e quantos ficaram (No)