import pprint
from typing import Dict

import pandas
import webull

wb = webull.paper_webull()


def get_buy_sell_hold_signals(symbol: str) -> Dict[str, str]:
    # Fetch historical stock data using the 'get_bars' method from the 'webull' package
    bars = wb.get_bars(stock=symbol, interval='d', count=100)

    # Create a DataFrame from the fetched data
    stock_data = pandas.DataFrame(bars)

    # Calculate short-term (e.g., 20-day) and long-term (e.g., 50-day) moving averages
    stock_data['SMA_short'] = stock_data['close'].rolling(window=20).mean()
    stock_data['SMA_long'] = stock_data['close'].rolling(window=50).mean()

    # Generate the buy, sell, and hold signals
    stock_data['Buy Signal'] = stock_data['SMA_short'] > stock_data['SMA_long']
    stock_data['Sell Signal'] = stock_data['SMA_short'] < stock_data['SMA_long']
    stock_data['Hold Signal'] = ~(stock_data['Buy Signal'] | stock_data['Sell Signal'])

    # Filter and display the buy, sell, and hold signals
    buy_signals = stock_data[stock_data['Buy Signal']]
    sell_signals = stock_data[stock_data['Sell Signal']]
    hold_signals = stock_data[stock_data['Hold Signal']]

    assessment = {
        "Buy": len(buy_signals),
        "Sell": len(sell_signals),
        "Hold": len(hold_signals)
    }
    for key, value in assessment.items():
        print(f"{key} Signals:", value)

    print(f"Algorithm's assessment: {max(assessment, key=assessment.get)}")

    buy_signals_timestamped = {
        pandas.Timestamp(timestamp).to_pydatetime(): "Buy"
        for timestamp in buy_signals.index.values
    }
    sell_signals_timestamped = {
        pandas.Timestamp(timestamp).to_pydatetime(): "Sell"
        for timestamp in sell_signals.index.values
    }
    hold_signals_timestamped = {
        pandas.Timestamp(timestamp).to_pydatetime(): "Hold"
        for timestamp in hold_signals.index.values
    }

    all_signals = dict(sorted(
        {**buy_signals_timestamped, **sell_signals_timestamped, **hold_signals_timestamped}.items(),
        key=lambda x: x[0].timestamp()
    ))

    assert len(all_signals) == len(stock_data), "Not all bars were accounted for stock signals."

    return {
        k.strftime("%Y-%m-%d"): v
        for k, v in all_signals.items()
    }


if __name__ == '__main__':
    result = get_buy_sell_hold_signals(symbol="EXPE")
    pprint.pprint(result)
