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
                    className='row',
                    children=[
                        html.Div(
                            className='four columns div-user-controls',
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
                                        # 'width': '100%',
                                        # 'height': '60px',
                                        # 'lineHeight': '60px',
                                        'borderWidth': '1px',
                                        'borderStyle': 'dashed',
                                        'borderRadius': '5px',
                                        'textAlign': 'center',
                                        'margin': '10px'
                                    },
                                )
                        ]),
                        html.Div(className='eight columns div-for-charts bg-grey')
                    ]
                )
])

# Run app
if __name__ == '__main__':
    app.run_server(debug=True)
