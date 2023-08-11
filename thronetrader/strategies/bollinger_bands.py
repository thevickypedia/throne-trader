import logging

from thronetrader.helper import squire


def get_bollinger_bands_signals(symbol: str, logger: logging.Logger,
                                bar_count: int = 100,
                                days: int = 1,
                                window: int = 20,
                                num_std: int = 2) -> str:
    """Get buy, sell, and hold signals using the Bollinger Bands strategy.

    Args:
        symbol: Stock ticker.
        logger: Logger object.
        bar_count: Number of bars from Yahoo Finance.
        days: Number of days to consider.
        window: The window size for the moving average.
        num_std: The number of standard deviations for the Bollinger Bands.

    Returns:
        str:
        Analysis of buy/hold/sell.
    """
    try:
        stock_data = squire.get_bars(symbol=symbol, bar_count=bar_count, days=days)
    except ValueError as error:
        logger.error(error)
        return "undetermined"

    # Calculate the moving average and Bollinger Bands
    stock_data['SMA'] = stock_data['Close'].rolling(window=window).mean()
    stock_data['Upper Band'] = stock_data['SMA'] + stock_data['Close'].rolling(window=window).std() * num_std
    stock_data['Lower Band'] = stock_data['SMA'] - stock_data['Close'].rolling(window=window).std() * num_std

    # Generate the buy, sell, and hold signals based on Bollinger Bands
    stock_data['buy'] = stock_data['Close'] < stock_data['Lower Band']
    stock_data['sell'] = stock_data['Close'] > stock_data['Upper Band']
    stock_data['hold'] = ~(stock_data['buy'] | stock_data['sell'])

    return squire.classify(stock_data, logger)
