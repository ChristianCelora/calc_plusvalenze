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

def test_getSubtotal(dataset):
    coinb_reader = CoinbCsvReader()
    t = Transaction(
            coinb_reader.getDatetimeFromCoinbTimestamp(dataset["timestamp"]), 
            dataset["type"], dataset["asset"], 
            dataset["qty"], dataset["currency"], dataset["asset_price"],
            dataset["fees"], dataset["notes"]
        )

    assert t.getSubtotal() == dataset["subtotal"]

def test_getTotal(dataset):
    coinb_reader = CoinbCsvReader()
    t = Transaction(
            coinb_reader.getDatetimeFromCoinbTimestamp(dataset["timestamp"]), 
            dataset["type"], dataset["asset"], 
            dataset["qty"], dataset["currency"], dataset["asset_price"],
            dataset["fees"], dataset["notes"]
    )
                
    assert t.getTotal() == dataset["total"]

def test_getConvertedTransactionOk():
    coinb_reader = CoinbCsvReader()
    data_t = {
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
    t = Transaction(
            coinb_reader.getDatetimeFromCoinbTimestamp(data_t["timestamp"]), 
            data_t["type"], data_t["asset"], 
            data_t["qty"], data_t["currency"], data_t["asset_price"],
            data_t["fees"], data_t["notes"]
    )
                
    tc = t.getConvertedTransaction()
    assert isinstance(tc, Transaction)
    assert tc.timestamp == t.timestamp
    assert tc.type == Transaction.TYPE_BUY
    assert tc.asset == "ETH"
    assert tc.qty == 0.12126672
    assert tc.currency == t.currency
    # price = (0.003863 * 22343.59) / 0.12126672
    assert tc.asset_price == 711.764
    assert tc.fees == 0
    assert tc.notes == t.notes

def test_getConvertedTransactionErr1():
    coinb_reader = CoinbCsvReader()
    data_t = {
        "timestamp": "2020-12-17T07:47:24Z",
        "type": "Buy",
        "asset": "BTC",
        "qty": 0.004028,
        "currency": "USD",
        "asset_price": 22343.59,
        "fees": 0.86,
        "notes": "Converted 0,003863 BTC to 0,12126672 ETH",
        "subtotal": 89.14,
        "total": 90
    }
    t = Transaction(
            coinb_reader.getDatetimeFromCoinbTimestamp(data_t["timestamp"]), 
            data_t["type"], data_t["asset"], 
            data_t["qty"], data_t["currency"], data_t["asset_price"],
            data_t["fees"], data_t["notes"]
    )
                
    assert t.getConvertedTransaction() is None

def test_getConvertedTransactionErr2():
    coinb_reader = CoinbCsvReader()
    data_t = {
        "timestamp": "2020-12-17T07:47:24Z",
        "type": "Convert",
        "asset": "BTC",
        "qty": 0.004028,
        "currency": "USD",
        "asset_price": 22343.59,
        "fees": 0.86,
        "notes": "Converted 0,003863 BTC to 0,12126672",
        "subtotal": 89.14,
        "total": 90
    }
    t = Transaction(
            coinb_reader.getDatetimeFromCoinbTimestamp(data_t["timestamp"]), 
            data_t["type"], data_t["asset"], 
            data_t["qty"], data_t["currency"], data_t["asset_price"],
            data_t["fees"], data_t["notes"]
    )
                
    assert t.getConvertedTransaction() is None
    