import requests
import dash
from dash import html, dcc

URL = "https://api.nbp.pl/api/cenyzlota/2024-01-01/2024-12-31/?format=json"

response = requests.get(URL)
data = response.json()

app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children='Ceny Złota w latach 2023-2024', style={'textAlign': 'center'})
])

if __name__ == '__main__':
    app.run_server(debug=True)
