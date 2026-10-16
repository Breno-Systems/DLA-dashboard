import pandas as pd
import streamlit as st
import random
from datetime import datetime, timedelta


# ---------- MAPEAMENTOS (constantes globais) ----------
MAPA_DIA = {
    0: "Segunda", 1: "Terça", 2: "Quarta",
    3: "Quinta", 4: "Sexta", 5: "Sábado", 6: "Domingo"
}

MAPA_SCORE = {"Alto": 3, "Médio": 2, "Baixo": 1}

ORDEM_DIAS = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
ORDEM_AULAS = ["1ª", "2ª", "3ª", "4ª", "5ª", "6ª", "7ª"]


# ---------- CARREGAR DADOS REAIS ----------
@st.cache_data(ttl=300)
def carregar_dados():
    URL = st.secrets["URL_PLANILHA"]
    return pd.read_csv(URL)


# ---------- GERAR DADOS FAKE ----------
def gerar_fake(n=500):
    TURMAS = ["6ºA","6ºB","6ºC","7ºA","7ºB","7ºC",
              "8ºA","8ºB","8ºC","9ºA","9ºB","9ºC"]
    AULAS = ["1ª", "2ª", "3ª", "4ª", "5ª", "6ª", "7ª"]
    NOTAS = ["Alto", "Médio", "Baixo"]

    random.seed(42)
    inicio = datetime.now() - timedelta(days=n)

    linhas = []
    for _ in range(n):
        data = inicio + timedelta(
            days=random.randint(0, n),
            hours=random.randint(7, 17),
            minutes=random.randint(0, 59)
        )
        linhas.append({
            "Data": data,
            "Turma": random.choice(TURMAS),
            "Aulas": random.choice(AULAS),
            "Engajamento": random.choice(NOTAS)
        })

    return pd.DataFrame(linhas)


# ---------- TRATAMENTO PADRÃO ----------
def tratar(df):
    """Aplica o tratamento padrão: renomeia, converte data, cria Score e Dia da Semana."""
    df.columns = ["Data", "Turma", "Aulas", "Engajamento"]
    df["Data"] = pd.to_datetime(df["Data"], dayfirst=True)
    df["Score"] = df["Engajamento"].map(MAPA_SCORE)
    df.insert(1, "Dia da Semana", df["Data"].dt.dayofweek.map(MAPA_DIA))
    return df


# ---------- CARREGAR + TRATAR (função única) ----------

def obter_dados():
    if st.secrets.get("MODO_TESTE") == "On":
        df = gerar_fake()
        return tratar(df)
    else:
        df = carregar_dados()
        return tratar(df)

def calcular_insight(valor_anterior, valor_atual, tipo):
    # "porcentagem" compara a variação com o valor inicial; "diferenca" retorna a variação absoluta.
    if tipo == "diferenca":
        insight = valor_atual - valor_anterior
    elif tipo == "porcentagem":
        if valor_anterior == 0:
            return "Sem valor inicial para comparar"
        insight = (valor_atual-valor_anterior)/valor_anterior * 100
    return insight

def calcular_insight_engajamento(df):
    df_ord = df.sort_values("Data")
    
    meio = len(df_ord) // 2
    
    if meio == 0 or len(df_ord) - meio == 0:
        insight_engajamento = 0
    else:
        media_antiga = df_ord.iloc[:meio]["Score"].mean()
        media_atual = df_ord.iloc[meio:]["Score"].mean()
    
        insight_engajamento = calcular_insight(media_antiga, media_atual, "porcentagem")

    return insight_engajamento

def descobrir_hoje():
    hoje = pd.Timestamp.today().date()
    return hoje

def calcular_respostas_hoje(df):
    hoje = descobrir_hoje()
    respostas_hoje = (df["Data"].dt.date == hoje).sum()
    return respostas_hoje

def calcular_respostas_ultimo_dia(df):
    ultimo_dia = df["Data"].max().date()
    respostas_ultimo_dia = (df["Data"].dt.date == ultimo_dia).sum()
    return respostas_ultimo_dia

# ---------- UTILITÁRIOS DE VISUAL ----------
def colorir_engajamento(nota):
    cores = {
        "Alto": "background-color: #4CAF50; color: white",
        "Médio": "background-color: #FFC107; color: black",
        "Baixo": "background-color: #E53935; color: white"
    }
    return cores.get(nota, "")