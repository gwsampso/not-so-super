import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from components import Column, Header, Row

from app import app, server
from layouts import noheader, frontier, aist

app.layout = html.Div(children=[
    dcc.Location(id='url', refresh=False),
    html.Div(id='page')
    ])

@app.callback(Output('page', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/not-so-super/not-so-super':
        return frontier.layout
    elif pathname == '/not-so-super/aist-not-so-super':
        return aist.layout
    elif pathname == '/not-so-super/no-header':
        return noheader.layout
    else:
        return '404'

if __name__ == '__main__':
    app.run_server(debug=True)
