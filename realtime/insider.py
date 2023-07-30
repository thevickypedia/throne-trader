from collections.abc import Generator
from typing import List, Dict, Union

from pyfinviz.insider import Insider


def get_insider():
    module = Insider(filter_option=Insider.FilterOption.ALL)
    return module.table_df.to_dict(orient='records')


def aggregate_data(transactions: List[Dict[str, Union[str, int, float]]]):
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


def get_insider_signals(ticker: str) -> Generator[Dict[str, Union[str, int, float]]]:
    insider_data = get_insider()
    for data in aggregate_data(transactions=insider_data):
        if data['Ticker'] == ticker.upper():
            yield data


def get_all_insider_signals() -> List[Dict[str, Union[str, int, float]]]:
    return aggregate_data(transactions=get_insider())


if __name__ == '__main__':
    print(list(get_insider_signals(ticker='rcg')))
