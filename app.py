# Import packages
import requests
import json
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px

header = ''
data = []
info_text = ''

# Initialize the app
app = Dash(__name__)

# App layout
app.layout = html.Div([
    html.Div(children='My First App with Data, Graph, and Controls'),
    html.Hr(),
    html.Label("Enter stock symbol:"),
    dcc.Input(id='stock-symbol', type='text', value='MSFT'),
    html.Button('Submit', id='submit-val', n_clicks=0),
    html.Div(id='output-container-button'),
    html.Hr(),
    dcc.RadioItems(options=[], value='', id='controls-and-radio-item'),
    dash_table.DataTable(id='data-table', columns=[], data=[]),
    dcc.Graph(figure={}, id='controls-and-graph'),
    html.Hr(),
    html.Div([
        html.Label("SEC 10-K Information (1000 words max):", style={'font-size': '24px', 'font-weight': 'bold', 'color': 'blue'}),
        dcc.Markdown(id='info-div')  # Use dcc.Markdown to render Markdown
    ])
])

# Function to fetch data based on stock symbol
def fetch_data(stock_symbol):
    response = json.loads(requests.get(f'http://127.0.0.1:8001/infer/{stock_symbol}').text)
    df = pd.DataFrame(response['data'][0], columns=response['cols'][0])
    global info_text
    info_text = response.get('info', '')
    return df

# Add controls to build the interaction
@app.callback(
    Output(component_id='controls-and-radio-item', component_property='options'),
    Output(component_id='data-table', component_property='data'),
    Output(component_id='info-div', component_property='children'),
    Input(component_id='submit-val', component_property='n_clicks'),
    Input(component_id='stock-symbol', component_property='value')
)
def update_data(n_clicks, stock_symbol):
    df = fetch_data(stock_symbol)
    options = [{'label': col, 'value': col} for col in df.columns[1:]]
    global data, header
    data = df.to_dict('records')
    header = df.columns[0]
    return options, data, info_text


# Add controls to build the interaction
@callback(
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
    app.run(debug=True)

