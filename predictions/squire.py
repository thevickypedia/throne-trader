import os
import sys
from datetime import datetime, timedelta
from typing import Tuple, List

import yfinance


def get_historical_data(symbol: str, years: int = 1) -> List[Tuple[str, float]]:
    """Download historical stock data for a given symbol and date range.

    Args:
        symbol: Stock ticker.
        years: Number of years.

    Returns:
        List[Tuple[str, float]]:
        Tuples of date and stock price in a list for the duration of years.
    """
    start = (datetime.now() - timedelta(days=years * 365)).strftime("%Y-%m-%d")
    end = datetime.now().strftime("%Y-%m-%d")
    sys.stdout = open(os.devnull, 'w')  # block print
    stock_data = yfinance.download(symbol, start=start, end=end)
    sys.stdout = sys.__stdout__  # release print
    return [(date.strftime("%Y-%m-%d"), close_price) for date, close_price in
            zip(stock_data.index, stock_data['Close'])]
