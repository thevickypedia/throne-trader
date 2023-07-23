from typing import Dict

import pandas
import webull

from . import squire


def get_breakout_signals(symbol: str,
                         short_window: int = 20,
                         long_window: int = 50,
                         bar_count: int = 100) -> Dict[str, str]:
    """Get buy, sell and hold signals for a particular stock using breakout strategy.

    Args:
        symbol: Stock ticker.
        short_window: Short term moving average.
        long_window: Long term moving average.
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
    bars = webull.paper_webull().get_bars(stock=symbol, interval='d', count=bar_count)

    # Create a DataFrame from the fetched data
    stock_data = pandas.DataFrame(bars)

    # Calculate short-term (e.g., 20-day) and long-term (e.g., 50-day) moving averages
    stock_data['SMA_short'] = stock_data['close'].rolling(window=short_window).mean()
    stock_data['SMA_long'] = stock_data['close'].rolling(window=long_window).mean()

    # Generate the buy, sell, and hold signals
    stock_data['buy'] = stock_data['SMA_short'] > stock_data['SMA_long']
    stock_data['sell'] = stock_data['SMA_short'] < stock_data['SMA_long']
    stock_data['hold'] = ~(stock_data['buy'] | stock_data['sell'])

    return squire.classify(stock_data)
