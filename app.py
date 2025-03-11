import streamlit as st
import pandas as pd
import plotly.express as px

# Configurar o app
st.title("Visualização de Resíduos por Estado e Unidade de Tratamento")

# Upload do arquivo
uploaded_file = st.file_uploader("Carregue a planilha Excel", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file, sheet_name="2024-11-23T23-14_export")
    
    # Seleção de filtros
    estados = st.multiselect("Selecione os estados", df["UF"].unique())
    unidades = st.multiselect("Selecione as unidades de tratamento", df["Unidade"].unique())
    
    # Filtrar os dados conforme seleção do usuário
    if estados:
        df = df[df["UF"].isin(estados)]
    if unidades:
        df = df[df["Unidade"].isin(unidades)]
    
    # Exibir os dados filtrados
    st.write("### Dados Filtrados", df)
    
    # Verificar a seleção para definir o tipo de gráfico
    if len(estados) > 1:
        # Comparação de resíduos entre estados
        residuos_cols = df.columns[2:]
        df_melted = df.melt(id_vars=["UF", "Unidade"], value_vars=residuos_cols, var_name="Resíduo", value_name="Quantidade")
        fig = px.bar(df_melted, x="Resíduo", y="Quantidade", color="UF", barmode="group",
                     title="Comparação de Resíduos entre Estados")
        st.plotly_chart(fig)
    
    elif len(unidades) > 1:
        # Fluxos de resíduos específicos da unidade de tratamento
        residuos_cols = df.columns[2:]
        df_melted = df.melt(id_vars=["UF", "Unidade"], value_vars=residuos_cols, var_name="Resíduo", value_name="Quantidade")
        fig = px.bar(df_melted, x="Resíduo", y="Quantidade", color="Unidade", barmode="group",
                     title="Fluxo de Resíduos por Unidade de Tratamento")
        st.plotly_chart(fig)
    
    else:
        st.write("Selecione ao menos um estado ou unidade de tratamento para visualizar os gráficos.")
else:
    st.write("Por favor, carregue um arquivo Excel para começar.")
