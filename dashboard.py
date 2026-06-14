import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from scipy.stats import gaussian_kde

st.set_page_config(
    page_title="Sports Injury Risk",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Paleta azul / preta / cinza ───────────────────────────────────────────────
C0     = "#4A90D9"   # azul médio — sem risco
C1     = "#1C3A5E"   # azul escuro — com risco
ACCENT = "#4A90D9"
BG     = "#0D0D0D"
CARD   = "#161616"
CARD2  = "#1F1F1F"
BORDER = "#2E2E2E"
TXT    = "#E8E8E8"
MUTED  = "#888888"
LIGHT  = "#AAAAAA"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [data-testid="stAppViewContainer"] {{
  background: {BG};
  color: {TXT};
  font-family: 'Inter', sans-serif;
}}
[data-testid="stSidebar"] {{ background: {CARD}; border-right: 1px solid {BORDER}; }}
[data-testid="stSidebar"] * {{ color: {TXT} !important; }}
[data-testid="stSidebar"] .stSlider > div > div > div {{ background: {ACCENT} !important; }}

/* ───────────────────────────────────────────────────────────────────────
   Substitui o vermelho padrao do Streamlit pelo azul da paleta em todos
   os widgets interativos (sliders, radios, toggles, multiselect, checkbox)
   ─────────────────────────────────────────────────────────────────────── */
:root {{
  --primary-color: {ACCENT};
}}
[data-testid="stSlider"] [role="slider"] {{
  background-color: {ACCENT} !important;
  border-color: {ACCENT} !important;
  box-shadow: 0 0 0 0.2rem rgba(74,144,217,0.18) !important;
}}
[data-testid="stSlider"] > div > div > div > div,
[data-testid="stSlider"] > div > div > div {{
  background-color: {ACCENT} !important;
}}
div[data-baseweb="radio"] label div:first-of-type {{
  border-color: {MUTED} !important;
}}
div[data-baseweb="radio"] label div:first-of-type > div,
div[data-baseweb="radio"] label input:checked + div {{
  background-color: {ACCENT} !important;
  border-color: {ACCENT} !important;
}}
[data-testid="stMultiSelect"] span[data-baseweb="tag"],
[data-baseweb="tag"] {{
  background-color: {ACCENT} !important;
}}
[role="switch"] {{
  background-color: {BORDER} !important;
}}
[role="switch"][aria-checked="true"] {{
  background-color: {ACCENT} !important;
}}
[data-testid="stCheckbox"] [data-baseweb="checkbox"] div[aria-checked="true"] {{
  background-color: {ACCENT} !important;
  border-color: {ACCENT} !important;
}}

/* Tabs */
[data-testid="stTabs"] button {{
  font-family: 'Inter', sans-serif;
  font-weight: 500;
  font-size: 0.85rem;
  color: {MUTED} !important;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  padding: 0.5rem 1.4rem;
  border-radius: 0;
  border-bottom: 2px solid transparent !important;
  transition: all .2s;
}}
[data-testid="stTabs"] button[aria-selected="true"] {{
  color: {TXT} !important;
  border-bottom: 2px solid {ACCENT} !important;
  background: transparent;
}}
[data-testid="stTabs"] [role="tablist"] {{
  border-bottom: 1px solid {BORDER};
  gap: 0;
}}

.page-title {{
  font-size: 1.75rem;
  font-weight: 700;
  color: {TXT};
  letter-spacing: -0.02em;
  margin-bottom: 0.1rem;
}}
.page-sub {{
  color: {MUTED};
  font-size: 0.85rem;
  font-weight: 400;
}}
.kpi-card {{
  background: {CARD};
  border: 1px solid {BORDER};
  border-radius: 8px;
  padding: 1rem 1.3rem;
  text-align: center;
}}
.kpi-val {{
  font-size: 1.8rem;
  font-weight: 700;
  color: {ACCENT};
  letter-spacing: -0.02em;
}}
.kpi-lbl {{
  font-size: 0.72rem;
  color: {MUTED};
  margin-top: 0.2rem;
  text-transform: uppercase;
  letter-spacing: 0.06em;
}}
.chart-card {{
  background: {CARD};
  border: 1px solid {BORDER};
  border-radius: 8px;
  padding: 1.4rem 1.4rem 1rem;
  margin-bottom: 0.8rem;
}}
.chart-title {{
  font-size: 0.95rem;
  font-weight: 600;
  color: {TXT};
  margin-bottom: 0.25rem;
}}
.chart-desc {{
  font-size: 0.8rem;
  color: {MUTED};
  line-height: 1.5;
  margin-bottom: 0.8rem;
  border-left: 2px solid {BORDER};
  padding-left: 0.75rem;
}}
.story-box {{
  background: {CARD2};
  border: 1px solid {BORDER};
  border-radius: 8px;
  padding: 1rem 1.3rem;
  margin: 0.6rem 0 1.2rem;
  font-size: 0.82rem;
  color: {LIGHT};
  line-height: 1.6;
}}
.story-box b {{ color: {TXT}; }}
.story-box .highlight {{ color: {ACCENT}; font-weight: 600; }}
.section-label {{
  font-size: 0.68rem;
  font-weight: 600;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: {MUTED};
  margin-bottom: 0.6rem;
}}
hr.div {{ border: none; border-top: 1px solid {BORDER}; margin: 1.2rem 0; }}
</style>
""", unsafe_allow_html=True)

# ── Dados ─────────────────────────────────────────────────────────────────────
@st.cache_data
def load():
    df = pd.read_csv("df_balanced.csv")
    df["Genero"]       = df["Gender"].map({0: "Feminino", 1: "Masculino"})
    df["Risco"]        = df["Injury_Risk"].map({0: "Sem Risco", 1: "Com Risco"})
    df["Faixa_Etaria"] = pd.cut(
        df["Age"], bins=[17, 20, 25, 30, 35, 40],
        labels=["ate 20", "21-25", "26-30", "31-35", "36-40"]
    )
    return df

df_all = load()

# ── Tema Plotly base ──────────────────────────────────────────────────────────
BASE = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color=TXT, family="Inter", size=12),
    margin=dict(l=10, r=10, t=30, b=10),
)
GRID = dict(gridcolor=BORDER, zerolinecolor=BORDER, linecolor=BORDER)

def apply(fig, h=320):
    fig.update_layout(**BASE, height=h)
    fig.update_xaxes(**GRID)
    fig.update_yaxes(**GRID)
    return fig

def hlegend(fig):
    fig.update_layout(legend=dict(
        orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0,
        title="", bgcolor="rgba(0,0,0,0)",
        font=dict(size=11, color=LIGHT)
    ))
    return fig

COLOR_MAP = {"Sem Risco": C0, "Com Risco": C1}

# ── Helpers de layout ─────────────────────────────────────────────────────────
def card(title, desc):
    st.markdown(f"""<div class='chart-card'>
      <div class='chart-title'>{title}</div>
      <div class='chart-desc'>{desc}</div>""", unsafe_allow_html=True)

def endcard():
    st.markdown("</div>", unsafe_allow_html=True)

def story(text):
    st.markdown(f"<div class='story-box'>{text}</div>", unsafe_allow_html=True)

def kpi(col, val, label):
    col.markdown(f"""<div class='kpi-card'>
      <div class='kpi-val'>{val}</div>
      <div class='kpi-lbl'>{label}</div>
    </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown(f"<div style='font-size:1rem;font-weight:600;color:{TXT};margin-bottom:0.2rem;'>Filtros</div>", unsafe_allow_html=True)
    st.markdown("<hr class='div'>", unsafe_allow_html=True)

    gender_sel = st.multiselect("Genero", ["Feminino", "Masculino"],
                                default=["Feminino", "Masculino"])
    age_sel    = st.slider("Faixa etaria", 18, 40, (18, 40))
    risk_sel   = st.multiselect("Situacao de risco", ["Sem Risco", "Com Risco"],
                                default=["Sem Risco", "Com Risco"])

    st.markdown("<hr class='div'>", unsafe_allow_html=True)
    st.markdown(f"<div style='font-size:0.7rem;color:{MUTED};line-height:1.6;'>Fonte: Sports Injury Risk<br>Kaggle — 694 registros<br>Dataset balanceado e normalizado</div>",
                unsafe_allow_html=True)

df = df_all[
    df_all["Genero"].isin(gender_sel) &
    df_all["Age"].between(*age_sel) &
    df_all["Risco"].isin(risk_sel)
].copy()

# ══════════════════════════════════════════════════════════════════════════════
#  CABECALHO
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("<div class='page-title'>Sports Injury Risk</div>", unsafe_allow_html=True)
st.markdown("<div class='page-sub'>Analise exploratoria de fatores associados ao risco de lesao em atletas</div>",
            unsafe_allow_html=True)
st.markdown("<hr class='div'>", unsafe_allow_html=True)

# KPIs
n      = len(df)
n_risk = int(df["Injury_Risk"].sum()) if n else 0
pct    = f"{n_risk/n*100:.1f}%" if n else "—"
sleep  = f"{df['Sleep_Hours'].mean():.1f}h" if n else "—"
stress = f"{df['Stress_Level'].mean():.1f}/10" if n else "—"

c1,c2,c3,c4,c5 = st.columns(5)
kpi(c1, n,      "Atletas analisados")
kpi(c2, n_risk, "Em risco de lesao")
kpi(c3, pct,    "Taxa de risco")
kpi(c4, sleep,  "Horas de sono / media")
kpi(c5, stress, "Estresse medio")

st.markdown("<br>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  ABAS
# ══════════════════════════════════════════════════════════════════════════════
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Perfil do Atleta",
    "Habitos de Treino",
    "Recuperacao",
    "Condicao Fisica",
    "Visao Geral",
])

