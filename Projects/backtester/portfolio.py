class Portfolio:
    def __init__(self):
        self.holdings = {}  # {symbol: units}

    def add_asset(self, symbol, units):
        self.holdings[symbol] = float(units)

    def remove_asset(self, symbol, units):
        if symbol in self.holdings:
            self.holdings[symbol] -= units
            if self.holdings[symbol] <= 0:
                del self.holdings[symbol]

    def get_portfolio_value(self, price_df):
        portfolio_value = 0
        for symbol, amount in self.holdings.items():
            print(f"cal. Symbol: {symbol}, Amount: {amount}")
            price = float(price_df[symbol]['2024-12-31'])#example date, need to be dynamic
            value = amount * price
            print(f"Value for {symbol}: {value}")
            portfolio_value += float(value)
        return portfolio_value

