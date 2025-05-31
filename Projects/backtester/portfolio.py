import datetime

class Portfolio:
    """
    A class to represent a portfolio of assets.
    Attributes:
        holdings (dict): A dictionary where keys are asset symbols and values are the number of units held.
    """

    def __init__(self):
        '''Initialize the portfolio with an empty dictionary to hold assets.
            Dictionary structure: {symbol: units}
            where symbol is the key to the dictionary, and it is a string of 4 letters (as per the normal stock symbol format), 
            and units is a float representing the number of units held of that asset.'''
        self.holdings = {}  # {symbol: units}

    def add_asset(self, symbol, units):
        '''Add an asset to the portfolio.
        If the asset already exists, it will update the number of units held.
        Args:
            symbol (str): The symbol of the asset to add.
            units (float): The number of units to add.
        '''
        #Error handling for symbol and units
        if not isinstance(symbol, str) or not isinstance(units, (int, float)):
            raise ValueError("Symbol must be a string and units must be a number.")
        if len(symbol) != 4: 
            raise ValueError("Symbol must be exactly 4 characters long.")
        if units < 0:
            raise ValueError("Units cannot be negative.")
        
        # Add asset to the portfolio
        if symbol in self.holdings:
            self.holdings[symbol] += float(units)
        else:
            self.holdings[symbol] = float(units)
            
        

    def remove_asset(self, symbol, units):
        '''Remove an asset from the portfolio.'''
        if symbol in self.holdings:
            self.holdings[symbol] -= units
            if self.holdings[symbol] <= 0:
                del self.holdings[symbol]

    def get_portfolio_value(self, closing_data_df, date= datetime.date.today()):
        '''Calculate the total value of the portfolio at a given date.
        Args:
            closing_data_df (DataFrame): A DataFrame containing the closing prices of assets with dates as index.
            date (datetime.date): The date for which to calculate the portfolio value. Defaults to today.
        Returns:
            float: The total value of the portfolio at the given date.
        '''

        # date = date.strftime('%Y-%m-%d')  # Ensure date is in string format #1
        portfolio_value = 0
        for symbol, amount in self.holdings.items():
            print(f"Calculating Symbol: {symbol}, Amount: {amount}, Date: {date}")
            if date not in closing_data_df[symbol].index: # CHANGE CODE TO GET DATA FROM CLOSEST DATE TO THE GIVEN DATE
                print(f"Price for {symbol} on {date} is not available. calculating with the latest available")
                #change today to the latest available date in price_df
                date = closing_data_df[symbol].index[-1]  # Get the last available date #2 Latest date works if we want to know closest price to today, for other dates need to calculate timedelta
                print(f"Using latest available date: {date}")
            price = float(closing_data_df[symbol][date])#example date, need to be dynamic
            value = amount * price
            print(f"Value for {symbol}: {value}")
            portfolio_value += float(value)
            print(f"Current Portfolio Value: {portfolio_value}")
        return portfolio_value

