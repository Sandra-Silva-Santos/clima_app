import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import geopandas as gpd
from datetime import datetime, timedelta

# Lista de estados brasileiros com coordenadas aproximadas (latitude, longitude)
estados = {
    "Acre": (-9.9754, -67.8249),
    "Alagoas": (-9.5713, -35.7727),
    "Amapá": (0.0340, -51.0664),
    "Amazonas": (-3.4168, -65.8561),
    "Bahia": (-12.5797, -41.7007),
    "Ceará": (-3.7172, -38.5434),
    "Distrito Federal": (-15.7998, -47.8645),
    "Espírito Santo": (-20.2976, -40.2958),
    "Goiás": (-16.6869, -49.2648),
    "Maranhão": (-2.5307, -44.3068),
    "Mato Grosso": (-15.5989, -56.0949),
    "Mato Grosso do Sul": (-20.4697, -54.6201),
    "Minas Gerais": (-19.9288, -43.9386),
    "Pará": (-1.4558, -48.4902),
    "Paraíba": (-7.1153, -34.8640),
    "Paraná": (-25.4284, -49.2731),
    "Pernambuco": (-8.0476, -34.8770),
    "Piauí": (-5.0920, -42.8038),
    "Rio de Janeiro": (-22.9068, -43.1729),
    "Rio Grande do Norte": (-5.7945, -35.2110),
    "Rio Grande do Sul": (-30.0346, -51.2177),
    "Rondônia": (-8.7612, -63.9020),
    "Roraima": (2.8235, -60.6758),
    "Santa Catarina": (-27.5954, -48.5480),
    "São Paulo": (-23.5489, -46.6388),
    "Sergipe": (-10.9472, -37.0731),
    "Tocantins": (-10.1841, -48.3338)
}

# Função para obter dados climáticos da API Open-Meteo
def get_weather_data(lat, lon):
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
    
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=temperature_2m_max,temperature_2m_min,temperature_2m_mean,relative_humidity_2m_mean,relative_humidity_2m_max,relative_humidity_2m_min&start_date={start_date}&end_date={end_date}&timezone=America/Sao_Paulo"
    
    response = requests.get(url)
    data = response.json()
    
    df = pd.DataFrame({
        'Data': data['daily']['time'],
        'Temp Média': data['daily']['temperature_2m_mean'],
        'Temp Máxima': data['daily']['temperature_2m_max'],
        'Temp Mínima': data['daily']['temperature_2m_min'],
        'Umidade Média': data['daily']['relative_humidity_2m_mean'],
        'Umidade Máxima': data['daily']['relative_humidity_2m_max'],
        'Umidade Mínima': data['daily']['relative_humidity_2m_min']
    })
    return df

# Carregar dados geográficos dos estados brasileiros
@st.cache_data
def load_geo_data():
    url = "https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson"
    gdf = gpd.read_file(url)
    return gdf

# Interface com Streamlit
st.title("Análise Climática para Cultivo de Café no Brasil")

# Dropdown para selecionar estado
estado = st.selectbox("Selecione um Estado", ["Selecione um Estado"] + list(estados.keys()))

if estado != "Selecione um Estado":
    lat, lon = estados[estado]

    # Obter dados climáticos
    df = get_weather_data(lat, lon)

    # Exibir métricas
    st.subheader(f"Dados Climáticos de {estado} (Últimos 30 dias)")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Temperatura Média", f"{df['Temp Média'].mean():.1f}°C")
        st.metric("Temperatura Máxima", f"{df['Temp Máxima'].max():.1f}°C")
        st.metric("Temperatura Mínima", f"{df['Temp Mínima'].min():.1f}°C")
    with col2:
        st.metric("Umidade Média", f"{df['Umidade Média'].mean():.1f}%")
        st.metric("Umidade Máxima", f"{df['Umidade Máxima'].max():.1f}%")
        st.metric("Umidade Mínima", f"{df['Umidade Mínima'].min():.1f}%")

    # Gráficos de temperatura
    fig_temp = go.Figure()
    fig_temp.add_trace(go.Scatter(x=df['Data'], y=df['Temp Média'], name='Média', line=dict(color='blue')))
    fig_temp.add_trace(go.Scatter(x=df['Data'], y=df['Temp Máxima'], name='Máxima', line=dict(color='red')))
    fig_temp.add_trace(go.Scatter(x=df['Data'], y=df['Temp Mínima'], name='Mínima', line=dict(color='green')))
    fig_temp.update_layout(title='Temperatura (°C)', xaxis_title='Data', yaxis_title='Temperatura')
    st.plotly_chart(fig_temp)

    # Gráficos de umidade
    fig_hum = go.Figure()
    fig_hum.add_trace(go.Scatter(x=df['Data'], y=df['Umidade Média'], name='Média', line=dict(color='blue')))
    fig_hum.add_trace(go.Scatter(x=df['Data'], y=df['Umidade Máxima'], name='Máxima', line=dict(color='red')))
    fig_hum.add_trace(go.Scatter(x=df['Data'], y=df['Umidade Mínima'], name='Mínima', line=dict(color='green')))
    fig_hum.update_layout(title='Umidade (%)', xaxis_title='Data', yaxis_title='Umidade')
    st.plotly_chart(fig_hum)

    # Mapa geográfico com heatmap
    st.subheader("Mapa Geográfico Com a Temperatura Média por Estado")
    gdf = load_geo_data()

    # Obter temperaturas médias para todos os estados
    data = []
    for estado_key, (lat, lon) in estados.items():
        temp_data = get_weather_data(lat, lon)
        temp_mean = temp_data['Temp Média'].mean()
        data.append({
            'Estado': estado_key,
            'Temperatura Média': temp_mean
        })

    df_geo = pd.DataFrame(data)
    gdf = gdf.merge(df_geo[['Estado', 'Temperatura Média']], 
                    left_on='name', right_on='Estado', how='left')

    # Criar mapa geográfico com heatmap (escala contínua)
    fig_map = px.choropleth(
        gdf,
        geojson=gdf.geometry,
        locations=gdf.index,
        color='Temperatura Média',
        color_continuous_scale='RdYlGn_r',  # Escala de vermelho (quente) a verde (ideal)
        range_color=[15, 28],  # Intervalo de temperatura para o cultivo
        hover_data=['Estado', 'Temperatura Média'],
        labels={'Temperatura Média': 'Temp Média (°C)'}
    )
    fig_map.add_scattergeo(
        lat=[lat for lat, lon in estados.values()],
        lon=[lon for lat, lon in estados.values()],
        hoverinfo='skip',
        mode='markers',
        marker=dict(size=5, color='black')
    )
    fig_map.update_geos(fitbounds="locations", visible=False)
    fig_map.update_layout(
        coloraxis_colorbar_title="Temperatura (°C)",
        margin={"r":0,"t":50,"l":0,"b":0},
        annotations=[
            dict(
                x=0.5,
                y=-0.1,
                xref="paper",
                yref="paper",
                text="Ideal: 18-24°C | Não Ideal: 25-29°C | Não Recomendado: >30°C",
                showarrow=False
            )
        ]
    )
    st.plotly_chart(fig_map)