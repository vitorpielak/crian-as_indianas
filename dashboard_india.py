# total de crianças
# media geral de horas de tela
# % que excederam o limite de tempo de tela
# media de tempo educacional
# media de tempo recreacional
# barras horizontais impactos na saude x contagem crianças
# total de horas por dispositivo
# genero por localidade


import pandas as pd
import streamlit as st
import plotly_express as px


st.set_page_config(layout='wide')

df = pd.read_csv('Indian_Kids_Screen_Time.csv', delimiter =',')

# LIMPEZA DOS DADOS
df['Gender'] = df['Gender'].map({'Male': 'Masculino', 'Female': 'Feminino'})
generos = df['Gender'].unique().tolist()
generos.insert(0, 'Todos')

df['Urban_or_Rural'] = df['Urban_or_Rural'].map({'Urban': 'Urbano', 'Rural': 'Rural'})
localidades = df['Urban_or_Rural'].unique().tolist()
localidades.insert(0, 'Todos')

# tradução dos impactos na saúde
health_map = {
    'Poor Sleep': 'Sono Ruim',
    'Eye Strain': 'Cansaço Visual',
    'Anxiety': 'Ansiedade',
    'Obesity Risk': 'Risco de Obesidade',
    'None': 'Nenhum'
}
def traduzir_impactos(impactos):
    if pd.isna(impactos):
        return 'Nenhum'
    return ', '.join([health_map.get(i.strip(), i.strip()) for i in impactos.split(',')])
df['Health_Impacts'] = df['Health_Impacts'].apply(traduzir_impactos)

#criar faixa etária
bins = [0, 8, 12, 15, 18, 100]
labels = ['Até 8', '9-12', '13-15', '16-18', '18+']
df['Faixa_Etária'] = pd.cut(df['Age'], bins=bins, labels=labels, right=True, include_lowest=True)
faixas_etarias = df['Faixa_Etária'].unique().tolist()
faixas_etarias.insert(0, 'Todos') # Adiciona a opção 'Todos' no início da lista




#traduzir colunas   
colunas_traduzidas = {
    'Age': 'Idade',
    'Gender': 'Gênero',
    'Avg_Daily_Screen_Time_hr': 'Media_tela_hora',
    'Primary_Device': 'Dispositivo',
    'Exceeded_Recommended_Limit': 'Excedeu_limite_recomendado',
    'Educational_to_Recreational_Ratio': 'Proporcao_educacional_recreacional',
    'Health_Impacts': 'Impactos_na_Saúde',
    'Urban_or_Rural': 'Urbano ou Rural'
}
df = df.rename(columns=colunas_traduzidas)

#streamlit
st.title('Dashboard de Tempo de Tela de Crianças na Índia')
st.sidebar.header('Filtros')


# Filtros
idade = st.sidebar.selectbox('Selecione a faixa etária:', faixas_etarias, index=0)
genero = st.sidebar.selectbox('Selecione o gênero:', generos, index=0)
localidade = st.sidebar.selectbox('Selecione a localidade:', localidades, index=0)

# Aplicar filtros
df_fil = df.copy()

if idade != 'Todos':
    df_fil = df_fil[df_fil['Faixa_Etária'] == idade]

if genero != 'Todos':
    df_fil = df_fil[df_fil['Gênero'] == genero]

if localidade != 'Todos':
    df_fil = df_fil[df_fil['Urbano ou Rural'] == localidade]

col1,col2,col3,col4 = st.columns(4)
col5,col6 = st.columns(2)


col1.metric('Total de Crianças', len(df_fil))
col2.metric('Média Geral de Horas de Tela', f"{df_fil['Media_tela_hora'].mean():.2f} horas")
col3.metric('% que Excederam o Limite de Tempo de Tela', f"{(df_fil['Excedeu_limite_recomendado'].mean() * 100):.2f}%")

df_fil


