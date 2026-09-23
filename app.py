import streamlit as st
import pandas as pd
import plotly.express as px

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

df = carregar_dados()

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

st.subheader("Evolução do engajamento")
st.info("gráfico")

st.subheader("Comparativo entre turmas")
st.info("gráfico")

st.divider()

# Filtros
with st.sidebar:
  st.header("Filtrar")
  st.info("Filtros")
