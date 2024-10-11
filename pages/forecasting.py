from pages import navigation
from app import app
import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from dash import html, dcc, Input, Output , State
import plotly.graph_objs as go

# Add input components for stock symbol, range of days, and number of future prediction days
forecast_layout = html.Div(children=[
    navigation.navbar,
    html.H1("Stock Forecasting Dashboard"),
    html.Label("Enter Stock Symbol:"),
    dcc.Input(id='stock-input', type='text'),
    html.Label("Enter Range of Days to Visualize:"),
    dcc.Input(id='range-days-input', type='number'),
    html.Label("Enter Number of Future Prediction Days:"),
    dcc.Input(id='prediction-days-input', type='number'),
    html.Button('Update Graph', id='update-graph-button', n_clicks=0),
    html.Div(id='output-graph')
])

@app.callback(
    Output('output-graph', 'children'),
    [Input('update-graph-button', 'n_clicks')],
    [State('stock-input', 'value'),
     State('range-days-input', 'value'),
     State('prediction-days-input', 'value')]
)
def update_graph(n_clicks, stock_symbol, range_days, prediction_days):
    if n_clicks == 0:
        return None  # No button click yet, so no graph to update

    # Check for empty input boxes
    if not stock_symbol or not range_days or not prediction_days:
        return html.Div("Please fill in all input boxes.", style={'color': 'red'})

    try:
        # Fetching historical stock data
        stock_data = yf.download(stock_symbol, period=f"{range_days}d")

        # Data preprocessing
        stock_data['Price_Up'] = np.where(stock_data['Close'].shift(-1) > stock_data['Close'], 1, 0)

        # Features and target variable
        X = stock_data[['Open', 'High', 'Low', 'Close', 'Volume']].values
        y = stock_data['Price_Up'].values

        # Model training
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X, y)

        # Define the last date
        last_date = stock_data.index[-1]

        # Making predictions for the specified number of future days
        last_close_price = stock_data['Close'].iloc[-1]
        future_dates = pd.date_range(start=last_date, periods=prediction_days)
        future_prices = [last_close_price]  # Start with the last known price
        for i in range(prediction_days):
            prediction = model.predict(X[-1].reshape(1, -1))
            daily_return = np.random.normal(loc=0, scale=stock_data['Close'].pct_change().std())  # Using historical volatility
            future_price = future_prices[-1] * (1 + daily_return)
            future_prices.append(max(0, future_price)) 

        # Plotting the graph
        trace = go.Scatter(
            x=stock_data.index,
            y=stock_data['Close'],
            mode='lines',
            name='Historical Close Price'
        )

        # Line for future predictions
        trace_future = go.Scatter(
            x=future_dates,
            y=future_prices[1:],  # Exclude the first price (last known price)
            mode='lines',
            name='Future Predictions'
        )

        layout = {
            'title': f'Stock Price and Predicted Movement for {stock_symbol}',
            'xaxis': {'title': 'Date'},
            'yaxis': {'title': 'Price'},
        }

        figure = {'data': [trace, trace_future], 'layout': layout}

        return dcc.Graph(id='stock-graph', figure=figure)
    
    except Exception as e:
        return html.Div(f"An error occurred: {str(e)}", style={'color': 'red'})
