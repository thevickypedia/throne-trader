import pandas
import yfinance


def get_financial_ratios_yfinance(symbol: str) -> pandas.DataFrame:
    """Get financial ratios for a given stock symbol using yfinance.

    Args:
        symbol: Stock ticker.

    Returns:
        pandas.DataFrame: DataFrame containing financial ratios.
    """
    try:
        financial_ratios_data = yfinance.Ticker(symbol).info
        financial_ratios = {
            'PE Ratio': financial_ratios_data.get('trailingPE', None),
            'Forward PE Ratio': financial_ratios_data.get('forwardPE', None),
            'Price to Sales Ratio': financial_ratios_data.get('priceToSalesTrailing12Months', None),
            'Price to Book Ratio': financial_ratios_data.get('priceToBook', None),
            'Dividend Yield': financial_ratios_data.get('dividendYield', None),
            'Payout Ratio': financial_ratios_data.get('payoutRatio', None),
            'Profit Margin': financial_ratios_data.get('profitMargins', None),
        }
        return pandas.DataFrame([financial_ratios])
    except Exception as error:
        raise ValueError(f"Error fetching financial ratios for {symbol}: {error}")


def predict_signals_based_on_ratios(symbol: str,
                                    pe_threshold: int = 20,
                                    pb_threshold: int = 1.5,
                                    payout_ratio_threshold_buy: int = 0.5,
                                    payout_ratio_threshold_sell: int = 0.7) -> str:
    """Predict buy/sell/hold signals based on financial ratios.

    Args:
        symbol: Stock ticker.
        pe_threshold: Maximum Price-to-Earnings (P/E) ratio considered acceptable for a "Buy" signal.
        pb_threshold: Maximum Price-to-Book (P/B) ratio considered acceptable for a "Buy" signal.
        payout_ratio_threshold_buy: Maximum payout ratio considered acceptable for a "Buy" signal.
        payout_ratio_threshold_sell: Minimum payout ratio considered acceptable for a "Sell" signal.

    Returns:
        str: Buy, Sell, or Hold signal.
    """
    financial_ratios_data = get_financial_ratios_yfinance(symbol)

    # Extract the financial ratios values from the DataFrame
    pe_ratio = financial_ratios_data['PE Ratio'].iloc[0]
    payout_ratio = financial_ratios_data['Payout Ratio'].iloc[0]
    pb_ratio = financial_ratios_data['Price to Book Ratio'].iloc[0]

    if any(map(lambda x: x is None, (pe_ratio, payout_ratio, pb_ratio))):
        print(f"PE ratio: {pe_ratio}")
        print(f"PB ratio: {pb_ratio}")
        print(f"Payout ratio: {payout_ratio}")
        return "Unpredictable"

    # Check the conditions for generating buy/sell/hold signals based on financial ratios
    if pe_ratio < pe_threshold and payout_ratio < payout_ratio_threshold_buy and pb_ratio < pb_threshold:
        return "Buy"  # All conditions met for a "Buy" signal
    elif pe_ratio > pe_threshold and payout_ratio > payout_ratio_threshold_sell and pb_ratio > pb_threshold:
        return "Sell"  # All conditions met for a "Sell" signal
    else:
        return "Hold"  # None of the conditions met for a "Buy" or "Sell" signal, so it's a "Hold" signal
