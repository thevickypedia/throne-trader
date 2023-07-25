import os
import sys
from datetime import datetime, timedelta
from typing import Tuple, List, Union, Dict

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


def classify(stock_data: pandas.DataFrame, simple: bool) -> Union[Dict[str, str], str]:
    """Calculates short term moving average, long term moving average to generate the signals."""
    # Filter buy, sell, and hold signals
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
    assert all_signals_ct == len(stock_data), "Not all data was accounted for stock signals."

    assessment = {
        "Buy": round(len(buy_signals) / all_signals_ct * 100, 2),
        "Sell": round(len(sell_signals) / all_signals_ct * 100, 2),
        "Hold": round(len(hold_signals) / all_signals_ct * 100, 2)
    }

    if simple:
        return max(assessment, key=assessment.get).upper()

    for key, value in assessment.items():
        print(f"{key} Signals:", f"{value}%")

    print(f"\nAlgorithm's assessment: {max(assessment, key=assessment.get).upper()}\n")

    return {
        k.strftime("%A - %Y-%m-%d"): v
        for k, v in all_signals.items()
    }
