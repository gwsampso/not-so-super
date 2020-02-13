# -*- coding: utf-8 -*-
import dash
import dash_html_components as html
import dash_table

from dash.dependencies import Input, Output
import dash_core_components as dcc

from components import Column, Header, Row
from utils.functions import dropdown_option_builder, return_table, graph_peer_universe
from data.data import get_columns, get_df_data, get_color_dropdown, get_axis_dropwdown

import plotly.graph_objs as go

import constants

from app import app

# df=get_df_data()
performance_cols, size_cols, details_cols, objective_cols = get_columns()


table_style_data_conditional=[
    {
        'if': {'row_index': 'odd'},
        'backgroundColor': 'rgb(248, 248, 248)'
    }]

table_style_header = {
        'backgroundColor': '#e96f28',
        'fontWeight': 'bold',
        'color': 'white',
        'textAlign': 'center'
    }

table_style_table = {'overflowX': 'scroll'}
table_style_table = {'overflowX': 'scroll'} 
table_style_cell = {'minWidth': '25px', 'maxWidth': '180px','whiteSpace': 'normal', 'font-family': 'Open Sans', 'font-size': '90%'}
table_css = [{
    'selector': '.dash-cell div.dash-cell-value',
    'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'
}]

table_style_cell_conditional=[
    {
        'if': {'column_id': c},
        'textAlign': 'left'
    } for c in ['investment_name', 'superfund_type', 'asset_class']
    ],  


