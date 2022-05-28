import pytest
from PlusvCalc.CoinbCsvReader import CoinbCsvReader
from PlusvCalc.Transaction import Transaction

def dataset1():
    return {
        "timestamp": "2020-12-04T08:29:45Z",
        "type": "Convert",
        "asset": "BTC",
        "qty": 0.003863,
        "currency": "USD",
        "asset_price": 19414.96,
        "fees": 0.78,
        "notes": "Converted 0,004028 BTC to 89,144745 USDC",
        "subtotal": 74.22,
        "total": 75
    }

def dataset2():
    return {
        "timestamp": "2020-12-17T07:47:24Z",
        "type": "Convert",
        "asset": "BTC",
        "qty": 0.004028,
        "currency": "USD",
        "asset_price": 22343.59,
        "fees": 0.86,
        "notes": "Converted 0,003863 BTC to 0,12126672 ETH",
        "subtotal": 89.14,
        "total": 90
    }

@pytest.fixture(scope='module', params=[1, 2])
def dataset(request):
    if request.param == 1:
        return dataset1()
    if request.param == 2:
        return dataset2()

def test_get_subtotal(dataset):
    coinb_reader = CoinbCsvReader()
    t = Transaction(
            coinb_reader.getDatetimeFromCoinbTimestamp(dataset["timestamp"]), 
            dataset["type"], dataset["asset"], 
            dataset["qty"], dataset["currency"], dataset["asset_price"],
            dataset["fees"], dataset["notes"]
        )

    assert t.get_subtotal() == dataset["subtotal"]

def test_get_total(dataset):
    coinb_reader = CoinbCsvReader()
    t = Transaction(
            coinb_reader.getDatetimeFromCoinbTimestamp(dataset["timestamp"]), 
            dataset["type"], dataset["asset"], 
            dataset["qty"], dataset["currency"], dataset["asset_price"],
            dataset["fees"], dataset["notes"]
    )
                
    assert t.get_total() == dataset["total"]
    