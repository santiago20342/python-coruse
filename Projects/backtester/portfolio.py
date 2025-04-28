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

    def get_portfolio_value(self, price_dict):
        total_value = 0
        for symbol, units in self.holdings.items():
            price = price_dict.get(symbol, 0)
            total_value += units * price
        return total_value
