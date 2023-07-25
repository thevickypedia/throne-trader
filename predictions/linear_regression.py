from typing import Dict

import numpy as np
from sklearn.linear_model import LinearRegression

from helper import squire


def linear_regression_prediction(symbol: str) -> Dict[str, str]:
    """Predict stock price using linear regression method.

    Args:
        symbol: Stock ticker.

    Returns:
        Dict[str, str]:
        A dictionary containing the prediction signal for the next two days.
    """
    data = squire.get_historical_data(symbol=symbol)
    dates, close_prices = zip(*data)
    x = np.arange(len(dates)).reshape(-1, 1)
    y = np.array(close_prices)

    # Train a linear regression model
    model = LinearRegression()
    model.fit(x, y)

    # Predict the stock prices for the next two days
    next_days = np.array([len(dates), len(dates) + 1]).reshape(-1, 1)
    predictions = model.predict(next_days)

    # Calculate the difference between the predictions
    diff = predictions[1] - predictions[0]

    # Define a threshold for classifying the signals
    threshold = 5  # You can adjust this value as per your needs

    # Generate the signals based on the predictions
    signals = {}
    if diff >= threshold:
        signals["Buy"] = "Strong Buy (Hold)"
    elif -threshold <= diff <= threshold:
        signals["Hold"] = "Neutral"
    else:
        signals["Sell"] = "Strong Sell (Hold)"

    return signals


if __name__ == '__main__':
    result = linear_regression_prediction("HLX")
    print(result)
