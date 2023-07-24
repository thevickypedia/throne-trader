import os
import sys
from datetime import datetime, timedelta
from typing import Tuple, List, Union

import pandas
import yfinance


def get_historical_data(symbol: str,
                        years: int = 1,
                        df: bool = False) -> Union[List[Tuple[str, float]], pandas.DataFrame]:
    """Download historical stock data for a given symbol and date range.

    Args:
        symbol: Stock ticker.
        years: Number of years.
        df: Return data as a pandas DataFrame.

    Returns:
        List[Tuple[str, float]]:
        Tuples of date and stock price in a list for the duration of years.
    """
    start = (datetime.now() - timedelta(days=years * 365)).strftime("%Y-%m-%d")
    end = datetime.now().strftime("%Y-%m-%d")
    sys.stdout = open(os.devnull, 'w')  # block print
    stock_data = yfinance.download(symbol, start=start, end=end)
    sys.stdout = sys.__stdout__  # release print
    if df:
        return stock_data
    return [(date.strftime("%Y-%m-%d"), close_price) for date, close_price in
            zip(stock_data.index, stock_data['Close'])]
