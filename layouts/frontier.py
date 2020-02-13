import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from components import Column, Header, Row
from app import app
from layouts import main

layout = html.Div(children=[
    dcc.Location(id='url-frontier', refresh=False),
    html.Div(id='main-header', children=[Header('', app)]),
    html.Div(id='app-page-content', children=[html.Div(id='frontier-page-content', className='app-body')])
    ])

@app.callback(Output('frontier-page-content', 'children'),               
              [Input('url-frontier', 'pathname')])
def display_page(pathname):
    if pathname == '/not-so-super/not-so-super':
        return main.layout