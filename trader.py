from strategies import get_rsi_signals, get_macd_signals, get_breakout_signals, get_crossover_signals

if __name__ == '__main__':
    ticker = "AAPL"
    get_breakout_signals(symbol=ticker)
    get_crossover_signals(symbol=ticker)
    get_macd_signals(symbol=ticker)
    get_rsi_signals(symbol=ticker)
