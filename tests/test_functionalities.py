import logging
import random
import unittest

import pandas as pd

from thronetrader.trader import Predictions, RealTimeSignals, StrategicSignals


class TestFunctionalities(unittest.TestCase):
    """Module to test all functionalities.

    >>> TestFunctionalities

    """

    TICKER = random.choice(("AAPL", "FAILED_TICKER"))
    LOGGER = logging.getLogger(__name__)
    SIGNALS = ("hold", "buy", "sell", "undetermined")
    LOGGER.propagate = False

    def test_realtime_functionalities(self):
        """Test realtime signals functionalities."""
        realtime_signals = RealTimeSignals(symbol=self.TICKER, logger=self.LOGGER)
        self.assertEqual(first=type(realtime_signals), second=RealTimeSignals)

        trading_volume = realtime_signals.get_trading_volume()
        if trading_volume:
            series1, series2 = trading_volume
            self.assertEqual(first=series1.name, second="Predicted buying volume")
            self.assertEqual(first=isinstance(series1, pd.Series), second=True)
            self.assertEqual(first=series2.name, second="Predicted selling volume")
            self.assertEqual(first=isinstance(series2, pd.Series), second=True)
        self.assertIn(member=realtime_signals.get_financial_signals(),
                      container=self.SIGNALS)
        self.assertEqual(first=isinstance(realtime_signals.get_insider_signals(), list), second=True)

    def test_strategic_signals(self):
        """Test strategic signals functionalities."""
        strategic_signals = StrategicSignals(symbol=self.TICKER, logger=self.LOGGER)
        self.assertEqual(first=type(strategic_signals), second=StrategicSignals)

        self.assertIn(member=strategic_signals.get_bollinger_bands_signals(), container=self.SIGNALS)
        self.assertIn(member=strategic_signals.get_breakout_signals(), container=self.SIGNALS)
        self.assertIn(member=strategic_signals.get_crossover_signals(), container=self.SIGNALS)
        self.assertIn(member=strategic_signals.get_macd_signals(), container=self.SIGNALS)
        self.assertIn(member=strategic_signals.get_rsi_signals(), container=self.SIGNALS)

    def test_predictions(self):
        """Test predictions functionalities."""
        predictions = Predictions(symbol=self.TICKER, logger=self.LOGGER)
        self.assertEqual(first=type(predictions), second=Predictions)

        gradient = predictions.gradient_boosting_prediction()
        assert gradient is None or (isinstance(gradient, dict) and
                                    tuple(gradient.keys()) == ('ticker', 'signal', 'signal_rate', 'recommendation'))
        linear = predictions.linear_regression_prediction()
        assert linear is None or (isinstance(gradient, dict) and
                                  tuple(gradient.keys()) == ('ticker', 'signal', 'signal_rate', 'recommendation'))
