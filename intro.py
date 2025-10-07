import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as pt


st.title("Dashboard Fifa26")

df = pd.read_csv("fifa26.csv")

players_quantity = df["short_name"].count()

st.header("Dados Brutos")
st.dataframe(df)

st.header("Dados Tratados")
st.dataframe(df[["player_url","short_name","player_positions","overall","potential","age","height_cm","value_eur","wage_eur","weight_kg","club_name","nationality_name","club_position"]])

st.header("Gráficos")

st.subheader("Gráfico de Overall x Quantidade de Jogadores")
st.bar_chart(df[["overall","short_name"]].groupby("overall").count())

st.subheader("Gráfico de Potencial x Idade")
fig = pt.bar(
    x = df["age"],
    y = df["potential"],
    labels = {
        "x": "Idade",
        "y": "Potencial"
    }
)

st.plotly_chart(fig)


