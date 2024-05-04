import requests
import json
import dash
from dash import Dash, html, dash_table, dcc, callback, Output, Input, State
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc

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
        dbc.Button("Submit", id='submit-val', n_clicks=0, color="primary", className="mr-1", type='button', style={'font-size': '18px', 'border-radius': '1px'}),
        html.Div(id='output-container-button'),
    ]),
    html.Hr(),
    dcc.RadioItems(options=[], value='', id='controls-and-radio-item'),
    dbc.Spinner(color="primary", children=[
        dash_table.DataTable(id='data-table', columns=[], data=[]),
        dcc.Graph(figure={}, id='controls-and-graph'),
    ]),
    html.Hr(),
    html.Div([
        html.Label("SEC 10-K Information (1000 words max):", style={'font-size': '24px', 'font-weight': 'bold', 'color': 'blue'}),
        dcc.Markdown(id='info-div')
    ])
])


@app.callback(
    [Output('controls-and-radio-item', 'options'),
     Output('data-table', 'data'),
     Output('info-div', 'children')],
    [Input('submit-val', 'n_clicks')],
    [State('stock-symbol', 'value')]
)
def update_data(n_clicks, stock_symbol):
    if not n_clicks:
        return [], [], ''
    
    # Fetch data
    response = requests.get(f'http://127.0.0.1:8001/infer/{stock_symbol}')
    
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
    Input(component_id='controls-and-radio-item', component_property='value')
)
def update_graph(col_chosen):
    if not data:
        # Return empty figure if data is empty
        return {}
    fig = px.histogram(data, x=header, y=col_chosen, histfunc='avg')
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