# ══════════════════════════════════════════════════════════════════════════════
#  TAB 1 — PERFIL DO ATLETA
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    story("""
    <b>Contexto:</b> Antes de entender o que causa lesoes, precisamos conhecer quem sao esses atletas.
    Esta secao apresenta a distribuicao por <span class='highlight'>idade</span> e
    <span class='highlight'>indice de massa corporal (IMC)</span>, separando sempre os
    atletas <b>sem risco</b> dos <b>com risco</b> de lesao.
    Essas variaveis ajudam a identificar se grupos demograficos especificos sao mais vulneraveis.
    """)

    col_a, col_b = st.columns(2)

    with col_a:
        suavizacao = st.slider("Suavizacao da curva", 0.2, 1.0, 0.4, 0.1,
                               key="kde", help="Ajusta quao suave a linha aparece")
        card(
            "Distribuicao de Idade",
            "Cada barra mostra quantos atletas tem aquela idade. As linhas suavizadas (curvas) facilitam "
            "ver o perfil geral de cada grupo. Quando a curva azul escura estiver acima da azul clara em "
            "uma faixa de idade, isso indica que aquela faixa concentra mais atletas em risco."
        )
        fig = go.Figure()
        for rv, color, label in [(0, C0, "Sem Risco"), (1, C1, "Com Risco")]:
            sub = df[df["Injury_Risk"] == rv]["Age"].dropna()
            fig.add_trace(go.Histogram(
                x=sub, name=label, marker_color=color,
                opacity=0.45, nbinsx=16, histnorm="probability density"
            ))
            if len(sub) > 5:
                kde  = gaussian_kde(sub, bw_method=suavizacao)
                xs   = np.linspace(sub.min(), sub.max(), 300)
                fig.add_trace(go.Scatter(
                    x=xs, y=kde(xs), mode="lines",
                    line=dict(color=color, width=2.5),
                    name=f"Tendencia {label}", showlegend=False
                ))
        apply(fig); hlegend(fig)
        fig.update_layout(barmode="overlay")
        fig.update_xaxes(title="Idade (anos)")
        fig.update_yaxes(title="Proporcao de atletas")
        st.plotly_chart(fig, use_container_width=True)
        endcard()

    with col_b:
        card(
            "Indice de Massa Corporal (IMC) por Grupo de Risco",
            "O box plot resume a distribuicao do IMC: a linha central e a mediana (valor do meio), "
            "a caixa representa os 50% centrais dos atletas, e os pontos fora sao casos extremos. "
            "Se a caixa do grupo em risco estiver mais alta, atletas com IMC elevado lesionam mais."
        )
        fig = go.Figure()
        for rv, color, label in [(0, C0, "Sem Risco"), (1, C1, "Com Risco")]:
            sub = df[df["Injury_Risk"] == rv]["BMI"].dropna()
            fig.add_trace(go.Box(
                y=sub, name=label, marker_color=color,
                fillcolor=color, line_width=1.5,
                boxmean="sd", opacity=0.85
            ))
        apply(fig)
        fig.update_yaxes(title="IMC")
        st.plotly_chart(fig, use_container_width=True)
        endcard()


