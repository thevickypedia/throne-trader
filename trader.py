# import strategies
# import predictions
# import realtime
#
# TICKER = "AAPL"
#
#
# def demo_strategies():
#     breakout = strategies.get_breakout_signals(symbol=TICKER, simple=True)
#     print(f"Breakout analysis: {breakout}")
#     crossover = strategies.get_crossover_signals(symbol=TICKER, simple=True)
#     print(f"Crossover analysis: {crossover}")
#     macd = strategies.get_macd_signals(symbol=TICKER, simple=True)
#     print(f"MACD analysis: {macd}")
#     rsi = strategies.get_rsi_signals(symbol=TICKER, simple=True)
#     print(f"RSI analysis: {rsi}")
#     bollinger_bands = strategies.get_bollinger_bands_signals(symbol=TICKER, simple=True)
#     print(f"Bollinger Bands' analysis: {bollinger_bands}")
#
#
# def demo_predictions():
#     linear = predictions.linear_regression_prediction(symbol=TICKER)
#     print(f"Linear Regression Prediction: {linear}")
#     gradient = predictions.gradient_boosting_prediction(symbol=TICKER)
#     print(f"Gradient Boosting Prediction: {gradient}")
#
#
# def demo_realtime():
#     ratios = realtime.get_financial_signals(symbol=TICKER, payout_ratio_threshold_buy=0,
#                                             payout_ratio_threshold_sell=0)
#     print(f"Current financials analysis: {ratios}")
#
#
# if __name__ == '__main__':
#     demo_strategies()
#     demo_predictions()
#     demo_realtime()
expected_result1 = [
    {'Ticker': 'ACEL', 'Owner': 'Peterson Karl Mr.', 'Relationship': 'Director', 'Date': 'Jul 26',
     'Transaction': 'Sale', 'Cost': '11.30', 'Shares': 32500, 'Value': 367329, 'SharesTotal': 5406290},
    {'Ticker': 'REXR', 'Owner': 'CLARK LAURA E', 'Relationship': 'Chief Financial Officer',
     'Date': 'Jul 28', 'Transaction': 'Sale', 'Cost': '54.48', 'Shares': 7410, 'Value': 403703,
     'SharesTotal': 2562}
]
expected_result2 = [
    {'Ticker': 'ACEL', 'Owner': 'Peterson Karl Mr.', 'Relationship': 'Director', 'Transaction': 'Sale',
     'Shares': 32500, 'Value': 367329, 'SharesTotal': 5406290, 'Date': 'Jul 26'},
    {'Ticker': 'REXR', 'Owner': 'CLARK LAURA E', 'Relationship': 'Chief Financial Officer',
     'Transaction': 'Sale', 'Shares': 7410, 'Value': 403703, 'SharesTotal': 2562, 'Date': 'Jul 28'}
]
from deepdiff import DeepDiff

print(DeepDiff(expected_result1, expected_result2))
