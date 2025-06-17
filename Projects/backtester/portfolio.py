import pandas as pd

def get_closest_date_index(date, df_original):
    """
    Get the index of the closest date in a list of dates.
    Args:
        date (timestamp): The date to find the closest match for.
        date_series (pandas.Series): A pandas series of pandas.Timestamp objects.
    Returns:
        int: The index of the closest date in the list.
    """
    # getting the closest date index
    df_with_dates = df_original.copy()
    df_with_dates['timedeltas'] = abs(df_with_dates.index - date)
    min_diff = min(df_with_dates['timedeltas'])
    # Calculate the difference between the last date in the DataFrame and today
    index = df_with_dates['timedeltas'].isin([min_diff]).idxmax()
    return index

class Portfolio:
    """
    A class to represent a portfolio of assets.
    Attributes:
        holdings (dict): A dictionary where keys are asset symbols and values are the number of units held.
    """

    def __init__(self, first_name, last_name):
        '''Initialize the portfolio with an empty dictionary to hold assets.
            Dictionary structure: {symbol: units}
            where symbol is the key to the dictionary, and it is a string of 4 letters (as per the normal stock symbol format), 
            and units is a float representing the number of units held of that asset.'''
        self.holdings = [] #queue
        self.holdings_dates = []#queue
        self.value = 0.0
        self.first_name = first_name
        self.last_name = last_name
        self.full_name = f"{self.first_name} {self.last_name}"

    def add_asset(self, symbol, units, buy_date):
        '''Add an asset to the portfolio.
        If the asset already exists, it will update the number of units held.
        If runnning several times, make sure dates are in chronological order.
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
        if buy_date is None or not isinstance(buy_date, pd.Timestamp):
            raise ValueError("Buy date must be a valid pandas Timestamp.")
        
        # Add asset to the portfolio
        #check if the date provided is already in the holdings_dates queue
        if buy_date in self.holdings_dates:
            index = self.holdings_dates.index(buy_date)
            #if the symbol is already in the holdings, update the units
            if symbol in self.holdings[index]:
                self.holdings[index][symbol] += float(units)
            else:
                self.holdings[index][symbol] = float(units)
        else:
            #if the date is not in the holdings_dates queue, add a new entry
            self.holdings_dates.append(buy_date)
            self.holdings.append({symbol: float(units)})
            
        

    def remove_asset(self, symbol, units, sell_date):
        '''Remove an asset from the portfolio by selling a certain number of units.
        If  running several times, make sure dates are in chronological order.
        Args:
            symbol (str): The symbol of the asset to remove.
            units (float): The number of units to remove.
            sell_date (pandas.Timestamp): The date on which the asset is sold.
        '''
        #check if the sell date is in the holdings_dates queue
        if sell_date not in self.holdings_dates:
            #copy the portfolio from last available date
            self.holdings.append(self.holdings[-1].copy())# copy data so it is not connected to the original in case of changing
            self.holdings_dates.append(sell_date)
        # Get the last available date
        #check if the symbol is in the holdings
        if symbol in self.holdings[-1]:
            self.holdings[symbol] -= units
            if self.holdings[symbol] <= 0:
                del self.holdings[symbol]

    def get_portfolio_value(self, closing_data_df, date= pd.Timestamp.today()):
        '''Calculate the total value of the portfolio at a given date.
        Args:
            closing_data_df (DataFrame): A DataFrame containing the closing prices of assets with dates as index.
            date (pandas.Timestamp): The date for which to calculate the portfolio value. Defaults to today.
        Returns:
            float: The total value of the portfolio at the given date.
        '''

        # date = date.strftime('%Y-%m-%d')  # Ensure date is in string format #1
        portfolio_value = 0
        for symbol, amount in self.holdings.items():
            print(f"Calculating Symbol: {symbol}, Amount: {amount}, input Date: {date}")
            if date not in closing_data_df[symbol].index: # CHANGE CODE TO GET DATA FROM CLOSEST DATE TO THE GIVEN DATE
                print(f"Price for {symbol} on {date} is not available. calculating with the latest available")
                #change today to the latest available date in price_df
                date = get_closest_date_index(date, closing_data_df) # Get the last available date #2 Latest date works if we want to know closest price to today, for other dates need to calculate timedelta
                print(f"Using latest available date: {date}")
            price = float(closing_data_df[symbol][date])#example date, need to be dynamic
            if type(price) is not float:
                price = 0
            value = amount * price
            print(f"Value for {symbol}: {value}")
            portfolio_value += float(value)
            self.value = portfolio_value
            print(f"Current Portfolio Value: {portfolio_value}")
        return portfolio_value

