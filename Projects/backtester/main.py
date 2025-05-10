from data_fetch import get_price
from portfolio import Portfolio
from plotter import plot_prices
import pandas as pd

# Creating a portfolio with multiple assets
from data_fetch import get_price
from portfolio import Portfolio
from plotter import plot_prices

shares = ['AAPL', 'MSFT', 'GOOG', 'AMZN', 'TSLA', 'NVDA', 'NFLX']
portfolio = Portfolio()
for symbol in shares:
    portfolio.add_asset(symbol, 1)


start = '2024-01-01'
end = '2025-01-01'

#calling API to get prices
prices_df = get_price(shares, start, end)
prices_df.to_csv('prices.csv', index=True) #saving prices to csv
#retrieving prices from csv
prices_df = pd.read_csv('prices.csv', parse_dates=True)

#transforming prices to close prices
prices_close_df = prices_df[['Price', 'Close','Close.1','Close.2','Close.3','Close.4','Close.5','Close.6']]#select columns
prices_close_df.columns = ['Date', 'AAPL', 'MSFT', 'GOOG', 'AMZN', 'TSLA', 'NVDA', 'NFLX']#setting column names\
prices_close_df = prices_close_df.drop([0, 1])#dopping first two rows

prices_close_df.set_index('Date', inplace=True) #setting date as index (not sure if needed)

value = portfolio.get_portfolio_value(prices_close_df)

print("Portfolio Value:", value)