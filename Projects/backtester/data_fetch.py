import yfinance as yf

def get_price(symbol, start, end):
    data = yf.download(symbol, start=start, end=end)
    return data['Adj Close']