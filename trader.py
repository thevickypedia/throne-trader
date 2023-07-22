import pandas as pd
import webull

wb = webull.paper_webull()


def get_buy_sell_signals(symbol):
    # Fetch historical stock data using the 'get_bars' method from the 'webull' package
    bars = wb.get_bars(stock=symbol, interval='d', count=100)

    # Create a DataFrame from the fetched data
    stock_data = pd.DataFrame(bars)

    # Calculate short-term (e.g., 20-day) and long-term (e.g., 50-day) moving averages
    stock_data['SMA_short'] = stock_data['close'].rolling(window=20).mean()
    stock_data['SMA_long'] = stock_data['close'].rolling(window=50).mean()

    # Generate the buy signal
    stock_data['Buy Signal'] = stock_data['SMA_short'] > stock_data['SMA_long']

    # Generate the sell signal
    stock_data['Sell Signal'] = stock_data['SMA_short'] < stock_data['SMA_long']

    # Filter and display the buy and sell signals
    buy_signals = stock_data[stock_data['Buy Signal']]
    sell_signals = stock_data[stock_data['Sell Signal']]

    print("Buy Signals:")
    print(len(buy_signals))

    print("Sell Signals:")
    print(len(sell_signals))

    if len(sell_signals) > len(buy_signals):
        print('ASSESSMENT: SELL')
    else:
        print('ASSESSMENT: BUY')


if __name__ == '__main__':
    get_buy_sell_signals(symbol="AAPL")
