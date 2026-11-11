# Objetivo: rodar as consultas SQL e salvar cada resultado em um arquivo CSV para o dashboard

import os                                   # trabalha com pastas e caminhos
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

pasta_saida = r"C:\portfolio-churn\dashboard_data"  # pasta onde os CSVs serão salvos
os.makedirs(pasta_saida, exist_ok=True)             # cria a pasta se ela ainda não existir

# nome do arquivo SQL (dentro da pasta sql) e nome do CSV que será gerado
consultas = {
    "01_taxa_churn.sql": "taxa_churn.csv",
    "02_churn_por_contrato.sql": "churn_por_contrato.csv",
    "03_churn_por_tempo_de_casa.sql": "churn_por_tempo_de_casa.csv",
    "04_churn_por_internet.sql": "churn_por_internet.csv",
    "05_churn_por_pagamento.sql": "churn_por_pagamento.csv",
    "06_segmentos_de_risco.sql": "segmentos_de_risco.csv",
    "07_clientes_ativos_em_risco.sql": "clientes_ativos_em_risco.csv",
    "08_validacao_do_score.sql": "validacao_do_score.csv",
}

for arquivo_sql, arquivo_csv in consultas.items():                 # repete para cada consulta
    caminho_sql = os.path.join(r"C:\portfolio-churn\sql", arquivo_sql)  # caminho do arquivo SQL
    with open(caminho_sql, encoding="utf-8") as f:                 # abre o arquivo SQL
        consulta = f.read()                                        # lê o texto da consulta
    with engine.connect() as conn:                                 # abre a conexão com o banco
        tabela = pd.read_sql(text(consulta), conn)                 # executa e guarda o resultado
    destino = os.path.join(pasta_saida, arquivo_csv)               # caminho do CSV de saída
    tabela.to_csv(destino, index=False, encoding="utf-8")          # salva o CSV sem a coluna de índice
    print(f"{arquivo_csv}: {len(tabela)} linhas salvas")           # mostra o resumo no terminal

print("Concluído!")