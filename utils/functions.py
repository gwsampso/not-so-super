# -*- coding: utf-8 -*-
# Helper function library
import constants
import plotly.graph_objs as go
from data.data import get_data_date

def dropdown_option_builder(data_frame_list=None, with_all=False, is_data_frame=True):

    list_unique = data_frame_list

    if is_data_frame:
        list_unique = data_frame_list.unique()

    if with_all:
        return [{'label': 'All', 'value': 'All'}] + sorted([{'label': i, 'value': i}for i in list_unique], key=lambda k: k['label'])
    
    return sorted([{'label': i, 'value': i}for i in list_unique], key=lambda k: k['label'])

def return_table(data, hidden, fund_types, asset_class, investment_name, fund_access, strategy, convert_to_dict=True):
    if hidden == 'On':
        if fund_types !='All':
            data = data[data['superfund_type']==fund_types]
        if asset_class !='All':
            data = data[data['asset_class']==asset_class]
        if investment_name is not None: 
            if len(investment_name) is not 0:
                data = data[data['investment_name'].isin(investment_name)]
        if fund_access is not None:
            data = data[data['lifecycle_in'].isin(fund_access)]
        if strategy is not None:
            data = data[data['public_offer'].isin(strategy)]
        if convert_to_dict:
            data = data.to_dict("rows")

    return data
    
def graph_peer_universe(data, hidden, fund_types, asset_class, investment_name, fund_access, strategy, x_axis, y_axis, color):
    filtered_df = return_table(data, hidden, fund_types, asset_class, investment_name, fund_access, strategy, convert_to_dict=False)

    # dynamic axis formatting 

    grid_lables = {'return_1yr' : 'Return 1 Year', 
            'return_3yr' : 'Return 3 Year' , 
            'return_5yr' : 'Return 5 Year', 
            'targetreturn' : 'Target Return', 
            'risk' : 'Risk', 
            'investment_size' : 'Investment Size', 
            'fee' :'Fee', 
            'invfee' : 'Inv Fee', 
            'admin_fee' : 'Admin Fee', 
            'fund_assets' : 'Fund Assets'}

    percent_array = ['return_1yr','return_3yr','return_5yr','targetreturn', 'invfee', 'admin_fee']
    money_cols = ['investment_size','fee', 'fund_assets']

    if x_axis in percent_array:
        tickformat_x = constants.SYM_PERCENT_DEC_1
        hoverformat_x = constants.SYM_PERCENT_DEC
    else:
        tickformat_x = ''
        hoverformat_x = constants.SYM_DEC_FM
    if y_axis in percent_array:
        tickformat_y = constants.SYM_PERCENT_DEC_1
        hoverformat_y = constants.SYM_PERCENT_DEC
    else:
        tickformat_y = ''
        hoverformat_y = constants.SYM_DEC_FM


    x_axis_title = grid_lables[x_axis]
    y_axis_title = grid_lables[y_axis]

    the_date = "as at {}".format(get_data_date())

    traces = []
    for i in filtered_df[color].unique():
        df_by_continent = filtered_df[filtered_df[color] == i]
        traces.append(go.Scatter(
            x=df_by_continent[x_axis],
            y=df_by_continent[y_axis],
            text=df_by_continent['investment_name'],
            mode='markers',
            opacity=0.7,
            marker={
                'size': 15,
                'line': {'width': 0.5, 'color': 'white'}
            },
            name=i
        ))

    return {
        'data': traces,
        'layout': go.Layout(
            title='Superannuation Statistics ' + the_date,
            xaxis={'title': x_axis_title, 'tickformat': tickformat_x, 'linecolor': '#555555', 'linewidth': 0.5, 'gridcolor':"#555555", 'zerolinecolor':"#555555"},
            yaxis={'title': y_axis_title, 'tickformat': tickformat_y, 'linecolor': '#555555', 'linewidth': 0.5, 'gridcolor':"#555555", 'zerolinecolor':"#555555"},
            plot_bgcolor='#eee',
            paper_bgcolor='#eee',
            margin={'l': 60, 'b': 20, 't': 60, 'r': 10},
            legend={'x': 0, 'y': -0.2, 'orientation': 'h'},
            hovermode='closest',
            height= 500
        )
    }
