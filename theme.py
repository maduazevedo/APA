"""
Tokens de tema e CSS do dashboard Sports Injury Risk.

Principios de paleta (Few / Cairo):
- Violeta = identidade / destaque de UI (nao representa dado)
- Verde-agua = "sem risco" — associacao positiva, calma
- Laranja = "com risco" — alerta visivel sem agressividade do vermelho
- Amarelo = aviso moderado
Nenhum vermelho, nenhum azul nos dados.
"""

# Paleta navy: #12086F → #2B35AF → #4361EE → #4895EF → #4CC9F0
DATA_NO_RISK = "#1069CF"   # azul medio: grupo seguro
DATA_RISK    = "#27B8D8"   # ciano fechado: grupo em risco (sem jujuba)

THEMES = {
    "dark": {
        # Fundos — sidebar mais escura que antes
        "bg":       "#06091A",   # navy quase preto
        "card":     "#0C0A38",   # sidebar/card mais escuro
        "card2":    "#0A0C3C",   # card elevado
        "border":   "#20287E",   # azul escuro (2o da paleta)
        # Texto
        "text":     "#E8EEF7",   # branco frio
        "muted":    "#4895EF",   # azul claro (4o) — legivel sobre card
        "light":    "#4361EE",   # azul medio (3o)
        # Destaque — ciano fechado, sem saturacao de jujuba
        "accent":   "#2785D8",   # ciano muted
        # Graficos
        "plot_bg":  "rgba(0,0,0,0)",
        "grid":     "#0C0F49",   # grade sutil
        "heat_low": "#0A064A",
        "heat_mid": "#4361EE",
        "heat_high":"#2777D8",
        # Tokens de estado (gamificacao)
        "positive": "#2780D8",   # ciano fechado = positivo
        "negative": "#4895EF",   # azul claro — diferenciado
        "warning":  "#4361EE",   # azul medio — aviso
    },
    "light": {
        "bg":       "#EDF1FF",   # branco com leve tint navy
        "card":     "#FFFFFF",
        "card2":    "#DDE4FF",   # azul muito palido
        "border":   "#4895EF",   # azul claro como borda
        "text":     "#12086F",   # navy escuro para texto (alto contraste)
        "muted":    "#2B35AF",   # azul escuro muted
        "light":    "#4361EE",   # azul medio claro
        "accent":   "#4361EE",   # royal blue — contraste bom no branco
        "plot_bg":  "rgba(0,0,0,0)",
        "grid":     "#DDE4FF",
        "heat_low": "#EDF1FF",
        "heat_mid": "#4895EF",
        "heat_high":"#12086F",
        "positive": "#27B8D8",
        "negative": "#2B35AF",
        "warning":  "#4361EE",
    },
}

COLOR_MAP_LABELS = {"Sem Risco": DATA_NO_RISK, "Com Risco": DATA_RISK}


def get_theme(mode: str) -> dict:
    return THEMES["dark"] if mode == "dark" else THEMES["light"]


