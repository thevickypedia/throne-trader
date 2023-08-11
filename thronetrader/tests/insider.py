import unittest

from thronetrader.realtime.insider import aggregate_data


class TestGroupTransactions(unittest.TestCase):
    """Module to test grouping transactions from finviz.

    >>> TestGroupTransactions

    """

    def test_grouping(self):
        """Test grouping functionality with sample data."""
        data = [
            {'Ticker': 'ACEL', 'Owner': 'Peterson Karl Mr.', 'Relationship': 'Director', 'Date': 'Jul 26',
             'Transaction': 'Sale', 'Cost': '11.30', 'Shares': '22,500', 'Value': '254,329',
             'SharesTotal': '2,698,145', 'SECForm4': 'Jul 28 09:20 PM'},
            {'Ticker': 'ACEL', 'Owner': 'Peterson Karl Mr.', 'Relationship': 'Director', 'Date': 'Jul 26',
             'Transaction': 'Sale', 'Cost': '11.30', 'Shares': '10,000', 'Value': '113,000',
             'SharesTotal': '2,708,145', 'SECForm4': 'Jul 28 09:20 PM'},
            {'Ticker': 'REXR', 'Owner': 'CLARK LAURA E', 'Relationship': 'Chief Financial Officer',
             'Date': 'Jul 28', 'Transaction': 'Sale', 'Cost': '54.48', 'Shares': '7,410', 'Value': '403,703',
             'SharesTotal': '2,562', 'SECForm4': 'Jul 28 09:02 PM'}
        ]

        # Expected result after grouping
        expected_result = [
            {'Ticker': 'ACEL', 'Owner': 'Peterson Karl Mr.', 'Relationship': 'Director', 'Date': 'Jul 26',
             'Transaction': 'Sale', 'Shares': 32500, 'Value': 367329, 'SharesTotal': 5406290},
            {'Ticker': 'REXR', 'Owner': 'CLARK LAURA E', 'Relationship': 'Chief Financial Officer',
             'Date': 'Jul 28', 'Transaction': 'Sale', 'Shares': 7410, 'Value': 403703,
             'SharesTotal': 2562}
        ]
        result = aggregate_data(transactions=data)
        self.assertEqual(first=result, second=expected_result)


if __name__ == '__main__':
    unittest.main()
