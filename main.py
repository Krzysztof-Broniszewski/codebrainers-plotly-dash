import requests
import dash
import pandas as pd
import plotly.graph_objs as go
from dash import html, dcc
from dash.dependencies import Input, Output
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

combined_df = pd.concat(dfs, keys=dfs.keys()).reset_index(level=0).rename(columns={"level_0": "Rok"})
print(combined_df)

app = dash.Dash(__name__)

app.layout = html.Div(style={'backgroundColor': '#1f2c56', 'color': '#ffffff', 'padding': '20px'},
    children=[
    html.H1(children='Ceny Złota w latach 2023-2024', style={'textAlign': 'center'}),
    html.Label("Wybierz rok:"),
    dcc.RadioItems(
        id='year-selector',
        options=[
            {'label': '2023', 'value': '2023'},
            {'label': '2024', 'value': '2024'},
            {'label': 'Oba lata', 'value': 'all'}
        ],
        value='all',
        inline=True,
        style={'marginBottom': '20px'}
    ),
    html.Div(style={'border': '2px solid #FFD700', 'borderRadius': '15px', 'padding': '10px', 'backgroundColor': '#243a6b'},
    children=[
        dcc.Graph(id='gold-price-graph')
    ])
])

@app.callback(
    Output('gold-price-graph', 'figure'),
    [Input('year-selector', 'value')]
)
def update_graph(selected_year):
    if selected_year == 'all':
        filtered_df = combined_df
    else:
        filtered_df = combined_df[combined_df["Rok"] == selected_year]

    traces = []
    for year in filtered_df["Rok"].unique():
        df_year = filtered_df[filtered_df["Rok"] == year]
        traces.append(go.Scatter(
            x=df_year["data"],
            y=df_year["cena"],
            mode='lines',
            name=f'Cena złota {year}',
            line=dict(color='#FFD700', width=2)
        ))

    layout = {
        'title': 'Zmiany cen złota',
        'xaxis': {'title': 'Data', 'gridcolor': '#4a5a8d', 'tickfont': {'color': 'white'}},
        'yaxis': {'title': 'Cena (PLN)', 'gridcolor': '#4a5a8d', 'tickfont': {'color': 'white'}},
        'plot_bgcolor': '#1f2c56',
        'paper_bgcolor': '#1f2c56',
        'font': {'color': 'white'}
    }

    return {'data': traces, 'layout': layout}

if __name__ == '__main__':
    app.run_server(debug=True)