# ══════════════════════════════════════════════════════════════════════════════
#  TAB 2 — HABITOS DE TREINO
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    story("""
    <b>Contexto:</b> Como e quanto um atleta treina influencia diretamente sua saude.
    Aqui analisamos <span class='highlight'>frequencia</span>,
    <span class='highlight'>duracao</span>, <span class='highlight'>intensidade</span>
    e <span class='highlight'>tempo de aquecimento</span>.
    A hipotese e que treinar em excesso — ou sem preparo adequado — aumenta o risco de lesao.
    """)

    col_a, col_b = st.columns(2)

    with col_a:
        card(
            "Risco de Lesao por Frequencia de Treino",
            "Cada barra representa quantos dias por semana o atleta treina. "
            "A altura da barra mostra qual percentual dos atletas daquela frequencia sofre risco de lesao. "
            "Barras mais altas = aquela frequencia e mais perigosa."
        )
        freq = (df.groupby("Training_Frequency")["Injury_Risk"]
                .agg(pct_risco=lambda x: x.mean()*100, total="count")
                .reset_index())
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=freq["Training_Frequency"],
            y=freq["pct_risco"],
            marker=dict(
                color=freq["pct_risco"],
                colorscale=[[0, "#1a3a5c"], [0.5, C0], [1, "#FFFFFF"]],
                cmin=0, cmax=100,
                showscale=True,
                colorbar=dict(title="% risco", tickfont=dict(color=MUTED), len=0.7)
            ),
            text=freq["pct_risco"].round(1).astype(str) + "%",
            textposition="outside",
            textfont=dict(color=LIGHT, size=11)
        ))
        apply(fig)
        fig.update_xaxes(title="Dias de treino por semana", dtick=1)
        fig.update_yaxes(title="Atletas com risco (%)", range=[0, 80])
        st.plotly_chart(fig, use_container_width=True)
        endcard()

    with col_b:
        card(
            "Duracao vs. Intensidade do Treino",
            "Cada ponto representa um atleta. O eixo horizontal mostra quanto tempo ele treina por sessao "
            "e o eixo vertical mostra a intensidade do esforco. "
            "Pontos agrupados no canto direito-superior (treino longo e intenso) que sejam predominantemente "
            "azuis escuros indicam maior concentracao de risco."
        )
        opac = st.slider("Transparencia dos pontos", 0.1, 1.0, 0.5, 0.05, key="op6")
        fig = px.scatter(
            df, x="Training_Duration", y="Training_Intensity",
            color="Risco", color_discrete_map=COLOR_MAP,
            opacity=opac, trendline="ols", trendline_scope="overall",
            labels={"Training_Duration": "Duracao da sessao (min)",
                    "Training_Intensity": "Intensidade do treino",
                    "Risco": ""}
        )
        apply(fig); hlegend(fig)
        st.plotly_chart(fig, use_container_width=True)
        endcard()

    card(
        "Tempo de Aquecimento antes do Treino",
        "O grafico de violino combina o box plot com a forma real da distribuicao dos dados. "
        "Quanto mais larga a forma em determinada altura, mais atletas tem aquele tempo de aquecimento. "
        "Se a forma do grupo em risco for mais larga em valores baixos, significa que quem aquece pouco se lesiona mais."
    )
    fig = go.Figure()
    for rv, color, label in [(0, C0, "Sem Risco"), (1, C1, "Com Risco")]:
        sub = df[df["Injury_Risk"] == rv]["Warmup_Time"].dropna()
        fig.add_trace(go.Violin(
            y=sub, name=label, fillcolor=color, line_color=color,
            opacity=0.7, box_visible=True, meanline_visible=True
        ))
    apply(fig, h=270); hlegend(fig)
    fig.update_yaxes(title="Minutos de aquecimento")
    st.plotly_chart(fig, use_container_width=True)
    endcard()


