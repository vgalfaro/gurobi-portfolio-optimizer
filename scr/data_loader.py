import pandas as pd, yfinance as yf, numpy as np

MARKET_SUFFIX = {
    "chile": ".SN",
    "ny": "",
}
# ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']
PERIOD = '1mo'

def load_tickers(path, market):
    with open(path) as f:
        raw = f.read().split()
    return [t + MARKET_SUFFIX[market] for t in raw]

# tickers_ipsa = load_tickers("tickers_ipsa.txt", market="chile")
tickers = load_tickers("tickers_test.txt", market="ny")


data = yf.download(tickers, period=PERIOD)

df_close = data['Close']
df_close.to_csv(f'close-values-{PERIOD}.csv')