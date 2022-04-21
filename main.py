import requests
from twilio.rest import Client

twilio_id = 'AC50ec95c0dd11b927888bf2bb611a5ea5'
auth_token = '693bc1b28204087ba61e6409d0a17a04'

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"
ACCESS_KEY_STOCK = "NOPGA9E1IWJ157FD"
NEWS_API_KEY = "db68be269e7c4d5693375c82354ca96b"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"


stock_params = {
    "function": 'TIME_SERIES_DAILY',
    "symbol": STOCK_NAME,
    "apikey":ACCESS_KEY_STOCK
}
response = requests.get(STOCK_ENDPOINT, params=stock_params)
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data ["4. close"]
print(yesterday_closing_price)

day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data ["4. close"]
print(day_before_yesterday_closing_price)

difference = abs( float(yesterday_closing_price) - float(day_before_yesterday_closing_price))
up_down = None
if difference > 0 :
    up_down = "🔺"
else:
    up_down = "🔻"

diff_percent = round((difference / float(yesterday_closing_price)) * 100)
print(diff_percent)

if abs(diff_percent) > 4:
    tesla_news = {
        "apiKey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME,
    }
    news_response = requests.get(NEWS_ENDPOINT, params=tesla_news)
    #articles = news_response.json()['articles']
    articles = news_response.json()["articles"]
    three_articles = articles[:3]
    print(three_articles)

    formated_articles = [f"{STOCK_NAME}: {up_down}{diff_percent}%\nHeadline : {article['title']}. \nBrief: {article['description']}" for article in three_articles]
    client = Client(twilio_id, auth_token)

for article in formated_articles:
    message = client.messages.create(
        body=article,
        from_='+18124135961',
        to='+7792012033'
    )

