import pandas as pd
from unidecode import unidecode
from dash import html, dcc, Dash, Input, Output
import plotly.express as px

response = pd.read_excel("D:/Programowanie/Python/Projects/codebrainers-plotly-dash/Wypadki_2004_2023_KGP.xlsx")
new_columns_names = [unidecode(col) for col in response.iloc[4, 1:5].values]
crash_stats = pd.DataFrame(response.iloc[6:26, 1:5].values, columns=new_columns_names)

px.defaults.template = "plotly_dark"

external_css = ["https://cdn.jsdelivr.net/npm/bootswatch@5.3.1/dist/darkly/bootstrap.min.css"]

app = Dash(__name__, external_stylesheets=external_css)

app.layout = html.Div(
    style={'fontFamily': 'Arial, sans-serif', 'backgroundColor': '#f4f4f9', 'padding': '20px'},
    children=[
        html.H1(
            children="Wypadki w Polsce w latach 2004-2023",
            style={'textAlign': 'center', 'color': '#3a3a3a', 'fontSize': '36px'}
        ),
        html.Div(id='output-container-range-slider'),
        dcc.RangeSlider(2004, 2023, 1, value=[2005, 2023], id='my-range-slider', marks={i: str(i) for i in range(2004, 2024)}),
        dcc.Checklist(
            id="checkbox-selection",
            options=[
                {'label': 'Wypadki drogowe', 'value': 'Wypadki drogowe'},
                {'label': 'Ofiary śmiertelne', 'value': 'Ofiary smiertelne'},
                {'label': 'Ranni', 'value': 'Ranni'}
            ],
            value=['Wypadki drogowe'],
            inline=True,
            style={
                'display': 'flex', 
                'justifyContent': 'center', 
                'gap': '15px', 
                'fontSize': '18px'
            }
        ),
        dcc.Graph(
            id='graph-container',
            style={
                'marginTop': '40px',
                'backgroundColor': '#ffffff',
                'borderRadius': '10px',
                'boxShadow': '0 4px 10px rgba(0, 0, 0, 0.1)'
            }
        )
    ]
)

@app.callback(
    [Output('graph-container', 'figure'),
    Output('output-container-range-slider', 'children')],
    [Input('checkbox-selection', 'value'), 
    Input('my-range-slider', 'value')]
)
def update_graph(selected_values, year_range):
    crash_stats["Rok"] = crash_stats["Rok"].astype(int)
    filtered_df = crash_stats[(crash_stats["Rok"] >= year_range[0]) & (crash_stats["Rok"] <= year_range[1])]
    if not selected_values:
        return {}, "Proszę wybrać co najmniej jedną kategorię !"
    if not year_range:
        return {}, "Proszę wybrać zakres lat !"
    fig = px.line(
        filtered_df,
        x="Rok",
        y=selected_values,
        title=f'{" i ".join(selected_values)} w Polsce w latach {year_range[0]}-{year_range[1]}',
        labels={'Rok': 'Rok'},
        line_shape='linear',
        color_discrete_map={
            "Wypadki drogowe": "#28a745",
            "Ofiary smiertelne": "#dc3545",
            "Ranni": "#007bff"
        }
    )

    fig.update_layout(
        template="plotly_dark",
        legend_title_text="Statystyki",
        title_x=0.5,
        title_font=dict(size=24, color='#3a3a3a'),
        xaxis_title='Rok',
        yaxis_title=', '.join(selected_values),
        font=dict(family='Arial, sans-serif', size=16, color='#3a3a3a'),
        plot_bgcolor='#f4f4f9',
        paper_bgcolor='#f4f4f9',
        xaxis=dict(showgrid=True, gridwidth=0.5, gridcolor='rgba(0,0,0,0.1)', tickformat="d", tickangle=45, tickmode="linear"),
        yaxis=dict(showgrid=True, gridwidth=0.5, gridcolor='rgba(0,0,0,0.1)', tickformat="d"),
        margin=dict(l=50, r=50, t=80, b=50)
    )

    return fig, f'Zakres lat: {year_range[0]} - {year_range[1]}'

if __name__ == '__main__':
    app.run_server(debug=True)
