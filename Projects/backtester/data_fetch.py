import yfinance as yf
import pandas as pd

def get_price(symbol):
    data = yf.download(symbol, period='max', interval='1d', rounding=True)
    return data


def import_yf_df(path, shares_list):
    """    Import a CSV file containing historical stock prices and return a DataFrame with closing prices."""
    #retrieve data from csv
    prices_df = pd.read_csv(path)
    prices_df

    columns_to_filter = ['Price', 'Close']
    for i,element in enumerate(shares_list[1:]):
        columns_to_filter.append('Close'+'.'+str(i+1))
        #print(columns_to_filter)

    #filtering the columns to get only the closing prices
    prices_close_df = prices_df[columns_to_filter]

    column_new = ['Date']
    for i,element in enumerate(shares_list):
        column_new.append(element)
    prices_close_df.columns = column_new

    #erase rows 0 and 1
    prices_close_df = prices_close_df.drop([0, 1])

    # Convert 'Date' column to datetime objects
    prices_close_df['Date'] = pd.to_datetime(prices_close_df['Date'])
    prices_close_df.set_index('Date', inplace=True)

    #making the columns float
    cols = prices_close_df.columns
    cols
    for col in cols:
        prices_close_df[col] = prices_close_df[col].astype(float)

    return prices_close_df