import requests
import dash
from dash import html, dcc

URL = "https://api.nbp.pl/api/cenyzlota/2024-01-01/2024-12-31/?format=json"

response = requests.get(URL)
data = response.json()

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Podstawy Dash"),
    html.P("Przykład wykorzystania komponentów HTML i interaktywnych."),
    html.Ul([
        html.Li("Pierwszy element listy"),
        html.Li("Drugi element listy"),
        html.Li("Trzeci element listy")
    ]),
    html.Button("Kliknij mnie", id="example-button"),
    dcc.Input(id="example-input", type="text", placeholder="Wpisz coś..."),
    dcc.Graph(id="example-graph")
])

if __name__ == '__main__':
    app.run_server(debug=True)
