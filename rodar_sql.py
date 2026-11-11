# Objetivo: executar um arquivo .sql no banco e mostrar o resultado como tabela

import os                                   # acessa variáveis do sistema
import sys                                  # lê o argumento passado no terminal
import pandas as pd                         # biblioteca de análise de dados
from dotenv import load_dotenv              # lê o arquivo .env
from sqlalchemy import create_engine, text  # conexão com o banco

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

arquivo = sys.argv[1]                        # caminho do arquivo SQL, informado no terminal
with open(arquivo, encoding="utf-8") as f:   # abre o arquivo SQL
    consulta = f.read()                      # lê o texto da consulta

with engine.connect() as conn:               # abre a conexão com o banco
    resultado = pd.read_sql(text(consulta), conn)  # executa e guarda o resultado

print(resultado.to_string(index=False))      # mostra a tabela completa, sem o índice