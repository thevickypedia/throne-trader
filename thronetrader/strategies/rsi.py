import logging

from thronetrader.helper import squire


def get_rsi_signals(symbol: str,
                    logger: logging.Logger,
                    bar_count: int = 100,
                    days: int = 1) -> str:
    """Get buy, sell, and hold signals using the Relative Strength Index (RSI) strategy.

    Args:
        symbol: Stock ticker.
        logger: Logger object.
        bar_count: Number of bars from yfinance.
        days: Number of days to consider.

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

    # Calculate the Relative Strength Index (RSI)
    delta = stock_data['Close'].diff()
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
