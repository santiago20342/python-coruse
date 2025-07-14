import pandas as pd

def get_closest_date_index(date, df_original):
    """
    Get the index of the closest date in a list of dates.
    Args:
        date (timestamp):                   The date to find the closest match for.
        date_series (pandas.Series):        A pandas series of pandas.Timestamp objects.
    Returns:
        nearest date (datetime.date):       The index of the closest date in the list.
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
            self.first_name(str):                       first name of every sentor
            self.last_name(str):                        last name of every sentor
            self.holding(dict):                         initial_date][symbol]= [float(units), float(single_stock_prices[symbol])]
            self.single_stock_prices(panda Series):     a series that hold the values of assets of the porfiolo 
            self.initial_date(str):                     the date the stock was brough
    """

    def __init__(self, first_name, last_name, holdings, single_stock_prices, initial_date):
        '''Initialize the portfolio with an empty dictionary to hold assets.
            Arguments:
            first_name:str
            last_name:str
            holdings:dict
            single_stock_prices:panda Series
            initil_date:str

            Attributes:  
            self.first_name(str):                       first name of every sentor
            self.last_name(str):                        last name of every sentor
            self.holding(dict):                         {[initial_date]:{[symbol]:[float(units), float(single_stock_prices[symbol]}}
            self.single_stock_prices(panda Series):     a series that hold the values of assets of the porfiolo 
            self.initial_date(str):                     the date the stock was brought 
            '''
        
        self.holdings = holdings #dictionary
        self.investment = {} #dictionary
        self.capital_gains = {} #dictionary
        self.portfolio_value = None
        #calculate the first portfolio value
        self.temp_value = 0
        for symbol, units in self.holdings[initial_date].items():
            self.holdings[initial_date][symbol]= [float(units), float(single_stock_prices[symbol])]
            self.temp_value += (units * float(single_stock_prices[symbol]))
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
        if buy symbol in holding and date then add to it, but if not then 
        
        Args:
            symbol (str):           The symbol of the asset to add.
            units (float):          The number of units to add.
            buy_date(str):          Date the assest was brought 
            buy_price(str):         Price the asset was brought 
        '''
        #Error handling for symbol and units
        if not isinstance(symbol, str) or not isinstance(units, (int, float)):
            raise ValueError("Symbol must be a string and units must be a number.")

        if units < 0:
            raise ValueError("Units cannot be negative.")

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
        
        if buy_date not in self.investment:
            self.investment[buy_date] = float(units) * buy_price #update the investment value
        else:
            self.investment[buy_date] += float(units) * buy_price

    def remove_asset(self, symbol, units, sell_date, sell_price):
        '''Remove an asset from the portfolio by selling a certain number of units.
        If  running several times, make sure dates are in chronological order.
        if we don't have buy date then set it to 0 and negative for now 
        
        Args:
            symbol (str):                   The symbol of the asset to remove.
            units (float):                  The number of units to remove.
            sell_date (pandas.Timestamp):   The date on which the asset is sold.
            sell_price(float):              The price of the stock when sold
        '''
        # Find out last time the asset was bought. 
        self.last_buy_date = sell_date
        date_list = list(sorted(self.holdings.keys(), reverse=True))# newest to oldest
        
        if len(date_list) > 1:
            for i in range(len(date_list) - 1): # the dates themselves and we use them to check if the symbol value is in dict
                if symbol not in self.holdings[date_list[i+1]]:#checking second-newest date
                    self.holdings[date_list[i+1]][symbol] = [0, sell_price-1]#set the number of stock to zero 
                if symbol not in self.holdings[date_list[i]]:
                    self.holdings[date_list[i]][symbol] = self.holdings[date_list[i+1]][symbol]
            if self.holdings[date_list[0]][symbol][0] > self.holdings[date_list[1]][symbol][0]:
                self.last_buy_date = date_list[1]
            else:
                self.last_buy_date = date_list[0]
        else:
            self.last_buy_date = date_list[0] #in the case of only one date

        if self.last_buy_date not in self.holdings: 
            date_list = list(sorted(self.holdings.keys(), reverse=True))#order from largest to smallest (newst to oldest)
            #create a dict empty if last buy date is not in holding
            self.holdings[self.last_buy_date] = self.holdings[date_list[0]].copy()# copy data so it is not connected to the original in case of changing
        if symbol not in self.holdings[self.last_buy_date]:
            self.holdings[self.last_buy_date][symbol] = [0, sell_price-2] #set number of stock to 0      
        
        
        #check if the sell date is in the holdings
        if sell_date not in self.holdings.keys(): #checks if sell date is in holding keys 
            date_list = list(sorted(self.holdings.keys(), reverse=True))#order from largest to smallest (newest to oldest)
            #copy the portfolio from last available date
            self.holdings[sell_date] = self.holdings[date_list[-1]].copy()# copy data so it is not connected to the original in case of changing
        if symbol not in self.holdings[sell_date].keys(): # symbol is not in the dict then i will set the number of stock to zero
            self.holdings[sell_date][symbol] = [0, sell_price-1] 
     
       

        if symbol in self.holdings[sell_date].keys():
            self.holdings[sell_date][symbol][0] -= units 
        else:
            self.holdings[sell_date][symbol] = [-units, sell_price] # If the symbol is not in the holdings, set it to 0 units
      

         #Calculating capital gain 
        capital_gain = (sell_price - self.holdings[self.last_buy_date][symbol][1]) * units 
        if sell_date not in self.capital_gains:
            self.capital_gains[sell_date] = capital_gain #update the investment value
        else:
            self.capital_gains[sell_date] += capital_gain
        
        if sell_date not in self.investment:
            self.investment[sell_date] = - (float(units) * self.holdings[self.last_buy_date][symbol][1])
        else:
            self.investment[sell_date] -= (float(units) * self.holdings[self.last_buy_date][symbol][1])
        


    def get_portfolio_value(self, closing_data_df):
        '''Calculate the total value of the portfolio at a given date.
        
        Args:
            closing_data_df (DataFrame):        A DataFrame containing the closing prices of assets with dates as index.
            date (pandas.Timestamp):            The date for which to calculate the portfolio value. Defaults to today.
            merage_df (date frame):             To join 2 portfolio into one
       
        Returns:
            self.portfolio_value(DataFrame):    The total value of the portfolio at the given date.
        '''
        # Turn self.holdings and self.holdings_dates into a DataFrame
        # Clean holdings: keep only the first element for each symbol
        #clean holding is to get the first item of the list which is the number of stock 
        cleaned_holdings = {
            date: {symbol: max(0, value[0]) if isinstance(value, list) and len(value) > 0 else value
                   for symbol, value in symbols.items()}
            for date, symbols in self.holdings.items()
        }

        holdings_df = pd.DataFrame(cleaned_holdings).T

        #holdings_df = pd.DataFrame(self.holdings).T
        original_columns = holdings_df.columns #get original columns to calculate values later

        #truncate the closing_data_df to the range of dates in holdings_df
        holdings_df['Date'] = pd.to_datetime(holdings_df.index)#need to check if dates are in order
        sorted_dates = sorted(holdings_df['Date'])
        before = sorted_dates[0]
        after  = sorted_dates[-1]
        pr_trunc = closing_data_df.truncate(before=before, after=after)#to set date the data  begin and ends 

        #merge
        #merging the holding_df with the original_columns 
        merged_df = holdings_df.join(pr_trunc, on='Date', how='right', rsuffix='_prices')#joins two profilos together 
        merged_df.fillna(method='ffill', inplace=True)  # Forward fill to copy portfolio values to all dates until manually changed
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
        final['yield'] = final['Total_Value'].pct_change()
        self.portfolio_value = final

        