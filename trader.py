import pprint
from typing import Dict

import pandas
import webull

wb = webull.paper_webull()


def get_signals(symbol: str, bar_count: int = 100) -> Dict[str, str]:
    """Get buy, sell and hold signals for a particular stock.

    Args:
        symbol: Stock ticker.
        bar_count: Number of bars from webull.

    See Also:
        - A larger `bar_count` gives longer historical data for trend analysis.
        - A smaller count focuses on recent data for short-term signals.
        - Experiment and backtest to find the best fit for your approach.

    Returns:
        Dict[str, str]:
        A dictionary of each day's buy, sell and hold signals.
    """
    # Fetch historical stock data using the 'get_bars' method from the 'webull' package
    bars = wb.get_bars(stock=symbol, interval='d', count=bar_count)

    # Create a DataFrame from the fetched data
    stock_data = pandas.DataFrame(bars)

    # Calculate short-term (e.g., 20-day) and long-term (e.g., 50-day) moving averages
    stock_data['SMA_short'] = stock_data['close'].rolling(window=20).mean()
    stock_data['SMA_long'] = stock_data['close'].rolling(window=50).mean()

    # Generate the buy, sell, and hold signals
    stock_data['buy'] = stock_data['SMA_short'] > stock_data['SMA_long']
    stock_data['sell'] = stock_data['SMA_short'] < stock_data['SMA_long']
    stock_data['hold'] = ~(stock_data['buy'] | stock_data['sell'])

    # Filter and display the buy, sell, and holds
    buy_signals = stock_data[stock_data['buy']]
    sell_signals = stock_data[stock_data['sell']]
    hold_signals = stock_data[stock_data['hold']]

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

    all_signals_ct = len(all_signals)
    assert all_signals_ct == len(stock_data), "Not all bars were accounted for stock signals."

    assessment = {
        "Buy": round(len(buy_signals) / all_signals_ct * 100, 2),
        "Sell": round(len(sell_signals) / all_signals_ct * 100, 2),
        "Hold": round(len(hold_signals) / all_signals_ct * 100, 2)
    }
    for key, value in assessment.items():
        print(f"{key} Signals:", f"{value}%")

    print(f"\nAlgorithm's assessment: {max(assessment, key=assessment.get).upper()}\n")

    return {
        k.strftime("%A - %Y-%m-%d"): v
        for k, v in all_signals.items()
    }


if __name__ == '__main__':
    result = get_signals(symbol="EXPE", bar_count=1000)
    pprint.pprint(result, sort_dicts=False)
