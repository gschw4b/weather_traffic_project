import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from sqlalchemy import create_engine
import re
import os
from dotenv import load_dotenv

# Função para converter a duração da viagem para minutos
def duracao_para_minutos(duracao_str):
    horas_padrao = r'(\d+)\s*hours?'
    minutos_padrao = r'(\d+)\s*mins?'

    # Busca por horas e minutos na string
    horas = re.search(horas_padrao, duracao_str)
    minutos = re.search(minutos_padrao, duracao_str)

    # Calcula o total de minutos
    total_minutos = 0
    if horas:
        total_minutos += int(horas.group(1)) * 60
    if minutos:
        total_minutos += int(minutos.group(1))

    return total_minutos

# Conecta ao db MySQL
load_dotenv() # Carrega variáveis de ambiente do .env

db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_name = os.getenv('DB_NAME')

conexao_db_str = f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}/{db_name}'
conexao_db = create_engine(conexao_db_str)

# Carrega os dados das tabelas de clima e trafego do db
consulta_clima = "SELECT * FROM clima"
consulta_trafego = "SELECT * FROM trafego"
clima_df = pd.read_sql(consulta_clima, conexao_db)
trafego_df = pd.read_sql(consulta_trafego, conexao_db)

# Converte a coluna 'duracao' de string para numerico (minutos)
trafego_df['duracao_minutos'] = trafego_df['duracao'].apply(duracao_para_minutos)

# Cria um DataFrame para representar as rotas
rotas_df = pd.DataFrame({
    'lat': trafego_df['origem_lat'].tolist() + trafego_df['destino_lat'].tolist(),
    'lon': trafego_df['origem_lon'].tolist() + trafego_df['destino_lon'].tolist(),
    'tipo': ['origem'] * len(trafego_df) + ['destino'] * len(trafego_df),
    'id_rota': list(range(len(trafego_df))) * 2
})

# Cria a aplicação Dash
app = dash.Dash(__name__)

# Layout da aplicação
app.layout = html.Div([
    html.H1("Painel de Clima e Trânsito"),
    dcc.Tabs([
        dcc.Tab(label='Clima', children=[
            html.Div([
                html.H2("Comparação de Temperaturas Máximas e Mínimas"),
                dcc.Graph(
                    id='temperature-bar-chart',
                    figure=px.bar(clima_df, x='cidade', y=['temperatura_min', 'temperatura_max'], barmode='group', title='Temperaturas Máximas e Mínimas por Cidade')
                ),
                html.H2("Mapa de Temperatura Atual"),
                dcc.Graph(
                    id='temperature-map',
                    figure=px.scatter_mapbox(clima_df, lat='latitude', lon='longitude', color='temperatura',
                                             size='temperatura', hover_name='cidade', title='Temperatura Atual por Cidade',
                                             mapbox_style="carto-positron")
                )
            ])
        ]),
        dcc.Tab(label='Trânsito', children=[
            html.Div([
                html.H2("Distância e Duração das Viagens"),
                dcc.Graph(
                    id='distance-duration-bar-chart',
                    figure=px.bar(trafego_df, x='endereco_origem', y=['distancia_km', 'duracao_minutos'], barmode='group', title='Distância e Duração das Viagens por Origem')
                ),
                html.H2("Mapa de Rotas"),
                dcc.Graph(
                    id='routes-map',
                    figure=px.scatter_mapbox(trafego_df, lat='origem_lat', lon='origem_lon', color='distancia_km',
                                             size='distancia_km', hover_name='endereco_origem', title='Rotas de Viagens',
                                             mapbox_style="carto-positron")
                )
            ])
        ])
    ])
])

# Roda a aplicação
if __name__ == '__main__':
    app.run_server(debug=True)