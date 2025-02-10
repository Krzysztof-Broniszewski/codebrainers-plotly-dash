import pandas as pd
from unidecode import unidecode
from dash import html, dcc, Dash, Input, Output
import plotly.express as px

response = pd.read_excel("D:/Programowanie/Python/Projects/codebrainers-plotly-dash/Wypadki_2004_2023_KGP.xlsx")
new_columns_names = [unidecode(col) for col in response.iloc[4, 1:5].values]
crash_stats = pd.DataFrame(response.iloc[6:26, 1:5].values, columns=new_columns_names)

app = Dash()

dropdown_options = [
    {'label': 'Wypadki drogowe', 'value': 'Wypadki drogowe'},
    {'label': 'Ofiary smiertelne', 'value': 'Ofiary smiertelne'},
    {'label': 'Ranni', 'value': 'Ranni'}
]

app.layout = html.Div(
    style={'fontFamily': 'Arial, sans-serif', 'backgroundColor': '#f4f4f9', 'padding': '20px'},
    children=[
        html.H1(
            children="Wypadki w Polsce w latach 2004-2023",
            style={'textAlign': 'center', 'color': '#3a3a3a', 'fontSize': '36px'}
        ),
        dcc.Dropdown(
            id="dropdown-selection",
            options=dropdown_options,
            value='Wypadki drogowe',
            style={
                "width": "50%",
                "margin": "auto",
                'fontSize': '18px',
                'color': '#3a3a3a',
                'backgroundColor': '#ffffff',
                'borderRadius': '8px',
                'padding': '10px'
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
    Output('graph-container', 'figure'),
    [Input('dropdown-selection', 'value')]
)
def update_graph(value):
    fig = px.line(
        crash_stats,
        x="Rok",
        y=value,
        title=f'{value} w Polsce w latach 2004-2023',
        labels={'Rok': 'Rok', value: value},
        line_shape='linear'
    )

    fig.update_layout(
        title=f'{value} w Polsce w latach 2004-2023',
        title_x=0.5,
        title_font=dict(size=24, color='#3a3a3a'),
        xaxis_title='Rok',
        yaxis_title=value,
        font=dict(family='Arial, sans-serif', size=16, color='#3a3a3a'),
        plot_bgcolor='#f4f4f9',
        paper_bgcolor='#f4f4f9',
        xaxis=dict(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.1)'),
        yaxis=dict(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.1)'),
        margin=dict(l=50, r=50, t=80, b=50)
    )

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
