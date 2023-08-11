import logging
from typing import Dict, List, Union

from thronetrader.helper.logger import default_logger
from thronetrader.helper.wrapper import wraps
from thronetrader.ML_algorithms import gradient_boosting, linear_regression
from thronetrader.realtime import financial, insider
from thronetrader.strategies import (bollinger_bands, breakout, crossover,
                                     macd, rsi)


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


class Predictions(Trader):
    """Inherited object from base class for predictions.

    >>> Predictions

    """

    @wraps(gradient_boosting.gradient_boosting_prediction)
    def gradient_boosting_prediction(self, threshold: int = None) -> Dict[str, str]:  # noqa: D102
        return gradient_boosting.gradient_boosting_prediction(symbol=self.symbol, threshold=threshold)

    @wraps(linear_regression.linear_regression_prediction)
    def linear_regression_prediction(self, threshold: int = None) -> Dict[str, str]:  # noqa: D102
        return linear_regression.linear_regression_prediction(symbol=self.symbol, threshold=threshold)


class RealTimeSignals(Trader):
    """Inherited object from base class for realtime signals.

    >>> RealTimeSignals

    """

    @wraps(financial.get_financial_signals)
    def get_financial_signals(self, pe_threshold: int = 20,  # noqa: D102
                              pb_threshold: int = 1.5,
                              payout_ratio_threshold_buy: int = 0.5,
                              payout_ratio_threshold_sell: int = 0.7) -> Union[str, None]:
        return financial.get_financial_signals(
            symbol=self.symbol, pe_threshold=pe_threshold, pb_threshold=pb_threshold,
            payout_ratio_threshold_buy=payout_ratio_threshold_buy,
            payout_ratio_threshold_sell=payout_ratio_threshold_sell,
            logger=self.logger
        )

    @wraps(insider.get_insider_signals)
    def get_insider_signals(self) -> List[Dict[str, Union[str, int, float]]]:  # noqa: D102
        return list(insider.get_insider_signals(symbol=self.symbol))


class StrategicSignals(Trader):
    """Inherited object from base class for strategic signals.

    >>> StrategicSignals

    """

    @wraps(bollinger_bands.get_bollinger_bands_signals)
    def get_bollinger_bands_signals(self, bar_count: int = 100,  # noqa: D102
                                    days: int = 1,
                                    window: int = 20,
                                    num_std: int = 2) -> str:
        return bollinger_bands.get_bollinger_bands_signals(
            symbol=self.symbol,
            bar_count=bar_count,
            days=days,
            window=window,
            num_std=num_std,
            logger=self.logger
        )

    @wraps(breakout.get_breakout_signals)
    def get_breakout_signals(self, bar_count: int = 100,  # noqa: D102
                             days: int = 1,
                             short_window: int = 20,
                             long_window: int = 50) -> str:
        return breakout.get_breakout_signals(
            symbol=self.symbol,
            bar_count=bar_count,
            days=days,
            short_window=short_window,
            long_window=long_window,
            logger=self.logger
        )

    @wraps(crossover.get_crossover_signals)
    def get_crossover_signals(self, short_window: int = 20,  # noqa: D102
                              long_window: int = 50,
                              years: int = 1) -> str:
        return crossover.get_crossover_signals(
            symbol=self.symbol,
            short_window=short_window,
            long_window=long_window,
            years=years,
            logger=self.logger
        )

    @wraps(macd.get_macd_signals)
    def get_macd_signals(self, bar_count: int = 100) -> str:  # noqa: D102
        return macd.get_macd_signals(
            symbol=self.symbol,
            logger=self.logger,
            bar_count=bar_count
        )

    @wraps(rsi.get_rsi_signals)
    def get_rsi_signals(self, bar_count: int = 100) -> str:  # noqa: D102
        return rsi.get_rsi_signals(
            symbol=self.symbol,
            logger=self.logger,
            bar_count=bar_count
        )
