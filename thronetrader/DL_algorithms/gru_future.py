from typing import NoReturn

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from thronetrader.DL_algorithms import \
    gru_model  # Assuming you have a similar module for GRU model
from thronetrader.helper import squire


class GRUTransformer:
    """GRUTransformer object to predict future prices using Gated Recurrent Unit (GRU) model.

    >>> GRUTransformer

    See Also:
        - Gated Recurrent Unit (GRU) is a type of recurrent neural network (RNN)
        - GRU is designed to capture sequential patterns and relationships in data.
        - GRU has a more straightforward architecture compared to LSTM, which makes it easier to train and understand.
        - Due to its simplified design, GRU may require less computational resources and training time compared to LSTM.
    """

    def __init__(self, symbol: str, epochs: int = 100, batch_size: int = 32,
                 years_to_train: int = 5, years_to_validate: int = 1):
        """Download historical stock data and instantiate GRUTransformer object.

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
        """Prepare the data, build the GRU model, train the model and predict future stock prices.

        Returns:
            numpy.ndarray:
            Returns the predictions as a multidimensional, homogeneous array of fixed-size items.
        """
        # Prepare the data
        x, y = gru_model.prepare_data_gru(self.historical_data)

        # Build the GRU model
        model = gru_model.build_gru_model(input_shape=(x.shape[1], 1))

        # Train the model on the entire historical dataset
        model.fit(x, y, epochs=self.epochs, batch_size=self.batch_size, verbose=1)

        # Use the trained model to predict future stock prices
        # evaluate the model's predictive capability in a realistic scenario where it encounters new, unseen data
        future_data = self.validation_dataset()
        future_x, _ = gru_model.prepare_data_gru(future_data)

        # Make predictions for the future period
        return model.predict(future_x)

    def transform(self) -> np.ndarray:
        """Inverse transform the predictions to get the actual stock prices.

        Returns:
            numpy.ndarray:
            Returns the inverse of scaling predictions as a multidimensional, homogeneous array of fixed-size items.
        """
        gru_model.scaler.fit(self.historical_data['Close'].values.reshape(-1, 1))
        future_predictions = self.generate_predictions()
        return gru_model.scaler.inverse_transform(future_predictions)

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
        future_prices = pd.Series(data=transformed_future_predictions[:, 0], index=future_dates)
        self.plot_it(data=future_prices)
        return future_prices


if __name__ == '__main__':
    GRUTransformer(symbol="GOOGL").future_prices()
