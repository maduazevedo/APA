"""Aba: Perfil do Atleta. Sinais fracos — Age (rho~0.01), BMI (rho~-0.04)."""

import streamlit as st
import plotly.graph_objects as go

from theme import apply, hlegend, COLOR_MAP_LABELS
import components as ui

_INFO_IDADE = (
    "<strong>O que este grafico mostra</strong><br>"
    "Distribuicao de idade por grupo de risco. A sobreposicao quase total "
    "das barras indica que <em>idade isolada nao prediz lesao</em>. "
    "Correlacao com risco: rho ≈ 0.01 — sinal negligenciavel."
)

_INFO_IMC = (
    "<strong>O que este grafico mostra</strong><br>"
    "Boxplot de IMC por grupo. As medianas sao praticamente identicas — "
    "<em>IMC isolado nao diferencia atletas em risco</em>. "
    "Correlacao: rho ≈ -0.04."
)


def render(df, t):
    col_a, col_b = st.columns(2)

    with col_a:
        ui.chart_header("Distribuicao de idade por grupo de risco",
                        info=_INFO_IDADE, signal=1)
        fig = go.Figure()
        for label in ["Sem Risco", "Com Risco"]:
            sub = df[df["Risco"] == label]["Age"].dropna()
            fig.add_trace(go.Histogram(
                x=sub, name=label, marker_color=COLOR_MAP_LABELS[label],
                opacity=0.6, nbinsx=12, histnorm="percent",
            ))
        apply(fig, t); hlegend(fig, t)
        fig.update_layout(barmode="overlay")
        fig.update_xaxes(title="Idade (anos)")
        fig.update_yaxes(title="% de atletas no grupo")
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        ui.chart_header("IMC por grupo de risco", info=_INFO_IMC, signal=1)
        fig = go.Figure()
        for label in ["Sem Risco", "Com Risco"]:
            sub = df[df["Risco"] == label]["BMI"].dropna()
            fig.add_trace(go.Box(
                y=sub, name=label, marker_color=COLOR_MAP_LABELS[label],
                fillcolor=COLOR_MAP_LABELS[label], line_width=1.5,
                boxmean=True, opacity=0.85,
            ))
        apply(fig, t)
        fig.update_yaxes(title="IMC")
        st.plotly_chart(fig, use_container_width=True)
