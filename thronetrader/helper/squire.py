import logging
from datetime import datetime, timedelta
from typing import List, Tuple, Union

import pandas as pd
import yfinance as yf
from blockstdout import BlockPrint


def get_historical_data(symbol: str,
                        years: int = 1,
                        df: bool = False) -> Union[List[Tuple[str, float]], pd.DataFrame]:
    """Download historical stock data for a given symbol and date range.

    Args:
        symbol: Stock ticker.
        years: Number of years.
        df: Return data as a pandas DataFrame.

    Returns:
        Union[List[Tuple[str, float]], pandas.DataFrame]:
        Dataframe or Tuples of date and stock price in a list for the duration of years.
    """
    start = (datetime.now() - timedelta(days=years * 365)).strftime("%Y-%m-%d")
    end = datetime.now().strftime("%Y-%m-%d")
    try:
        with BlockPrint():
            stock_data = yf.download(symbol, start=start, end=end)
    except Exception as error:
        raise ValueError(error)
    if stock_data.empty:
        raise ValueError("Empty dataframe was downloaded.")
    if df:
        return stock_data
    return [(date.strftime("%Y-%m-%d"), close_price) for date, close_price in
            zip(stock_data.index, stock_data['Close'])]


def get_bars(symbol: str, bar_count: int, days: int) -> pd.DataFrame:
    """Download historical stock data for a given symbol and date range.

    Args:
        symbol: Stock ticker.
        bar_count: Number of bars from yfinance.
        days: Number of days to consider.

    Returns:
        pandas.DataFrame:
        Returns the historical data as a DataFrame.
    """
    try:
        with BlockPrint():
            df = yf.download(symbol, period=f"{bar_count}d", interval=f"{days}d")
        if df.empty:
            raise ValueError("Empty dataframe was downloaded.")
    except Exception as error:
        raise ValueError(error)
    return df


def classify(stock_data: pd.DataFrame, logger: logging.Logger) -> str:
    """Calculates short term moving average, long term moving average to generate the signals."""
    # Filter buy, sell, and hold signals
    buy_signals = stock_data[stock_data['buy']]
    sell_signals = stock_data[stock_data['sell']]
    hold_signals = stock_data[stock_data['hold']]

    buy_signals_timestamped = {
        pd.Timestamp(timestamp).to_pydatetime(): "buy"
        for timestamp in buy_signals.index.values
    }
    sell_signals_timestamped = {
        pd.Timestamp(timestamp).to_pydatetime(): "sell"
        for timestamp in sell_signals.index.values
    }
    hold_signals_timestamped = {
        pd.Timestamp(timestamp).to_pydatetime(): "hold"
        for timestamp in hold_signals.index.values
    }

    all_signals = dict(sorted(
        {**buy_signals_timestamped, **sell_signals_timestamped, **hold_signals_timestamped}.items(),
        key=lambda x: x[0].timestamp()
    ))

    all_signals_ct = len(all_signals)
    assert all_signals_ct == len(stock_data), "Not all data was accounted for stock signals."

    assessment = {
        "buy": round(len(buy_signals) / all_signals_ct * 100, 2),
        "sell": round(len(sell_signals) / all_signals_ct * 100, 2),
        "hold": round(len(hold_signals) / all_signals_ct * 100, 2)
    }

    for key, value in assessment.items():
        msg = f"{key} Signals: {value}%"
        logger.info(msg)

    logger.info(f"Algorithm's assessment: {max(assessment, key=assessment.get).upper()}")

    logger.debug({
        k.strftime("%A - %Y-%m-%d"): v
        for k, v in all_signals.items()
    })

    return max(assessment, key=assessment.get)
