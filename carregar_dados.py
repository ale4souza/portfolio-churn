# Objetivo: carregar o dataset de churn no Postgres (Supabase)

import os                                   # acessa variáveis do sistema
import re                                   # expressões regulares, para ajustar nomes de colunas
import pandas as pd                         # biblioteca de análise de dados
from dotenv import load_dotenv              # lê o arquivo .env
from sqlalchemy import create_engine        # conexão com o banco

load_dotenv(r"C:\portfolio-churn\.env")     # carrega a senha do banco guardada no .env
url = os.getenv("DATABASE_URL")             # pega a connection string

# ajusta o início da string conforme o driver do Postgres instalado
try:
    import psycopg2  # noqa: F401           # testa se o driver psycopg2 existe
    if url.startswith("postgresql://"):
        url = url.replace("postgresql://", "postgresql+psycopg2://", 1)
except ImportError:                          # se não existir, usa o psycopg novo
    if url.startswith("postgresql://"):
        url = url.replace("postgresql://", "postgresql+psycopg://", 1)

engine = create_engine(url)                  # cria a conexão com o Supabase


def para_snake(nome):
    # transforma CamelCase em snake_case, por exemplo MonthlyCharges vira monthly_charges
    nome = re.sub(r"(?<=[a-z])(?=[A-Z])", "_", nome)  # coloca _ entre minúscula e maiúscula
    return nome.lower()                               # deixa tudo em minúsculas


# lê o arquivo CSV com os dados dos clientes
df = pd.read_csv(r"C:\portfolio-churn\data\WA_Fn-UseC_-Telco-Customer-Churn.csv")

# padroniza os nomes das colunas, para escrever o SQL sem aspas depois
df.columns = [para_snake(c) for c in df.columns]

# total_charges vem como texto e tem espaços em branco; converte para número
# (o que não for número vira vazio)
df["total_charges"] = pd.to_numeric(df["total_charges"], errors="coerce")
print("total_charges vazios:", df["total_charges"].isna().sum())  # quantos ficaram vazios

# grava a tabela no banco (se já existir, substitui)
df.to_sql("telco_churn", engine, if_exists="replace", index=False,
          chunksize=2000, method="multi")
print(f"telco_churn: {len(df)} linhas carregadas")  # confirma a carga