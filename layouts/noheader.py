import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from app import app
from layouts import main

layout = html.Div(children=[
    dcc.Location(id='url-no-header', refresh=False),
    html.Div(id='app-page-content', style={'top': '0px'}, children=[html.Div(id='no-header-page-content', className='app-body')])
    ])

@app.callback(Output('no-header-page-content', 'children'),               
              [Input('url-no-header', 'pathname')])
def display_page(pathname):
    if pathname == '/not-so-super/no-header':
        return main.layout