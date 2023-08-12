from typing import NoReturn

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from thronetrader.DL_algorithms import lstm_model
from thronetrader.helper import squire


class LSTMTransformer:
    """LSTMTransformer object to predict future prices using Long short-term memory (LSTM) network.

    >>> LSTMTransformer

    See Also:
        - Long short-term memory (LSTM) network is a recurrent neural network (RNN)
        - LSTM is aimed to deal with the vanishing gradient problem present in traditional RNNs.
        - | Its relative insensitivity to gap length is its advantage over other RNNs,
          | hidden Markov models and other sequence learning methods.
    """

    def __init__(self, symbol: str, epochs: int = 100, batch_size: int = 32,
                 years_to_train: int = 5, years_to_validate: int = 1):
        """Download historical stock data and instantiate LSTMTransformer object.

        Args:
            symbol: Stock ticker.
            epochs: Total number of iterations of all the training data in one cycle for training the model.
            batch_size: Number of samples propagated through the network before the model is updated.
        """
        self.symbol = symbol
        assert years_to_train > years_to_validate, \
            "training dataset should be significantly larger than the validation dataset"
        self.training_period = years_to_train
        self.validation_period = years_to_validate
        self.epochs = epochs
        self.batch_size = batch_size
        self.historical_data = self.training_dataset()

    def training_dataset(self) -> pd.DataFrame:
        """Download training dataset for the duration of training period specified.

        Returns:
            pandas.DataFrame:
            Returns the training data as a DataFrame.
        """
        return squire.get_historical_data(symbol=self.symbol, years=self.training_period, df=True)

    def validation_dataset(self) -> pd.DataFrame:
        """Download validation dataset for the duration of validation period specified.

        Returns:
            pandas.DataFrame:
            Returns the validation data as a DataFrame.
        """
        return squire.get_historical_data(self.symbol, years=self.validation_period, df=True)

    def generate_predictions(self) -> np.ndarray:
        """Prepare the data, build the LSTM model, train the model and predict future stock prices.

        Returns:
            numpy.ndarray:
            Returns the predictions as a multidimensional, homogeneous array of fixed-size items.
        """
        # Prepare the data
        x, y = lstm_model.prepare_data_lstm(self.historical_data)

        # Build the LSTM model
        model = lstm_model.build_lstm_model(input_shape=(x.shape[1], 1))

        # Train the model on the entire historical dataset
        model.fit(x, y, epochs=self.epochs, batch_size=self.batch_size, verbose=1)

        # Use the trained model to predict future stock prices
        # evaluate the model's predictive capability in a realistic scenario where it encounters new, unseen data
        future_data = self.validation_dataset()
        future_x, _ = lstm_model.prepare_data_lstm(future_data)

        # Make predictions for the future period
        return model.predict(future_x)

    def transform(self) -> np.ndarray:
        """Inverse transform the predictions to get the actual stock prices.

        Returns:
            numpy.ndarray:
            Returns the inverse of scaling predictions as a multidimensional, homogeneous array of fixed-size items.
        """
        lstm_model.scaler.fit(self.historical_data['Close'].values.reshape(-1, 1))
        future_predictions = self.generate_predictions()
        return lstm_model.scaler.inverse_transform(future_predictions)

    def plot_it(self, data: pd.Series) -> NoReturn:
        """Plot the data using matplotlib.

        Args:
            data: Takes the future prices as an argument.
        """
        plt.figure(figsize=(10, 6))
        plt.plot(data.index, data.values, label="Predicted Prices")
        actual_data = pd.Series(self.historical_data['Close'])
        plt.plot(actual_data.index, actual_data.values, label="Actual Prices")
        plt.xlabel("Date")
        plt.ylabel("Stock Price")
        plt.title("Predicted Future Stock Prices")
        plt.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def future_prices(self) -> pd.Series:
        """Get future predictions mapped to the future dates.

        Returns:
            pandas.Series:
            Returns the future predictions mapped to the dates as a Series.
        """
        transformed_future_predictions = self.transform()
        future_dates = pd.date_range(start=self.historical_data.index[-1],
                                     periods=len(transformed_future_predictions))
        future_series = pd.Series(data=transformed_future_predictions[:, 0], index=future_dates)
        self.plot_it(future_series)
        return future_series


if __name__ == '__main__':
    LSTMTransformer(symbol="GOOGL").future_prices()
