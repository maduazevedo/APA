"""Carregamento e preparo do dataset Sports Injury Risk."""

import streamlit as st
import pandas as pd

DATA_PATH = "df_balanced.csv"


@st.cache_data
def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH)
    df["Genero"] = df["Gender"].map({0: "Masculino", 1: "Feminino"})
    df["Risco"] = df["Injury_Risk"].map({0: "Sem Risco", 1: "Com Risco"})
    df["Faixa_Etaria"] = pd.cut(
        df["Age"], bins=[17, 20, 25, 30, 35, 40],
        labels=["até 20", "21-25", "26-30", "31-35", "36-40"]
    )
    return df


def apply_filters(df: pd.DataFrame, gender_sel, age_sel, risk_sel) -> pd.DataFrame:
    return df[
        df["Genero"].isin(gender_sel) &
        df["Age"].between(*age_sel) &
        df["Risco"].isin(risk_sel)
    ].copy()
