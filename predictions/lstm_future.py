import numpy
import pandas
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import squire


def prepare_data(data: pandas.DataFrame, look_back: int = 7) -> tuple:
    """Prepare the data for LSTM model training.

    Args:
        data (pandas.DataFrame): Historical stock data as a DataFrame.
        look_back (int, optional): Number of look-back periods for the LSTM model. Defaults to 7.

    Returns:
        tuple: A tuple containing the prepared input data (X) and labels (y).
    """
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(data['Close'].values.reshape(-1, 1))

    X, y = [], []
    for i in range(len(scaled_data) - look_back):
        X.append(scaled_data[i:i + look_back])
        y.append(scaled_data[i + look_back])

    X, y = numpy.array(X), numpy.array(y)
    X = numpy.reshape(X, (X.shape[0], X.shape[1], 1))

    return X, y

def build_lstm_model(input_shape: tuple) -> Sequential:
    """Build an LSTM model for stock price prediction.

    Args:
        input_shape (tuple): Shape of the input data (X) for the LSTM model.

    Returns:
        Sequential: Compiled LSTM model.
    """
    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=input_shape))
    model.add(LSTM(units=50))
    model.add(Dense(1))

    model.compile(optimizer='adam', loss='mean_squared_error')
    return model


if __name__ == '__main__':
    # Get the historical stock data
    stock_data = squire.get_historical_data("AAPL", years=5, df=True)

    # Prepare the data
    X, y = prepare_data(stock_data)

    # Build the LSTM model
    model = build_lstm_model(input_shape=(X.shape[1], 1))

    # Train the model on the entire historical dataset
    model.fit(X, y, epochs=100, batch_size=32, verbose=1)

    # Use the trained model to predict future stock prices
    future_data = squire.get_historical_data("AAPL", years=1, df=True)  # Adjust the number of years as needed
    future_X, _ = prepare_data(future_data)

    # Make predictions for the future period
    future_predictions = model.predict(future_X)

    # Inverse transform the predictions to get the actual stock prices
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaler.fit(stock_data['Close'].values.reshape(-1, 1))
    future_predictions = scaler.inverse_transform(future_predictions)

    # Print the future predictions
    future_dates = pandas.date_range(start=stock_data.index[-1], periods=len(future_predictions))
    future_prices = pandas.Series(future_predictions[:, 0], index=future_dates)
    pandas.reset_option('all')
    print(future_prices)
