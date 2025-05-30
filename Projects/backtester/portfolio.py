import datetime

class Portfolio:
    """
    A class to represent a portfolio of assets."""

    def __init__(self):
        self.holdings = {}  # {symbol: units}

    def add_asset(self, symbol, units):
        self.holdings[symbol] = float(units)

    def remove_asset(self, symbol, units):
        if symbol in self.holdings:
            self.holdings[symbol] -= units
            if self.holdings[symbol] <= 0:
                del self.holdings[symbol]

    def get_portfolio_value(self, closing_data_df, date= datetime.date.today()):
        date = date.strftime('%Y-%m-%d')  # Ensure date is in string format
        portfolio_value = 0
        for symbol, amount in self.holdings.items():
            print(f"Calculating Symbol: {symbol}, Amount: {amount}, Date: {date}")
            if date not in closing_data_df[symbol].index: # CHANGE CODE TO GET DATA FROM CLOSEST DATE TO THE GIVEN DATE
                print(f"Price for {symbol} on {date} is not available. calculating with the latest available")
                #change today to the latest available date in price_df
                date = closing_data_df[symbol].index[-1]  # Get the last available date
                print(f"Using latest available date: {date}")
            price = float(closing_data_df[symbol][date])#example date, need to be dynamic
            value = amount * price
            print(f"Value for {symbol}: {value}")
            portfolio_value += float(value)
            print(f"Current Portfolio Value: {portfolio_value}")
        return portfolio_value

