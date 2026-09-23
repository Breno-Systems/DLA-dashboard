import streamlit as st
import pandas as pd
import plotly.express as px
import random
from datetime import datetime, timedelta

st.set_page_config(
    page_title="Dashboard de Engajamento",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={"About":"Dashboard de Engajamento"}
)


URL = st.secrets["URL_PLANILHA"]

@st.cache_data(ttl=300)
def carregar_dados():
  df = pd.read_csv(URL)
  return df

# Temporário
def gerar_fake(n=500):
    TURMAS = ["6ºA","6ºB","6ºC","7ºA","7ºB","7ºC",
              "8ºA","8ºB","8ºC","9ºA","9ºB","9ºC"]
    AULAS = ["1ª, 2ª", "3ª, 4ª", "5ª, 6ª", "7ª"]
    NOTAS = ["Alto", "Médio", "Baixo"]

    random.seed(42)
    inicio = datetime(2020, 1, 1)

    linhas = []
    for _ in range(n):
        data = inicio + timedelta(
            days=random.randint(0, 50),
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

df = gerar_fake()

# DF Config
df.columns = ["Data", "Turma", "Aulas", "Engajamento"]

      # Data -> Datetime
df["Data"] = pd.to_datetime(df["Data"], dayfirst=True)

      # Mapeamento de Score
df["Score"] = df["Engajamento"].map({"Alto": 3, "Médio": 2, "Baixo": 1})

      # Cálculo da colina "Dia da Semana"
MAPA_DIA = {
    0: "Segunda",
    1: "Terça",
    2: "Quarta",
    3: "Quinta",
    4: "Sexta",
    5: "Sábado",
    6: "Domingo"
}
df.insert(1, "Dia da Semana", df["Data"].dt.dayofweek.map(MAPA_DIA))


if df.empty:
  st.warning("⚠️ Nenhuma resposta ainda. Preencha o formulário para ver os dados.")
  st.stop()

st.title("Dashboard de Engajamento")
st.caption("Escola Estadual - Ensino Fundamental II e Ensino Médio")

# Exibição Cabeçalho do DataFrame
st.divider()
st.dataframe(df)

st.divider()
# Gráficos

# Evolução -> Linhas
evolucao = df.groupby(pd.Grouper(key="Data", freq="W"))["Score"].mean().reset_index()
fig = px.line(
    evolucao,
    x="Data",
    y="Score",
    markers=True,  # pontos visíveis
    title="Evolução do Engajamento"
)
fig.update_yaxes(range=[0, 3.2])

st.subheader("Evolução do engajamento")
st.plotly_chart(fig, width="stretch")

# Comparativo -> Barras
st.subheader("Comparativo entre turmas")
st.info("gráfico")


st.divider()

# Filtros
with st.sidebar:
  st.header("Filtrar")
  st.info("Filtros")
