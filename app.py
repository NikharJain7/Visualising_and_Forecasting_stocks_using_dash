import dash
import dash_bootstrap_components as dbc

custom_css_url = "/assets/styles.css"


app = dash.Dash(__name__,external_stylesheets=[dbc.themes.SPACELAB ,  custom_css_url])
server = app.server