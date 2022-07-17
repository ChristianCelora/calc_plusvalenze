import pytest

from datetime import datetime
from PlusvCalc.PlusVCalculator import PlusVCalculator
from PlusvCalc.Transaction import Transaction

def test_BuySellProcessTransactions():
    transactions = [
        Transaction(
            datetime(2022, 5, 29, 0, 0, 0), Transaction.TYPE_BUY, "BTC", 
            1, "USD", 19414.96, 15, "test"
        ),
        Transaction(
            datetime(2022, 5, 29, 15, 0, 0), Transaction.TYPE_BUY, "BTC", 
            1, "USD", 12500.67, 12, "test"
        ),
        Transaction(
            datetime(2022, 5, 30, 0, 0, 0), Transaction.TYPE_SELL, "BTC", 
            2, "USD", 30000.67, 27, "test"
        )
    ]

    plusv_calc = PlusVCalculator()
    t_dict = plusv_calc.processTransactions(transactions)

    assert isinstance(t_dict, dict)
    assert "BTC" in t_dict
    assert Transaction.TYPE_BUY in t_dict["BTC"]
    assert Transaction.TYPE_SELL in t_dict["BTC"]
    assert len(t_dict["BTC"][Transaction.TYPE_BUY]) == 2
    assert len(t_dict["BTC"][Transaction.TYPE_SELL]) == 1

def test_ConvertProcessTransactions():
    transactions = [
        Transaction(
            datetime(2022, 5, 29, 0, 0, 0), 
            Transaction.TYPE_CONVERT, 
            "BTC", 
            0.003863, 
            "USD", 
            19414.96, 
            15, 
            "Converted 0,003863 BTC to 0,12126672 ETH"
        )
    ]

    plusv_calc = PlusVCalculator()
    t_dict = plusv_calc.processTransactions(transactions)

    assert isinstance(t_dict, dict)
    assert "BTC" in t_dict
    assert "ETH" in t_dict
    assert Transaction.TYPE_SELL in t_dict["BTC"]
    assert Transaction.TYPE_BUY in t_dict["ETH"]

    t_btc = t_dict["BTC"][Transaction.TYPE_SELL].popitem()[1]
    t_eth = t_dict["ETH"][Transaction.TYPE_BUY].popitem()[1]
    assert isinstance(t_btc, Transaction)
    assert isinstance(t_eth, Transaction)
    assert t_btc.qty == 0.003863
    assert t_btc.asset_price == 19414.96
    assert t_btc.currency == "USD"

    assert t_eth.qty == 0.12126672
    # 19414.96 : 0.12126672 = x : 
    # x = (19414.96 * 0.003863) / 0.12126672
    assert t_eth.asset_price == 618.471 # in USD
    assert t_eth.currency == "USD"

def test_calculateBasicPlusValenzeFromDict():
    t_dict = {
        "BTC": {
            Transaction.TYPE_BUY: {
                datetime(2022, 5, 29, 0, 0, 0): Transaction(
                    datetime(2022, 5, 29, 0, 0, 0), 
                    Transaction.TYPE_BUY, 
                    "BTC", 
                    1, 
                    "USD", 
                    19414.96, 
                    15, 
                    "test"
                )
            },
            Transaction.TYPE_SELL: {
                datetime(2022, 5, 29, 15, 0, 0): Transaction(
                    datetime(2022, 5, 29, 15, 0, 0), 
                    Transaction.TYPE_BUY, 
                    "BTC", 
                    1, 
                    "USD", 
                    12500.67, 
                    12, 
                    "test"
                )
            }
        }
    }

    plusv_calc = PlusVCalculator()
    plusv = plusv_calc.calculatePlusValenzeFromDict(t_dict)

    assert isinstance(plusv, dict)
    assert "BTC" in plusv
    assert plusv["BTC"] == -6926.29

def test_calculateZeroPlusValenzeFromDict1():
    t_dict = {
        "BTC": {
            Transaction.TYPE_BUY: {
                datetime(2022, 5, 29, 0, 0, 0): Transaction(
                    datetime(2022, 5, 29, 0, 0, 0), 
                    Transaction.TYPE_BUY, 
                    "BTC", 
                    1, 
                    "USD", 
                    19414.96, 
                    15, 
                    "test"
                )
            }
        }
    }

    plusv_calc = PlusVCalculator()
    plusv = plusv_calc.calculatePlusValenzeFromDict(t_dict)

    assert isinstance(plusv, dict)
    assert "BTC" in plusv
    assert plusv["BTC"] == 0

