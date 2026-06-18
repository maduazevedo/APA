"""Componentes de UI reutilizaveis para o dashboard."""

import streamlit as st


# ── Signal badges ─────────────────────────────────────────────────────────
_SIG_DOTS = {1: "●○○○", 2: "●●○○", 3: "●●●○", 4: "●●●●"}
_SIG_TIPS = {
    1: "Sinal minimo",
    2: "Sinal fraco",
    3: "Sinal moderado",
    4: "Preditor-chave",
}


def _signal_html(signal: int) -> str:
    if signal < 1 or signal > 4:
        return ""
    return (
        f"<span class='signal-badge sig-{signal}' title='{_SIG_TIPS[signal]}'>"
        f"{_SIG_DOTS[signal]}</span>"
    )


def _info_html(info: str) -> str:
    if not info:
        return ""
    return (
        "<div class='chart-info-wrap'>"
        "<span class='info-icon-btn'>i</span>"
        f"<div class='info-tooltip-box'>{info}</div>"
        "</div>"
    )


# ── Chart header (self-contained — sem card_open/card_close) ──────────────

def chart_header(title: str, info: str = "", signal: int = 0):
    """Cabecalho de grafico: titulo + badge de sinal + icone de info."""
    st.markdown(
        f"<div class='chart-hdr'>"
        f"<span class='chart-title'>{title}</span>"
        f"{_signal_html(signal)}{_info_html(info)}"
        f"</div>",
        unsafe_allow_html=True,
    )


# ── KPI ───────────────────────────────────────────────────────────────────

def kpi(col, val, label):
    col.markdown(
        f"<div class='kpi-card'>"
        f"<div class='kpi-val'>{val}</div>"
        f"<div class='kpi-lbl'>{label}</div>"
        f"</div>",
        unsafe_allow_html=True,
    )


def kpi_delta(col, val, label, delta_pct: float = None, higher_is_worse: bool = False):
    """KPI com seta de variacao vs. total do dataset."""
    delta_html = ""
    if delta_pct is not None and abs(delta_pct) >= 0.1:
        is_bad = (delta_pct > 0) if higher_is_worse else (delta_pct < 0)
        css    = "delta-bad" if is_bad else "delta-good"
        arrow  = "▲" if delta_pct > 0 else "▼"
        delta_html = (
            f"<div class='kpi-delta {css}'>"
            f"{arrow} {abs(delta_pct):.1f}% vs. total"
            f"</div>"
        )
    col.markdown(
        f"<div class='kpi-card'>"
        f"<div class='kpi-val'>{val}</div>"
        f"<div class='kpi-lbl'>{label}</div>"
        f"{delta_html}"
        f"</div>",
        unsafe_allow_html=True,
    )


# ── Gauge de risco com tier ───────────────────────────────────────────────

def risk_gauge(pct: float, t: dict, total_pct: float = None):
    """
    Gauge de nivel de risco com sistema de tiers:
    ELITE (<25%) → SEGURO (25-40%) → ATENCAO (40-55%) → CRITICO (>55%)
    """
    fill = round(pct * 100, 1)

    if pct < 0.25:
        level, fill_color, badge = "ELITE",    t["positive"], "gauge-low"
    elif pct < 0.40:
        level, fill_color, badge = "SEGURO",   t["accent"],   "gauge-accent"
    elif pct < 0.55:
        level, fill_color, badge = "ATENCAO",  t["warning"],  "gauge-mid"
    else:
        level, fill_color, badge = "CRITICO",  t["negative"], "gauge-high"

    delta_html = ""
    if total_pct is not None:
        delta = (pct - total_pct) * 100
        sign  = "+" if delta >= 0 else ""
        color = t["negative"] if delta > 0 else t["positive"]
        delta_html = (
            f"<span style='color:{color};font-weight:600;'>"
            f"{sign}{delta:.1f}pp vs. media</span>"
        )

    st.markdown(
        f"<div class='risk-gauge-wrap'>"
        f"<div class='gauge-header'>"
        f"<span class='gauge-label'>Risco do grupo</span>"
        f"<span class='gauge-badge {badge}'>{level}</span>"
        f"</div>"
        f"<div class='gauge-track'>"
        f"<div class='gauge-fill' style='width:{fill}%;background:{fill_color};'></div>"
        f"</div>"
        f"<div class='gauge-footer'>"
        f"<span style='color:{fill_color};font-weight:700;font-size:1rem;'>{fill}%</span>"
        f"{delta_html}"
        f"</div>"
        f"</div>",
        unsafe_allow_html=True,
    )


