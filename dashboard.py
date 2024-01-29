import plotly.express as px
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import pandas as pd

global data_to_display
data_to_display = None

def load_sample_data():
    global data_to_display
    df = pd.read_csv('./output/clean_data_to_visualise.csv')
    data_to_display = df.sample(int(df.shape[0]*.8)).copy()

load_sample_data()

# Inicjalizacja aplikacji Dash
app = dash.Dash(__name__)

# Layout aplikacji
app.layout = html.Div([
    # Dropdown do wyboru zmiennej dla analizy
    dcc.Dropdown(
        id='variable-dropdown',
        options=[{'label': i, 'value': i} for i in data_to_display.columns],
        value='carat'
    ),

    # Wykres do wyświetlenia danych
    dcc.Graph(
        id='scatter-plot'
    ),

    # Tabela z danymi
    html.Div(
        id='table-div'
    )
])

# Callback do aktualizacji wykresu
@app.callback(
    Output('scatter-plot', 'figure'),
    [Input('variable-dropdown', 'value')]
)
def update_graph(selected_variable):
    global data_to_display
    fig = px.scatter(data_to_display, x=selected_variable, y='price', title=f'Cena w zależności od {selected_variable}')
    return fig

# Callback do aktualizacji tabeli
@app.callback(
    Output('table-div', 'children'),
    [Input('variable-dropdown', 'value')]
)
def update_table(selected_variable):
    global data_to_display
    table = html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in data_to_display.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(data_to_display.iloc[i][col]) for col in data_to_display.columns
            ]) for i in range(min(len(data_to_display), 10))
        ])
    ])
    return table

if __name__ == '__main__':
    app.run_server(debug=True)
