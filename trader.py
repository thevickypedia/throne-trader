import predictions
import realtime
import strategies

TICKER = "AAPL"


def demo_strategies():
    breakout = strategies.get_breakout_signals(symbol=TICKER, simple=True)
    print(f"Breakout analysis: {breakout}")
    crossover = strategies.get_crossover_signals(symbol=TICKER, simple=True)
    print(f"Crossover analysis: {crossover}")
    macd = strategies.get_macd_signals(symbol=TICKER, simple=True)
    print(f"MACD analysis: {macd}")
    rsi = strategies.get_rsi_signals(symbol=TICKER, simple=True)
    print(f"RSI analysis: {rsi}")
    bollinger_bands = strategies.get_bollinger_bands_signals(symbol=TICKER, simple=True)
    print(f"Bollinger Bands' analysis: {bollinger_bands}")


def demo_predictions():
    linear = predictions.linear_regression_prediction(symbol=TICKER)
    print(f"Linear Regression Prediction: {linear}")
    gradient = predictions.gradient_boosting_prediction(symbol=TICKER)
    print(f"Gradient Boosting Prediction: {gradient}")


def demo_realtime():
    ratios = realtime.get_financial_signals(symbol=TICKER, payout_ratio_threshold_buy=0,
                                            payout_ratio_threshold_sell=0)
    print(f"Current financials analysis: {ratios}")


def demo_insider():
    result = list(realtime.get_insider_signals(symbol=TICKER))
    print(result)


def demo_volume():
    buy_volume, sell_volume = realtime.get_trading_volume(symbol=TICKER, simple=True)
    print(f"Buy volume for {TICKER} in the last 48 hours: {buy_volume}")
    print(f"Sell volume for {TICKER} in the last 48 hours: {sell_volume}")


if __name__ == '__main__':
    demo_strategies()
    demo_predictions()
    demo_realtime()
    demo_insider()
    demo_volume()
