"""Sports Injury Risk — orquestrador principal."""

import streamlit as st

from theme import get_theme, inject_css
from data import load_data, apply_filters
import components as ui
from charts import perfil, treino, recuperacao, condicao, visao_geral

st.set_page_config(
    page_title="Sports Injury Risk",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Tema ──────────────────────────────────────────────────────────────────
if "theme_mode" not in st.session_state:
    st.session_state.theme_mode = "dark"

# ── Exploração de abas ────────────────────────────────────────────────────
for i in range(1, 6):
    if f"tab{i}_done" not in st.session_state:
        st.session_state[f"tab{i}_done"] = False

t = get_theme(st.session_state.theme_mode)
st.markdown(inject_css(t), unsafe_allow_html=True)

df_all = load_data()
pct_all = df_all["Injury_Risk"].mean()

# ══════════════════════════════════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown(
        f"<div style='font-size:0.95rem;font-weight:800;"
        f"color:{t['text']};letter-spacing:-0.02em;margin-bottom:0.1rem;'>"
        f"Sports Injury Risk</div>"
        f"<div style='font-size:0.67rem;color:{t['muted']};margin-bottom:0.7rem;'>"
        f"Painel de analise exploratoria</div>",
        unsafe_allow_html=True,
    )
    ui.divider()

    gender_sel = st.multiselect("Genero", ["Feminino", "Masculino"],
                                 default=["Feminino", "Masculino"])
    age_sel    = st.slider("Faixa etaria", 18, 40, (18, 40))
    risk_sel   = st.multiselect("Situacao de risco", ["Sem Risco", "Com Risco"],
                                 default=["Sem Risco", "Com Risco"])

    ui.divider()

    # ── Tier de risco do grupo selecionado ───────────────────────────
    df_prev = apply_filters(df_all, gender_sel, age_sel, risk_sel)
    n_prev  = len(df_prev)
    pct_prev = df_prev["Injury_Risk"].mean() if n_prev else 0.0

    ui.risk_gauge(pct_prev, t, total_pct=pct_all)

    # Mensagem dinamica de descoberta
    if n_prev > 0:
        if pct_prev > 0.72:
            disc_msg   = "Grupo de risco extremo encontrado!"
            disc_color = t["negative"]
        elif pct_prev < 0.18:
            disc_msg   = "Perfil de elite encontrado — baixissimo risco."
            disc_color = t["positive"]
        elif n_prev < 35:
            disc_msg   = f"Amostra pequena ({n_prev} atletas) — cautela na leitura."
            disc_color = t["warning"]
        else:
            disc_msg, disc_color = None, None

        if disc_msg:
            st.markdown(
                f"<div style='font-size:0.71rem;color:{disc_color};font-weight:600;"
                f"padding:0.35rem 0.5rem;text-align:center;"
                f"border:1px solid {disc_color}44;border-radius:6px;"
                f"background:{disc_color}11;margin-bottom:0.4rem;'>"
                f"{disc_msg}</div>",
                unsafe_allow_html=True,
            )

    st.markdown(
        f"<div style='font-size:0.67rem;color:{t['muted']};text-align:center;"
        f"margin:0.1rem 0 0.4rem;'>"
        f"{n_prev} de {len(df_all)} atletas</div>",
        unsafe_allow_html=True,
    )

    ui.divider()

    # ── Progresso de exploracao ───────────────────────────────────────
    ui.exploration_progress(t)

    ui.divider()

    label_tema = "Modo claro" if st.session_state.theme_mode == "dark" else "Modo escuro"
    if st.button(label_tema, use_container_width=True):
        st.session_state.theme_mode = (
            "light" if st.session_state.theme_mode == "dark" else "dark"
        )
        st.rerun()

    ui.divider()
    st.markdown(
        f"<div style='font-size:0.65rem;color:{t['muted']};line-height:1.7;'>"
        f"Fonte: Sports Injury Risk — Kaggle<br>"
        f"{len(df_all)} registros · balanceado e normalizado</div>",
        unsafe_allow_html=True,
    )

df = apply_filters(df_all, gender_sel, age_sel, risk_sel)

# ══════════════════════════════════════════════════════════════════════════
#  CABECALHO + KPIS
# ══════════════════════════════════════════════════════════════════════════
st.markdown("<div class='page-title'>Sports Injury Risk</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='page-sub'>"
    "Analise exploratoria de fatores associados ao risco de lesao em atletas"
    "</div>",
    unsafe_allow_html=True,
)
ui.divider()

n        = len(df)
n_risk   = int(df["Injury_Risk"].sum()) if n else 0
pct_f    = n_risk / n if n else 0.0
sleep_f  = df["Sleep_Hours"].mean()  if n else 0.0
stress_f = df["Stress_Level"].mean() if n else 0.0

delta_risk   = (pct_f - pct_all) * 100
delta_sleep  = (sleep_f  - df_all["Sleep_Hours"].mean())  / df_all["Sleep_Hours"].mean()  * 100 if df_all["Sleep_Hours"].mean() else 0
delta_stress = (stress_f - df_all["Stress_Level"].mean()) / df_all["Stress_Level"].mean() * 100 if df_all["Stress_Level"].mean() else 0

c1, c2, c3, c4, c5 = st.columns(5)
ui.kpi_delta(c1, n,                        "Atletas analisados",
             delta_pct=(n/len(df_all)-1)*100, higher_is_worse=False)
ui.kpi_delta(c2, n_risk,                   "Em risco de lesao",
             delta_pct=delta_risk,           higher_is_worse=True)
ui.kpi_delta(c3, f"{pct_f*100:.1f}%" if n else "—",
                                             "Taxa de risco",
             delta_pct=delta_risk,           higher_is_worse=True)
ui.kpi_delta(c4, f"{sleep_f:.1f}h" if n else "—",
                                             "Sono medio / noite",
             delta_pct=delta_sleep,          higher_is_worse=False)
ui.kpi_delta(c5, f"{stress_f:.1f}/10" if n else "—",
                                             "Estresse medio",
             delta_pct=delta_stress,         higher_is_worse=True)

st.markdown("<br>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════
#  ABAS
# ══════════════════════════════════════════════════════════════════════════
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Perfil do Atleta",
    "Habitos de Treino",
    "Recuperacao",
    "Condicao Fisica",
    "Visao Geral",
])

with tab1:
    perfil.render(df, t)
    ui.tab_complete_btn(1, t)

with tab2:
    treino.render(df, t)
    ui.tab_complete_btn(2, t)

with tab3:
    recuperacao.render(df, t)
    ui.tab_complete_btn(3, t)

with tab4:
    condicao.render(df, t)
    ui.tab_complete_btn(4, t)

with tab5:
    visao_geral.render(df, t)
    ui.tab_complete_btn(5, t)

ui.divider()
st.markdown(
    f"<div style='text-align:center;color:{t['muted']};font-size:0.70rem;padding-bottom:1rem;'>"
    f"Sports Injury Risk · Analise Exploratoria de Dados · {len(df_all)} registros</div>",
    unsafe_allow_html=True,
)