layout = html.Div(children=[
    dcc.RadioItems(
                        id="hidden-data-radio",
                        options=[
                            {'label': 'On', 'value': 'On'}
                        ],
                        value='On',
                        style={'display': 'none'}
    ),
        Column(children=[html.Div(id='manhattan-control-tabs-1', className='control-tabs', children=[
            dcc.Tabs(id='', value='what-is', parent_className='custom-tabs', className='custom-tabs-container',
            children=[
                dcc.Tab(
                    label='About',
                    value='what-is',
                    className='custom-tab',
                    selected_className='custom-tab--selected',
                    children=html.Div(className='control-tab', children=[
                        html.H2(className='what-is', style={'text-align': 'center'}, children='Which funds are not so super?'),
                        html.P( 'The challenge to compare fund performance is most acute for choice super products.'
                                ' Astoundingly, super funds aren’t required to provide simple, comparable information on the fees '
                                'and returns of choice products'),
                        html.P('This tool should be used by anyone who wants to check on their fund, '
                                'with the appropriate focus on long-term performance.'
                                'You can compare performance at the click of a mouse button.'),
                        html.P('You can adjust the products in the "Filters" tab, '
                               'and the ordering/ranking on the tables'),
                        html.P('So which funds really are super?'),
                        html.Br(),
                        html.P('The data in these tabs is drawn from the latest published information provided by'
                                'super funds to the Australian Prudential Regulation Authority (APRA).'),
                        dcc.Link('See APRAs Quarterly MySuper Statistics', href='https://www.apra.gov.au/publications/quarterly-superannuation-statistics')
                    ])
                ),
                dcc.Tab(
                    label='Filters',
                    value='graph',
                    className='custom-tab',
                    selected_className='custom-tab--selected',
                    children=html.Div(className='control-tab', children=[
                        html.Div(className='app-controls-block', children=[
                            html.Div(
                                className='app-controls-name',
                                children=[
                                    'Fund Types'
                                ]
                            ),
                            dcc.Dropdown(
                                        id='fund-types-dropdown',
                                        value='All',
                                        multi=False,
                                        clearable=False,
                                    ),
                        ]),
                        html.Div(
                            className='app-controls-block', children=[
                                html.Div(
                                    className='app-controls-name',
                                    children=[
                                        'Asset Classes',
                                    ]
                                ),
                                    dcc.Dropdown(
                                        id='asset-class-dropdown',
                                        value='All',
                                        multi=False,
                                        clearable=False,
                                    ),
                            ]
                        ),
                        html.Div(
                            className='app-controls-block', children=[
                                html.Div(
                                    className='app-controls-name',
                                    children=[
                                        'Fund Access',
                                    ]
                                ),
                                dcc.Checklist(
                                    id='fund-access-checklist',
                                    options=[
                                        {'label': 'Public', 'value': '1'},
                                        {'label': 'Private', 'value': '0'},
                                    ],
                                    value=['1', '0'],
                                    labelStyle={'display': 'inline-block'}
                                )  
                            ]
                        ),
                        html.Div(
                            className='app-controls-block', children=[
                                html.Div(
                                    className='app-controls-name',
                                    children=[
                                        'Strategy',
                                    ]
                                ),
                                dcc.Checklist(
                                    id='strategy-checklist',
                                    options=[
                                        {'label': 'Life Cycle', 'value': '1'},
                                        {'label': 'Single Diversified', 'value': '0'},
                                    ],
                                    value=['1', '0'],
                                    labelStyle={'display': 'inline-block'}
                                )  
                            ]
                        ),
                        
                        html.Div(
                            className='app-controls-block', children=[
                                html.Div(
                                    className='app-controls-name',
                                    children=[
                                        'Name Search',
                                    ]
                                ),
                                    dcc.Dropdown(
                                        id='name-search',                                        
                                        multi=True,                                     
                                        placeholder="Search Investment Name"
                                    ),
                            ]
                        ),
                    ])
                )
            ])
        ]),], width=3),
        
        Column(children=[html.Div(id='manhattan-control-tabs-2', className='control-tabs', children=[
            dcc.Tabs(id='manhattan-tabs-2', value='performance', parent_className='custom-tabs', className='custom-tabs-container',
            children=[
                dcc.Tab(
                    label='Performance',
                    value='performance',
                    className='custom-tab',
                    selected_className='custom-tab--selected',
                    children=html.Div(className='control-tab', children=[                        
                        dcc.Loading(className='dashbio-loading', children=html.Div(
                            children=
                                dash_table.DataTable(
                                    id="data-table",
                                    merge_duplicate_headers=True,
                                        sort_action="native",
                                        sort_mode="single",
                                        style_cell_conditional=[
                                        {
                                            'if': {'column_id': c},
                                            'textAlign': 'left'
                                        } for c in ['investment_name', 'superfund_type', 'asset_class', 'risk_label']
                                        ],                                        
                                        style_data_conditional=table_style_data_conditional,
                                        style_header=table_style_header,
                                        style_table=table_style_table,
                                        style_cell=table_style_cell,
                                        css=table_css,
                                )
                                )
                        ),
                    ])
                ),
                dcc.Tab(
                    label='Sizes',
                    value='size',
                    className='custom-tab',
                    selected_className='custom-tab--selected',
                    children=html.Div(className='control-tab', children=[                        
                        dcc.Loading(className='dashbio-loading', children=html.Div(
                            children=
                                dash_table.DataTable(
                                    id="data-table-sizes",
                                        sort_action="native",
                                        sort_mode="single",
                                        style_cell_conditional=[
                                            {
                                                'if': {'column_id': c},
                                                'textAlign': 'left'
                                            } for c in ['investment_name', 'superfund_type', 'asset_class', 'risk_label']
                                        ],
                                        style_data_conditional=table_style_data_conditional,
                                        style_header=table_style_header,
                                        style_table=table_style_table,
                                        style_cell=table_style_cell,
                                        css=table_css,
                                )
                                )
                        ),
                    ])
                ),
                dcc.Tab(
                    label='Objectives',
                    value='Objectives',
                    className='custom-tab',
                    selected_className='custom-tab--selected',
                    children=html.Div(className='control-tab', children=[                        
                        dcc.Loading(className='dashbio-loading', children=html.Div(
                            children=
                                dash_table.DataTable(
                                    id="data-table-objectives",
                                        sort_action="native",
                                        sort_mode="single",
                                        style_cell_conditional=[
                                            {
                                                'if': {'column_id': c},
                                                'textAlign': 'left'
                                            } for c in ['investment_name', 'superfund_type', 'asset_class', 'risk_label']
                                        ],
                                        style_data_conditional=table_style_data_conditional,
                                        style_header=table_style_header,
                                        style_table=table_style_table,
                                        style_cell=table_style_cell,
                                        css=table_css,
                                )
                                )
                        ),
                    ])
                ),
                dcc.Tab(
                    label='Scatter',
                    value='scatter',
                    className='custom-tab',
                    selected_className='custom-tab--selected',
                    children=html.Div(className='control-tab', children=[
                        Row(style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}, children=[
                            Column(children=[
                                    html.Strong("X Axis",),
                                    dcc.Dropdown(
                                        id='x-axis-dropdown',
                                        value='return_1yr',
                                        multi=False,
                                        options=get_axis_dropwdown()
                                    ),]
                                    , width=3),
                            Column(children=[
                                    html.Strong("Y Axis"),
                                    dcc.Dropdown(
                                        id='y-axis-dropdown',
                                        value='fee',
                                        multi=False,
                                        options=get_axis_dropwdown()
                                    ),]
                                    , width=3),
                            Column(children=[
                                    html.Strong("Colour By"),
                                    dcc.Dropdown(
                                        id='color-dropdown',
                                        value='superfund_type',
                                        multi=False,
                                        options=get_color_dropdown()
                                    ),]
                                    , width=3)
                        ]),
                        html.Br(),
                        html.Br(),
                        dcc.Graph(
                        id="graph-peer-universe",
                        )
                    ])
                )
            ])
        ])], width=8)
])

