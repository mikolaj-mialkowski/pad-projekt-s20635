import plotly.express as px
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import pandas as pd

global data_to_display


def load_sample_data():
    global data_to_display
    df = pd.read_csv('./output/clean_data.csv')
    data_to_display = df.sample(int(df.shape[0] * .8)).copy()


load_sample_data()

images = {
    'histogram': 'assets/histograms.png',
    'box': 'assets/boxplots.png',
    'heatmap': 'assets/heatmap.png',
    'scatter': 'assets/scatterplots.png',
    'pairplot': 'assets/pairplots.png'
}

app = dash.Dash(__name__)
app.layout = html.Div([
    html.H1("Price analysis", style={'text-align': 'center'}),
    html.Label("Chose variable (feature) to display:"),
    dcc.Dropdown(
        id='variable-dropdown',
        options=[{'label': i, 'value': i} for i in data_to_display.columns],
        value='carat'
    ),
    html.Br(),
    html.Label("Choose chart type:"),
    dcc.RadioItems(
        id='chart-type',
        options=[
            {'label': 'Scatter chart', 'value': 'scatter'},
            {'label': 'Bar chart', 'value': 'bar'}
        ],
        value='scatter',
        style={'width': '50%'}
    ),
    dcc.Graph(
        id='dynamic-graph'
    ),
    html.Br(),
    html.Div(
        id='table-div',
        style={'width': '50%'}
    ),
    html.Br(),
    dcc.Dropdown(
        id='image-dropdown',
        options=[{'label': k, 'value': v} for k, v in images.items()],
        value='/assets/heatmap.png'
    ),
    html.Br(),
    html.Div(id='image-container')
], style={'text-align': 'center', 'fontSize': 18, 'padding': '20px'})


@app.callback(
    Output('image-container', 'children'),
    [Input('image-dropdown', 'value')]
)
def update_image(selected_image):
    return html.Img(src=selected_image, style={'width': '50%', 'height': 'auto'})


@app.callback(
    Output('dynamic-graph', 'figure'),
    [Input('variable-dropdown', 'value'),
     Input('chart-type', 'value')]
)
def update_graph(selected_variable, chart_type):
    global data_to_display
    if chart_type == 'scatter':
        fig = px.scatter(data_to_display, x=selected_variable, y='price',
                         title=f'Price depending on {selected_variable}')
    else:
        fig = px.bar(data_to_display, x=selected_variable, y='price', title=f'Price depending on {selected_variable}')
    return fig


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
            ]) for i in range(min(len(data_to_display), data_to_display.shape[0]))
        ])
    ])
    return table


if __name__ == '__main__':
    app.run_server(debug=False)
