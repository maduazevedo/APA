"""Aba: Visao Geral — correlacoes e podio dos preditores."""

import streamlit as st
import plotly.graph_objects as go

from theme import apply
import components as ui


_INFO_CORR = (
    "<strong>O que este grafico mostra</strong><br>"
    "Matriz de correlacao de Pearson. Olhe a coluna <em>Injury_Risk</em>: "
    "Injury_History e Sleep_Hours destacam-se com tons mais intensos — "
    "os preditores mais relevantes do dataset."
)

_INFO_DIFF = (
    "<strong>O que este grafico mostra</strong><br>"
    "Diferenca de medias normalizadas entre os grupos. Barras maiores = "
    "maior poder diferenciador. Injury_History lidera com grande margem. "
    "Variaveis com barra proxima de zero tem pouco poder preditivo isolado."
)

_INFO_HEATMAP = (
    "<strong>O que este grafico mostra</strong><br>"
    "Taxa de risco cruzando faixa etaria e genero. Celulas mais escuras = "
    "subgrupos com maior proporcao de atletas em risco. Identifique perfis "
    "combinados que merecem atencao prioritaria."
)


def render(df, t):
    all_num = [
        "Age", "BMI", "Training_Frequency", "Training_Duration", "Warmup_Time",
        "Sleep_Hours", "Flexibility_Score", "Muscle_Asymmetry", "Recovery_Time",
        "Injury_History", "Stress_Level", "Training_Intensity", "Injury_Risk",
    ]
    sel = st.multiselect("Variaveis para o mapa de correlacao",
                          all_num, default=all_num, key="hm")

    if len(sel) >= 2:
        ui.chart_header("Mapa de correlacao entre variaveis", info=_INFO_CORR)
        corr = df[sel].corr()
        fig = go.Figure(go.Heatmap(
            z=corr.values, x=corr.columns, y=corr.columns,
            colorscale=[[0, t["heat_low"]], [0.5, t["heat_mid"]], [1, t["heat_high"]]],
            zmid=0,
            text=corr.values.round(2), texttemplate="%{text}",
            textfont=dict(size=9, color=t["text"]),
            colorbar=dict(title="correlacao", tickfont=dict(color=t["muted"])),
        ))
        fig.update_layout(
            paper_bgcolor=t["plot_bg"], plot_bgcolor=t["plot_bg"],
            font=dict(color=t["text"], family="Inter", size=12),
            margin=dict(l=120, r=60, t=80, b=120), height=460,
            hovermode=False,
        )
        fig.update_xaxes(automargin=True, tickangle=-60)
        st.plotly_chart(fig, use_container_width=True, theme=None)
    else:
        st.info("Selecione ao menos 2 variaveis.")

    st.markdown("<br>", unsafe_allow_html=True)
    col_a, col_b = st.columns(2)

    diff_vars = [
        "BMI", "Training_Frequency", "Training_Duration", "Warmup_Time",
        "Sleep_Hours", "Flexibility_Score", "Muscle_Asymmetry",
        "Stress_Level", "Training_Intensity", "Recovery_Time",
    ]

    with col_a:
        ui.chart_header("O que mais diferencia quem esta em risco", info=_INFO_DIFF)
        dn = df[diff_vars + ["Injury_Risk"]].copy()
        for c in diff_vars:
            mn, mx = dn[c].min(), dn[c].max()
            dn[c] = (dn[c] - mn) / (mx - mn + 1e-9)
        means = dn.groupby("Injury_Risk")[diff_vars].mean()
        if 0 in means.index and 1 in means.index:
            diff   = (means.loc[1] - means.loc[0]).sort_values()
            colors = [t["negative"] if v >= 0 else t["positive"] for v in diff.values]
            fig = go.Figure(go.Bar(
                x=diff.values, y=diff.index, orientation="h",
                marker_color=colors,
                text=[f"{v:+.2f}" for v in diff.values],
                textposition="outside",
                textfont=dict(color=t["light"], size=11),
            ))
            apply(fig, t, h=380)
            fig.add_vline(x=0, line_color=t["grid"], line_width=1)
            fig.update_xaxes(title="Diferenca normalizada (Com Risco - Sem Risco)")
            fig.update_yaxes(title="")
            st.plotly_chart(fig, use_container_width=True, theme=None)

    with col_b:
        ui.chart_header("Taxa de risco por faixa etaria e genero", info=_INFO_HEATMAP)
        hm  = df.groupby(["Faixa_Etaria", "Genero"])["Injury_Risk"].mean().reset_index()
        piv = hm.pivot(index="Genero", columns="Faixa_Etaria", values="Injury_Risk")
        fig = go.Figure(go.Heatmap(
            z=piv.values, x=[str(c) for c in piv.columns], y=piv.index.tolist(),
            colorscale=[[0, t["heat_low"]], [0.5, t["heat_mid"]], [1, t["heat_high"]]],
            text=(piv.values * 100).round(1), texttemplate="%{text}%",
            textfont=dict(size=13, color=t["text"]),
            colorbar=dict(title="% risco", tickfont=dict(color=t["muted"])),
        ))
        fig.update_layout(
            paper_bgcolor=t["plot_bg"], plot_bgcolor=t["plot_bg"],
            font=dict(color=t["text"], family="Inter", size=12),
            margin=dict(l=60, r=20, t=40, b=55), height=380,
            xaxis_title="Faixa etaria", yaxis_title="Genero",
            hovermode=False,
        )
        st.plotly_chart(fig, use_container_width=True, theme=None)

