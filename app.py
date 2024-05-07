#!/usr/bin/python3

"""
Dash App to visualize SEC 10-k
Data and Info from the Backend Flask Server
"""

import requests
from dash import Dash, html, dash_table, dcc, Output, Input, State
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from datetime import datetime as dt

header = ''
data = []
info_text = ''
prev_clicks = 0

# Initialize the app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], title="SEC-10K Filing Viewer")

# App layout with loading indicator
app.layout = dbc.Container([
    html.Div(children='SEC-10K Filing Viewer', style={'font-size': '24px', 'font-weight': 'bold', 'margin-bottom': '10px', 'text-align': 'center'}),
    html.Hr(),
    html.Div([
        html.Label("Enter stock symbol:"),
        dcc.Input(id='stock-symbol', type='text', value='MSFT', style={'margin-right': '10px', 'width': '200px'}),
        html.Label("Start Date:"),
        dcc.DatePickerSingle(
            id='start-date',
            min_date_allowed=dt(1990, 1, 1),
            max_date_allowed=dt.today(),
            initial_visible_month=dt.today(),
            date=str(dt.today()),
            display_format='YYYY-MM-DD',
            style={'margin-right': '10px', 'margin-left': '5px'}
        ),
        html.Label("End Date:"),
        dcc.DatePickerSingle(
            id='end-date',
            min_date_allowed=dt(1990, 1, 1),
            max_date_allowed=dt.today(),
            initial_visible_month=dt.today(),
            date=str(dt.today()),
            display_format='YYYY-MM-DD',
            style={'margin-right': '10px'}
        ),
        dbc.Button("Submit", id='submit-val', n_clicks=0, color="primary", className="mr-1", type='button', style={'font-size': '18px', 'border-radius': '1px'}),
        html.Div(id='output-container-button'),
    ]),
    html.Hr(),
    dcc.Dropdown(
        id='graph-type',
        options=[
            {'label': 'Histogram', 'value': 'histogram'},
            {'label': 'Scatter Plot', 'value': 'scatter'},
            {'label': 'Line Plot', 'value': 'line'},
            {'label': 'Pie Chart', 'value': 'pie'}
        ],
        value='histogram',
        style={'margin-bottom': '20px', 'width': '200px'}
    ),
    dcc.Dropdown(id='y-axis-column', style={'width': '200px'}),
    dbc.Spinner(color="primary", children=[
        dash_table.DataTable(id='data-table', columns=[], data=[]),
        dcc.Graph(figure={}, id='controls-and-graph'),
    ]),
    html.Hr(),
    html.Div([
        html.Label("SEC 10-K Information (1000 words max):", style={'font-size': '24px', 'font-weight': 'bold', 'color': 'blue'}),
        dcc.Loading(
            id="info-div-loading",
            type="default",
            children=dcc.Markdown(id='info-div')
        )
    ])
])


@app.callback(
    [Output('y-axis-column', 'options'),
     Output('data-table', 'data'),
     Output('info-div', 'children')],
    [Input('submit-val', 'n_clicks')],
    [State('stock-symbol', 'value'),
     State('start-date', 'date'),
     State('end-date', 'date')]
)
def update_data(n_clicks, stock_symbol, start_date, end_date):
    if not n_clicks:
        return [], [], ''
    
    # Fetch data
    start_date = start_date[:10]
    end_date = end_date[:10]
    print(f"Received request for {stock_symbol} from {start_date} to {end_date}")
    response = requests.get(f'http://127.0.0.1:8001/infer/{stock_symbol}/{start_date}/{end_date}')
    
    if response.status_code != 200:
        return [], [], "Error fetching data"
    
    response_data = response.json()
    
    if not response_data['data']:
        return [], [], response_data['info']
        
    df = pd.DataFrame(response_data['data'][0], columns=response_data['cols'][0])
    options = [{'label': col, 'value': col} for col in df.columns[1:]]
    global data, header
    data = df.to_dict('records')
    header = df.columns[0]

    return options, data, response_data['info']


# Add controls to build the interaction
@app.callback(
    Output(component_id='controls-and-graph', component_property='figure'),
    [Input('graph-type', 'value'),
     Input('y-axis-column', 'value')]
)
def update_graph(graph_type, y_axis_column):
    if not data or not y_axis_column:
        # Return empty figure if data or y_axis_column is empty
        return {}
    
    if graph_type == 'histogram':
        fig = px.histogram(data, x=header, y=y_axis_column, histfunc='avg')
    elif graph_type == 'scatter':
        fig = px.scatter(data, x=header, y=y_axis_column)
    elif graph_type == 'line':
        fig = px.line(data, x=header, y=y_axis_column)
    elif graph_type == 'pie':
        fig = px.pie(data, values=y_axis_column, names=header)
    else:
        fig = {}
    
    return fig


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

