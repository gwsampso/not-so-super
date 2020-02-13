import dash_html_components as html

def Header(app_title, app,  bg_color="#222222", font_color="#F3F6FA", logo="Frontier-Advisors-Logo.gif", home_address="https://frontieradvisors.com.au/" ):
    return html.Div(
                id='app-page-header',
                children=[
                    html.A(
                        id='dashbio-logo', children=[                            
                            html.Img(
                                src=app.get_asset_url(logo),
                            )],
                        href=home_address
                    ),
                    html.H2(
                        app_title
                    ),
                ],
                style={
                    'background': bg_color,
                    'color': font_color
                }
            )

