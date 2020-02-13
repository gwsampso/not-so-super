import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from components import Column, Header, Row
from app import app
from layouts import main

layout = html.Div(children=[
    dcc.Location(id='url-aist', refresh=False),
    html.Div(id='main-header', children=[Header('', app, bg_color="#fff", font_color="#F3F6FA", logo="aist.svg", home_address="https://www.aist.asn.au/")]),
    html.Div(id='app-page-content', children=[html.Div(id='aist-page-content', className='app-body')])
    ])

@app.callback(Output('aist-page-content', 'children'),               
              [Input('url-aist', 'pathname')])
def display_page(pathname):
    if pathname == '/not-so-super/aist-not-so-super':
        return main.layout