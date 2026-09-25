import streamlit as st
import pandas as pd
import plotly.express as px
from utils.dados import obter_dados, colorir_engajamento

st.set_page_config(
    page_title = "Por Turma",
    page_icon = "🏫",
    layout = "wide"
)

st.logo("assets/logo.png")

# -------------------- DADOS --------------------
df = obter_dados()
if df.empty:
    st.warning("Nenhum dado com esses filtros.")
    st.stop()

st.title("Análise por Turma")
st.caption("Mergulhe nos dados de uma turma específica")

todas_turmas = sorted(df["Turma"].unique())
turma_sel = st.selectbox("Escolha a turma: ", todas_turmas)

df_turma = df[df["Turma"] == turma_sel]

# -------------------- Continua --------------------