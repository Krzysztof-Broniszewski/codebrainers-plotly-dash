import requests
import dash
import pandas as pd
from dash import html, dcc
from requests.exceptions import Timeout, RequestException, HTTPError 

URLS = {
    "2023": "https://api.nbp.pl/api/cenyzlota/2023-01-01/2023-12-31/?format=json",
    "2024": "https://api.nbp.pl/api/cenyzlota/2024-01-01/2024-12-31/?format=json"
}

dfs = {}
try:
    for year, url in URLS.items():
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data)
            df["data"] = pd.to_datetime(df["data"])
            df.sort_values("data", inplace=True)
            dfs[year] = df
except Timeout:
    print(f"Error: Request timed out")
    data = []
except HTTPError as http_err:
    print(f"HTTP Error occured: {http_err}")
    data = []
except RequestException as req_err:
    print(f"Error fetching data: {req_err}")
    data = []
except Exception as e:
    print(f"Unexpected error: {e}")
    data = []

print(dfs)

app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children='Ceny Złota w latach 2023-2024', style={'textAlign': 'center'}),
    html.Label("Wybierz rok:"),
    dcc.RadioItems(
        id='year-selector',
        options=[
            {'label': '2023', 'value': '2023'},
            {'label': '2024', 'value': '2024'},
            {'label': 'Oba lata', 'value': 'all'}
        ],
        value='all'
    ),
    html.Div(children=[
        dcc.Graph(id='gold-price-graph')
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True)
