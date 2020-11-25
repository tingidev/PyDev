# Based on: https://www.statworx.com/at/blog/how-to-build-a-dashboard-in-python-plotly-dash-step-by-step-tutorial/
# Padding: https://www.htmldog.com/guides/css/beginner/margins/

# System
import base64
import datetime
import io

# Dash
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table

# Packages
import pandas as pd
import numpy as np
import plotly.express as px

# Initialise app
app = dash.Dash(__name__)

# Define app
app.layout = html.Div(children=[
    html.Div(
        id='main-div',
        className='row',
        children=[
            html.Div(
                id='left-col-div',
                className='four columns div-user-controls',
                style={'borderStyle': 'dashed'},
                children=[
                    html.Div(
                        id='upload-div',
                        children=[
                            html.H2('PyDev - Data Explorer and Visualizer'),
                            html.P(
                                'Perform a first-pass exploration of your machine-learning data',
                                style={'margin-bottom': '60px'}
                            ),
                            dcc.Upload(
                                id='upload-data',
                                children=html.Div([
                                    'Drag and Drop or ',
                                    html.A('Select Files')
                                ]),
                                style={
                                    'borderWidth': '1px',
                                    'borderStyle': 'dashed',
                                    'borderRadius': '5px',
                                    'textAlign': 'center',
                                    'margin-right': '55px',
                                    'margin-bottom': '60px'
                                },
                                multiple=True
                            ),
                        ]
                    ),
                    html.Div(
                        id='meta-table-div',
                        children=[],
                        style={
                            'borderStyle': 'dashed',
                            'margin-right': '55px'
                        }
                    )
            ]),
            dcc.Store(id='memory'),
            html.Div(
                id='right-col-div',
                className='eight columns div-for-charts bg-grey',
                style={'margin-left': '0%', 'borderStyle': 'dashed'},
                children=[
                    html.Div(
                        id='table-data-upload',
                        style={
                            'margin': '55px',
                            'margin-top': '64px',
                            'borderStyle': 'dashed'
                        }
                    )
            ])
    ])
])

# Parse data file
def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
        elif 'json' in filename:
            # Assume that the user uploaded a JSON file
            df = pd.read_json(decoded.decode('utf-8'))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return df.to_json(orient='split')

# Callback to store file in Store element after upload
@app.callback(Output('memory', 'data'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children

# Callback to fill meta data table
@app.callback(Output('meta-table-div', 'children'),
                Input('memory', 'data'),
                State('upload-data', 'filename'),
                State('upload-data', 'last_modified'))
def update_meta_table(data, filename, date):
    table = html.Div()
    if data:
        data = data[0]
        df = pd.read_json(data, orient='split')
        table = html.Div(
            # className='row',
            children=[
                html.H2('File name: '+filename[0]),
                html.H2('Last modified: '+str(datetime.datetime.fromtimestamp(date[0]))[:19]),
        ])
    return table

# Callback to fill data table
@app.callback(Output('table-data-upload', 'children'),
                Input('memory', 'data'),
                State('upload-data', 'filename'),
                State('upload-data', 'last_modified'))
def update_table(data, filename, date):
    table = html.Div()
    if data:
        data = data[0]
        df = pd.read_json(data, orient='split')
        table = html.Div(
                    children=[
                        dash_table.DataTable(
                            data=df.to_dict('records'),
                            columns=[{'name': i, 'id': i} for i in df.columns],
                            style_as_list_view=True,
                            page_size=10,
                            style_header={
                                'backgroundColor': '#1E1E1E',
                                'fontWeight': 'bold'},
                            style_cell={
                                'backgroundColor': 'rgb(50, 50, 50)',
                                'color': 'white'}
                        ),
                        html.Hr() # horizontal line
                    ],
                    className='bg-grey',
        )
    return table

# Run app
if __name__ == '__main__':
    app.run_server(debug=True)
