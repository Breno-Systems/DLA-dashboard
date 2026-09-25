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

with st.sidebar:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("assets/logo.png", width=110)

# -------------------- DADOS --------------------
df = obter_dados()
if df.empty:
    st.warning("Nenhum dado com esses filtros.")
    st.stop()

st.title("Análise por Turma")
st.caption("Mergulhe nos dados de uma turma específica")

todas_turmas = sorted(df["Turma"].unique())
turma_sel = st.selectbox("Escolha a turma: ", todas_turmas, index=None, placeholder="Selecione uma turma...")
if turma_sel == None:
    st.info("👆 Selecione uma turma para ver os dados.")
    st.stop()

df_turma = df[df["Turma"] == turma_sel]

st.divider()
# -------------------- MÉTRICAS --------------------

col1, col2, col3, col4 = st.columns(4)
col1.metric("Engajamento Médio", round(df_turma["Score"].mean(), 2))
col2.metric("Total de respostas", len(df_turma))
col3.metric("Aulas avaliadas", df_turma["Aulas"].nunique())
col4.metric("Última atualização", df_turma["Data"].max().strftime("%d/%m/%Y"))

st.divider()
# -------------------- CORPO DE GRÁFICOS --------------------



st.divider()
# ------------------ DADOS BRUTOS DA TURMA ------------------

with st.expander ("📋 Ver dados brutos"):
    df_view = df_turma.sort_values("Data", ascending=False).copy()
    df_view["Data"] = df_view["Data"].dt.strftime("%d/%m/%Y")
    df_view = df_view.reset_index(drop=True)
    styled = (df_view.style.map(colorir_engajamento, subset=["Engajamento"]).hide(axis="index"))
    st.dataframe(
        styled,
        height=300
    )