import requests
import dash
from dash import html

URL = "https://api.nbp.pl/api/cenyzlota/2024-01-01/2024-12-31/?format=json"

response = requests.get(URL)
data = response.json()

app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1("Witaj w Dash!"),
])

if __name__ == '__main__':
    app.run_server(debug=True)
