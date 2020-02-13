# -*- coding: utf-8 -*-
import pandas as pd
import os
import dash_table.FormatTemplate as FormatTemplate

DATAPATH = os.path.join(".", "data/")

CSVPATH = 'https://raw.githubusercontent.com/gwsampso/website_data/master/not_so_super/not_so_super.csv'

DATEPATH = 'https://raw.githubusercontent.com/gwsampso/website_data/master/not_so_super/data_date.csv'


def get_data_date():
    data_date = pd.read_csv(DATEPATH)
    return data_date['data_date'][0]


def calc_risk_label(risk_number):
    risk_label=''
    if risk_number < 0.5:
        risk_label='Very Low'
    if 0.5 <= risk_number < 1:
        risk_label='Low'
    if 1 <= risk_number < 2:
        risk_label='Low to Medium'
    if 2 <= risk_number < 3:
        risk_label='Medium'
    if 3 <= risk_number < 4:
        risk_label='Medium to High'
    if 4 <= risk_number < 6:
        risk_label='High'
    if  risk_number >= 6:
        risk_label='Very High'
    
    return risk_label


def get_df_data():
    df = pd.read_csv(CSVPATH)
    # df = pd.read_csv(DATAPATH + 'data.csv')
    df_superfund_type = df['superfund_type']   
    df['asset_class'].fillna('Empty', inplace=True)
    df.drop(['investment_id', 'fund_name', 'investment_id.1'], axis=1, inplace=True)

    percent_cols = ['return_1yr','return_3yr','return_5yr','targetreturn']
    money_cols = ['investment_size','fee', 'fund_assets', 'risk']

    for col_name in percent_cols:
        df[col_name] = pd.to_numeric(df[col_name], errors='coerce')/100

    for col_name in money_cols:
        df[col_name] = pd.to_numeric(df[col_name], errors='coerce')
    
    df['risk_label'] = df['risk'].apply(lambda x: calc_risk_label(x))

    df = df[['investment_name',
        'superfund_type',
        'asset_class',
        'fund_assets',
        'return_1yr',
        'return_3yr',
        'return_5yr',
        'investment_size',
        'targetreturn',
        'risk',
        'risk_label',
        'fee',
        'invfee',
        'admin_fee',
        'lifecycle_in',
        'public_offer'
        ]]
    return df

def get_columns():

    the_date = "Return % as at {}".format(get_data_date())
    
    size_cols = [{
            'id': 'investment_name',
            'name': 'Investment Name',
            'type': 'text'
        }, {
            'id': 'superfund_type',
            'name': 'Super Fund Type',
            'type': 'text'
        }, {
            'id': 'asset_class',
            'name': 'Asset Class',
            'type': 'text'
        }, {
            'id': 'fund_assets',
            'name': 'Fund Assets ($)',
            'type': 'numeric',
            'format': FormatTemplate.money(2)
        }, {
            'id': 'investment_size',
            'name': 'Investment Size ($)',
            'type': 'numeric',
            'format': FormatTemplate.money(2)
        }]

    performance_cols = [{
            'id': 'investment_name',
            'name': ['', 'Fund'],
            'type': 'text'
        }, {
            'id': 'return_5yr',
            'name': [the_date, '5 Year'],
            'type': 'numeric',
            'format': FormatTemplate.percentage(2)
        }, {
            'id': 'return_3yr',
            'name': [the_date, '3 Year'],
            'type': 'numeric',
            'format': FormatTemplate.percentage(2)
        }, {
            'id': 'return_1yr',
            'name': [the_date, '1 Year'],
            'type': 'numeric',
            'format': FormatTemplate.percentage(2)
        }, {
            'id': 'fee',
            'name': ['Fee', '$'],
            'type': 'numeric',
            'format': FormatTemplate.money(0)
        }]

    # performance_cols = [{
    #         'id': 'investment_name',
    #         'name': 'Investment Name',
    #         'type': 'text'
    #     }, {
    #         'id': 'superfund_type',
    #         'name': 'Super Fund Type',
    #         'type': 'text'
    #     }, {
    #         'id': 'asset_class',
    #         'name': 'Asset Class',
    #         'type': 'text'
    #     }, {
    #         'id': 'fee',
    #         'name': 'Fee ($)',
    #         'type': 'numeric',
    #         'format': FormatTemplate.money(0)
    #     }, {
    #         'id': 'risk_label',
    #         'name': 'Risk',
    #         'type': 'text'
        
    #     }, {
    #         'id': 'targetreturn',
    #         'name': 'Target Return (%)',
    #         'type': 'numeric',
    #         'format': FormatTemplate.percentage(2)
        
    #     }, {
    #         'id': 'return_1yr',
    #         'name': '1 Year Return (%)',
    #         'type': 'numeric',
    #         'format': FormatTemplate.percentage(2)
    #     }, {
    #         'id': 'return_3yr',
    #         'name': '3 Year Return (%)',
    #         'type': 'numeric',
    #         'format': FormatTemplate.percentage(2)
    #     }, {
    #         'id': 'return_5yr',
    #         'name': '5 Year Return (%)',
    #         'type': 'numeric',
    #         'format': FormatTemplate.percentage(2)
    #     }, {
    #         'id': 'invfee',
    #         'name': 'Investment Fee (%)',
    #         'type': 'numeric',
    #         'format': FormatTemplate.percentage(4)
    #     }, {
    #         'id': 'admin_fee',
    #         'name': 'Admin Fee (%)',
    #         'type': 'numeric',
    #         'format': FormatTemplate.percentage(4)
    #     }]
    
    details_cols = [{
            'id': 'investment_name',
            'name': 'Fund',
            'type': 'text'
        }, {
            'id': 'superfund_type',
            'name': 'Fund Type',
            'type': 'text'
        }, {
            'id': 'asset_class',
            'name': 'Asset Class',
            'type': 'text'
        }, {
            'id': 'fund_assets',
            'name': 'Fund Assets',
            'type': 'numeric',
            'format': FormatTemplate.money(2)
        }]
    
    objective_cols = [{
            'id': 'investment_name',
            'name': 'Fund',
            'type': 'text'
        }, {
            'id': 'targetreturn',
            'name': 'Target Return',
            'type': 'numeric',
            'format': FormatTemplate.percentage(2)
        
        }, {
            'id': 'risk_label',
            'name': 'Risk',
            'type': 'text'
        
        }]

    return performance_cols, size_cols, details_cols, objective_cols

def get_axis_dropwdown():
    return [{'label': 'Return 1yr', 'value': 'return_1yr'}, 
            {'label': 'Return 3yr', 'value': 'return_3yr'}, 
            {'label': 'Return 5yr', 'value': 'return_5yr'}, 
            {'label': 'Target Return', 'value': 'targetreturn'}, 
            {'label': 'Risk', 'value': 'risk'}, 
            {'label': 'Investment Size', 'value': 'investment_size'}, 
            {'label': 'Fee', 'value': 'fee'}, 
            {'label': 'Inv Fee', 'value': 'invfee'}, 
            {'label': 'Admin Fee', 'value': 'admin_fee'}, 
            {'label': 'Fund Assets', 'value': 'fund_assets'}]

def get_color_dropdown():
    return [{'label': 'Fund Type', 'value': 'superfund_type'}, 
            {'label': 'Asset Class', 'value': 'asset_class'}, 
            {'label': 'Risk', 'value': 'risk_label'}]
