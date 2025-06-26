import matplotlib.pyplot as plt

def plot_df_prices_components(price_data):
    price_data.plot.area()
    plt.title('Asset Prices')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.show()


def plot_df_prices_lines(portfolio_list):
    plt.figure(figsize=(10,6))
    for portfolio in portfolio_list:
        
        plt.plot(portfolio.portfolio_value.index, portfolio.portfolio_value['Total_Value'], label=portfolio.full_name)
    plt.legend()
    plt.title("Portfolio Values (from inception)")
    plt.show()

