from dash import html 
import requests
from pages import navigation

# Fetch news data from News API
def fetch_news():
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": "stock market OR business OR banking",
        "apiKey": "ec60ee0618234b308621882d8456f3b3",  # Replace with your News API key
        "pageSize": 20  # Number of articles to fetch
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        news_data = response.json()
        return news_data.get("articles", [])
    else:
        return []

# Create news layout
def create_news_layout(news_articles):
    news_layout = []
    for article in news_articles:
        title = article.get("title", "")
        description = article.get("description", "")
        source = article.get("source", {}).get("name", "")
        url = article.get("url", "")

        # Validate if title and URL are not empty before adding the news item
        if title and url:
            news_item = html.Div([
                html.H2(title),
                html.P(description),
                html.P(f"Source: {source}"),
                html.A("Read More", href=url, target="_blank")
            ])
            news_layout.append(news_item)
        else:
            # Log a message or handle the case where the article data is incomplete
            print("Incomplete or missing data for news article:", article)

    return html.Div(news_layout)


# Define app layout
news_layout = html.Div(children=[
    navigation.navbar,
    html.H1("Stock Forecasting Dashboard"),
    html.H2("Latest News"),
    create_news_layout(fetch_news())
])

