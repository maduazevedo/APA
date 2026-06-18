"""Aba: Recuperacao.
Sleep_Hours rho~-0.23 (2o preditor) | Stress rho~-0.06 | Recovery rho~-0.03
"""

import streamlit as st
import plotly.graph_objects as go

from theme import apply, hlegend, COLOR_MAP_LABELS
import components as ui

_INFO_SONO = (
    "<strong>O que este grafico mostra</strong><br>"
    "Horas de sono comparadas entre grupos. Atletas em risco dormem "
    "sistematicamente menos — diferenca de mediana estatisticamente relevante. "
    "Correlacao: rho ≈ -0.23 · <em>2o preditor mais forte do dataset</em>."
)

_INFO_ESTRESSE = (
    "<strong>O que este grafico mostra</strong><br>"
    "Taxa de risco por nivel de estresse declarado. O padrao irregular "
    "sem tendencia clara confirma: <em>estresse isolado nao prediz bem o risco</em>. "
    "Correlacao: rho ≈ -0.06."
)

_INFO_RECUP = (
    "<strong>O que este grafico mostra</strong><br>"
    "Tempo de recuperacao entre sessoes por grupo. As distribuicoes sao "
    "quase identicas — <em>recuperacao isolada nao diferencia atletas em risco</em>. "
    "Correlacao: rho ≈ -0.03."
)


def render(df, t):
    col_a, col_b = st.columns(2)

    with col_a:
        ui.chart_header("Horas de sono por grupo de risco",
                        info=_INFO_SONO, signal=3)
        fig = go.Figure()
        for label in ["Sem Risco", "Com Risco"]:
            sub = df[df["Risco"] == label]["Sleep_Hours"].dropna()
            fig.add_trace(go.Box(
                y=sub, name=label, marker_color=COLOR_MAP_LABELS[label],
                fillcolor=COLOR_MAP_LABELS[label], line_width=1.5,
                boxmean=True, opacity=0.85,
            ))
        apply(fig, t)
        hlegend(fig, t)
        fig.update_yaxes(title="Horas de sono por noite")
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        ui.chart_header("Risco por nivel de estresse",
                        info=_INFO_ESTRESSE, signal=1)
        sr = (df.groupby("Stress_Level")["Injury_Risk"]
              .agg(pct=lambda x: x.mean() * 100).reset_index())
        fig = go.Figure(go.Bar(
            x=sr["Stress_Level"], y=sr["pct"],
            marker_color=t["accent"],
            text=sr["pct"].round(1).astype(str) + "%",
            textposition="outside",
            textfont=dict(color=t["light"], size=10),
        ))
        apply(fig, t)
        fig.update_xaxes(title="Nivel de estresse (1 = baixo, 10 = alto)", dtick=1)
        fig.update_yaxes(title="Atletas com risco (%)",
                         range=[0, max(75, sr["pct"].max() * 1.2)])
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    ui.chart_header("Tempo de recuperacao entre treinos por grupo de risco",
                    info=_INFO_RECUP, signal=1)
    fig = go.Figure()
    for label in ["Sem Risco", "Com Risco"]:
        sub = df[df["Risco"] == label]["Recovery_Time"].dropna()
        fig.add_trace(go.Box(
            y=sub, name=label, marker_color=COLOR_MAP_LABELS[label],
            fillcolor=COLOR_MAP_LABELS[label], line_width=1.5,
            boxmean=True, opacity=0.85,
        ))
    apply(fig, t, h=270)
    hlegend(fig, t)
    fig.update_yaxes(title="Horas de recuperacao entre sessoes")
    st.plotly_chart(fig, use_container_width=True)
