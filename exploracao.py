# Objetivo: explorar os dados de churn com Python e calcular a curva de retenção (Kaplan-Meier)

import os                                   # acessa variáveis do sistema
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

with engine.connect() as conn:               # abre a conexão com o banco
    df = pd.read_sql(text("SELECT * FROM telco_churn"), conn)  # lê a tabela inteira

# ---------- 1. Tamanho e tipos ----------
print("Linhas e colunas:", df.shape)         # quantidade de linhas e colunas
print("\nTipos de dados:")
print(df.dtypes.to_string())                 # tipo de cada coluna

# ---------- 2. Valores vazios ----------
print("\nValores vazios por coluna (só as que têm):")
vazios = df.isna().sum()                     # conta os vazios de cada coluna
print(vazios[vazios > 0].to_string())        # mostra só as colunas com algum vazio

# os vazios de total_charges são clientes com 0 meses de casa?
sem_total = df[df["total_charges"].isna()]   # linhas com total_charges vazio
print("\nClientes com total_charges vazio:", len(sem_total))
print("Tempo de casa desses clientes:", sorted(sem_total["tenure"].unique()))
print("Churn desses clientes:", sem_total["churn"].value_counts().to_dict())

# ---------- 3. Resumo dos números ----------
print("\nResumo de tempo de casa e mensalidade:")
print(df[["tenure", "monthly_charges"]].describe().round(2).to_string())

# ---------- 4. Curva de retenção (Kaplan-Meier) ----------
df["saiu"] = (df["churn"] == "Yes").astype(int)   # 1 se o cliente saiu, 0 se ainda é cliente


def kaplan_meier(dados):
    # conta, para cada mês de casa, quantos clientes saíram e quantos foram observados
    por_mes = dados.groupby("tenure").agg(
        saidas=("saiu", "sum"),              # clientes que saíram naquele mês de casa
        total=("saiu", "size"))              # clientes observados naquele mês (saíram ou ainda ativos)
    # em risco no mês t = clientes com tempo de casa maior ou igual a t
    por_mes["em_risco"] = por_mes["total"][::-1].cumsum()[::-1]
    # chance de sair naquele mês, entre quem ainda estava na base
    por_mes["prob_sair"] = por_mes["saidas"] / por_mes["em_risco"]
    # retenção acumulada: multiplica a chance de ficar em cada mês
    por_mes["retencao"] = (1 - por_mes["prob_sair"]).cumprod()
    return por_mes


def retencao_em(curva, mes):
    # retenção no mês pedido (usa o último mês observado até ali)
    return curva.loc[:mes, "retencao"].iloc[-1]


grupos = {"Todos": df}                       # começa com a base inteira
for contrato in sorted(df["contract"].unique()):          # e adiciona um grupo por contrato
    grupos[contrato] = df[df["contract"] == contrato]

marcos = [6, 12, 24, 36, 48, 60, 72]         # meses de casa que vamos mostrar
linhas = []                                  # guarda a tabela resumo
saida_csv = []                               # guarda a curva completa para o dashboard

for nome, dados in grupos.items():           # repete para cada grupo
    curva = kaplan_meier(dados)              # calcula a curva do grupo
    linha = {"grupo": nome, "clientes": len(dados)}
    for m in marcos:
        linha[f"ret_{m}m_%"] = round(100 * retencao_em(curva, m), 1)  # retenção em cada marco
    abaixo = curva.index[curva["retencao"] <= 0.5]        # primeiro mês com retenção de 50% ou menos
    linha["mes_em_que_cai_a_50%"] = int(abaixo[0]) if len(abaixo) else "não atinge"
    linhas.append(linha)
    # guarda a curva inteira, em formato de tabela, para o dashboard
    tabela = curva[["retencao"]].reset_index()
    tabela["retencao_pct"] = (tabela["retencao"] * 100).round(2)
    tabela["grupo"] = nome
    saida_csv.append(tabela[["tenure", "grupo", "retencao_pct"]])

print("\nRetenção (%) por tempo de casa:")
print(pd.DataFrame(linhas).to_string(index=False))

# ---------- 5. Salvar a curva para o dashboard ----------
pasta = r"C:\portfolio-churn\dashboard_data"          # pasta de saída
os.makedirs(pasta, exist_ok=True)                     # cria a pasta se não existir
pd.concat(saida_csv).to_csv(os.path.join(pasta, "curva_retencao.csv"), index=False)
print("\ncurva_retencao.csv salvo em", pasta)