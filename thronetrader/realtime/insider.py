from collections.abc import Generator
from typing import List, Dict, Union

from pyfinviz.insider import Insider


def get_insider(filter_option: Insider.FilterOption) -> List[Dict[str, Union[str, int, float]]]:
    """Retrieves dataframe from finviz.

    Args:
        filter_option: Takes the filter option (either buy/sell/all)

    Returns:
        List[Dict[str, Union[str, int, float]]]:
        Converts the DataFrame into a list of dictionaries and returns it.
    """
    module = Insider(filter_option=filter_option)
    return module.table_df.to_dict(orient='records')


def aggregate_data(transactions: List[Dict[str, Union[str, int, float]]]) -> List[Dict[str, Union[str, int, float]]]:
    """Aggregates the data if there are multiple transactions made by the same owner for the same ticker.

    Args:
        transactions: Transactions received from finviz.

    Returns:
        List[Dict[str, Union[str, int, float]]]:
        Aggregated transactions.
    """
    grouped_transactions = {}
    for transaction in transactions:
        # Create a key tuple based on 'Ticker', 'Owner', 'Relationship', and 'Transaction'
        key = (transaction['Ticker'], transaction['Owner'], transaction['Relationship'], transaction['Transaction'])
        if key in grouped_transactions:
            # If the key already exists, update the aggregated values
            grouped_transactions[key]['Shares'] += int(transaction['Shares'].replace(',', ''))
            grouped_transactions[key]['Value'] += int(transaction['Value'].replace(',', ''))
            # Update the value by adding the SharesTotal of the current transaction
            grouped_transactions[key]['SharesTotal'] += int(transaction['SharesTotal'].replace(',', ''))
        else:
            # If the key is not present, create a new entry in the dictionary
            grouped_transactions[key] = {
                'Ticker': transaction['Ticker'],
                'Owner': transaction['Owner'],
                'Relationship': transaction['Relationship'],
                'Transaction': transaction['Transaction'],
                'Shares': int(transaction['Shares'].replace(',', '')),
                'Value': int(transaction['Value'].replace(',', '')),
                'SharesTotal': int(transaction['SharesTotal'].replace(',', '')),
                'Date': transaction['Date']
            }
    return list(grouped_transactions.values())


def get_insider_signals(symbol: str) -> Generator[Dict[str, Union[str, int, float]]]:
    """Get insider signals for a particular transaction (if found).

    Args:
        symbol: Stock ticker.

    Yields:
        Dictionary of key value pairs with the transaction information.
    """
    insider_data = get_insider(Insider.FilterOption.ALL)
    for data in aggregate_data(transactions=insider_data):
        if data['Ticker'] == symbol.upper():
            yield data


def get_all_insider_signals() -> List[Dict[str, Union[str, int, float]]]:
    """Get ALL the insider trading information available."""
    return aggregate_data(transactions=get_insider(Insider.FilterOption.ALL))


def get_all_insider_buy() -> List[Dict[str, Union[str, int, float]]]:
    """Get the insider trading information for all BUY transactions."""
    return aggregate_data(transactions=get_insider(Insider.FilterOption.BUY))


def get_all_insider_sell() -> List[Dict[str, Union[str, int, float]]]:
    """Get the insider trading information for all SELL transactions."""
    return aggregate_data(transactions=get_insider(Insider.FilterOption.SELL))
