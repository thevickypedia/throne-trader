import logging
from typing import Dict

import pandas as pd
import webull

from helper import squire

wb = webull.paper_webull()


def get_bollinger_bands_signals(symbol: str, logger: logging.Logger,
                                bar_count: int = 100,
                                window: int = 20,
                                num_std: int = 2) -> str:
    """Get buy, sell, and hold signals using the Bollinger Bands strategy.

    Args:
        symbol: Stock ticker.
        logger: Logger object.
        bar_count: Number of bars from Webull.
        window: The window size for the moving average.
        num_std: The number of standard deviations for the Bollinger Bands.

    Returns:
        str:
        Analysis of buy/hold/sell.
    """
    # Fetch historical stock data using the 'get_bars' method from the 'webull' package
    bars = wb.get_bars(stock=symbol, interval='d', count=bar_count)

    # Create a DataFrame from the fetched data
    stock_data = pd.DataFrame(bars)

    # Calculate the moving average and Bollinger Bands
    stock_data['SMA'] = stock_data['close'].rolling(window=window).mean()
    stock_data['Upper Band'] = stock_data['SMA'] + stock_data['close'].rolling(window=window).std() * num_std
    stock_data['Lower Band'] = stock_data['SMA'] - stock_data['close'].rolling(window=window).std() * num_std

    # Generate the buy, sell, and hold signals based on Bollinger Bands
    stock_data['buy'] = stock_data['close'] < stock_data['Lower Band']
    stock_data['sell'] = stock_data['close'] > stock_data['Upper Band']
    stock_data['hold'] = ~(stock_data['buy'] | stock_data['sell'])

    return squire.classify(stock_data, logger)