# ══════════════════════════════════════════════════════════════════════════════
#  TAB 3 — RECUPERACAO
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    story("""
    <b>Contexto:</b> O corpo precisa de descanso para se recuperar do esforco fisico.
    Sono insuficiente, estresse elevado e pouco tempo de recuperacao entre treinos
    sao fatores frequentemente ignorados — mas que podem ser decisivos.
    Esta secao revela como esses <span class='highlight'>habitos de vida</span> se relacionam
    com o risco de lesao.
    """)

    col_a, col_b = st.columns(2)

    with col_a:
        card(
            "Horas de Sono por Grupo de Risco",
            "O grafico de violino mostra a distribuicao das horas de sono para cada grupo. "
            "A linha horizontal central e a media. Se a forma do grupo com risco estiver "
            "concentrada em menos horas, dormir pouco aparece como fator de risco para lesoes."
        )
        fig = go.Figure()
        for rv, color, label in [(0, C0, "Sem Risco"), (1, C1, "Com Risco")]:
            sub = df[df["Injury_Risk"] == rv]["Sleep_Hours"].dropna()
            fig.add_trace(go.Violin(
                y=sub, name=label, fillcolor=color, line_color=color,
                opacity=0.7, box_visible=True, meanline_visible=True
            ))
        apply(fig); hlegend(fig)
        fig.update_yaxes(title="Horas de sono por noite")
        st.plotly_chart(fig, use_container_width=True)
        endcard()

    with col_b:
        viz = st.radio("Tipo de visualizacao", ["Barras", "Linha de tendencia"],
                       horizontal=True, key="vg9")
        card(
            "Nivel de Estresse e Risco de Lesao",
            "O nivel de estresse e avaliado de 1 (baixo) a 10 (alto). "
            "Cada barra mostra o percentual de atletas com risco de lesao para aquele nivel. "
            "Se as barras crescem conforme o estresse aumenta, isso confirma que o estado psicologico "
            "afeta diretamente a saude fisica do atleta."
        )
        sr = (df.groupby("Stress_Level")["Injury_Risk"]
              .agg(pct=lambda x: x.mean()*100)
              .reset_index())
        fig = go.Figure()
        if viz == "Barras":
            fig.add_trace(go.Bar(
                x=sr["Stress_Level"], y=sr["pct"],
                marker=dict(
                    color=sr["pct"],
                    colorscale=[[0, "#1a3a5c"], [1, C0]],
                ),
                text=sr["pct"].round(1).astype(str) + "%",
                textposition="outside",
                textfont=dict(color=LIGHT, size=10)
            ))
        else:
            fig.add_trace(go.Scatter(
                x=sr["Stress_Level"], y=sr["pct"],
                mode="lines+markers",
                line=dict(color=C0, width=2.5),
                marker=dict(size=7, color=C0),
                fill="tozeroy",
                fillcolor="rgba(74,144,217,0.12)"
            ))
        apply(fig)
        fig.update_xaxes(title="Nivel de estresse (1 = baixo, 10 = alto)", dtick=1)
        fig.update_yaxes(title="Atletas com risco (%)", range=[0, 75])
        st.plotly_chart(fig, use_container_width=True)
        endcard()

    nbins = st.slider("Detalhe do histograma", 8, 30, 15, key="nb10")
    card(
        "Tempo de Recuperacao entre Treinos",
        "Este histograma mostra quantos atletas de cada grupo descansam por determinado numero de horas "
        "entre uma sessao e outra. As barras dos dois grupos estao sobrepostas para facilitar a comparacao. "
        "Se as barras azuis escuras (com risco) estiverem concentradas nos valores menores, "
        "recuperacao insuficiente e um fator de risco."
    )
    fig = go.Figure()
    for rv, color, label in [(0, C0, "Sem Risco"), (1, C1, "Com Risco")]:
        sub = df[df["Injury_Risk"] == rv]["Recovery_Time"].dropna()
        fig.add_trace(go.Histogram(
            x=sub, name=label, marker_color=color,
            opacity=0.6, nbinsx=nbins
        ))
    apply(fig, h=270); hlegend(fig)
    fig.update_layout(barmode="overlay")
    fig.update_xaxes(title="Horas de recuperacao entre treinos")
    fig.update_yaxes(title="Numero de atletas")
    st.plotly_chart(fig, use_container_width=True)
    endcard()


