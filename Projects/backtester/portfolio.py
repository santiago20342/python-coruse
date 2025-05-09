class Portfolio:
    def __init__(self):
        self.holdings = {}  # {symbol: units}

    def add_asset(self, symbol, units):
        self.holdings[symbol] = self.holdings.get(symbol, 0) + units

    def remove_asset(self, symbol, units):
        if symbol in self.holdings:
            self.holdings[symbol] -= units
            if self.holdings[symbol] <= 0:
                del self.holdings[symbol]

    def get_portfolio_value(self, price_df):
        portfolio_value = 0
        for symbol, amount in self.holdings.items():
            #print(f"Symbol: {symbol}, Amount: {amount}")
            price = price_df[symbol]['2024-12-31']#example date, need to be dynamic
            value = amount * price
            #print(f"Value for {symbol}: {value}")
            portfolio_value += value
        return portfolio_value


# Example usage
from data_fetch import get_price

shares = ['AAPL', 'MSFT', 'GOOG', 'AMZN', 'TSLA', 'NVDA', 'NFLX']
portfolio = Portfolio()
for symbol in shares:
    portfolio.add_asset(symbol, 1)



start = '2024-01-01'
end = '2025-01-01'

prices_df = get_price(shares, start, end)
prices_close_df = prices_df['Close']

print("Portfolio Value:", portfolio.get_portfolio_value(prices_close_df))