


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

# calcular a % de pessoas que excederam o limite recomendado
qtde_true = df[df['Exceeded_Recommended_Limit'] == True].shape[0]
qtde_false = df[df['Exceeded_Recommended_Limit'] == False].shape[0]
excederam_limite = qtde_true / (qtde_true + qtde_false) * 100


# media de tempo educacional
df['Educacional'] = df['Avg_Daily_Screen_Time_hr'] * df['Educational_to_Recreational_Ratio']


# media de tempo recreacional
df['Recreacional'] = df['Avg_Daily_Screen_Time_hr'] * (1-df['Educational_to_Recreational_Ratio'])


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

st.title('Dashboard de Tempo de Tela de Crianças na Índia')
st.markdown(''' A OMS indica que crianças de 2 a 4 anos devem ter no máximo 1 hora de tela por dia, enquanto crianças de 5 a 17 anos devem ter no máximo 2 horas. Este dashboard analisa o tempo de tela de crianças na Índia e os impactos na saúde associados. :sunny: :computer: :baby: ''')


abas = st.tabs(['Visão Geral', 'Outra Análise','Impactos na Saúde','Recreacional e Educacional'])
#streamlit
with abas[0]:
    st.markdown('''## Visão Geral do Tempo de Tela de Crianças na Índia''')
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





    col1,col2,col3,col4,col5 = st.columns(5)
    col6 = st.columns(1)[0]
    col7,col8 = st.columns(2)

    # total de crianças
    col1.metric('Total de Crianças', len(df_fil))

    # media geral de horas de tela
    col2.metric('Média Geral de Horas de Tela', f"{df_fil['Media_tela_hora'].mean():.2f} horas")

    # % que excederam o limite de tempo de tela
    col3.metric('Excederam o Limite de Tempo de Tela', f"{excederam_limite:.2f}%")

    # media de tempo educacional
    col4.metric('Média de Tempo Educacional', f"{df_fil['Educacional'].mean():.2f} horas")

    # media de tempo recreacional
    col5.metric('Média de Tempo Recreacional', f"{df_fil['Recreacional'].mean():.2f} horas")

    # barras horizontais impactos na saude x contagem crianças
    impactos_count = df_fil['Impactos_na_Saúde'].value_counts().reset_index()
    impactos_count.columns = ['Impactos_na_Saúde', 'Contagem']

    fig_impactos = px.bar(
        impactos_count,
        x='Contagem',
        y='Impactos_na_Saúde',
        color='Impactos_na_Saúde',
        orientation='h',
        title='Impactos na Saúde x Contagem de Crianças'
    )
    col6.plotly_chart(fig_impactos, use_container_width=True)


    # total de horas por dispositivo
    fig_dispositivo = px.pie(
        df_fil,
        names='Dispositivo',
        values='Media_tela_hora',
        title='Total de Horas por Dispositivo'
    )
    col7.plotly_chart(fig_dispositivo, use_container_width=True)


    # genero por localidade
    fig_genero_localidade = px.histogram(
        df_fil,
        x='Urbano ou Rural',
        color='Gênero',
        barmode='group',
        title='Gênero por Localidade',
        labels={'Urbano ou Rural': 'Localidade', 'Gênero': 'Gênero', 'count': 'Contagem'}
    )
    col8.plotly_chart(fig_genero_localidade, use_container_width=True)  


    # tabela de dados filtrados
    st.dataframe(df_fil)

with abas[1]:
    st.markdown('''## Análise Detalhada do Tempo de Tela''')
    st.markdown('''Nesta seção, vamos explorar a relação entre idade, tempo médio de tela e gênero, além de analisar o tempo médio por dispositivo e faixa etária.''')
    
    col10 = st.columns(1)[0]
    col11,col12 = st.columns(2)

    #idade x tempo médio x genero dispersão
    fig_dispersao = px.scatter(
        df_fil,
        x='Media_tela_hora',
        y='Idade',
        color='Gênero',
        size='Media_tela_hora',
        hover_data=['Gênero', 'Media_tela_hora'],
        title='Idade x Tempo Médio x Gênero',
        labels={'Media_tela_hora': 'Tempo Médio de Tela (horas)', 'Idade': 'Idade', 'Gênero': 'Gênero'},
        color_discrete_map={
            'Masculino': '#339CFF',   # Azul
            'Feminino': '#FF69B4'     # Rosa
        }
)
    
    col10.plotly_chart(fig_dispersao, use_container_width=True)

    #tempo médio por dipositivo x genero matriz
    fig_matriz = px.imshow(
        df_fil.pivot_table(index='Dispositivo', columns='Gênero', values='Media_tela_hora', aggfunc='mean'),
        title='Tempo Médio por Dispositivo x Gênero',
        labels={'x': 'Gênero', 'y': 'Dispositivo', 'color': 'Tempo Médio de Tela (horas)'},
        color_continuous_scale='Viridis'
    )
    col11.plotly_chart(fig_matriz, use_container_width=True)

    #tempo médio de uso x genero x faixa etaria barras
    fig_barras = px.bar(
        df_fil,
        x='Faixa_Etária',
        y='Media_tela_hora',
        color='Gênero',
        barmode='group',
        title='Tempo Médio de Uso x Gênero x Faixa Etária',
        labels={'Faixa_Etária': 'Faixa Etária', 'Media_tela_hora': 'Tempo Médio de Tela (horas)', 'Gênero': 'Gênero'}
    )
    col12.plotly_chart(fig_barras, use_container_width=True)