# ══════════════════════════════════════════════════════════════════════════════
#  TAB 4 — CONDICAO FISICA
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    story("""
    <b>Contexto:</b> Condicao fisica vai alem de forca — envolve
    <span class='highlight'>equilibrio muscular</span> e
    <span class='highlight'>historico de lesoes anteriores</span>.
    Atletas com assimetrias musculares ou que ja sofreram lesoes antes
    tendem a ser mais vulneraveis no futuro.
    """)

    col_a, col_b = st.columns(2)

    with col_a:
        card(
            "Assimetria Muscular e Risco de Lesao",
            "Assimetria muscular e a diferenca de forca ou tamanho entre os lados do corpo (ex: braco direito vs esquerdo). "
            "Um valor maior indica maior desequilibrio. Se a caixa do grupo em risco estiver mais elevada, "
            "desequilibrios musculares aparecem como um preditor importante de lesoes."
        )
        fig = go.Figure()
        for rv, color, label in [(0, C0, "Sem Risco"), (1, C1, "Com Risco")]:
            sub = df[df["Injury_Risk"] == rv]["Muscle_Asymmetry"].dropna()
            fig.add_trace(go.Box(
                y=sub, name=label, marker_color=color,
                fillcolor=color, line_width=1.5, boxmean="sd"
            ))
        apply(fig)
        fig.update_yaxes(title="Indice de assimetria muscular")
        st.plotly_chart(fig, use_container_width=True)
        endcard()

    with col_b:
        show_pct = st.toggle("Exibir em percentual", value=True, key="pct13")
        card(
            "Historico de Lesoes e Risco Atual",
            "Cada grupo de barras representa atletas com 0, 1, 2 ou 3 lesoes anteriores. "
            "A altura da barra mostra quantos (ou qual percentual) desses atletas estao hoje em risco. "
            "Uma tendencia crescente confirmaria que lesoes anteriores aumentam a chance de novas lesoes."
        )
        hr = (df.groupby("Injury_History")["Injury_Risk"]
              .agg(com_risco="sum", total="count")
              .reset_index())
        hr["pct"] = hr["com_risco"] / hr["total"] * 100
        y_col = "pct" if show_pct else "com_risco"
        y_lbl = "Atletas com risco (%)" if show_pct else "Quantidade com risco"
        rotulos = hr["Injury_History"].astype(str) + " lesao(oes) anterior(es)"
        fig = go.Figure(go.Bar(
            x=rotulos, y=hr[y_col],
            marker=dict(
                color=hr["pct"],
                colorscale=[[0, "#1a3a5c"], [1, C0]],
            ),
            text=hr[y_col].round(1).astype(str) + ("%" if show_pct else ""),
            textposition="outside",
            textfont=dict(color=LIGHT, size=11)
        ))
        apply(fig)
        fig.update_xaxes(title="Lesoes anteriores")
        fig.update_yaxes(title=y_lbl)
        st.plotly_chart(fig, use_container_width=True)
        endcard()


