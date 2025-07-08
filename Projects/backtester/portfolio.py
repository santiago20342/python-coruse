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
    df_with_dates['timedeltas'] =  df_with_dates.index - date
    df_with_dates = df_with_dates[['timedeltas']]
    min_diff = df_with_dates[df_with_dates['timedeltas']<= pd.Timedelta(days=0)] #get the minimum timedelta that is less than or equal to 0
    #print(f"Minimum difference: {min_diff}")
    # Calculate the difference between the last date in the DataFrame and today
    index = min_diff.index[-1]
    #print (index.date())
    return index.date()


class Portfolio:
    """
    A class to represent a portfolio of assets.
    Attributes:
        holdings (dict): A dictionary where keys are asset symbols and values are the number of units held.
    """

    def __init__(self, first_name, last_name, holdings, single_stock_prices, initial_date):
        '''Initialize the portfolio with an empty dictionary to hold assets.
            Dictionary structure: {symbol: units}
            where symbol is the key to the dictionary, and it is a string of 4 letters (as per the normal stock symbol format), 
            and units is a float representing the number of units held of that asset.'''
        self.holdings = holdings #dictionary
        self.investment = {} #dictionary
        self.capital_gains = {} #dictionary
        self.portfolio_value = None
        #calculate the first portfolio value
        self.temp_value = 0
        for symbol, units in self.holdings[initial_date].items():
            self.holdings[initial_date][symbol]= [float(units), float(single_stock_prices[symbol])]
            self.temp_value += units * float(single_stock_prices[symbol])
        self.investment[initial_date] = self.temp_value
        self.capital_gains[initial_date] = 0
        self.temp_value = 0

        self.first_name = first_name
        self.last_name = last_name
        self.full_name = f"{self.first_name} {self.last_name}"




    def add_asset(self, symbol, units, buy_date, buy_price):
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
        # if len(symbol) != 4: 
        #     raise ValueError("Symbol must be exactly 4 characters long.")
        if units < 0:
            raise ValueError("Units cannot be negative.")
        #if buy_date is None or not isinstance(buy_date, pd.Timestamp):
        #   raise ValueError("Buy date must be a valid pandas Timestamp.")
        
        # Add asset to the portfolio
        #check if the date provided is already in the holdings
        if buy_date not in self.holdings.keys():
            date_list = list(sorted(self.holdings.keys(), reverse=True))
            # Sort the dates to get the last available date
            self.holdings[buy_date] = self.holdings[date_list[-1]].copy() #copying last portfolio state
        
        if symbol in self.holdings[buy_date].keys():
            self.holdings[buy_date][symbol][1] = buy_price #update the number of units held
            self.holdings[buy_date][symbol][0] += units 
            self.investment[buy_date] = float(units) * buy_price #update the investment value
        else:
            self.holdings[buy_date][symbol] = [units, buy_price]
            self.investment[buy_date] = float(units) * buy_price #update the investment value

    def remove_asset(self, symbol, units, sell_date, sell_price):
        '''Remove an asset from the portfolio by selling a certain number of units.
        If  running several times, make sure dates are in chronological order.
        Args:
            symbol (str): The symbol of the asset to remove.
            units (float): The number of units to remove.
            sell_date (pandas.Timestamp): The date on which the asset is sold.
        '''
        # Find out last time the asset was bought. 
        self.last_buy_date = None
        date_list = list(sorted(self.holdings.keys()))
        if len(date_list) > 1:
            for i, date in enumerate(date_list): 
                if symbol not in self.holdings[date_list[i-1]]:
                    self.holdings[date_list[i-1]][symbol] = [0, sell_price]
                if symbol not in self.holdings[date_list[i]]:
                    self.holdings[date_list[i]][symbol] = self.holdings[date_list[i-1]][symbol]
                if self.holdings[date_list[i]][symbol][0] > self.holdings[date_list[i-1]][symbol][0]:
                    self.last_buy_date = date_list[i]
                    
        else:
            self.last_buy_date = date_list[0]
             
        #check if the sell date is in the holdings_dates queue
        if sell_date not in self.holdings.keys():
            date_list = list(sorted(self.holdings.keys(), reverse=True))
            #copy the portfolio from last available date
            self.holdings[sell_date] = self.holdings[date_list[-1]].copy()# copy data so it is not connected to the original in case of changing
        if symbol not in self.holdings[sell_date].keys():
            self.holdings[sell_date][symbol] = [0, sell_price]
        # Get the last available date
        #check if the symbol is in the holdings
        # try:
        #     capital_gain = (sell_price - self.holdings[self.last_buy_date][symbol][1]) * units   
        # except:
        #     capital_gain = 0
        capital_gain = (sell_price - self.holdings[self.last_buy_date][symbol][1]) * units 

        if symbol in self.holdings[sell_date].keys():
            self.holdings[sell_date][symbol][0] -= units
            self.capital_gains[sell_date] = capital_gain #update the investment value
            self.investment[sell_date] = -float(units) * self.holdings[sell_date][symbol][0] #update the investment value
        else:
            self.holdings[sell_date][symbol] = [-units, sell_price]  # If the symbol is not in the holdings, set it to 0 units

    def get_portfolio_value(self, closing_data_df):
        '''Calculate the total value of the portfolio at a given date.
        Args:
            closing_data_df (DataFrame): A DataFrame containing the closing prices of assets with dates as index.
            date (pandas.Timestamp): The date for which to calculate the portfolio value. Defaults to today.
        Returns:
            float: The total value of the portfolio at the given date.
        '''
        # Turn self.holdings and self.holdings_dates into a DataFrame
        holdings_df = pd.DataFrame(self.holdings).T
        original_columns = holdings_df.columns #get original columns to calculate values later

        #truncate the closing_data_df to the range of dates in holdings_df
        holdings_df['Date'] = pd.to_datetime(holdings_df.index)#need to check if dates are in order
        sorted_dates = sorted(holdings_df['Date'])
        before = sorted_dates[0]
        after  = sorted_dates[-1]
        pr_trunc = closing_data_df.truncate(before=before, after=after)

        #merge
        merged_df = holdings_df.join(pr_trunc, on='Date', how='right', rsuffix='_prices')
        merged_df.fillna(method='ffill', inplace=True)  # Forward fill to copy portfolio values to all dates until manually changed
        #print(merged_df)
        merged_df.index =  pr_trunc.index  # Set the index to match prices_close_df

        # Calculate the value held for each asset on each date
        for col in original_columns:
            merged_df[col + '_value'] = merged_df[col] * merged_df[col + '_prices']

        # get sum of all asset values for each date
        merged_df['Total_Value'] = merged_df[[col + '_value' for col in original_columns]].sum(axis=1)

        #get new dataframe with only value columns
        value_columns = [col + '_value' for col in original_columns] + ['Total_Value']
        final = merged_df[['Date'] + value_columns]
        final.set_index('Date', inplace=True)
        self.portfolio_value = final

