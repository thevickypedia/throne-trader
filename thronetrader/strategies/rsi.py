import logging

import pandas
import webull

from thronetrader.helper import squire

wb = webull.paper_webull()


def get_rsi_signals(symbol: str, logger: logging.Logger,
                    bar_count: int = 100) -> str:
    """Get buy, sell, and hold signals using the Relative Strength Index (RSI) strategy.

    Args:
        symbol: Stock ticker.
        logger: Logger object.
        bar_count: Number of bars from webull.

    See Also:
        - A larger `bar_count` gives longer historical data for analysis.
        - A smaller count focuses on recent data for short-term signals.
        - Experiment and backtest to find the best fit for your approach.

    Returns:
        str:
        Analysis of buy/hold/sell.
    """
    # Fetch historical stock data using the 'get_bars' method from the 'webull' package
    bars = wb.get_bars(stock=symbol, interval='d', count=bar_count)

    # Create a DataFrame from the fetched data
    stock_data = pandas.DataFrame(bars)

    # Calculate the Relative Strength Index (RSI)
    delta = stock_data['close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()
    relative_strength = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + relative_strength))

    # Generate the buy, sell, and hold signals based on RSI levels
    stock_data['buy'] = (rsi < 30)
    stock_data['sell'] = (rsi > 70)
    stock_data['hold'] = ~(stock_data['buy'] | stock_data['sell'])

    return squire.classify(stock_data, logger)
