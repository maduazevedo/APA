"""Aba: Habitos de Treino.
Training_Intensity rho~0.21 | Training_Frequency rho~0.15 | Warmup rho~0.01
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from theme import apply, hlegend, COLOR_MAP_LABELS
import components as ui

_INFO_FREQ = (
    "<strong>O que este grafico mostra</strong><br>"
    "Taxa de risco para cada volume semanal de treino. "
    "Atletas que treinam 6-7 dias/semana tendem a apresentar maior risco — "
    "possivel sinal de <em>overtraining</em>. Correlacao: rho ≈ 0.15."
)

_INFO_INTENS = (
    "<strong>O que este grafico mostra</strong><br>"
    "Taxa de risco por faixa de intensidade. Treinos de alta intensidade (8-10) "
    "estao associados a maior risco — um dos preditores mais relevantes. "
    "Correlacao: rho ≈ 0.21."
)

_INFO_AQUEC = (
    "<strong>O que este grafico mostra</strong><br>"
    "Tempo de aquecimento comparado entre grupos. As distribuicoes sao "
    "quase identicas — <em>aquecimento isolado nao diferencia quem se lesiona</em>. "
    "Correlacao: rho ≈ 0.01."
)


def render(df, t):
    col_a, col_b = st.columns(2)

    with col_a:
        ui.chart_header("Risco por frequencia de treino (dias/semana)",
                        info=_INFO_FREQ, signal=2)
        freq = (df.groupby("Training_Frequency")["Injury_Risk"]
                .agg(pct_risco=lambda x: x.mean() * 100).reset_index())
        fig = go.Figure(go.Bar(
            x=freq["Training_Frequency"], y=freq["pct_risco"],
            marker_color=t["accent"],
            text=freq["pct_risco"].round(1).astype(str) + "%",
            textposition="outside",
            textfont=dict(color=t["light"], size=11),
        ))
        apply(fig, t)
        fig.update_xaxes(title="Dias de treino por semana", dtick=1)
        fig.update_yaxes(title="Atletas com risco (%)",
                         range=[0, max(80, freq["pct_risco"].max() * 1.2)])
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        ui.chart_header("Risco por nivel de intensidade de treino",
                        info=_INFO_INTENS, signal=3)
        bins, labels = [0, 2, 4, 6, 8, 10], ["0-2", "2-4", "4-6", "6-8", "8-10"]
        df_tmp = df.copy()
        df_tmp["Faixa_Intensidade"] = pd.cut(
            df_tmp["Training_Intensity"], bins=bins, labels=labels, include_lowest=True)
        intens = (df_tmp.groupby("Faixa_Intensidade")["Injury_Risk"]
                  .agg(pct_risco=lambda x: x.mean() * 100).reset_index())
        fig = go.Figure(go.Bar(
            x=intens["Faixa_Intensidade"].astype(str), y=intens["pct_risco"],
            marker_color=t["accent"],
            text=intens["pct_risco"].round(1).astype(str) + "%",
            textposition="outside",
            textfont=dict(color=t["light"], size=11),
        ))
        apply(fig, t)
        fig.update_xaxes(title="Intensidade do treino")
        fig.update_yaxes(title="Atletas com risco (%)",
                         range=[0, max(80, intens["pct_risco"].max() * 1.2)])
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    ui.chart_header("Tempo de aquecimento por grupo de risco",
                    info=_INFO_AQUEC, signal=1)
    fig = go.Figure()
    for label in ["Sem Risco", "Com Risco"]:
        sub = df[df["Risco"] == label]["Warmup_Time"].dropna()
        fig.add_trace(go.Box(
            y=sub, name=label, marker_color=COLOR_MAP_LABELS[label],
            fillcolor=COLOR_MAP_LABELS[label], line_width=1.5,
            boxmean=True, opacity=0.85,
        ))
    apply(fig, t, h=270)
    fig.update_yaxes(title="Minutos de aquecimento")
    hlegend(fig, t)
    st.plotly_chart(fig, use_container_width=True)
