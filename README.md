# Sports Injury Risk — Dashboard

Dashboard interativo para explorar os fatores associados ao risco de lesão em atletas. A ideia central é simples: dado um conjunto de informações sobre o atleta — quanto dorme, com que frequência treina, se já se machucou antes — **o que mais diferencia quem está em risco de quem não está?**

Desenvolvido com Python, Streamlit e Plotly.

---

## O que o dashboard faz

Na barra lateral, você aplica filtros por gênero, faixa etária e situação de risco. O painel inteiro atualiza em tempo real mostrando apenas os atletas que correspondem à seleção — inclusive um indicador visual (gauge) com a taxa de risco percentual do grupo filtrado.

No topo da página, cinco cards resumem o grupo selecionado: total de atletas, quantos estão em risco, taxa de risco, sono médio e nível de estresse médio.

O conteúdo está organizado em cinco abas:

| Aba | O que mostra |
|---|---|
| **Perfil do Atleta** | Distribuição de idade, IMC e proporção por gênero |
| **Hábitos de Treino** | Frequência, duração, aquecimento e intensidade de treino comparados entre grupos |
| **Recuperação** | Horas de sono, nível de estresse e tempo de recuperação entre sessões |
| **Condição Física** | Assimetria muscular e histórico de lesões anteriores |
| **Visão Geral** | Mapa de correlação, ranking de variáveis diferenciadoras e taxa de risco por faixa etária e gênero |

---

## Dataset

**Sports Injury Risk** — disponível no Kaggle.
694 registros de atletas com 15 variáveis: idade, gênero, IMC, frequência e duração de treino, tempo de aquecimento, horas de sono, flexibilidade, assimetria muscular, tempo de recuperação, histórico de lesões, nível de estresse, intensidade de treino e risco de lesão (variável alvo).

O arquivo usado é `df_balanced.csv` — versão balanceada e normalizada entre atletas em risco e sem risco.

---

## Como rodar localmente

**1. Instale as dependências:**
```bash
pip install streamlit pandas numpy plotly scipy
```

**2. Execute o app:**
```bash
streamlit run app.py
```

O arquivo `df_balanced.csv` precisa estar na mesma pasta que `app.py`.

---

## Prompt base

Caso queira recriar ou adaptar o projeto com um assistente de IA:

> Crie um dashboard analítico no Streamlit chamado **Sports Injury Risk** usando o dataset `df_balanced.csv` 
> e crie 5 abas para que eu possa adicionar gráficos posteriormente:
> - **Perfil do Atleta:**
> - **Hábitos de Treino:** 
> - **Recuperação:** 
> - **Condição Física:** 
> - **Visão Geral:** 

---

## Estrutura do projeto

```
app.py              → ponto de entrada: sidebar, KPIs e abas
theme.py            → paleta de cores dark/light e estilos dos gráficos
data.py             → leitura e filtragem do dataset
components.py       → cards e elementos visuais reutilizáveis
df_balanced.csv     → dataset (694 registros)
charts/
  perfil.py         → aba Perfil do Atleta
  treino.py         → aba Hábitos de Treino
  recuperacao.py    → aba Recuperação
  condicao.py       → aba Condição Física
  visao_geral.py    → aba Visão Geral
```

---
