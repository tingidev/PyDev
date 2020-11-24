import base64
import datetime
import io

import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table

import pandas as pd
import numpy as np
import plotly.express as px

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),
    dcc.Store(id='memory'),
    html.Div(id='table-data-upload'),
])

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
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return df.to_json(orient='split')

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

# Table callback
@app.callback(Output('table-data-upload', 'children'),
                Input('memory', 'data'),
                State('upload-data', 'filename'),
                State('upload-data', 'last_modified'))
def update_table(data, filename, date):
    table = html.Div()
    if data:
        data = data[0]
        df = pd.read_json(data, orient='split')
        dfinfo = pd.DataFrame(index=df.columns)
        dfinfo['Variable'] = df.columns
        dfinfo['Dtype'] = [str(df[x].dtype) for x in df.columns]
        dfinfo['Non-Null Count'] = df.count()
        dfinfo['Mean'] = [round(df[x].mean(),2) if (df[x].dtype == 'float64' or df[x].dtype == 'int64') else np.nan for x in df.columns]
        dfinfo['Min'] = [round(df[x].min(),2) if (df[x].dtype == 'float64' or df[x].dtype == 'int64') else np.nan for x in df.columns]
        dfinfo['25%'] = [round(df[x].quantile(0.25),2) if (df[x].dtype == 'float64' or df[x].dtype == 'int64') else np.nan for x in df.columns]
        dfinfo['50%'] = [round(df[x].quantile(0.50),2) if (df[x].dtype == 'float64' or df[x].dtype == 'int64') else np.nan for x in df.columns]
        dfinfo['75%'] = [round(df[x].quantile(0.75),2) if (df[x].dtype == 'float64' or df[x].dtype == 'int64') else np.nan for x in df.columns]
        dfinfo['Max'] = [round(df[x].max(),2) if (df[x].dtype == 'float64' or df[x].dtype == 'int64') else np.nan for x in df.columns]
        table = html.Div([
            html.Div([
                html.H6("Filename: "+filename[0]),
                html.H6("Last modified: "+str(datetime.datetime.fromtimestamp(date[0]))),
                dash_table.DataTable(
                    data=df.to_dict('records'),
                    columns=[{'name': i, 'id': i} for i in df.columns],
                    page_size=10
                ),
                html.Hr(),  # horizontal line
            ]),
            html.Div([
                dash_table.DataTable(
                    data=dfinfo.to_dict('records'),
                    columns=[{'name': i, 'id': i} for i in dfinfo.columns],
                ),
            ]),
        ])
    return table


#
# @app.callback(Output('memory','data'),
#               Input('upload-data', 'contents'),
#               State('upload-data', 'filename'))
# def store_output(contents, filename):
#     content_type, content_string = contents.split(',')
#     decoded = base64.b64decode(content_string)
#     try:
#         if 'csv' in filename:
#             # Assume that the user uploaded a CSV file
#             data = pd.read_csv(
#                 io.StringIO(decoded.decode('utf-8')))
#         elif 'xls' in filename:
#             # Assume that the user uploaded an excel file
#             data = pd.read_excel(io.BytesIO(decoded))
#     except Exception as e:
#         print(e)
#         return html.Div([
#             'There was an error processing this file.'
#         ])
#
#     return data



# def store_output(list_of_contents, list_of_names, list_of_dates):
#     if list_of_contents is not None:
#         children = [
#             parse_contents(c, n, d) for c, n, d in
#             zip(list_of_contents, list_of_names, list_of_dates)]
#         return children



# def parse_contents(contents, filename):
#     content_type, content_string = contents.split(',')
#     decoded = base64.b64decode(content_string)
#     try:
#         if 'csv' in filename:
#             # Assume that the user uploaded a CSV file
#             df = pd.read_csv(
#                 io.StringIO(decoded.decode('utf-8')))
#         elif 'xls' in filename:
#             # Assume that the user uploaded an excel file
#             df = pd.read_excel(io.BytesIO(decoded))
#     except Exception as e:
#         print(e)
#         return html.Div([
#             'There was an error processing this file.'
#         ])
#
#     return df


# def parse_contents(contents, filename):
#     content_type, content_string = contents.split(',')
#     decoded = base64.b64decode(content_string)
#     try:
#         if 'csv' in filename:
#             # Assume that the user uploaded a CSV file
#             df = pd.read_csv(
#                 io.StringIO(decoded.decode('utf-8')))
#         elif 'xls' in filename:
#             # Assume that the user uploaded an excel file
#             df = pd.read_excel(io.BytesIO(decoded))
#     except Exception as e:
#         print(e)
#         return html.Div([
#             'There was an error processing this file.'
#         ])
#
#     return df

# Table callback
# @app.callback(Output('table-data-upload', 'children'),
#             [
#                 Input('upload-data', 'contents'),
#                 State('upload-data', 'filename')
#                 # State('upload-data', 'last_modified')
#             ])
# def update_table(contents, filename):
#     table = html.Div()
#     if contents:
#         contents = contents[0]
#         filename = filename[0]
#         df = parse_contents(contents, filename)
#
#         table = html.Div([
#             html.H5(filename),
#             # html.H6(datetime.datetime.fromtimestamp(date)),
#             dash_table.DataTable(
#                 data=df.to_dict('records'),
#                 columns=[{'name': i, 'id': i} for i in df.columns],
#                 page_size=10
#             ),
#
#         html.Hr(),  # horizontal line
#
#         # For debugging, display the raw contents provided by the web browser
#         html.Div('Raw Content'),
#         html.Pre(contents[0:200] + '...', style={
#             'whiteSpace': 'pre-wrap',
#             'wordBreak': 'break-all'
#         })
#
#         ])
#     return table
#
# # Graph callback
# @app.callback(Output('graph-data-upload', 'children'),
#             [
#                 Input('upload-data', 'contents'),
#                 State('upload-data', 'filename')
#                 # State('upload-data', 'last_modified')
#             ])
# def update_table(contents, filename):
#     graph = html.Div()
#     if contents:
#         contents = contents[0]
#         filename = filename[0]
#         df = parse_contents(contents, filename)
#         cols = df.columns
#         fig = px.scatter(df, x=cols[0], y=cols[1])
#         graph = html.Div([
#             dcc.Graph(figure=fig)
#         ])
#     return graph






if __name__ == '__main__':
    app.run_server(debug=True)