# ── Exploracao de abas (gamificacao) ─────────────────────────────────────

def exploration_progress(t: dict):
    """Tracker de abas exploradas na sidebar."""
    n_done = sum(st.session_state.get(f"tab{i}_done", False) for i in range(1, 6))
    c_on, c_off = t["accent"], t["border"]
    dots = "".join(
        f"<span style='color:{c_on};'>●</span>"
        if st.session_state.get(f"tab{i}_done", False)
        else f"<span style='color:{c_off};'>●</span>"
        for i in range(1, 6)
    )
    msg = "Tudo explorado!" if n_done == 5 else "Explore as abas e conclua cada painel"
    msg_color = t["positive"] if n_done == 5 else t["muted"]
    st.markdown(
        f"<div class='risk-gauge-wrap'>"
        f"<div class='gauge-header'>"
        f"<span class='gauge-label'>Exploracao dos paineis</span>"
        f"<span style='font-size:0.72rem;font-weight:700;color:{t['accent']};'>{n_done}/5</span>"
        f"</div>"
        f"<div style='font-size:1.15rem;letter-spacing:0.38em;margin:0.25rem 0;line-height:1;'>{dots}</div>"
        f"<div style='font-size:0.62rem;color:{msg_color};margin-top:0.2rem;'>{msg}</div>"
        f"</div>",
        unsafe_allow_html=True,
    )


def tab_complete_btn(tab_num: int, t: dict):
    """Botao de conclusao no final de cada aba."""
    key = f"tab{tab_num}_done"
    st.markdown("<br>", unsafe_allow_html=True)
    divider()
    if st.session_state.get(key, False):
        st.markdown(
            f"<div style='text-align:center;font-size:0.8rem;"
            f"color:{t['positive']};font-weight:700;padding:0.3rem;'>"
            f"Painel concluido!</div>",
            unsafe_allow_html=True,
        )
    else:
        _, col, _ = st.columns([3, 2, 3])
        with col:
            if st.button("Concluir painel", key=f"btn_{key}", use_container_width=True):
                st.session_state[key] = True
                st.rerun()


# ── Podio dos preditores ──────────────────────────────────────────────────

def podium(items: list, t: dict):
    """
    Podio visual dos top preditores.
    items: [(display_name, abs_corr_value), ...] max 3, ordem decrescente.
    Layout visual: 2o (esq) | 1o (centro) | 3o (dir).
    """
    items = items[:3]
    if len(items) < 2:
        return

    if len(items) == 3:
        vis_order = [1, 0, 2]
    else:
        vis_order = [1, 0]

    heights = [110, 70, 46]                                     # altura p/ 1o, 2o, 3o
    colors  = [t["accent"], t["positive"], t["muted"]]          # cor p/ 1o, 2o, 3o

    slots = ""
    for item_idx in vis_order:
        rank       = item_idx + 1
        name, corr = items[item_idx]
        h          = heights[item_idx]
        color      = colors[item_idx]
        slots += (
            f"<div class='pod-slot'>"
            f"<div class='pod-rank' style='color:{color};'>{rank}o</div>"
            f"<div class='pod-name'>{name}</div>"
            f"<div class='pod-corr'>|rho| = {corr:.2f}</div>"
            f"<div style='height:{h}px;"
            f"background:{color}20;border:1.5px solid {color}66;"
            f"border-bottom:none;border-radius:6px 6px 0 0;width:100%;'></div>"
            f"</div>"
        )

    st.markdown(
        f"<div class='podium-wrap'>{slots}</div>",
        unsafe_allow_html=True,
    )


# ── Misc ──────────────────────────────────────────────────────────────────

def section_label(text: str):
    st.markdown(f"<div class='section-label'>{text}</div>", unsafe_allow_html=True)


def divider():
    st.markdown("<hr class='div'>", unsafe_allow_html=True)
