import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Análise de Produtividade",
    layout="wide",
)

df= pd.read_csv("https://raw.githubusercontent.com/redsonlopez/productivity/refs/heads/main/data/dataset.csv")

view_option = st.sidebar.radio('Escolha o tipo de exibição', ('Introdução', 'Gráficos', 'Relatório'))

st.sidebar.header("Filtro")

multiselect_categoria = st.sidebar.multiselect('Selecione múltiplas Categorias', options=df['TURNO'].unique(), default=df['TURNO'].unique())

df_filtrado = df[(df['PRODUTIVIDADE'] >= df['PRODUTIVIDADE'].min()) & (df['PRODUTIVIDADE'] <= df['PRODUTIVIDADE'].max())]
if multiselect_categoria:
    df_filtrado = df_filtrado[df_filtrado['TURNO'].isin(multiselect_categoria)]

st.title("Análise de Produtividade")

if view_option == 'Introdução':
    st.header("Introdução ao Painel de Análise de Produtividade")
    st.markdown("""
Bem-vindo ao **Painel de Análise de Produtividade**! Este painel foi desenvolvido para facilitar a análise e visualização de dados da produtividade pessoal de Hedson Lopes ao longo dos diferentes períodos do dia, coletados ao longo dos 30 dias. Utilizando gráficos interativos e relatórios dinâmicos, é possível explorar como o desempenho varia entre os turnos da manhã, tarde e noite.

### Contexto dos Dados:
Os dados apresentados neste painel foram coletados diariamente durante o mês de junho. Cada dia foi avaliado e classificado com base em três categorias de produtividade:
- **Baixa produtividade (1)**: Indicando momentos de baixa eficiência.
- **Produtividade média (5)**: Representando um desempenho satisfatório.
- **Alta produtividade (9)**: Refletindo um alto nível de desempenho.

### Tipos de Exibição:
- **Gráficos**: A visualização gráfica, incluindo gráficos de barras e de linhas, permite uma análise clara das tendências de produtividade ao longo do mês, destacando os períodos mais e menos produtivos.
- **Relatório**: Além dos gráficos, uma tabela detalhada exibe os dados filtrados, permitindo uma visão mais específica dos registros diários coletados.

### Utilização do Painel:
- Utilize o filtro na barra lateral para selecionar o turno específico que deseja analisar.
- Explore as visualizações para identificar padrões e entender quais horários e dias foram mais produtivos ao longo do mês.

Este painel interativo foi criado para auxiliar no autoconhecimento e na otimização da gestão do tempo, facilitando decisões mais informadas sobre como organizar tarefas diárias de forma eficiente.
""")

elif view_option == 'Gráficos':
    col1, col2= st.columns([1, 2])

    with col1:
        fig_bar = px.bar(df_filtrado, x='TURNO', y='PRODUTIVIDADE', title="Produtividade por turno", color='PRODUTIVIDADE')
        st.plotly_chart(fig_bar, use_container_width=True)

    with col2:
        fig_line = px.line(df_filtrado, x='DATA', y='PRODUTIVIDADE', title="Série temporal da produtividade", color='TURNO')
        st.plotly_chart(fig_line, use_container_width=True)
        
    col3= st.container()

    with col3:
        fig_bar = px.bar(df_filtrado, x='PRODUTIVIDADE', y='DATA', title="Produtividade por data", color='PRODUTIVIDADE', orientation= "h")
        st.plotly_chart(fig_bar, use_container_width=True)

else:
    turno_sum = df_filtrado.groupby('TURNO')['PRODUTIVIDADE'].sum()
    col4, col5 = st.columns(2)

    with col4:
        st.subheader("Relatório de dados")
        st.dataframe(df_filtrado)  

    with col5:
        st.subheader("Produtividade total por turno")
        st.write(f"• Manhã: {turno_sum.get('MANHA', 0)}")
        st.write(f"• Tarde: {turno_sum.get('TARDE', 0)}")
        st.write(f"• Noite: {turno_sum.get('NOITE', 0)}")

