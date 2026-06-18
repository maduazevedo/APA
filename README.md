# Sports Injury Risk — Dashboard

Dashboard exploratório sobre fatores associados ao risco de lesão em atletas.

## Estrutura

```
app.py                  → orquestrador: sidebar, KPIs, abas
theme.py                → tokens de cor (dark/light) + helpers de estilo Plotly
data.py                 → carregamento e filtros do dataset
components.py           → cards, KPIs e divisores reutilizáveis (sem texto de insight)
df_balanced.csv         → dataset (Kaggle, 694 registros, balanceado)
charts/
  perfil.py             → aba Perfil do Atleta (idade, IMC)
  treino.py             → aba Hábitos de Treino (frequência, intensidade, aquecimento)
  recuperacao.py        → aba Recuperação (sono, estresse, tempo de recuperação)
  condicao.py           → aba Condição Física (assimetria muscular, histórico de lesão)
  visao_geral.py         → aba Visão Geral (correlação, diferença entre grupos, idade×gênero)
```

## Como rodar

```bash
pip install streamlit pandas numpy plotly scipy
streamlit run app.py
```

O arquivo `df_balanced.csv` precisa estar na mesma pasta que `app.py`.

## Decisões de design

**Sem textos de interpretação fixos.** Os cards trazem apenas o título do
gráfico — o insight deve ser obtido olhando o gráfico, não lendo um
parágrafo ao lado. Isso segue o princípio de que o gráfico certo comunica
por si só.

**Gráficos simplificados conforme a força real do sinal.** Antes de
desenhar cada gráfico, a correlação da variável com `Injury_Risk` foi
verificada. Variáveis com correlação muito baixa (IMC, idade, tempo de
aquecimento, tempo de recuperação, estresse — todas abaixo de 0.1 em
módulo) ganharam visualizações diretas (boxplot, barras simples), sem
suavizações (KDE), linhas de tendência (OLS) ou violinos que sugerem uma
nuance que o dado não sustenta. Variáveis com sinal real (`Injury_History`,
`Training_Intensity`, `Muscle_Asymmetry`, `Sleep_Hours`) mantiveram
gráficos que destacam essa diferença com clareza.

**Radar substituído por barras ordenadas.** O gráfico de radar comparando
os dois grupos foi trocado por um gráfico de barras horizontais mostrando
a diferença normalizada de cada variável entre quem está em risco e quem
não está, ordenado da maior para a menor diferença. Um radar com 7+ eixos
exige comparar áreas de contornos sobrepostos — o que é cognitivamente
custoso e impreciso. As barras ordenadas respondem direto à pergunta "o
que mais diferencia os grupos", com o ranking já pronto.

**Scatter com regressão removido.** O gráfico de duração × intensidade de
treino com linha de tendência OLS foi removido, pois ambas as variáveis
têm correlação fraca com o risco isoladamente — uma regressão ali sugeria
uma relação que os dados não sustentam. A intensidade (que tem sinal real)
passou a ter seu próprio gráfico de barras por faixa, no mesmo padrão dos
demais gráficos de taxa de risco.

**Tema dark/light corrigido.** Todas as cores de UI (fundo, texto, bordas,
grid dos gráficos) vêm de um único dicionário de tokens em `theme.py`,
selecionado por `st.session_state.theme_mode`. O bug original acontecia
porque as cores estavam soltas em constantes globais fixas (`BG`, `CARD`
etc.) — agora qualquer parte do app que precisa de cor lê do tema ativo,
então alternar o botão "Modo claro / Modo escuro" na sidebar re-renderiza
tudo corretamente.
