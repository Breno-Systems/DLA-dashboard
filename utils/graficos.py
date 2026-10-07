import plotly.express as px
import streamlit as st

def grafico_evolucao(df):
    evolucao = df.groupby(pd.Grouper(key="Data", freq="W"))["Score"].mean().reset_index()
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
    return fig