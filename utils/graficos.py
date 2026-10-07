import plotly.express as px
import streamlit as st
import pandas as pd

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

def grafico_por_dia(df):
    por_dia = (
        df.groupby("Dia da Semana")["Score"]
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

    return fig

def grafico_por_turma(df):
    por_turma = (df.groupby("Turma")["Score"].mean().sort_values(ascending=False).reset_index())
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
    return fig