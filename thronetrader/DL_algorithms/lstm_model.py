import os
from typing import Any, Tuple

import matplotlib.pyplot as plt
import numpy
import pandas
from sklearn.preprocessing import MinMaxScaler

from thronetrader.helper import squire

scaler = MinMaxScaler(feature_range=(0, 1))


def import_tensorflow() -> Tuple['LSTM', 'Dense', 'Sequential']:
    """Imports tensorflow objects, suppressing the logger information.

    Returns:
        Tuple[LSTM, Dense, Sequential]:
        Returns a tuple of LSTM, Dense and Sequential objects.
    """
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # TensorFlow to only display warning messages (level 2) and higher
    from tensorflow.keras.layers import LSTM, Dense  # noqa: F401
    from tensorflow.keras.models import Sequential  # noqa: F401
    return LSTM, Dense, Sequential


LSTM, Dense, Sequential = import_tensorflow()


def prepare_data(data: pandas.DataFrame,
                 look_back: int = 7) -> Tuple[numpy.ndarray, numpy.ndarray]:
    """Prepare the data for LSTM model training.

    Args:
        data (pandas.DataFrame): Historical stock data as a DataFrame.
        look_back (int, optional): Number of look-back periods for the LSTM model. Defaults to 7.

    Returns:
        Tuple[numpy.ndarray, numpy.ndarray]:
        A tuple containing the prepared input data (X) and labels (y).
    """
    scaled_data = scaler.fit_transform(data['Close'].values.reshape(-1, 1))

    x_axis, y_axis = [], []
    for i in range(len(scaled_data) - look_back):
        x_axis.append(scaled_data[i:i + look_back])
        y_axis.append(scaled_data[i + look_back])

    x_axis, y_axis = numpy.array(x_axis), numpy.array(y_axis)
    x_axis = numpy.reshape(x_axis, (x_axis.shape[0], x_axis.shape[1], 1))

    return x_axis, y_axis


def build_lstm_model(input_shape: Tuple[Any, int]) -> Sequential:
    """Build the LSTM model.

    Args:
        input_shape: A tuple containing the prepared input data (X) and labels (y).

    Returns:
        Sequential:
        Sequential object.
    """
    sequential = Sequential()
    sequential.add(LSTM(units=50, return_sequences=True, input_shape=input_shape))
    sequential.add(LSTM(units=50))
    sequential.add(Dense(1))
    sequential.compile(optimizer='adam', loss='mean_squared_error')
    return sequential


if __name__ == '__main__':
    stock_data = squire.get_historical_data("AAPL", years=5, df=True)
    X, y = prepare_data(stock_data)

    train_size = int(len(X) * 0.8)
    X_train, X_test, y_train, y_test = X[:train_size], X[train_size:], y[:train_size], y[train_size:]

    model = build_lstm_model(input_shape=(X_train.shape[1], 1))
    model.fit(X_train, y_train, epochs=100, batch_size=32, validation_split=0.1, verbose=1)

    # Make predictions
    y_pred = model.predict(X_test)

    # Inverse transform predictions and original prices
    scaler.fit(stock_data['Close'].values.reshape(-1, 1))
    y_pred = scaler.inverse_transform(y_pred)
    y_test = scaler.inverse_transform(y_test)

    # Evaluate the model (you can use appropriate metrics based on your needs)
    mse = numpy.mean((y_pred - y_test) ** 2)
    print("Mean Squared Error:", mse)

    # Plot the predictions and actual prices
    plt.figure(figsize=(12, 6))
    plt.plot(stock_data.index[train_size + 7:], y_pred, label='Predictions')
    plt.plot(stock_data.index[train_size + 7:], y_test, label='Actual Prices')
    plt.legend()
    plt.show()
