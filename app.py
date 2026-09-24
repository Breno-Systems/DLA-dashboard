import streamlit as st
import pandas as pd
import plotly.express as px
import random
from datetime import datetime, timedelta

st.set_page_config(
    page_title="Dashboard de Engajamento",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items={"About":"Dashboard de Engajamento"}
)

MODO_TESTE = st.secrets["MODO_TESTE"]
URL = st.secrets["URL_PLANILHA"]

def colorir(nota):
    cores = {"Alto": "background-color: #4CAF50; color: white",
             "Médio": "background-color: #FFC107; color: black",
             "Baixo": "background-color: #E53935; color: white"}
    return cores.get(nota, "")

@st.cache_data(ttl=300)
def carregar_dados():
    df = pd.read_csv(URL)
    return df

# Temporário
def gerar_fake(n=500):
    TURMAS = ["6ºA","6ºB","6ºC","7ºA","7ºB","7ºC",
              "8ºA","8ºB","8ºC","9ºA","9ºB","9ºC", "1ªA", "1ªB", "2ªADM", "2ªB", "3ªA", "3ªADM"]
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

if MODO_TESTE == "On":
    df = gerar_fake()
else:
    df = carregar_dados()

# DF Config
df.columns = ["Data", "Turma", "Aulas", "Engajamento"]

      # Data -> Datetime
df["Data"] = pd.to_datetime(df["Data"], dayfirst=True)

      # Mapeamento de Score
df["Score"] = df["Engajamento"].map({"Alto": 3, "Médio": 2, "Baixo": 1})

      # Cálculo da coluna "Dia da Semana"
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

# Filtros
with st.sidebar:
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

st.logo("assets/logo_dla.png", icon_image="assets/logo_dla.png")
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






