import requests
import dash
from dash import html, dcc

URL = "https://api.nbp.pl/api/cenyzlota/2024-01-01/2024-12-31/?format=json"

response = requests.get(URL)
data = response.json()

app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children='Ceny Złota w latach 2023-2024', style={'textAlign': 'center'}),
    html.Label("Wybierz rok:"),
    dcc.RadioItems(
        id='year-selector',
        options=[
            {'label': '2023', 'value': '2023'}
        ],
        value='2023'
    ),
    html.Div(children=[
        dcc.Graph(id='gold-price-graph')
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True)
