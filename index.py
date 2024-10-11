import dash
from dash import html
from dash import dcc
from dash.dependencies import Input , Output
from app import app
from pages import home , forecasting , about , visualize , news

url_content_layout=html.Div(children=[
    dcc.Location(id="url" , refresh = False),
    html.Div(id="output-div")
])

app.layout = url_content_layout

app.validation_layout = html.Div([
    url_content_layout,
    home.home_layout,
    visualize.visual_layout,
    forecasting.forecast_layout,
    about.about_layout,
    news.news_layout
])

@app.callback(Output(component_id="output-div", component_property="children") , Input(component_id="url", component_property="pathname"))
def update_output_div(pathname):
    if pathname == "/forecasting":
        return forecasting.forecast_layout
    elif pathname == "/visualize":
        return visualize.visual_layout
    elif pathname == "/about":
        return about.about_layout
    elif pathname == "/news":
        return news.news_layout
    else:
        return home.home_layout

if __name__ == "__main__":
    app.run_server(debug = True)