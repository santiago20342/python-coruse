from data_fetch import get_price
from portfolio import Portfolio
from plotter import plot_prices

# Example usage
portfolio = Portfolio()
portfolio.add_asset('AAPL', 10)
portfolio.add_asset('MSFT', 5)

start = '2024-01-01'
end = '2025-01-01'

#prices = {
#    'AAPL': get_price('AAPL', start, end),
#    'MSFT': get_price('MSFT', start, end)
#}

prices = get_price(['AAPL', 'MSFT'], start, end)
plot_prices(prices['Close'])

# Calculate today's value
latest_prices = {symbol: data.iloc[-1] for symbol, data in prices.items()}
print("Portfolio Value:", portfolio.get_portfolio_value(latest_prices))