def test_calculateZeroPlusValenzeFromDict2():
    t_dict = {
        "BTC": {
            Transaction.TYPE_BUY: {
                datetime(2022, 5, 29, 0, 0, 0): Transaction(
                    datetime(2022, 5, 29, 0, 0, 0), 
                    Transaction.TYPE_BUY, 
                    "BTC", 
                    1, 
                    "USD", 
                    19414.96, 
                    15, 
                    "test"
                ),
                datetime(2022, 5, 30, 0, 0, 0): Transaction(
                    datetime(2022, 5, 30, 0, 0, 0), 
                    Transaction.TYPE_BUY, 
                    "BTC", 
                    1, 
                    "USD", 
                    19414.96, 
                    15, 
                    "test"
                )
            }
        }
    }

    plusv_calc = PlusVCalculator()
    plusv = plusv_calc.calculatePlusValenzeFromDict(t_dict)

    assert isinstance(plusv, dict)
    assert "BTC" in plusv
    assert plusv["BTC"] == 0

def test_calculateMultipleBuysPlusValenzeFromDict1():
    t_dict = {
        "BTC": {
            Transaction.TYPE_BUY: {
                datetime(2022, 5, 28, 0, 0, 0): Transaction(
                    datetime(2022, 5, 28, 0, 0, 0), 
                    Transaction.TYPE_BUY, 
                    "BTC", 
                    1, 
                    "USD", 
                    25123.48, 
                    15, 
                    "test"
                ),
                datetime(2022, 5, 29, 0, 0, 0): Transaction(
                    datetime(2022, 5, 29, 0, 0, 0), 
                    Transaction.TYPE_BUY, 
                    "BTC", 
                    0.5, 
                    "USD", 
                    19414.96, 
                    15, 
                    "test"
                )
            },
            Transaction.TYPE_SELL: {
                datetime(2022, 5, 29, 15, 0, 0): Transaction(
                    datetime(2022, 5, 29, 15, 0, 0), 
                    Transaction.TYPE_SELL, 
                    "BTC", 
                    1, 
                    "USD", 
                    12500.67, 
                    12, 
                    "test"
                )
            }
        }
    }

    plusv_calc = PlusVCalculator()
    plusv = plusv_calc.calculatePlusValenzeFromDict(t_dict)

    assert isinstance(plusv, dict)
    assert "BTC" in plusv
    assert plusv["BTC"] == -9780.54

def test_calculateMultipleBuysPlusValenzeFromDict2():
    t_dict = {
        "BTC": {
            Transaction.TYPE_BUY: {
                datetime(2022, 5, 28, 0, 0, 0): Transaction(
                    datetime(2022, 5, 28, 0, 0, 0), 
                    Transaction.TYPE_BUY, 
                    "BTC", 
                    1, 
                    "USD", 
                    25123.48, 
                    15, 
                    "test"
                ),
                datetime(2022, 5, 29, 0, 0, 0): Transaction(
                    datetime(2022, 5, 29, 0, 0, 0), 
                    Transaction.TYPE_BUY, 
                    "BTC", 
                    0.5, 
                    "USD", 
                    19414.96, 
                    15, 
                    "test"
                ),
                # should not conisder this buy
                datetime(2022, 6, 15, 0, 0, 0): Transaction(
                    datetime(2022, 5, 29, 0, 0, 0), 
                    Transaction.TYPE_BUY, 
                    "BTC", 
                    4, 
                    "USD", 
                    49000.96, 
                    15, 
                    "test"
                )
            },
            Transaction.TYPE_SELL: {
                datetime(2022, 5, 29, 15, 0, 0): Transaction(
                    datetime(2022, 5, 29, 15, 0, 0), 
                    Transaction.TYPE_SELL, 
                    "BTC", 
                    1, 
                    "USD", 
                    12500.67, 
                    12, 
                    "test"
                )
            }
        }
    }

    plusv_calc = PlusVCalculator()
    plusv = plusv_calc.calculatePlusValenzeFromDict(t_dict)

    assert isinstance(plusv, dict)
    assert "BTC" in plusv
    assert plusv["BTC"] == -9780.54