# ══════════════════════════════════════════════════════════════════════════════
#  TAB 5 — VISAO GERAL (multivariada)
# ══════════════════════════════════════════════════════════════════════════════
with tab5:
    story("""
    <b>Contexto:</b> Ate aqui analisamos cada fator separadamente.
    Agora, vemos o <span class='highlight'>panorama completo</span>:
    quais variaveis mais se relacionam entre si, como o perfil dos grupos se compara
    de forma simultanea, e quais combinacoes de idade e genero concentram mais risco.
    """)

    # G14 — Heatmap correlacao
    all_num = ["Age","BMI","Training_Frequency","Training_Duration","Warmup_Time",
               "Sleep_Hours","Flexibility_Score","Muscle_Asymmetry","Recovery_Time",
               "Injury_History","Stress_Level","Training_Intensity","Injury_Risk"]
    sel = st.multiselect("Selecione as variaveis para o mapa de correlacao",
                         all_num, default=all_num, key="hm")

    if len(sel) >= 2:
        corr = df[sel].corr()
        card(
            "Mapa de Correlacao entre Variaveis",
            "Cada celula mostra a correlacao entre duas variaveis: azul mais intenso significa relacao positiva "
            "(quando uma sobe, a outra tende a subir), cinza indica ausencia de relacao. "
            "Foque na linha e coluna 'Injury_Risk' para ver o que mais influencia o risco de lesao."
        )
        fig = go.Figure(go.Heatmap(
            z=corr.values, x=corr.columns, y=corr.columns,
            colorscale=[[0, CARD2], [0.5, "#1a3a5c"], [1, C0]],
            zmid=0,
            text=corr.values.round(2), texttemplate="%{text}",
            textfont=dict(size=9, color=TXT),
            colorbar=dict(title="correlacao", tickfont=dict(color=MUTED))
        ))
        fig.update_layout(**BASE, height=440)
        fig.update_xaxes(tickangle=-30)
        st.plotly_chart(fig, use_container_width=True)
        endcard()
    else:
        st.info("Selecione ao menos 2 variaveis para gerar o mapa.")

    st.markdown("<br>", unsafe_allow_html=True)
    col_a, col_b = st.columns(2)

    with col_a:
        radar_opts = ["BMI","Training_Frequency","Training_Duration","Warmup_Time",
                      "Sleep_Hours","Flexibility_Score","Muscle_Asymmetry",
                      "Stress_Level","Training_Intensity","Recovery_Time"]
        radar_sel = st.multiselect("Dimensoes do radar", radar_opts,
                                   default=radar_opts[:7], key="rad")
        card(
            "Perfil Comparativo: Com Risco vs. Sem Risco",
            "O grafico radar mostra, ao mesmo tempo, varias caracteristicas dos dois grupos. "
            "Cada ponta representa uma variavel normalizada de 0 a 1. "
            "Onde o contorno azul escuro se expande mais que o azul claro, o grupo em risco tem valores maiores — "
            "essas sao as variaveis que mais os diferenciam."
        )
        if len(radar_sel) >= 3:
            dn = df[radar_sel + ["Injury_Risk"]].copy()
            for c in radar_sel:
                mn, mx = dn[c].min(), dn[c].max()
                dn[c] = (dn[c] - mn) / (mx - mn + 1e-9)
            means = dn.groupby("Injury_Risk")[radar_sel].mean()
            fig = go.Figure()
            for rv, color, label in [(0, C0, "Sem Risco"), (1, C1, "Com Risco")]:
                if rv not in means.index: continue
                vals = means.loc[rv].tolist()
                vals += [vals[0]]
                cats = radar_sel + [radar_sel[0]]
                fig.add_trace(go.Scatterpolar(
                    r=vals, theta=cats, name=label, fill="toself",
                    fillcolor=color, line=dict(color=color, width=2), opacity=0.4
                ))
            fig.update_layout(
                **BASE, height=370,
                polar=dict(
                    bgcolor="rgba(0,0,0,0)",
                    radialaxis=dict(visible=True, gridcolor=BORDER, range=[0,1],
                                   tickfont=dict(color=MUTED, size=9)),
                    angularaxis=dict(gridcolor=BORDER, tickfont=dict(color=LIGHT))
                ),
                legend=dict(orientation="h", yanchor="bottom", y=-0.2, title="",
                            bgcolor="rgba(0,0,0,0)", font=dict(color=LIGHT))
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Selecione ao menos 3 dimensoes.")
        endcard()

    with col_b:
        card(
            "Taxa de Risco por Faixa Etaria e Genero",
            "Cada celula combina uma faixa de idade com um genero e mostra qual percentual de atletas "
            "daquela combinacao esta em risco. Celulas mais azuis concentram mais risco. "
            "Isso permite identificar grupos demograficos que merecem atencao especial."
        )
        hm = (df.groupby(["Faixa_Etaria","Genero"])["Injury_Risk"]
              .mean().reset_index())
        piv = hm.pivot(index="Genero", columns="Faixa_Etaria", values="Injury_Risk")
        fig = go.Figure(go.Heatmap(
            z=piv.values,
            x=[str(c) for c in piv.columns],
            y=piv.index.tolist(),
            colorscale=[[0, CARD2], [0.5, "#1a3a5c"], [1, C0]],
            text=(piv.values * 100).round(1),
            texttemplate="%{text}%",
            textfont=dict(size=13, color=TXT),
            colorbar=dict(title="% risco", tickfont=dict(color=MUTED))
        ))
        fig.update_layout(**BASE, height=370,
                          xaxis_title="Faixa etaria",
                          yaxis_title="Genero")
        st.plotly_chart(fig, use_container_width=True)
        endcard()

# ── Rodape ─────────────────────────────────────────────────────────────────────
st.markdown("<hr class='div'>", unsafe_allow_html=True)
st.markdown(f"<div style='text-align:center;color:{MUTED};font-size:0.72rem;padding-bottom:1rem;'>"
            f"Sports Injury Risk — Analise Exploratoria de Dados — {len(df_all)} registros</div>",
            unsafe_allow_html=True)
