import matplotlib.pyplot as plt

def plot_df_prices(price_data):
    price_data.plot()
    plt.title('Asset Prices')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.show()
