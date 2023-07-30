import os
import sys
from typing import Tuple

import yfinance
from pandas.core.series import Series


def get_trading_volume(symbol: str, hours: int = 48, simple: bool = False) -> Tuple[Series, Series]:
    """Get assumed trading volume of a particular stock.

    Args:
        symbol: Stock ticker.
        hours: Number of hours to fetch the historical data.
        simple: Boolean flag to simply return the total volume.

    Returns:
        Returns a tuple of the Series of information for buy and sell.
    """
    # Fetch historical stock data using yfinance
    sys.stdout = open(os.devnull, 'w')  # block print
    stock_data = yfinance.download(symbol, period=f"{hours}h", interval="1h")
    sys.stdout = sys.__stdout__  # release print

    # Filter rows with non-zero buy and sell volumes
    filtered_data = stock_data[(stock_data['Volume'] > 0)]

    # Separate buy and sell volume data
    assumed_buy_volume = filtered_data[filtered_data['Close'] > filtered_data['Close'].shift(-1)]['Volume']
    assumed_sell_volume = filtered_data[filtered_data['Close'] < filtered_data['Close'].shift(-1)]['Volume']

    if simple:
        return assumed_buy_volume.sum(), assumed_sell_volume.sum()
    return assumed_buy_volume, assumed_sell_volume
