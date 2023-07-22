import pprint

import pandas
import webull

wb = webull.paper_webull()


def get_buy_sell_signals(symbol):
    # Fetch historical stock data using the 'get_bars' method from the 'webull' package
    bars = wb.get_bars(stock=symbol, interval='d', count=100)

    # Create a DataFrame from the fetched data
    stock_data = pandas.DataFrame(bars)

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

    print(f"Buy Signals: {len(buy_signals)}")
    print(f"Sell Signals: {len(sell_signals)}")

    buy_signals_timestamped = {
        pandas.Timestamp(timestamp).to_pydatetime(): True
        for timestamp in buy_signals['Buy Signal'].index.values
    }
    sell_signals_timestamped = {
        pandas.Timestamp(timestamp).to_pydatetime(): False
        for timestamp in sell_signals['Sell Signal'].index.values
    }
    if len(sell_signals) > len(buy_signals):
        print('ASSESSMENT: SELL')
    else:
        print('ASSESSMENT: BUY')
    return {
        k.strftime("%Y-%m-%d"): v
        for k, v in dict(sorted({**buy_signals_timestamped, **sell_signals_timestamped}.items())).items()
    }


if __name__ == '__main__':
    result = get_buy_sell_signals(symbol="AAPL")
    pprint.pprint(result)
