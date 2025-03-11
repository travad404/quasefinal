import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

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
    df_filtered = df.copy()
    if estados:
        df_filtered = df_filtered[df_filtered["UF"].isin(estados)]
    if unidades:
        df_filtered = df_filtered[df_filtered["Unidade"].isin(unidades)]
    
    # Exibir KPIs
    st.write("### Visão Geral")
    col1, col2 = st.columns(2)
    col1.metric("Total de Estados", len(df_filtered["UF"].unique()))
    col2.metric("Total de Unidades de Tratamento", len(df_filtered["Unidade"].unique()))
    
    # Exibir dados filtrados
    st.write("### Dados Filtrados", df_filtered)
    
    # Comparação entre Estados
    if len(estados) > 1:
        residuos_cols = df_filtered.columns[2:]
        df_melted = df_filtered.melt(id_vars=["UF", "Unidade"], value_vars=residuos_cols, var_name="Resíduo", value_name="Quantidade")
        fig = px.bar(df_melted, x="Resíduo", y="Quantidade", color="UF", barmode="group",
                     title="Comparação de Resíduos entre Estados")
        st.plotly_chart(fig)
    
    # Comparação entre Unidades de Tratamento por Tipo
    elif len(unidades) > 1:
        residuos_cols = df_filtered.columns[2:]
        df_melted = df_filtered.melt(id_vars=["UF", "Unidade"], value_vars=residuos_cols, var_name="Resíduo", value_name="Quantidade")
        unidade_tipos = df_filtered["Unidade"].unique()
        
        for unidade in unidade_tipos:
            df_unidade = df_melted[df_melted["Unidade"] == unidade]
            fig = px.bar(df_unidade, x="Resíduo", y="Quantidade", color="UF", barmode="group",
                         title=f"Fluxo de Resíduos para {unidade}")
            st.plotly_chart(fig)
    
    # TreeMap dos Resíduos por Estado
    st.write("### Proporção de Resíduos por Estado")
    for estado in df_filtered["UF"].unique():
        df_estado = df_filtered[df_filtered["UF"] == estado]
        df_melted = df_estado.melt(id_vars=["UF", "Unidade"], value_vars=residuos_cols, var_name="Resíduo", value_name="Quantidade")
        fig_treemap = px.treemap(df_melted, path=["Resíduo"], values="Quantidade", title=f"TreeMap dos Resíduos em {estado}")
        st.plotly_chart(fig_treemap)
    
    # TreeMap dos Resíduos por Unidade de Tratamento
    st.write("### Proporção de Resíduos por Unidade de Tratamento")
    for unidade in df_filtered["Unidade"].unique():
        df_unidade = df_filtered[df_filtered["Unidade"] == unidade]
        df_melted = df_unidade.melt(id_vars=["UF", "Unidade"], value_vars=residuos_cols, var_name="Resíduo", value_name="Quantidade")
        fig_treemap = px.treemap(df_melted, path=["Resíduo"], values="Quantidade", title=f"TreeMap dos Resíduos na Unidade {unidade}")
        st.plotly_chart(fig_treemap)
    
else:
    st.write("Por favor, carregue um arquivo Excel para começar.")
