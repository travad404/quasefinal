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
    
    # Separar classificações especiais
    colunas_extras = ["Redução Peso Líquido", "Redução Peso Seco", "Valor energético (Mj/ton)", "Outros", "Outros processados"]
    residuos_cols = [col for col in df.columns if col not in colunas_extras and col not in ["UF", "Unidade"]]
    
    # Criar tabs
    tab1, tab2 = st.tabs(["Resíduos Gerais", "Classificações Especiais"])
    
    with tab1:
        # Filtrar os dados conforme seleção do usuário
        df_filtered = df[["UF", "Unidade"] + residuos_cols].copy()
        if estados:
            df_filtered = df_filtered[df_filtered["UF"].isin(estados)]
        if unidades:
            df_filtered = df_filtered[df_filtered["Unidade"].isin(unidades)]
        
        # Exibir KPIs
        st.write("### Visão Geral")
        col1, col2 = st.columns(2)
        col1.metric("Total de Estados", len(df_filtered["UF"].unique()))
        col2.metric("Total de Unidades de Tratamento", len(df_filtered["Unidade"].unique()))
        
        # Comparação entre Estados
        if len(estados) > 1:
            df_melted = df_filtered.melt(id_vars=["UF", "Unidade"], value_vars=residuos_cols, var_name="Resíduo", value_name="Quantidade")
            fig = px.bar(df_melted, x="Resíduo", y="Quantidade", color="UF", barmode="group",
                         title="Comparação de Resíduos entre Estados")
            st.plotly_chart(fig)
        
        # Comparação entre Unidades de Tratamento por Tipo dentro de cada Estado
        if len(estados) > 1:
            for estado in estados:
                df_estado = df_filtered[df_filtered["UF"] == estado]
                df_melted = df_estado.melt(id_vars=["UF", "Unidade"], value_vars=residuos_cols, var_name="Resíduo", value_name="Quantidade")
                for unidade in df_estado["Unidade"].unique():
                    df_unidade = df_melted[df_melted["Unidade"] == unidade]
                    fig = px.bar(df_unidade, x="Resíduo", y="Quantidade", color="UF", barmode="group",
                                 title=f"Fluxo de Resíduos para {unidade} em {estado}")
                    st.plotly_chart(fig)
        
        # TreeMap dos Resíduos por Estado individualmente
        st.write("### Proporção de Resíduos por Estado")
        for estado in df_filtered["UF"].unique():
            df_estado = df_filtered[df_filtered["UF"] == estado]
            df_melted = df_estado.melt(id_vars=["UF", "Unidade"], value_vars=residuos_cols, var_name="Resíduo", value_name="Quantidade")
            fig_treemap = px.treemap(df_melted, path=["Resíduo"], values="Quantidade", title=f"TreeMap dos Resíduos em {estado}")
            st.plotly_chart(fig_treemap)
    
    with tab2:
        st.write("### Classificações Especiais")
        df_filtered_class = df[["UF", "Unidade"] + colunas_extras].copy()
        if estados:
            df_filtered_class = df_filtered_class[df_filtered_class["UF"].isin(estados)]
        if unidades:
            df_filtered_class = df_filtered_class[df_filtered_class["Unidade"].isin(unidades)]
        
        for coluna in colunas_extras:
            df_classificacao = df_filtered_class[["UF", "Unidade", coluna]].dropna().copy()
            df_melted = df_classificacao.melt(id_vars=["UF", "Unidade"], value_vars=[coluna], var_name="Classificação", value_name="Valor")
            fig_classificacao = px.bar(df_melted, x="UF", y="Valor", color="Unidade", barmode="group",
                                       title=f"{coluna} por Estado e Unidade de Tratamento")
            st.plotly_chart(fig_classificacao, key=coluna)
else:
    st.write("Por favor, carregue um arquivo Excel para começar.")
