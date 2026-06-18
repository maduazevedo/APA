"""Aba: Condicao Fisica.
Injury_History rho~0.50 (preditor #1) | Muscle_Asymmetry rho~0.21
"""

import streamlit as st
import plotly.graph_objects as go

from theme import apply, hlegend, COLOR_MAP_LABELS
import components as ui

_INFO_ASSIMETRIA = (
    "<strong>O que este grafico mostra</strong><br>"
    "Indice de assimetria muscular por grupo de risco. Atletas em risco "
    "apresentam indices sistematicamente maiores — indicativo de "
    "desequilibrio funcional entre membros. Correlacao: rho ≈ 0.21."
)

_INFO_HISTORICO = (
    "<strong>O que este grafico mostra</strong><br>"
    "Taxa de risco agrupada pelo numero de lesoes anteriores. A progressao "
    "e nitida e crescente — quem ja se lesionou tem probabilidade muito maior "
    "de nova lesao. Correlacao: rho ≈ 0.50 · "
    "<em>preditor mais forte do dataset</em>."
)


def render(df, t):
    acc = t["accent"]
    txt = t["text"]
    st.markdown(
        f"<div style='background:{acc}14;border:1.5px solid {acc}55;"
        f"border-radius:8px;padding:0.65rem 1rem;margin-bottom:1rem;"
        f"font-size:0.78rem;color:{txt};'>"
        f"<strong style='color:{acc};font-size:0.65rem;text-transform:uppercase;"
        f"letter-spacing:0.09em;'>Preditor #1 do Dataset</strong><br>"
        f"Historico de Lesoes Anteriores tem a maior correlacao com risco de lesao "
        f"de todas as variaveis analisadas (|rho| = 0.50).</div>",
        unsafe_allow_html=True,
    )

    col_a, col_b = st.columns(2)

    with col_a:
        ui.chart_header("Assimetria muscular por grupo de risco",
                        info=_INFO_ASSIMETRIA, signal=3)
        fig = go.Figure()
        for label in ["Sem Risco", "Com Risco"]:
            sub = df[df["Risco"] == label]["Muscle_Asymmetry"].dropna()
            fig.add_trace(go.Box(
                y=sub, name=label, marker_color=COLOR_MAP_LABELS[label],
                fillcolor=COLOR_MAP_LABELS[label], line_width=1.5, boxmean=True,
            ))
        apply(fig, t)
        hlegend(fig, t)
        fig.update_yaxes(title="Indice de assimetria muscular")
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        show_pct = st.toggle("Exibir em percentual", value=True, key="pct_hist")
        ui.chart_header("Risco por historico de lesoes anteriores",
                        info=_INFO_HISTORICO, signal=4)
        hr = (df.groupby("Injury_History")["Injury_Risk"]
              .agg(com_risco="sum", total="count").reset_index())
        hr["pct"] = hr["com_risco"] / hr["total"] * 100
        y_col  = "pct" if show_pct else "com_risco"
        y_lbl  = "Atletas com risco (%)" if show_pct else "Quantidade com risco"
        rotulos = hr["Injury_History"].astype(str) + " anterior(es)"
        fig = go.Figure(go.Bar(
            x=rotulos, y=hr[y_col],
            marker_color=t["negative"],   # laranja = alerta para o preditor critico
            text=hr[y_col].round(1).astype(str) + ("%" if show_pct else ""),
            textposition="outside",
            textfont=dict(color=t["light"], size=11),
        ))
        apply(fig, t)
        fig.update_xaxes(title="Lesoes anteriores")
        fig.update_yaxes(title=y_lbl)
        st.plotly_chart(fig, use_container_width=True)
