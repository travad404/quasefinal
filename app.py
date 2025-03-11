import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import folium
from streamlit_folium import folium_static

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
        
        # Mapa Interativo
        st.write("### Distribuição Geográfica dos Resíduos")
        mapa = folium.Map(location=[-15.78, -47.93], zoom_start=4)
        for _, row in df_filtered.iterrows():
            folium.Marker(
                location=[-15.78, -47.93],
                popup=f"{row['UF']}: {row[residuos_cols].sum():.2f} toneladas",
                icon=folium.Icon(color="blue")
            ).add_to(mapa)
        folium_static(mapa)
    
    # Comparação entre Unidades de Tratamento
    elif len(unidades) > 1:
        residuos_cols = df_filtered.columns[2:]
        df_melted = df_filtered.melt(id_vars=["UF", "Unidade"], value_vars=residuos_cols, var_name="Resíduo", value_name="Quantidade")
        fig = px.bar(df_melted, x="Resíduo", y="Quantidade", color="Unidade", barmode="group",
                     title="Fluxo de Resíduos por Unidade de Tratamento")
        st.plotly_chart(fig)
    
    # Heatmap dos Resíduos por Estado
    st.write("### Distribuição dos Resíduos por Estado")
    residuos_sum = df_filtered.groupby("UF")[residuos_cols].sum()
    fig_heatmap = go.Figure(data=go.Heatmap(
        z=residuos_sum.values,
        x=residuos_sum.columns,
        y=residuos_sum.index,
        colorscale="Viridis"
    ))
    fig_heatmap.update_layout(title="Heatmap dos Resíduos por Estado", xaxis_title="Tipo de Resíduo", yaxis_title="Estados")
    st.plotly_chart(fig_heatmap)
    
    # TreeMap dos Resíduos
    st.write("### Proporção de Resíduos")
    df_melted = df_filtered.melt(id_vars=["UF", "Unidade"], value_vars=residuos_cols, var_name="Resíduo", value_name="Quantidade")
    fig_treemap = px.treemap(df_melted, path=["UF", "Resíduo"], values="Quantidade", title="TreeMap dos Resíduos")
    st.plotly_chart(fig_treemap)
    
else:
    st.write("Por favor, carregue um arquivo Excel para começar.")
