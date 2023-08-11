import logging

from thronetrader.helper import squire


def get_macd_signals(symbol: str,
                     logger: logging.Logger,
                     bar_count: int = 100,
                     days: int = 1) -> str:
    """Get buy, sell, and hold signals using the Moving Average Convergence Divergence (MACD) strategy.

    Args:
        symbol: Stock ticker.
        logger: Logger object.
        bar_count: Number of bars from yfinance.
        days: Number of days to consider.

    See Also:
        - A larger ``bar_count``/``days`` gives longer historical data for trend analysis.
        - A smaller count focuses on recent data for short-term signals.
        - Experiment and backtest to find the best fit for your approach.
        - | Short-term EMA (12-day EMA): A smaller span value for the short-term EMA means that it reacts more quickly
          | to recent price changes. This can lead to more frequent and sensitive crossovers between the MACD line and
          | the Signal line, resulting in more buy and sell signals. However, it might also generate more false signals
          | in volatile markets.
        - | Long-term EMA (26-day EMA): A larger span value for the long-term EMA makes it smoother and less reactive
          | to short-term price fluctuations. This helps in identifying the long-term trends in the stock's price
          | movement. However, a larger span might result in delayed signals and could miss some short-term trends.
        - | Crossover Sensitivity: When the short-term EMA crosses above the long-term EMA, it generates a bullish
          | signal (buy), and when it crosses below the long-term EMA, it generates a bearish signal (sell).
          | The span value influences how quickly these crossovers occur. A smaller span makes crossovers more
          | sensitive, potentially leading to more frequent signals.

    Returns:
        str:
        Analysis of buy/hold/sell.
    """
    # Fetch historical stock data
    stock_data = squire.get_bars(symbol=symbol, bar_count=bar_count, days=days)

    # Calculate the short-term (e.g., 12-day) and long-term (e.g., 26-day) Exponential Moving Averages (EMAs)
    stock_data['EMA_short'] = stock_data['Close'].ewm(span=12, adjust=False).mean()
    stock_data['EMA_long'] = stock_data['Close'].ewm(span=26, adjust=False).mean()

    # Calculate the MACD line and the Signal line (9-day EMA of the MACD line)
    stock_data['MACD'] = stock_data['EMA_short'] - stock_data['EMA_long']
    stock_data['Signal'] = stock_data['MACD'].ewm(span=9, adjust=False).mean()

    # Generate the buy, sell, and hold signals based on MACD crossovers
    stock_data['buy'] = stock_data['MACD'] > stock_data['Signal']
    stock_data['sell'] = stock_data['MACD'] < stock_data['Signal']
    stock_data['hold'] = ~(stock_data['buy'] | stock_data['sell'])

    return squire.classify(stock_data, logger)
