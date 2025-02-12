import requests
import dash
import pandas as pd
import plotly.graph_objs as go
from dash import html, dcc
from dash.dependencies import Input, Output
from requests.exceptions import Timeout, RequestException, HTTPError 

URLS = {
    "2022": "https://api.nbp.pl/api/cenyzlota/2022-01-01/2022-12-31/?format=json",
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

app = dash.Dash(__name__)

app.layout = html.Div(style={'backgroundColor': '#1f2c56', 'color': '#ffffff', 'padding': '20px'},
    children=[
    html.H1(children='Ceny Złota w latach 2023-2024', style={'textAlign': 'center'}),
    html.Label("Wybierz rok:"),
    dcc.Checklist(
        id='year-selector',
        options=[
            {'label': '2022', 'value': '2022'},
            {'label': '2023', 'value': '2023'},
            {'label': '2024', 'value': '2024'},
        ],
        value=['2022', '2023', '2024'],
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
    if not selected_year:
        return {'data': [], 'layout': {'title': 'Wybierz przynajmniej jeden rok !'}}

    if selected_year == 'value':
        filtered_df = combined_df
    else:
        filtered_df = combined_df[combined_df["Rok"].isin(selected_year)]

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
    event_dates = {
        "2022-02-24": "Początek wojny na Ukrainie",
        "2024-02-01": "Historyczne maksima cen złota",
        "2024-06-01": "Rekordowy popyt na złoto"
    }

    for date, label in event_dates.items():
        traces.append(go.Scatter(
            x=[date, date],
            y=[filtered_df["cena"].min(), filtered_df["cena"].max()],
            mode="lines",
            name=label,
            line=dict(color="red", width=2, dash="dash")
        ))

        traces.append(go.Scatter(
            x=[date],
            y=[filtered_df["cena"].max()],
            text=[f"📌 {label}"],
            mode="text",
            textposition="top right",
            showlegend=False,
            marker=dict(color="red", size=12)
        ))

    layout = {
        'title': 'Zmiany cen złota',
        'xaxis': {'title': 'Data', 'gridcolor': '#4a5a8d', 'tickfont': {'color': 'white'}},
        'yaxis': {'title': 'Cena (PLN)','gridcolor': '#4a5a8d', 'tickfont': {'color': 'white'}},
        'plot_bgcolor': '#1f2c56',
        'paper_bgcolor': '#1f2c56',
        'font': {'color': 'white'}
    }

    return {'data': traces, 'layout': layout}

if __name__ == '__main__':
    app.run_server(debug=True)
