import logging

from thronetrader.helper import squire


def get_breakout_signals(symbol: str, logger: logging.Logger,
                         bar_count: int = 100,
                         days: int = 1,
                         short_window: int = 20,
                         long_window: int = 50) -> str:
    """Get buy, sell and hold signals for a particular stock using breakout strategy.

    Args:
        symbol: Stock ticker.
        logger: Logger object.
        bar_count: Number of bars from yfinance.
        days: Number of days to consider.
        short_window: Short term moving average.
        long_window: Long term moving average.

    See Also:
        - A larger ``bar_count``/``days`` gives longer historical data for trend analysis.
        - A smaller count focuses on recent data for short-term signals.
        - Experiment and backtest to find the best fit for your approach.

    Returns:
        str:
        Analysis of buy/hold/sell.
    """
    # Fetch historical stock data
    stock_data = squire.get_bars(symbol=symbol, bar_count=bar_count, days=days)

    # Calculate short-term (e.g., 20-day) and long-term (e.g., 50-day) moving averages
    stock_data['SMA_short'] = stock_data['Close'].rolling(window=short_window).mean()
    stock_data['SMA_long'] = stock_data['Close'].rolling(window=long_window).mean()

    # Generate the buy, sell, and hold signals
    stock_data['buy'] = stock_data['SMA_short'] > stock_data['SMA_long']
    stock_data['sell'] = stock_data['SMA_short'] < stock_data['SMA_long']
    stock_data['hold'] = ~(stock_data['buy'] | stock_data['sell'])

    return squire.classify(stock_data, logger)