@app.callback(Output('fund-types-dropdown', 'options'),
              [Input('hidden-data-radio', "value")])
def return_fund_types(hidden):
    # data=df
    data=get_df_data()
    options = dropdown_option_builder(data['superfund_type'], True)
    return options


@app.callback(Output('asset-class-dropdown', 'options'),
              [Input('hidden-data-radio', "value"),
              Input('fund-types-dropdown', 'value')])
def return_assets_class(hidden, fund_types):
    # data=df
    data=get_df_data()
    if fund_types !='All':
        data = data[data['superfund_type']==fund_types].copy()
    options = dropdown_option_builder(data['asset_class'], True)
    return options

@app.callback(Output('name-search', 'options'),
              [Input('hidden-data-radio', "value"),
              Input('fund-types-dropdown', 'value'),
              Input('asset-class-dropdown', 'value')])
def return_names(hidden, fund_types, asset_class):
    # data=df
    data=get_df_data()
    if fund_types !='All':
        data = data[data['superfund_type']==fund_types].copy()
    if asset_class !='All':
        data = data[data['asset_class']==asset_class].copy()
    options = dropdown_option_builder(data['investment_name'], False)
    return options


@app.callback([Output('data-table', 'data'),
              Output('data-table', 'columns')],
              [Input('hidden-data-radio', "value"),
              Input('fund-types-dropdown', 'value'),
              Input('asset-class-dropdown', 'value'),
              Input('name-search', 'value'),
              Input('fund-access-checklist', 'value'),
              Input('strategy-checklist', 'value'),
              ])
def return_performance_table(hidden, fund_types, asset_class, investment_name, fund_access, strategy):
    columns=performance_cols
    # data=df
    df=get_df_data()
    data=return_table(df, hidden, fund_types, asset_class, investment_name, fund_access, strategy)
    return data, columns

@app.callback([Output('data-table-sizes', 'data'),
              Output('data-table-sizes', 'columns')],
              [Input('hidden-data-radio', "value"),
              Input('fund-types-dropdown', 'value'),
              Input('asset-class-dropdown', 'value'),
              Input('name-search', 'value'),
              Input('fund-access-checklist', 'value'),
              Input('strategy-checklist', 'value'),
              ])
def return_size_table(hidden, fund_types, asset_class,  investment_name, fund_access, strategy):
    columns=details_cols
    df=get_df_data()
    data=return_table(df, hidden, fund_types, asset_class, investment_name, fund_access, strategy)
    return data, columns



@app.callback([Output('data-table-objectives', 'data'),
              Output('data-table-objectives', 'columns')],
              [Input('hidden-data-radio', "value"),
              Input('fund-types-dropdown', 'value'),
              Input('asset-class-dropdown', 'value'),
              Input('name-search', 'value'),
              Input('fund-access-checklist', 'value'),
              Input('strategy-checklist', 'value'),
              ])
def return_size_table(hidden, fund_types, asset_class,  investment_name, fund_access, strategy):
    columns=objective_cols
    df=get_df_data()
    data=return_table(df, hidden, fund_types, asset_class, investment_name, fund_access, strategy)
    return data, columns


@app.callback(
    Output('graph-peer-universe', 'figure'),
    [Input('hidden-data-radio', 'value'),
    Input('fund-types-dropdown', 'value'),
    Input('asset-class-dropdown', 'value'),
    Input('name-search', 'value'),
    Input('fund-access-checklist', 'value'),
    Input('strategy-checklist', 'value'),
    Input('x-axis-dropdown', 'value'),
    Input('y-axis-dropdown', 'value'),
    Input('color-dropdown', 'value'),])
def return_size_table(hidden, fund_types, asset_class,  investment_name, fund_access, strategy, x_axis, y_axis, color):
    df = get_df_data()
    return graph_peer_universe(df, hidden, fund_types, asset_class, investment_name, fund_access, strategy, x_axis, y_axis, color)

if __name__ == '__main__':
    app.run_server(debug=True)