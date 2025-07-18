import matplotlib.pyplot as plt

def plot_df_prices_components(portfolio):
    df = portfolio.portfolio_value.drop(columns=['Total_Value', 'yield'], errors='ignore')
    df.plot.area(colormap='tab20')  # Use a nicer palette
    plt.title('Asset Prices')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.show()


def plot_df_prices_lines(portfolio_list):
    plt.figure(figsize=(10,6))
    for portfolio in portfolio_list:   
        plt.plot(portfolio.portfolio_value.index, portfolio.portfolio_value['yield'], label=portfolio.full_name)
    plt.title("Portfolio Values (from inception)")
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.show()


def plot_df_networth_lines(portfolio_list):
    plt.figure(figsize=(10,6))
    for portfolio in portfolio_list:   
        plt.plot(portfolio.networth.index, portfolio.networth['Net_worth'], label=portfolio.full_name)
    plt.title("Portfolio Values (from inception)")
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.show()