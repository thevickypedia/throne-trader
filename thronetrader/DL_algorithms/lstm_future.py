import pandas
from lstm_model import build_lstm_model, prepare_data
from sklearn.preprocessing import MinMaxScaler

from thronetrader.helper import squire

if __name__ == '__main__':
    # Get the historical stock data
    stock_data = squire.get_historical_data(symbol="AAPL", years=5, df=True)

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

    print(future_prices)