def test_calculateMultipleSellsPlusValenzeFromDict1():
    t_dict = {
        "BTC": {
            Transaction.TYPE_BUY: {
                datetime(2022, 5, 28, 0, 0, 0): Transaction(
                    datetime(2022, 5, 28, 0, 0, 0), 
                    Transaction.TYPE_BUY, 
                    "BTC", 
                    2, 
                    "USD", 
                    25123.48, 
                    15, 
                    "test"
                ),
                datetime(2022, 5, 29, 0, 0, 0): Transaction(
                    datetime(2022, 5, 29, 0, 0, 0), 
                    Transaction.TYPE_BUY, 
                    "BTC", 
                    0.5, 
                    "USD", 
                    19414.96, 
                    15, 
                    "test"
                ),
                datetime(2022, 6, 15, 0, 0, 0): Transaction(
                    datetime(2022, 5, 29, 0, 0, 0), 
                    Transaction.TYPE_BUY, 
                    "BTC", 
                    4, 
                    "USD", 
                    49000.96, 
                    15, 
                    "test"
                )
            },
            Transaction.TYPE_SELL: {
                datetime(2022, 5, 29, 15, 0, 0): Transaction(
                    datetime(2022, 5, 29, 15, 0, 0), 
                    Transaction.TYPE_SELL, 
                    "BTC", 
                    1, 
                    "USD", 
                    12500.67, 
                    12, 
                    "test"
                ),
                datetime(2022, 6, 29, 15, 0, 0): Transaction(
                    datetime(2022, 5, 29, 15, 0, 0), 
                    Transaction.TYPE_SELL, 
                    "BTC", 
                    5, 
                    "USD", 
                    55500.50, 
                    100, 
                    "test"
                )
            }
        }
    }

    plusv_calc = PlusVCalculator()
    plusv = plusv_calc.calculatePlusValenzeFromDict(t_dict)

    assert isinstance(plusv, dict)
    assert "BTC" in plusv
    # (55500,50−49000,96) × 4 + (55500,50−19414,96) × 0,5 + (55500,50−25123,48) × 0,5
    # (12500,67−25123,48) × 1
    # minus fees
    plus_expected_mius_fees = (46606.63 - 100 - 12)
    assert plusv["BTC"] == plus_expected_mius_fees

def test_calculatePlusvalenzeForMultipleCoins():
    t_dict = {
        "BTC": {
            Transaction.TYPE_BUY: {
                datetime(2022, 5, 28, 0, 0, 0): Transaction(
                    datetime(2022, 5, 28, 0, 0, 0), 
                    Transaction.TYPE_BUY, 
                    "BTC", 
                    2, 
                    "USD", 
                    25123.48, 
                    15, 
                    "test"
                ),
            },
            Transaction.TYPE_SELL: {
                datetime(2022, 5, 29, 15, 0, 0): Transaction(
                    datetime(2022, 5, 29, 15, 0, 0), 
                    Transaction.TYPE_SELL, 
                    "BTC", 
                    1, 
                    "USD", 
                    12500.67, 
                    12, 
                    "test"
                )
            }
        },
        "ETH": {
            Transaction.TYPE_BUY: {
                datetime(2022, 5, 28, 0, 0, 0): Transaction(
                    datetime(2022, 5, 28, 0, 0, 0), 
                    Transaction.TYPE_BUY, 
                    "ETH", 
                    2, 
                    "USD", 
                    350.50, 
                    15, 
                    "test"
                ),
            },
            Transaction.TYPE_SELL: {
                datetime(2022, 5, 29, 15, 0, 0): Transaction(
                    datetime(2022, 5, 29, 15, 0, 0), 
                    Transaction.TYPE_SELL, 
                    "ETH", 
                    2, 
                    "USD", 
                    4508.00, 
                    10.50, 
                    "test"
                )
            }
        }
    }

    plusv_calc = PlusVCalculator()
    plusv = plusv_calc.calculatePlusValenzeFromDict(t_dict)

    assert isinstance(plusv, dict)
    assert "BTC" in plusv
    assert "ETH" in plusv
    # (55500,50−49000,96) × 4 + (55500,50−19414,96) × 0,5 + (55500,50−25123,48) × 0,5
    # (12500,67−25123,48) × 1
    # minus fees
    plus_expected_mius_fees = (46606.63 - 100 - 12)
    assert plusv["BTC"] == 12500.67 - 25123.48 - 12
    assert plusv["ETH"] == 4508.00*2 - 350.50*2 - 10.50