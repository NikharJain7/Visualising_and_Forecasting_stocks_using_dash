from dash import html , dcc , State
from pages import navigation
import yfinance as yf
import plotly.graph_objs as go
from app import app
from dash.dependencies import Input , Output
from datetime import date
import plotly.express as px
import pandas as pd

# Function to fetch company information
def get_company_info(stock_code):
    ticker = yf.Ticker(stock_code)
    info = ticker.info
    df = pd.DataFrame().from_dict(info, orient="index").T
    try:
        logo_url = df.iloc[0]['logo_url']  # Access logo_url if it exists
    except KeyError:
        logo_url = None  # Set to None if not available
    return df.iloc[0]['longBusinessSummary'], logo_url, df.iloc[0]['shortName']

def get_stock_price_fig(df):
    try:
        if 'Date' in df.columns:
            fig = px.line(df,
                          x='Date',  # Use 'Date' if available
                          y=['Open', 'Close'],
                          title="Closing and Opening Price vs Date")
        else:
            fig = px.line(df,
                          x=df.index,  # Use index as x-axis if 'Date' is missing
                          y=['Open', 'Close'],
                          title="Closing and Opening Price vs Date")
    except KeyError:
        # Handle case where 'Open' or 'Close' columns are missing
        pass
    return fig

# Function to generate EMA plot
def get_ema_fig(df):
    df['EWA_20'] = df['Close'].ewm(span=20, adjust=False).mean()
    fig = px.scatter(df,
                    x='Date',
                    y='EWA_20',
                    title="Exponential Moving Average vs Date")
    fig.update_traces(mode='lines+markers')
    return fig

visual_layout = html.Div(className="visual_container", children=[
    navigation.navbar,
    # html.P(children="Welcome to FinSight!", className="start"),
    html.Div([
    html.Div([
        html.Div([
            html.Label("Input Stock Code: ", className="line"),
            html.Br(),
            dcc.Input(id="stock-code", value="", type="text"),
            html.Button('Search', id="search-button", n_clicks=0)
        ], className="inputs"),
        html.Div([
            dcc.DatePickerRange(
                id='date-picker-range',
                start_date=date(2020, 6, 21),
                end_date=date(2021, 1, 21),
                month_format='MMM Do, YY',
                clearable=True,
            )
        ], className="inputs_1"),
        html.Div([
            dcc.Dropdown(
                id='chart-type-dropdown',
                options=[
                    {'label': 'Line Charts', 'value': 'line'},
                    {'label': 'Candlesticks', 'value': 'candlestick'}
                ],
                placeholder="Charts",
            )
        ], className="inputs_2"),
    ],className="content_1"),
    html.Div([
        html.Div(id='description', className="decription_ticker"),
        dcc.Graph(id='graphs-content'),
        dcc.Graph(id='main-content'),
        # html.Div(id='forecast-content')
    ], className="content_2"),
],className ="content-wrapper")
])

@app.callback([
    Output('graphs-content', 'figure'),
    Output('description', 'children')],
    [Input('search-button', 'n_clicks')],
    [State('stock-code', 'value'),
     State('date-picker-range', 'start_date'),
     State('date-picker-range', 'end_date'),
     State('chart-type-dropdown', 'value')]
)
def update_content(n_clicks, stock_code, start_date, end_date, chart_type):
    if n_clicks is None:
        return {}, ''

    try:
        df = yf.download(stock_code, start=start_date, end=end_date)
        if isinstance(df.index, pd.RangeIndex) and not df.index.name:
            df.reset_index(inplace=True)

        if chart_type == 'candlestick':
            fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                                                 open=df['Open'],
                                                 high=df['High'],
                                                 low=df['Low'],
                                                 close=df['Close'])])
        else:
            fig = get_stock_price_fig(df)  # Call get_stock_price_fig to create the figure

        try:
            description, _, _ = get_company_info(stock_code)
            if description:
                return fig, [description]
            else:
                return fig, ['No company description available.']
        except (ValueError, KeyError) as e:  # Catch potential errors from get_company_info
            return {}, f"Error retrieving data or description: {str(e)}"
    except (ValueError, KeyError) as e:  # Handle download or data processing errors
        return {}, f"Error retrieving data or description: {str(e)}"

@app.callback(
    Output('main-content', 'figure'),
    [Input('search-button', 'n_clicks')],
    [State('stock-code', 'value'),
     State('date-picker-range', 'start_date'),
     State('date-picker-range', 'end_date')]
)
def update_ema_graph(n_clicks, stock_code, start_date, end_date):
    if n_clicks is None:
        return {}  # Return empty dict on initial load

    try:
        df = yf.download(stock_code, start=start_date, end=end_date)
        df.reset_index(inplace=True)
        fig = get_ema_fig(df)
        return fig
    except (ValueError, KeyError):  # Handle potential download errors
        return {}  # Return empty dict on download errors

