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