with abas[2]:
    
    st.markdown('''## Análise dos Impactos na Saúde''')
    st.markdown('''Entre os principais impactos na saúde identificados estão: Sono Ruim, Cansaço Visual, Ansiedade e Risco de Obesidade. Vamos analisar como esses impactos variam entre diferentes dispositivos e ocorrências.''')
    col13 = st.columns(1)[0]
    col14,col15 = st.columns(2)

    #impactos na saude por dispositivo barras horizontais
    impactos_dispositivo = df_fil.groupby('Dispositivo')['Impactos_na_Saúde'].value_counts().unstack().fillna(0)
    impactos_dispositivo = impactos_dispositivo.div(impactos_dispositivo.sum(axis=1),
                                                        axis=0) * 100
    impactos_dispositivo = impactos_dispositivo.reset_index().melt(id_vars='Dispositivo', var_name='Impactos_na_Saúde', value_name='Percentual')
    fig_impactos_dispositivo = px.bar(
        impactos_dispositivo,
        x='Percentual',
        y='Dispositivo',
        color='Impactos_na_Saúde',
        orientation='h',
        title='Impactos na Saúde por Dispositivo',
        labels={'Percentual': 'Percentual (%)', 'Dispositivo': 'Dispositivo', 'Impactos_na_Saúde': 'Impactos na Saúde'}
    )
    col13.plotly_chart(fig_impactos_dispositivo, use_container_width=True)

    #impactos na saúde por ocorrencia treemap
    impactos_ocorrencia = df_fil['Impactos_na_Saúde'].value_counts().reset_index()
    impactos_ocorrencia.columns = ['Impactos_na_Saúde', 'Contagem']
    fig_impactos_ocorrencia = px.treemap(
        impactos_ocorrencia,
        path=['Impactos_na_Saúde'],
        values='Contagem',
        title='Impactos na Saúde por Ocorrência',
        labels={'Impactos_na_Saúde': 'Impactos na Saúde', 'Contagem': 'Contagem'}
    )
    col14.plotly_chart(fig_impactos_ocorrencia, use_container_width=True)

    #problemas reportados vs problemas não reportados barra vertical
    problemas_reportados = df_fil['Impactos_na_Saúde'].apply(lambda x: 'Nenhum' not in x).value_counts().reset_index()
    problemas_reportados.columns = ['Problemas Reportados', 'Contagem']
    fig_problemas_reportados = px.bar(
        problemas_reportados,
        x='Problemas Reportados',
        y='Contagem',
        title='Problemas Reportados vs Problemas Não Reportados',
        labels={'Problemas Reportados': 'Problemas Reportados', 'Contagem': 'Contagem'},
        color='Problemas Reportados',
        color_discrete_map={True: '#FF6347', False: '#90EE90'}  # Tomate e Verde Claro
    )
    col15.plotly_chart(fig_problemas_reportados, use_container_width=True)

with abas[3]:
    col16 = st.columns(1)[0]
    col17 = st.columns(1)[0]
    #educacional  e recrecional por dispositivo
    fig_educacional_recreacional = px.bar(
        df_fil,
        x='Dispositivo',
        y=['Educacional', 'Recreacional'],
        title='Tempo Educacional e Recreacional por Dispositivo',
        labels={'value': 'Tempo (horas)', 'variable': 'Tipo', 'Dispositivo': 'Dispositivo'},
        barmode='group'
    )  
    col16.plotly_chart(fig_educacional_recreacional, use_container_width=True)

