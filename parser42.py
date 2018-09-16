import requests
import config
import datetime
from matplotlib.dates import date2num


def get_currency(symbol):
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    params = {'symbol': symbol, 'CMC_PRO_API_KEY': config.marketup}
    request = requests.get(url, params=params).json()
    data = dict(request)['data'][symbol]
    return (str(data['symbol']),
            round(data['quote']['USD']['price'], 4),
            data['quote']['USD']['percent_change_1h'],
            data['id'],
            data['quote']['USD']['percent_change_24h'],
            data['quote']['USD']['percent_change_7d'],
            data['name'])


def get_news(cur_name):
    url = ('https://newsapi.org/v2/everything?sources=crypto-coins-news&q=' +
           cur_name +
           '&apiKey=' +
           config.news_token +
           '&pageSize=5&sortBy=publishedAt')
    request = requests.get(url).json()
    data = dict(request)['articles']
    return data


def top_currincies(limit=10):
    url = f'https://api.coinmarketcap.com/v2/ticker/?limit={limit}&structure=array'
    request = requests.get(url).json()
    for i in dict(request)['data']:
        yield(str(i['symbol']), round(i['quotes']['USD']['price'], 4),
              i['quotes']['USD']['percent_change_1h'], i['id'], i['name'])


def get_histodata(cur_name):
    answer = []
    url = f'https://min-api.cryptocompare.com/data/histoday'\
        f'?fsym={cur_name}&tsym=USD&limit=100&aggregate=1&e=CCCAGG'
    data = requests.get(url).json()
    for quotes in data['Data']:
        date = date2num(datetime.datetime.fromtimestamp(quotes['time']))
        answer.append(tuple([date, quotes['open'], quotes['high'],
                             quotes['low'], quotes['close']]))
    return answer
