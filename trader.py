import strategies

if __name__ == '__main__':
    ticker = "AAPL"
    breakout = strategies.get_breakout_signals(symbol=ticker, simple=True)
    print(f"Breakout analysis: {breakout}")
    crossover = strategies.get_crossover_signals(symbol=ticker, simple=True)
    print(f"Crossover analysis: {crossover}")
    macd = strategies.get_macd_signals(symbol=ticker, simple=True)
    print(f"MACD analysis: {macd}")
    rsi = strategies.get_rsi_signals(symbol=ticker, simple=True)
    print(f"RSI analysis: {rsi}")
    bollinger_bands = strategies.get_bollinger_bands_signals(symbol=ticker, simple=True)
    print(f"Bollinger Bands' analysis: {bollinger_bands}")
