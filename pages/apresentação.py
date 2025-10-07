import streamlit as st
import plotly.express as pt
import pandas as pd
import numpy as np

df = pd.read_csv("fifa26.csv")

st.title("Apresentação de Dados sobre o FIFA 26")

st.write("""
Este dashboard apresenta uma análise detalhada dos dados dos jogadores do FIFA 26.
""")

st.subheader("Grafico de Porcentagem de Posições")
position_counts = df["club_position"].value_counts()

fig = pt.bar(
    x=position_counts.values,
    y=position_counts.index,
    orientation="h",
    labels={
        "x": "Quantidade de Jogadores",
        "y": "Posições"
    },
    text_auto=True
)

fig.update_layout(yaxis={'categoryorder':'total ascending'})

st.plotly_chart(fig, use_container_width=True)


st.subheader("Grafico de Idade dos Jogadores")
fig = pt.histogram(
    df,
    x="age",
    nbins=20,
    labels={
        "age": "Idade",
        "count": "Quantidade de Jogadores"
    },
    title="Distribuição de Idade dos Jogadores"
)

st.plotly_chart(fig, use_container_width=True)


st.subheader("Grafico de Overall x Valor")
fig = pt.scatter(
    df,
    x="overall",
    y="value_eur",
    labels={
        "overall": "Overall",
        "value_eur": "Valor"
    },
    title="Relação Entre Overall e Valor"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("Paises com Mais Talentos no FIFA 26")
data_for_map = df['nationality_name'].value_counts().reset_index()
data_for_map.columns = ['country', 'player_count']

# 2. Crie o gráfico
fig = pt.choropleth(
    data_for_map,
    locations="country",            
    locationmode="country names",    
    color="player_count",           
    hover_name="country",            
    color_continuous_scale=pt.colors.sequential.Plasma, 
    title="Distribuição de Jogadores por País"
)

st.plotly_chart(fig, use_container_width=True)


st.header("Scout interativo")

st.write("Selecione os atributos para encontrar jogadores:")

age_range = st.slider("Idade", min_value=int(df["age"].min()), max_value=int(df["age"].max()), value=(int(df["age"].min()), int(df["age"].max())), key="age_range")

overall_range = st.slider("Overall", min_value=int(df["overall"].min()), max_value=int(df["overall"].max()), value=(int(df["overall"].min()), int(df["overall"].max())), key="overall_range")

potential_range = st.slider("Potencial", min_value=int(df["potential"].min()), max_value=int(df["potential"].max()), value=(int(df["potential"].min()), int(df["potential"].max())), key="potential_range")

st.multiselect("Posições", options=df["club_position"].unique(), default=df["club_position"].unique(), key="positions")

st.multiselect("Ligas", options=df["league_name"].unique(), default=df["league_name"].unique(), key="leagues")


st.subheader("Jogadores Encontrados")
filtered_df = df[
    (df["age"].between(*st.session_state.age_range)) &
    (df["overall"].between(*st.session_state.overall_range)) &
    (df["potential"].between(*st.session_state.potential_range)) &
    (df["club_position"].isin(st.session_state.positions)) &
    (df["league_name"].isin(st.session_state.leagues))
]

st.dataframe(filtered_df[["short_name","player_positions","overall","potential","age","value_eur","club_name","nationality_name","club_position"]])


st.subheader("Grafico de Overall x Potencial")
promessas = df[(df['age'] <= 23) & (df['potential'] >= 85)].sort_values('short_name')

estrelas = df[(df['age'] > 26) & (df['overall'] >= 87)].sort_values('short_name')

col1, col2 = st.columns(2)
with col1:
    promessa_selecionada = st.selectbox("Selecione uma promessa", promessas["short_name"].unique(), key="promessa_selection")
with col2:
    estrela_selecionada = st.selectbox("Selecione uma estrela", estrelas["short_name"].unique(), key="estrela_selection")
    
    promessa_data = promessas[promessas["short_name"] == promessa_selecionada].iloc[0]
    estrela_data = estrelas[estrelas["short_name"] == estrela_selecionada].iloc[0]
    
    idade_auge = 27
    idade_aposentadoria = 38
    
    idade_atual_p = int(promessa_data["age"])
    overall_atual_p = int(promessa_data["overall"])
    potential_p = int(promessa_data["potential"])
    
    crescimento_anos = np.arange(idade_atual_p, idade_auge + 1)
    crescimento_overall = np.linspace(overall_atual_p, potential_p, len(crescimento_anos))
    
    decaimento_anos = np.arange(idade_auge + 1, idade_aposentadoria + 1)
    decaimento_overall = np.linspace(potential_p, overall_atual_p - 10, len(decaimento_anos))
    
    anos = np.concatenate((crescimento_anos, decaimento_anos))
    overall = np.concatenate((crescimento_overall, decaimento_overall))
    
    
    df_grafico = pd.DataFrame({
        'Jogador': promessa_selecionada,
        "Idade": anos,
        "Overall Projetado": overall
    })
    
    df_grafico_estrela = pd.DataFrame({
        'Jogador': estrela_selecionada,
        "Idade": np.arange(int(estrela_data["age"]), idade_aposentadoria + 1),
        "Overall Projetado": np.linspace(int(estrela_data["overall"]), int(estrela_data["overall"]) - 15, idade_aposentadoria - int(estrela_data["age"]) + 1)
    })
    
    df_plot = pd.concat([df_grafico, df_grafico_estrela])
    
    fig = pt.line(
        df_plot,
        x="Idade",
        y="Overall Projetado",
        color="Jogador",
        markers=True,
        labels={
            "Idade": "Idade",
            "Overall Projetado": "Overall Projetado"
        },
        title=f'Projeção de Overall: {promessa_selecionada} vs {estrela_selecionada}'
    )
    
    fig.update_traces(
        selector={"name": f"Nivel de {estrela_selecionada}"},
        line={"dash": "dash"}
        )
    
    st.plotly_chart(fig, use_container_width=True)

