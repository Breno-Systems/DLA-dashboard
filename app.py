import streamlit as st
import pandas as pd
import gspread
import plotly.express as px

URL = st.secrets["URL_PLANILHA"]

@st.cache_data(ttl=300)
def carregar_dados():
  df = pd.read_csv(URL)
  return df

df = carregar_dados()

st.set_page_config(
    page_title="Dashboard de Engajamento",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={"About":"Dashboard de Engajamento"}
)

st.title("Dashboard de Engajamento")
st.caption("Escola Estadual - Ensino Fundamental II e Ensino Médio")

st.divider()
st.write(df.columns.tolist())
st.write(df.head())

st.divider()

st.subheader("Evolução do engajamento")
st.info("gráfico")

st.subheader("Comparativo entre turmas")
st.info("gráfico")

st.divider()

with st.sidebar:
  st.header("Filtrar")
  st.info("Filtros")
