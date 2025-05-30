import yfinance as yf

def get_price(symbol):
    data = yf.download(symbol, period='max', interval='1d', rounding=True)
    return data