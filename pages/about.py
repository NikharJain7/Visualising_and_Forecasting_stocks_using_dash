from dash import html
from pages import navigation

about_layout = html.Div(children=[
    navigation.navbar,
    html.H1(children="About FinSight", style={'textAlign': 'center'}),

    html.Div([
        html.H2("Our Mission", style={'marginBottom': '10px'}),
        html.P(
            "At FinSight, we are committed to providing you with the tools and information you need to make informed decisions in the world of finance. "
            "Our mission is to empower investors of all levels with accurate data, insightful analysis, and timely news updates.",
            style={'marginBottom': '20px'}
        ),
    ], style={'marginBottom': '30px'}),

    # html.Div([
    #     html.H2("Our Team", style={'marginBottom': '10px'}),
    #     html.Ul([
    #         html.Li("Name: Role"),
    #         html.Li("Name: Role"),
    #         html.Li("Name: Role")
    #     ], style={'listStyleType': 'none', 'marginBottom': '20px'})
    # ], style={'marginBottom': '30px'}),

    html.Div([
        html.H2("Technologies Used", style={'marginBottom': '10px'}),
        html.Ul([
            html.Li("Dash: A Python framework for building interactive web applications"),
            html.Li("Plotly: A graphing library for creating interactive charts and graphs"),
            html.Li("yfinance: A Python library for accessing stock market data from Yahoo Finance"),
            html.Li("Pandas: A powerful data manipulation library in Python"),
            html.Li("Scikit-learn: A machine learning library for building predictive models"),
            html.Li("News API: An API for fetching real-time news articles"),
            
        ], style={'listStyleType': 'none', 'marginBottom': '20px'})
    ], style={'marginBottom': '30px'}),

    html.Div([
        html.H2("Contact Us", style={'marginBottom': '10px'}),
        html.P("We'd love to hear from you! If you have any questions, feedback, or suggestions for improvement, please don't hesitate to reach out to us:",
               style={'marginBottom': '20px'}),
       
    ])
])
