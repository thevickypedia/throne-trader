import numpy
import pandas
import squire
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.models import Sequential


def prepare_data(data: pandas.DataFrame, look_back: int = 7):
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(data['Close'].values.reshape(-1, 1))

    X, y = [], []
    for i in range(len(scaled_data) - look_back):
        X.append(scaled_data[i:i + look_back])
        y.append(scaled_data[i + look_back])

    X, y = numpy.array(X), numpy.array(y)
    X = numpy.reshape(X, (X.shape[0], X.shape[1], 1))

    return X, y


def build_lstm_model(input_shape):
    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=input_shape))
    model.add(LSTM(units=50))
    model.add(Dense(1))

    model.compile(optimizer='adam', loss='mean_squared_error')
    return model


if __name__ == '__main__':
    stock_data = squire.get_historical_data("AAPL", years=5)
    X, y = prepare_data(stock_data)

    train_size = int(len(X) * 0.8)
    X_train, X_test, y_train, y_test = X[:train_size], X[train_size:], y[:train_size], y[train_size:]

    model = build_lstm_model(input_shape=(X_train.shape[1], 1))
    model.fit(X_train, y_train, epochs=100, batch_size=32, validation_split=0.1, verbose=1)

    # Make predictions
    y_pred = model.predict(X_test)

    # Inverse transform predictions and original prices
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaler.fit(stock_data['Close'].values.reshape(-1, 1))
    y_pred = scaler.inverse_transform(y_pred)
    y_test = scaler.inverse_transform(y_test)

    # Evaluate the model (you can use appropriate metrics based on your needs)
    mse = numpy.mean((y_pred - y_test) ** 2)
    print("Mean Squared Error:", mse)

    # Plot the predictions and actual prices
    import matplotlib.pyplot as plt

    plt.figure(figsize=(12, 6))
    plt.plot(stock_data.index[train_size + 7:], y_pred, label='Predictions')
    plt.plot(stock_data.index[train_size + 7:], y_test, label='Actual Prices')
    plt.legend()
    plt.show()
