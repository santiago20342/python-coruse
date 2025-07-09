import matplotlib.pyplot as plt

def plot_df_prices_components(portfolio):
    df = portfolio.portfolio_value.drop(columns=['Total_Value'], errors='ignore')
    df.plot.area()
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

