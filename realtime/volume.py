import yfinance as yf


def assumed_trading_volume(ticker: str, hours: int = 48):
    # Fetch historical stock data using yfinance
    stock_data = yf.download(ticker, period=f"{hours}h", interval="1h")

    # Filter rows with non-zero buy and sell volumes
    filtered_data = stock_data[(stock_data['Volume'] > 0)]

    # Separate buy and sell volume data
    assumed_buy_volume = filtered_data[filtered_data['Close'] > filtered_data['Close'].shift(-1)]['Volume']
    assumed_sell_volume = filtered_data[filtered_data['Close'] < filtered_data['Close'].shift(-1)]['Volume']

    return assumed_buy_volume, assumed_sell_volume


if __name__ == '__main__':
    ticker_symbol = "AAPL"
    buy_volume, sell_volume = assumed_trading_volume(ticker_symbol)

    print("Buy volume per hour for", ticker_symbol, "in the last 48 hours:")
    print(buy_volume)

    print("\nSell volume per hour for", ticker_symbol, "in the last 48 hours:")
    print(sell_volume)
