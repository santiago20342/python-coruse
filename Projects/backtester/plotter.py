import matplotlib.pyplot as plt

def plot_df_prices_components(price_data):
    price_data.plot.area()
    plt.title('Asset Prices')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.show()


def plot_df_prices_lines(price_data):
    price_data.plot()
    plt.title('Asset Prices')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.show()
