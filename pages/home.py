import dash
from dash import html
from dash import dcc
from dash.dependencies import Input , Output
from pages import navigation


home_layout = html.Div(children=[
    navigation.navbar,
    html.H1(children="Welcome to FinSight - Your Ultimate Stock Forecasting and News Dashboard"),
    html.Hr(),
    html.H2("Explore FinSight's Features:"),
    html.Ul([
        html.Li("Visualize Historical Stock Data"),
        html.Li("Forecast Future Stock Prices"),
        html.Li("Stay Updated with Latest News"),
        html.Li("Learn About Companies"),
    ]),
    html.P("Whether you're a seasoned investor or just getting started in the world of finance, FinSight has everything you need to stay informed and make confident investment decisions.")
])
