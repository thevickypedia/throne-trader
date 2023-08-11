import logging
import os.path

from predictions import gradient_boosting, linear_regression
from realtime import financial, insider
from strategies import bollinger_bands, breakout, crossover, macd, rsi


def default_logger() -> logging.Logger:
    """Generates a default console logger.

    Returns:
        logging.Logger:
        Logger object.
    """
    logger = logging.getLogger(__name__)
    logger.setLevel(level=logging.INFO)
    handler = logging.StreamHandler()
    handler.setFormatter(
        fmt=logging.Formatter(
            fmt='%(asctime)s - %(levelname)s - [%(processName)s:%(module)s:%(lineno)d] - %(funcName)s - %(message)s'
        )
    )
    logger.addHandler(hdlr=handler)
    return logger


class Trader:
    """Base class to load logger and stock ticker.

    >>> Trader

    """

    def __init__(self, symbol: str, logger: logging.Logger = None):
        """Instantiates base class.

        Args:
            symbol: Stock symbol.
            logger: Logger object.
        """
        self.symbol = symbol
        if logger:
            self.logger = logger
        else:
            self.logger = default_logger()

    def __del__(self):
        if os.path.isfile('did.bin'):
            os.remove('did.bin')


class Predictions(Trader):
    """Inherited object from base class for predictions.

    >>> Predictions

    """

    def gradient_boosting_prediction(self, threshold: int = None):
        return gradient_boosting.gradient_boosting_prediction(symbol=self.symbol, threshold=threshold)

    def linear_regression_prediction(self, threshold: int = None):
        return linear_regression.linear_regression_prediction(symbol=self.symbol, threshold=threshold)


class RealTimeSignals(Trader):
    """Inherited object from base class for realtime signals.

    >>> RealTimeSignals

    """

    def get_financial_signals(self, pe_threshold: int = 20,
                              pb_threshold: int = 1.5,
                              payout_ratio_threshold_buy: int = 0.5,
                              payout_ratio_threshold_sell: int = 0.7):
        return financial.get_financial_signals(
            symbol=self.symbol, pe_threshold=pe_threshold, pb_threshold=pb_threshold,
            payout_ratio_threshold_buy=payout_ratio_threshold_buy,
            payout_ratio_threshold_sell=payout_ratio_threshold_sell,
            logger=self.logger
        )

    def get_insider_signals(self):
        return list(insider.get_insider_signals(symbol=self.symbol))


class StrategicSignals(Trader):
    """Inherited object from base class for strategic signals.

    >>> StrategicSignals

    """

    def get_bollinger_bands_signals(self, bar_count: int = 100,
                                    window: int = 20,
                                    num_std: int = 2):
        return bollinger_bands.get_bollinger_bands_signals(
            symbol=self.symbol,
            bar_count=bar_count,
            window=window,
            num_std=num_std,
            logger=self.logger
        )

    def get_breakout_signals(self, bar_count: int = 100,
                             short_window: int = 20,
                             long_window: int = 50):
        return breakout.get_breakout_signals(
            symbol=self.symbol,
            bar_count=bar_count,
            short_window=short_window,
            long_window=long_window,
            logger=self.logger
        )

    def get_crossover_signals(self, short_window: int = 20,
                              long_window: int = 50,
                              years: int = 1):
        return crossover.get_crossover_signals(
            symbol=self.symbol,
            short_window=short_window,
            long_window=long_window,
            years=years,
            logger=self.logger
        )

    def get_macd_signals(self, bar_count: int = 100) -> str:
        return macd.get_macd_signals(
            symbol=self.symbol,
            logger=self.logger,
            bar_count=bar_count
        )

    def get_rsi_signals(self, bar_count: int = 100) -> str:
        return rsi.get_rsi_signals(
            symbol=self.symbol,
            logger=self.logger,
            bar_count=bar_count
        )
