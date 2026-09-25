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

col_esq, col_dir = st.columns(2)

with col_esq:
    # Evolução -> Linhas
    evolucao = df_turma.groupby(pd.Grouper(key="Data", freq="W"))["Score"].mean().reset_index()
    fig = px.line(
        evolucao,
        x="Data",
        y="Score",
        markers=True,  # pontos visíveis
        title="Evolução do Engajamento"
    )
    fig.update_yaxes(range=[0, 3.2])
    fig.update_layout(
        dragmode="pan"
    )
    
    st.subheader("Evolução do engajamento")
    st.plotly_chart(fig, width="stretch")

    por_dia = (
        df_turma.groupby("Dia da Semana")["Score"]
        .mean()
        .reindex(["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"])
        .dropna()
        .reset_index()
    )

    fig = px.bar(
        por_dia,
        x="Dia da Semana",
        y="Score",
        color="Score",
        color_continuous_scale="RdYlGn",
        text_auto=".2f",
        title="Engajamento por dia da semana"
    )
    fig.update_yaxes(range=[0,3.2])
    fig.update_layout(dragmode="pan")

    st.subheader("Engajamento por Dia da Semana")
    st.plotly_chart(fig, width="stretch")

with col_dir:
    # Comparativo -> Barras
    ORDEM_AULAS = ["1ª", "2ª", "3ª", "4ª", "5ª", "6ª", "7ª"]
    por_aula = (df_turma.groupby("Aulas")["Score"].mean().reindex(ORDEM_AULAS).reset_index())
    fig = px.bar(
        por_aula,
        x="Aulas",
        y="Score",
        color="Score",
        color_continuous_scale="RdYlGn",
        text_auto=".2f",
        title="Comparativo de Engajamento"
    )
    fig.update_yaxes(range=[0, 3.2])
    fig.update_layout(
        dragmode="pan"
    )
    
    st.subheader("Comparativo entre aulas")
    st.plotly_chart(fig, width="stretch")



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