def inject_css(t: dict) -> str:
    return f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* ── Base ─────────────────────────────────────────────────────── */
    html, body,
    [data-testid="stAppViewContainer"],
    [data-testid="stHeader"] {{
        background: {t['bg']};
        color: {t['text']};
        font-family: 'Inter', sans-serif;
    }}
    [data-testid="stHeader"] {{ background: {t['bg']}; }}

    /* ── Sidebar ──────────────────────────────────────────────────── */
    [data-testid="stSidebar"] {{
        background: {t['card']};
        border-right: 1px solid {t['border']};
    }}
    [data-testid="stSidebar"] * {{ color: {t['text']} !important; }}

    /* ── Sidebar inputs — fix de tema ────────────────────────────── */
    [data-testid="stSidebar"] [data-baseweb="select"] > div,
    [data-testid="stSidebar"] [data-baseweb="select"] [role="combobox"],
    [data-testid="stSidebar"] [data-baseweb="select"] [role="combobox"] > div {{
        background-color: {t['card2']} !important;
        border-color: {t['border']} !important;
        color: {t['text']} !important;
    }}
    [data-testid="stSidebar"] input[type="text"] {{
        background-color: transparent !important;
        color: {t['text']} !important;
    }}
    [data-testid="stSidebar"] [data-baseweb="tag"],
    [data-testid="stSidebar"] span[data-baseweb="tag"] {{
        background-color: {t['accent']} !important;
        color: #fff !important;
    }}
    [data-testid="stSidebar"] [data-baseweb="tag"] span,
    [data-testid="stSidebar"] [data-baseweb="tag"] svg {{
        color: #fff !important; fill: #fff !important;
    }}
    [data-testid="stSlider"] [role="slider"] {{
        background-color: {t['accent']} !important;
        border-color: {t['accent']} !important;
        box-shadow: 0 0 0 3px {t['accent']}33 !important;
    }}
    [data-testid="stSlider"] > div > div > div > div,
    [data-testid="stSlider"] > div > div > div {{
        background-color: {t['accent']} !important;
    }}
    [data-testid="stSidebar"] [data-testid="stSlider"] p {{
        color: {t['muted']} !important;
        font-size: 0.72rem !important;
    }}

    /* ── Dropdown popup (portal fora da sidebar) ─────────────────── */
    [data-baseweb="popover"] > div {{
        background-color: {t['card']} !important;
        border: 1px solid {t['border']} !important;
        border-radius: 8px !important;
        box-shadow: 0 8px 24px rgba(0,0,0,0.18) !important;
    }}
    [data-baseweb="menu"] {{ background-color: {t['card']} !important; }}
    li[role="option"] {{
        background-color: {t['card']} !important;
        color: {t['text']} !important;
    }}
    li[role="option"]:hover,
    li[role="option"][aria-selected="true"] {{
        background-color: {t['card2']} !important;
        color: {t['accent']} !important;
    }}

    /* ── Controls ─────────────────────────────────────────────────── */
    div[data-baseweb="radio"] label div:first-of-type {{
        border-color: {t['muted']} !important;
    }}
    div[data-baseweb="radio"] label div:first-of-type > div,
    div[data-baseweb="radio"] label input:checked + div {{
        background-color: {t['accent']} !important;
        border-color: {t['accent']} !important;
    }}
    [data-testid="stCheckbox"] [data-baseweb="checkbox"] div[aria-checked="true"] {{
        background-color: {t['accent']} !important;
        border-color: {t['accent']} !important;
    }}
    [role="switch"] {{ background-color: {t['border']} !important; }}
    [role="switch"][aria-checked="true"] {{ background-color: {t['accent']} !important; }}

    /* ── Abas ─────────────────────────────────────────────────────── */
    [data-testid="stTabs"] button {{
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        font-size: 0.84rem;
        color: {t['muted']} !important;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        padding: 0.5rem 1.4rem;
        border-radius: 0;
        border-bottom: 2px solid transparent !important;
        transition: all .2s;
    }}
    [data-testid="stTabs"] button[aria-selected="true"] {{
        color: {t['text']} !important;
        border-bottom: 2px solid {t['accent']} !important;
        background: transparent;
    }}
    [data-testid="stTabs"] [role="tablist"] {{
        border-bottom: 1px solid {t['border']}; gap: 0;
    }}

    /* ── Botao de tema ────────────────────────────────────────────── */
    [data-testid="stSidebar"] [data-testid="stButton"] button {{
        background: {t['card2']};
        color: {t['text']};
        border: 1px solid {t['border']};
        width: 100%;
        border-radius: 6px;
        font-size: 0.82rem;
        transition: border-color .15s, color .15s;
    }}
    [data-testid="stSidebar"] [data-testid="stButton"] button:hover {{
        border-color: {t['accent']}; color: {t['accent']};
    }}

    /* ── Tipografia ───────────────────────────────────────────────── */
    .page-title {{
        font-size: 1.75rem; font-weight: 800; color: {t['text']};
        letter-spacing: -0.03em; margin-bottom: 0.05rem;
    }}
    .page-sub {{
        color: {t['muted']}; font-size: 0.84rem; font-weight: 400;
    }}

    /* ── KPI Cards ────────────────────────────────────────────────── */
    .kpi-card {{
        background: {t['card']};
        border: 1px solid {t['border']};
        border-top: 3px solid {t['accent']};
        border-radius: 8px;
        padding: 0.9rem 1.2rem;
        text-align: center;
        transition: transform 0.18s ease, box-shadow 0.18s ease;
    }}
    .kpi-card:hover {{
        transform: translateY(-3px);
        box-shadow: 0 8px 24px rgba(0,0,0,0.14);
    }}
    .kpi-val {{
        font-size: 1.75rem; font-weight: 700;
        color: {t['accent']}; letter-spacing: -0.02em;
    }}
    .kpi-lbl {{
        font-size: 0.70rem; color: {t['muted']};
        margin-top: 0.2rem; text-transform: uppercase; letter-spacing: 0.07em;
    }}
    .kpi-delta {{
        font-size: 0.67rem; margin-top: 0.35rem;
        font-weight: 600; letter-spacing: 0.02em;
    }}
    .delta-good {{ color: {t['positive']}; }}
    .delta-bad  {{ color: {t['negative']}; }}

    /* ── Chart header (self-contained, sem card aberto/fechado) ───── */
    .chart-hdr {{
        display: flex;
        align-items: center;
        gap: 0.55rem;
        padding-bottom: 0.55rem;
        border-bottom: 1px solid {t['border']};
        margin-bottom: 0.4rem;
        position: relative;
        overflow: visible;
    }}
    .chart-title {{
        font-size: 0.93rem; font-weight: 600;
        color: {t['text']}; flex: 1; min-width: 0;
    }}

    /* ── Signal dots ──────────────────────────────────────────────── */
    .signal-badge {{
        font-size: 0.60rem; font-family: monospace;
        padding: 0.1rem 0.42rem; border-radius: 3px;
        flex-shrink: 0; letter-spacing: 0.1em; white-space: nowrap;
    }}
    .sig-1 {{ color: {t['muted']};    background: {t['card2']}; }}
    .sig-2 {{ color: {t['warning']};  background: {t['card2']}; border: 1px solid {t['warning']}44; }}
    .sig-3 {{ color: {t['positive']}; background: {t['card2']}; border: 1px solid {t['positive']}44; }}
    .sig-4 {{ color: {t['accent']};   background: {t['card2']}; border: 1px solid {t['accent']}66; font-weight: 700; }}

    /* ── Info tooltip ─────────────────────────────────────────────── */
    .chart-info-wrap {{
        position: relative; display: inline-block; flex-shrink: 0;
    }}
    .info-icon-btn {{
        display: inline-flex; align-items: center; justify-content: center;
        width: 18px; height: 18px; border-radius: 50%;
        background: {t['card2']}; color: {t['muted']};
        font-size: 10px; font-weight: 700; font-style: italic;
        border: 1px solid {t['border']}; cursor: help;
        user-select: none; line-height: 1;
        transition: background .15s, color .15s, border-color .15s;
    }}
    .chart-info-wrap:hover .info-icon-btn {{
        background: {t['accent']}; color: #fff; border-color: {t['accent']};
    }}
    .info-tooltip-box {{
        visibility: hidden; opacity: 0;
        position: absolute; right: 0;
        bottom: calc(100% + 10px); top: auto;
        width: 290px;
        background: {t['card']};
        border: 1px solid {t['border']};
        border-left: 3px solid {t['accent']};
        border-radius: 8px; padding: 0.8rem 1rem;
        font-size: 0.75rem; color: {t['light']}; line-height: 1.7;
        z-index: 99999;
        box-shadow: 0 10px 32px rgba(0,0,0,0.22);
        transition: opacity .15s ease, visibility .15s ease;
        pointer-events: none; text-align: left;
    }}
    .info-tooltip-box strong {{
        color: {t['text']}; font-size: 0.72rem;
        text-transform: uppercase; letter-spacing: 0.07em;
    }}
    .chart-info-wrap:hover .info-tooltip-box {{
        visibility: visible; opacity: 1;
    }}
    /* Permite tooltip escapar dos containers Streamlit */
    [data-testid="stMarkdownContainer"],
    [data-testid="stVerticalBlock"] > div {{
        overflow: visible !important;
    }}

    /* ── Risk Gauge (sidebar) ─────────────────────────────────────── */
    .risk-gauge-wrap {{
        background: {t['card2']}; border: 1px solid {t['border']};
        border-radius: 8px; padding: 0.7rem 0.85rem; margin-bottom: 0.5rem;
    }}
    .gauge-header {{
        display: flex; align-items: center;
        justify-content: space-between; margin-bottom: 0.45rem;
    }}
    .gauge-label {{
        font-size: 0.63rem; text-transform: uppercase;
        letter-spacing: 0.09em; color: {t['muted']}; font-weight: 600;
    }}
    .gauge-badge {{
        font-size: 0.60rem; font-weight: 700;
        padding: 0.1rem 0.45rem; border-radius: 4px;
        text-transform: uppercase; letter-spacing: 0.07em;
    }}
    .gauge-low    {{ color: {t['positive']}; background: {t['positive']}22; border: 1px solid {t['positive']}44; }}
    .gauge-accent {{ color: {t['accent']};   background: {t['accent']}22;   border: 1px solid {t['accent']}44; }}
    .gauge-mid    {{ color: {t['warning']};  background: {t['warning']}22;  border: 1px solid {t['warning']}44; }}
    .gauge-high   {{ color: {t['negative']}; background: {t['negative']}22; border: 1px solid {t['negative']}44; }}
    .gauge-track {{
        height: 7px; background: {t['border']};
        border-radius: 4px; overflow: hidden; margin-bottom: 0.35rem;
    }}
    .gauge-fill {{
        height: 100%; border-radius: 4px; transition: width 0.5s ease;
    }}
    .gauge-footer {{
        display: flex; align-items: center;
        justify-content: space-between; font-size: 0.68rem;
    }}

    /* ── Podio dos preditores ─────────────────────────────────────── */
    .podium-wrap {{
        display: flex; align-items: flex-end;
        justify-content: center; gap: 1rem;
        padding: 1.5rem 2rem 0; margin-top: 0.5rem;
        border-top: 1px solid {t['border']};
    }}
    .pod-slot {{
        flex: 1; display: flex; flex-direction: column;
        align-items: center; text-align: center; max-width: 200px;
    }}
    .pod-rank {{
        font-size: 2.2rem; font-weight: 800;
        letter-spacing: -0.05em; line-height: 1; margin-bottom: 0.45rem;
    }}
    .pod-name {{
        font-size: 0.74rem; font-weight: 600; color: {t['text']};
        line-height: 1.3; margin-bottom: 0.2rem;
    }}
    .pod-corr {{
        font-size: 0.64rem; font-family: monospace;
        color: {t['muted']}; margin-bottom: 0.55rem;
    }}

    /* ── Misc ─────────────────────────────────────────────────────── */
    .section-label {{
        font-size: 0.67rem; font-weight: 600;
        letter-spacing: 0.12em; text-transform: uppercase;
        color: {t['muted']}; margin-bottom: 0.6rem;
    }}
    hr.div {{
        border: none; border-top: 1px solid {t['border']}; margin: 1.2rem 0;
    }}
    </style>
    """


def base_layout(t: dict) -> dict:
    return dict(
        paper_bgcolor=t["plot_bg"],
        plot_bgcolor=t["plot_bg"],
        font=dict(color=t["text"], family="Inter", size=12),
        margin=dict(l=10, r=10, t=30, b=10),
    )


def apply(fig, t: dict, h: int = 320):
    fig.update_layout(**base_layout(t), height=h)
    fig.update_xaxes(gridcolor=t["grid"], zerolinecolor=t["grid"], linecolor=t["grid"])
    fig.update_yaxes(gridcolor=t["grid"], zerolinecolor=t["grid"], linecolor=t["grid"])
    return fig


def hlegend(fig, t: dict):
    fig.update_layout(legend=dict(
        orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0,
        title="", bgcolor="rgba(0,0,0,0)",
        font=dict(size=11, color=t["light"])
    ))
    return fig
