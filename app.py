import streamlit as st
import pandas as pd
import plotly.express as px
from utils.dados import obter_dados, colorir_engajamento

st.set_page_config(
    page_title="Dashboard de Engajamento",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items={"About":"Dashboard de Engajamento"}
)

df = obter_dados()

# Filtros
with st.sidebar:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("assets/logo.png", width=110)
    
    st.divider()
    
    st.header("Filtros:")

    todas_turmas = sorted(df["Turma"].unique())
    turmas_sel = st.multiselect(
        "Turma",
        options=todas_turmas
    )

    data_min = df["Data"].min().date()
    data_max = df["Data"].max().date()
    inicio, fim = st.slider(
        "Periodo",
        value=(data_min, data_max),
        min_value=data_min,
        max_value=data_max,
        format="DD/MM/YYYY"
    )

if turmas_sel: 
    df_filtrado = df[
        (df["Turma"].isin(turmas_sel)) & (df["Data"].dt.date >= inicio) & (df["Data"].dt.date <= fim)
    ]
else:
    df_filtrado = df[
        (df["Data"].dt.date >= inicio) & (df["Data"].dt.date <= fim)
    ]

if df_filtrado.empty:
    st.warning("Nenhum dado com esses filtros.")
    st.stop()

st.title("Dashboard de Engajamento")

caption = "Escola Estadual - Ensino Fundamental II e Ensino Médio"
if len(df_filtrado) < len(df):
    caption += f" · 🔍 Filtrado: {len(df_filtrado)}/{len(df)}"
st.caption(caption)

st.divider()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Engajamento Médio", round(df_filtrado["Score"].mean(), 2))
col2.metric("Total de respostas", len(df_filtrado))
col3.metric("Turmas avaliadas", df_filtrado["Turma"].nunique())
col4.metric("Última atualização", df_filtrado["Data"].max().strftime("%d/%m/%Y"))

st.divider()
# Gráficos

col_esq, col_dir = st.columns(2)

with col_esq:
    # Evolução -> Linhas
    evolucao = df_filtrado.groupby(pd.Grouper(key="Data", freq="W"))["Score"].mean().reset_index()
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
        df_filtrado.groupby("Dia da Semana")["Score"]
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
    por_turma = (df_filtrado.groupby("Turma")["Score"].mean().sort_values(ascending=False).reset_index())
    fig = px.bar(
        por_turma,
        x="Turma",
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
    
    st.subheader("Comparativo entre turmas")
    st.plotly_chart(fig, width="stretch")


st.divider()



# Dados Brutos em Tabela (colapsado)
with st.expander ("📋 Ver dados brutos"):
    df_view = df_filtrado.sort_values("Data", ascending=False).copy()
    df_view["Data"] = df_view["Data"].dt.strftime("%d/%m/%Y")
    df_view = df_view.reset_index(drop=True)
    styled = (df_view.style.map(colorir, subset=["Engajamento"]).hide(axis="index"))
    st.dataframe(
        styled,
        height=300
    )






