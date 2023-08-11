import logging
from typing import Dict

import numpy as np
from sklearn.ensemble import GradientBoostingRegressor

from helper import squire


def gradient_boosting_prediction(symbol: str, threshold: int = None) -> Dict[str, str]:
    """Predict stock price using a Gradient Boosting Regressor model.

    Args:
        symbol: Stock ticker.
        threshold: Limit used to classify predicted price differences into trading signals based on their significance.

    See Also:
        - By adjusting the threshold value, you can control the sensitivity of the trading signals.
        - | A higher threshold would lead to fewer and stronger signals,
          | indicating more significant price movements required to trigger a signal.
        - A lower threshold would result in more frequent signals, capturing smaller price fluctuations.
        - | The choice of the threshold value depends on your risk tolerance, trading strategy,
          | and the volatility of the stock being analyzed.

    Returns:
        Dict[str, str]:
        A dictionary containing the prediction signal for the next two days.
    """
    if threshold is None:
        threshold = 5
    data = squire.get_historical_data(symbol=symbol)
    dates, close_prices = zip(*data)
    x = np.arange(len(dates)).reshape(-1, 1)
    y = np.array(close_prices)

    # Train a Gradient Boosting Regressor model
    model = GradientBoostingRegressor()
    model.fit(x, y)

    # Predict the stock prices for the next two days
    next_days = np.array([len(dates), len(dates) + 1]).reshape(-1, 1)
    predictions = model.predict(next_days)

    # Calculate the difference between the predictions
    diff = predictions[1] - predictions[0]

    # Generate the signals based on the predictions
    signals = {"ticker": symbol}
    if diff >= threshold:
        return signals | {"signal": "buy", "signal_rate": "strong buy", "recommendation": "hold"}
    elif -threshold <= diff <= threshold:
        return signals | {"signal": "hold", "signal_rate": "neutral", "recommendation": "hold"}
    else:
        return signals | {"signal": "sell", "signal_rate": "strong sell", "recommendation": "hold"}


if __name__ == '__main__':
    result = gradient_boosting_prediction("HLX")
    print(result)
