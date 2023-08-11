## Financial Ratios Analysis
- Analyzes a stock ticker based on financial ratios.
- Based on the financial data `buy`/`sell`/`hold` signals are generated per the predefined threshold values for key financial indicators.

#### Financial Data Considered:
- Price-to-earnings (P/E) ratio is the ratio for valuing a company that measures its current share price relative to its per-share earnings.
- Price-to-book value (P/B) is the ratio of the market value of a company's shares (share price) over its book value of equity.
- Payout ratio is a financial metric showing the proportion of earnings a company pays its shareholders in the form of dividends, expressed as a percentage of the company's total earnings.
  - On some occasions, the payout ratio refers to the dividends paid out as a percentage of a company's cash flow.

## Insider Trading Signals
- Get bulk buy/sell activity from insider trading collected from finviz.
- Aggregates the data if there are multiple transactions made by the same owner for the same ticker.

## Volume
- **Calculating Buy Volume**:
  - Buy volume is calculated by identifying periods where the stock's closing price is higher than the closing price of the subsequent hour.
  - This pattern suggests potential buying activity.
- **Calculating Sell Volume**:
  - Sell volume is calculated by identifying periods where the stock's closing price is lower than the closing price of the subsequent hour.
  - This pattern indicates potential selling activity.
